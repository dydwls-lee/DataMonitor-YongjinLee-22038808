from data_monitor.cli import run
from data_monitor.models import Order, Sample
from data_monitor.repository import ReadOnlyJsonRepository


class FakeRepository:
    """reload 호출 여부를 관찰하기 위한 테스트 더블. 쓰기 메서드는 없다."""

    def __init__(self, samples, orders):
        self._samples = samples
        self._orders = orders
        self.reload_call_count = 0

    def list_samples(self):
        return list(self._samples)

    def list_orders(self):
        return list(self._orders)

    def reload(self):
        self.reload_call_count += 1


def make_input(responses):
    it = iter(responses)
    return lambda _prompt="": next(it)


def run_cli(repository, responses):
    outputs = []
    run(repository, read_input=make_input(responses), write_output=outputs.append)
    return "\n".join(outputs)


SAMPLES = [Sample("S-001", "웨이퍼", 0.5, 0.9, 100)]
ORDERS = [
    Order("ORD-1", "S-001", "고객1", 10, "RESERVED", "2026-01-01T00:00:00"),
    Order("ORD-2", "S-001", "고객2", 5, "CONFIRMED", "2026-01-01T00:00:00"),
]


def test_menu_choice_summary_then_exit():
    repo = FakeRepository(SAMPLES, ORDERS)

    text = run_cli(repo, ["1", "6"])

    assert "등록 시료 수: 1" in text
    assert "전체 주문 수: 2" in text


def test_menu_choice_sample_list_then_exit():
    repo = FakeRepository(SAMPLES, ORDERS)

    text = run_cli(repo, ["2", "6"])

    assert "S-001" in text
    assert "웨이퍼" in text


def test_menu_choice_sample_list_shows_default_stock_classification():
    repo = FakeRepository(SAMPLES, ORDERS)

    text = run_cli(repo, ["2", "6"])

    # stock=100 -> shortage_threshold(300) 미만이므로 기본 임계값으로는 고갈
    assert "고갈" in text


def test_menu_choice_view_thresholds_shows_current_default_values():
    repo = FakeRepository(SAMPLES, ORDERS)

    text = run_cli(repo, ["5", "", "", "6"])

    assert "1000" in text
    assert "300" in text


def test_menu_choice_change_thresholds_updates_subsequent_sample_list_view():
    repo = FakeRepository(SAMPLES, ORDERS)

    # plenty_threshold=50, shortage_threshold=10으로 변경하면 stock=100인 S-001은 여유가 된다.
    text = run_cli(repo, ["5", "50", "10", "2", "6"])

    lines = text.splitlines()
    s001_line = next(line for line in lines if "S-001" in line)
    assert "여유" in s001_line


def test_menu_choice_change_thresholds_blank_input_keeps_current_value():
    repo = FakeRepository(SAMPLES, ORDERS)

    # 첫 값은 변경(500), 두 번째는 빈 값으로 유지(기본 300 유지)
    text = run_cli(repo, ["5", "500", "", "5", "", "", "6"])

    assert "500" in text
    assert "300" in text


def test_menu_choice_order_list_filtered_by_status_then_exit():
    repo = FakeRepository(SAMPLES, ORDERS)

    text = run_cli(repo, ["3", "CONFIRMED", "6"])

    assert "ORD-2" in text
    assert "ORD-1" not in text


def test_menu_choice_order_list_all_when_blank_filter_then_exit():
    repo = FakeRepository(SAMPLES, ORDERS)

    text = run_cli(repo, ["3", "", "6"])

    assert "ORD-1" in text
    assert "ORD-2" in text


def test_menu_choice_refresh_calls_repository_reload():
    repo = FakeRepository(SAMPLES, ORDERS)

    run_cli(repo, ["4", "6"])

    assert repo.reload_call_count == 1


def test_invalid_menu_choice_shows_error_and_continues():
    repo = FakeRepository(SAMPLES, ORDERS)

    text = run_cli(repo, ["9", "6"])

    assert "알 수 없는" in text or "잘못된" in text


def test_cli_never_writes_to_repository():
    repo = FakeRepository(SAMPLES, ORDERS)

    run_cli(repo, ["1", "2", "3", "", "4", "5", "", "", "6"])

    for forbidden in ("save", "write", "add_sample", "add_order", "delete", "update"):
        assert not hasattr(repo, forbidden)


def test_cli_end_to_end_with_real_repository_reads_fixture_files():
    repo = ReadOnlyJsonRepository("tests/fixtures")

    text = run_cli(repo, ["1", "6"])

    assert "등록 시료 수: 2" in text
    assert "전체 주문 수: 5" in text
