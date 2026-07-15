from data_monitor.models import Order, Sample


def test_sample_from_dict_maps_schema_fields():
    raw = {
        "id": "S-001",
        "name": "실리콘 웨이퍼-8인치",
        "avgProductionTime": 0.5,
        "yield": 0.92,
        "stock": 480,
    }

    sample = Sample.from_dict(raw)

    assert sample.id == "S-001"
    assert sample.name == "실리콘 웨이퍼-8인치"
    assert sample.avg_production_time == 0.5
    assert sample.yield_rate == 0.92
    assert sample.stock == 480


def test_order_from_dict_maps_schema_fields():
    raw = {
        "orderId": "ORD-20260416-0043",
        "sampleId": "S-003",
        "customerName": "삼성전자 파운드리",
        "quantity": 200,
        "status": "RESERVED",
        "createdAt": "2026-04-16T09:32:15",
    }

    order = Order.from_dict(raw)

    assert order.order_id == "ORD-20260416-0043"
    assert order.sample_id == "S-003"
    assert order.customer_name == "삼성전자 파운드리"
    assert order.quantity == 200
    assert order.status == "RESERVED"
    assert order.created_at == "2026-04-16T09:32:15"
