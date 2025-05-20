# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2020-present Team LibreELEC (https://libreelec.tv)

import xbmcaddon
import xbmcgui

import log


ADDON = xbmcaddon.Addon()
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name')


@log.log_function()
def notification(message, heading=ADDON_NAME, icon=ADDON_ICON, time=5000):
    xbmcgui.Dialog().notification(heading, message, icon, time)
