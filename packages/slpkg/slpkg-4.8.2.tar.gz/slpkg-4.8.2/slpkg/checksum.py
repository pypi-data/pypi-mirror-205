#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
import logging
from pathlib import Path
from typing import Union
from urllib.parse import unquote

from slpkg.views.ascii import Ascii
from slpkg.utilities import Utilities
from slpkg.error_messages import Errors
from slpkg.views.views import ViewMessage
from slpkg.logging_config import LoggingConfig


class Md5sum:
    """ Checksum the sources. """

    def __init__(self, flags: list):
        __slots__ = 'flags'
        self.flags: list = flags
        self.ascii = Ascii()
        self.errors = Errors()
        self.utils = Utilities()

        logging.basicConfig(filename=LoggingConfig.log_file,
                            filemode=LoggingConfig.filemode,
                            encoding=LoggingConfig.encoding,
                            level=LoggingConfig.level)

    def check(self, path: Union[str, Path], source: str, checksum: str) -> None:
        """ Checksum the source. """
        source_file = unquote(source)
        filename = source_file.split('/')[-1]
        source_path = Path(path, filename)

        md5 = self.read_file(source_path)

        file_check = hashlib.md5(md5).hexdigest()

        checksum = "".join(checksum)

        if file_check != checksum:
            self.ascii.draw_checksum_error_box(filename, checksum, file_check)
            view = ViewMessage(self.flags)
            view.question()

    def read_file(self, filename: Union[str, Path]) -> bytes:
        """ Reads the file. """
        try:
            with open(filename, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            logger = logging.getLogger(LoggingConfig.date)
            logger.exception(f'{self.__class__.__name__}: '
                             f'{self.__class__.read_file.__name__}')
            self.errors.raise_error_message(f"No such file or directory: '{filename}'", exit_status=20)
