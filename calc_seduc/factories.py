from decimal import Decimal
from functools import lru_cache
from typing import List
from calc_seduc.connection import defconn
from calc_seduc.models import School, Contract, PaymentTable, Earning, PerHourPayment


class SchoolCreator:
    """Factory class for School instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> School:
        """Retrieve a School object from database"""
        conn = defconn if not conn else conn
        cur = conn.cursor()
        cur.execute("select * from tb_school where id = ?", (id,))
        data = cur.fetchone()
        return School(id=data[0], name=data[1], inep=data[2])

    @lru_cache
    def get_all(self, conn=None) -> List[School]:
        """Retrieve all School objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_school")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]


class ContractCreator:
    """Factory class for Contract instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> Contract:
        """Retrieve a Contract object from database"""

        if not conn:
            conn = defconn
        cur = conn.cursor()
        cur.execute("select * from tb_contract where id = ?", (id,))
        data = cur.fetchone()
        return Contract(
            id=data[0],
            school_id=data[1],
            contract_id=data[2],
            starts=data[3],
            ends=data[4],
            hours=data[5],
        )

    @lru_cache
    def get_all(self, conn=None) -> List[Contract]:
        """Retrieve all Contract objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_contract")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]


class PaymentTableCreator:
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


class EarningCreator:
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


class PerHourPaymentCreator:
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


FACTORIES = {
    "school": SchoolCreator,
    "contract": ContractCreator,
    "paymenttable": PaymentTableCreator,
    "earning": EarningCreator,
    "perhourpayment": PerHourPaymentCreator,
}
