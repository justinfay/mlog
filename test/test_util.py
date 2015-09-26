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
