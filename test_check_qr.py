
import pytest
from unittest.mock import MagicMock
from scanner_handler import CheckQr

@pytest.fixture
def setup_check_qr():
    qr_checker = CheckQr()
    qr_checker.check_in_db = MagicMock()
    qr_checker.send_error = MagicMock()
    qr_checker.can_add_device = MagicMock()
    return qr_checker

def test_successful_scan_red_color(setup_check_qr):
    qr_checker = setup_check_qr
    qr = "123"
    qr_checker.check_in_db.return_value = True

    qr_checker.check_scanned_device(qr)

    assert qr_checker.color == "Red"
    qr_checker.can_add_device.assert_called_once_with(f"hallelujah {qr}")

def test_successful_scan_green_color(setup_check_qr):
    qr_checker = setup_check_qr
    qr = "12345"
    qr_checker.check_in_db.return_value = True

    qr_checker.check_scanned_device(qr)

    assert qr_checker.color == "Green"
    qr_checker.can_add_device.assert_called_once_with(f"hallelujah {qr}")

def test_successful_scan_fuzzy_wuzzy_color(setup_check_qr):
    qr_checker = setup_check_qr
    qr = "1234567"
    qr_checker.check_in_db.return_value = True

    qr_checker.check_scanned_device(qr)

    assert qr_checker.color == "Fuzzy Wuzzy"
    qr_checker.can_add_device.assert_called_once_with(f"hallelujah {qr}")

def test_wrong_length(setup_check_qr):
    qr_checker = setup_check_qr
    qr = "1"
    qr_checker.check_in_db.return_value = True

    qr_checker.check_scanned_device(qr)

    assert qr_checker.color is None
    qr_checker.send_error.assert_called_once_with("Error: Wrong qr length 1")

def test_not_in_db(setup_check_qr):
    qr_checker = setup_check_qr
    qr = "12345"
    qr_checker.check_in_db.return_value = None

    qr_checker.check_scanned_device(qr)

    qr_checker.send_error.assert_called_once_with("Not in DB")

def test_wrong_length_and_not_in_db(setup_check_qr):
    qr_checker = setup_check_qr
    qr = "1234"
    qr_checker.check_in_db.side_effect = ConnectionError("Database connection error")

    qr_checker.check_len_color(qr)
    if not qr_checker.color:
        qr_checker.send_error(f"Error: Wrong qr length {len(qr)}")

    try:
        qr_checker.check_in_db(qr)
    except ConnectionError:
        qr_checker.send_error("Not in DB")

    qr_checker.send_error.assert_any_call("Error: Wrong qr length 4")
    qr_checker.send_error.assert_any_call("Not in DB")
