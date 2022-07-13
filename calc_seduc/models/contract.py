import math
from dataclasses import dataclass
from functools import lru_cache
from datetime import datetime
from typing import Protocol, Optional, List
from calc_seduc.connection import defconn


class AbstractContract(Protocol):
    """Protocol that abstracts a Contract"""

    id: Optional[int] = None

    @property
    def planning(self):
        """Returns round up planning hours"""

    @property
    def total_hours(self):
        """Returns the sum of work hours and planning hours"""

    def save(self, conn=None):
        """Saves object data instance into database"""


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


class ContractFactory:
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
