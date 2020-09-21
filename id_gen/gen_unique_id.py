from typing import List
import time
import uuid


def gen_unique_id(cnt: int) -> List:
    sleep_for = ((cnt-1) // 10000) + 1
    time.sleep(sleep_for)
    return [uuid.uuid4() for _ in range(cnt)]
