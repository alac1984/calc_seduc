from decimal import DefaultContext, setcontext
from .school import AbstractSchool, School, SchoolFactory  # noqa
from .contract import AbstractContract, Contract, ContractFactory  # noqa
from .payment_table import (
    AbstractPaymentTable,
    PaymentTable,
    PaymentTableFactory,
)  # noqa
from .earning import AbstractEarning, Earning, EarningFactory  # noqa
from .payment import (
    AbstractPayment,
    PerHourPayment,
    FormulaPayment,
    PaymentFactory,
)  # noqa


# Decimal default precision
DefaultContext.prec = 9
setcontext(DefaultContext)
