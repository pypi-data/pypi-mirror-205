#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from typing import Generator
from packaging.version import parse, InvalidVersion

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories
from slpkg.logging_config import LoggingConfig


class Upgrade(Configs):
    """ Upgrade the installed packages. """

    def __init__(self, flags: list, data: dict):
        __slots__ = 'flags', 'data'
        super(Configs, self).__init__()
        self.flags: list = flags
        self.data: dict = data
        self.utils = Utilities()
        self.repos = Repositories()

        self.option_for_binaries: bool = self.utils.is_option(
            ['-B', '--bin-repo='], flags)

        logging.basicConfig(filename=LoggingConfig.log_file,
                            filemode=LoggingConfig.filemode,
                            encoding=LoggingConfig.encoding,
                            level=LoggingConfig.level)

    def packages(self) -> Generator:
        """ Returns the upgradable packages. """

        # Returns the matched packages between two lists.
        packages: list = list(set(self.utils.installed_packages.keys()) & set(self.data.keys()))

        for pkg in packages:
            if self.is_package_upgradeable(pkg):
                yield pkg

    def is_package_upgradeable(self, name: str) -> bool:
        """ Compares version of packages and returns the maximum. """
        repo_version = repo_build = '0'
        inst_version = inst_build = '0'
        inst_package: str = self.utils.is_package_installed(name)

        repo_tag: str = self.repos.repo_tag
        if self.option_for_binaries:
            repo_tag: str = self.repos.repositories[self.data[name][11]][6]

        if inst_package and inst_package.endswith(repo_tag):
            inst_version: str = self.utils.split_binary_pkg(inst_package)[1]
            inst_build: str = self.utils.split_binary_pkg(inst_package)[3]

            if self.option_for_binaries and self.data.get(name):
                repo_version: str = self.data[name][0]
                repo_package: str = self.data[name][1]
                repo_build: str = self.utils.split_binary_pkg(repo_package)[3]

            else:
                repo_version: str = self.data[name][2]
                repo_location: str = self.data[name][0]
                repo_build: str = self.utils.read_sbo_build_tag(name, repo_location)

        repo_pkg: str = f'{name}-{repo_version}'
        inst_pkg: str = f'{name}-{inst_version}'

        try:
            if parse(repo_pkg) > parse(inst_pkg):
                return True

            if (parse(repo_pkg) == parse(inst_pkg)
                    and parse(repo_build) > parse(inst_build)):
                return True

        except InvalidVersion:
            logger = logging.getLogger(LoggingConfig.date)
            logger.exception(f'{self.__class__.__name__}: '
                             f'{self.__class__.is_package_upgradeable.__name__}: '
                             f'{repo_tag=}, {repo_pkg=}, {inst_pkg=}, {repo_pkg > inst_pkg}, '
                             f'{repo_pkg == inst_pkg and repo_build > inst_build}')

            if repo_pkg > inst_pkg:
                return True

            if repo_pkg == inst_pkg and repo_build > inst_build:
                return True

        return False
