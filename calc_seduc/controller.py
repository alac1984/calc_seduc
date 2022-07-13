from typing import Protocol, Type, List
from calc_seduc.connection import defconn
from calc_seduc.models import (
    AbstractContract,
    AbstractPayment,
    ContractFactory,
    PaymentTableFactory,
)
from calc_seduc.processors import AbstractProcessor
from calc_seduc.utils import get_processed_contracts_ids


class AbstractController(Protocol):
    """Protocol that abstracts a controller calc_seduc application"""

    def __call__(self):
        """Execute Controller's pipeline"""

    def get_non_processed_contracts(self) -> List[AbstractContract]:
        """Method that gets all non processed contracts on database"""

    def process_contracts(self) -> None:
        """Method that process every contract in self.unprocessed using the
        provided processor"""

    def save_data(self) -> None:
        """Method that saves payments in self.payments on database"""

    def export_csv(self) -> None:
        """Method that creates a csv spreadsheet with all payment and earnings
        analysis"""


class Controller:
    """
    Class that represents the MainController of this application.
    The MainController is meant to process contracts, save processed data
    in database and create csv files to show this information
    """

    def __init__(
        self,
        contract_factory: ContractFactory,
        ptable_factory: Type[PaymentTableFactory],
        processor: Type[AbstractProcessor],
        conn=None,
    ):  # noqa
        self.conn = defconn if not conn else conn
        ptables = ptable_factory().get_all(self.conn)
        self.contract_factory = contract_factory
        self.processor = processor(ptables)
        self.unprocessed: List[AbstractContract] = []
        self.payments: List[AbstractPayment] = []

    def __call__(self):
        """Executes MainController process"""
        # 1. Check for non processed contracts
        self.get_non_processed_contracts()
        # 2. Process per hour payments for every non processed contract
        self.process_contracts()
        # 3. Save this processed information in database
        self.save_data()
        # 4. Creates a .csv with detailed information
        self.export_csv()

    def get_non_processed_contracts(self) -> None:
        """Method that gets all non processed contracts on database"""
        contracts = self.contract_factory.get_all(conn=self.conn)
        processed_ids = get_processed_contracts_ids(conn=self.conn)
        self.unprocessed = [
            contract for contract in contracts if contract.id not in processed_ids
        ]

    def process_contracts(self) -> None:
        """Method that process every contract in self.unprocessed using the
        provided processor"""
        for contract in self.unprocessed:
            self.payments.append(
                self.processor.process(contract=contract, year=2022, month=2)
            )

    def save_data(self) -> None:
        """Method that saves payments in self.payments on database"""
        for payment in self.payments:
            payment.save()

    def export_csv(self) -> None:
        """Method that creates a csv spreadsheet with all payment and earnings
        analysis"""
        print("csv created")
        # TODO: create export_csv logic
