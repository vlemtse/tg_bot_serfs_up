from datetime import datetime, UTC, timezone, timedelta
from uuid import uuid4


def str_datetime(tz: bool = True) -> str:
    dt = datetime.now(UTC)
    if tz:
        return dt.strftime("%Y-%m-%d_%H:%M:%S.%fZ")[:-3]
    else:
        return dt.strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3]


async def str_datetime_file(include_time: bool = True) -> str:
    dt = await get_datetime_shri()
    if include_time:
        return dt.strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
    else:
        return dt.strftime("%Y_%m_%d")


def str_uuid4():
    return str(uuid4())


async def prepare_data(prefix: str, data: str):
    return data.replace(prefix, "").replace("_", " ")


async def get_datetime_shri() -> datetime:
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))
