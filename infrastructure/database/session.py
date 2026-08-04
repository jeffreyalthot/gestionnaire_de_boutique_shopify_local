from contextlib import contextmanager
from typing import Iterator
import sqlite3
from infrastructure.database.engine import Database

@contextmanager
def database_session(db: Database) -> Iterator[sqlite3.Connection]:
    with db.transaction() as connection:
        yield connection
