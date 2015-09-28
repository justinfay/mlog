import datetime
import unittest
import unittest.mock

import mlog


class TestBlog(unittest.TestCase):

    def setUp(self):
        self.blog = mlog.Blog(
            title='test title',
            description='test description',
            post_dir='foo')

    def test_empty_posts(self):
        self.assertEqual([], self.blog.posts)

    def test_duplicate_tags(self):
        post_1 = {'tags': [1, 2]}
        post_2 = {'tags': [1, 3]}
        self.blog.posts = [post_1, post_2]
        self.assertEqual({
            1: [post_1, post_2],
            2: [post_1],
            3: [post_2],
        }, self.blog.tags)

    def test_duplicate_categories(self):
        post_1 = {'categories': [1, 2]}
        post_2 = {'categories': [1, 3]}
        self.blog.posts = [post_1, post_2]
        self.assertEqual({
            1: [post_1, post_2],
            2: [post_1],
            3: [post_2],
        }, self.blog.categories)

    @unittest.mock.patch('mlog.blog.util.read_post')
    @unittest.mock.patch('mlog.blog.util.pathlib.Path')
    def test_load_posts_ordering(self, Path, read_post):
        post_1 = {'date': datetime.datetime(2001, 2, 1)}
        post_2 = {'date': datetime.datetime(2005, 2, 1)}
        read_post.side_effect = [post_1, post_2]
        Path.return_value = unittest.mock.Mock(
            glob=unittest.mock.Mock(return_value=[1, 2]))
        self.blog.load_posts()
        self.assertEqual(
            [post_2, post_1],
            self.blog.posts)

    @unittest.mock.patch('mlog.blog.util.read_post')
    @unittest.mock.patch('mlog.blog.util.pathlib.Path')
    def test_load_page_ordering(self, Path, read_post):
        page_1 = {'menu_name': 'about'}
        page_2 = {'menu_name': 'zzz'}
        read_post.side_effect = [page_1, page_2]
        Path.return_value = unittest.mock.Mock(
            glob=unittest.mock.Mock(return_value=[1, 2]))
        self.blog.load_pages()
        self.assertEqual(
            [page_1, page_2],
            self.blog.pages)
        page_1 = {'menu_name': 'xabout'}
        page_2 = {'menu_name': 'azzz'}
        read_post.side_effect = [page_1, page_2]
        self.blog.load_pages()
        self.assertEqual(
            [page_2, page_1],
            self.blog.pages)

        page_1 = {'menu_name': '1about'}
        page_2 = {'menu_name': '0zzz'}
        read_post.side_effect = [page_1, page_2]
        self.blog.load_pages()
        self.assertEqual(
            [page_2, page_1],
            self.blog.pages)
