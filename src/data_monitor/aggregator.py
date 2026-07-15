"""전체 요약 집계.

data-monitor 자체 요약(PRD 기능 요구사항 1)은 관리자가 데이터 저장소의
있는 그대로의 상태를 점검하기 위한 것이므로, 통합 저장소 메인 시스템의
"모니터링" 메뉴와 달리 REJECTED도 상태별 건수에 포함한다
(SCHEMA.md §3, docs/HARNESS.md 참고).
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
