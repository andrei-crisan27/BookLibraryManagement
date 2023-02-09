class RepositoryException(Exception):
    def __init__(self, key):
        self._key = key

    def __str__(self):
        return str(self._key)

