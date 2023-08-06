#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories
from slpkg.models.models import session as Session
from slpkg.models.models import LastRepoUpdated, SBoTable, BinariesTable


class RepoInfo(Configs):

    def __init__(self):
        super(Configs, self).__init__()

        self.session = Session
        self.utils = Utilities()
        self.repos = Repositories()
        self.columns, self.rows = shutil.get_terminal_size()

    def info(self):
        """ Prints information about repositories. """
        total_packages: int = 0
        enabled: int = 0

        print('Repositories Information:')
        print('=' * self.columns)
        print(f"{'Name:':<18}{'Status:':<15}{'Last Updated:':<35}{'Packages:':>12}")
        print('=' * self.columns)

        for repo, value in self.repos.repositories.items():
            status: str = 'Disabled'
            color: str = self.red

            last: str = self.session.query(
                LastRepoUpdated.date).where(
                LastRepoUpdated.repo == repo).first()

            if last is None:
                last: tuple = ('',)

            if value[0]:
                enabled += 1
                status: str = 'Enabled'
                color: str = self.green

            if repo in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
                count = self.session.query(SBoTable.id).count()
            else:
                count = self.session.query(BinariesTable).where(BinariesTable.repo == repo).count()

            total_packages += count

            print(f"{self.cyan}{repo:<18}{self.endc}{color}{status:<15}{self.endc}{last[0]:<35}"
                  f"{self.yellow}{count:>12}{self.endc}")

        print('=' * self.columns)
        print(f"{self.grey}Total of {enabled}/{len(self.repos.repositories)} "
              f"repositories are enabled with {total_packages} packages available.\n")
