import typing as T

from ssapi.entities import Sale, Return
from ssapi.relational import Database


class ShopDatabase(Database):
    """A database that stores data about shops"""

    def _tables_init(self) -> None:
        """Initialize the tables"""
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS shops"
            "("
            "name VARCHAR(255)"
            ")"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS sales"
            "("
            "id INTEGER PRIMARY KEY,"
            "product VARCHAR(255), "
            "shop VARCHAR(255), "
            "quantity INT, "
            "date DATE DEFAULT CURRENT_TIMESTAMP, "
            "is_discounted BOOLEAN"
            ")"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS returns"
            "("
            "id INTEGER PRIMARY KEY,"
            "product VARCHAR(255), "
            "shop VARCHAR(255), "
            "quantity INT, "
            "date DATE DEFAULT CURRENT_TIMESTAMP"
            ")"
        )

    def add_sales(self, *sales: Sale) -> int:
        """Record sale transactions and return the number of rows created"""
        cur = self.conn.executemany(
            "INSERT INTO sales VALUES(?, ?, ?, ?, ?, ?)",
            (sale.as_tuple() for sale in sales)
        )
        self.conn.commit()
        return cur.rowcount

    def add_returns(self, *returns: Return) -> int:
        """Record sale transactions and return the number of rows created"""
        cur = self.conn.executemany(
            "INSERT INTO returns VALUES(?, ?, ?, ?, ?)",
            (ret.as_tuple() for ret in returns)
        )
        self.conn.commit()
        return cur.rowcount

    def get_shops(self) -> T.Generator[str, None, None]:
        """Get all the shops"""
        cur = self.conn.execute(
            "SELECT DISTINCT shop FROM sales"
        )
        for shop, *_ in cur.fetchall():
            yield shop

    def get_sales(self,
                  date_start=None,
                  date_end=None) -> T.Generator[Sale, None, None]:
        """Get the sales according to the given criteria"""
        cur = self.conn.execute("SELECT * FROM sales")
        for result in cur.fetchall():
            yield Sale(*result)

    def get_returns(self,
                    date_start=None,
                    date_end=None) -> T.Generator[Return, None, None]:
        """Get the sales according to the given criteria"""
        cur = self.conn.execute("SELECT * FROM returns")
        for result in cur.fetchall():
            yield Return(*result)
