import pathlib
import shutil
import string

from .config import blog_config as config
from .constants import *  # noqa
from .util import jinja_env


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


class Renderer:
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
        output_file = self.output_dir.joinpath(*sections, INDEX)  # noqa
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
