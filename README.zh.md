# openwrt-bandix

[English](README.md) 简体中文

[![许可证](https://img.shields.io/badge/许可证-Apache--2.0-blue.svg)](LICENSE)

## 简介

openwrt-bandix 是 luci-app-bandix 的依赖包，提供网络流量监控的核心功能。

## 安装方法

### 从 Release 下载安装

1. 前往 [Release 页面](https://github.com/timsaya/openwrt-bandix/releases) 下载适合您设备架构的 ipk 文件

2. 将下载的 ipk 文件上传到您的 OpenWrt 设备

3. 安装：

```bash
opkg install /path/to/bandix_xxx.ipk
```

## 许可证

本项目采用 Apache-2.0 许可证。

## 维护者

- [timsaya](https://github.com/timsaya)
## GeoIP 数据库支持

新版 Bandix 服务端支持 GeoIP 数据库管理。LuCI 入口在**设置 → 连接监控设置**。
包本身不携带数据库，下载后由 Bandix 校验、加载，并保存启用状态和版本。

数据库目录通过 `/etc/config/bandix` 配置：

```uci
config bandix 'connections'
    option enabled '1'
    option geoip_dir '/usr/share/bandix-geoip'
```

支持使用外置磁盘目录。数据库目录未加入本包的 sysupgrade 保留列表，升级后可以重新下载；
如需保留数据库，请选择合适的外置持久存储或自行配置备份。
启动脚本会检测服务端是否支持 `--geoip-dir`，兼容不含 GeoIP 功能的旧二进制。

### 打包尚未发布的服务端

当前包默认仍使用 Makefile 内已有的公开发布版及其校验值。打包本地新服务端时，在 SDK 中指定：

```sh
make package/feeds/local/openwrt-bandix/compile V=s \
    BANDIX_LOCAL_BINARY=/absolute/path/to/new/bandix
```

二进制必须与 SDK 的设备架构匹配。此参数跳过公开归档的下载，直接将本地二进制装入 ipk/apk；
可与新版 luci-app-bandix 一起安装验证，不需要先发布 GitHub release。

## 监听地址

在**设置 → 基本设置 → 监听地址**中配置 `bandix.general.host`，默认为 `127.0.0.1`。
支持 IPv4 和 IPv6；`0.0.0.0`、`::` 分别监听所有 IPv4、IPv6 接口。保存并应用后重启服务。
LuCI 会自动使用配置的地址；监听所有接口时，通过对应的 loopback 地址访问。
HTTP API 不提供身份认证，非 loopback 访问应限制在可信客户端范围。
修改监听地址需要支持 `--host` 的新版服务端；旧配置缺少此项时仍使用默认值。
