from datetime import datetime, UTC
from uuid import uuid4


def str_datetime(tz: bool = True) -> str:
    dt = datetime.now(UTC)
    if tz:
        return dt.strftime("%Y-%m-%d_%H:%M:%S.%fZ")[:-3]
    else:
        return dt.strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3]


def str_datetime_file(tz: bool = True) -> str:
    dt = datetime.now(UTC)
    if tz:
        return dt.strftime("%Y-%m-%d_%H_%M_%S_%fZ")[:-3]
    else:
        return dt.strftime("%Y-%m-%d_%H_%M_%S_%f")[:-3]


def str_uuid4():
    return str(uuid4())


async def prepare_data(prefix: str, data: str):
    return data.replace(prefix, "").replace("_", " ")
