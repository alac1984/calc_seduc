from dataclasses import dataclass
from typing import Protocol, Optional, List
from calc_seduc.connection import defconn
from functools import lru_cache


class AbstractSchool(Protocol):
    """Protocol that abstracts School model"""

    id: Optional[int] = None

    def save(self, conn=None):
        """Saves object data instance into database"""


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


class SchoolFactory:
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
