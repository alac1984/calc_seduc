"""Default connection for database"""

import sqlite3


# Default connection
defconn = sqlite3.connect(
    "db.sqlite",
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
)
