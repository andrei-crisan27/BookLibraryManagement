import pickle
import random

from src.domain.rental import Rental
from src.repository.RepositoryException import RepositoryException


class RentalsRepo:
    def __init__(self):
        self._rentals = {}
        self._books_rented_times = {}
        self._clients_rented_days = {}
        self._rented_authors = {}

    def add_rental(self, rental):
        """
        adds a rental to the dictionary of rentals
        """
        if len(self._rentals) == 0:
            self._rentals[rental.get_rental_id] = rental
        elif rental.get_rental_id < 0:
            raise RepositoryException("Invalid ID!")
        elif rental.get_rental_id not in self._rentals.keys():
            self._rentals[rental.get_rental_id] = rental
        else:
            raise RepositoryException("Rental already in list.")

    def remove_rental(self, rental_id):
        """
        removes a rental from the dictionary of rentals
        """
        if rental_id < 0:
            raise RepositoryException("Invalid ID!")
        if rental_id in self._rentals:
            self._rentals.pop(rental_id)

    def list(self):
        """
        :return: the dictionary of rentals
        """
        return self._rentals

    def remove_rental_book(self, book_id):
        """
        removes a book from rentals if it is removed from book repo
        """
        rentals_list = self.list()
        id = 0
        for rental in rentals_list:
            if rentals_list[rental].get_book_id == book_id:
                id += rental
                break
        if id != 0:
            self.remove_rental(id)

    def remove_rental_client(self, client_id):
        """
        removes a client from rentals if it is removed from client repo
        """
        # rentals_list = self.list()
        # remove_list = []
        # for rental in rentals_list:
        #     if rentals_list[rental].get_client_id == client_id:
        #         remove_list.append(rental)
        # for i in range(len(remove_list)):
        #     self.remove_rental(remove_list[i])
        # for i in range(0, k):
        #     if self._rentals[i].get_client_id == client_id:
        #         self._rentals.pop(self._rentals[i].get_rental_id)
        for key, value in list(self._rentals.items()):
            if value.get_client_id == client_id:
                del self._rentals[key]

    def init_rented_days(self, i_d):
        """
        function that generates past rentals for each book
        """
        self._books_rented_times[i_d] = random.randint(0, 5)

    def list_rented_times(self):
        """
        function that returns the list of past rentals for each book
        """
        return self._books_rented_times

    def increase_rented_times(self, i_d):
        """
        function that increases the statistics for a book rental with one
        """
        self._books_rented_times[i_d] += 1

    def remove_rented_days(self, i_d):
        """
        function that removes a book from the book days statistic
        """
        if i_d in self._books_rented_times:
            self._books_rented_times.pop(i_d)

    def add_new_rented_days(self, i_d):
        """
        function that adds a new book to the book days statistic
        """
        self._books_rented_times[i_d] = 0

    def client_statistics(self):
        """
        returns the client statistics list
        """
        return self._clients_rented_days

    def init_client_statistics(self, client_id):
        """
        initializes the statistic corresponding to a client with 0
        """
        self._clients_rented_days[client_id] = 0

    def get_client_statistics(self, rental_id):
        """
        returns the number of days from a certain statistic
        """
        rentals_list = self._rentals
        client_id = rentals_list[rental_id].get_client_id
        if client_id not in self._clients_rented_days.keys():
            self.init_client_statistics(client_id)
        days = self._clients_rented_days[client_id]
        return days

    def add_client_statistics(self, client_id, days):
        """
        adds days to a client statistic, used in the initialization of elements
        """
        self._clients_rented_days[client_id] += days

    def add1_client_statistics(self, client_id, days1, days2):
        """
        adds days to a client statistic, used when adding new elements
        """
        self._clients_rented_days[client_id] = days1 + days2

    def remove_client_statistics(self, rental_id):
        """
        removes days from a client statistic
        """
        rentals_list = self._rentals
        client_id = rentals_list[rental_id].get_client_id
        day1 = rentals_list[rental_id].get_rented_date
        day2 = rentals_list[rental_id].get_returned_date
        days = day2 - day1
        self._clients_rented_days[client_id] -= days

    def init_author(self, author_name):
        """
        initializes the number of rentals for an author in the most rented authors list
        """
        self._rented_authors[author_name] = 0

    def inc_author(self, author_name):
        """
        increases the number of rentals for an author by one
        """
        if author_name not in self._rented_authors.keys():
            self._rented_authors[author_name] = 1
        else:
            self._rented_authors[author_name] += 1

    def dec_author(self, author_name):
        """
        decreases the number of rentals for an author by one
        """
        self._rented_authors[author_name] -= 1

    def list_author_statistics(self):
        """
        returns the list of the most rented authors
        """
        return self._rented_authors

    def return_current_value(self, client_id):
        if client_id not in self._clients_rented_days.keys():
            return 0
        return self._clients_rented_days[client_id]

    def return_rental_id(self, client_id):
        for i in self._rentals:
            if self._rentals[i].get_client_id == client_id:
                return self._rentals[i].get_rental_id
        return -1

    def return_values_as_list(self, client_id):
        values_list = []
        for i in self._rentals:
            if self._rentals[i].get_client_id == client_id:
                lst = [self._rentals[i].get_rental_id, self._rentals[i].get_book_id, self._rentals[i].get_client_id,
                       self._rentals[i].get_rented_date, self._rentals[i].get_returned_date]
                values_list.append(lst)
        return values_list

    def return_rented_days(self, author_name):
        if author_name in self._rented_authors.keys():
            return self._rented_authors[author_name]
        return 0

    def restore_rented_days(self, author_name, data):
        self._rented_authors[author_name] = data

    def remove_author_rented_times(self, author_name):
        self._rented_authors[author_name] = 0


