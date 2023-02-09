from src.domain.book import Book


class BookService:
    def __init__(self, book_repo):
        self._books = book_repo

    def add_book(self, book_id, title, author):
        """
        creates a book and calls the add_element function from repo
        """
        b = Book(book_id, title, author)
        self._books.add_element(b)

    def remove_book(self, book_id):
        """
        removes a book from the dictionary
        :param book_id: id of the book that is going to be removed
        """
        self._books.remove_element(book_id)

    def update_book(self, book_id, opt, param):
        """
        updates either the title or the author of a book
        :param opt: 1 for title, 2 for author
        :param param: new value
        """
        self._books.update_element(book_id, opt, param)

    def list(self):
        """
        :return: dictionary of books
        """
        return self._books.list()

    def validate_book(self, book_lst, book_id):
        """
        looks for a book in the book list
        :return: True if the book can be found, False if not
        """
        return self._books.validate_book(book_lst, book_id)

    def init_list(self):
        """
        calls the function that generates the list of books
        """
        return self._books.init_list()

    def search_book_id(self, param):
        """
        calls the book ID search function from Repo
        """
        self._books.search_book_id(param)

    def search_book_title(self, param):
        """
        calls the book title search function from Repo
        """
        self._books.search_book_title(param)

    def search_book_author(self, param):
        """
        calls the book author search function from Repo
        """
        self._books.search_book_author(param)
