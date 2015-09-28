from itertools import islice
import unittest

from mlog import util


@unittest.mock.patch('mlog.util.strip_html')
def test_generate_excerpt(strip_html):
    strip_html.side_effect = lambda x: x
    assert (
        util.generate_excerpt('a' * 201, length=200) ==
        "<p>{0}...</p>".format('a' * 200))

    assert (
        util.generate_excerpt('a' * 2, length=2) ==
        "<p>{0}...</p>".format('a' * 2))

    assert (
        util.generate_excerpt('a' * 2000, length=400) ==
        "<p>{0}...</p>".format('a' * 400))


def test_make_url():
    assert (
        util.make_url('http://example.com', '1', '2', '3.html') ==
        'http://example.com/1/2/3.html')
    assert (
        util.make_url('http://example.com') ==
        'http://example.com/')


def test_gen_page_names():
    assert(
        ['index.html', '2.html'] ==
        list(islice(util.gen_page_names(), 2)))


@unittest.mock.patch('mlog.util.gen_page_names')
def test_page_names(gen_page_names):
    names = util.page_names(10)
    assert 10 == len(names)


class TestPager(unittest.TestCase):
    def test_page_count(self):
        pager = util.Pager([], 1)
        self.assertEqual(0, pager.page_count)

        pager = util.Pager([1], 1)
        self.assertEqual(1, pager.page_count)

        pager = util.Pager([1, 2], 1)
        self.assertEqual(2, pager.page_count)

        pager = util.Pager([1, 2, 3], 2)
        self.assertEqual(2, pager.page_count)

    def test_get_filename(self):
        pager = util.Pager([1, 2, 3], 2)
        self.assertIsNone(pager._get_filename(-1))
        self.assertIsNone(pager._get_filename(2))
        self.assertEqual('index.html', pager._get_filename(0))
        self.assertEqual('2.html', pager._get_filename(1))
