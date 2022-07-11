"""Unit tests for data.py module"""

from datetime import datetime
from decimal import Decimal
from calc_seduc.models import (
    School,
    Contract,
    PaymentTable,
    Earning,
    PerHourPayment,
)
from calc_seduc.factories import FACTORIES


def test_declarative_datatype_dates(database):
    """Assert if dates are being parsed by sqlite3 correctly"""
    cur = database.cursor()
    cur.execute("select * from tb_contract")
    result = cur.fetchall()
    assert isinstance(result[0][3], datetime)


def test_school_save_new_instance(objs):
    """
    Test if School save method creates a new instance
    and saves it in database
    """
    objs.school.save(conn=objs.conn)
    cur = objs.conn.cursor()
    cur.execute("select * from tb_school where id = ?", (objs.school.id,))
    result = cur.fetchone()
    assert objs.school.name == result[1]


def test_school_save_update(objs):
    """Test if School save method updates an existing object"""
    objs.school.name = "This is it"
    objs.school.save(conn=objs.conn)
    new_school = FACTORIES["school"]().get(objs.school.id, conn=objs.conn)
    assert objs.school.name == new_school.name


def test_school_creator_get(objs):
    """Test if SchoolCreator get method works"""
    school = FACTORIES["school"]().get(1, conn=objs.conn)
    assert isinstance(school, School)


def test_school_creator_get_all(objs):
    """Test if SchoolCreator get_all method is working"""
    schools = FACTORIES["school"]().get_all(conn=objs.conn)
    check = True
    for school in schools:
        if not isinstance(school, School):
            check = False
    assert check


def test_contract_save_new_instance(objs):
    """
    Test if Contract save method saves a new instance
    on database
    """
    objs.contract.save(conn=objs.conn)
    cur = objs.conn.cursor()
    cur.execute("select * from tb_contract where id = ?", (objs.contract.id,))
    result = cur.fetchone()
    assert result[5] == 10


def test_contract_save_update(objs):
    """
    Test if Contract save method updates an object
    already stored on database
    """
    objs.contract.hours = 999
    objs.contract.save(conn=objs.conn)

    new_contract = FACTORIES["contract"]().get(objs.contract.id, conn=objs.conn)
    assert objs.contract.hours == new_contract.hours


def test_contract_creator_get(objs):
    """Test if ContractCreator get method works"""
    contract = FACTORIES["contract"]().get(1, conn=objs.conn)
    assert isinstance(contract, Contract)


def test_contract_creator_get_all(objs):
    """Test if ContractCreator get_all method is working"""
    contracts = FACTORIES["contract"]().get_all(conn=objs.conn)
    check = True
    for contract in contracts:
        if not isinstance(contract, Contract):
            check = False
    assert check


def test_contract_start_date(objs):
    """Test if contract start is a datetime object"""
    contract = FACTORIES["contract"]().get(1, conn=objs.conn)
    assert isinstance(contract.starts, datetime)


def test_contract_property_planning_type(objs):
    """Assert if contract planning property is an int"""
    contract = FACTORIES["contract"]().get(1, conn=objs.conn)
    assert isinstance(contract.planning, int)


def test_contract_property_planning_value(objs):
    """Assert if contract planning property is correctly calculated"""
    assert objs.contract.planning == 4


def test_contract_property_total_hours_type(objs):
    """Assert if contract total hours property is an int"""
    assert isinstance(objs.contract.total_hours, int)


def test_contract_property_total_hours_value(objs):
    """Assert if contract total hours property is correctly calculated"""
    assert objs.contract.total_hours == 14


def test_payment_table_save_new_instance(objs):
    """Test if PaymentTable save method saves a new instance"""
    objs.ptable.save(conn=objs.conn)
    cur = objs.conn.cursor()
    cur.execute("select * from tb_paymenttable where id = ?", (objs.ptable.id,))
    result = cur.fetchone()
    assert result[3] == float(objs.ptable.hour_value)


def test_payment_table_save_update_instance(objs):
    """
    Assert if PaymentTable save method updates an instance
    of a object already saved in database
    """
    objs.ptable.prv = Decimal(9.999)
    objs.ptable.save(conn=objs.conn)
    new_ptable = FACTORIES["paymenttable"]().get(objs.ptable.id, conn=objs.conn)
    assert new_ptable.prv == objs.ptable.prv


