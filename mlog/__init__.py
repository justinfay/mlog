"""
A miminmal static blog generator.
"""

import collections
import functools
import pkg_resources
import pathlib
import operator
import re
import shutil
import string
import urllib.parse

import dateutil.parser
import jinja2
import markdown

from .config import blog_config as config
from .constants import *


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


def generate_excerpt(html, length=200):
    """
    Generate an excerpt from a given string of html.
    """
    return '<p>{0}...</p>'.format(
        strip_html(html)[:200])
jinja_env.globals['excerpt'] = generate_excerpt


def make_url(base, *fragments):
    """
    >>> make_url('http://example.com', '1', '2', '3.html')
    'http://example.com/1/2/3.html'
    >>> make_url('http://example.com')
    'http://example.com/'
    """
    path = urllib.parse.quote(str(pathlib.Path(*fragments)).replace(' ', '-'))
    return urllib.parse.urljoin(base, path)
jinja_env.globals['make_site_url'] = functools.partial(make_url, config.BASE_URL)


def create_output_structure(
        base=config.OUTPUT_DIR,
        script=config.SCRIPT_DIR,
        css=config.STYLE_DIR,
        img=config.IMAGE_DIR):
    """
    Create all the output directories needed
    for the blog and copies over any static files.

    WARNING: This will unlink all directories if
    they currently exists.
    """
    shutil.rmtree(str(base), ignore_errors=True)
    base = pathlib.Path(base)
    base.mkdir()

    output_static = base.joinpath(STATIC)
    output_static.mkdir()

    output_css = output_static.joinpath(STYLE)
    shutil.copytree(str(css), str(output_css))

    output_script = output_static.joinpath(SCRIPT)
    shutil.copytree(str(script), str(output_script))

    output_img = output_static.joinpath(IMAGE)
    shutil.copytree(str(img), str(output_img))


class Blog:
    """
    Encapsulates all the blog content
    """

    def __init__(
            self,
            title=config.TITLE,
            description=config.DESCRIPTION,
            post_dir=config.POSTS_DIR):

        self.posts = []
        self.title = title
        self.description = description
        self.post_dir = post_dir

    @property
    def tags(self):
        """
        Retuns a dictionary type where the keys are tags
        and the values are a list of posts tagged with key.
        """
        tags = collections.defaultdict(list)
        for post in self.posts:
            for tag in post['tags']:
                tags[tag.strip()].append(post)
        return tags

    @property
    def categories(self):
        """
        Retuns a dictionary type where the keys are tags
        and the values are a list of posts tagged with key.
        """
        categories = collections.defaultdict(list)
        for post in self.posts:
            for category in post['categories']:
                categories[category.strip()].append(post)
        return categories

    def load_posts(self):
        """
        Load posts from the file system.
        """
        posts = []
        for post in pathlib.Path(self.post_dir).glob('*.md'):
            posts.append(self._load_post(post))
        self.posts = list(sorted(
            posts,
            key=operator.itemgetter('date'),
            reverse=True))  # Chronological order newest first.

    def _load_post(self, path):
        """
        Load the posts from the filesystem markdown files.
        """
        def get_section(section, default=''):
            return ''.join(md.Meta.get(section, default))

        with path.open() as fh:
            html = md.convert(fh.read())
            post = {
                'content': html,
                'title': get_section('title'),
                'description': get_section('description'),
                'tags': [
                    tag.strip()
                    for tag in get_section('tags').split(',')
                    if tag.strip()],
                'categories': [
                    category.strip()
                    for category in get_section('categories').split(',')
                    if category.strip()],
                'author': get_section('author'),
                'date': dateutil.parser.parse(get_section('date')),
                'slug': path.name.replace('.md', '.html'),
            }
        return post


class BlogRenderer:
    """
    Creates the actual template files on disk.
    """

    def __init__(
            self,
            blog,
            posts_per_page=config.POSTS_PER_PAGE,
            output_dir=config.OUTPUT_DIR):

        self.blog = blog
        self.posts_per_page = posts_per_page
        self.output_dir = output_dir

    def render_to_files(self):
        """
        Create a deployable blog of static html pages.
        """
        create_output_structure()
        self._create_post_pages()
        self._create_tag_pages()
        self._create_category_pages()

    def _create_post_list(self, posts, sections=()):
        """
        Creates a stream of blog post snippets.
        """
        template = jinja_env.get_template('post_list.html')
        template_stream = template.stream(
            posts=posts,
            tags=self._create_tag_menu(),
            categories=self._create_category_menu())
        output_file = self.output_dir.joinpath(*sections, INDEX)
        if not output_file.parent.exists():
            output_file.parent.mkdir(parents=True)
        with output_file.open('w') as fh:
            template_stream.dump(fh)

    def _create_post_page(self, post):
        """
        Write a rendered blog post template.
        """
        template = jinja_env.get_template('post.html')
        template_stream = template.stream(
            post=post,
            tags=self._create_tag_menu(),
            categories=self._create_category_menu())
        output_file = self.output_dir.joinpath(POST, post['slug'])
        if not output_file.parent.exists():
            output_file.parent.mkdir(parents=True)
        with output_file.open('w') as fh:
            template_stream.dump(fh)

    def _create_post_pages(self):
        """
        Create the blog post pages.
        """
        self._create_post_list(self.blog.posts)
        for post in self.blog.posts:
            self._create_post_page(post)

    def _create_category_pages(self):
        """
        Create the category pages.
        """
        for category in self.blog.categories:
            posts = [
                post
                for post in self.blog.posts
                if category in post['categories']]
            self._create_post_list(
                posts,
                sections=[CATEGORY, category.replace(' ', '-')])

    def _create_tag_pages(self):
        """
        Create the tag pages.
        """
        for tag in self.blog.tags:
            posts = [
                post
                for post in self.blog.posts
                if tag in post['tags']]
            self._create_post_list(
                posts,
                sections=[TAG, tag.replace(' ', '-')])

    def _create_tag_menu(self):
        """
        Create the tag list.
        """
        # Sort tags by how frequently they are used.
        tags = sorted(
            self.blog.tags.items(),
            key=lambda item: len(item[1]),
            reverse=True)
        return [tag[0] for tag in tags]

    def _create_category_menu(self):
        """
        Create the category list.
        """
        # Sort categories alphabetically.
        categories = sorted(
            self.blog.categories.keys(),
            key=lambda k: string.ascii_lowercase.find(k.lower()),
            reverse=True)
        return categories

    def _create_atom_feed(self):
        raise NotImplementedError()
