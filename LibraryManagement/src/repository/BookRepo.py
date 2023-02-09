import pickle

from src.domain.book import Book
from src.repository.RepositoryException import RepositoryException
from src.domain.a10 import SortFilter, filter_function, gnome_sort
import random


class BookRepo:
    def __init__(self):
        self._data = {}
        self._ids = []
        self._iterable = SortFilter()

    def generate_author(self):
        author_list = ["William Shakespeare", "Lev Tolstoi", "Fyodor Dostoevsky", "Charles Dickens", "Victor Hugo",
                       "Mark Twain", "Roald Dahl", "Jules Verne", "Daniel Defoe", "Bram Stoker"]
        return random.choice(author_list)

    def generate_title(self):
        author = self.generate_author()
        shakespeare_list = ["The Merchant of Venice", "A Midsummer Night’s Dream", "Twelfth Night", "Romeo and Juliet",
                            "Macbeth"]
        tolstoi_list = ["Anna Karenina", "War and Peace", "Resurrection", "The Cossacks", "A Confession"]
        dostoevsky_list = ["Crime and Punishment", "The Idiot", "Poor Folk", "The Gambler", "The Brothers Karamazov"]
        dickens_list = ["Great Expectations", "David Copperfield", "Bleak House", "Little Dorrit", "Oliver Twist"]
        hugo_list = ["The Hunchback of Notre-Dame", "Les Miserables", "The Man Who Laughs",
                     "The Last Day of a Condemned Man", "Les Contemplations"]
        twain_list = ["Life on the Mississippi", "The Adventures of Huckleberry Finn", "The Adventures of Tom Sawyer",
                      "The Innocents Abroad", "Tom Sawyer Abroad, By Huck Finn"]
        dahl_list = ["The BFG", "Charlie and the Chocolate Factory", "James and the Giant Peach", "The Witches",
                     "Matilda"]
        verne_list = ["Twenty Thousand Leagues Under the Sea", "Journey To The Center Of The Earth",
                      "Around the World in 80 Days", "The Mysterious Island", "From the Earth to The Moon"]
        defoe_list = ["The Consolidator", "Atlantis Major", "Robinson Crusoe", "Memoirs of a Cavalier",
                      "A Journal of the Plague Year"]
        stoker_list = ["Dracula", "Seven Golden Buttons", "Miss Betty", "The Mystery of the Sea", "The Man"]
        titles_dict = {'William Shakespeare': shakespeare_list, 'Lev Tolstoi': tolstoi_list,
                       'Fyodor Dostoevsky': dostoevsky_list, 'Charles Dickens': dickens_list, 'Victor Hugo': hugo_list,
                       'Mark Twain': twain_list, 'Roald Dahl': dahl_list,
                       'Jules Verne': verne_list, 'Daniel Defoe': defoe_list, 'Bram Stoker': stoker_list}
        return author, random.choice(titles_dict[author])

    def init_list(self):
        """
        initializes the list of books
        """
        i = 0
        while i < 20:
            book_id = random.randint(1, 100)
            author, title = self.generate_title()
            b = Book(book_id, title, author)
            if b.get_id not in self._data.keys():
                self._data[b.get_id] = b
                self._iterable.add(b)
                i += 1

    def add_element(self, book):
        """
        adds an element to the dictionary of books
        """
        if book.get_id < 0:
            raise RepositoryException("Invalid ID!")
        if book.get_id in self._data.keys():
            raise RepositoryException("Duplicate book ID!")
        self._data[book.get_id] = book

    def remove_element(self, book_id):
        """
        removes an element from the dictionary of books
        """
        # if book_id < 0:
        #     raise RepositoryException("Invalid ID!")
        # if book_id in self._data.keys():
        #     self._data.pop(book_id)
        # else:
        #     raise RepositoryException("Book not found.")
        if book_id not in self._data.keys():
            raise RepositoryException("Book not found.")
        book_ids = []
        self._ids.clear()
        self._ids.append(book_id)
        for i in self._data:
            book_ids.append(i)
        filter_function(book_ids, self.book_validation)
        book_list = self.list()
        for i in book_list:
            if i not in book_ids:
                self._data.pop(i)

    def update_element(self, book_id, opt, param):
        """
        updates either the title or the author of a book
        """
        if book_id < 0:
            raise RepositoryException("Invalid ID!")
        ok = 0
        for i in self._data:
            if i == book_id:
                ok = 1
                if opt == 1:
                    self._data[i].set_title(param)
                elif opt == 2:
                    self._data[i].set_author(param)
                else:
                    raise RepositoryException("Invalid option.")
        if ok == 0:
            raise RepositoryException("Book not found.")

    def list(self):
        """
        :return: the dictionary of books
        """
        return self._data

    def book_validation(self, current_id):
        if current_id == self._ids[0]:
            return True
        return False

    def validate_book(self, book_lst, book_id):
        """
        searches for a book in the list of books
        :return: True if the book is found, False if not
        """
        for i in book_lst:
            if book_id == book_lst[i].get_id:
                return True
        return False

    def search_book_id(self, param):
        """
         searches books in the list of books based on their ID
        """
        book_list = self._data
        ok = 0
        for i in book_list:
            if str(param) in str(book_list[i].get_id):
                print(book_list[i])
                ok += 1
        if ok == 0:
            raise RepositoryException("No books were found with this ID.")

    def search_book_title(self, param):
        """
        searches for books in the book list based on their title
        """
        book_list = self._data
        ok = 0
        for i in book_list:
            param1 = str(param)
            param2 = str(book_list[i].get_title)
            if param1.lower() in param2.lower():
                print(book_list[i])
                ok += 1
        if ok == 0:
            raise RepositoryException("No books were found with this title.")

    def search_book_author(self, param):
        """
        searches for books with a specific author in the list of books
        """
        book_list = self._data
        ok = 0
        for i in book_list:
            param1 = str(param)
            param2 = str(book_list[i].get_author)
            if param1.lower() in param2.lower():
                print(book_list[i])
                ok += 1
        if ok == 0:
            raise RepositoryException("No books were found with this author.")


class BookTextFileRepository(BookRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self.save_file()

    def load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            book_id, title, author = line.split(maxsplit=2, sep=',')
            self.add_element(Book(int(book_id), title, author))
        f.close()

    def save_file(self):
        f = open(self._file_name, "wt")
        for book in self._data.values():
            f.write(str(book.get_id) + ',' + book.get_title + ',' + book.get_author + '\n')
        f.close()

    def add_element(self, book):
        super(BookTextFileRepository, self).add_element(book)
        self.save_file()

    def remove_element(self, book_id):
        super(BookTextFileRepository, self).remove_element(book_id)
        self.save_file()

    def update_element(self, book_id, opt, param):
        super(BookTextFileRepository, self).update_element(book_id, opt, param)
        self.save_file()


class BookBinFileRepository(BookRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self.save_file()

    def load_file(self):
        f = open(self._file_name, "rb")
        self._data = pickle.load(f)
        f.close()

    def save_file(self):
        f = open(self._file_name, "wb")
        pickle.dump(self._data, f)
        f.close()

    def add_element(self, book):
        super(BookBinFileRepository, self).add_element(book)
        self.save_file()

    def remove_element(self, book_id):
        super(BookBinFileRepository, self).remove_element(book_id)
        self.save_file()

    def update_element(self, book_id, opt, param):
        super(BookBinFileRepository, self).update_element(book_id, opt, param)
        self.save_file()