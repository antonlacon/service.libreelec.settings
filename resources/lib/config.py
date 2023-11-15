# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2020-present Team LibreELEC (https://libreelec.tv)

'''This file sets variables for which the rest of the addon may refer to.
'''

import os

import os_tools


OS_RELEASE = os_tools.read_shell_settings('/etc/os-release')
DISTRIBUTION = OS_RELEASE['NAME'] if 'NAME' in OS_RELEASE else ''
VERSION = OS_RELEASE['VERSION'] if 'VERSION' in OS_RELEASE else ''
VERSION_ID = OS_RELEASE['VERSION_ID'] if 'VERSION_ID' in OS_RELEASE else ''
BUILD = OS_RELEASE['LIBREELEC_BUILD'] if 'LIBREELEC_BUILD' in OS_RELEASE else ''
ARCHITECTURE = OS_RELEASE['LIBREELEC_ARCH'] if 'LIBREELEC_ARCH' in OS_RELEASE else ''
PROJECT = OS_RELEASE['LIBREELEC_PROJECT'] if 'LIBREELEC_PROJECT' in OS_RELEASE else ''
DEVICE = OS_RELEASE['LIBREELEC_DEVICE'] if 'LIBREELEC_DEVICE' in OS_RELEASE else ''
BUILDER_NAME = OS_RELEASE['BUILDER_NAME'] if 'BUILDER_NAME' in OS_RELEASE else ''
BUILDER_VERSION = OS_RELEASE['BUILDER_VERSION'] if 'BUILDER_VERSION' in OS_RELEASE else ''

XBMC_USER_HOME = os.environ.get('XBMC_USER_HOME', '/storage/.kodi')
ADDON_CONFIG_FILE = f'{XBMC_USER_HOME}/userdata/addon_data/service.libreelec.settings/oe_settings.xml'
CONFIG_CACHE = os.environ.get('CONFIG_CACHE', '/storage/.cache')
USER_CONFIG = os.environ.get('USER_CONFIG', '/storage/.config')

SYSTEMID = os_tools.read_file_setting('/etc/machine-id') if os.path.isfile('/etc/machine-id') else os.environ.get('SYSTEMID', '')
HOSTNAME = os.path.join(CONFIG_CACHE, 'hostname')
HOSTS_CONF = os.path.join(USER_CONFIG, 'hosts.conf')
TIMEZONE = os.path.join(CONFIG_CACHE, 'timezone')

REGDOMAIN_CONF = os.path.join(CONFIG_CACHE, 'regdomain.conf')
SETREGDOMAIN = '/usr/lib/iw/setregdomain'

BOOT_STATUS = os_tools.read_file_setting('/storage/.config/boot.status')
