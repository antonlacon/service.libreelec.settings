# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2009-2013 Stephan Raue (stephan@openelec.tv)
# Copyright (C) 2013 Lutz Fiebach (lufie@openelec.tv)
# Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)

import os
import socket

import xbmc
import xbmcaddon

import syspath
from config import CONFIG_CACHE, XBMC_USER_HOME


__scriptid__ = 'service.libreelec.settings'
__addon__ = xbmcaddon.Addon(id=__scriptid__)
__cwd__ = __addon__.getAddonInfo('path')
__media__ = f'{__cwd__}/resources/skins/Default/media'
_ = __addon__.getLocalizedString


# set up addon settings location
try:
    if not os.path.isdir(f'{XBMC_USER_HOME}/userdata/addon_data/service.libreelec.settings'):
        os.makedirs(f'{XBMC_USER_HOME}/userdata/addon_data/service.libreelec.settings')
    if not os.path.isdir(f'{CONFIG_CACHE}/services'):
        os.makedirs(f'{CONFIG_CACHE}/services')
except Exception:
    pass

try:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect('/var/run/service.libreelec.settings.sock')
    sock.send(bytes('openConfigurationWindow', 'utf-8'))
    sock.close()
except Exception as e:
    xbmc.executebuiltin(f'Notification("LibreELEC", "{_(32390)}", 5000, "{__media__}/icon.png"')
