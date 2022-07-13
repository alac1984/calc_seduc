from decimal import Decimal
from dataclasses import dataclass
from functools import lru_cache
from datetime import datetime
from typing import Protocol, Optional, List
from calc_seduc.connection import defconn


class AbstractEarning(Protocol):
    """Protocol that abstracts a Earning"""

    id: Optional[int] = None

    def save(self, conn=None):
        """Saves object data instance into database"""


@dataclass(slots=True)
class Earning:
    """Class that represents a concrete Earning"""

    date: datetime
    value: Decimal
    id: Optional[int] = None

    @property
    def ref_month(self):
        """Return month of reference from earning"""
        return self.date.month - 1 if self.date.month != 1 else 12

    @property
    def ref_year(self):
        """Return year of reference from earning"""
        return self.date.year if self.date.month != 1 else self.date.year - 1

    def save(self, conn=None):
        """Saves Earning instance data on database"""
        if not conn:
            conn = defconn
        cur = conn.cursor()

        if not self.id:
            cur.execute(
                """
                insert into tb_earning
                (date, value) values
                (?, ?)
                returning id
            """,
                (
                    datetime(self.date.year, self.date.month, self.date.day),
                    float(self.value),
                ),
            )
            id = cur.fetchone()[0]
            self.id = id
        else:
            cur.execute(
                """
                update tb_earning
                set date = ?,
                value = ?
                where id = ?;
            """,
                (
                    datetime(self.date.year, self.date.month, self.date.day),
                    float(self.value),
                    self.id,
                ),
            )
        conn.commit()


class EarningFactory:
    """Factory class for Earning instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> Earning:
        """Retrieve a Earning object from database"""

        if not conn:
            conn = defconn
        cur = conn.cursor()
        cur.execute("select * from tb_earning where id = ?", (id,))
        data = cur.fetchone()
        return Earning(id=data[0], date=data[1], value=Decimal(data[2]))

    @lru_cache
    def get_all(self, conn=None) -> List[Earning]:
        """Retrieve all Earning objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_earning")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]
