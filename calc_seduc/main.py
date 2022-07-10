"""Main module of calc_seduc application"""

from calc_seduc.models import ContractCreator, PaymentTableCreator
from calc_seduc.controller import MainController
from calc_seduc.processors import PerHourProcessor
from calc_seduc.connection import defconn


if __name__ == "__main__":
    main = MainController(
        contract_creator=ContractCreator(),
        ptable_creator=PaymentTableCreator,
        processor=PerHourProcessor,
        conn=defconn,
    )
    main()
