import collections
import operator
import pathlib

from . import util
from .config import blog_config as config
from .constants import *  # noqa
from .site import PathTree


def build_menu(items):
    """
    Return a list of two tuples representing a menu.
    The returned list can contain nested lists of the same
    structure representing sub menus.

    Items should be a list of two tuples containing label
    and slug. This label contain a `/` character to specify
    sub menus.

    The items sorted by the label, 0-z case insensitive.

    To provide a custom menu order prefix each part of the
    label can be prefixed with a hidden character and then
    the characters '__' (double underscore). When displaing
    the label with be stripped up to the first char after '__'.
    """
    menu_tree = PathTree()
    for label, slug in items:
        menu_tree.post(label, slug)
    menu_items = flatten(menu_tree.parent_items())
    sorted_menu = menu_sort(menu_items)
    return sorted_menu


def menu_sort(menu_items):
    sub_sorted = []
    for elem in menu_items:
        if isinstance(elem[1], list):
            sub_sorted.append((elem[0], menu_sort(elem[1])))
        else:
            sub_sorted.append(elem)
    menu_sorted = sorted(
        sub_sorted,
        key=lambda x: SORT_ORDER.find(x[0][0]))
    return [
        (next(reversed(elem[0].split('__', 1))), elem[1])
        for elem in menu_sorted]


def flatten(items):
    menu = []
    for item in items:
        if isinstance(item[1], PathTree):
            menu.append((item[0], flatten(item[1].parent_items())))
        else:
            menu.append(item)
    return menu


class Blog:
    """
    Encapsulates all the blog content
    """

    def __init__(
            self,
            title=config.TITLE,
            description=config.DESCRIPTION,
            post_dir=config.POSTS_DIR,
            page_dir=config.PAGES_DIR):

        self.posts = []
        self.pages = []
        self.title = title
        self.description = description
        self.post_dir = post_dir
        self.page_dir = page_dir

    @classmethod
    def load(cls, *args, **kwargs):
        """
        Alternate init method which will also load
        the blog content.
        """
        obj = cls(*args, **kwargs)
        obj.load_posts()
        obj.load_pages()
        return obj

    @property
    def tags(self):
        """
        Retuns a dictionary type where the keys are tags
        and the values are a list of posts tagged with key.
        """
        tags = collections.defaultdict(list)
        for post in self.posts:
            for tag in post['tags']:
                tags[tag].append(post)
        return tags

    @property
    def categories(self):
        """
        Retuns a dictionary type where the keys are categories
        and the values are a list of posts within that category.
        """
        categories = collections.defaultdict(list)
        for post in self.posts:
            for category in post['categories']:
                categories[category].append(post)
        return categories

    def load_posts(self):
        """
        Load posts from the file system.
        """
        posts = []
        for post in pathlib.Path(self.post_dir).glob('*.md'):
            posts.append(util.read_post(post))
        self.posts = list(sorted(
            posts,
            key=operator.itemgetter('date'),
            reverse=True))  # Chronological order newest first.

    def load_pages(self):
        """
        Load static pages from the file system.
        """
        pages = []
        for path in pathlib.Path(self.page_dir).glob('*.md'):
            pages.append(util.read_post(path))
        self.pages = list(sorted(
            pages,
            key=lambda k: SORT_ORDER.find(k['menu_name'][0].lower())))
