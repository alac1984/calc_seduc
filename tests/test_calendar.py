from datetime import datetime
from calc_seduc.calendar import Week, Month


def test_month_generate_weeks_2022_07_len_weeks():
    """Assert with given method is creating weeks correctly"""
    m = Month(year=2022, month=7)
    assert len(m.weeks) == 5


def test_month_generate_weeks_2022_07_first_week_workdays():
    """Assert with given method is creating weeks correctly"""
    m = Month(year=2022, month=7)
    assert m.weeks[0].workdays == 1


def test_month_generate_weeks_2022_07_second_week_workdays():
    """Assert with given method is creating weeks correctly"""
    m = Month(year=2022, month=7)
    assert m.weeks[2].workdays == 5


def test_month_generate_weeks_2022_06_len_weeks():
    """Assert with given method is creating weeks correctly"""
    m = Month(year=2022, month=6)
    assert len(m.weeks) == 5


def test_month_generate_weeks_2022_06_first_week_workdays():
    """Assert with given method is creating weeks correctly"""
    m = Month(year=2022, month=6)
    assert m.weeks[0].workdays == 3


def test_month_generate_weeks_2022_02_len_weeks():
    """Assert with given method is creating weeks correctly"""
    m = Month(year=2022, month=2)
    assert len(m.weeks) == 5


def test_month_generate_weeks_2022_02_last_week_workdays():
    """Assert with given method is creating weeks correctly"""
    m = Month(year=2022, month=2)
    assert m.weeks[4].workdays == 1