class RentalsTextFileRepository(RentalsRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self.save_file()

    def load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            rental_id, book_id, client_id, rented_date, returned_date = line.split(maxsplit=4, sep=',')
            self.add_rental(Rental(int(rental_id), int(book_id), int(client_id), int(rented_date), int(returned_date)))
        f.close()

    def save_file(self):
        f = open(self._file_name, "wt")
        for rental in self._rentals.values():
            f.write(
                str(rental.get_rental_id) + ',' + str(rental.get_book_id) + ',' + str(rental.get_client_id) + ',' + str(
                    rental.get_rented_date) + ',' + str(rental.get_returned_date) + '\n')
        f.close()

    def add_rental(self, rental):
        super(RentalsTextFileRepository, self).add_rental(rental)
        self.save_file()

    def remove_rental(self, rental_id):
        super(RentalsTextFileRepository, self).remove_rental(rental_id)
        self.save_file()

    def remove_rental_book(self, book_id):
        super(RentalsTextFileRepository, self).remove_rental_book(book_id)
        self.save_file()

    def remove_rental_client(self, client_id):
        super(RentalsTextFileRepository, self).remove_rental_client(client_id)
        self.save_file()


class RentalsBinFileRepository(RentalsRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self.save_file()

    def load_file(self):
        f = open(self._file_name, "rb")
        self._rentals = pickle.load(f)
        f.close()

    def save_file(self):
        f = open(self._file_name, "wb")
        pickle.dump(self._rentals, f)
        f.close()

    def add_rental(self, rental):
        super(RentalsBinFileRepository, self).add_rental(rental)
        self.save_file()

    def remove_rental(self, rental_id):
        super(RentalsBinFileRepository, self).remove_rental(rental_id)
        self.save_file()

    def remove_rental_book(self, book_id):
        super(RentalsBinFileRepository, self).remove_rental_book(book_id)
        self.save_file()

    def remove_rental_client(self, client_id):
        super(RentalsBinFileRepository, self).remove_rental_client(client_id)
        self.save_file()
