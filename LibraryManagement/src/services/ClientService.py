from src.domain.client import Client


class ClientService:
    def __init__(self, clients_repo):
        self._clients = clients_repo

    def add_client(self, client_id, client_name):
        """
        creates a new client and calls the add_element function from repo
        """
        c = Client(client_id, client_name)
        self._clients.add_element(c)

    def remove_client(self, client_id):
        """
        removes a client from the dictionary
        """
        self._clients.remove_element(client_id)

    def update_client(self, client_id, param):
        """
        updates the name of a client
        :param param: new name
        """
        self._clients.update_client(client_id, param)

    def list(self):
        """
        returns dictionary of clients
        """
        return self._clients.list()

    def validate_client(self, cl_lst, cl_id):
        """
        verifies if a client is in the list of clients
        """
        return self._clients.validate_client(cl_lst, cl_id)

    def init_list(self):
        """
        calls the function that generates clients from Repo
        """
        return self._clients.init_list()

    def search_client_id(self, param):
        """
        calls the search client by ID function from Repo
        """
        self._clients.search_client_id(param)

    def search_client_name(self, param):
        """
        calls the search client by name function from Repo
        """
        self._clients.search_client_name(param)
