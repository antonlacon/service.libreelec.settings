# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2020-present Team LibreELEC (https://libreelec.tv)

'''This module holds support functions for interacting with the underlying OS.

Support functions are grouped by purpose:
1. File access: read / write / copy / move / download
2. System access: executing system commands
'''

import os
import subprocess
import urllib.parse
import urllib.request

import xbmcgui

import config
import log


### FILE ACCESS ###
def read_file(file):
    '''Return contents of file.'''
    content = None
    if os.path.isfile(file):
        with open(file, 'r', encoding='utf-8') as data:
            content = data.read()
    else:
        log.log(f'Error: Failed to read file: {file}', log.ERROR)
    return content.strip() if content else ''


def read_shell_setting(file, default):
    setting = default
    if os.path.isfile(file):
        with open(file) as input:
            setting = input.readline().strip()
    return setting


def read_shell_settings(file, defaults={}):
    settings = defaults
    if os.path.isfile(file):
        with open(file) as input:
            for line in input:
                name, value = line.strip().split('=', 1)
                if len(value) and value[0] in ['"', '"'] and value[0] == value[-1]:
                    value = value[1:-1]
                settings[name] = value
    return settings


### SYSTEM ACCESS ###
def download_file(source, destination, silent=False):
    '''Download source file to destination. Optionally show progress bar'''
    def progress_bar_update(chunk_count, chunk_size, total_size):
        '''Updates progress bar using urlretrieve's report hook'''
        nonlocal progress_bar
        if total_size != -1:
            progress_percentage = int(chunk_count * chunk_size / total_size * 100)
            progress_bar.update(progress_percentage)
        else:
            progress_bar.update(0, 'Filesize unknown')

    source = urllib.parse.quote(source, safe=':/')
    if silent:
        urllib.request.urlretrieve(source, destination)
    else:
        with xbmcgui.DialogProgress() as progress_bar:
            progress_bar.create('File Download', f'Downloading {source}')
            urllib.request.urlretrieve(source, destination, progress_bar_update)
            if progress_bar.iscanceled() and os.path.isfile(destination):
                os.remove(destination)


def execute(command, get_result=False):
    '''Run command, waiting for it to finish. Returns: command output or None'''
    log.log(f'Executing command: {command}', log.DEBUG)
    try:
        cmd_status = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        log.log(f'Command failed: {command}', log.ERROR)
        log.log(f'Executed command: {e.cmd}', log.DEBUG)
        # with shell=True, this is the shell's exit code
        log.log(f'shell exit code: {e.returncode}', log.ERROR)
        log.log(f'START COMMAND OUTPUT:\n{e.stdout.decode()}\nEND COMMAND OUTPUT', log.ERROR)
        # return None on failure. Commands that want output get nothing; remainder weren't expecting output
        return None
    except FileNotFoundError:
        # this will be whether the shell is found while shell=True
#        log.log(f'os_tools.execute: Command not found: {command.split(" ")[0]}', log.ERROR)
        log.log('os_tools.execute: Failed to find shell.', log.ERROR)
        return None
    # return output if requested, otherwise None
    return cmd_status.stdout.decode() if get_result else None


def get_rpi_cpu_ver():
    '''Parse RPi CPU revision for model'''
    if config.PROJECT == 'RPi':
        try:
            vc_cmd_output = execute('vcgencmd otp_dump 2>/dev/null', get_result=True)
        except Exception:
            return None
        if vc_cmd_output:
            for line in vc_cmd_output.splitlines():
                if line[0:3] == '30:':
                    rpi_revision_id = line.split(':')[1]
                    return rpi_revision_id[4:5]
    return None


def get_timestamp():
    '''Return timestamp of system time in YYYYMMDDHHMMSS format'''
    return time.strftime('%Y%m%d%H%M%S')
