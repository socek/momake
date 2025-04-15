from functools import cache

from sqlalchemy import create_engine

import logan.runlog.tables
from logan.runlog.db import metadata

FILE_URL = "logan.db"
URL = f"sqlite:///{FILE_URL}"


@cache
def engine():
    engine = create_engine(URL)
    metadata.create_all(engine, checkfirst=True)
    return engine
