import functools
import pathlib
import shutil

from .config import blog_config as config
from .constants import *  # noqa
from . import util


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


class _Renderer:
    """
    Generic renderer class. Maintains a class mapping
    of types to templates.
    """
    _templates = {}

    def __init__(self, default_template=None):
        if default_template is not None:
            self._templates[None] = default_template

    def _find_template(self, content):
        template = next((
            key
            for key in self._templates
            if isinstance(content, type(key))
            and isinstance(key, type(content))),
            None)
        return self._templates[template]


class Renderer:
    """
    Creates the actual template files on disk.
    """

    def __init__(
            self,
            blog,
            posts_per_page=config.POSTS_PER_PAGE,
            output_dir=config.OUTPUT_DIR,
            template_env=util.jinja_env):

        self.blog = blog
        self.posts_per_page = posts_per_page
        self.output_dir = output_dir
        self.template_env = template_env
        self.template_env.globals.update(self.template_env_globals)

    @property
    def template_env_globals(self):
        return {
            'category_menu': self._create_category_menu,
            'page_menu': self._create_page_menu,
            'site_url': config.BASE_URL,
            'site_description': self.blog.description,
            'site_title': self.blog.title,
            'POST': POST,
            'PAGE': PAGE,
            'CATEGORY': CATEGORY,
            'TAG': TAG,
            'STATIC': STATIC,
            'STYLE': STYLE,
            'excerpt': util.generate_excerpt,
            'make_site_url': functools.partial(util.make_url, config.BASE_URL),
        }

    def render_to_files(self):
        """
        Create a deployable blog of static html pages.
        """
        create_output_structure()
        self._create_post_pages()
        self._create_page_pages()
        self._create_tag_pages()
        self._create_category_pages()

    def _create_post_list(self, posts, sections=()):
        """
        Creates a stream of blog post snippets.
        """
        template = self.template_env.get_template('post_list.html')
        pager = util.Pager(posts, self.posts_per_page)

        for index in range(pager.page_count):
            context = pager.page_context(index)
            template_stream = template.stream(
                context=context,
                sections=sections)

            output_file = self.output_dir.joinpath(
                *sections, context['file_name'])
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with output_file.open('w') as fh:
                template_stream.dump(fh)

    def _create_post_page(self, post):
        """
        Write a rendered blog post template.
        """
        template = self.template_env.get_template('post.html')
        template_stream = template.stream(post=post)
        output_file = self.output_dir.joinpath(POST, post['slug'])
        if not output_file.parent.exists():
            output_file.parent.mkdir(parents=True)
        with output_file.open('w') as fh:
            template_stream.dump(fh)

    def _create_page_page(self, page):
        """
        Write a rendered page.
        """
        template = self.template_env.get_template('page.html')
        template_stream = template.stream(page=page)
        output_file = self.output_dir.joinpath(PAGE, page['slug'])
        if not output_file.parent.exists():
            output_file.parent.mkdir(parents=True)
        with output_file.open('w') as fh:
            template_stream.dump(fh)

    def _create_page_menu(self):
        """
        Return a list of two tuples containing the page_menu item
        and slug for the page.
        """
        return list(sorted([
            (page['menu_name'], page['slug'])
            for page in self.blog.pages],
            key=lambda page: SORT_ORDER.find(page[0][0].lower())))

    def _create_post_pages(self):
        """
        Create the blog post pages.
        """
        self._create_post_list(self.blog.posts)
        for post in self.blog.posts:
            self._create_post_page(post)

    def _create_page_pages(self):
        """
        Create the static pages.
        """
        for page in self.blog.pages:
            self._create_page_page(page)

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

    def _create_category_menu(self):
        """
        Create the category list.
        """
        # Sort categories alphabetically.
        categories = sorted(
            self.blog.categories.keys(),
            key=lambda k: SORT_ORDER.find(k[0].lower()))
        return categories

    def _create_atom_feed(self):
        raise NotImplementedError()
