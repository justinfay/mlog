import unittest
import unittest.mock

import mlog


class TestRender(unittest.TestCase):

    def setUp(self):
        blog = unittest.mock.Mock(categories={
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
