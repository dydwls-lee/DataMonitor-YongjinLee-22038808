"""독립 실행 entry point: ``python -m data_monitor [data_dir]``.

기본 데이터 디렉터리는 SCHEMA.md §4에 정의된 ``data/`` (samples.json,
orders.json이 위치하는 곳)이다. 메인 시스템/dummy-data-generator와 동시에
실행되어도 안전하도록 이 프로세스는 파일을 읽기만 한다.
"""

from __future__ import annotations

import sys

from data_monitor.cli import run
from data_monitor.repository import ReadOnlyJsonRepository

DEFAULT_DATA_DIR = "data"


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    data_dir = args[0] if args else DEFAULT_DATA_DIR

    repository = ReadOnlyJsonRepository(data_dir)
    run(repository)


if __name__ == "__main__":
    main()
