import mock
import unittest

from mlog import site


class TestSite(unittest.TestCase):
    def setUp(self):
        self.site = site.Site()

    def test_nonexistant(self):
        self.assertRaises(KeyError, self.site.get)

    def test_top_level_get(self):
        content = mock.Mock()
        self.site.post('slug', content)
        self.assertEqual(content, self.site.get('slug'))

    def test_multiple_top_level(self):
        content = mock.Mock()
        content2 = mock.Mock()
        self.site.post('slug', content)
        self.site.post('slug2', content2)
        self.assertEqual(self.site.get('slug'), content)
        self.assertEqual(self.site.get('slug2'), content2)

    def test_nested_level(self):
        content = mock.Mock()
        self.site.post('a/b/c/slug', content)
        self.assertEqual(content, self.site.get('a/b/c/slug'))
        first = self.site.get('a')
        self.assertTrue(isinstance(first, site.Site))
        second = self.site.get('a/b')
        self.assertTrue(isinstance(second, site.Site))
        third = self.site.get('a/b/c')
        self.assertTrue(isinstance(third, site.Site))
        self.assertTrue(
            first.get('b/c/slug') is
            second.get('c/slug') is
            third.get('slug'))
        self.assertTrue(
            self.site.a.b.c.get('slug') is
            first.b.c.get('slug') is
            second.c.get('slug') is
            third.get('slug'))
        self.assertTrue(
            self.site['a']['b']['c'].get('slug') is
            first['b']['c'].get('slug') is
            second['c'].get('slug') is
            third.get('slug'))

    def test_spider(self):
        self.site.post('slug', '')
        self.assertEqual(
            sorted(['slug']),
            sorted(list(self.site.spider())))
        self.site.post('foo/slug', '')
        self.assertEqual(
            sorted(['slug', 'foo/slug']),
            sorted(list(self.site.spider())))
        self.site.post('foo/slug2', '')
        self.assertEqual(
            sorted(['slug', 'foo/slug', 'foo/slug2']),
            sorted(list(self.site.spider())))

    def test_split_path(self):
        self.assertEqual(['a', 'b', 'c'], self.site._split_path('a/b/c'))
        self.assertEqual(['a'], self.site._split_path('/a/'))
        self.assertEqual(['a'], self.site._split_path('////a/'))
        self.assertEqual(['a', 'b'], self.site._split_path('a///b//'))
