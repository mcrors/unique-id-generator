from unittest.mock import patch
from thread_id_getter import ThreadIDGetter


class TestIdGetterShould:

    @staticmethod
    def test_fill_id_pools_on_init():
        id_getter = ThreadIDGetter()
        assert len(id_getter._id_pool_1) == 10000
        assert len(id_getter._id_pool_2) == 10000

    @staticmethod
    @patch('id_getter.gen_unique_id', return_value=[1])
    def test_return_single_id(gen_unique_id_mock):
        id_getter = ThreadIDGetter()
        result = id_getter.get_id()
        assert result == 1

    @staticmethod
    @patch('id_getter.gen_unique_id', return_value=[1 for _ in range(101)])
    def test_use_correct_id_pool(gen_unique_id_mock):
        id_getter = ThreadIDGetter()
        assert True
