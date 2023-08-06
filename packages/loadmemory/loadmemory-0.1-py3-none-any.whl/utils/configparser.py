#!/usr/bin/python3.8+
# -*- coding:utf-8 -*-
import json
from typing import Union
from pathlib import Path


def json_config(filepath: Union[Path, str]):
    with open(filepath, 'rb') as f:
        conf = json.load(f)
    return conf
