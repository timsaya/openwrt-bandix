include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.12.12
PKG_RELEASE:=1

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.12.12
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=9d3c0266e966b879dd5a1a4471fc5e37925c2d5fb006865e4d4ea53b68d652cc
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
		PKG_HASH:=f8f097dba4978bc6906741304bff4922f20a70d0fd998fffa3a23e2dd67c4d30
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=cc8966d7959d62e575c8fba3ddd38de50be7a8064bba5316e5c3076b141fe90e
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=5e669f7a7e8094ea34c554945a35e7787458905c5c5b0001043837bb4ebc2b6b
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=8a05b351259e4ff83589cdbcb7c40c06b59e7407b49e207c126caf01d8a77a0b
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=d35e43ff355b0ea0d197c500565a0cdafebeb60f173e38115280cc5ae7057563
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=07049c912b0be9904aa32a1e62a68d533f8a752152ccd169b293f251a4e75d1e
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=5d0a3c20a060d2ecbad2c3bd200cfddd060f28334d2c68e9ae24142e893b4a87
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=f58d1b8dfb49d01573ee585f525594bc316399e1d0310dce6e0989ddaec17d92
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=1428ac0a492e4944c40f641bffccb9fe1cb68cc068edec328ab4ae93267de3d3
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=a951a64b835fc0eb9c53b3166154fbc067b85f9e6a4a5d6ebdd4282ef7b492dd
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
