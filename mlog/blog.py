import collections
import operator
import pathlib

import dateutil.parser

from .config import blog_config as config
from .util import md


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
