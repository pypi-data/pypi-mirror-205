#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import subprocess
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class RemovePackages(Configs):
    """ Removes installed packages. """

    def __init__(self, packages: list, flags: list):
        __slots__ = 'packages', 'flags'
        super(Configs, self).__init__()
        self.packages: list = packages
        self.flags: list = flags

        self.session = Session
        self.utils = Utilities()
        self.progress = ProgressBar()
        self.view = ViewMessage(flags)

        self.process_message: str = ''
        self.installed_packages: list = []
        self.dependencies: list = []
        self.stderr = None
        self.stdout = None

        self.option_resolve_off: bool = self.utils.is_option(
            ['-o', '--resolve-off'], flags)

        self.option_for_no_silent: bool = self.utils.is_option(
            ['-n', '--no-silent'], flags)

        self.option_for_yes: bool = self.utils.is_option(
            ['-y', '--yes'], flags)

    def remove(self) -> None:
        """ Removes package with dependencies. """
        self.installed_packages, self.dependencies = self.view.remove_packages(self.packages)

        self.view.question()

        start: float = time.time()
        self.remove_packages()

        if self.dependencies and not self.option_resolve_off:
            self.delete_deps_logs()

        self.delete_main_logs()

        elapsed_time: float = time.time() - start

        self.utils.finished_time(elapsed_time)

    def remove_packages(self) -> None:
        """ Run Slackware command to remove the packages. """
        for package in self.installed_packages:
            name: str = self.utils.split_binary_pkg(package)[0]
            self.process_message: str = f"package '{name}' to remove"

            if self.check_in_logs_for_dependencies_to_remove(name):
                command: str = f'{self.removepkg} {package}'
                self.multi_process(command, package)

    def check_in_logs_for_dependencies_to_remove(self, name: str) -> bool:
        dependencies: list = []
        logs: dict = self.query_dependencies()

        for package, requires in logs.items():
            if name in requires:
                dependencies.append(package)

        if dependencies and not self.option_for_yes and self.ask_question:
            print(f"\n{self.bold}{self.violet}WARNING!{self.endc}: The package '{self.red}{name}{self.endc}' "
                  f"is a dependency for the packages:")

            for dep in dependencies:
                print(f"{self.cyan:>16}-> {dep}{self.endc}")

            try:
                answer: str = input('\nDo you want to remove? [y/N] ')
            except KeyboardInterrupt:
                raise SystemExit()

            if answer not in ['Y', 'y']:
                return False
            print()

        return True

    def query_dependencies(self) -> dict:
        """ Returns a dictionary with the package name and the dependencies
            before they are saved with the command slpkg install. """
        logs_deps: dict = {}
        package_requires: tuple = self.session.query(
            LogsDependencies.name, LogsDependencies.requires).all()

        for package in package_requires:
            if package[0] not in self.packages:
                logs_deps[package[0]] = package[1].split()

        return logs_deps

    def delete_main_logs(self) -> None:
        """ Deletes main packages from logs. """
        for pkg in self.packages:
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()

    def delete_deps_logs(self) -> None:
        """ Deletes depends packages from logs. """
        for pkg in self.dependencies:
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()

    def multi_process(self, command: str, package: str) -> None:
        """ Starting multiprocessing remove process. """
        if self.silent_mode and not self.option_for_no_silent:

            done: str = f' {self.byellow} Done{self.endc}'
            message: str = f'{self.bold}{self.red}Remove{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            # Starting multiprocessing
            p1 = Process(target=self.utils.process, args=(command, self.stderr, self.stdout))
            p2 = Process(target=self.progress.bar, args=(f'{message}:', package))

            p1.start()
            p2.start()

            # Wait until process 1 finish
            p1.join()

            # Terminate process 2 if process 1 finished
            if not p1.is_alive():

                if p1.exitcode != 0:
                    done: str = f'{self.bred}Failed: {self.endc}{self.process_message}'

                print(f'{self.endc}{done}', end='')
                p2.terminate()

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h', self.endc)
        else:
            self.utils.process(command, self.stderr, self.stdout)
