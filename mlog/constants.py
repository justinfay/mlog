"""
Constants which are not configurable are stored in this file.
"""

import string


__all__ = (
    'APPLICATION_NAME',
    'TEMPLATE_DIR',
    'PAGE',
    'POST',
    'CATEGORY',
    'TAG',
    'STATIC',
    'SCRIPT',
    'IMAGE',
    'STYLE',
    'INDEX',
    'SORT_ORDER')


# Application constants.
APPLICATION_NAME = 'mlog'
TEMPLATE_DIR = 'templates'

# URL segments for specific sections.
PAGE = 'page'
POST = 'post'
CATEGORY = 'category'
TAG = 'tag'

# Name of directories for output static files.
STATIC = 'static'
SCRIPT = 'js'
IMAGE = 'img'
STYLE = 'css'

INDEX = 'index.html'

# Sort order for pages and categories.
SORT_ORDER = string.digits + string.ascii_lowercase
