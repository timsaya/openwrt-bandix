include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.12.9
PKG_RELEASE:=1

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.12.9
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=17803eeb6964187626e6af2e2b0a3b081d87a8017ff2b6505ba313b0c7b8ba7f
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
		PKG_HASH:=cbf9cf705218211e0a5cd1427049632aa40086831feee2994e9d4b7b2cf46ab4
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=2901c5f98e77fce574bcaef1aa8c20acd58ca341f3f3bd5f3bc80d745946f632
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=390840c939cec718570cd8cbf50ed130fd02d7f75b80d74af251bd1ecd0f43a8
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=965f9e88398f42cf5535612b58629b89c058db46afaf3c814929a7cfc9fa4e3b
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=f47df37959f73b2188f89faf8c9a3217966ca4c1389f695886f263d28911e8fb
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=318587b09b37d1ab8af96466e5191ce32c4dbc92294f5c55826ebe1a88c7bcab
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=fd1b12b7cd2034aa8afa89901d0d38784528f10921b6c0f806dac9dcbf523085
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=24dab3f89f8930cb925ec1a20d73111e09bae7e6a87954b56a681395660f6ed4
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=916bf42c60c49df5c3ee6f4a60ce542d2b080788445b9bf47f3322eb9a5b66cf
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=4909cf2e80861d082c4d4870950259d8c6f14e606f9dfa16c92514f178f3ae40
else
	PKG_HASH:=dummy
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
	gzip -dc "$(DL_DIR)/$(PKG_SOURCE)" | tar -C $(PKG_BUILD_DIR)/bin --strip-components=1 -xf -
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
