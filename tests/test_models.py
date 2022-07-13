"""Unit tests for data.py module"""

from datetime import datetime
from decimal import Decimal
from calc_seduc.models import (
    School,
    SchoolFactory,
    Contract,
    ContractFactory,
    PaymentTable,
    PaymentTableFactory,
    Earning,
    EarningFactory,
    PerHourPayment,
    PaymentFactory,
)


def test_declarative_datatype_dates(database):
    """Assert if dates are being parsed by sqlite3 correctly"""
    cur = database.cursor()
    cur.execute("select * from tb_contract")
    result = cur.fetchall()
    assert isinstance(result[0][3], datetime)


def test_school_save_new_instance(database):
    """
    Test if School save method creates a new instance
    and saves it in database
    """
    school = School(name="Rogério Fróes", inep=3934039)
    school.save(database)
    cur = database.cursor()
    cur.execute("select * from tb_school where id = ?", (school.id,))
    result = cur.fetchone()
    assert school.name == result[1]


def test_school_save_update(database):
    """Test if School save method updates an existing object"""
    school = SchoolFactory().get(1, conn=database)
    school.name = "This is it"
    school.save(conn=database)
    new_school = SchoolFactory().get(school.id, conn=database)
    assert school.name == new_school.name

    # TODO: fix all test_models with new organization


def test_school_creator_get(database):
    """Test if SchoolCreator get method works"""
    school = SchoolFactory().get(1, conn=database)
    assert isinstance(school, School)


def test_school_creator_get_all(database):
    """Test if SchoolCreator get_all method is working"""
    schools = SchoolFactory().get_all(conn=database)
    check = True
    for school in schools:
        if not isinstance(school, School):
            check = False
    assert check


def test_contract_save_new_instance(database):
    """
    Test if Contract save method saves a new instance
    on database
    """
    contract = Contract(
        school_id=1,
        contract_id=1,
        starts=datetime(2022, 1, 1, 0, 0, 0, 1),
        ends=datetime(2022, 3, 1, 0, 0, 0, 1),
        hours=10,
    )
    contract.save(conn=database)
    cur = database.cursor()
    cur.execute("select * from tb_contract where id = ?", (contract.id,))
    result = cur.fetchone()
    assert result[5] == 10


def test_contract_save_update(database):
    """
    Test if Contract save method updates an object
    already stored on database
    """
    contract = ContractFactory().get(id=1, conn=database)
    contract.hours = 999
    contract.save(conn=database)

    new_contract = ContractFactory().get(contract.id, conn=database)
    assert contract.hours == new_contract.hours


def test_contract_creator_get(database):
    """Test if ContractCreator get method works"""
    contract = ContractFactory().get(1, conn=database)
    assert isinstance(contract, Contract)


def test_contract_creator_get_all(database):
    """Test if ContractCreator get_all method is working"""
    contracts = ContractFactory().get_all(conn=database)
    check = True
    for contract in contracts:
        if not isinstance(contract, Contract):
            check = False
    assert check


def test_contract_start_date(database):
    """Test if contract start is a datetime object"""
    contract = ContractFactory().get(1, conn=database)
    assert isinstance(contract.starts, datetime)


def test_contract_property_planning_type(database):
    """Assert if contract planning property is an int"""
    contract = ContractFactory().get(1, conn=database)
    assert isinstance(contract.planning, int)


def test_contract_property_planning_value(database):
    """Assert if contract planning property is correctly calculated"""
    contract = Contract(
        school_id=1,
        contract_id=1,
        starts=datetime(2022, 1, 1, 0, 0, 0, 1),
        ends=datetime(2022, 3, 1, 0, 0, 0, 1),
        hours=10,
    )
    assert contract.planning == 4


def test_contract_property_total_hours_type(database):
    """Assert if contract total hours property is an int"""
    contract = Contract(
        school_id=1,
        contract_id=1,
        starts=datetime(2022, 1, 1, 0, 0, 0, 1),
        ends=datetime(2022, 3, 1, 0, 0, 0, 1),
        hours=10,
    )
    assert isinstance(contract.total_hours, int)


def test_contract_property_total_hours_value(database):
    """Assert if contract total hours property is correctly calculated"""
    contract = Contract(
        school_id=1,
        contract_id=1,
        starts=datetime(2022, 1, 1, 0, 0, 0, 1),
        ends=datetime(2022, 3, 1, 0, 0, 0, 1),
        hours=10,
    )
    assert contract.total_hours == 14


def test_payment_table_save_new_instance(database):
    """Test if PaymentTable save method saves a new instance"""
    ptable = PaymentTable(
        starts=datetime(2022, 1, 1, 0, 0, 0, 1),
        ends=datetime(2022, 2, 1, 0, 0, 0, 1),
        hour_value=Decimal(2.4),
        prv=Decimal(1.2),
        eoy_bonus=Decimal(4.2),
    )
    ptable.save(conn=database)
    cur = database.cursor()
    cur.execute("select * from tb_paymenttable where id = ?", (ptable.id,))
    result = cur.fetchone()
    assert result[3] == float(ptable.hour_value)


def test_payment_table_save_update_instance(database):
    """
    Assert if PaymentTable save method updates an instance
    of a object already saved in database
    """
    ptable = PaymentTable(
        starts=datetime(2022, 1, 1, 0, 0, 0, 1),
        ends=datetime(2022, 2, 1, 0, 0, 0, 1),
        hour_value=Decimal(2.4),
        prv=Decimal(1.2),
        eoy_bonus=Decimal(4.2),
    )
    ptable.prv = Decimal(9.999)
    ptable.save(conn=database)
    new_ptable = PaymentTableFactory().get(ptable.id, conn=database)
    assert new_ptable.prv == ptable.prv


