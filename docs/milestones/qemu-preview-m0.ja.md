# QEMU preview: serial boot only (Milestone 0)

## 目的

`routeros-x86_64-uefi-preview.img` を x86_64 QEMU/OVMF の仮想ディスクとして
起動し、serial console からログインできるようにする。これは AX23V、物理 PC、USB、
Secure Boot、Wi-Fi、更新、Web UI を対象にしない隔離された preview である。

## 完了条件

- 成果物名は厳密に `routeros-x86_64-uefi-preview.img` である。
- QEMU は OVMF とリポジトリ管理の COW overlay を使い、ホストの block device と
  UEFI variable store を入力に受け取らない。
- UEFI がディスクから起動し、serial console にログイン可能なプロンプトが現れる。
- 実行ログは QEMU、OVMF、イメージの識別子、実行コマンド、ログイン確認を記録する。
- source lock、x86_64 toolchain、rootfs、GPT/ESP layout の証拠が全て `locked` になる
  までは build が fail closed で停止する。

## この Milestone に入れないもの

- WAN/LAN、DHCP、DNS、NAT/firewall の E2E
- Jool/NAT64、hostapd、Web UI、更新・rollback
- AX23V の image assembly、flash、RF 動作、実機の変更
- physical PC、USB boot、Secure Boot

## 作業分解

1. source lock metadata を、正確な archive URL・version・SHA-256・ローカル cache
   一致を添えて review する。
2. QEMU/OVMF 最小 boot の image layout と serial console 設計を review する。
3. 実イメージの COW-only QEMU 起動を記録・再現可能にする。

次の Milestone で、二つの virtual NIC による
`networkd → Kea DHCP → Unbound DNS → nftables NAT/firewall` の E2E を扱う。
AX23V は別レーンの非破壊観測だけを扱い、未確認の値を補完しない。
