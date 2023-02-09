import unittest

from src.domain.book import Book
from src.domain.client import Client
from src.domain.rental import Rental
from src.repository.BookRepo import BookRepo
from src.repository.ClientRepo import ClientRepo
from src.repository.RentalsRepo import RentalsRepo

class BookRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self._book_repo = BookRepo()

    def tearDown(self) -> None:
        pass

    def test_repo_add_one(self):
        """
        test for repo book add
        """
        book = Book(101, "Luceafarul", "Mihai Eminescu")
        self._book_repo.add_element(book)
        book_list = self._book_repo.list()
        self.assertEqual(book_list[101].get_title, "Luceafarul")
        self.assertEqual(book_list[101].get_author, "Mihai Eminescu")

    def test_repo_remove_one(self):
        """
        test for repo book remove
        """
        book = Book(101, "Luceafarul", "Mihai Eminescu")
        self._book_repo.add_element(book)
        book_list = self._book_repo.list()
        self.assertEqual(book_list[101].get_title, "Luceafarul")
        len1 = len(self._book_repo.list())
        self._book_repo.remove_element(101)
        len2 = len(self._book_repo.list())
        self.assertEqual(len1, len2+1)

    def test_repo_update(self):
        """
        test for repo book update
        """
        book = Book(101, "Luceafarul", "Mihai Eminescu")
        self._book_repo.add_element(book)
        self._book_repo.update_element(101, 1, "Sleepy Birds")
        book_list = self._book_repo.list()
        self.assertEqual(book_list[101].get_title, "Sleepy Birds")
        self._book_repo.update_element(101, 2, "Ion Creanga")
        self.assertEqual(book_list[101].get_author, "Ion Creanga")

    def test_validate_book(self):
        """
        test for repo book validate
        """
        book = Book(101, "Luceafarul", "Mihai Eminescu")
        self._book_repo.add_element(book)
        book_list = self._book_repo.list()
        self.assertEqual(self._book_repo.validate_book(book_list, 101), True)


class ClientRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self._client_repo = ClientRepo()

    def tearDown(self) -> None:
        pass

    def test_client_add(self):
        """
        test for repo client add
        """
        client = Client(101, "John Michael")
        self._client_repo.add_element(client)
        client_list = self._client_repo.list()
        self.assertEqual(client_list[101].get_id, 101)
        self.assertEqual(client_list[101].get_name, "John Michael")

    def test_client_remove(self):
        """
        test for repo client remove
        """
        client = Client(101, "John Michael")
        self._client_repo.add_element(client)
        client_list = self._client_repo.list()
        self.assertEqual(client_list[101].get_name, "John Michael")
        len1 = len(self._client_repo.list())
        self._client_repo.remove_element(101)
        len2 = len(self._client_repo.list())
        self.assertEqual(len1, len2+1)

    def test_client_update(self):
        """
        test for repo client update
        """
        client = Client(101, "John Michael")
        self._client_repo.add_element(client)
        client_list = self._client_repo.list()
        self.assertEqual(client_list[101].get_name, "John Michael")
        self._client_repo.update_client(101, "John")
        self.assertEqual(client_list[101].get_name, "John")

    def test_validate_client(self):
        """
        test for repo client validate
        """
        client = Client(101, "Mihai Eminescu")
        self._client_repo.add_element(client)
        client_list = self._client_repo.list()
        self.assertEqual(self._client_repo.validate_client(client_list, 101), True)


class RentalsRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self._rentals_repo = RentalsRepo()

    def tearDown(self) -> None:
        pass

    def test_rentals_add(self):
        """
        test for repo rentals add
        """
        rental = Rental(101, 101, 57, 9, 24)
        self._rentals_repo.add_rental(rental)
        rentals_list = self._rentals_repo.list()
        self.assertEqual(rentals_list[101].get_book_id, 101)
        self.assertEqual(rentals_list[101].get_client_id, 57)
        self.assertEqual(rentals_list[101].get_rented_date, 9)
        self.assertEqual(rentals_list[101].get_returned_date, 24)

    def test_rentals_remove(self):
        """
        test for repo rentals remove
        """
        rental = Rental(101, 101, 57, 9, 24)
        self._rentals_repo.add_rental(rental)
        rentals_list = self._rentals_repo.list()
        self.assertEqual(rentals_list[101].get_book_id, 101)
        len1 = len(self._rentals_repo.list())
        self._rentals_repo.remove_rental(101)
        len2 = len(self._rentals_repo.list())
        self.assertEqual(len1, len2+1)
