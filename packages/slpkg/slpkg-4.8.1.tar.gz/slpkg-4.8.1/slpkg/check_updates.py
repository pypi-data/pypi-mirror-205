#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from multiprocessing import Process
from urllib3 import PoolManager, ProxyManager, make_headers

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.progress_bar import ProgressBar
from slpkg.repositories import Repositories


class CheckUpdates(Configs):
    """ Check for changes in the ChangeLog file. """

    def __init__(self, flags: list, repo: str):
        __slots__ = 'flags', 'repo'
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repo: str = repo
        self.utils = Utilities()
        self.progress = ProgressBar()
        self.repos = Repositories()

        self.compare: dict = {}
        self.local_chg_txt = None
        self.repo_chg_txt = None

        self.option_for_binaries: bool = self.utils.is_option(
            ['-B', '--bin-repo='], self.flags)

    def check(self) -> dict:
        if self.option_for_binaries:

            for repo in list(self.repos.repositories.keys())[2:]:

                if self.repos.repositories[repo][0] and repo == self.repo:
                    self.binary_repository(repo)
                    break

                if self.repos.repositories[repo][0] and self.repo == '*':
                    self.binary_repository(repo)
        else:

            if self.repos.ponce_repo:
                self.ponce_repository()
            else:
                self.sbo_repository()

        return self.compare

    def binary_repository(self, repo) -> None:
        local_chg_txt: Path = Path(self.repos.repositories[repo][1], self.repos.repositories[repo][5])
        repo_chg_txt: str = f'{self.repos.repositories[repo][2][0]}{self.repos.repositories[repo][5]}'
        self.compare[repo] = self.compare_dates(local_chg_txt, repo_chg_txt)

    def sbo_repository(self) -> None:
        local_chg_txt: Path = Path(self.repos.sbo_repo_path, self.repos.sbo_repo_changelog)
        repo_chg_txt: str = f'{self.repos.sbo_repo_mirror[0]}{self.repos.sbo_repo_changelog}'
        self.compare[self.repos.sbo_repo_name] = self.compare_dates(local_chg_txt, repo_chg_txt)

    def ponce_repository(self) -> None:
        local_chg_txt: Path = Path(self.repos.ponce_repo_path, self.repos.ponce_repo_changelog)
        repo_chg_txt: str = f'{self.repos.ponce_repo_mirror[0]}{self.repos.ponce_repo_changelog}'
        self.compare[self.repos.ponce_repo_name] = self.compare_dates(local_chg_txt, repo_chg_txt)

    def compare_dates(self, local_chg_txt: Path, repo_chg_txt: str) -> bool:
        local_size: int = 0

        if repo_chg_txt.startswith('file'):
            return False

        try:
            http = PoolManager()
            proxy_default_headers = make_headers(proxy_basic_auth=f'{self.proxy_username}:{self.proxy_password}')

            if self.proxy_address.startswith('http'):
                http = ProxyManager(f'{self.proxy_address}', headers=proxy_default_headers)

            elif self.proxy_address.startswith('socks'):
                # https://urllib3.readthedocs.io/en/stable/advanced-usage.html#socks-proxies
                try:  # Try to import PySocks if it's installed.
                    from urllib3.contrib.socks import SOCKSProxyManager
                except (ModuleNotFoundError, ImportError):
                    raise SystemExit()

                http = SOCKSProxyManager(f'{self.proxy_address}', headers=proxy_default_headers)

            repo = http.request('GET', repo_chg_txt)
        except KeyboardInterrupt:
            raise SystemExit(1)

        if local_chg_txt.is_file():
            local_size: int = int(os.stat(local_chg_txt).st_size)

        repo_size: int = int(repo.headers['Content-Length'])

        return local_size != repo_size

    def view_message(self) -> None:
        self.check()

        print()
        for repo, comp in self.compare.items():
            if comp:
                print(f"\n{self.endc}There are new updates available for the "
                      f"'{self.bgreen}{repo}{self.endc}' repository!")

        if True not in self.compare.values():
            print(f'\n{self.endc}{self.yellow}No updated packages since the last check.{self.endc}')

    def updates(self) -> None:
        message: str = 'Checking for news, please wait...'

        # Starting multiprocessing
        p1 = Process(target=self.view_message)
        p2 = Process(target=self.progress.bar, args=(message, ''))

        p1.start()
        p2.start()

        # Wait until process 1 finish
        p1.join()

        # Terminate process 2 if process 1 finished
        if not p1.is_alive():
            p2.terminate()

        # Wait until process 2 finish
        p2.join()

        # Restore the terminal cursor
        print('\x1b[?25h', self.endc)
