import unittest

from src.repository.BookRepo import BookRepo
from src.repository.ClientRepo import ClientRepo
from src.repository.RentalsRepo import RentalsRepo
from src.services.BookService import BookService
from src.services.ClientService import ClientService
from src.services.RentalsService import RentalService


class BookServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._B = BookRepo()
        self._book_service = BookService(self._B)

    def tearDown(self) -> None:
        pass

    def test_service_add_one(self):
        """
        test for service book add
        """
        self._book_service.add_book(101, "Luceafarul", "Mihai Eminescu")
        book_list = self._book_service.list()
        self.assertEqual(book_list[101].get_title, "Luceafarul")
        self.assertEqual(book_list[101].get_author, "Mihai Eminescu")

    def test_service_remove_one(self):
        """
        test for service book remove
        """
        self._book_service.add_book(101, "Luceafarul", "Mihai Eminescu")
        book_list = self._book_service.list()
        self.assertEqual(book_list[101].get_title, "Luceafarul")
        len1 = len(self._book_service.list())
        self._book_service.remove_book(101)
        len2 = len(self._book_service.list())
        self.assertEqual(len1, len2+1)

    def test_service_update(self):
        """
        test for service book update
        """
        self._book_service.add_book(101, "Luceafarul", "Mihai Eminescu")
        book_list = self._book_service.list()
        self.assertEqual(book_list[101].get_title, "Luceafarul")
        self._book_service.update_book(101, 1, "Sleepy Birds")
        self.assertEqual(book_list[101].get_title, "Sleepy Birds")
        self._book_service.update_book(101, 2, "Ion Creanga")
        self.assertEqual(book_list[101].get_author, "Ion Creanga")

    def test_service_validation(self):
        """
        test for service book validation
        """
        self._book_service.add_book(101, "Luceafarul", "Mihai Eminescu")
        book_list = self._book_service.list()
        self.assertEqual(self._book_service.validate_book(book_list, 101), True)


class ClientServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._C = ClientRepo()
        self._client_service = ClientService(self._C)

    def tearDown(self) -> None:
        pass

    def test_service_add_client(self):
        """
        test for service client add
        """
        self._client_service.add_client(101, "Mihai Eminescu")
        client_list = self._client_service.list()
        self.assertEqual(client_list[101].get_id, 101)
        self.assertEqual(client_list[101].get_name, "Mihai Eminescu")

    def test_service_remove_client(self):
        """
        test for service client remove
        """
        self._client_service.add_client(101, "Mihai Eminescu")
        client_list = self._client_service.list()
        self.assertEqual(client_list[101].get_name, "Mihai Eminescu")
        len1 = len(self._client_service.list())
        self._client_service.remove_client(101)
        len2 = len(self._client_service.list())
        self.assertEqual(len1, len2+1)

    def test_service_update_client(self):
        """
        test for service client update
        """
        self._client_service.add_client(101, "Mihai Eminescu")
        client_list = self._client_service.list()
        self.assertEqual(client_list[101].get_name, "Mihai Eminescu")
        self._client_service.update_client(101, "Eminescu")
        self.assertEqual(client_list[101].get_name, "Eminescu")

    def test_service_validation(self):
        """
        test for service client validation
        """
        self._client_service.add_client(101, "Mihai Eminescu")
        client_list = self._client_service.list()
        self.assertEqual(self._client_service.validate_client(client_list, 101), True)


class RentalsServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._B = BookRepo()
        self._C = ClientRepo()
        self._R = RentalsRepo()
        self._rental_service = RentalService(self._B, self._C, self._R)

    def tearDown(self) -> None:
        pass

    def test_service_add_rental(self):
        """
        test for service rental add
        """
        self._rental_service.add_rental(101, 101, 57, 15, 19)
        rental_list = self._rental_service.list()
        self.assertEqual(rental_list[101].get_book_id, 101)
        self.assertEqual(rental_list[101].get_client_id, 57)
        self.assertEqual(rental_list[101].get_rented_date, 15)
        self.assertEqual(rental_list[101].get_returned_date, 19)

    def test_service_remove_rental(self):
        """
        test for service rental remove
        """
        self._rental_service.add_rental(101, 101, 57, 15, 19)
        rental_list = self._rental_service.list()
        self.assertEqual(rental_list[101].get_book_id, 101)
        len1 = len(self._rental_service.list())
        self._rental_service.remove_rental(101)
        len2 = len(self._rental_service.list())
        self.assertEqual(len1, len2+1)
