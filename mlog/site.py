class Site:
    """
    A website.
    """

    def __init__(self):
        self._site = {}

    def get(self, uri=''):
        """
        Get the content at `uri`.
        """
        response = self._site
        for part in self._parts(uri):
            response = response[part]
        return response

    def post(self, content, uri):
        """
        Put the content at the given URI
        """
        head, tail = self._split(uri)
        if tail is None:
            self._site[head] = content
        else:
            site = self._site.setdefault(head, Site())
            site.post(content, tail)

    def spider(self):
        """
        Generator for all urls belonging to this site.
        """
        for key in self._site:
            if isinstance(self._site[key], Site):
                for fragment in self._site[key].spider():
                    yield self._join(key, fragment)
            else:
                yield key

    def __str__(self):
        return 'Website:\n    ' + '\n    '.join(self.spider())

    def _split(self, uri):
        """
        Return the parent path and the tail.
        """
        if '/' in uri:
            return uri.split('/', 1)
        return [uri, None]

    def __getattr__(self, attr):
        return self._site[attr]

    def __getitem__(self, item):
        return self._site[item]

    def _parts(self, uri):
        return [
            part
            for part in uri.split('/')
            if part] or ['']

    def _join(self, *parts):
        return '/'.join(
            part
            for part in parts
            if part)
