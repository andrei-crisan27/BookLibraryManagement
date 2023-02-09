import random
from src.domain.rental import Rental


class RentalService:
    def __init__(self, book_repo, client_repo, rentals_repo):
        self._books_repo = book_repo
        self._clients_repo = client_repo
        self._rentals_repo = rentals_repo

    def add_rental(self, rental_id, book_id, client_id, date1, date2):
        """
        creates a new rental and calls add_rental method from repo
        """
        r = Rental(rental_id, book_id, client_id, date1, date2)
        self._rentals_repo.add_rental(r)
        self._rentals_repo.increase_rented_times(book_id)

    def remove_rental(self, rental_id):
        """
        removes a rental from the list
        """
        self._rentals_repo.remove_rental(rental_id)

    def list(self):
        """
        returns dictionary of rentals
        """
        return self._rentals_repo.list()

    def generate_rentals(self):
        """
        generates a list of rentals
        """
        j = 1
        rental_id = 0
        book_id = 0
        while j <= 10:
            rentals_list = self._rentals_repo.list()
            ok = 1
            while ok == 1:
                rental_id = random.randint(1, 100)
                ok = 0
                for i in rentals_list:
                    if rentals_list[i].get_rental_id == rental_id:
                        ok = 1
            book_list = self._books_repo.list()
            ok = 1
            while ok == 1:
                book_id = random.choice(list(book_list))
                ok = 0
                for i in rentals_list:
                    if rentals_list[i].get_book_id == book_id:
                        ok = 1
            client_list = self._clients_repo.list()
            client_id = random.choice(list(client_list))
            date_1 = random.randint(1, 15)
            date_2 = random.randint(16, 30)
            r = Rental(rental_id, book_id, client_id, date_1, date_2)
            self._rentals_repo.add_rental(r)
            self._rentals_repo.init_client_statistics(client_id)
            j += 1

    def remove_rental_book(self, book_id):
        """
        removes a book from rentals if it is removed from book repo
        """
        self._rentals_repo.remove_rental_book(book_id)

    def remove_rental_client(self, client_id):
        """
        removes a client from rentals if it is removed from client repo
        """
        self._rentals_repo.remove_rental_client(client_id)

    def generate_rented_days(self):
        """
        generates past rentals for each book
        """
        book_list = self._books_repo.list()
        for i in book_list:
            new_id = book_list[i].get_id
            self._rentals_repo.init_rented_days(new_id)
        rentals_list = self._rentals_repo.list()
        for j in rentals_list:
            book_id = rentals_list[j].get_book_id
            self._rentals_repo.increase_rented_times(book_id)

    def list_rented_days(self):
        """
        function that returns the statistics for each book
        """
        return self._rentals_repo.list_rented_times()

    def remove_rented_days(self, book_id):
        """
        function that removes a book from statistics
        """
        self._rentals_repo.remove_rented_days(book_id)

    def add_new_rented_days(self, book_id):
        """
        function that adds a book to statistics
        """
        self._rentals_repo.add_new_rented_days(book_id)

    def init_clients_statistics(self, client_id):
        """
        calls the repo function that initializes a client statistic with 0
        """
        self._rentals_repo.init_client_statistics(client_id)

    def generate_clients_statistics(self):
        """
        adds the first client statistics in the statistics list
        """
        rentals_list = self._rentals_repo.list()
        for i in rentals_list:
            clnt_id = rentals_list[i].get_client_id
            day1 = rentals_list[i].get_rented_date
            day2 = rentals_list[i].get_returned_date
            days = day2 - day1
            self._rentals_repo.add_client_statistics(clnt_id, days)

    def add_client_statistics(self, client_id, days1, days2):
        """
        adds days to a client statistic
        """
        self._rentals_repo.add1_client_statistics(client_id, days1, days2)

    def remove_client_statistics(self, rental_id):
        """
        removes days from a client statistic
        """
        self._rentals_repo.remove_client_statistics(rental_id)

    def list_clients_statistics(self):
        """
        returns the list of client statistics
        """
        return self._rentals_repo.client_statistics()

    def get_days_clients_statistics(self, rental_id):
        """
        calls the repo function that returns the days from a client statistic
        """
        return self._rentals_repo.get_client_statistics(rental_id)

    def init_author(self, author_name):
        """
        calls the repo function that initializes the number of times an author was rented
        """
        self._rentals_repo.init_author(author_name)

    def inc_author(self, author_name):
        """
        increases the number of rentals for an author by one
        """
        self._rentals_repo.inc_author(author_name)

    def dec_author(self, author_name):
        """
        decreases the number of rentals for an author by one
        """
        self._rentals_repo.dec_author(author_name)

    def remove_book_statistics(self, book_id):
        """
        removes rentals for a book that has been removed from the book list
        """
        book_list = self._books_repo.list()
        author_name = book_list[book_id].get_author
        books_statistics = self._rentals_repo.list_rented_times()
        times = books_statistics[book_id]
        for l in range(0, times):
            self.dec_author(author_name)

    def generate_author_statistics(self):
        """
        generates the first elements for the most rented authors list
        """
        books_list = self._books_repo.list()
        for i in books_list:
            author_name = books_list[i].get_author
            self.init_author(author_name)
        books_statistics = self._rentals_repo.list_rented_times()
        for j in books_statistics:
            book_id = j
            times = books_statistics[j]
            author_name = books_list[book_id].get_author
            for l in range(0, times):
                self.inc_author(author_name)

    def check_author_list(self, book_id):
        """
        looks for an author in the book list
        :return: True if found, false if not
        """
        books_list = self._books_repo.list()
        author_name = books_list[book_id].get_author
        for i in books_list:
            if author_name == books_list[i].get_author and books_list[i].get_id != book_id:
                return True
        return False

    def list_rented_authors(self):
        """
        returns the list of author statistics
        """
        return self._rentals_repo.list_author_statistics()

    def return_current_value(self, client_id):
        return self._rentals_repo.return_current_value(client_id)

    def return_rental_id(self, client_id):
        return self._rentals_repo.return_rental_id(client_id)

    def return_values_as_list(self, client_id):
        return self._rentals_repo.return_values_as_list(client_id)

    def return_rented_days(self, author_name):
        return self._rentals_repo.return_rented_days(author_name)

    def restore_rented_days(self, author_name, data):
        return self._rentals_repo.restore_rented_days(author_name, data)

    def remove_book_rentals(self):
        pass

    def remove_author_rented_times(self, author_name):
        return self._rentals_repo.remove_author_rented_times(author_name)