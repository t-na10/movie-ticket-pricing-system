# READMEの概念クラス図に従い、クラスを定義するモジュール

from datetime import datetime
from typing import Callable, List, Optional

from pydantic import BaseModel


class Condition(BaseModel):
    description: str
    check: Callable[[datetime, int], bool]


class MovieSession(BaseModel):
    showDateTime: datetime
    availableSeats: int


class PricePolicy(BaseModel):
    policyName: str
    policyPrice: int
    policyConditions: List[Condition]


class Viewer(BaseModel):
    age: int


class TicketRequest(BaseModel):
    currentDateTime: datetime
    viewers: List[Viewer]


class TicketResponse(BaseModel):
    sessionDateTime: datetime
    totalPrice: int
    remainingSeats: int
    message: Optional[str] = None
