import unittest
from a10 import SortFilter, gnome_sort, filter_function


class TestSortFilter(unittest.TestCase):
    def setUp(self):
        self._sort_filter = SortFilter()

    def tearDown(self):
        pass

    def test_add_item(self):
        self._sort_filter.add(1)
        assert self._sort_filter[0] == 1

    def test_get_item(self):
        self._sort_filter.add(1)
        assert self._sort_filter.__getitem__(0) == 1

    def test_iterable(self):
        assert hasattr(self._sort_filter, '__iter__')

    def test_next(self):
        self._sort_filter.__iter__()
        self._sort_filter.add(1)
        self._sort_filter.add(2)
        self._sort_filter.add(3)
        assert self._sort_filter.__next__() == 1
        assert self._sort_filter.__next__() == 2
        assert self._sort_filter.__next__() == 3
        try:
            self._sort_filter.__next__()
        except StopIteration as ve:
            print(ve)

    def test_list(self):
        self._sort_filter.__iter__()
        self._sort_filter.add(1)
        new_list = self._sort_filter.list()
        assert len(new_list) == 1

    def test_gnome_sort(self):
        self._sort_filter.__iter__()
        self._sort_filter.add(4)
        self._sort_filter.add(3)
        self._sort_filter.add(2)
        self._sort_filter.add(1)
        new_list = self._sort_filter.list()
        gnome_sort(new_list)
        assert new_list[0] == 1
        assert new_list[1] == 2
        assert new_list[2] == 3
        assert new_list[3] == 4

    def test_filter(self):
        self._sort_filter.__iter__()
        self._sort_filter.add(4)
        self._sort_filter.add(3)
        self._sort_filter.add(2)
        self._sort_filter.add(1)
        new_list = self._sort_filter.list()
        filter_function(new_list, valid_fct)
        assert new_list[0] == 4
        assert new_list[1] == 3


def valid_fct(instance):
    return instance >= 3
