#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil
from pathlib import PosixPath

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.views.views import ViewMessage
from slpkg.repositories import Repositories
from slpkg.models.models import session as Session
from slpkg.models.models import (Base, engine, LogsDependencies,
                                 SBoTable, PonceTable, BinariesTable,
                                 LastRepoUpdated)


class Cleanings(Configs):
    """ Cleans the logs from packages. """

    def __init__(self, flags: list):
        __slots__ = 'flags'
        super(Configs, self).__init__()
        self.flags: list = flags
        self.session = Session

        self.view = ViewMessage(flags)
        self.repos = Repositories()
        self.utils = Utilities()

    def tmp(self):
        print('Deleting of local data:\n')

        for file in self.tmp_slpkg.glob('*'):
            print(f"  {self.bred}>{self.endc} '{file}'")

        print(f"\n{self.prog_name}: {self.blink}{self.bold}{self.bred}WARNING!{self.endc}: All the files and "
              f"folders will delete!")

        views = ViewMessage(self.flags)
        views.question()

        self.utils.remove_folder_if_exists(self.tmp_slpkg)
        self.utils.create_directory(self.build_path)
        print(f'{self.byellow}Successfully cleared!{self.endc}\n')

    def logs_deps(self) -> None:
        """ Deletes the log table from the database. """
        dependencies: list = self.session.query(
            LogsDependencies.name, LogsDependencies.requires).all()  # type: ignore

        if dependencies:
            self.view.logs_packages(dependencies)
            self.view.question()

            self.session.query(LogsDependencies).delete()
            self.session.commit()
        else:
            print('\nNothing to clean.\n')

    def db_tables(self) -> None:
        """ Drop all the tables from the database. """
        print('Deleting repositories of local data and the database:\n')
        for repo, values in self.repos.repositories.items():
            if values[1].exists() and isinstance(values[1], PosixPath):
                print(f"  {self.bred}>{self.endc} '{values[1]}'")

        print(f'\n{self.prog_name}: {self.blink}{self.bold}{self.bred}WARNING!{self.endc}: '
              f'All the data from the database will be deleted!')
        self.view.question()

        tables: list = [
            PonceTable.__table__,
            SBoTable.__table__,
            BinariesTable.__table__,
            LastRepoUpdated.__table__
        ]

        Base.metadata.drop_all(bind=engine, tables=tables)

        # Deletes local downloaded data.
        self.delete_repositories_data()

        print(f"{self.byellow}Successfully cleared!{self.endc}\n\n"
              "You need to update the package lists now:\n\n"
              "  $ slpkg update\n"
              "  $ slpkg update --bin-repo=[repo_name] for binaries\n")

    def delete_repositories_data(self):
        """ Deletes local folders with the repository downloaded data. """
        for repo, values in self.repos.repositories.items():
            if values[1].exists() and isinstance(values[1], PosixPath):
                shutil.rmtree(values[1])
