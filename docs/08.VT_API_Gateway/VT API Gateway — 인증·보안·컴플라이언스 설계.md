**문서 통제**

| 문서 ID | ESIP-GW-SEC |
| --- | --- |
| 문서 버전 | v0.2 (Roadmap 흡수) |
| 적용 제품 버전 | gw/1.0.0.0 |
| 분류 | 통제 문서 (Controlled · IEC 62304 / ISO 13485) |
| 상태 | Draft |

## 0. 개정 이력

| v0.1 | 2026-06-08 | Scott | 인증·인가·보안·컴플라이언스 설계 초안 |
| --- | --- | --- | --- |
| v0.2 | 2026-06-15 | Scott | Roadmap 흡수 — OneID 인증면(2면)·Webhook 검증·버전 호환 위협 추가 |

출처: [ARD](<VT API Gateway — ARD (아키텍처).md>) (ADR·시퀀스) · [요구사항 명세](<VT API Gateway — 요구사항 명세 (Requirements).md>).

## 1. 인증 (Authentication)

- 디바이스 무인: OAuth2 **client_credentials** → 단명 JWT(claim: device_id·region·audience·짧은 TTL).
- 외부 토큰: 암호화 저장(at-rest)·만료 전 자동 갱신. secret **자동 회전(dual-window)**.
- v1.1: **DPoP**(sender-constrained) + 하드웨어 키(SE/TPM). (mTLS 미채택 — ADR-01)
- **인증 2면(ADR-08)**: 위 디바이스 머신 인증과 별개로, 사람·클리닉·사내 호출자(EzServer/CleverOne)는 **OneID(OIDC)**로 인증. 두 surface는 분리·매핑(FR-AUTH-08/09).

## 2. 온보딩 (Enrollment)

- 신뢰 뿌리 순서: 하드웨어 신원 > 공장 토큰 > OOB 일회 코드.
- nonce challenge(replay 방지) · device fingerprint · geo/velocity 이상탐지. allowlist = 토큰 발급 집합.

## 3. 인가 (Authorization)

OPA — allowlist · region · scope · connector egress 판단. data classification 태그가 판단 근거.

## 4. 데이터 보호

전 구간 TLS · 시크릿 KMS · 평문 로깅 금지 · **PHI/PII 비저장(control)** · 파일 staging 즉시 정리.

## 5. 위협 → 대응 (ADR 정합)

| 토큰 탈취 후 remote replay | DPoP(sender-constrained) — 디바이스 키 바인딩 |
| --- | --- |
| 물리 접근 키 추출(의료기기) | 하드웨어(SE/TPM) 보관 — mTLS로는 미해결 |
| 임의 기기 등록 | enrollment token·nonce·fingerprint·이상탐지·allowlist |
| 국경 데이터 유출 | 주권 라우팅 + consent·classification 게이팅 |
| 위조된 외부 Webhook 호출 | Webhook Receiver — HMAC 서명·IP allowlist·timestamp·eventId 멱등(ADR-09) |
| 버전 불일치 원인불명 실패 | API Compatibility Gate — Vatech-* 헤더·well-known·매트릭스(ADR-07) |

## 6. 컴플라이언스 (IEC 62304 / ISO 13485)

- 요구사항 추적성: FR/NFR ID ↔ 설계(ADR) ↔ 테스트 수용 기준 ([요구사항 명세](<VT API Gateway — 요구사항 명세 (Requirements).md>)).
- 통제 문서·개정 이력·승인(위임전결)·릴리스 baseline 동결.
- append-only 감사 로그 · cross-border consent tracking · data classification.