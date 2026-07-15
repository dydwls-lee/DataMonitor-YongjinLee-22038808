# HARNESS — data-monitor

이 저장소는 통합 저장소(`SampleOrderSystem-YongjinLee-22038808`)의 에이전틱 개발 오케스트레이션 중 `implementer`/`test-reviewer` 두 에이전트가 담당하는 모듈이다. 전체 파이프라인과 다른 에이전트(`main`, `docs-checker`, `integration-builder`, `compliance-reviewer`, `scenario-tester`)의 역할은 통합 저장소의 `docs/HARNESS.md`를 따른다.

## implementer (data-monitor)

- 요구사항 원천: [PRD.md](PRD.md), 공유 스키마 `docs/SCHEMA.md`(통합 저장소 루트)
- `data-persistence`의 Repository(또는 동일 JSON 파일 규칙)를 읽기 전용으로만 사용 — 이 모듈에서 데이터를 변경하는 코드를 작성하지 않는다
- `test-driven-development` 스킬에 따라 RED → GREEN → REFACTOR로 구현
- 커밋은 `[ACTION]` 접두사만 사용
- `data-persistence`의 Repository 인터페이스가 아직 확정되지 않았다면 계약(메서드 시그니처)만 가정하고 진행하되, 확정되는 대로 `main`에게 확인 요청

## test-reviewer (data-monitor)

- [PRD.md](PRD.md)의 "완료 기준"과 실제 구현/테스트를 대조
- 확인 항목: 상태별 집계(`REJECTED` 제외 여부는 이 도구 자체 집계가 아니라 통합 저장소 PRD의 모니터링 정의를 따르는지 확인), 시료/주문 목록 조회, 재조회 시 최신 데이터 반영 여부, 원본 데이터 미변경 여부
- 미충족 시 구체적 사유와 함께 `implementer`에 반려, 통과 시 통합 저장소 `main`에 "통합 준비 완료" 보고
