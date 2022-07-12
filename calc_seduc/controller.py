from typing import Type, List
from calc_seduc.connection import defconn
from calc_seduc.models import Contract
from calc_seduc.factories import ContractCreator
from calc_seduc.protocols import Model, Processor, ModelCreator
from calc_seduc.utils import get_processed_contracts_ids


class MainController:
    """
    Class that represents the MainController of this application.
    The MainController is meant to process contracts, save processed data
    in database and create csv files to show this information
    """

    def __init__(
        self,
        contract_creator: ContractCreator,
        ptable_creator: Type[ModelCreator],
        processor: Type[Processor],
        conn=None,
    ):  # noqa
        self.conn = defconn if not conn else conn
        ptables = ptable_creator().get_all(self.conn)
        self.contract_creator = contract_creator
        self.processor = processor(ptables)
        self.unprocessed: List[Contract] = []
        self.payments: List[Model] = []

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
        contracts = self.contract_creator.get_all(conn=self.conn)
        processed_ids = get_processed_contracts_ids(conn=self.conn)
        self.unprocessed = [
            contract for contract in contracts if contract.id not in processed_ids
        ]

    def process_contracts(self) -> None:
        """Method that process every contract in self.unprocessed using the
        provided processor"""
        for contract in self.unprocessed:
            self.payments.append(self.processor.process(contract=contract))

    def save_data(self) -> None:
        """Method that saves payments in self.payments on database"""
        for payment in self.payments:
            payment.save()

    def export_csv(self) -> None:
        """Method that creates a csv spreadsheet with all payment and earnings
        analysis"""
        print("csv created")
        # TODO: create export_csv logic
