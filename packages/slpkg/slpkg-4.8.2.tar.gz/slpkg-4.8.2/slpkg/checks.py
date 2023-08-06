#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.error_messages import Errors
from slpkg.repositories import Repositories
from slpkg.models.models import session as Session

from slpkg.models.models import SBoTable, PonceTable, BinariesTable


class Check(Configs):
    """ Some checks before proceed. """

    def __init__(self, flags: list, data: dict):
        __slots__ = 'flags', 'data'
        super(Configs, self).__init__()
        self.flags: list = flags
        self.data: dict = data

        self.errors = Errors()
        self.utils = Utilities()
        self.repos = Repositories()

        self.session = Session

        self.option_for_binaries: bool = self.utils.is_option(
            ['-B', '--bin-repo='], flags)

        if self.option_for_binaries:
            self.repo_table = BinariesTable
        else:
            self.repo_table = SBoTable
            if self.repos.ponce_repo:
                self.repo_table = PonceTable

    def exists_in_the_database(self, packages: list) -> None:
        """ Checking if the slackbuild exists in the database. """
        not_packages: list = []

        for pkg in packages:

            if self.option_for_binaries:
                if not self.data.get(pkg) and pkg != '*':
                    not_packages.append(pkg)
            else:
                if not self.data.get(pkg) and pkg != '*':
                    not_packages.append(pkg)

        if not_packages:
            self.errors.raise_error_message(f"Packages '{', '.join(not_packages)}' does not exists",
                                            exit_status=1)

    def is_package_unsupported(self, slackbuilds: list) -> None:
        """ Checking for unsupported slackbuilds. """
        for sbo in slackbuilds:
            if sbo != '*':
                if self.os_arch == 'x86_64' and self.data[sbo][4]:
                    sources: list = self.data[sbo][4].split()
                else:
                    sources: list = self.data[sbo][3].split()

                if 'UNSUPPORTED' in sources:
                    self.errors.raise_error_message(f"Package '{sbo}' unsupported by arch",
                                                    exit_status=1)

    def is_installed(self, packages: list) -> None:
        """ Checking for installed packages. """
        not_found: list = []

        for pkg in packages:
            if not self.utils.is_package_installed(pkg):
                not_found.append(pkg)

        if not_found:
            self.errors.raise_error_message(f'Not found \'{", ".join(not_found)}\' installed packages',
                                            exit_status=1)

    def is_empty_database(self, repo: str) -> None:
        """ Checking for empty table and database file. """
        db = Path(self.db_path, self.database_name)

        if self.option_for_binaries and repo != '*':
            count: int = self.session.query(self.repo_table.id).where(self.repo_table.repo == repo).count()
        else:
            count: int = self.session.query(self.repo_table.id).count()

        if not self.session.query(self.repo_table).first() or not db.is_file() or count == 0:
            self.errors.raise_error_message("You need to update the package lists first, run:\n\n"
                                            "              $ slpkg update\n"
                                            "              $ slpkg update --bin-repo=[repo_name] for binaries",
                                            exit_status=1)
