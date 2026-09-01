# Archer AX23V v1 consumer contract

This directory is the canonical platform-data unit for `ax23v-v1`.

## Owned here

- board identity, SoC and physical-interface observations;
- GPIO, NVMEM and radio capability records, including unknown values;
- partition preservation policy and storage/capacity evidence;
- non-authorizing regulatory profile input and the evidence register.

## Not owned here

- package selection, kernel configuration, source locks, root filesystem,
  image-layout implementation, image signing, or release artifacts.

## Required consumer behavior

A consumer must resolve this directory explicitly, validate that `device.yaml`
has `id: ax23v-v1`, and retain every safety state without promotion. Missing
platform data is an error; it must not fall back to a copied device definition.
`discovery`, `unverified`, `unset`, and `observed` prohibit image assembly,
flash authorization, and RF authorization. The TP-Link `special_id` is a
distribution identifier, not regulatory evidence.

The data is intentionally compatible with a manifest-v2 release consumer only
as input: it neither declares an artifact nor sets `flashable: true`.
