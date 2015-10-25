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
        self.site.post(content, 'slug')
        self.assertEqual(content, self.site.get('slug'))

    def test_multiple_top_level(self):
        content = mock.Mock()
        content2 = mock.Mock()
        self.site.post(content, uri='slug')
        self.site.post(content2, uri='slug2')
        self.assertEqual(content, self.site.get('slug'))
        self.assertEqual(content2, self.site.get('slug2'))

    def test_nested_level(self):
        content = mock.Mock()
        self.site.post(content, 'a/b/c/slug')
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
        self.site.post(mock.Mock(), uri='slug')
        self.assertEqual(
            sorted(['slug']),
            sorted(list(self.site.spider())))
        self.site.post(mock.Mock(), 'foo/slug')
        self.assertEqual(
            sorted(['slug', 'foo/slug']),
            sorted(list(self.site.spider())))
        self.site.post(mock.Mock(), 'foo/slug2')
        self.assertEqual(
            sorted(['slug', 'foo/slug', 'foo/slug2']),
            sorted(list(self.site.spider())))

    def test_parts(self):
        self.assertEqual(['a', 'b', 'c'], self.site._parts('a/b/c'))
        self.assertEqual([''], self.site._parts(''))
        self.assertEqual(['a'], self.site._parts('/a/'))
        self.assertEqual(['a'], self.site._parts('////a/'))
        self.assertEqual(['a', 'b'], self.site._parts('a///b//'))

    def test_join(self):
        self.assertEqual('a/b/c', self.site._join('a', 'b', 'c'))
