# データベースの代わりにインメモリデータストアとしての役割を持つモジュール
# 映画の上映スケジュールと料金ポリシーを提供する

from datetime import datetime

from src.models import Condition, MovieSession, PricePolicy

# 映画の上映スケジュール
movie_sessions = [
    MovieSession(showDateTime=datetime(2023, 11, 30, 15, 0), availableSeats=4),
    MovieSession(showDateTime=datetime(2023, 11, 30, 20, 0), availableSeats=6),
    MovieSession(showDateTime=datetime(2023, 12, 1, 15, 0), availableSeats=1),
    MovieSession(showDateTime=datetime(2023, 12, 1, 20, 0), availableSeats=2),
    MovieSession(showDateTime=datetime(2023, 12, 2, 15, 0), availableSeats=4),
    MovieSession(showDateTime=datetime(2023, 12, 2, 20, 0), availableSeats=5),
]


# 条件判定の関数
def is_minor(session_date: datetime, viewer_age: int) -> bool:
    return viewer_age < 18


def is_first_day_of_month(session_date: datetime, viewer_age: int) -> bool:
    return session_date.day == 1


def is_after_20(session_date: datetime, viewer_age: int) -> bool:
    return session_date.hour >= 20


def is_senior_weekday(session_date: datetime, viewer_age: int) -> bool:
    return session_date.weekday() < 5 and viewer_age >= 60


# Conditionオブジェクトの作成
conditions = [
    Condition(description="Minor", check=is_minor),
    Condition(description="First Day of Month", check=is_first_day_of_month),
    Condition(description="After 20", check=is_after_20),
    Condition(description="Senior Weekday", check=is_senior_weekday),
]


# 料金ポリシー
price_policies = [
    PricePolicy(policyName="General", policyPrice=1600, policyConditions=[]),
    PricePolicy(policyName="Minor", policyPrice=1000, policyConditions=[conditions[0]]),
    PricePolicy(
        policyName="First Day Discount",
        policyPrice=1000,
        policyConditions=[conditions[1]],
    ),
    PricePolicy(
        policyName="Late Show Discount",
        policyPrice=1400,
        policyConditions=[conditions[2]],
    ),
    PricePolicy(
        policyName="Senior Weekday Discount",
        policyPrice=1200,
        policyConditions=[conditions[3]],
    ),
]
