include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.11.0
PKG_RELEASE:=1

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.11.0
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=6c7bd335027152b50f3df38fec2babd93bd92892ac58c9e766867bdc15504879
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
		PKG_HASH:=dfaebfca69c9597fb5086a9ec70d6adeb5c4445227805f1fef826ee7823879a0
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=31b42b38d0890b27c135310c847d6767f62239a5f7eb86ff7c44cfbf166b5a2f
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=9c9ad03edc361e5910e121b768c410887dd791cc2bb5d8bc803a87ac37449d7f
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=bd3878cd948ae7cc311d7bab933d483090b8fb2ef9aa115132cad1d2b329d084
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=7b599bd27d8d8193472ca5611e9665693f3148a37a73eabf55d60db794d171b5
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=527dff7ec593427adde3fd045346773d684526b962cafd3651f6a9d75f928138
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=628fe8a9128d383cc817d9aa43d39b8f4ebfbc3319a49f14df1eb5197a4883be
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=75e986782be593736c6c99b04a2b85aa8cd843bb7899c59daaa7e381210ce55d
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=b6eca874a62645556ba2910760cc65eddad640532e356e704b700e40a0ad2bf6
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=59f19fba55d67bbb8757b837076a4372ed577725d38bf91964a6d3af9c9a29d0
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
