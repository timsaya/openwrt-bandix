include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.12.7
PKG_RELEASE:=1

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.12.7
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=ef9af01841a9bb421b14226c1de360d3d8c4a79529b7e5c69ea04219b5ef47bd
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
		PKG_HASH:=f12a38c414c1a5e41aebd6730ea99a258de8f730770b2e90801759606897dab5
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=da9e3b0be1fed5f89c1c0984f0391e25f12761824ba8a7891c57eee07817c140
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=a0365bf3ea6292d8f6bc3c1a451588cc803ef8dc3827a416c7a23f5b7215ff5c
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=ca645ce8239d63865df9a6562d10ec103df6d8a2d9f7d88cf39573f1143db35b
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=6c93d197a8df40514983a983fb950dd641122426ed2bca0999e849d917df821b
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=dc93ec02f94ddc35e1e6fe0e108f0883526b4c54331c26a1f27c20a8f37957ec
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=6d60527faade80023e8b8d7ad9c61774fc2143243f64569882dab1b76b5c2c15
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=9c3dc4bde05e1f7a3a7a7a63ee5119195f5172bdf6e6e7879a02a0f10c75cfbc
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=f1310e49a9e9239c0dbd377efa6c8e29221016e34890493f91b402d81760b6a1
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=9cd5dd6b5af5d40db6477f38502eaa5662e2a0d003883b3ae6733063948864fd
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