def test_payment_table_creator_get(database):
    """Test if PaymentTableCreator get method works"""
    ptable = PaymentTableFactory().get(1, conn=database)
    assert isinstance(ptable, PaymentTable)


def test_payment_table_creator_get_all(database):
    """Test if PaymentTableCreator retrieve_all method is working"""
    ptables = PaymentTableFactory().get_all(conn=database)
    check = True
    for ptable in ptables:
        if not isinstance(ptable, PaymentTable):
            check = False
    assert check


def test_payment_table_hour_value_decimal(database):
    """Assert that PaymentTable hour_value is decimal"""
    ptable = PaymentTableFactory().get(1, conn=database)
    assert isinstance(ptable.hour_value, Decimal)


def test_payment_table_prv_decimal(database):
    """Assert that PaymentTable prv is decimal"""
    ptable = PaymentTableFactory().get(1, conn=database)
    assert isinstance(ptable.prv, Decimal)


def test_payment_table_prv_eoy_bonus(database):
    """Assert that PaymentTable eoy_bonus is decimal"""
    ptable = PaymentTableFactory().get(1, conn=database)
    assert isinstance(ptable.eoy_bonus, Decimal)


def test_payment_table_is_applicable_case_true(database):
    """Assert if PaymentTable is_applicable is working"""
    ptable = PaymentTableFactory().get(1, conn=database)
    assert ptable.is_applicable(7, 2022) is True


def test_payment_table_is_applicable_case_false(database):
    """Assert if PaymentTable is_applicable is working"""
    ptable = PaymentTableFactory().get(2, conn=database)
    assert ptable.is_applicable(5, 2022) is False


def test_earning_save_new_instance(database):
    """
    Test if Earning save method stores a new
    instance on database
    """
    earning = Earning(
        date=datetime(2022, 1, 1, 0, 0, 0, 1), value=Decimal("3.999999999999")
    )
    earning.save(conn=database)
    cur = database.cursor()
    cur.execute("select * from tb_earning where id = ?", (earning.id,))
    result = cur.fetchone()
    assert float(earning.value) == result[2]


def test_earning_save_update(database):
    """
    Test if Earning save method updates an already saved
    instance on database
    """
    earning = Earning(
        date=datetime(2022, 1, 1, 0, 0, 0, 1), value=Decimal("3.999999999999")
    )
    earning.value = Decimal(3.14)
    earning.save(conn=database)

    new_earning = EarningFactory().get(earning.id, conn=database)
    assert earning.value == new_earning.value


def test_earning_creator_get(database):
    """Test if EarningCreator get method works"""
    earning = EarningFactory().get(1, conn=database)
    assert isinstance(earning, Earning)


def test_earning_value_decimal(database):
    """Test if earning value is a Decimal"""
    earning = EarningFactory().get(1, conn=database)
    assert isinstance(earning.value, Decimal)


def test_earning_ref_month_with_month_01(database):
    """Test if earning ref month is correctly calculated
    given date.month = 1"""
    earning = Earning(
        date=datetime(2022, 1, 1, 0, 0, 0, 1), value=Decimal("3.999999999999")
    )
    assert earning.ref_month == 12


def test_earning_ref_month_with_month_02(database):
    """Test if earning ref month is correctly calculated
    given date.month = 2"""
    earning = Earning(
        date=datetime(2022, 1, 1, 0, 0, 0, 1), value=Decimal("3.999999999999")
    )
    earning.date = datetime(2022, 2, 1, 0, 0, 0, 0)
    assert earning.ref_month == 1


def test_earning_creator_get_all(database):
    """Test if EarningCreator get_all method is working"""
    earnings = EarningFactory().get_all(conn=database)
    check = True
    for earning in earnings:
        if not isinstance(earning, Earning):
            check = False
    assert check


def test_perhourpayment_save_new_instance(database):
    """
    Test if PerHourPayment save method stores a new
    instance on database
    """
    perhourpayment = PerHourPayment(
        contract_id=1,
        paymenttable_id=1,
        ref_month=3,
        ref_year=2022,
        process_date=datetime(2022, 1, 1, 0, 0, 0, 1),
        value=Decimal("1094.99"),
    )
    perhourpayment.save(conn=database)
    cur = database.cursor()
    cur.execute("select * from tb_perhourpayment where id = ?", (perhourpayment.id,))
    result = cur.fetchone()

    assert float(perhourpayment.value) == result[6]


def test_perhourpayment_save_update(database):
    """
    Test if PerHourPayment save method updates an already saved
    instance on database
    """
    perhourpayment = PaymentFactory()("perhour").get(id=1, conn=database)
    perhourpayment.value = Decimal(3.14)
    perhourpayment.save(conn=database)

    new_payment = PaymentFactory()("perhour").get(id=perhourpayment.id, conn=database)

    assert perhourpayment.value == new_payment.value


def test_perhourpayment_creator_get(database):
    """Test if PerHourPaymentCreator get method works"""
    perhourpayment = PaymentFactory()("perhour").get(1, conn=database)
    assert isinstance(perhourpayment, PerHourPayment)


def test_perhourpayment_creator_get_all(database):
    """Test if PerHourPaymentCreator get_all method is working"""
    payments = PaymentFactory()("perhour").get_all(conn=database)
    check = True
    for payment in payments:
        if not isinstance(payment, PerHourPayment):
            check = False
    assert check
