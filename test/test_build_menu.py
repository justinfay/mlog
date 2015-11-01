import unittest

from mlog.blog import build_menu


class TestBuildMenu(unittest.TestCase):

    def test_returns_list(self):
        self.assertTrue(isinstance(build_menu([]), list))

    def test_simple_sort(self):
        self.assertEqual(
            [('0', '0'), ('1', '1')],
            build_menu([('1', '1'), ('0', '0')]))

    def test_nested_menu(self):
        self.assertEqual(
            [('0', '0'), ('1', [('0', '1'), ('1', '1')])],
            build_menu([('0', '0'), ('1/0', '1'), ('1/1', '1')]))

    def test_custom_sort(self):
        self.assertEqual(
            [('1', '1'), ('0', '0')],
            build_menu([('0__1', '1'), ('1__0', '0')]))
