import pickle
import random
from src.domain.client import Client
from src.repository.RepositoryException import RepositoryException


class ClientRepo:
    def __init__(self):
        self._data = {}

    def generate_name(self):
        first_name = ["David", "Alexandru", "Gabriel", "Andrei", "Cristian", "Darius", "Mihai", "Daniel", "Maria",
                      "Andreea", "Elena", "Ioana", "Alexandra", "Ana", "Antonia", "Daria"]
        last_name = ["Pop", "Popescu", "Radu", "Ionescu", "Georgescu", "Rusu", "Stan", "Munteanu", "Ilie", "Florea",
                     "Stanciu", "Oprea", "Tudor", "Dinu", "Neagu", "Dragomir"]
        return random.choice(first_name) + " " + random.choice(last_name)

    def init_list(self):
        """
        initializes the dictionary of clients
        """
        i = 0
        while i < 20:
            client_id = random.randint(1, 100)
            client_name = self.generate_name()
            c = Client(client_id, client_name)
            if c.get_id not in self._data.keys():
                self._data[c.get_id] = c
                i += 1

    def add_element(self, client):
        """
        adds a client to the dictionary of clients
        """
        if client.get_id < 0:
            raise RepositoryException("Invalid ID!")
        if client.get_id in self._data.keys():
            raise RepositoryException("Duplicate client ID!")
        self._data[client.get_id] = client

    def remove_element(self, client_id):
        """
        removes a client from the dictionary of clients
        """
        if client_id < 0:
            raise RepositoryException("Invalid ID!")
        if client_id in self._data.keys():
            self._data.pop(client_id)
        else:
            raise RepositoryException("Client doesn't exist!")

    def update_client(self, client_id, param):
        """
        updates the name of a client
        """
        if client_id < 0:
            raise RepositoryException("Invalid ID!")
        ok = 0
        for i in self._data:
            if i == client_id:
                ok = 1
                self._data[i].set_name(param)
        if ok == 0:
            raise RepositoryException("ID not found in ID list!")

    def list(self):
        """
        :return: the dictionary of clients
        """
        return self._data

    def validate_client(self, cl_lst, cl_id):
        """
        searches a client in the list of clients
        :return: True if the client is in the list, False if not
        """
        for i in cl_lst:
            if cl_id == cl_lst[i].get_id:
                return True
        return False

    def search_client_id(self, param):
        """
        function used to search for a client with a specific id in the clients list
        """
        client_list = self._data
        ok = 0
        for i in client_list:
            if str(param) in str(client_list[i].get_id):
                print(client_list[i])
                ok += 1
        if ok == 0:
            raise RepositoryException("There are no clients with this ID.")

    def search_client_name(self, param):
        """
        function used to search for a client with a specific id in the clients list
        """
        client_list = self._data
        ok = 0
        for i in client_list:
            param1 = str(param)
            param2 = str(client_list[i].get_name)
            if param1.lower() in param2.lower():
                print(client_list[i])
                ok += 1
        if ok == 0:
            raise RepositoryException("There are no clients with this name.")


class ClientTextFileRepository(ClientRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self.save_file()

    def load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            id, name = line.split(maxsplit=1, sep=',')
            self.add_element(Client(int(id), name))
        f.close()

    def save_file(self):
        f = open(self._file_name, "wt")
        for client in self._data.values():
            f.write(str(client.get_id) + ',' + client.get_name + '\n')
        f.close()

    def add_element(self, client):
        super(ClientTextFileRepository, self).add_element(client)
        self.save_file()

    def remove_element(self, client_id):
        super(ClientTextFileRepository, self).remove_element(client_id)
        self.save_file()

    def update_client(self, client_id, param):
        super(ClientTextFileRepository, self).update_client(client_id, param)
        self.save_file()


class ClientBinFileRepository(ClientRepo):
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

    def add_element(self, client):
        super(ClientBinFileRepository, self).add_element(client)
        self.save_file()

    def remove_element(self, client_id):
        super(ClientBinFileRepository, self).remove_element(client_id)
        self.save_file()

    def update_client(self, client_id, param):
        super(ClientBinFileRepository, self).update_client(client_id, param)
        self.save_file()