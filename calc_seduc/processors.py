"""Module that offers all types of payment processors objects"""

from decimal import Decimal
from typing import List
from calc_seduc.models import Contract, PaymentTable
from calc_seduc.calendar import Month


class NoPaymentTable(Exception):
    """This error is raised when PerHourProcessor did not find a PaymentTable
    applicable for a given year/month"""

    pass


class PerHourProcessor:
    """A processor that generates PerHourPayments"""

    # TODO: create PerHourProcessor logic

    def __init__(self, payment_tables: List[PaymentTable], conn=None):
        self.payment_tables = payment_tables

    def define_payment_table(self, year: int, month: int) -> PaymentTable:
        """Get payment table, raise KeyError if none"""
        for table in self.payment_tables:
            if table.is_applicable(month, year):
                return table
        raise NoPaymentTable(f"No payment table for {year}/{month}")

    def process(self, contract: Contract, year: int, month: int) -> Decimal:
        """Method that process information from a given contract"""
        ptable = self.define_payment_table(year, month)
        month_obj = Month(year, month)
        value = Decimal(0)
        for week in month_obj.weeks:
            value += (
                (ptable.hour_value * Decimal(contract.total_hours)) / 5 * week.workdays
            )

        return value


class FormulaProcessor:
    """A processor that generates Formula Payments"""

    # TODO: create FormulaProcessor logic
