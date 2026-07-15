import json

import pytest

from data_monitor.repository import ReadOnlyJsonRepository

FIXTURES_DIR = "tests/fixtures"


def test_list_samples_reads_from_samples_json():
    repo = ReadOnlyJsonRepository(FIXTURES_DIR)

    samples = repo.list_samples()

    assert [s.id for s in samples] == ["S-001", "S-002"]
    assert samples[0].stock == 480


def test_list_orders_reads_from_orders_json():
    repo = ReadOnlyJsonRepository(FIXTURES_DIR)

    orders = repo.list_orders()

    assert len(orders) == 5
    assert orders[0].order_id == "ORD-20260416-0043"


def test_missing_files_are_treated_as_empty_arrays(tmp_path):
    repo = ReadOnlyJsonRepository(str(tmp_path))

    assert repo.list_samples() == []
    assert repo.list_orders() == []


def test_reload_picks_up_changes_made_after_initial_load(tmp_path):
    samples_path = tmp_path / "samples.json"
    orders_path = tmp_path / "orders.json"
    samples_path.write_text("[]", encoding="utf-8")
    orders_path.write_text("[]", encoding="utf-8")

    repo = ReadOnlyJsonRepository(str(tmp_path))
    assert repo.list_samples() == []

    samples_path.write_text(
        json.dumps(
            [
                {
                    "id": "S-999",
                    "name": "신규 시료",
                    "avgProductionTime": 1.0,
                    "yield": 1.0,
                    "stock": 10,
                }
            ]
        ),
        encoding="utf-8",
    )

    # 명시적으로 reload()를 호출하기 전에는 이전 스냅샷을 유지한다.
    assert repo.list_samples() == []

    repo.reload()

    assert [s.id for s in repo.list_samples()] == ["S-999"]


def test_repository_has_no_write_methods():
    repo = ReadOnlyJsonRepository(FIXTURES_DIR)

    for forbidden in ("save", "write", "add_sample", "add_order", "delete", "update"):
        assert not hasattr(repo, forbidden)


def test_repository_never_modifies_source_files(tmp_path):
    samples_path = tmp_path / "samples.json"
    orders_path = tmp_path / "orders.json"
    original_samples = "[]"
    original_orders = "[]"
    samples_path.write_text(original_samples, encoding="utf-8")
    orders_path.write_text(original_orders, encoding="utf-8")

    repo = ReadOnlyJsonRepository(str(tmp_path))
    repo.list_samples()
    repo.list_orders()
    repo.reload()
    repo.list_samples()

    assert samples_path.read_text(encoding="utf-8") == original_samples
    assert orders_path.read_text(encoding="utf-8") == original_orders
