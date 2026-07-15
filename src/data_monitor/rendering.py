"""콘솔 출력용 순수 렌더링 함수.

I/O(입력 대기, print)는 cli.py에서 담당하고, 여기서는 문자열만 만든다.
"""

from __future__ import annotations

from data_monitor.aggregator import ORDER_STATUSES, StockThresholds, Summary, classify_stock
from data_monitor.models import Order, Sample

_EMPTY_SAMPLES_MESSAGE = "등록된 시료가 없습니다."
_EMPTY_ORDERS_MESSAGE = "표시할 주문이 없습니다."


def render_summary(summary: Summary) -> str:
    lines = [
        "=== 전체 요약 ===",
        f"등록 시료 수: {summary.sample_count}",
        f"전체 주문 수: {summary.total_order_count}",
        "상태별 주문 건수:",
    ]
    for status in ORDER_STATUSES:
        lines.append(f"  {status:<10}: {summary.status_counts[status]}")
    return "\n".join(lines)


def render_samples_table(samples: list[Sample], thresholds: StockThresholds) -> str:
    """시료 목록을 표로 렌더링한다.

    ``thresholds``는 재고 상태(여유/부족/고갈) 분류에 쓰이는 절대 임계값으로,
    콘솔 메뉴에서 실행 중 변경할 수 있다 (docs/PRD.md 기능 요구사항 항목2).
    """
    if not samples:
        return _EMPTY_SAMPLES_MESSAGE

    header = (
        f"{'ID':<8} {'이름':<20} {'평균생산시간(min/ea)':>20} {'수율':>8} "
        f"{'재고':>8} {'재고상태':>8}"
    )
    lines = ["=== 시료 목록 ===", header, "-" * len(header)]
    for sample in samples:
        status = classify_stock(sample.stock, thresholds)
        lines.append(
            f"{sample.id:<8} {sample.name:<20} {sample.avg_production_time:>20} "
            f"{sample.yield_rate:>8} {sample.stock:>8} {status:>8}"
        )
    return "\n".join(lines)


def render_orders_table(orders: list[Order]) -> str:
    if not orders:
        return _EMPTY_ORDERS_MESSAGE

    header = (
        f"{'주문번호':<20} {'시료ID':<8} {'고객명':<16} {'수량':>6} "
        f"{'상태':<10} {'접수시각':<20}"
    )
    lines = ["=== 주문 목록 ===", header, "-" * len(header)]
    for order in orders:
        lines.append(
            f"{order.order_id:<20} {order.sample_id:<8} {order.customer_name:<16} "
            f"{order.quantity:>6} {order.status:<10} {order.created_at:<20}"
        )
    return "\n".join(lines)
