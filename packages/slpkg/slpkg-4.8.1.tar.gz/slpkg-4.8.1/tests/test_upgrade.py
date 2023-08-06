import unittest

from slpkg.upgrade import Upgrade
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.binaries.queries import BinQueries


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.utils = Utilities()
        self.sbo_queries = SBoQueries()
        self.data: dict = self.sbo_queries.repository_data()

    def test_installed_is_upgradable_for_sbo_repository(self):
        flags: list = []
        packages: list = ['sbo-create', 'ptpython', 'pycharm', 'powerline-status']

        for pkg in packages:
            self.assertFalse(False, Upgrade(flags, self.data).is_package_upgradeable(pkg))

    def test_installed_is_upgradable_for_slack_patches_repository(self):
        repo: str = 'slack_patches'
        bin_queries = BinQueries(repo)
        data: dict = bin_queries.repository_data()
        flags: list = ['-B', '--bin-repo=']
        packages: list = ['vim', 'httpd', 'seamonkey', 'sudo', 'python3', 'qt5', 'php']

        for pkg in packages:
            self.assertFalse(False, Upgrade(flags, data).is_package_upgradeable(pkg))

    def test_installed_is_upgradable_for_alien_repository(self):
        repo: str = 'alien'
        bin_queries = BinQueries(repo)
        data: dict = bin_queries.repository_data()
        flags: list = ['-B', '--bin-repo=']
        packages: list = ['audacity', 'vlc', 'dnspython']

        for pkg in packages:
            self.assertFalse(False, Upgrade(flags, data).is_package_upgradeable(pkg))


if __name__ == '__main__':
    unittest.main()
