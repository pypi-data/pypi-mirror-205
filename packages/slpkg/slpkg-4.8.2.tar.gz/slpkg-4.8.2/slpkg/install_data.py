#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories
from slpkg.models.models import session as Session
from slpkg.models.models import (SBoTable, PonceTable,
                                 BinariesTable, LastRepoUpdated)


class InstallData(Configs):

    def __init__(self):
        super(Configs, self).__init__()
        self.session = Session
        self.utils = Utilities()
        self.repos = Repositories()

    def last_updated(self, repo_file: Path) -> str:
        """ Reads the first date of the changelog file."""
        lines: list = self.utils.read_file(repo_file)
        days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
        for line in lines:
            if line.startswith(days):
                return line.replace('\n', '')

    def install_sbos_data(self) -> None:
        """ Install the data for SBo repository. """
        sbo_tags = [
            'SLACKBUILD NAME:',
            'SLACKBUILD LOCATION:',
            'SLACKBUILD FILES:',
            'SLACKBUILD VERSION:',
            'SLACKBUILD DOWNLOAD:',
            'SLACKBUILD DOWNLOAD_x86_64:',
            'SLACKBUILD MD5SUM:',
            'SLACKBUILD MD5SUM_x86_64:',
            'SLACKBUILD REQUIRES:',
            'SLACKBUILD SHORT DESCRIPTION:'
        ]
        sbo_table = SBoTable
        sbo_name: str = self.repos.sbo_repo_name
        path_slackbuilds: Path = Path(self.repos.sbo_repo_path, self.repos.sbo_repo_slackbuilds)
        path_changelog: Path = Path(self.repos.sbo_repo_path, self.repos.sbo_repo_changelog)

        if self.repos.ponce_repo:
            sbo_table = PonceTable
            sbo_name: str = self.repos.ponce_repo_name
            path_slackbuilds = Path(self.repos.ponce_repo_path, self.repos.ponce_repo_slackbuilds)
            path_changelog: Path = Path(self.repos.ponce_repo_path, self.repos.ponce_repo_changelog)

        slackbuilds_txt: list = self.utils.read_file(path_slackbuilds)

        cache: list = []  # init cache

        print(f"Updating the database for '{self.cyan}{sbo_name}{self.endc}'... ", end='', flush=True)

        for i, line in enumerate(slackbuilds_txt, 1):

            for tag in sbo_tags:
                if line.startswith(tag):
                    line = line.replace(tag, '').strip()
                    cache.append(line)

            if (i % 11) == 0:
                data: str = sbo_table(name=cache[0], location=cache[1].split('/')[1],
                                      files=cache[2], version=cache[3],
                                      download=cache[4], download64=cache[5],
                                      md5sum=cache[6], md5sum64=cache[7],
                                      requires=cache[8], short_description=cache[9])
                self.session.add(data)

                cache: list = []  # reset cache after 11 lines

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=sbo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_slack_data(self) -> None:
        """ Install the data for slackware repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.slack_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE MIRROR:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.slack_repo_path, self.repos.slack_repo_packages)
        path_checksums: Path = Path(self.repos.slack_repo_path, self.repos.slack_repo_checksums)
        path_changelog: Path = Path(self.repos.slack_repo_path, self.repos.slack_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum
        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.slack_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[2]):
                package_location = line.replace(pkg_tag[2], '').strip()
                cache.append(package_location[2:])  # Do not install (.) dot

            if line.startswith(pkg_tag[3]):
                package_size_comp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[4]):
                package_size_uncomp = line.replace(pkg_tag[4], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.slack_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.slack_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_slack_extra_data(self) -> None:
        """ Install the data for slackware extra repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.slack_extra_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE MIRROR:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.slack_extra_repo_path, self.repos.slack_extra_repo_packages)
        path_checksums: Path = Path(self.repos.slack_extra_repo_path, self.repos.slack_extra_repo_checksums)
        path_changelog: Path = Path(self.repos.slack_extra_repo_path, self.repos.slack_extra_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum
        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.slack_extra_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[2]):
                package_location = line.replace(pkg_tag[2], '').strip()
                cache.append(package_location[2:])  # Do not install (.) dot

            if line.startswith(pkg_tag[3]):
                package_size_comp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[4]):
                package_size_uncomp = line.replace(pkg_tag[4], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.slack_extra_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.slack_extra_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_slack_patches_data(self) -> None:
        """ Install the data for slackware patches repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.slack_patches_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE MIRROR:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.slack_patches_repo_path, self.repos.slack_patches_repo_packages)
        path_checksums: Path = Path(self.repos.slack_patches_repo_path, self.repos.slack_patches_repo_checksums)
        path_changelog: Path = Path(self.repos.slack_patches_repo_path, self.repos.slack_patches_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum
        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.slack_patches_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[2]):
                package_location = line.replace(pkg_tag[2], '').strip()
                cache.append(package_location[2:])  # Do not install (.) dot

            if line.startswith(pkg_tag[3]):
                package_size_comp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[4]):
                package_size_uncomp = line.replace(pkg_tag[4], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.slack_patches_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.slack_patches_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_alien_data(self) -> None:
        """ Install the data for alien repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.alien_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE REQUIRED:',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.alien_repo_path, self.repos.alien_repo_packages)
        path_checksums: Path = Path(self.repos.alien_repo_path, self.repos.alien_repo_checksums)
        path_changelog: Path = Path(self.repos.alien_repo_path, self.repos.alien_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append("".join(self.repos.alien_repo_mirror))
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (.) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                required = line.replace(pkg_tag[4], '').strip()
                package_required = required.replace(',', ' ').strip()
                cache.append(package_required)

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 10:
                data: str = BinariesTable(
                    repo=self.repos.alien_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    required=cache[8],
                    description=cache[9],
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.alien_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_multilib_data(self) -> None:
        """ Install the data for multilib repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.multilib_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.multilib_repo_path, self.repos.multilib_repo_packages)
        path_checksums: Path = Path(self.repos.multilib_repo_path, self.repos.multilib_repo_checksums)
        path_changelog: Path = Path(self.repos.multilib_repo_path, self.repos.multilib_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append("".join(self.repos.multilib_repo_mirror))
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                package_description = line.replace(pkg_tag[4], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.multilib_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.multilib_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_restricted_data(self) -> None:
        """ Install the data for multilib repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.restricted_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.restricted_repo_path, self.repos.restricted_repo_packages)
        path_checksums: Path = Path(self.repos.restricted_repo_path, self.repos.restricted_repo_checksums)
        path_changelog: Path = Path(self.repos.restricted_repo_path, self.repos.restricted_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append("".join(self.repos.restricted_repo_mirror))
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                package_description = line.replace(pkg_tag[4], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.restricted_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.restricted_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_gnome_data(self) -> None:
        """ Install the data for gnome repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.gnome_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE MIRROR:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.gnome_repo_path, self.repos.gnome_repo_packages)
        path_checksums: Path = Path(self.repos.gnome_repo_path, self.repos.gnome_repo_checksums)
        path_changelog: Path = Path(self.repos.gnome_repo_path, self.repos.gnome_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.gnome_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[2]):
                package_location = line.replace(pkg_tag[2], '').strip()
                cache.append(package_location[1:])  # Do not install (.) dot

            if line.startswith(pkg_tag[3]):
                package_size_comp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[4]):
                package_size_uncomp = line.replace(pkg_tag[4], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.gnome_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.gnome_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_msb_data(self) -> None:
        """ Install the data for msb repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.msb_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.msb_repo_path, self.repos.msb_repo_packages)
        path_checksums: Path = Path(self.repos.msb_repo_path, self.repos.msb_repo_checksums)
        path_changelog: Path = Path(self.repos.msb_repo_path, self.repos.msb_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append("".join(self.repos.msb_repo_mirror))
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                package_description = line.replace(pkg_tag[4], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.msb_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.msb_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_csb_data(self) -> None:
        """ Install the data for csb repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.csb_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.csb_repo_path, self.repos.csb_repo_packages)
        path_checksums: Path = Path(self.repos.csb_repo_path, self.repos.csb_repo_checksums)
        path_changelog: Path = Path(self.repos.csb_repo_path, self.repos.csb_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append("".join(self.repos.csb_repo_mirror))
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                package_description = line.replace(pkg_tag[4], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.csb_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.csb_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_conraid_data(self) -> None:
        """ Install the data for conraid repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.conraid_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE MIRROR:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.conraid_repo_path, self.repos.conraid_repo_packages)
        path_checksums: Path = Path(self.repos.conraid_repo_path, self.repos.conraid_repo_checksums)
        path_changelog: Path = Path(self.repos.conraid_repo_path, self.repos.conraid_repo_changelog)
        checksums_md5: list = self.utils.read_file(path_checksums)

        packages_txt: list = self.utils.read_file(path_packages)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name: str = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.conraid_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[2]):
                package_location: str = line.replace(pkg_tag[2], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[3]):
                package_size_comp: str = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[4]):
                package_size_uncomp: str = line.replace(pkg_tag[4], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[5]):
                package_description: str = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 9:
                data: str = BinariesTable(
                    repo=self.repos.conraid_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    description=cache[8],
                    required='',
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.conraid_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_slackonly_data(self) -> None:
        """ Install the data for slackonly repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.slackonly_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE REQUIRED:',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.slackonly_repo_path, self.repos.slackonly_repo_packages)
        path_checksums: Path = Path(self.repos.slackonly_repo_path, self.repos.slackonly_repo_checksums)
        path_changelog: Path = Path(self.repos.slackonly_repo_path, self.repos.slackonly_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.slackonly_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                required = line.replace(pkg_tag[4], '').strip()
                package_required = required.replace(',', ' ').strip()
                cache.append(package_required)

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 10:
                data: str = BinariesTable(
                    repo=self.repos.slackonly_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    required=cache[8],
                    description=cache[9],
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.slackonly_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_salixos_data(self) -> None:
        """ Install the data for salixos repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.salixos_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE REQUIRED:',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.salixos_repo_path, self.repos.salixos_repo_packages)
        path_checksums: Path = Path(self.repos.salixos_repo_path, self.repos.salixos_repo_checksums)
        path_changelog: Path = Path(self.repos.salixos_repo_path, self.repos.salixos_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.salixos_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                deps: list = []
                required = line.replace(pkg_tag[4], '').strip()

                for req in required.split(','):
                    dep = req.split('|')
                    if len(dep) > 1:
                        deps.append(dep[1])
                    else:
                        deps += dep

                cache.append(' '.join(deps))

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 10:
                data: str = BinariesTable(
                    repo=self.repos.salixos_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    required=cache[8],
                    description=cache[9],
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.salixos_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_salixos_extra_data(self) -> None:
        """ Install the data for salixos_extra repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.salixos_extra_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE REQUIRED:',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.salixos_extra_repo_path, self.repos.salixos_extra_repo_packages)
        path_checksums: Path = Path(self.repos.salixos_extra_repo_path, self.repos.salixos_extra_repo_checksums)
        path_changelog: Path = Path(self.repos.salixos_extra_repo_path,
                                    self.repos.salixos_extra_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.salixos_extra_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                deps: list = []
                required = line.replace(pkg_tag[4], '').strip()

                for req in required.split(','):
                    dep = req.split('|')
                    if len(dep) > 1:
                        deps.append(dep[1])
                    else:
                        deps += dep

                cache.append(' '.join(deps))

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 10:
                data: str = BinariesTable(
                    repo=self.repos.salixos_extra_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    required=cache[8],
                    description=cache[9],
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.salixos_extra_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_salixos_patches_data(self) -> None:
        """ Install the data for salixos_patches repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.salixos_patches_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE REQUIRED:',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.salixos_patches_repo_path, self.repos.salixos_patches_repo_packages)
        path_checksums: Path = Path(self.repos.salixos_patches_repo_path, self.repos.salixos_patches_repo_checksums)
        path_changelog: Path = Path(self.repos.salixos_patches_repo_path,
                                    self.repos.salixos_patches_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.salixos_patches_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                deps: list = []
                required = line.replace(pkg_tag[4], '').strip()

                for req in required.split(','):
                    dep = req.split('|')
                    if len(dep) > 1:
                        deps.append(dep[1])
                    else:
                        deps += dep

                cache.append(' '.join(deps))

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 10:
                data: str = BinariesTable(
                    repo=self.repos.salixos_patches_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    required=cache[8],
                    description=cache[9],
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.salixos_patches_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_slackel_data(self) -> None:
        """ Install the data for slackel repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.slackel_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE REQUIRED:',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.slackel_repo_path, self.repos.slackel_repo_packages)
        path_checksums: Path = Path(self.repos.slackel_repo_path, self.repos.slackel_repo_checksums)
        path_changelog: Path = Path(self.repos.slackel_repo_path, self.repos.slackel_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.slackel_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                deps: list = []
                required = line.replace(pkg_tag[4], '').strip()

                for req in required.split(','):
                    dep = req.split('|')
                    if len(dep) > 1:
                        deps.append(dep[1])
                    else:
                        deps += dep

                cache.append(' '.join(deps))

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 10:
                data: str = BinariesTable(
                    repo=self.repos.slackel_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    required=cache[8],
                    description=cache[9],
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.slackel_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()

    def install_slint_data(self) -> None:
        """ Install the data for slint repository. """
        print(f"Updating the database for '{self.cyan}{self.repos.slint_repo_name}{self.endc}'... ",
              end='', flush=True)

        checksums_dict: dict = {}
        pkg_tag = [
            'PACKAGE NAME:',
            'PACKAGE LOCATION:',
            'PACKAGE SIZE (compressed):',
            'PACKAGE SIZE (uncompressed):',
            'PACKAGE REQUIRED:',
            'PACKAGE DESCRIPTION:'
        ]
        path_packages: Path = Path(self.repos.slint_repo_path, self.repos.slint_repo_packages)
        path_checksums: Path = Path(self.repos.slint_repo_path, self.repos.slint_repo_checksums)
        path_changelog: Path = Path(self.repos.slint_repo_path, self.repos.slint_repo_changelog)
        packages_txt: list = self.utils.read_file(path_packages)
        checksums_md5: list = self.utils.read_file(path_checksums)

        for line in checksums_md5:
            line = line.strip()

            if line.endswith(('.txz', '.tgz')):
                file: str = line.split('./')[1].split('/')[-1].strip()
                checksum: str = line.split('./')[0].strip()
                checksums_dict[file] = checksum

        cache: list = []  # init cache

        for line in packages_txt:

            if line.startswith(pkg_tag[0]):
                package_name = line.replace(pkg_tag[0], '').strip()
                split_package: list = self.utils.split_binary_pkg(package_name)
                cache.append(split_package[0])  # package name
                cache.append(split_package[1])  # package version
                cache.append(package_name)
                cache.append(self.repos.slint_repo_mirror[0])
                try:
                    cache.append(checksums_dict[package_name])
                except KeyError:
                    cache.append('error checksum')

            if line.startswith(pkg_tag[1]):
                package_location = line.replace(pkg_tag[1], '').strip()
                cache.append(package_location[2:])  # Do not install (./) dot

            if line.startswith(pkg_tag[2]):
                package_size_comp = line.replace(pkg_tag[2], '').strip()
                cache.append(f'{package_size_comp}B')

            if line.startswith(pkg_tag[3]):
                package_size_uncomp = line.replace(pkg_tag[3], '').strip()
                cache.append(f'{package_size_uncomp}B')

            if line.startswith(pkg_tag[4]):
                deps: list = []
                required = line.replace(pkg_tag[4], '').strip()

                for req in required.split(','):
                    dep = req.split('|')
                    if len(dep) > 1:
                        deps.append(dep[1])
                    else:
                        deps += dep

                cache.append(' '.join(deps))

            if line.startswith(pkg_tag[5]):
                package_description = line.replace(pkg_tag[5], '').strip()
                cache.append(package_description)

            if len(cache) == 10:
                data: str = BinariesTable(
                    repo=self.repos.slint_repo_name,
                    name=cache[0],
                    version=cache[1],
                    package=cache[2],
                    mirror=cache[3],
                    checksum=cache[4],
                    location=cache[5],
                    size_comp=cache[6],
                    size_uncomp=cache[7],
                    required=cache[8],
                    description=cache[9],
                    conflicts='',
                    suggests=''
                )

                self.session.add(data)

                cache: list = []  # reset cache

        last_updated: str = self.last_updated(path_changelog)
        date: str = LastRepoUpdated(repo=self.repos.slint_repo_name, date=last_updated)
        self.session.add(date)

        print(f'{self.byellow}Done{self.endc}')

        self.session.commit()
