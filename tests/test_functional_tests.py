import time
import asyncio
import logging
import pytest
from concurrent.futures import ThreadPoolExecutor
from id_getter import IDGetter
from thread_id_getter import ThreadIDGetter
from async_id_getter import AsyncIDGetter


class Client:

    def __init__(self, id_getter: IDGetter):
        self._id_getter = id_getter
        self.id = None
        self.execution_time = 0

    def work(self):
        start = time.perf_counter()
        self.id = self._id_getter.get_id()
        end = time.perf_counter()
        self.execution_time = end - start

    async def asyncWork(self):
        start = time.perf_counter()
        self.id = await self._id_getter.get_id()
        end = time.perf_counter()
        self.execution_time = end - start

    def __lt__(self, other):
        return self.execution_time < other.execution_time

    def __gt__(self, other):
        return self.execution_time > other.execution_time

    def __eq__(self, other):
        return self.execution_time == other.execution_time


def do_work(client):
    client.work()


async def do_async_work(client):
    await client.asyncWork()


class TestThreadIdGetterFromClientShould:

    def test_get_ids_in_less_than_1_second(self):
        logging.basicConfig(level=logging.INFO,
                            filename='thread_id_getter.log',
                            filemode='w',
                            format='%(asctime)s - %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='thread_id_getter.log', mode='w')
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        id_getter = ThreadIDGetter(logger)
        clients = [Client(id_getter) for _ in range(22000)]
        # execute clients work using threads
        for client in clients:
            client.work()
        times_less_than_1 = [self._less_than_1_second(client.execution_time) for client in clients]
        min_time = min(clients)
        max_time = max(clients)
        print(f'\nMin Time: {min_time.execution_time}')
        print(f'\nMax Time: {max_time.execution_time}')
        assert all(times_less_than_1)
        unique_ids = set([client.id for client in clients])
        assert len(unique_ids) == len(clients)

    @staticmethod
    def _less_than_1_second(t):
        if t < 1:
            return True
        return False


class TestAsyncIdGetterFromClientShould:

    @pytest.mark.asyncio
    async def test_get_ids_in_less_than_1_second(self):

        async def main(clients):
            tasks = [loop.create_task(client.asyncWork()) for client in clients]
            return await asyncio.gather(*tasks, return_exceptions=True)

        id_getter = ThreadIDGetter()
        clients = [Client(id_getter) for _ in range(10)]
        # execute clients work using asyncio
        loop = asyncio.get_running_loop()
        try:
            loop.run_until_complete(main(clients))
        except Exception as e:
            print("An error Occured")
        finally:
            print('closing loop')
            loop.close()
        times_less_than_1 = [self._less_than_1_second(client.execution_time) for client in clients]
        min_time = min(clients)
        max_time = max(clients)
        print(min_time)
        print(max_time)
        assert all(times_less_than_1)
        unique_ids = set([client.id for client in clients])
        print('Hi')
        assert len(unique_ids) == len(clients)

    @staticmethod
    def _less_than_1_second(t):
        if t < 1:
            return True
        return False
