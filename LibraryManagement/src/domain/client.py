class Client:
    def __init__(self, client_id, cname):
        self._client_id = client_id
        self._cname = cname

    @property
    def get_id(self):
        return self._client_id

    def set_id(self, new):
        self._client_id = new

    @property
    def get_name(self):
        return self._cname

    def set_name(self, new):
        self._cname = new

    def __repr__(self):
        return str(self._cname) + " with ID: " + str(self._client_id)
