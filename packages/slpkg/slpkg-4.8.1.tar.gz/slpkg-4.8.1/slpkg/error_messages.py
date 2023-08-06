#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.configs import Configs


class Errors(Configs):

    def __init__(self):
        super(Configs, self).__init__()

    def raise_error_message(self, message: str) -> None:
        """ A general method to raise an error message and exit. """
        raise SystemExit(f"\n{self.prog_name}: {self.bred}Error{self.endc}: {message}.\n")
