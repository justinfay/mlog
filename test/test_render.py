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
        self.template_writer = mock.Mock()
        self.renderer = mlog.render._Renderer(self.template_writer)

    def test_no_default_template(self):
        with self.assertRaises(KeyError):
            self.renderer._find_template(mock.Mock())

    def test_find_template(self):
        content = mock.Mock()
        self.renderer.register_template(type(content), 'template')
        self.assertEqual(
            'template',
            self.renderer._find_template(content))

    def test_render(self):
        self.renderer._get_fh = mock.Mock()
        content = mock.Mock()
        self.renderer.register_template(type(content), 'template')
        self.renderer.render('/foo/bar', content)
        self.renderer._get_fh.assert_called_with('/foo/bar')
        self.template_writer.called  # TODO: check args.
