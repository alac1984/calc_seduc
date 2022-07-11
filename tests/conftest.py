"""Fixtures for testing calc_seduc"""

import sqlite3
from decimal import Decimal
from collections import namedtuple
from datetime import datetime
from pytest import fixture
from calc_seduc.models import (
    School,
    Contract,
    PaymentTable,
    Earning,
    PerHourPayment,
)
from calc_seduc.processors import PerHourProcessor
from calc_seduc.controller import MainController
from calc_seduc.factories import FACTORIES


@fixture(scope="module")
def database():
    """Fixture that define database tables"""
    conn = sqlite3.connect(
        ":memory:", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    cur = conn.cursor()
    cur.execute(
        """
        create table tb_school (
            id integer primary key autoincrement,
            name varchar(100) not null,
            inep integer not null
        );
    """
    )
    cur.execute(
        """
        create table tb_contract (
            id integer primary key autoincrement,
            school_id int not null,
            contract_id varchar(20) not null,
            starts timestamp not null,
            ends timestamp not null,
            hours int not null,
            constraint fk_school_id foreign key (school_id) references tb_school(id)
        );
    """
    )
    cur.execute(
        """
        create table tb_paymenttable (
            id integer primary key autoincrement,
            starts timestamp not null,
            ends timestamp not null,
            hour_value float not null,
            prv float not null,
            eoy_bonus float not null
        );
    """
    )
    cur.execute(
        """
        create table tb_earning (
            id integer primary key autoincrement,
            "date" timestamp not null,
            value float not null
        )
    """
    )
    cur.execute(
        """
        create table tb_perhourpayment (
            id integer primary key autoincrement,
            contract_id int not null,
            paymenttable_id int not null,
            process_date timestamp not null,
            ref_month integer not null,
            ref_year integer not null,
            value float not null
        )
    """
    )
    cur.execute(
        """
        insert into tb_school (name, inep) values
        ('EEFM MARECHAL HUMBERTO DE ALENCAR CASTELO BRANCO', 23071095),
        ('EEFM ANÍSIO TEIXEIRA', 23065214),
        ('EEFM ARQUITETO ROGÉRIO FRÓES', 23077140),
        ('EEFM PARÓQUIA DA PAZ', 23068973),
        ('EEFM PATRONATO SAGRADA FAMÍLIA', 23075686),
        ('EEMTI SENADOR FERNANDES TÁVORA', 23069627),
        ('EEM DEPUTADO FRANCISCO DE ALMEIDA MONTE', 23069961)
    """
    )
    cur.execute(
        """
        insert into tb_contract
        (school_id, contract_id, starts, ends, hours) values
        (1, '22200180950012', '2022-04-01 00:00:00.000001','2022-05-13 00:00:00.000001', 5),
        (2, '22200180950012', '2022-04-05 00:00:00.000001', '2023-01-13 00:00:00.000001', 4),
        (2, '22200180950004', '2022-04-05 00:00:00.000001', '2023-01-13 00:00:00.000001', 6),
        (2, '22200180949995', '2022-04-05 00:00:00.000001', '2022-09-12 00:00:00.000001', 2),
        (3, '22200180507011', '2021-10-30 00:00:00.000001', '2022-01-14 00:00:00.000001', 4),
        (4, '22200180506414', '2020-03-27 00:00:00.000001', '2020-05-20 00:00:00.000001', 14),
        (4, '22200180506414', '2020-02-21 00:00:00.000001', '2020-03-26 00:00:00.000001', 17),
        (4, '22200180506414', '2020-02-04 00:00:00.000001', '2020-02-20 00:00:00.000001', 17),
        (3, '22200180499914', '2021-10-30 00:00:00.000001', '2022-01-14 00:00:00.000001', 3),
        (3, '22200180499914', '2021-06-01 00:00:00.000001', '2021-10-29 00:00:00.000001', 3),
        (3, '22200180499914', '2021-01-16 00:00:00.000001', '2021-05-31 00:00:00.000001', 3),
        (3, '22200180499914', '2020-02-03 00:00:00.000001', '2021-01-15 00:00:00.000001', 3),
        (4, '22200180353316', '2020-02-04 00:00:00.000001', '2020-02-20 00:00:00.000001', 11),
        (4, '22200181067929', '2022-05-25 00:00:00.000001', '2023-01-13 00:00:00.000001', 12)
    """
    )
    cur.execute(
        """
        insert into tb_paymenttable(starts, ends, hour_value, prv, eoy_bonus) values
        ('2022-05-01 00:00:00.000001', '2022-10-31 00:00:00.000001', 19.228, 1.794, 0),
        ('2022-01-01 00:00:00.000001', '2022-04-30 00:00:00.000001', 19.228, 0, 0),
        ('2020-01-01 00:00:00.000001', '2021-12-31 00:00:00.000001', 14.432, 0, 0);
    """
    )
    cur.execute(
        """
        insert into tb_earning(date, value) values
        ('2022-01-03 00:00:00.000001', 74.04),
        ('2022-01-03 00:00:00.000001', 222.12),
        ('2022-01-03 00:00:00.000001', 518.28),
        ('2022-01-03 00:00:00.000001', 681.52),
        ('2022-01-14 00:00:00.000001', 99.74),
        ('2022-01-14 00:00:00.000001', 111.96),
        ('2022-01-14 00:00:00.000001', 335.86),
        ('2022-01-14 00:00:00.000001', 776.06),
        ('2022-02-01 00:00:00.000001', 35.32),
        ('2022-02-01 00:00:00.000001', 105.98),
        ('2022-02-01 00:00:00.000001', 211.96),
        ('2022-02-01 00:00:00.000001', 211.29),
        ('2022-03-02 00:00:00.000001', 75.95),
        ('2022-03-02 00:00:00.000001', 759.42),
        ('2022-03-02 00:00:00.000001', 2278.22),
        ('2022-04-01 00:00:00.000001', 97.07),
        ('2022-04-01 00:00:00.000001', 970.82),
        ('2022-04-01 00:00:00.000001', 2145.78),
        ('2022-05-02 00:00:00.000001', 88.49),
        ('2022-05-02 00:00:00.000001', 619.49),
        ('2022-05-02 00:00:00.000001', 826.19),
        ('2022-05-02 00:00:00.000001', 884.98),
        ('2022-06-01 00:00:00.000001', 53.56),
        ('2022-06-01 00:00:00.000001', 287.87),
        ('2022-06-01 00:00:00.000001', 604.28),
        ('2022-06-01 00:00:00.000001', 852.62),
        ('2022-06-01 00:00:00.000001', 863.27),
        ('2022-06-01 00:00:00.000001', 1276.22),
        ('2022-07-01 00:00:00.000001', 51.87),
        ('2022-07-01 00:00:00.000001', 194.16),
        ('2022-07-01 00:00:00.000001', 457.22),
        ('2022-07-01 00:00:00.000001', 582.48),
        ('2022-07-01 00:00:00.000001', 616.99),
        ('2022-07-01 00:00:00.000001', 1922.02);
    """
    )
    cur.execute(
        """
        insert into tb_perhourpayment(
                contract_id,
                paymenttable_id,
                process_date,
                ref_month,
                ref_year,
                value
        ) values
        (1, 1, '2022-02-01 00:00:00.00001', 1, 2022, 2000.00),
        (1, 2, '2022-03-01 00:00:00.00001', 2, 2022, 2500.00),
        (1, 3, '2022-04-01 00:00:00.00001', 3, 2022, 3500.00);
    """
    )

    yield conn


@fixture
def objs(database):
    """Fixture that creates dummy Model and ModelCreator objects for tests to
    interact with"""
    conn = database
    objects_names = """
        conn
        school
        contract
        ptable
        earning
        perhourpayment
    """
    school = School(name="Rogério Fróes", inep=3934039)
    contract = Contract(
        school_id=1,
        contract_id=1,
        starts=datetime(2022, 1, 1, 0, 0, 0, 1),
        ends=datetime(2022, 3, 1, 0, 0, 0, 1),
        hours=10,
    )
    ptable = PaymentTable(
        starts=datetime(2022, 1, 1, 0, 0, 0, 1),
        ends=datetime(2022, 2, 1, 0, 0, 0, 1),
        hour_value=Decimal(2.4),
        prv=Decimal(1.2),
        eoy_bonus=Decimal(4.2),
    )
    earning = Earning(
        date=datetime(2022, 1, 1, 0, 0, 0, 1), value=Decimal("3.999999999999")
    )
    perhourpayment = PerHourPayment(
        contract_id=1,
        paymenttable_id=1,
        ref_month=3,
        ref_year=2022,
        process_date=datetime(2022, 1, 1, 0, 0, 0, 1),
        value=Decimal("1094.99"),
    )
    Objects = namedtuple("Objects", objects_names)
    objects = Objects(
        conn,
        school,
        contract,
        ptable,
        earning,
        perhourpayment,
    )

    yield objects


@fixture(scope="module")
def main_controller():
    """Fixture that contains a MainController object for tests"""
    controller = MainController(
        contract_creator=FACTORIES["contract"](),
        ptable_creator=FACTORIES["paymenttable"],
        processor=PerHourProcessor,
    )

    yield controller
