"""
Default configuration values for mlog.

Create you own config file to override these.
"""


import pathlib
import pkg_resources

from .constants import *  # noqa


# Specifies to use the templates packaged with mlog.
TEMPLATE_DIR = None

# Base static directory.
STATIC_DIR = pathlib.Path(
    pkg_resources.resource_filename(APPLICATION_NAME, 'static'))

# CSS styles directory.
STYLE_DIR = STATIC_DIR.joinpath('css')

# scripts directory.
SCRIPT_DIR = STATIC_DIR.joinpath('js')

# Images directory.
IMAGE_DIR = STATIC_DIR.joinpath('img')

# The amount of posts to display per page.
POSTS_PER_PAGE = 5

# The amount of character to use in the excerpt.
EXCERPT_CHAR_COUNT = 200

# Assume blog posts to be in the CWD.
POSTS_DIR = pathlib.Path('posts')

# Assume pages to be in the CWD.
PAGES_DIR = pathlib.Path('pages')

# Output directory for compiled html files.
OUTPUT_DIR = pathlib.Path('html')

# The public url of the site
BASE_URL = 'http://zyppa.com:8000/'

# Meta information for the blog.
TITLE = 'mlog static blog platform'
DESCRIPTION = 'mlog static blog platform for python'
