import functools
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
    >>> make_url('http://example.com', '1', '2', '3.html')
    'http://example.com/1/2/3.html'
    >>> make_url('http://example.com')
    'http://example.com/'
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
            'author': get_section('author'),
            'date': dateutil.parser.parse(get_section('date')),
            'slug': path.name.replace('.md', '.html'),
        }
    if not post['description']:
        post['description'] = excerpt(post['content'])
    return post


if config.TEMPLATE_DIR is None:
    template_loader = jinja2.PackageLoader(APPLICATION_NAME, TEMPLATE_DIR)
else:
    template_loader = jinja2.FileSystemLoader(config.TEMPLATE_DIR)

jinja_env = jinja2.Environment(loader=template_loader)
jinja_env.globals['site_url'] = config.BASE_URL
jinja_env.globals['site_description'] = config.DESCRIPTION
jinja_env.globals['site_title'] = config.TITLE
jinja_env.globals['POST'] = POST
jinja_env.globals['CATEGORY'] = CATEGORY
jinja_env.globals['TAG'] = TAG
jinja_env.globals['STATIC'] = STATIC
jinja_env.globals['STYLE'] = STYLE
jinja_env.globals['excerpt'] = generate_excerpt
jinja_env.globals['make_site_url'] = functools.partial(
    make_url, config.BASE_URL)
