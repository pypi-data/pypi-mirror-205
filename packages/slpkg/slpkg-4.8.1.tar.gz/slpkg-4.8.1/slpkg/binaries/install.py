#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess
from collections import OrderedDict
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.checksum import Md5sum
from slpkg.upgrade import Upgrade
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.repositories import Repositories
from slpkg.binaries.required import Required
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class Packages(Configs):

    def __init__(self, data: dict, packages: list, flags: list, mode: str):
        __slots__ = 'data', 'packages', 'flags', 'mode'
        super(Configs, self).__init__()
        self.data: dict = data
        self.packages: list = packages
        self.flags: list = flags
        self.mode: str = mode

        self.progress = ProgressBar()
        self.utils = Utilities()
        self.repos = Repositories()
        self.dialogbox = DialogBox()
        self.upgrade = Upgrade(self.flags, self.data)
        self.view_message = ViewMessage(self.flags, self.data)
        self.session = Session

        self.stderr = None
        self.stdout = None
        self.process_message: str = ''

        self.packages_requires: list = []
        self.install_order: list = []
        self.binary_packages: list = []

        self.option_for_reinstall: bool = self.utils.is_option(
            ['-r', '--reinstall'], self.flags)

        self.option_for_skip_installed: bool = self.utils.is_option(
            ['-k', '--skip-installed'], self.flags)

        self.option_for_resolve_off: bool = self.utils.is_option(
            ['-o', '--resolve-off'], self.flags)

        self.option_for_no_silent: bool = self.utils.is_option(
            ['-n', '--no-silent'], self.flags)

        self.packages: list = self.utils.apply_package_pattern(self.data, self.packages)

    def execute(self) -> None:
        self.dependencies()

        self.view_message.install_packages(self.packages, self.packages_requires, self.mode)
        self.view_message.question()

        start: float = time.time()
        self.download()
        self.checksum()
        self.install_packages()
        elapsed_time: float = time.time() - start

        self.utils.finished_time(elapsed_time)

    def dependencies(self):
        """ Creating the dependencies list and the order for install. """
        if not self.option_for_resolve_off:

            for pkg in self.packages:

                # Skip installed package when the option --skip-installed is applied.
                if self.option_for_skip_installed and self.utils.is_package_installed(pkg):
                    continue

                self.packages_requires += Required(self.data, pkg).resolve()

            # Clean dependencies from the dependencies list if already added with main packages.
            requires = list(OrderedDict.fromkeys(self.packages_requires))

            if requires:
                self.packages_requires = self.choose_dependencies(requires)

        # Clean up the main packages if they were selected for dependencies.
        for dep in self.packages_requires:
            if dep in self.packages:
                self.packages.remove(dep)

        self.install_order = [*self.packages_requires, *self.packages]

    def download(self) -> None:
        """ Download packages from the repositories. """
        pkg_urls: list = []

        for pkg in self.install_order:

            if self.continue_install(pkg):
                package: str = self.data[pkg][1]
                mirror: str = self.data[pkg][2]
                location: str = self.data[pkg][3]

                pkg_urls.append(f'{mirror}{location}/{package}')

                self.binary_packages.append(package)
                self.utils.remove_file_if_exists(self.tmp_slpkg, package)
            else:
                version: str = self.data[pkg][0]
                self.view_message.view_skipping_packages(pkg, version)

        if pkg_urls:
            down = Downloader(self.tmp_slpkg, pkg_urls, self.flags)
            down.download()
            print()

    def continue_install(self, name) -> bool:
        """ Skip installed package when the option --skip-installed is applied
            and continue to install if the package is upgradable or the --reinstall option
            applied.
         """
        if not self.utils.is_package_installed(name):
            return True

        if self.upgrade.is_package_upgradeable(name):
            return True

        if self.utils.is_package_installed(name) and self.option_for_reinstall:
            return True

        return False

    def checksum(self) -> None:
        """ Packages checksums. """
        md5 = Md5sum(self.flags)
        for package in self.binary_packages:
            name: str = self.utils.split_binary_pkg(package[:-4])[0]
            pkg_checksum: str = self.data[name][10]
            md5.check(self.tmp_slpkg, package, pkg_checksum)

    def install_packages(self) -> None:
        """ Install the packages. """
        for package in self.binary_packages:

            message: str = f'{self.cyan}Installing{self.endc}'
            slack_command: str = self.installpkg

            if (self.option_for_reinstall or self.utils.is_package_installed(package)
                    or self.mode == 'upgrade'):

                message: str = f'{self.cyan}Upgrade{self.endc}'
                slack_command: str = self.reinstall

            command: str = f'{slack_command} {self.tmp_slpkg}/{package}'
            self.process_message: str = f"package '{package}' to install"
            self.multi_process(command, package, message)

            if not self.option_for_resolve_off:
                name: str = self.utils.split_binary_pkg(package[:-4])[0]
                self.logging_installed_dependencies(name)

    def logging_installed_dependencies(self, name: str) -> None:
        """ Logging installed dependencies. """
        exist = self.session.query(LogsDependencies.name).filter(
            LogsDependencies.name == name).first()

        requires: list = Required(self.data, name).resolve()

        # Update the dependencies if exist else create it.
        if exist:
            self.session.query(
                LogsDependencies).filter(
                    LogsDependencies.name == name).update(
                        {LogsDependencies.requires: ' '.join(requires)})

        elif requires:
            deps: list = LogsDependencies(name=name, requires=' '.join(requires))
            self.session.add(deps)
        self.session.commit()

    def multi_process(self, command: str, filename: str, message: str) -> None:
        """ Starting multiprocessing install/upgrade process. """
        if self.silent_mode and not self.option_for_no_silent:

            done: str = f' {self.byellow} Done{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            # Starting multiprocessing
            p1 = Process(target=self.utils.process, args=(command, self.stderr, self.stdout))
            p2 = Process(target=self.progress.bar, args=(f'{message}:', filename))

            p1.start()
            p2.start()

            # Wait until process 1 finish
            p1.join()

            # Terminate process 2 if process 1 finished
            if not p1.is_alive():

                if p1.exitcode != 0:
                    done: str = f'{self.bred}Failed: {self.endc}{self.process_message}.'

                print(f'{self.endc}{done}', end='')
                p2.terminate()

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h', self.endc)
        else:
            self.utils.process(command, self.stderr, self.stdout)

    def choose_dependencies(self, dependencies: list) -> list:
        """ Choose packages for install. """
        height: int = 10
        width: int = 70
        list_height: int = 0
        choices: list = []
        title: str = ' Choose dependencies you want to install '

        for package in dependencies:
            status: bool = False

            repo_ver: str = self.data[package][0]
            help_text: str = f'Package: {package} {repo_ver}'
            upgradable: bool = self.upgrade.is_package_upgradeable(package)
            installed: str = self.utils.is_package_installed(package)

            if self.mode == 'upgrade' and upgradable:
                status: bool = True

            if self.mode == 'install' and upgradable:
                status: bool = True

            if self.mode == 'install' and not installed:
                status: bool = True

            if self.option_for_reinstall:
                status: bool = True

            choices += [(package, repo_ver, status, help_text)]

        text: str = f'There are {len(choices)} dependencies:'

        code, tags = self.dialogbox.checklist(text, dependencies, title, height,
                                              width, list_height, choices)

        if not code:
            return dependencies

        os.system('clear')

        return tags
