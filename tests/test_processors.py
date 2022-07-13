from calc_seduc.processors import PerHourProcessor
from calc_seduc.models import ContractFactory, PaymentTableFactory


def test_define_payment_table_case_2022_5(database):
    """Assert if payment table is correctly defined with year/month 2022/5"""
    ptables = PaymentTableFactory().get_all()
    processor = PerHourProcessor(ptables, database)
    ptable = processor.define_payment_table(2022, 5)
    assert ptable.id == 1


def test_define_payment_table_case_2022_2(database):
    """Assert if payment table is correctly defined with year/month 2022/2"""
    ptables = PaymentTableFactory().get_all()
    processor = PerHourProcessor(ptables, database)
    ptable = processor.define_payment_table(2022, 2)
    assert ptable.id == 2


def test_process(database):
    """Not written yet"""
    contract = ContractFactory().get(2, database)
    ptables = PaymentTableFactory().get_all()
    processor = PerHourProcessor(ptables, database)
    value = processor.process(contract, 2022, 6)
    breakpoint()
    assert value
