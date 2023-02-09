from src.services.BookService import BookService
from src.services.ClientService import ClientService
from src.services.RentalsService import RentalService
from src.repository.RepositoryException import RepositoryException
from src.repository.BookRepo import BookRepo, BookTextFileRepository, BookBinFileRepository
from src.repository.ClientRepo import ClientRepo, ClientTextFileRepository, ClientBinFileRepository
from src.services.UndoService import UndoService, FunctionCall
from src.repository.RentalsRepo import RentalsRepo, RentalsTextFileRepository, RentalsBinFileRepository
from src.domain.a10 import gnome_sort, filter_function, SortFilter

class Ui:
    def __init__(self):
        input_file = open("settings.properties", "rt")
        repository = input_file.readline().split(' ')[2].rstrip("\n")
        if repository == "inmemory":
            self._B = BookRepo()
            self._C = ClientRepo()
            self._R = RentalsRepo()
        elif repository == "textfiles":
            bookfile = input_file.readline().split(' ')[2].rstrip("\n")
            clientfile = input_file.readline().split(' ')[2].rstrip("\n")
            rentalsfile = input_file.readline().split(' ')[2].rstrip("\n")
            self._B = BookTextFileRepository(bookfile)
            self._C = ClientTextFileRepository(clientfile)
            self._R = RentalsTextFileRepository(rentalsfile)
        else:
            bookfile = input_file.readline().split(' ')[2].rstrip("\n")
            clientfile = input_file.readline().split(' ')[2].rstrip("\n")
            rentalsfile = input_file.readline().split(' ')[2].rstrip("\n")
            self._B = BookBinFileRepository(bookfile)
            self._C = ClientBinFileRepository(clientfile)
            self._R = RentalsBinFileRepository(rentalsfile)
        self._B.init_list()
        self._C.init_list()
        self._books = BookService(self._B)
        self._clients = ClientService(self._C)
        self._rentals = RentalService(self._B, self._C, self._R)
        self._undo_service = UndoService(self._books, self._clients, self._rentals)
        self._rentals.generate_rentals()
        self._rentals.generate_rented_days()
        self._rentals.generate_clients_statistics()
        self._rentals.generate_author_statistics()
        if repository != "inmemory":
            self._B.save_file()
            self._C.save_file()
            self._R.save_file()
        input_file.close()

    def book_menu(self):
        print("Type 1 to print all books.")
        print("Type 2 to add a book.")
        print("Type 3 to remove a book.")
        print("Type 4 to update a book.")

    def client_menu(self):
        print("Type 1 to print all clients.")
        print("Type 2 to add a client.")
        print("Type 3 to remove a client.")
        print("Type 4 to update a client.")

    def rentals_menu(self):
        print("Type 1 to print all rentals.")
        print("Type 2 to add rental.")
        print("Type 3 to remove rental.")

    def search_menu(self):
        print("Type 1 to search a book.")
        print("Type 2 to search a client.")

    def start(self):
        while True:
            try:
                print(
                    "Type 1 for books, 2 for clients, 3 for rentals, 4 for search, 5 for statistics, 6 for undo, 7 for redo or 8 to exit.")
                option = input("Give option: ")
                if option == "1":
                    self.book_menu()
                    option1 = input("Give option: ")
                    if option1 == "1":
                        book_list = self._B.list()
                        new_list = []
                        for i in book_list:
                            new_list.append(i)
                        gnome_sort(new_list)
                        for i in new_list:
                            print(book_list[i])
                    elif option1 == "2":
                        book_id = int(input("Give id: "))
                        book_name = input("Give name: ")
                        book_author = input("Give author: ")
                        self._books.add_book(book_id, book_name, book_author)
                        self._rentals.add_new_rented_days(book_id)
                        undo_op1 = FunctionCall(self._books.remove_book, book_id)
                        redo_op1 = FunctionCall(self._books.add_book, book_id, book_name, book_author)
                        redo_cascade = [FunctionCall(self._rentals.add_new_rented_days, book_id)]
                        undo_cascade = [FunctionCall(self._rentals.remove_book_statistics, book_id),
                                        FunctionCall(self._rentals.remove_rental_book, book_id),
                                        FunctionCall(self._rentals.remove_rented_days, book_id)]
                        self._undo_service.record_undo_operation(undo_op1)
                        self._undo_service.record_reversed_operation(redo_op1)
                        self._undo_service.record_undo_cascade(undo_cascade)
                        self._undo_service.record_undo_cascade_reversed(redo_cascade)
                        self._undo_service.restore_redo()
                    elif option1 == "3":
                        book_id = int(input("Give id: "))
                        book_list = self._books.list()
                        undo_op2 = FunctionCall(self._books.add_book, book_id, book_list[book_id].get_title,
                                                book_list[book_id].get_author)
                        redo_op2 = FunctionCall(self._books.remove_book, book_id)
                        self._undo_service.record_undo_operation(undo_op2)
                        self._undo_service.record_reversed_operation(redo_op2)
                        self._undo_service.restore_redo()
                        redo_cascade = [FunctionCall(self._rentals.remove_book_statistics, book_id),
                                        FunctionCall(self._rentals.remove_rental_book, book_id),
                                        FunctionCall(self._rentals.remove_rented_days, book_id)]
                        undo_cascade = [FunctionCall(self._rentals.add_new_rented_days, book_id)]
                        self._undo_service.record_undo_cascade(undo_cascade)
                        self._undo_service.record_undo_cascade_reversed(redo_cascade)
                        self._rentals.remove_book_statistics(book_id)
                        self._books.remove_book(book_id)
                        self._rentals.remove_rental_book(book_id)
                        self._rentals.remove_rented_days(book_id)
                    elif option1 == "4":
                        book_id = int(input("Give id: "))
                        opt = int(input("Type 1 to change the title, 2 for the author: "))
                        param = input("Give new value: ")
                        book_list = self._books.list()
                        if opt == 1:
                            undo_op3 = FunctionCall(self._books.update_book, book_id, opt, book_list[book_id].get_title)
                            redo_op3 = FunctionCall(self._books.update_book, book_id, opt, param)
                            self._undo_service.record_undo_operation(undo_op3)
                            self._undo_service.record_reversed_operation(redo_op3)
                        elif opt == 2:
                            undo_op3 = FunctionCall(self._books.update_book, book_id, opt,
                                                    book_list[book_id].get_author)
                            redo_op3 = FunctionCall(self._books.update_book, book_id, opt, param)
                            self._undo_service.record_undo_operation(undo_op3)
                            self._undo_service.record_reversed_operation(redo_op3)
                        undo_cascaded = []
                        redo_cascaded = []
                        self._undo_service.record_undo_cascade(undo_cascaded)
                        self._undo_service.record_undo_cascade_reversed(redo_cascaded)
                        self._undo_service.restore_redo()
                        self._books.update_book(book_id, opt, param)
                    else:
                        print("Invalid command!")
                elif option == "2":
                    self.client_menu()
                    option1 = input("Give option: ")
                    if option1 == "1":
                        client_list = self._clients.list()
                        new_list = []
                        for i in client_list:
                            new_list.append(i)
                        gnome_sort(new_list)
                        for i in new_list:
                            print(client_list[i])
                    elif option1 == "2":
                        client_id = int(input("Give id: "))
                        client_name = input("Give name: ")
                        self._clients.add_client(client_id, client_name)
                        undo_operation = FunctionCall(self._clients.remove_client, client_id)
                        redo_operation = FunctionCall(self._clients.add_client, client_id, client_name)
                        undo_cascaded = []
                        redo_cascaded = []
                        self._undo_service.record_undo_cascade(undo_cascaded)
                        self._undo_service.record_undo_cascade_reversed(redo_cascaded)
                        self._undo_service.record_undo_operation(undo_operation)
                        self._undo_service.record_reversed_operation(redo_operation)
                        self._undo_service.restore_redo()
                    elif option1 == "3":
                        client_id = int(input("Give id: "))
                        client_list = self._clients.list()
                        undo_operation1 = FunctionCall(self._clients.add_client, client_id,
                                                       client_list[client_id].get_name)
                        redo_operation1 = FunctionCall(self._clients.remove_client, client_id)
                        self._undo_service.record_undo_operation(undo_operation1)
                        self._undo_service.record_reversed_operation(redo_operation1)
                        days1 = 0
                        days2 = self._rentals.return_current_value(client_id)
                        undo_cascaded = []
                        rent_id = self._rentals.return_rental_id(client_id)
                        if rent_id != -1:
                            rentals_elems = self._rentals.return_values_as_list(client_id)
                            for i in rentals_elems:
                                op = FunctionCall(self._rentals.add_rental, i[0], i[1], i[2], i[3], i[4])
                                undo_cascaded.append(op)
                        undo_cascaded.append(FunctionCall(self._rentals.add_client_statistics, client_id, days1, days2))
                        redo_cascaded = [FunctionCall(self._rentals.init_clients_statistics, client_id),
                                         FunctionCall(self._rentals.remove_rental_client, client_id)]
                        self._undo_service.record_undo_cascade(undo_cascaded)
                        self._undo_service.record_undo_cascade_reversed(redo_cascaded)
                        self._undo_service.restore_redo()
                        self._rentals.init_clients_statistics(client_id)
                        self._clients.remove_client(client_id)
                        self._rentals.remove_rental_client(client_id)
                    elif option1 == "4":
                        client_id = int(input("Give id: "))
                        param = input("Give new name: ")
                        client_list = self._clients.list()
                        undo_operation2 = FunctionCall(self._clients.update_client, client_id,
                                                       client_list[client_id].get_name)
                        redo_operation2 = FunctionCall(self._clients.update_client, client_id, param)
                        undo_cascaded = []
                        redo_cascaded = []
                        self._undo_service.record_undo_cascade(undo_cascaded)
                        self._undo_service.record_undo_cascade_reversed(redo_cascaded)
                        self._undo_service.record_undo_operation(undo_operation2)
                        self._undo_service.record_reversed_operation(redo_operation2)
                        self._undo_service.restore_redo()
                        self._clients.update_client(client_id, param)
                    else:
                        print("Invalid command!")
                elif option == "3":
                    self.rentals_menu()
                    option1 = input("Give option: ")
                    if option1 == "1":
                        rental_list = self._rentals.list()
                        new_list = []
                        for i in rental_list:
                            new_list.append(i)
                        gnome_sort(new_list)
                        for i in new_list:
                            print(rental_list[i])
                    elif option1 == "2":
                        try:
                            book_list = self._books.list()
                            client_list = self._clients.list()
                            rental_id = int(input("Give rental id: "))
                            book_id = int(input("Give book id: "))
                            if self._books.validate_book(book_list, book_id) is False:
                                raise ValueError("Book doesn't exist!")
                            client_id = int(input("Give client id: "))
                            if self._clients.validate_client(client_list, client_id) is False:
                                raise ValueError("Client doesn't exist!")
                            rent_date = int(input("Give rent date: "))
                            return_date = int(input("Give return date: "))
                            self._rentals.add_rental(rental_id, book_id, client_id, rent_date, return_date)
                            days1 = self._rentals.get_days_clients_statistics(rental_id)
                            days2 = return_date - rent_date
                            und_op = FunctionCall(self._rentals.remove_rental, rental_id)
                            red_op = FunctionCall(self._rentals.add_rental, rental_id, book_id, client_id, rent_date,
                                                  return_date)
                            undo_cascaded = [FunctionCall(self._rentals.remove_client_statistics, rental_id)]
                            redo_cascaded = []
                            op = FunctionCall(self._rentals.add_client_statistics, client_id, days1, days2)
                            redo_cascaded.append(op)
                            self._undo_service.record_undo_operation(und_op)
                            self._undo_service.record_reversed_operation(red_op)
                            self._rentals.add_client_statistics(client_id, days1, days2)
                            author_name = book_list[book_id].get_author
                            if self._rentals.check_author_list(book_id) is True:
                                self._rentals.inc_author(author_name)
                                op = FunctionCall(self._rentals.inc_author, author_name)
                                redo_cascaded.append(op)
                            else:
                                self._rentals.init_author(author_name)
                                self._rentals.inc_author(author_name)
                                op = [FunctionCall(self._rentals.init_author, author_name),
                                      FunctionCall(self._rentals.inc_author, author_name)]
                                redo_cascaded.append(op)
                            self._undo_service.record_undo_cascade(undo_cascaded)
                            self._undo_service.record_undo_cascade_reversed(redo_cascaded)
                            self._undo_service.restore_redo()
                        except ValueError as ve:
                            print(ve)
                    elif option1 == "3":
                        try:
                            rental_id = int(input("Give rental id: "))
                            rentals_list = self._rentals.list()
                            client_id = rentals_list[rental_id].get_client_id
                            book_list = self._books.list()
                            book_id = rentals_list[rental_id].get_book_id
                            author_name = book_list[book_id].get_author
                            days1 = 0
                            days2 = self._rentals.return_current_value(client_id)
                            und_op1 = FunctionCall(self._rentals.add_rental, rental_id,
                                                   rentals_list[rental_id].get_book_id,
                                                   rentals_list[rental_id].get_client_id,
                                                   rentals_list[rental_id].get_rented_date,
                                                   rentals_list[rental_id].get_returned_date)
                            red_op1 = FunctionCall(self._rentals.remove_rental, rental_id)
                            self._undo_service.record_undo_operation(und_op1)
                            self._undo_service.record_reversed_operation(red_op1)
                            undo_cascaded = [FunctionCall(self._rentals.add_client_statistics, client_id, days1, days2),
                                             FunctionCall(self._rentals.inc_author, author_name)]
                            redo_cascaded = [FunctionCall(self._rentals.remove_client_statistics, rental_id),
                                             FunctionCall(self._rentals.remove_author_rented_times, author_name)]
                            self._undo_service.record_undo_cascade(undo_cascaded)
                            self._undo_service.record_undo_cascade_reversed(redo_cascaded)
                            self._undo_service.restore_redo()
                            self._rentals.remove_client_statistics(rental_id)
                            self._rentals.remove_rental(rental_id)
                        except KeyError as ve:
                            print("There is no rental with id " + str(ve))
                    else:
                        print("Invalid command!")
                elif option == "4":
                    self.search_menu()
                    option1 = input("Give option: ")
                    if option1 == "1":
                        option2 = input("Type 1 to search for ID, 2 for title or 3 for author: ")
                        if option2 == "1":
                            book_id = int(input("Give ID: "))
                            self._books.search_book_id(book_id)
                        elif option2 == "2":
                            book_title = input("Give title: ")
                            self._books.search_book_title(book_title)
                        elif option2 == "3":
                            book_author = input("Give author: ")
                            self._books.search_book_author(book_author)
                        else:
                            print("Invalid command!")
                    elif option1 == "2":
                        option2 = input("Type 1 to search for ID, 2 for name: ")
                        if option2 == "1":
                            c_id = input("Give ID: ")
                            self._clients.search_client_id(c_id)
                        elif option2 == "2":
                            c_name = input("Give name: ")
                            self._clients.search_client_name(c_name)
                        else:
                            print("Invalid command!")
                    else:
                        print("Invalid command!")
                elif option == "5":
                    option1 = input(
                        "Type 1 for most rented books, 2 for most active clients or 3 for most rented authors: ")
                    if option1 == "1":
                        books_days_statistics = self._rentals.list_rented_days()
                        books_days_statistics_sorted = dict(
                            sorted(books_days_statistics.items(), key=lambda kv: kv[1], reverse=True))
                        book_lst = self._books.list()
                        for i in books_days_statistics_sorted:
                            print("'" + str(book_lst[i].get_title) + "' with ID " + str(
                                book_lst[i].get_id) + " was rented for " + str(
                                books_days_statistics_sorted[i]) + " times.")
                    elif option1 == "2":
                        clients_statistics = self._rentals.list_clients_statistics()
                        clients_statistics_sorted = dict(
                            sorted(clients_statistics.items(), key=lambda kv: kv[1], reverse=True))
                        for i in clients_statistics_sorted:
                            print("Client with ID " + str(i) + " has a total of " + str(
                                clients_statistics_sorted[i]) + " rented days.")
                    elif option1 == "3":
                        author_statistics = self._rentals.list_rented_authors()
                        author_statistics_sorted = dict(
                            sorted(author_statistics.items(), key=lambda kv: kv[1], reverse=True))
                        for i in author_statistics_sorted:
                            print(str(i) + " was rented " + str(author_statistics[i]) + " times.")
                elif option == "6":
                    self._undo_service.undo()
                elif option == "7":
                    self._undo_service.redo()
                elif option == "8":
                    print("Program successfully ended!")
                    return
                else:
                    print("Invalid command!")
            except RepositoryException as re:
                print(re)


ui = Ui()
ui.start()
