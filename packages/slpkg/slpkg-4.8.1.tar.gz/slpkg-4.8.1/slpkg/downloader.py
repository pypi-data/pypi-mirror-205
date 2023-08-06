#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil
from typing import Union
from pathlib import Path
from urllib.parse import unquote
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.error_messages import Errors


class Downloader(Configs):

    def __init__(self, path: Union[str, Path], urls: list, flags: list):
        __slots__ = 'path', 'urls', 'flags'
        super(Configs, self).__init__()
        self.path: Path = path
        self.urls: list = urls
        self.flags: list = flags

        self.errors = Errors()
        self.utils = Utilities()

        self.option_for_parallel: bool = self.utils.is_option(
            ['-P', '--parallel'], self.flags)

    def download(self) -> None:
        """ Starting the processing for downloading. """
        process: list = []

        if self.parallel_downloads or self.option_for_parallel:
            for url in self.urls:
                p1 = Process(target=self.tools, args=(url,))
                process.append(p1)
                p1.start()

            for proc in process:
                proc.join()
        else:
            for url in self.urls:
                self.tools(url)

    def tools(self, url: str) -> None:
        """ Downloader tools wget, curl and lftp. """
        command: str = ''
        filename: str = url.split('/')[-1]

        if url.startswith('file'):
            shutil.copy2(url[7:], self.tmp_slpkg)
        else:
            if self.downloader in ['wget', 'wget2']:
                command: str = f'{self.downloader} {self.wget_options} --directory-prefix={self.path} "{url}"'

            elif self.downloader == 'curl':
                command: str = f'{self.downloader} {self.curl_options} "{url}" --output {self.path}/{filename}'

            elif self.downloader == 'lftp':
                command: str = f'{self.downloader} {self.lftp_get_options} {url} -o {self.path}'

            else:
                self.errors.raise_error_message(f"Downloader '{self.downloader}' not supported")

        self.utils.process(command)
        self.check_if_downloaded(url)

    def check_if_downloaded(self, url: str) -> None:
        """ Checks if the file downloaded. """
        url: str = unquote(url)
        file: str = url.split('/')[-1]
        path_file: Path = Path(self.path, file)

        if not path_file.exists():
            self.errors.raise_error_message(f"Download the '{file}' file")
