"""All models for calc_seduc"""

import math
from decimal import Decimal, DefaultContext, setcontext
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Optional, List
from functools import lru_cache
from calc_seduc.connection import defconn

# Decimal default precision
DefaultContext.prec = 9
setcontext(DefaultContext)


class Model(Protocol):
    """Protocol that abstracts all application's Models"""

    id: Optional[int] = None

    def save(self, conn=None):
        """Saves object data instance into database"""


class ModelCreator(Protocol):
    """Protocol that abstracts all application's ModelCreator"""

    def get(self, id: int, conn=None):
        """Method that retrieves a instance of given Model"""

    def get_all(self, conn=None):
        """Method that retrieves all instances from a given Model"""


@dataclass(slots=True)
class School:
    """Class that represents a School"""

    name: str
    inep: int
    id: Optional[int] = None

    def save(self, conn=None):
        """Saves School instance data on database"""
        if not conn:
            conn = defconn
        cur = conn.cursor()

        if not self.id:
            cur.execute(
                """
                insert into tb_school
                (name, inep) values
                (?, ?)
                returning id
            """,
                (self.name, self.inep),
            )
            id = cur.fetchone()[0]
            self.id = id
        else:
            cur.execute(
                """
                update tb_school
                set name = ?,
                    inep = ?
                where id = ?;
            """,
                (self.name, self.inep, self.id),
            )
        conn.commit()


class SchoolCreator:
    """Factory class for School instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> Model:
        """Retrieve a School object from database"""
        conn = defconn if not conn else conn
        cur = conn.cursor()
        cur.execute("select * from tb_school where id = ?", (id,))
        data = cur.fetchone()
        return School(id=data[0], name=data[1], inep=data[2])

    @lru_cache
    def get_all(self, conn=None) -> List[Model]:
        """Retrieve all School objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_school")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]


@dataclass(slots=True)
class Contract:
    """Class that represents a Contract"""

    school_id: int
    contract_id: str
    starts: datetime
    ends: datetime
    hours: int
    id: Optional[int] = None

    @property
    def planning(self):
        """Returns round up planning hours"""
        return math.ceil(self.hours / 3)

    @property
    def total_hours(self):
        """Returns the sum of work hours and planning hours"""
        return self.hours + self.planning

    # TODO: check if this property is needed
    # @property
    # @lru_cache
    # def is_processable(self):
    #     """Given today's date, check if contract should be processed"""
    #     now = datetime.now()

    def save(self, conn=None):
        """Saves Contract instance data on database"""

        if not conn:
            conn = defconn
        cur = conn.cursor()

        if not self.id:
            cur.execute(
                """
                insert into tb_contract
                (school_id, contract_id, starts, ends, hours) values
                (?, ?, ?, ?, ?)
                returning id
            """,
                (
                    self.school_id,
                    self.contract_id,
                    datetime(self.starts.year, self.starts.month, self.starts.day),
                    datetime(self.ends.year, self.ends.month, self.ends.day),
                    self.hours,
                ),
            )
            id = cur.fetchone()[0]
            self.id = id
        else:
            cur.execute(
                """
                update tb_contract
                set school_id = ?,
                starts = ?,
                ends = ?,
                hours = ?
                where id = ?;
            """,
                (self.school_id, self.starts, self.ends, self.hours, self.id),
            )
        conn.commit()


class ContractCreator:
    """Factory class for Contract instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> Model:
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
    def get_all(self, conn=None) -> List[Model]:
        """Retrieve all Contract objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_contract")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]


@dataclass(slots=True)
class PaymentTable:
    """Class that represents a PaymentTable"""

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


class PaymentTableCreator:
    """Factory class for PaymentTable instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> Model:
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
    def get_all(self, conn=None) -> List[Model]:
        """Retrieve all PaymentTable objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_paymenttable")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]


@dataclass(slots=True)
class Earning:
    """Class that represents a Earning"""

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


class EarningCreator:
    """Factory class for Earning instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> Model:
        """Retrieve a Earning object from database"""

        if not conn:
            conn = defconn
        cur = conn.cursor()
        cur.execute("select * from tb_earning where id = ?", (id,))
        data = cur.fetchone()
        return Earning(id=data[0], date=data[1], value=Decimal(data[2]))

    @lru_cache
    def get_all(self, conn=None) -> List[Model]:
        """Retrieve all Earning objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_earning")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]


@dataclass(slots=True)
class PerHourPayment:
    """Class that represents a Per Hour Payment"""

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


class PerHourPaymentCreator:
    """Factory class for PerHourPayment instances"""

    @lru_cache
    def get(self, id: int, conn=None) -> Model:
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
    def get_all(self, conn=None) -> List[Model]:
        """Retrieve all PerHourPayment objects from database"""

        if not conn:
            conn = defconn

        cur = conn.cursor()
        cur.execute("select id from tb_perhourpayment")
        ids = cur.fetchall()
        ids = (id[0] for id in ids)
        return [self.get(id, conn) for id in ids]