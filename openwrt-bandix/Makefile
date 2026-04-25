include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.12.8
PKG_RELEASE:=1

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.12.8
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)

# 修正二进制文件校验值
ifeq ($(ARCH),aarch64)
	PKG_HASH:=8df5f5964e903b51b45a1b4f549bb956a5882b940eb971eb670536e3dbd116b7
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
		PKG_HASH:=bcd2757dbce28bdf9206fe2a1412f2969a07df52300c2eab0e3769d78c7bb079
	else ifeq ($(ARM_CPU_TYPE),arm-armhf)
		PKG_HASH:=f9a1402615e20add9d7f7cb9911216de5589a96499a3326d1fcd3b0fc522819e
	else ifeq ($(ARM_CPU_TYPE),armv5te-armel)
		PKG_HASH:=735bb18828c2025fb80f14b2fc3031732883da63cbb53ed28c8096ce383258de
	else ifeq ($(ARM_CPU_TYPE),armv7-armel)
		PKG_HASH:=95a61618e15bce75d31c0eb9b652a08063bef8d7ad747aac51913a934515d924
	else ifeq ($(ARM_CPU_TYPE),armv7-armhf)
		PKG_HASH:=43452d9d72603fe2f3e565b0d16be8a8b8425e932bf4553c1a940ff21f5e4ddc
	else
		PKG_HASH:=dummy
	endif
else ifeq ($(ARCH),mips)
	PKG_HASH:=e3028bf695e6f7c626872069e32d0176337ce25e024737f51b912f7501d0f268
else ifeq ($(ARCH),mipsel)
	PKG_HASH:=3b3de0e3acba42531614b573bdb453a283cbba0681154fa1a259e3726dfeca20
else ifeq ($(ARCH),powerpc64)
	PKG_HASH:=aa0b20bc11c6c6acdd7c7a730e082ee4e77caed3b1c06ae631c93bd2b19e0468
else ifeq ($(ARCH),riscv64)
	PKG_HASH:=0ae3a05ffee5f32d83e8169587c5db95fb9573b056cc3f5e9cc20fc3dd6f184a
else ifeq ($(ARCH),x86_64)
	PKG_HASH:=f2f2fd4683182a68fd6bc3ce52c3b60bf5123f30282ee0b207b28db2947f0bf4
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
