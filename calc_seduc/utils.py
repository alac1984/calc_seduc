from sqlite3 import Connection
from functools import lru_cache
from typing import List


@lru_cache
def get_processed_contracts_ids(conn: Connection) -> List[int]:
    """Function that gets all processed contracts ids"""
    cur = conn.cursor()
    cur.execute("select id from tb_perhourpayment")
    result = cur.fetchall()
    return [r[0] for r in result]
