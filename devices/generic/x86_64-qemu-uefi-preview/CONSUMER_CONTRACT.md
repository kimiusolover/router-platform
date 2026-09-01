# x86_64 QEMU/OVMF preview consumer contract

This is the canonical platform-data unit for `x86_64-qemu-uefi-preview`.
It applies only to a virtual disk in QEMU/OVMF. It is not a physical-PC,
USB-boot, Secure-Boot, Wi-Fi, or host-block-device profile.

Consumers must preserve `deployment: qemu-ovmf-only`, the two host preservation
entries, and `status: discovery` / `unverified`. These prohibit image release
and VM execution until independent image-layout and QEMU E2E evidence exists.
The only permitted execution model is an explicit, repository-managed
copy-on-write overlay of a verified preview image; no host disk input is valid.

Kernel configuration, package composition, source locks, image layout,
signing, and release artifacts remain owned by `router-firmware`.
