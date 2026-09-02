---
name: "help wanted: two-NIC DHCP/DNS/firewall E2E test plan"
about: Define the next-milestone QEMU network test without broadening Milestone 0.
title: "help wanted: two-NIC DHCP/DNS/firewall E2E test plan"
labels: "help wanted, qemu, testing"
---

## Goal

Design the next milestone's two-virtual-NIC E2E test:
`networkd → Kea DHCP → Unbound DNS → nftables NAT/firewall`.

## Acceptance criteria

- [ ] The plan identifies the WAN and LAN virtual NIC roles, addresses, and test client topology.
- [ ] It gives observable checks for DHCP lease, DNS resolution, outbound NAT, and firewall policy.
- [ ] The harness has no host block-device input and leaves the base image unchanged.
- [ ] Failure logs are sufficient to distinguish each integration boundary.

## Out of scope

This is not Milestone 0, and does not add Jool/NAT64, hostapd, Web UI, AX23V, or physical hardware.
