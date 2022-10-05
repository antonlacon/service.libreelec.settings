# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2020-present Team LibreELEC

import os
import shutil
import log


def delete_file(file):
    log.log(f'Deleting file: {file}', log.DEBUG)
    if os.path.isfile(file):
        try:
            os.remove(file)
        except Exception as e:
            log.log(f'Error deleting {file}: {repr(e)}', log.ERROR)
    else:
        log.log(f'Tried to delete file that does not exist: {file}', log.WARNING)


def delete_tree(tree):
    log.log(f'Deleting directory: {tree}', log.DEBUG)
    if os.path.isdir(tree):
        try:
            shutil.rmtree(tree)
        except Exception as e:
            log.log(f'Error deleting directory {tree}: {repr(e)}', log.ERROR)
    else:
        log.log(f'Tried to delete directory that does not exist: {tree}', log.WARNING)


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
