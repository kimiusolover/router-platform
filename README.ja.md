# router-platform

[English README](README.md)

対応ルーターのハードウェア・管轄固有の製品定義を管理します。機種マニフェスト、デバイスツリー、ボードオーバーレイ、フラッシュ配置の根拠、GPIO・無線の記述、認証プロファイルが対象です。

イメージの生成、パッケージ公開、未確認のハードウェアまたは認証事実の推測は行いません。

## 現在の正本

AX23V v1 のプラットフォーム定義の正本は
`devices/tplink/archer-ax23v-v1/` です。ここにはボード識別、配線、
GPIO、NVMEM／無線の未確認境界、パーティション保全方針、ストレージ観測、
および能力値を置きます。

`router-firmware` はこのディレクトリを消費し、パッケージ構成、カーネル設定、
ソースロック、rootfs とイメージ組み立てだけを管理します。消費側がこの
リポジトリを見つけられない場合は失敗しなければならず、旧来のコピーへ
フォールバックしてはなりません。詳細なファイル境界は
`devices/tplink/archer-ax23v-v1/CONSUMER_CONTRACT.md` を参照してください。

x86_64 の QEMU/OVMF 専用 preview は
`devices/generic/x86_64-qemu-uefi-preview/` が正本です。これは物理 PC、USB、
Secure Boot、またはホストディスクへの書込みを対象にしません。

詳細は [POLICY.ja.md](POLICY.ja.md) を参照してください。
