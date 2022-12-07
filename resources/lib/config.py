# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2020-present Team LibreELEC (https://libreelec.tv)

'''This file sets variables for which the rest of the addon may refer to.
'''

import os

import os_tools


OS_RELEASE = os_tools.read_shell_settings('/etc/os-release')
if 'NAME' in OS_RELEASE:
    DISTRIBUTION = OS_RELEASE['NAME']
if 'VERSION' in OS_RELEASE:
    VERSION = OS_RELEASE['VERSION']
if 'VERSION_ID' in OS_RELEASE:
    VERSION_ID = OS_RELEASE['VERSION_ID']
if 'LIBREELEC_BUILD' in OS_RELEASE:
    BUILD = OS_RELEASE['LIBREELEC_BUILD']
if 'LIBREELEC_ARCH' in OS_RELEASE:
    ARCHITECTURE = OS_RELEASE['LIBREELEC_ARCH']
if 'LIBREELEC_PROJECT' in OS_RELEASE:
    PROJECT = OS_RELEASE['LIBREELEC_PROJECT']
if 'LIBREELEC_DEVICE' in OS_RELEASE:
    DEVICE = OS_RELEASE['LIBREELEC_DEVICE']
if 'BUILDER_NAME' in OS_RELEASE:
    BUILDER_NAME = OS_RELEASE['BUILDER_NAME']
if 'BUILDER_VERSION' in OS_RELEASE:
    BUILDER_VERSION = OS_RELEASE['BUILDER_VERSION']

XBMC_USER_HOME = os.environ.get('XBMC_USER_HOME', '/storage/.kodi')
ADDON_CONFIG_FILE = f'{XBMC_USER_HOME}/userdata/addon_data/service.libreelec.settings/oe_settings.xml'
CONFIG_CACHE = os.environ.get('CONFIG_CACHE', '/storage/.cache')
USER_CONFIG = os.environ.get('USER_CONFIG', '/storage/.config')

BOOT_STATUS = os_tools.read_file('/storage/.config/boot.status')
SYSTEMID = os_tools.read_file('/etc/machine-id') if os.path.exists('/etc/machine-id') else os.environ.get('SYSTEMID', '')
HOSTNAME = os.path.join(CONFIG_CACHE, 'hostname')
HOSTS_CONF = os.path.join(USER_CONFIG, 'hosts.conf')

REGDOMAIN_CONF = os.path.join(CONFIG_CACHE, 'regdomain.conf')
SETREGDOMAIN = '/usr/lib/iw/setregdomain'

try:
    if PROJECT == 'RPi':
        RPI_CPU_VER = os_tools.execute('vcgencmd otp_dump 2>/dev/null | grep 30: | cut -c8', get_result=True).replace('\n','')
    else:
        RPI_CPU_VER = ''
except FileNotFoundError:
    # if vcgencmd is missing
    RPI_CPU_VER = ''
