from decimal import Decimal
from dataclasses import dataclass
from functools import lru_cache
from datetime import datetime
from typing import Protocol, Optional, List
from calc_seduc.connection import defconn


class AbstractPaymentTable(Protocol):
    """Protocol that abstracts PaymentTable"""

    id: Optional[int] = None

    def save(self, conn=None):
        """Saves object data instance into database"""


@dataclass(slots=True)
class PaymentTable:
    """Class that represents a concrete PaymentTable"""

    starts: datetime
    ends: datetime
    hour_value: Decimal
    prv: Decimal
    eoy_bonus: Decimal  # end of year bonus
    id: Optional[int] = None

    def save(self, conn=None):
        """Saves Payment instance data on database"""

        if not conn:
            conn = defconn
        cur = conn.cursor()

        if not self.id:
            cur.execute(
                """
                insert into tb_paymenttable
                (starts, ends, hour_value, prv, eoy_bonus) values
                (?, ?, ?, ?, ?)
                returning id
            """,
                (
                    self.starts,
                    self.ends,
                    float(self.hour_value),
                    float(self.prv),
                    float(self.eoy_bonus),
                ),
            )
            id = cur.fetchone()[0]
            self.id = id
        else:
            cur.execute(
                """
                update tb_paymenttable
                set starts = ?,
                    ends = ?,
                    hour_value = ?,
                    prv = ?,
                    eoy_bonus = ?
                where id = ?;
            """,
                (
                    datetime(self.starts.year, self.starts.month, self.starts.day),
                    datetime(self.ends.year, self.ends.month, self.ends.day),
                    float(self.hour_value),
                    float(self.prv),
                    float(self.eoy_bonus),
                    self.id,
                ),
            )
        conn.commit()

    def is_applicable(self, month: int, year: int) -> bool:
        """Check if a PaymentTable is applicable for a given month and year"""
        return (
            self.starts.month <= month <= self.ends.month
            and self.starts.year <= year <= self.ends.year
        )


class PaymentTableFactory:
    """Factory class for PaymentTable instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> PaymentTable:
        """Retrieve a PaymentTable object from database"""

        if not conn:
            conn = defconn
        cur = conn.cursor()
        cur.execute("select * from tb_paymenttable where id = ?", (id,))
        data = cur.fetchone()
        return PaymentTable(
            id=data[0],
            starts=data[1],
            ends=data[2],
            hour_value=Decimal(data[3]),
            prv=Decimal(data[4]),
            eoy_bonus=Decimal(data[5]),
        )

    @lru_cache
    def get_all(self, conn=None) -> List[PaymentTable]:
        """Retrieve all PaymentTable objects from database"""
        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_paymenttable")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]
