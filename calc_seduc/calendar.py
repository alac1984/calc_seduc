"""Module that deals with weeks, dates and stuff"""

import calendar
from datetime import datetime, timedelta
from typing import List, Optional


class InvalidWeek(Exception):
    """This error will be raised if we try to create a week with the same day
    for start and end days and without workdays. It happens sometimes when a
    month's last day is saturday or sunday"""

    pass


class Week:
    def __init__(self, starts: datetime, ends: datetime, workdays: int):
        if starts == ends and workdays == 0:
            raise InvalidWeek("This is not a valid week")

        self.starts = starts
        self.ends = ends
        self.workdays = workdays

    def __repr__(self):
        return f"Week(starts={self.starts}, ends={self.ends}, workdays={self.workdays})"


class Month:
    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month
        self.weeks = []
        self.generate_weeks()

    def generate_weeks(self) -> None:
        """Create Week objects and stores them in weeks attribute"""
        first_day = datetime(self.year, self.month, 1, 0, 0, 0, 0)
        last_day = datetime(
            self.year,
            self.month,
            calendar.monthrange(self.year, self.month)[1],
            0,
            0,
            0,
            0,
        )

        day = first_day
        workdays = 0
        while day <= last_day:
            if day.weekday() <= 4:
                workdays += 1

            if day.weekday() == 6:
                try:
                    self.weeks.append(Week(first_day, day, workdays))
                except InvalidWeek:
                    pass
                first_day = day + timedelta(days=1)
                workdays = 0

            day += timedelta(days=1)
        else:
            try:
                self.weeks.append(Week(first_day, day, workdays))
            except InvalidWeek:
                pass

        def __repr__(self):
            return f"Month(year={self.year}, month={self.month}, weeks={self.weeks}))"
