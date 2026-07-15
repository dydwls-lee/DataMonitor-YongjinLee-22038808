from data_monitor.aggregator import StockThresholds, summarize
from data_monitor.models import Order, Sample
from data_monitor.rendering import (
    render_orders_table,
    render_samples_table,
    render_summary,
)

SAMPLES = [
    Sample(id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=0.5, yield_rate=0.92, stock=480),
    Sample(id="S-002", name="실리콘 웨이퍼-12인치", avg_production_time=0.8, yield_rate=0.85, stock=0),
]

ORDERS = [
    Order("ORD-20260416-0043", "S-001", "삼성전자 파운드리", 200, "RESERVED", "2026-04-16T09:32:15"),
    Order("ORD-20260416-0044", "S-002", "SK하이닉스", 50, "REJECTED", "2026-04-16T10:00:00"),
]


def test_render_summary_includes_sample_and_order_counts():
    summary = summarize(SAMPLES, ORDERS)

    text = render_summary(summary)

    assert "등록 시료 수: 2" in text
    assert "전체 주문 수: 2" in text
    assert "RESERVED" in text and "1" in text
    assert "REJECTED" in text


def test_render_samples_table_lists_every_sample_with_stock():
    text = render_samples_table(SAMPLES, StockThresholds())

    assert "S-001" in text
    assert "실리콘 웨이퍼-8인치" in text
    assert "480" in text
    assert "S-002" in text
    assert "0" in text


def test_render_samples_table_shows_stock_classification_with_default_thresholds():
    # S-001 stock=480 -> 부족(300<=480<1000), S-002 stock=0 -> 고갈
    text = render_samples_table(SAMPLES, StockThresholds())

    lines = text.splitlines()
    s001_line = next(line for line in lines if "S-001" in line)
    s002_line = next(line for line in lines if "S-002" in line)

    assert "부족" in s001_line
    assert "고갈" in s002_line


def test_render_samples_table_reflects_custom_thresholds():
    # 커스텀 임계값: plenty=500 이상 여유, S-001 stock=480은 그대로 부족 유지되지만
    # shortage=500으로 올리면 부족 -> 고갈로 바뀐다.
    thresholds = StockThresholds(plenty_threshold=1000, shortage_threshold=500)

    text = render_samples_table(SAMPLES, thresholds)

    lines = text.splitlines()
    s001_line = next(line for line in lines if "S-001" in line)

    assert "고갈" in s001_line


def test_render_samples_table_handles_empty_list():
    text = render_samples_table([], StockThresholds())

    assert "없습니다" in text


def test_render_orders_table_lists_every_order():
    text = render_orders_table(ORDERS)

    assert "ORD-20260416-0043" in text
    assert "RESERVED" in text
    assert "ORD-20260416-0044" in text
    assert "REJECTED" in text


def test_render_orders_table_handles_empty_list():
    text = render_orders_table([])

    assert "없습니다" in text