def test_payment_table_creator_get(objs):
    """Test if PaymentTableCreator get method works"""
    ptable = FACTORIES["paymenttable"]().get(1, conn=objs.conn)
    assert isinstance(ptable, PaymentTable)


def test_payment_table_creator_get_all(objs):
    """Test if PaymentTableCreator retrieve_all method is working"""
    ptables = FACTORIES["paymenttable"]().get_all(conn=objs.conn)
    check = True
    for ptable in ptables:
        if not isinstance(ptable, PaymentTable):
            check = False
    assert check


def test_payment_table_hour_value_decimal(objs):
    """Assert that PaymentTable hour_value is decimal"""
    ptable = FACTORIES["paymenttable"]().get(1, conn=objs.conn)
    assert isinstance(ptable.hour_value, Decimal)


def test_payment_table_prv_decimal(objs):
    """Assert that PaymentTable prv is decimal"""
    ptable = FACTORIES["paymenttable"]().get(1, conn=objs.conn)
    assert isinstance(ptable.prv, Decimal)


def test_payment_table_prv_eoy_bonus(objs):
    """Assert that PaymentTable eoy_bonus is decimal"""
    ptable = FACTORIES["paymenttable"]().get(1, conn=objs.conn)
    assert isinstance(ptable.eoy_bonus, Decimal)


def test_earning_save_new_instance(objs):
    """
    Test if Earning save method stores a new
    instance on database
    """
    objs.earning.save(conn=objs.conn)
    cur = objs.conn.cursor()
    cur.execute("select * from tb_earning where id = ?", (objs.earning.id,))
    result = cur.fetchone()
    assert float(objs.earning.value) == result[2]


def test_earning_save_update(objs):
    """
    Test if Earning save method updates an already saved
    instance on database
    """
    objs.earning.value = Decimal(3.14)
    objs.earning.save(conn=objs.conn)

    new_earning = FACTORIES["earning"]().get(objs.earning.id, conn=objs.conn)
    assert objs.earning.value == new_earning.value


def test_earning_creator_get(objs):
    """Test if EarningCreator get method works"""
    earning = FACTORIES["earning"]().get(1, conn=objs.conn)
    assert isinstance(earning, Earning)


def test_earning_value_decimal(objs):
    """Test if earning value is a Decimal"""
    earning = FACTORIES["earning"]().get(1, conn=objs.conn)
    assert isinstance(earning.value, Decimal)


def test_earning_ref_month_with_month_01(objs):
    """Test if earning ref month is correctly calculated
    given date.month = 1"""
    assert objs.earning.ref_month == 12


def test_earning_ref_month_with_month_02(objs):
    """Test if earning ref month is correctly calculated
    given date.month = 2"""
    objs.earning.date = datetime(2022, 2, 1, 0, 0, 0, 0)
    assert objs.earning.ref_month == 1


def test_earning_creator_get_all(objs):
    """Test if EarningCreator get_all method is working"""
    earnings = FACTORIES["earning"]().get_all(conn=objs.conn)
    check = True
    for earning in earnings:
        if not isinstance(earning, Earning):
            check = False
    assert check


def test_perhourpayment_save_new_instance(objs):
    """
    Test if PerHourPayment save method stores a new
    instance on database
    """
    objs.perhourpayment.save(conn=objs.conn)
    cur = objs.conn.cursor()
    cur.execute(
        "select * from tb_perhourpayment where id = ?", (objs.perhourpayment.id,)
    )
    result = cur.fetchone()

    assert float(objs.perhourpayment.value) == result[6]


def test_perhourpayment_save_update(objs):
    """
    Test if PerHourPayment save method updates an already saved
    instance on database
    """
    objs.perhourpayment.value = Decimal(3.14)
    objs.perhourpayment.save(conn=objs.conn)

    new_payment = FACTORIES["perhourpayment"]().get(
        id=objs.perhourpayment.id, conn=objs.conn
    )

    assert objs.perhourpayment.value == new_payment.value


def test_perhourpayment_creator_get(objs):
    """Test if PerHourPaymentCreator get method works"""
    perhourpayment = FACTORIES["perhourpayment"]().get(1, conn=objs.conn)
    assert isinstance(perhourpayment, PerHourPayment)


def test_perhourpayment_creator_get_all(objs):
    """Test if PerHourPaymentCreator get_all method is working"""
    payments = FACTORIES["perhourpayment"]().get_all(conn=objs.conn)
    check = True
    for payment in payments:
        if not isinstance(payment, PerHourPayment):
            check = False
    assert check
