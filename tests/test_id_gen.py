import timeit
import pytest
from id_gen import gen_unique_id


class TestIdGenShould:

    @staticmethod
    def test_gen_10000_ids():
        expected = 10000
        result = gen_unique_id(10000)
        assert len(result) == expected

    @staticmethod
    @pytest.mark.parametrize('num_of_ids, low_bound, high_bound', [
        (900, 1, 2),
        (10000, 1, 2),
        (100000, 10, 11)
    ])
    def test_takes_1_sec_for_10000_ids_or_less(num_of_ids, low_bound, high_bound):
        setup = 'from id_gen import gen_unique_id'
        stmt = f'gen_unique_id({num_of_ids})'
        result = timeit.timeit(stmt=stmt, setup=setup, number=1)
        assert low_bound < result < high_bound

