from data_monitor.aggregator import (
    ORDER_STATUSES,
    StockThresholds,
    classify_stock,
    filter_orders_by_status,
    summarize,
)
from data_monitor.models import Order, Sample

SAMPLES = [
    Sample(id="S-001", name="A", avg_production_time=0.5, yield_rate=0.9, stock=100),
    Sample(id="S-002", name="B", avg_production_time=0.8, yield_rate=0.85, stock=0),
]

ORDERS = [
    Order("ORD-1", "S-001", "고객1", 10, "RESERVED", "2026-01-01T00:00:00"),
    Order("ORD-2", "S-002", "고객2", 5, "REJECTED", "2026-01-01T00:00:00"),
    Order("ORD-3", "S-002", "고객3", 5, "PRODUCING", "2026-01-01T00:00:00"),
    Order("ORD-4", "S-001", "고객4", 5, "CONFIRMED", "2026-01-01T00:00:00"),
    Order("ORD-5", "S-001", "고객5", 5, "CONFIRMED", "2026-01-01T00:00:00"),
    Order("ORD-6", "S-001", "고객6", 5, "RELEASE", "2026-01-01T00:00:00"),
]


def test_order_statuses_defines_all_five_in_domain_order():
    assert ORDER_STATUSES == ("RESERVED", "REJECTED", "PRODUCING", "CONFIRMED", "RELEASE")


def test_summarize_counts_samples_and_total_orders():
    summary = summarize(SAMPLES, ORDERS)

    assert summary.sample_count == 2
    assert summary.total_order_count == 6


def test_summarize_counts_orders_per_status_including_rejected():
    summary = summarize(SAMPLES, ORDERS)

    assert summary.status_counts == {
        "RESERVED": 1,
        "REJECTED": 1,
        "PRODUCING": 1,
        "CONFIRMED": 2,
        "RELEASE": 1,
    }


def test_summarize_reports_zero_for_statuses_with_no_orders():
    summary = summarize(SAMPLES, [])

    assert summary.total_order_count == 0
    assert summary.status_counts == {
        "RESERVED": 0,
        "REJECTED": 0,
        "PRODUCING": 0,
        "CONFIRMED": 0,
        "RELEASE": 0,
    }


def test_filter_orders_by_status_returns_only_matching_orders():
    confirmed = filter_orders_by_status(ORDERS, "CONFIRMED")

    assert [o.order_id for o in confirmed] == ["ORD-4", "ORD-5"]


def test_filter_orders_by_status_returns_empty_when_none_match():
    releases = filter_orders_by_status([], "RELEASE")

    assert releases == []


def test_filter_orders_by_status_none_returns_all_orders():
    assert filter_orders_by_status(ORDERS, None) == ORDERS


def test_stock_thresholds_default_values():
    thresholds = StockThresholds()

    assert thresholds.plenty_threshold == 1000
    assert thresholds.shortage_threshold == 300


def test_classify_stock_plenty_when_at_or_above_plenty_threshold():
    thresholds = StockThresholds()

    assert classify_stock(1000, thresholds) == "여유"
    assert classify_stock(5000, thresholds) == "여유"


def test_classify_stock_shortage_when_between_shortage_and_plenty_threshold():
    thresholds = StockThresholds()

    assert classify_stock(300, thresholds) == "부족"
    assert classify_stock(999, thresholds) == "부족"


def test_classify_stock_depleted_when_below_shortage_threshold_including_zero():
    thresholds = StockThresholds()

    assert classify_stock(299, thresholds) == "고갈"
    assert classify_stock(0, thresholds) == "고갈"


def test_classify_stock_uses_custom_thresholds():
    thresholds = StockThresholds(plenty_threshold=100, shortage_threshold=10)

    assert classify_stock(100, thresholds) == "여유"
    assert classify_stock(10, thresholds) == "부족"
    assert classify_stock(9, thresholds) == "고갈"
