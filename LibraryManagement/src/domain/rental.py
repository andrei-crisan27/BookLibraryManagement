class Rental:
    def __init__(self, rental_id, book_id, client_id, rented_date, returned_date):
        self._rental_id = rental_id
        self._book_id = book_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._returned_date = returned_date

    @property
    def get_rental_id(self):
        return self._rental_id

    def set_rental_id(self, new):
        self._rental_id = new

    @property
    def get_book_id(self):
        return self._book_id

    def set_book_id(self, new):
        self._book_id = new

    @property
    def get_client_id(self):
        return self._client_id

    def set_client_id(self, new):
        self._client_id = new

    @property
    def get_rented_date(self):
        return self._rented_date

    def set_rented_date(self, new):
        self._rented_date = new

    @property
    def get_returned_date(self):
        return self._returned_date

    def set_returned_date(self, new):
        self._returned_date = new

    def __repr__(self):
        return "Rental " + str(self._rental_id) + ": Book with id " + str(
            self._book_id) + " is rented by client with id " + str(self._client_id) + " from " + str(
            self._rented_date) + " November until " + str(self._returned_date) + " November."
