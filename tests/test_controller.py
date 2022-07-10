"""Module for testing controller.py methods"""


from models import Contract
from controller import MainController


def test_controller_instantiation(main_controller):
    """Assert if a Controller instance can be instatiated with given expected
    arguments"""
    assert isinstance(main_controller, MainController)


def test_controller_unprocessed_before_call_is_list(main_controller):
    """Assert if unprocessed attribute before call is a empty list"""
    assert isinstance(main_controller.unprocessed, list)


def test_controller_unprocessed_before_call_len_zero(main_controller):
    """Assert if unprocessed attribute before call lenght is zero"""
    assert len(main_controller.unprocessed) == 0


def test_controller_payments_before_call_is_list(main_controller):
    """Assert if payments attribute before call is a empty list"""
    assert isinstance(main_controller.payments, list)


def test_controller_payments_before_call_len_zero(main_controller):
    """Assert if payments attribute before call lenght is zero"""
    assert len(main_controller.payments) == 0


def test_controller_get_non_processed_contracts_len_gt_zero(main_controller, database):
    """Assert if given method updates unprocessed list"""
    # breakpoint()
    main_controller.get_non_processed_contracts()
    assert len(main_controller.unprocessed) > 0


def test_controller_get_non_processed_contracts_list_models(main_controller, database):
    """Assert if unprocessed contracts are Contract instances"""
    main_controller.get_non_processed_contracts()
    check = True
    for contract in main_controller.unprocessed:
        if not isinstance(contract, Contract):
            check = False
    assert check
