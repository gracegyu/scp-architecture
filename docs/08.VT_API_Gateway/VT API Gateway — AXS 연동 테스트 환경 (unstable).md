**문서 통제**

| 항목           | 내용                                                                                                                       |
| -------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 문서 ID        | ESIP-GW-AXS-TESTENV                                                                                                        |
| 문서 버전      | v0.1 (스켈레톤)                                                                                                            |
| 적용 제품 버전 | gw/1.0.0.0                                                                                                                 |
| 분류           | 통제 문서 (Controlled · IEC 62304 / ISO 13485)                                                                             |
| 상태           | Draft                                                                                                                      |
| Jira           | [ESIP-14](https://vts.vatech.com/browse/ESIP-14) (환경) · [ESIP-12](https://vts.vatech.com/browse/ESIP-12) (AXS Connector) |

## 0. 개정 이력

| 버전 | 일자       | 작성  | 변경                                    |
| ---- | ---------- | ----- | --------------------------------------- |
| v0.1 | 2026-06-08 | Scott | 스켈레톤 — 목적·환경·테스트 범위·케이스 |

## 1. 목적

AXS Connector([ESIP-12](https://vts.vatech.com/browse/ESIP-12)) 본 개발 전·중에 Straumann AXS 외부 연동을 조기 검증하기 위한 **비프로덕션 unstable 환경 + 기본 연동 테스트**. 외부 의존(스트라우만) 리스크를 앞단에서 제거(de-risk).

## 2. 환경 정의 (unstable)

- 비프로덕션 · 잦은 변경 허용(unstable) · 단일 리전.
- Straumann AXS **sandbox**에 연결(운영 자격증명 미사용).
- **PHI 미사용** — 테스트/더미 데이터만. 환경은 IaC로 재현.

## 3. 연동 테스트 범위 (smoke)

| ID | 테스트 | 판정 |
| ----- | ---------------------------------- | ---------------------------- |
| TC-01 | AXS OAuth2 인증 토큰 획득          | 토큰 발급·갱신 성공          |
| TC-02 | 기본 API 호출 (헬스/메타)          | 2xx 응답·스키마 일치         |
| TC-03 | 파일 전달 (presigned, 소용량 더미) | 업로드·전달 성공·상태 콜백   |
| TC-04 | 오류·재시도 경로                   | 표준 오류·백오프 재시도 동작 |

## 4. 사전 조건 (TBD)

- AXS sandbox endpoint · OAuth Client 자격증명 (스트라우만 제공 필요).
- unstable 환경 IaC · 단일 리전 storage.

## 5. 링크

[PRD (v2)](<VT API Gateway — PRD (v2).md>) · [ARD](<VT API Gateway — ARD (아키텍처).md>) · Jira: [ESIP-14](https://vts.vatech.com/browse/ESIP-14) · [ESIP-12](https://vts.vatech.com/browse/ESIP-12) · [ESIP-2](https://vts.vatech.com/browse/ESIP-2)
