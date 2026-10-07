import json
import os
import glob
import pytest
import yaml
import jsonschema

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTITIONS_SCHEMA_PATH = os.path.join(REPO_ROOT, "schemas", "partitions.schema.json")
AX23V_PARTITIONS_PATH = os.path.join(
    REPO_ROOT, "devices", "tplink", "archer-ax23v-v1", "partitions.yaml"
)
AX23V_DEVICE_PATH = os.path.join(
    REPO_ROOT, "devices", "tplink", "archer-ax23v-v1", "device.yaml"
)


def load_schema():
    with open(PARTITIONS_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_number(val):
    if isinstance(val, int):
        return val
    if isinstance(val, str) and val.startswith("0x"):
        return int(val, 16)
    return int(val)


def validate_partitions_contract(data, device_id="ax23v-v1"):
    schema = load_schema()
    jsonschema.validate(instance=data, schema=schema)

    total_bytes = parse_number(data["media"]["total_bytes"])
    partitions = data["partitions"]
    top_preserve = set(data.get("preserve", []))
    top_replaceable = set(data.get("replaceable", []))

    # Check partition name uniqueness
    names = [p["name"] for p in partitions]
    if len(names) != len(set(names)):
        raise ValueError("Partition names must be unique")

    # Disallowed physical partitions for ax23v-v1
    if device_id == "ax23v-v1":
        forbidden = {"factory", "art", "u-boot-env"}
        found_forbidden = set(names).intersection(forbidden)
        if found_forbidden:
            raise ValueError(f"Forbidden physical partitions found on {device_id}: {found_forbidden}")

    p_preserve = set()
    p_replaceable = set()
    spans = []

    for p in partitions:
        p_name = p["name"]
        preservation = p.get("preservation")
        if preservation not in ("preserve", "replaceable"):
            raise ValueError(f"Partition {p_name} has invalid preservation status: {preservation}")

        if preservation == "preserve":
            p_preserve.add(p_name)
        else:
            p_replaceable.add(p_name)

        offset = parse_number(p["offset"])
        size = parse_number(p["size"])
        if offset < 0 or size <= 0:
            raise ValueError(f"Partition {p_name} has invalid offset/size")

        end = offset + size
        if end > total_bytes:
            raise ValueError(
                f"Partition {p_name} bounds ({hex(offset)}..{hex(end)}) exceed media size ({hex(total_bytes)})"
            )

        spans.append((offset, end, p_name))

        # Check NVMEM
        if "nvmem" in p:
            for nv in p["nvmem"]:
                nv_offset = parse_number(nv["offset"])
                nv_length = parse_number(nv["length"])
                if nv_offset < 0 or nv_length <= 0:
                    raise ValueError(f"NVMEM {nv['name']} has invalid offset/length")
                if nv_offset + nv_length > size:
                    raise ValueError(
                        f"NVMEM {nv['name']} ({hex(nv_offset)}+{hex(nv_length)}) exceeds partition {p_name} size ({hex(size)})"
                    )

    # Overlap check
    spans.sort(key=lambda x: x[0])
    for i in range(len(spans) - 1):
        curr_off, curr_end, curr_name = spans[i]
        next_off, next_end, next_name = spans[i + 1]
        if curr_end > next_off:
            raise ValueError(f"Partitions overlap: {curr_name} ends at {hex(curr_end)} but {next_name} starts at {hex(next_off)}")

    # Preservation policy consistency
    if top_preserve != p_preserve:
        raise ValueError(f"Top-level preserve list {top_preserve} does not match partition classifications {p_preserve}")
    if top_replaceable != p_replaceable:
        raise ValueError(f"Top-level replaceable list {top_replaceable} does not match partition classifications {p_replaceable}")

    # AX23 v1 specific classifications
    if device_id == "ax23v-v1":
        if "firmware" not in p_replaceable:
            raise ValueError("'firmware' must be classified as replaceable")
        expected_preserved = {"u-boot", "config", "tplink", "radio"}
        missing_preserved = expected_preserved - p_preserve
        if missing_preserved:
            raise ValueError(f"Missing required preserved partitions for {device_id}: {missing_preserved}")


def test_canonical_ax23v_v1_partitions_pass():
    with open(AX23V_PARTITIONS_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    validate_partitions_contract(data, device_id="ax23v-v1")


def test_canonical_ax23v_v1_device_pass():
    with open(AX23V_DEVICE_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data["schema"] == "router-platform.device/v1"
    assert data["id"] == "ax23v-v1"
    assert data["status"] == "discovery"
    assert data["preserve"] == ["u-boot", "config", "tplink", "radio"]
    assert data["image"].get("rootfs") in (None, "unset")


# Negative Tests

def get_base_ax23v_data():
    with open(AX23V_PARTITIONS_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_overlapping_partitions_fail():
    data = get_base_ax23v_data()
    # Modify firmware offset to overlap with u-boot
    data["partitions"][1]["offset"] = "0x020000"
    with pytest.raises(ValueError, match="Partitions overlap"):
        validate_partitions_contract(data, device_id="ax23v-v1")


def test_partition_outside_media_bounds_fail():
    data = get_base_ax23v_data()
    # Increase radio partition size beyond total_bytes
    data["partitions"][4]["size"] = "0x020000"
    with pytest.raises(ValueError, match="exceed media size"):
        validate_partitions_contract(data, device_id="ax23v-v1")


def test_missing_preservation_classification_fail():
    data = get_base_ax23v_data()
    del data["partitions"][0]["preservation"]
    with pytest.raises((jsonschema.ValidationError, KeyError)):
        validate_partitions_contract(data, device_id="ax23v-v1")


def test_contradictory_preservation_policy_fail():
    data = get_base_ax23v_data()
    # Change top-level preserve list to exclude radio
    data["preserve"] = ["u-boot", "config", "tplink"]
    with pytest.raises(ValueError, match="Top-level preserve list"):
        validate_partitions_contract(data, device_id="ax23v-v1")


def test_unknown_preservation_region_fail():
    data = get_base_ax23v_data()
    data["partitions"][0]["preservation"] = "invalid_status"
    with pytest.raises(jsonschema.ValidationError):
        validate_partitions_contract(data, device_id="ax23v-v1")


def test_firmware_incorrectly_marked_preserve_fail():
    data = get_base_ax23v_data()
    data["partitions"][1]["preservation"] = "preserve"
    data["replaceable"] = []
    data["preserve"] = ["u-boot", "firmware", "config", "tplink", "radio"]
    with pytest.raises(ValueError, match="'firmware' must be classified as replaceable"):
        validate_partitions_contract(data, device_id="ax23v-v1")


def test_uboot_incorrectly_marked_replaceable_fail():
    data = get_base_ax23v_data()
    data["partitions"][0]["preservation"] = "replaceable"
    data["replaceable"] = ["firmware", "u-boot"]
    data["preserve"] = ["config", "tplink", "radio"]
    with pytest.raises(ValueError, match="Missing required preserved partitions"):
        validate_partitions_contract(data, device_id="ax23v-v1")


def test_factory_or_art_introduced_as_physical_partitions_fail():
    data = get_base_ax23v_data()
    # Add factory partition
    data["partitions"].append({
        "name": "factory",
        "offset": "0xfe0000",
        "size": "0x010000",
        "preservation": "preserve"
    })
    data["preserve"].append("factory")
    with pytest.raises(ValueError, match="Forbidden physical partitions found"):
        validate_partitions_contract(data, device_id="ax23v-v1")


def test_invalid_nvmem_range_fail():
    data = get_base_ax23v_data()
    # Set config macaddr length exceeding config partition size (0x10000)
    data["partitions"][2]["nvmem"][0]["length"] = "0x20000"
    with pytest.raises(ValueError, match="exceeds partition config size"):
        validate_partitions_contract(data, device_id="ax23v-v1")
