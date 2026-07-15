"""데이터 모니터링 Tool 콘솔 메뉴 루프.

이 모듈은 읽기 전용이다: repository에 대해 list_samples/list_orders/reload
외의 어떤 메서드도 호출하지 않는다.
"""

from __future__ import annotations

from typing import Callable, Protocol

from data_monitor.aggregator import filter_orders_by_status, summarize
from data_monitor.models import Order, Sample
from data_monitor.rendering import render_orders_table, render_samples_table, render_summary

MENU_TEXT = """=== 데이터 모니터링 Tool ===
1. 전체 요약
2. 시료 목록 조회
3. 주문 목록 조회 (상태 필터)
4. 새로고침
5. 종료
선택> """

_EXIT_CHOICE = "5"


class Repository(Protocol):
    def list_samples(self) -> list[Sample]: ...

    def list_orders(self) -> list[Order]: ...

    def reload(self) -> None: ...


def run(
    repository: Repository,
    read_input: Callable[[str], str] = input,
    write_output: Callable[[str], None] = print,
) -> None:
    while True:
        choice = read_input(MENU_TEXT).strip()

        if choice == "1":
            summary = summarize(repository.list_samples(), repository.list_orders())
            write_output(render_summary(summary))
        elif choice == "2":
            write_output(render_samples_table(repository.list_samples()))
        elif choice == "3":
            status = read_input("상태 필터 (빈 값이면 전체)> ").strip() or None
            filtered = filter_orders_by_status(repository.list_orders(), status)
            write_output(render_orders_table(filtered))
        elif choice == "4":
            repository.reload()
            write_output("최신 데이터로 새로고침했습니다.")
        elif choice == _EXIT_CHOICE:
            write_output("종료합니다.")
            return
        else:
            write_output(f"알 수 없는 선택입니다: {choice!r}. 1~5 중에서 선택하세요.")
