from typing import Protocol, Optional, List, Type
from calc_seduc.models import Contract


class Model(Protocol):
    """Protocol that abstracts all application's Models"""

    id: Optional[int] = None

    def save(self, conn=None):
        """Saves object data instance into database"""


class ModelCreator(Protocol):
    """Protocol that abstracts all application's ModelCreator"""

    def get(self, id: int, conn=None):
        """Method that retrieves a instance of given Model"""

    def get_all(self, conn=None):
        """Method that retrieves all instances from a given Model"""


class Processor(Protocol):
    """Protocol that abstracts all application's payment processors"""

    def process(self, contract: Contract, year: int, month: int):
        """Method that process information from a given contract"""

    # TODO: check what methods a PaymentProcessor should have


class Controller(Protocol):
    """Protocol that abstracts a controller calc_seduc application"""

    def __call__(self):
        """Execute Controller pipeline"""

    def get_non_processed_contracts(self) -> List[Model]:
        """Method that gets all non processed contracts on database"""

    def process_contracts(self) -> None:
        """Method that process every contract in self.unprocessed using the
        provided processor"""

    def save_data(self) -> None:
        """Method that saves payments in self.payments on database"""

    def export_csv(self) -> None:
        """Method that creates a csv spreadsheet with all payment and earnings
        analysis"""
