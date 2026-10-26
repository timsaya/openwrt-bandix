include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.12.11
PKG_RELEASE:=3

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.12.11
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=b921b0902501799c32ce83e27c5031a20151b5005082115096438caa40efb42a
else ifeq ($(ARCH),arm) # update.sh skip this tag, do not delete this comment
	# Ref https://github.com/openwrt/packages/blob/master/lang/rust/rust-values.mk

	ARM_CPU_TYPE:=arm-armel
	ifeq ($(CONFIG_arm_v6)$(CONFIG_arm_v7),)
		ARM_CPU_TYPE:=$(subst arm-,armv5te-,$(ARM_CPU_TYPE))
	else ifeq ($(CONFIG_arm_v7),y)
		ARM_CPU_TYPE:=$(subst arm-,armv7-,$(ARM_CPU_TYPE))
	endif

	ifeq ($(CONFIG_HAS_FPU),y)
		ARM_CPU_TYPE:=$(subst -armel,-armhf,$(ARM_CPU_TYPE))
	endif

	ifeq ($(ARM_CPU_TYPE),arm-armel)
		PKG_HASH:=c6a8b8aab33f273108fec9aa809c37c82f6b09c1541fbd54e0d6ee81700760ed
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=3600e5f5a1a6c79fd013ffab298cf0836fbe76521c700f3c0a3ddf82588a6611
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=eac3e4c80e00ef6c1e24879f5209c9582cf8b1e60a485f8dcb879be8db0d85ed
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=2e24acf374abf513b5a99a118bb43b45d4a3b5f459bf1b649d765f990d0ad4cc
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=6597d3479e48171e44d33eac632e5dcfe61e64899badfa008571c09d99304062
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=1401d9b2404ba532eff71807c4247106f9fa72bc43de100321ddd0da68ac154d
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=a3cb0e4ed2c16dbf092970cf35e46b1159bbdcdba7a3a58b7d4b9b48c55c42ff
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=66cfd2c58cb60d28ec676d7676629d60b553de0a48f349f932faa76d86ed1f93
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=7235709bf60785940f0869ee35a551648717dbcda7d9767a371a65995cbda7fc
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=de7526fc165a61c1928d95345a03f5450fc3e2e2596bc406e285b59f338d115f
else
	PKG_HASH:=dummy
endif

# Build an unreleased service with an SDK without changing published hashes:
# make package/bandix/compile BANDIX_LOCAL_BINARY=/absolute/path/to/bandix
BANDIX_LOCAL_BINARY?=
ifneq ($(strip $(BANDIX_LOCAL_BINARY)),)
  PKG_SOURCE:=
  PKG_SOURCE_URL:=
  PKG_FILE_DEPENDS+=$(BANDIX_LOCAL_BINARY)
endif

define Package/$(PKG_NAME)
	SECTION:=net
	CATEGORY:=Network
	TITLE:=Bandix - Network traffic monitoring tool
	DEPENDS:=+zoneinfo-all +conntrack +iw
endef

define Package/$(PKG_NAME)/description
	Bandix core service for network traffic monitoring
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)/bin
	$(if $(strip $(BANDIX_LOCAL_BINARY)),$(INSTALL_BIN) "$(BANDIX_LOCAL_BINARY)" $(PKG_BUILD_DIR)/bin/bandix,gzip -dc "$(DL_DIR)/$(PKG_SOURCE)" | tar -C $(PKG_BUILD_DIR)/bin --strip-components=1 -xf -)
	$(Build/Patch)
endef

define Build/Compile
	# nothing to do
endef

define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/bin/bandix $(1)/usr/bin/

	# 添加启动脚本和配置文件
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_BIN) ./files/bandix.init $(1)/etc/init.d/bandix

	# 安装配置文件
	$(INSTALL_DIR) $(1)/usr/share/bandix
	$(INSTALL_CONF) ./files/bandix.config $(1)/etc/config/bandix
	
	# 配置 sysupgrade 保留列表
	$(INSTALL_DIR) $(1)/lib/upgrade/keep.d
	$(INSTALL_DATA) ./files/bandix.keep $(1)/lib/upgrade/keep.d/bandix
endef

define Package/$(PKG_NAME)/conffiles
/etc/config/bandix
endef

$(eval $(call BuildPackage,bandix))
