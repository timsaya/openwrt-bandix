#!/bin/bash
# dependent: curl jq
#

export CURDIR="$(cd "$(dirname "$0")"; pwd)"

# func <user> <repo>
github_getLatest() {
	curl -sSL "https://api.github.com/repos/$1/$2/releases/latest"
}

LATEST_INFO="$(github_getLatest timsaya bandix)"

# version check
LATEST_VERSION="$(jq '.tag_name' -r <<< "$LATEST_INFO" | sed 's|^v||')"
[ -n "$LATEST_VERSION" ] || exit 1
RUST_BANDIX_VERSION="$(sed -n 's|RUST_BANDIX_VERSION:=||p' "$CURDIR/Makefile")"
[ "$RUST_BANDIX_VERSION" != "$LATEST_VERSION" ] || exit 0

# update PKG_HASH
# 从 Makefile 中提取 $ARCH 并将它们按字符多寡降序排列, 用于进行模糊匹配
ARCHS="$(sed -En '/ifeq \(\$\((ARCH|ARM_CPU_TYPE)\),.+\)$/{s|.+,([^\)]+).*|\1|;p}' "$CURDIR/Makefile" | sort -r)"
for (( i=0; i<$(jq -r '.assets | length' <<< "$LATEST_INFO"); i++ )); do
	name=$(jq -r '.assets['$i'].name | select(contains("bandix"))' <<< "$LATEST_INFO")
	[ -n "$name" ] || continue
	browser_download_url=$(jq -r '.assets['$i'].browser_download_url' <<< "$LATEST_INFO")
	digest_type=$(jq -r '.assets['$i'].digest' <<< "$LATEST_INFO" | cut -f1 -d':')
	digest=$(jq -r '.assets['$i'].digest' <<< "$LATEST_INFO" | cut -f2 -d':')

	# 精简的 Github Assets name
	arch="$(awk -F'-' '{ printf "%s-%s", $1, $NF }' <<< "$(sed "s|bandix-$LATEST_VERSION-||;s|\.tar\..*||" <<< "$name")")"
	for ARCH in $ARCHS; do
		# 使用从 Makefile 中提取的 $ARCH 对精简的 Github Assets name 进行模糊匹配
		! grep -Eq "$(sed 's|-armel|-.*abi$|;s|-armhf|-.*abihf$|' <<< "$ARCH")" <<< "$arch" || break
		unset ARCH
	done
	line="$(sed -En "/ifeq \(\\$\((ARCH|ARM_CPU_TYPE)\),$ARCH\)$/=" "$CURDIR/Makefile")"
	[ -n "$line" ] || continue

	if [[ "$digest_type" != "sha256" ]]; then
		digest="$(curl -fsSL "$browser_download_url" | sha256sum | awk '{print $1}')"
	fi
	sed -i "$((line + 1))s|\(PKG_HASH:=\).*|\1$digest|" "$CURDIR/Makefile"
done

# update version
sed -i "s|\(RUST_BANDIX_VERSION:=\).*|\1$LATEST_VERSION|" "$CURDIR/Makefile"
