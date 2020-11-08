from typing import List
import time
import uuid
import datetime

today = datetime.datetime.now()


def gen_unique_id(cnt):
    """Generate a list of unique IDs

    Args:
        cnt (int): The number of unique IDs you would like to be  returned

    Returns:
        List: A list of unique IDs
    """
    sleep_for = ((cnt-1) // 10000) + 1
    time.sleep(sleep_for)
    return [uuid.uuid4() for _ in range(cnt)]
