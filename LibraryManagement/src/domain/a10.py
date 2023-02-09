class SortFilter:
    def __init__(self):
        self._data = []

    def add(self, o):
        self._data.append(o)

    def __getitem__(self, item):
        return self._data[item]

    def list(self):
        return list(self._data)

    def __iter__(self):
        self._poz = 0
        return self

    def __len__(self):
        return len(self._data)

    def __next__(self):
        if self._poz == len(self._data):
            raise StopIteration()
        self._poz += 1
        return self._data[self._poz - 1]


def gnome_sort(obj_list):
    poz = 0
    while poz < len(obj_list):
        if poz == 0 or obj_list[poz] >= obj_list[poz - 1]:
            poz += 1
        else:
            aux = obj_list[poz]
            obj_list[poz] = obj_list[poz - 1]
            obj_list[poz - 1] = aux
            poz -= 1


def filter_function(obj_list, acc_function):
    index = 0
    while index < len(obj_list):
        if acc_function(obj_list[index]) is True:
            del obj_list[index]
        else:
            index += 1
