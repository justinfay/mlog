import functools
import math
import pathlib
import re
import urllib.parse

import dateutil.parser
import jinja2
import markdown

from .config import blog_config as config
from .constants import *  # noqa


MARKDOWN_EXTENSIONS = ['markdown.extensions.meta']
md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)


def strip_html(html):
    """
    Strip well formed HTML tags from text.

    This is woefully inadequate but may do as a
    temporary stop-gap until a better solution
    can be implemented.
    """
    match = re.compile(r'<[^>]*>')
    return match.sub('', html)


def generate_excerpt(html, length=config.EXCERPT_CHAR_COUNT):
    """
    Generate an excerpt from a given string of html.
    """
    return '<p>{0}...</p>'.format(
        strip_html(html)[:length])


def make_url(base, *fragments):
    """
    Construct a well formed url
    """
    path = urllib.parse.quote(str(pathlib.Path(*fragments)).replace(' ', '-'))
    return urllib.parse.urljoin(base, path)


def get_section(section, default='', split=None):
    """
    Return a metadta section from a markdown document.
    If the optional `split` argument is provided
    return a list which is split.
    """
    section = ''.join(md.Meta.get(section, default))
    if split is not None:
        section = [
            element.strip()
            for element in section.split(split)
            if element.strip()]
    return section


def read_post(path):
    """
    Read a blog post from a given file.
    """
    with path.open() as fh:
        html = md.convert(fh.read())
        post = {
            'content': html,
            'title': get_section('title'),
            'description': get_section('description'),
            'tags': get_section('tags', split=','),
            'categories': get_section('categories', split=','),
            'menu_name': get_section('menu_name'),
            'author': get_section('author'),
            'date': dateutil.parser.parse(get_section('date')),
            'slug': path.name.replace('.md', '.html'),
        }
    if not post['description']:
        post['description'] = excerpt(post['content'])
    return post


def gen_page_names():
    """
    Generator function which yields consecutive page names.
    """
    yield INDEX
    next_ = 2
    while True:
        yield "{0}.html".format(next_)
        next_ += 1


def page_names(count):
    """
    Return `count` amount of sequential page names.
    """
    gen = gen_page_names()
    return [next(gen) for _ in range(count)]


class Pager:
    """
    Helper class for creating next/prev links on list pages.

    TODO: Rethink this class.
    """

    def __init__(self, items, per_page):
        self._items = items
        self._per_page = per_page
        self._page_names = page_names(self.page_count)

    def page_context(self, page_index):
        """
        Return a context dict for the given page index.
        """
        return {
            'items': self._items_for_page(page_index),
            'next': self._get_filename(page_index + 1),
            'prev': self._get_filename(page_index - 1),
            'file_name': self._get_filename(page_index),
        }

    def _items_for_page(self, page_index):
        """
        The items for page with given index.
        """
        start = page_index * self._per_page
        return self._items[start:start + self._per_page]

    @property
    def page_count(self):
        """
        Return the total amount of pages.
        """
        return math.ceil(len(self._items) / self._per_page)

    def _get_filename(self, page_index):
        if 0 > page_index or page_index >= self.page_count:
            return
        return self._page_names[page_index]


if config.TEMPLATE_DIR is None:
    template_loader = jinja2.PackageLoader(APPLICATION_NAME, TEMPLATE_DIR)
else:
    template_loader = jinja2.FileSystemLoader(config.TEMPLATE_DIR)

jinja_env = jinja2.Environment(loader=template_loader)
jinja_env.globals['site_url'] = config.BASE_URL
jinja_env.globals['site_description'] = config.DESCRIPTION
jinja_env.globals['site_title'] = config.TITLE
jinja_env.globals['POST'] = POST
jinja_env.globals['PAGE'] = PAGE
jinja_env.globals['CATEGORY'] = CATEGORY
jinja_env.globals['TAG'] = TAG
jinja_env.globals['STATIC'] = STATIC
jinja_env.globals['STYLE'] = STYLE
jinja_env.globals['excerpt'] = generate_excerpt
jinja_env.globals['make_site_url'] = functools.partial(
    make_url, config.BASE_URL)
