import unittest

from mlog.site import _Tree


class TreeTest(unittest.TestCase):
    def setUp(self):
        self.tree = _Tree()

    def test_get_empty(self):
        self.assertEqual(
            self.tree,
            self.tree.get())

    def test_get_one(self):
        self.tree.add(['foo'], 'foo')
        self.assertEqual(
            'foo',
            self.tree.get(['foo']))
        # Test get root still works.
        self.test_get_empty()

    def test_add_multiple_sub(self):
        self.tree.add(['foo', 'bar'], 'foobar')
        self.assertTrue(isinstance(self.tree.get(['foo']), _Tree))
        self.assertEqual('foobar', self.tree.get(['foo', 'bar']))
        self.assertEqual(
            self.tree.get(['foo']).get(['bar']),
            self.tree.get(['foo', 'bar']))

    def test_get_item(self):
        self.tree.add(['foo', 'bar'], 'foobar')
        self.assertTrue(isinstance(self.tree['foo'], _Tree))
        self.assertEqual('foobar', self.tree['foo']['bar'])
        self.assertEqual(
            self.tree.get(['foo'])['bar'],
            self.tree['foo']['bar'])

    def test_del_item(self):
        self.tree.add(['foo'], 'foo')
        self.assertEqual(
            'foo',
            self.tree.get(['foo']))
        # Test get root still works.
        self.test_get_empty()
        del self.tree['foo']
        with self.assertRaises(KeyError):
            self.tree.get(['foo'])
        self.test_get_empty()

    def test_del_sub_trees(self):
        self.tree.add(['foo', 'bar'], 'foobar')
        self.tree.add(['foo', 'bill'], 'foobill')
        self.assertEqual('foobar', self.tree['foo']['bar'])
        self.assertEqual('foobill', self.tree['foo']['bill'])
        del self.tree['foo']['bar']
        self.assertEqual('foobill', self.tree['foo']['bill'])
        with self.assertRaises(KeyError):
            self.tree.get(['foo', 'bar'])

    def test_get_all_paths(self):
        self.tree.add(['foo', 'bar'], 'foobar')
        self.tree.add(['foo', 'bill'], 'foobill')
        self.assertEqual(
            sorted([['foo', 'bar'], ['foo', 'bill']]),
            sorted(list(self.tree.all_paths())))
