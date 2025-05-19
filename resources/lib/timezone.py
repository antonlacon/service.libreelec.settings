# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2024-present Team LibreELEC (https://libreelec.tv)

'''This module holds support functions for interacting with timezones.
'''

import os
from urllib.request import urlopen

import config
import log
import os_tools


def get_timezone():
    '''Read timezone setting from file or return default of UTC timezone.'''
    return os_tools.read_shell_setting(config.TIMEZONE, default='TIMEZONE=UTC').split('=', 1)[1]


def guess_timezone():
    '''Guess the device's timezone based on the public IP of the device.'''
    def QueryWebServer(url):
        '''Query a webserver for a response.'''
        try:
            response = urlopen(url)
        except Exception as err:
            log.log(f'Error querying: {url}', log.ERROR)
            log.log(err, log.ERROR)
            response = None
        return response.read().decode('utf-8').strip() if response else None

    my_ip = QueryWebServer('https://icanhazip.com')
    return QueryWebServer(f'https://ipapi.co/{my_ip}/timezone') if my_ip else None


def list_timezones():
    '''List timezones available from tzdata.'''
    timezones = []
    with open('/usr/share/zoneinfo/tzdata.zi', mode='r', encoding='utf-8') as tz_db:
        content = tz_db.read()
    for line in content.splitlines():
        # if line starts with Z take second field
        if line.startswith('Z'):
            timezones.append(line.split(' ')[1])
        # if line starts with L take third field
        elif line.startswith('L'):
            timezones.append(line.split(' ')[2])
    # sort and return
    timezones.sort()
    return timezones


def set_timezone(timezone):
    '''Write new timezone info to .cache file and commit change to system.'''
    current_timezone = get_timezone()
    if current_timezone != timezone or not os.path.isfile(config.TIMEZONE):
        with open(config.TIMEZONE, mode='w', encoding='utf-8') as out_file:
            out_file.write(f'TIMEZONE={timezone}\n')
        if os.path.isfile(config.TIMEZONE):
            os_tools.execute('systemctl restart tz-data')
        else:
            log.log(f'Failed to write: {config.TIMEZONE}', log.ERROR)
            log.log(f'Desired timezone was: {timezone}', log.ERROR)
