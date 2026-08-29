# router-platform

Hardware and jurisdiction-specific product definitions for supported routers.

## Boundary

This repository owns device manifests, device-tree and board overlays, flash
layout evidence, GPIO/radio descriptions, and certification profiles. It does
not build images, publish packages, or invent hardware or certification facts.

The initial target will be migrated from `router-firmware/devices/ax23v-v1`
only after its files are classified as platform data. Until then, that existing
repository remains the authoritative source.

## Layout

```
devices/<vendor>/<model>/
  device.toml
  dts/
  flash/
  gpio/
  radio/
  certification/<jurisdiction>/
schemas/
```
