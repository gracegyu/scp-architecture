# SCP 로컬 캐시 서버 – 컨텍스트(작업 기준 문서)

본 문서는 Cursor 멀티‑레포 환경에서 공통 컨텍스트를 빠르게 공유하기 위한 요약입니다. 문서/코드가 변경될 때 본 파일도 간단 요약으로 갱신합니다.

## 1) 목적/범위
- 치과 클리닉용 로컬 캐시 서버 사전 기술 검증(POC).
- 핵심 주제: Reverse Proxy(Nginx/OpenResty, Envoy, Pingora), 저장소(FS/RocksDB/PostgreSQL/Redis), 캐시 알고리즘(LRU/SLRU/W‑TinyLFU 등), 통합 프로토타입, Windows 설치(NSIS)·Linux(CacheBox) 배포.

## 2) 레포 구조(문서 ↔ 코드)
- 문서 레포: `scp-architecture`
  - 기준 문서 허브: `docs/SCP Cloud Server 연구/캐시 서버 연구/0.로컬 캐시 서버 연구.md`
  - PoC 문서: `docs/.../PoC/PoC1~5_*.md`
- 코드 레포: `scp-cache-poc` (모노레포)
  - `poc1/nginx-openresty`, `poc1/envoy`, `poc1/pingora`
  - `poc2/media-fs|media-rocksdb|meta-postgres|meta-redis`
  - `poc3/simulator`, `poc4/prototype`, `poc5/installer`
  - 공통: `services/cache-service-rust`, `bench/k6|wrk`, `env/docker|windows`, `RESULTS`

## 3) 워크스페이스
- Cursor 멀티 루트: `scp.code-workspace`
- 권장 열기: 워크스페이스 파일 더블클릭 → 좌측에 두 레포 동시 표시 → 레포별 커밋/푸시 분리

## 4) 기술 의사결정(요약)
- 개발 언어: Rust 우선(외부 서비스, WASM 필터 포함). C++/Lua는 대안.
- OS/배포: Windows(NSIS) + Linux 지원 재도입. CacheBox(HW) + Docker Compose 검토.
- Reverse Proxy: Nginx/OpenResty, Envoy 비교 + Pingora(Rust, Linux 우선) 추가 검토.
- 설치/운영: 자동 업데이트(백그라운드/무중단/롤백) 필수, 모니터링/진단 도구 포함.

## 5) 진행 관리
- 진행 상태는 각 PoC 문서의 체크리스트를 단일 소스오브트루스로 사용.
  - 예: `PoC1_Reverse_Proxy_비교.md`의 체크리스트(83행 이후)
  - 상태 표기: 완료 `[x]`, 진행중 `[(in-progress)]` 또는 하위 항목 체크, 보류 `[ ]` + 사유
- 결과 문서: `PoC1_Reverse_Proxy_비교_result.md` 등으로 모아 정리(원시 지표는 코드 레포 `RESULTS/`).

## 6) 브랜치/커밋 규칙(코드 레포)
- 기본: `main`
- 기능/실험: `feature/<poc>/<topic>` (예: `feature/poc1-nginx-lua`)
- 커밋 메시지: `[POC1] scope: summary`

## 7) 첨부/컨텍스트 공유 팁
- 새 채팅 시작 시 본 `CONTEXT.md`와 해당 PoC 문서를 첨부하면 충분.
- 재현 방법이 바뀌면 `env/docker|windows`, `bench`와 본 파일을 우선 갱신.

## 8) 빠른 링크
- 메인: `docs/SCP Cloud Server 연구/캐시 서버 연구/0.로컬 캐시 서버 연구.md`
- PoC1: `docs/SCP Cloud Server 연구/캐시 서버 연구/PoC/PoC1_Reverse_Proxy_비교.md`
- 결과: `docs/SCP Cloud Server 연구/캐시 서버 연구/PoC/PoC1_Reverse_Proxy_비교_result.md`
- 코드 레포 루트: `../scp-cache-poc`

(최종 업데이트: 수시 갱신)


