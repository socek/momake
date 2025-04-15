from functools import cache

import logan.runlog.tables
from logan.runlog.db import metadata
from sqlalchemy import create_engine


@cache
def engine():
    url = "sqlite:///logan.db"
    engine = create_engine(url)
    metadata.create_all(engine, checkfirst=True)
    return engine
