import unittest

from lk_urban import DensityUrbanMap, LocalAuthorityUrbanMap


class TestCase(unittest.TestCase):
    def test_all(self):
        for cls in [LocalAuthorityUrbanMap, DensityUrbanMap]:
            with self.subTest(cls=cls):
                cls().render()
