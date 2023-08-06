#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.utilities import Utilities
from slpkg.binaries.required import Required
from slpkg.sbos.dependencies import Requires
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class LoggingDeps:
    """ Logging installed dependencies. """

    def __init__(self, flags: list, data: dict):
        __slots__ = 'flags', 'data'
        self.flags: list = flags
        self.data: dict = data

        self.utils = Utilities()
        self.session = Session

        self.option_for_binaries: bool = self.utils.is_option(
            ['-B', '--bin-repo='], flags)

    def logging(self, name: str) -> None:
        exist = self.session.query(LogsDependencies.name).filter(
            LogsDependencies.name == name).first()

        if self.option_for_binaries:
            requires: list = Required(self.data, name).resolve()
        else:
            requires: list = Requires(self.data, name).resolve()

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
