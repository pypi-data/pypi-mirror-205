#!/usr/bin/python3
# -*- coding: utf-8 -*-


import logging
from pathlib import Path
from datetime import datetime


class LoggingConfig:
    dt = datetime.now()
    level = logging.INFO
    filemode: str = 'w'
    encoding: str = 'utf-8'
    log_path: Path = Path('/tmp/slpkg/logs')
    log_file: Path = Path(log_path, 'slpkg.log')
    d: str = f'{dt.day}/{dt.month}/{dt.year}'
    t: str = f'{dt.hour}:{dt.minute}:{dt.second}'
    date: str = f'{d} {t}'
