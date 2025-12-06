include $(TOPDIR)/rules.mk

PKG_NAME:=bandix
PKG_VERSION:=0.10.3
PKG_RELEASE:=2

PKG_LICENSE:=Apache-2.0
PKG_MAINTAINER:=timsaya

include $(INCLUDE_DIR)/package.mk

# 使用OpenWrt的Rust映射机制
include $(TOPDIR)/feeds/packages/lang/rust/rust-values.mk

# 二进制文件的文件名和URL
RUST_BANDIX_VERSION:=0.10.3
RUST_BINARY_FILENAME:=bandix-$(RUST_BANDIX_VERSION)-$(RUSTC_TARGET_ARCH).tar.gz


# 修正下载地址定义方式
PKG_SOURCE:=$(RUST_BINARY_FILENAME)
PKG_SOURCE_URL:=https://github.com/timsaya/bandix/releases/download/v$(RUST_BANDIX_VERSION)
PKG_HASH:=skip

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