import os
import sqlite3

from ssapi.types import Tabular


class Database:
    """A database"""
    conn: sqlite3.Connection
    engine = "sqlite"

    def __init__(self, name: str) -> None:
        self._name = name
        self.open()

    def open(self):
        self.conn = sqlite3.connect(self._name)
        self._tables_init()

    def _tables_init(self) -> None:
        """Initialize the tables"""

    @property
    def name(self) -> str:
        return self._name

    def drop(self) -> None:
        self.conn.close()
        if self.name != ":memory:":
            os.unlink(self.name)


class Table(Tabular):
    """Base class for a Table"""

    def __post_init__(self):
        for key, val in self.as_map():
            cons = getattr(self.Constraints, key, None)
            if cons:
                comparator, value, operator = cons
                if not operator(comparator(val), value):
                    raise ValueError(f"{key}:{val}")

    def create(self) -> None:
        """Create the table"""
        raise NotImplementedError()

    def as_tuple(self):
        return tuple(val for (key, val) in self)

    def as_map(self):
        for key in self.__dataclass_fields__:
            yield (key, getattr(self, key))

    def __iter__(self):
        return iter(self.as_map())
