from typing import List
import threading
import logging
from id_gen import gen_unique_id
from id_getter import IDGetter, IDPool, IDGetterError


logging.basicConfig(level=logging.INFO,
                    filename='thread_id_getter.log',
                    filemode='w',
                    format='%(asctime)s - %(message)s')


class ThreadIDGetter(IDGetter):

    def __init__(self):
        self._id_pool_1 = IDPool(name='Pool1')
        self._id_pool_2 = IDPool(name='Pool2')
        self._pool_lock = threading.Lock()
        self._fill_id_pool(self._id_pool_1)
        self._fill_id_pool(self._id_pool_2)

    def get_id(self):
        with self._pool_lock:
            id_pool = self._get_id_pool()
            result = id_pool.pop()
            logging.info(f'ID: {result}. Getting ID from {id_pool.name}. Remaining IDs in pool {len(id_pool)}')
        return result

    @staticmethod
    def _fill_id_pool(id_pool: IDPool):
        logging.info(f'STARTING: refill pool {id_pool.name}')
        id_pool.extend(gen_unique_id(10000))
        id_pool.is_filling = False
        logging.info(f'FINISHED: refill pool {id_pool.name}')

    def _get_id_pool(self):
        no_available_pool = True
        while no_available_pool:
            if len(self._id_pool_1) > 0:
                if not self._id_pool_2.is_filling and len(self._id_pool_2) < 10000:
                    self._id_pool_2.is_filling = True
                    t = threading.Thread(target=self._fill_id_pool, args=(self._id_pool_2,))
                    t.start()
                return self._id_pool_1
            elif len(self._id_pool_2) > 0:
                if not self._id_pool_1.is_filling and len(self._id_pool_1) < 10000:
                    self._id_pool_1.is_filling = True
                    t = threading.Thread(target=self._fill_id_pool, args=(self._id_pool_1,))
                    t.start()
                return self._id_pool_2
            else:
                logging.info("No available pools")
