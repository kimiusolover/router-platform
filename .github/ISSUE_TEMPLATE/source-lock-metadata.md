---
name: "good first issue: verify source lock metadata"
about: Verify immutable input metadata for the QEMU preview without downloading during a build.
title: "good first issue: verify source lock metadata"
labels: "good first issue, source-lock"
---

## Scope

Review one proposed source-lock record used by the x86_64 QEMU/OVMF preview.

## Acceptance criteria

- [ ] Version, exact archive filename, HTTPS origin URL, and lowercase SHA-256 are recorded.
- [ ] The archive is an immutable upstream release input; it is not `latest`, a moving branch,
      a documentation URL, or a mirror chosen by the build.
- [ ] The exact archive exists in the local source cache and its SHA-256 matches.
- [ ] The record becomes `status: locked` only after the above evidence is reviewable.
- [ ] Build-time network retrieval is neither added nor required.

## Out of scope

Do not change AX23V platform facts, request device dumps, publish artifacts, or enable hardware/RF action.
