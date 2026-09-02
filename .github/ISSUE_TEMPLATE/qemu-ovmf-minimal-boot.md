---
name: "help wanted: QEMU/OVMF minimal boot design review"
about: Review the serial-boot-only design for the x86_64 QEMU/OVMF preview.
title: "help wanted: QEMU/OVMF minimal boot design review"
labels: "help wanted, qemu, design"
---

## Goal

Enable `routeros-x86_64-uefi-preview.img` to boot in x86_64 QEMU/OVMF and reach a serial-console login prompt.

## Acceptance criteria

- [ ] The proposal specifies a GPT/ESP/rootfs layout and the boot path to the kernel/initramfs.
- [ ] It documents the serial-console configuration and how the login prompt is checked.
- [ ] QEMU uses an explicit repository-managed COW overlay only.
- [ ] It rejects host block-device input and does not alter host UEFI variables.
- [ ] It lists the source-lock, toolchain, rootfs, layout, and boot evidence needed before success is claimed.

## Out of scope

Physical PC/USB boot, Secure Boot, Wi-Fi, AX23V flashing, Web UI, updates, and multi-NIC networking.
