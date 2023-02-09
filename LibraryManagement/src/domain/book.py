class Book:
    def __init__(self, book_id, title, author):
        self._book_id = book_id
        self._title = title
        self._author = author

    @property
    def get_id(self):
        return self._book_id

    def set_id(self, new):
        self._book_id = new

    @property
    def get_title(self):
        return self._title

    def set_title(self, new):
        self._title = new

    @property
    def get_author(self):
        return self._author

    def set_author(self, new):
        self._author = new

    def __repr__(self):
        return "'"+ str(self._title) + "' by " + str(self._author) + " with ID " + str(self._book_id)
