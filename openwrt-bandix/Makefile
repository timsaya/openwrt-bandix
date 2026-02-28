include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.12.5
PKG_RELEASE:=1

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.12.5
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=f22eeb0a7e270ca34bb30022293f4eccbec372df80398bdc0367122f4767684e
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
		PKG_HASH:=307761c6969c15469e01008b5e6a6a426142353776d7c1ca0e8dbc24e521220b
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=51c933811d95bf352befc819a9077e2949e1f97af8f4865ee0e7ece598bcbc0f
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=484172500574ea860ce086d7f482e6a90edd8bbbb37dfd08e8fdb84e4f5c2ceb
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=10fc837d92f0b12cd03a8be957256abcbac8efee71d7e6574b228521583f9820
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=cb73e66a887e7b65051e99678416d61d915f1595b25f6354990f3fa7842bdc19
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=d4c33adc72ad20288d2b42ca3f4d4ec5ba925936fdbf8f95771d72a6958681f5
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=c2b1dc78f7252ceb7ec6ffad499df78100f9c5beddb5b1152acdc810ed180648
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=5413a85e60cdd3f28850e72228ce2a6fa5e66d263a11b2d7b359d37868fbe864
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=4e92ebc97760e42eb00f7948bf47897aace2037ba70416a2b89b322fe2843693
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=6b091e93a6d49ca1cceb6a0b3fff6fa01e09bcabe06553fdbd599c4c3f35084c
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
