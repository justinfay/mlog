import collections
import operator
import pathlib

from . import util
from .config import blog_config as config


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
                tags[tag].append(post)
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
