#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

def ensure_folder(path):
    full_path = path
    if path.startswith('~'):
        full_path = os.path.join(os.path.expanduser(path))
    if os.path.exists(full_path):
        return
    os.mkdir(full_path)

def ensure_file(path):
    full_path = path
    if path.startswith('~'):
        full_path = os.path.join(os.path.expanduser(path))
    if os.path.exists(full_path):
        return
    f = open(full_path, 'w')
    f.close()

def get_file_as_json(config_file_location):
    full_path = config_file_location
    if config_file_location.startswith('~'):
        full_path = os.path.join(os.path.expanduser(config_file_location))
    conf_contents = ''.join(open(full_path).readlines())
    conf_contents = conf_contents.strip()
    if len(conf_contents) == 0:
        return {}
    return json.loads(conf_contents)

if __name__ == '__main__':
    print get_file_as_json('temp.json')