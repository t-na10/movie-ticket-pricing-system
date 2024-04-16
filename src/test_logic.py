# logic.py のテストを行うためのファイルである。
# pytest test_logic.py を実行すると、test_logic.py内に記述されたテストが実行される。
from datetime import datetime

import pytest

from src.logic import process_ticket_request
from src.models import TicketRequest, Viewer


# テストケース(1) - ファーストデイ割引
def test_first_day_discount():
    request_datetime = datetime(2023, 11, 30, 14, 0)
    viewers = [Viewer(age=25)]
    ticket_request = TicketRequest(currentDateTime=request_datetime, viewers=viewers)
    expected_price = 1000
    expected_datetime = datetime(2023, 12, 1, 15, 0)
    response = process_ticket_request(ticket_request)
    assert (
        response.totalPrice == expected_price
    ), f"Expected total price to be {expected_price}, but got {response.totalPrice}."
    assert (
        response.sessionDateTime == expected_datetime
    ), f"Expected session datetime to be {expected_datetime}, but got {response.sessionDateTime}."


# テストケース(2) - ファーストデイ割引(複数人)
def test_first_day_discount_2():
    request_datetime = datetime(2023, 11, 30, 14, 0)
    viewers = [Viewer(age=25), Viewer(age=22)]
    ticket_request = TicketRequest(currentDateTime=request_datetime, viewers=viewers)
    expected_price = 1000 * 2
    expected_datetime = datetime(2023, 12, 1, 20, 0)
    response = process_ticket_request(ticket_request)
    assert (
        response.totalPrice == expected_price
    ), f"Expected total price to be {expected_price}, but got {response.totalPrice}."
    assert (
        response.sessionDateTime == expected_datetime
    ), f"Expected session datetime to be {expected_datetime}, but got {response.sessionDateTime}."


# テストケース(3) - レイトショー割引
def test_late_show_discount():
    request_datetime = datetime(2023, 12, 2, 12, 0)
    viewers = [Viewer(age=25)]
    ticket_request = TicketRequest(currentDateTime=request_datetime, viewers=viewers)
    expected_price = 1400
    expected_datetime = datetime(2023, 12, 2, 20, 0)
    response = process_ticket_request(ticket_request)
    assert (
        response.totalPrice == expected_price
    ), f"Expected total price to be {expected_price}, but got {response.totalPrice}."
    assert (
        response.sessionDateTime == expected_datetime
    ), f"Expected session datetime to be {expected_datetime}, but got {response.sessionDateTime}."


# テストケース(4) - 平日シニア割引
def test_weekday_senior_discount():
    request_datetime = datetime(2023, 11, 30, 11, 0)  # 平日
    viewers = [Viewer(age=65), Viewer(age=60), Viewer(age=62)]
    ticket_request = TicketRequest(currentDateTime=request_datetime, viewers=viewers)
    expected_price = 1200 * 3
    expected_datetime = datetime(2023, 11, 30, 15, 0)
    response = process_ticket_request(ticket_request)
    assert (
        response.totalPrice == expected_price
    ), f"Expected total price to be {expected_price}, but got {response.totalPrice}."
    assert (
        response.sessionDateTime == expected_datetime
    ), f"Expected session datetime to be {expected_datetime}, but got {response.sessionDateTime}."


# テストケース(5) - 未成年の20時以降入場不可
def test_no_entry_for_minors_after_20():
    request_datetime = datetime(2023, 11, 30, 19, 0)
    viewers = [Viewer(age=17)]
    ticket_request = TicketRequest(currentDateTime=request_datetime, viewers=viewers)
    expected_price = 1000
    expected_datetime = datetime(2023, 12, 1, 15, 0)
    response = process_ticket_request(ticket_request)
    # 20時以降のセッションが選ばれないので、利用可能なセッションがないというメッセージが返される
    assert (
        response.totalPrice == expected_price
    ), f"Expected total price to be {expected_price}, but got {response.totalPrice}."
    assert (
        response.sessionDateTime == expected_datetime
    ), f"Expected session datetime to be {expected_datetime}, but got {response.sessionDateTime}."


# テストケース(6) - 最安値になる日時が複数存在する場合
def test_earliest_session_for_best_price():
    request_datetime = datetime(2023, 11, 29, 12, 0)  # テストリクエスト日時
    viewers = [Viewer(age=30)]
    ticket_request = TicketRequest(currentDateTime=request_datetime, viewers=viewers)
    excepted_price = 1000
    excepted_datetime = datetime(2023, 12, 1, 15, 0)
    response = process_ticket_request(ticket_request)
    # 最初の利用可能なセッションが選ばれる
    assert (
        response.totalPrice == excepted_price
    ), f"Expected total price to be {excepted_price}, but got {response.totalPrice}."
    assert (
        response.sessionDateTime == excepted_datetime
    ), f"Expected session datetime to be {excepted_datetime}, but got {response.sessionDateTime}."


# テストケース(7) - 適当な日時が存在しない場合
def test_no_suitable_session():
    request_datetime = datetime(2023, 12, 3, 10, 0)  # 上映スケジュール外
    viewers = [Viewer(age=25)]
    ticket_request = TicketRequest(currentDateTime=request_datetime, viewers=viewers)

    response = process_ticket_request(ticket_request)
    assert (
        response.message == "No available movie sessions."
    ), "Expected no available sessions message, but got a different response."
