# このモジュールは、チケットリクエストを処理するためのロジックを提供する。
# database.pyで定義されたmovie_sessionsとprice_policiesに依存している。

from datetime import datetime
from typing import List

from src.database import movie_sessions, price_policies
from src.models import MovieSession, TicketRequest, TicketResponse, Viewer


def calculate_ticket_price(session: MovieSession, viewers: List[Viewer]) -> int:
    total_price = 0
    for viewer in viewers:
        # 各観客に適用可能な最安値のポリシーを探す
        applicable_prices = [
            policy.policyPrice
            for policy in price_policies
            if all(condition.check(session.showDateTime, viewer.age) for condition in policy.policyConditions)
        ]

        if applicable_prices:
            # 適用可能な最安値のポリシーを使用
            price = min(applicable_prices)
        else:
            # 適用可能なポリシーがなければ一般料金を使用
            price = [policy.policyPrice for policy in price_policies if policy.policyName == "General"][0]
        total_price += price

    return total_price


def process_ticket_request(ticket_request: TicketRequest) -> TicketResponse:
    # 未成年がリクエストに含まれるか確認
    has_minors = any(viewer.age < 18 for viewer in ticket_request.viewers)

    # 選択可能なセッションをフィルタリング
    possible_sessions = [
        session
        for session in movie_sessions
        if session.showDateTime >= ticket_request.currentDateTime
        and session.availableSeats >= len(ticket_request.viewers)
        and not (has_minors and session.showDateTime.hour >= 20)  # 未成年者の入場制限を考慮
    ]

    # 各セッションに対して料金を計算し、最安値のセッションを見つける
    best_session = None
    best_price = float("inf")
    for session in possible_sessions:
        price = calculate_ticket_price(session, ticket_request.viewers)
        if price < best_price:
            best_price = price
            best_session = session

    if not best_session:
        # 適当なセッションが見つからない場合
        return TicketResponse(
            sessionDateTime=datetime.min,
            totalPrice=0,
            remainingSeats=0,
            message="No available movie sessions.",
        )

    # 最適なセッションと料金を返す
    return TicketResponse(
        sessionDateTime=best_session.showDateTime,
        totalPrice=best_price,
        remainingSeats=best_session.availableSeats - len(ticket_request.viewers),
        message="",
    )
