import unittest
from slpkg.binaries.queries import BinQueries


class TestBinQueries(unittest.TestCase):

    def setUp(self):
        self.bin_queries = BinQueries('slack')
        self.repo_data = self.bin_queries.repository_data()
        self.repos_data = self.bin_queries.repositories_data()

    def test_repository_data(self):
        self.assertGreater(len(list(self.repo_data.keys())), 1)

    def test_repositories_data(self):
        self.assertGreater(len(list(self.repos_data.keys())), 1)

    def test_package_name(self):
        self.assertTrue(True, self.repo_data.get('aaa_base'))

    def test_version(self):
        self.assertEqual('15.0', self.repo_data['aaa_base'][0])

    def test_package_bin(self):
        self.assertEqual('aaa_base-15.0-x86_64-3.txz', self.repo_data['aaa_base'][1])

    def test_mirror(self):
        self.assertEqual('https://slackware.uk/slackware/slackware64-15.0/', self.repo_data['aaa_base'][2])

    def test_location(self):
        self.assertEqual('slackware64/a', self.repo_data['aaa_base'][3])

    def test_size_comp(self):
        self.assertEqual('12 KB', self.repo_data['aaa_base'][4])

    def test_size_uncomp(self):
        self.assertEqual('90 KB', self.repo_data['aaa_base'][5])

    def test_required(self):
        self.assertEqual('', self.repo_data['aaa_base'][6])

    def test_conflicts(self):
        self.assertEqual('', self.repo_data['aaa_base'][7])

    def test_suggests(self):
        self.assertEqual('', self.repo_data['aaa_base'][8])

    def test_description(self):
        self.assertEqual('', self.repo_data['aaa_base'][9])

    def test_package_checksum(self):
        self.assertEqual('ee674755e75a3f9cb3c7cfc0039f376d', self.repo_data['aaa_base'][10])


if __name__ == '__main__':
    unittest.main()
