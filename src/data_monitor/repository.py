"""SCHEMA.md §4 저장 포맷 계약에 따른 읽기 전용 JSON 리포지토리.

``data-persistence``가 기록하는 ``data/samples.json`` / ``data/orders.json``
파일을 직접 읽기만 한다. 이 클래스는 어떤 쓰기 메서드도 제공하지 않는다.

호출 시점마다 디스크를 읽지 않고, 최초 로드 시점의 스냅샷을 유지하다가
명시적으로 ``reload()``가 호출될 때만 다시 읽는다 (PRD의 "명시적 갱신" 요건).
"""

from __future__ import annotations

import json
from pathlib import Path

from data_monitor.models import Order, Sample


class ReadOnlyJsonRepository:
    SAMPLES_FILENAME = "samples.json"
    ORDERS_FILENAME = "orders.json"

    def __init__(self, data_dir: str) -> None:
        self._data_dir = Path(data_dir)
        self._samples: list[Sample] = []
        self._orders: list[Order] = []
        self.reload()

    def reload(self) -> None:
        """samples.json / orders.json을 다시 읽어 스냅샷을 갱신한다."""
        self._samples = [
            Sample.from_dict(raw) for raw in self._read_json_array(self.SAMPLES_FILENAME)
        ]
        self._orders = [
            Order.from_dict(raw) for raw in self._read_json_array(self.ORDERS_FILENAME)
        ]

    def list_samples(self) -> list[Sample]:
        return list(self._samples)

    def list_orders(self) -> list[Order]:
        return list(self._orders)

    def _read_json_array(self, filename: str) -> list[dict]:
        path = self._data_dir / filename
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            content = json.load(f)
        return content
