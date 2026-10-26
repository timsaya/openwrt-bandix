# openwrt-bandix

English | [简体中文](README.zh.md)


[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

## Introduction

openwrt-bandix is a dependency package for luci-app-bandix, providing core functionality for network traffic monitoring.

## Installation

### Install from Release

1. Visit the [Release page](https://github.com/timsaya/openwrt-bandix/releases) to download the ipk file suitable for your device architecture

2. Upload the downloaded ipk file to your OpenWrt device

3. Install:

```bash
opkg install /path/to/bandix_xxx.ipk
```

## License

This project is licensed under the Apache-2.0 License.

## Maintainer

- [timsaya](https://github.com/timsaya)
## GeoIP support

New service binaries provide optional GeoIP management under LuCI's Connection
Monitor Settings. Production databases are downloaded separately. Configure
`bandix.connections.geoip_dir` (default `/usr/share/bandix-geoip`) for persistent
or external storage. The directory is not added to sysupgrade retention by this
package. The init script detects `--geoip-dir` support and remains compatible
with older published binaries.

To package an unreleased service binary in an SDK without changing published
archive URLs or hashes:

```sh
make package/feeds/local/openwrt-bandix/compile V=s \
    BANDIX_LOCAL_BINARY=/absolute/path/to/new/bandix
```

Use a binary matching the SDK architecture and install it with the updated LuCI
package. The normal build continues to use the existing published service release.

## Listening address

Settings → Basic Settings → Listen Address configures `bandix.general.host`.
The default is `127.0.0.1`; IPv4 and IPv6 addresses are supported, including
`0.0.0.0` and `::` for all interfaces. Save & Apply restarts the service.
LuCI automatically follows the configured address and uses loopback for wildcard
listeners. The HTTP API has no authentication; restrict non-loopback access to trusted clients.
Changing the address requires a service binary supporting `--host`. Existing
configurations without this option keep the loopback default.
