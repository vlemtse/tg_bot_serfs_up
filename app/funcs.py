from datetime import datetime, UTC
from uuid import uuid4


def str_datetime():
    return str(datetime.now(UTC))


def str_uuid4():
    return str(uuid4())
