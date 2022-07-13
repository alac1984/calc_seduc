from decimal import Decimal
from dataclasses import dataclass
from functools import lru_cache
from datetime import datetime
from typing import Protocol, Optional, List
from calc_seduc.connection import defconn


class AbstractPayment(Protocol):
    """Protocol that abstracts Payment"""

    id: Optional[int] = None

    def save(self, conn=None):
        """Saves object data instance into database"""


@dataclass(slots=True)
class PerHourPayment:
    """Class that represents a PerHourPayment"""

    contract_id: int
    paymenttable_id: int
    process_date: datetime
    ref_month: int
    ref_year: int
    value: Decimal
    id: Optional[int] = None

    def save(self, conn=None):
        """Saves PerHourPayment instance data on database"""
        if not conn:
            conn = defconn
        cur = conn.cursor()

        if not self.id:
            cur.execute(
                """
                insert into tb_perhourpayment (
                        contract_id,
                        paymenttable_id,
                        process_date,
                        ref_month,
                        ref_year,
                        value
                ) values (?, ?, ?, ?, ?, ?)
                returning id
            """,
                (
                    self.contract_id,
                    self.paymenttable_id,
                    datetime(
                        self.process_date.year,
                        self.process_date.month,
                        self.process_date.day,
                    ),
                    self.ref_month,
                    self.ref_year,
                    float(self.value),
                ),
            )
            id = cur.fetchone()[0]
            self.id = id
        else:
            cur.execute(
                """
                update tb_perhourpayment
                set contract_id = ?,
                    paymenttable_id = ?,
                    process_date = ?,
                    ref_month = ?,
                    ref_year = ?,
                    value = ?
                where id = ?;
            """,
                (
                    self.contract_id,
                    self.paymenttable_id,
                    datetime(
                        self.process_date.year,
                        self.process_date.month,
                        self.process_date.day,
                    ),
                    self.ref_month,
                    self.ref_year,
                    float(self.value),
                    self.id,
                ),
            )
        conn.commit()


@dataclass
class FormulaPayment:
    """Class that represents a FormulaPayment"""

    pass

    # TODO: implement its logic


class AbstractPaymentFactory(Protocol):
    """Protocol that abstracts PaymentFactory"""

    def get(self, id: int, conn=None) -> AbstractPayment:
        """Retrieve a Payment object from database"""

    def get_all(self, conn=None) -> List[PerHourPayment]:
        """Retrieve all PerHourPayment objects from database"""


class PerHourPaymentFactory:
    """Factory class for PerHourPayment instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> PerHourPayment:
        """Retrieve a PerHourPayment object from database"""

        if not conn:
            conn = defconn
        cur = conn.cursor()
        cur.execute("select * from tb_perhourpayment where id = ?", (id,))
        data = cur.fetchone()
        return PerHourPayment(
            id=data[0],
            contract_id=data[1],
            paymenttable_id=data[2],
            process_date=data[3],
            ref_month=data[4],
            ref_year=data[5],
            value=Decimal(data[6]),
        )

    @lru_cache
    def get_all(self, conn=None) -> List[PerHourPayment]:
        """Retrieve all PerHourPayment objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_perhourpayment")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]


class FormulaPaymentFactory:
    """Factory class for PerHourPayment instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> PerHourPayment:
        """Retrieve a PerHourPayment object from database"""
        pass

        # TODO: create this method logic

    @lru_cache
    def get_all(self, conn=None) -> List[PerHourPayment]:
        """Retrieve all PerHourPayment objects from database"""
        pass

        # TODO: create this method logic


class PaymentFactory:
    """Concrete Factory for Payment"""

    def __init__(self):
        self.factories = {
            "perhour": PerHourPaymentFactory,
            "formula": FormulaPaymentFactory,
        }

    def __call__(self, payment: str):
        return self.factories[payment]()
