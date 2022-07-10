"""Module that offers all types of payment processors objects"""

from typing import Protocol, Type
from calc_seduc.models import Model, ModelCreator


class Processor(Protocol):
    """Protocol that abstracts all application's payment processors"""

    def __init__(self, ptable_creator: Type[ModelCreator], conn=None):
        """Instantiate a Processor object"""

    def process(self, contract: Model):
        """Method that process information from a given contract"""

    # TODO: check what methods a PaymentProcessor should have


class PerHourProcessor:
    """A processor that generates PerHourPayments"""

    # TODO: create PerHourProcessor logic

    def __init__(self, ptable_creator: Type[ModelCreator], conn=None):
        self.ptable_creator = ptable_creator()
        self.payment_tables = self.ptable_creator.get_all(conn=conn)

    def process(self, contract: Model):
        """Method that process information from a given contract"""
        pass


class FormulaProcessor:
    """A processor that generates Formula Payments"""

    # TODO: create FormulaProcessor logic


# Processor logic:
# 1. Define a paymenttable to use
# 2. Calculate, for every month, how many weeks it have,
# considering full weeks and partial weeks
# 3. For every month, calculate payment value based on
# weeks information.
# 4. Stores everything in a Payment object
# 5. Saves payment information on database
