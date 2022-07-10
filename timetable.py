"""Module that deals with weeks, dates and stuff"""

from typing import List, Tuple
from functools import lru_cache
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY, YEARLY
from models import Contract


def get_actual_month_and_year() -> Tuple[int, int]:
    return (datetime.now().year, datetime.now().month)
