include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.12.6
PKG_RELEASE:=1

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.12.6
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=8c8b94994497ea63e51fe2e259d7eba83f12e1196c70b2255dd1fb6dc986c74a
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
		PKG_HASH:=cef3217edb4980414497e3fcc881fa14f1ec48cec9420ef6b1a4ce5e887dbf32
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=391e56e8135492be9cf2895b4d07fa20faf3389643c898777e5d6c44b902c75b
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=a71f827049b5dceb72c7f1fa854bb8f0cbcd0c0bfdf9ac4e535aaf8db6b516b8
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=2fcd482fada4081d3fc9f6e27aff2c4c5b0464dbff9025147f86519393f851d7
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=852903c7060a884219e08f9f77f6899cc82df677c960b3e390b761ada00c773c
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=84280f3298881ab5cee9a20ccb8ab82de5a0cb26ffae8f71f5279a5001e209aa
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=5301916021e5b62bda4a6f95e4f000fe860e0725c5dc29e0cb7a0b983a878c1e
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=1fbd8a91228600b8277aef9105157b84e169e0f3402a4e293b049f715348cf10
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=02a2cc965f92a36e12fd42bc09cbc3ae5a89b0c77af3d5ebdc28f03d0ab4a121
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=4c67661e820ac3cdcba56f7dcd45596695d05a4c572bf9070c959d3fb74e1087
else
	PKG_HASH:=dummy
endif

define Package/$(PKG_NAME)
	SECTION:=net
	CATEGORY:=Network
	TITLE:=Bandix - Network traffic monitoring tool
	DEPENDS:=+zoneinfo-core +conntrack
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
