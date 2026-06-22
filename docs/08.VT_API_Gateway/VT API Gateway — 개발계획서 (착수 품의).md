**요약**

| 항목        | 내용                                         |
| --- | --- |
| 개발 제품 / 버전 | **VT API Gateway v1.0** — 2단계 (core `gw/1.0.0.b1` → full `gw/1.0.0.0`) |
| 일정 | core(pilot) **~2026-08-15** · full(정식) **~2026-09-26** · 기획 동결 06-27 |
| 공수 | **≤ 9.5 MM (6,940만 원)**, 목표는 그 이하 |
| 상태 | **IN REVIEW** 착수 품의 대기 |

## 1. 개발 목적

VT-Straumann **공진화 전략**(Straumann AXS 연동)의 실행 기반을 확보하고, 나아가 바텍 **전사 표준 API Gateway**를 구축한다. 의료 디바이스 통신을 중앙 control plane으로 일원화하고, 데이터는 디바이스–리전 직결로 주권을 보장한다. 아울러 ESMN *VatechAPIGateway Roadmap*(2026-06-11)의 API 버전 호환성·OneID 인증면·Webhook 분배를 v1.0 범위로 흡수하여 사내 클라우드 서비스(CleverOne·EzServer·CleverSpace) 연동까지 단일 게이트웨이로 수용한다.

사업 동인: [VGBX-8906](https://vts.vatech.com/browse/VGBX-8906) · [VTWB-16535](https://vts.vatech.com/browse/VTWB-16535)

## 2. 개발 범위

| 구분 | 내용 |
| --- | --- |
| **핵심** 제대로 동작 | 디바이스 인증 · 레지스트리 · 온보딩 · 단일 리전 주권 · 업로드 세션 · AXS 연동 · Fleet 기본(heartbeat·kill-switch) · **API 버전 호환성(Vatech-* 헤더·well-known)** · OneID 연계 · Webhook 수신(forward) |
| **경량** MVP 수준 | 감사 로그 · RBAC · 관리자 UI · consent · 데이터 분류 태깅 |
| **제외** post-MVP | DPoP+HW키 · 멀티클라우드 · 리전 signer 다수 · 레거시 10만대 마이그레이션 · 추가 connector |

## 3. 일정 (마일스톤)

| 단계 | 목표일 | 핵심 산출물 |
| --- | --- | --- |
| 기획·설계 동결 | 06-27 | PRD · ARD · API 명세 · 인증/주권 설계 + 착수 품의 |
| v1.0-core 개발 | ~08-08 | Control Plane · Upload Session · AXS 연동 · Fleet 기본 |
| **CORE** 출시 (pilot) | 08-15 | gw/1.0.0.b1 — 호주 Straumann pilot 투입 |
| v1.0-full 개발 | ~09-12 | 관리자/RBAC(경량) · relocation/consent · fleet 지표 |
| **FULL** 정식 출시 | 09-26 | gw/1.0.0.0 — v1.0 요구사항 전부 충족 |

## 4. 팀 구성 · 비용

- **팀**: BE Lead · BE Mid (코어) · FE Mid (관리 UI 경량) · DevOps Mid (IaC·배포)
- **비용**: 총 **≤ 9.5 MM (6,940만 원)**, 목표는 그 이하

## 5. 기술 스택

| 영역 | 스택 |
| --- | --- |
| Backend | NestJS + DDD + TDD |
| Frontend (관리 UI) | React + Vite + FSD + shadcn/ui |
| 데이터 | PostgreSQL · Redis(캐시) · RabbitMQ(큐) · S3/MinIO(스토리지) |
| 플랫폼 | OPA(정책) · KMS/Vault(시크릿) · OpenTelemetry+Pino(관측·로깅) · Feature Flag(Unleash) |
| 인프라 | IaC(Terraform/CDK) · CI(Azure Pipelines) · API 문서(Swagger) |

상세·근거: [ARD §4.5 기술 스택](<VT API Gateway — ARD (아키텍처).md>)

## 6. 첨부 · 근거 문서

- [VT API Gateway — PRD (v2)](<VT API Gateway — PRD (v2).md>) — 무엇을·왜
- [VT API Gateway — ARD (아키텍처)](<VT API Gateway — ARD (아키텍처).md>) — 아키텍처·ADR·시퀀스·컴포넌트
- [VT API Gateway — API 명세·데이터 모델·주권](<VT API Gateway — API 명세·데이터 모델·주권.md>) — 인터페이스·데이터
- [VT API Gateway — 인증·보안·컴플라이언스 설계](<VT API Gateway — 인증·보안·컴플라이언스 설계.md>) — 보안·인증·IEC62304
- [VT API Gateway — 요구사항 명세 (Requirements)](<VT API Gateway — 요구사항 명세 (Requirements).md>) — FR/NFR 67(v1.0 53)

## 7. 결재선

기안자(PL) → 개발실장 → 전략기획실장 → 대표이사

착수 승인 이슈: [ESIP-10](https://vts.vatech.com/browse/ESIP-10) · 작업 Epic: [ESIP-2](https://vts.vatech.com/browse/ESIP-2)

문서 통제 · 개정 이력

| 문서 ID | ESIP-GW-PLAN |
| --- | --- |
| 적용 제품 버전 | gw/1.0.0.0 |
| 분류 | 통제 문서 (Controlled · IEC 62304 / ISO 13485) |
| 상태 | Draft |

| v0.1 | 2026-06-08 | Scott | 착수 품의 초안 |
| --- | --- | --- | --- |
| v0.2 | 2026-06-08 | Scott | 기술 스택 반영 + 가독성 재정리 |
| v0.3 | 2026-06-15 | Scott | ESMN Roadmap 흡수 반영 — API 호환성·OneID·Webhook 범위 추가 |