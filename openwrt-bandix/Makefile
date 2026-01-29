include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.12.3
PKG_RELEASE:=1

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.12.3
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=a29337d592dea0cb56de028dda910ed35a83443a3aa7cca682e2ccf6eeb9991f
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
		PKG_HASH:=4fe41ea7f3e5ebce5944c32a57c393f743cde86f051ab75a400dade7ebf7322b
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=f0d7723e44ed037cbdda126992955ee1dc3dc19776a49a0069dce826696ed30c
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=344cdd7f2e52a6b732ae5c505cda6c96594afe09c2d261cb25e0f63e7411ee42
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=5b471fc2260d345ac4c32a4acf288a468d74ef359ea07c5b286a2d60125fe3ea
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=076fae6e45b5fa733b1bd49a3152b3fde16152b3181e6c161d0826bfb25b679d
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=950e24f3f5abb10a99c76ead120662ef838ddd8adf98e2fbc4ba982d63733309
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=d6918c63edc539ba50e73ecad4d3cb7e2ee89acbae96e264f5ff9d3ea93311ee
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=9ff785e423a81b66f533b7406c13f1266cbb1fa08c163dd5c4d131ecd0f16132
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=9d005f48811cbd0d887ef1445c560f7d5801763646b7054553f6f2f368ffc9fc
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=cb779666f43fc90ec367965edc85a82221b5e0e2017edd1de6260b012ae5dd15
else
	PKG_HASH:=dummy
endif

define Package/$(PKG_NAME)
	SECTION:=net
	CATEGORY:=Network
	TITLE:=Bandix - Network traffic monitoring tool
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

	# 将配置文件安装到临时位置，由 postinst 决定是否复制到最终位置
	$(INSTALL_DIR) $(1)/usr/share/bandix
	$(INSTALL_CONF) ./files/bandix.config $(1)/etc/config/bandix
endef

define Package/$(PKG_NAME)/conffiles
/etc/config/bandix
endef

define Package/$(PKG_NAME)/postinst
#!/bin/sh
if [ -z "$${IPKG_INSTROOT}" ]; then

    # 添加到 sysupgrade.conf 以在系统升级时保留
    if ! grep -q "^/usr/share/bandix$$" /etc/sysupgrade.conf; then
        echo "/usr/share/bandix" >> /etc/sysupgrade.conf
    fi
    if ! grep -q "^/etc/config/bandix$$" /etc/sysupgrade.conf; then
        echo "/etc/config/bandix" >> /etc/sysupgrade.conf
    fi
fi
endef

$(eval $(call BuildPackage,bandix))
