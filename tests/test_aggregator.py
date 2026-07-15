from data_monitor.aggregator import ORDER_STATUSES, summarize
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
