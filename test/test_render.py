import unittest
import mock

import mlog


class TestRender(unittest.TestCase):

    def setUp(self):
        blog = mock.Mock(categories={
            'b': '',
            'x': '',
            'a': '',
            '0': '',
            '9': '',
        })
        self.renderer = mlog.render.Renderer(blog)

    def test_categories_sorting(self):
        self.assertEqual(
            ['0', '9', 'a', 'b', 'x'],
            self.renderer._create_category_menu())


class Test_Render(unittest.TestCase):

    def setUp(self):
        mlog.render._Renderer._templates = {}
        self.renderer = mlog.render._Renderer()

    def test_default_template(self):
        renderer = mlog.render._Renderer(default_template='foo')
        self.assertEqual(
            'foo',
            renderer._find_template(mock.Mock()))

    def test_no_default_template(self):
        with self.assertRaises(KeyError):
            self.renderer._find_template(mock.Mock())
