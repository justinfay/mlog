class _Tree:
    """
    A tree data srtucture.
    """

    def __init__(self):
        self._tree = {}

    def get(self, path=()):
        """
        Return an element in the tree at the given path.
        path is given as a list of nodes starting from the
        root.
        """

        response = self
        for segment in path:
            response = response._tree[segment]
        return response

    def add(self, path, item):
        """
        Add the given item to the tree at path.
        """
        head, *tail = path
        if not tail:
            self._tree[head] = item
        else:
            sub_tree = self._tree.setdefault(head, self.__class__())
            sub_tree.add(tail, item)

    def __getattr__(self, attr):
        try:
            return self._tree[attr]
        except KeyError:
            raise AttributeError

    def __getitem__(self, item):
        return self._tree[item]

    def __delitem__(self, item):
        del self._tree[item]

    def parent_items(self):
        return self._tree.items()

    def paths(self):
        """
        Return all paths from the root to items.
        """
        for key in self._tree:
            if isinstance(self._tree[key], _Tree):
                for fragment in self._tree[key].paths():
                    yield [key, *fragment]
            else:
                yield [key]


class PathTree(_Tree):
    """
    A tree that uses file type paths for paths.
    """

    def get(self, uri=''):
        """
        Get the content at `uri`.
        """
        return super().get(self._split_path(uri))

    def post(self, uri, content):
        """
        Put the content at the given URI
        """
        self.add(self._split_path(uri), content)

    def spider(self):
        """
        Generator for all urls belonging to this site.
        """
        return (
            self._join_path(path)
            for path in self.paths())

    def _join_path(self, path):
        return '/'.join(path)

    def _split_path(self, path):
        return [
            fragment
            for fragment in path.split('/')
            if fragment] or ['']

    def __str__(self):
        return 'Website:\n    ' + '\n    '.join(self.spider())
