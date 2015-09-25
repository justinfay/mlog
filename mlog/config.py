from importlib.machinery import SourceFileLoader
import os

from . import defaults


ENVAR_CONFIG = 'MLOG_CONFIG'


class Config(dict):
    """
    A config object which can update itself via a dict, object or module.

    An element of the dict/object/module is deemed a configuration
    value if its `isupper` method returns `True`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow attribute like access.
        self.__dict__ = self

    def update_from_envar(self, envvar=ENVAR_CONFIG):
        """
        Update the config from a module path specified as an
        environment variable.
        """
        path = os.getenv(envvar)
        if path is not None:
            self.update_from_pyfile(path)

    def update_from_pyfile(self, path):
        """
        Update the config from a python file at the given path.
        """
        user_conf = SourceFileLoader('user_conf', path).load_module()
        self.update(user_conf)

    def update(self, obj):
        """
        Update the config dictionary either from a dict or
        an object.
        """
        if isinstance(obj, dict):
            for key in obj.keys():
                if key.isupper():
                    self[key] = obj[key]
        else:
            for key in dir(obj):
                if key.isupper():
                    self[key] = getattr(obj, key)


blog_config = Config()
blog_config.update(defaults)
blog_config.update_from_envar()
