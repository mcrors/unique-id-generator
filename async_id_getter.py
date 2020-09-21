from typing import List
import logging
import asyncio
from id_getter import IDGetter, IDPool
from id_gen import gen_unique_id


logging.basicConfig(level=logging.INFO,
                    filename='async_id_getter.log',
                    filemode='w',
                    format='%(asctime)s - %(message)s')


class AsyncIDGetter(IDGetter):

    def __init__(self):
        self._id_pool_1 = IDPool(name='Pool1')
        self._id_pool_2 = IDPool(name='Pool2')
        self._init_pool(self._id_pool_1)
        self._init_pool(self._id_pool_2)

    async def get_id(self):
        id_pool = await self._get_id_pool()
        result = id_pool.pop()
        return result

    @staticmethod
    async def _fill_id_pool(id_pool: IDPool):
        logging.info(f'STARTING: refill pool {id_pool.name}')
        id_pool.extend(gen_unique_id(10000))
        logging.info(f'FINISHED: refill pool {id_pool.name}')

    async def _get_id_pool(self):
        no_available_pool = True
        while no_available_pool:
            if len(self._id_pool_1) > 0:
                if not self._id_pool_2.is_filling and len(self._id_pool_2) < 10000:
                    await self._fill_id_pool(self._id_pool_2)
                return self._id_pool_1
            elif len(self._id_pool_2) > 0:
                if not self._id_pool_1.is_filling and len(self._id_pool_1) < 10000:
                    await self._fill_id_pool(self._id_pool_1)
                return self._id_pool_2
            else:
                logging.info("No available pools")

    @staticmethod
    def _init_pool(id_pool: IDPool):
        logging.info(f'STARTING: Init pool {id_pool.name}')
        id_pool.extend(gen_unique_id(10000))
        logging.info(f'FINISHED: Init pool {id_pool.name}')
