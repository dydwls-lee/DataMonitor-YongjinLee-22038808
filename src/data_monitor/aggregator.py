"""전체 요약 집계.

data-monitor 자체 요약(PRD.md 기능 요구사항 1)은 관리자가 데이터 저장소의
있는 그대로의 상태를 점검하기 위한 것이므로, 통합 저장소 메인 시스템
console-mvc의 "모니터링" 메뉴와 달리 REJECTED도 상태별 건수에 포함한다.
이는 결정된 사항이다 (근거: 통합 저장소 docs/DECISIONS.md,
docs/SCHEMA.md §3).
"""

from __future__ import annotations

from dataclasses import dataclass

from data_monitor.models import Order, Sample

ORDER_STATUSES: tuple[str, ...] = (
    "RESERVED",
    "REJECTED",
    "PRODUCING",
    "CONFIRMED",
    "RELEASE",
)


@dataclass(frozen=True)
class Summary:
    sample_count: int
    total_order_count: int
    status_counts: dict[str, int]


def summarize(samples: list[Sample], orders: list[Order]) -> Summary:
    status_counts = {status: 0 for status in ORDER_STATUSES}
    for order in orders:
        if order.status in status_counts:
            status_counts[order.status] += 1

    return Summary(
        sample_count=len(samples),
        total_order_count=len(orders),
        status_counts=status_counts,
    )


def filter_orders_by_status(orders: list[Order], status: str | None) -> list[Order]:
    """status가 None이면 전체 주문을, 아니면 해당 상태만 반환한다."""
    if status is None:
        return list(orders)
    return [order for order in orders if order.status == status]


PLENTY_LABEL = "여유"
SHORTAGE_LABEL = "부족"
DEPLETED_LABEL = "고갈"


@dataclass
class StockThresholds:
    """재고 상태(여유/부족/고갈) 분류에 쓰이는 절대 수량 기준 임계값.

    console-mvc의 모니터링 메뉴는 주문 수요 대비 상대값으로 분류하지만,
    이 도구는 절대 재고 수량 기준 2단계 임계값으로 판정한다
    (근거: 통합 저장소 docs/DECISIONS.md
    "data-monitor에 재고 여유/부족/고갈 분류 추가 여부").

    콘솔 메뉴에서 실행 중 값을 바꿀 수 있도록 불변(frozen)이 아니다.
    """

    plenty_threshold: int = 1000
    shortage_threshold: int = 300


def classify_stock(stock: int, thresholds: StockThresholds) -> str:
    """재고 수량을 여유/부족/고갈 3단계로 분류한다.

    경계값 처리: plenty_threshold 이상 -> 여유,
    shortage_threshold 이상 plenty_threshold 미만 -> 부족,
    shortage_threshold 미만(0 포함) -> 고갈.
    """
    if stock >= thresholds.plenty_threshold:
        return PLENTY_LABEL
    if stock >= thresholds.shortage_threshold:
        return SHORTAGE_LABEL
    return DEPLETED_LABEL
