"""Main module of calc_seduc application"""

from models import ContractCreator, PaymentTableCreator
from controller import MainController
from processors import PerHourProcessor
from connection import defconn


if __name__ == "__main__":
    main = MainController(
        contract_creator=ContractCreator(),
        ptable_creator=PaymentTableCreator,
        processor=PerHourProcessor,
        conn=defconn,
    )
    main()
