"""Sample/Order 데이터 모델.

필드 정의의 단일 소스는 통합 저장소 ``docs/SCHEMA.md`` 이다. 여기서는 해당 스키마를
읽기 전용으로 파싱하기 위한 값 객체만 정의한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Sample:
    id: str
    name: str
    avg_production_time: float
    yield_rate: float
    stock: int

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Sample":
        return cls(
            id=raw["id"],
            name=raw["name"],
            avg_production_time=raw["avgProductionTime"],
            yield_rate=raw["yield"],
            stock=raw["stock"],
        )


@dataclass(frozen=True)
class Order:
    order_id: str
    sample_id: str
    customer_name: str
    quantity: int
    status: str
    created_at: str

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Order":
        return cls(
            order_id=raw["orderId"],
            sample_id=raw["sampleId"],
            customer_name=raw["customerName"],
            quantity=raw["quantity"],
            status=raw["status"],
            created_at=raw["createdAt"],
        )
