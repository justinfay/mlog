"""
Constants which are not configurable are stored in this file.
"""

__all__ = (
    'APPLICATION_NAME',
    'TEMPLATE_DIR',
    'POST',
    'CATEGORY',
    'TAG',
    'STATIC',
    'SCRIPT',
    'IMAGE',
    'STYLE',
    'INDEX')


# Application constants.
APPLICATION_NAME = 'mlog'
TEMPLATE_DIR = 'templates'

# URL segments for specific sections.
POST = 'post'
CATEGORY = 'category'
TAG = 'tag'

# Name of directories for output static files.
STATIC = 'static'
SCRIPT = 'js'
IMAGE = 'img'
STYLE = 'css'

INDEX = 'index.html'
