**요약**

| 항목        | 내용                                         |
| --- | --- |
| 개발 제품 / 버전 | **VT API Gateway v1.0** — 2단계 (core `gw/1.0.0.b1` → full `gw/1.0.0.0`) |
| 일정 | core(pilot) **~2026-08-15** · full(정식) **~2026-09-26** · 기획 동결 06-27 |
| 공수 | **≤ 9.5 MM (6,940만 원)**, 목표는 그 이하 |
| 상태 | **IN REVIEW** 착수 품의 대기 |

## 1. 개발 목적

VT-Straumann **공진화 전략**(Straumann AXS 연동)의 실행 기반을 확보하고, 나아가 바텍 **전사 표준 API Gateway**를 구축한다. 의료 디바이스 통신을 중앙 control plane으로 일원화하고, 데이터는 디바이스–리전 직결로 주권을 보장한다. 아울러 ESMN *VatechAPIGateway Roadmap*(2026-06-11)의 API 버전 호환성·사람 인증면·Webhook 분배를 v1.0 범위로 흡수하여 사내 클라우드 서비스(CleverOne·EzServer·CleverSpace) 연동까지 단일 게이트웨이로 수용한다.

사업 동인: [VGBX-8906](https://vts.vatech.com/browse/VGBX-8906) · [VTWB-16535](https://vts.vatech.com/browse/VTWB-16535)

## 2. 개발 범위

| 구분 | 내용 |
| --- | --- |
| **핵심** 제대로 동작 | 디바이스 인증 · 레지스트리 · 온보딩 · 단일 리전 주권 · 업로드 세션 · AXS 연동 · Fleet 기본(heartbeat·kill-switch) · **API 버전 호환성(Vatech-* 헤더·well-known)** · 사람(운영자) 인증 연계 · Webhook 수신(forward) |
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
| 데이터 | PostgreSQL(엔진 확정; **Aurora 권장**) · **Valkey(ElastiCache for Valkey·Redis 호환)** · **SQS(A·내부 큐)** · MQTT 브로커(B·IoT Core/Amazon MQ) · S3(스토리지; **GW 비호스팅·Provider 발급/중계**, AWS 미지원국은 Provider MinIO) |
| 플랫폼 | OPA(정책) · KMS·Secrets Manager+IRSA(시크릿) · OpenTelemetry(ADOT)+Pino(관측, CloudWatch/AMP·AMG) · Feature Flag(Unleash) |
| 인프라 | **AWS EKS(K8s)·ECR·IRSA** · IaC(Terraform/CDK) · CI(Azure Pipelines) · API 문서(Swagger) — **GW는 AWS 전용 배포** |

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
| v0.4 | 2026-06-24 | Raymond | §5 기술 스택을 EKS 정합으로 갱신 — 데이터: 큐 `RabbitMQ`→**SQS(A·내부)**·MQTT는 IoT Core(B·엣지)로 분리, PostgreSQL→RDS/Aurora·Redis→ElastiCache 명시; 플랫폼: Secrets Manager·ADOT; 인프라: EKS·ECR·IRSA 추가 (SRS §3.1.2와 정합) |
| v0.5 | 2026-06-25 | Raymond | §5 DB 표기 정리 — 엔진=PostgreSQL 확정, 관리형 제품(Aurora 권장 vs RDS)은 확정 TBD로 명시(SRS §3.1.2 비교표·Appendix B #18과 정합) |
| v0.6 | 2026-06-25 | Raymond | §5 DB 권장 강화 — **처음부터 Aurora PostgreSQL 권장**(RDS-first는 멀티 리전 마이그레이션 비용으로 비권장), 인프라 비준 TBD(SRS §3.1.2와 정합) |
| v0.7 | 2026-06-25 | Raymond | §5 **포터빌리티(벤더 중립) 반영** — AWS 미지원 국가는 비AWS·private 배포. 큐 SQS→**RabbitMQ/AMQP**, 엣지 IoT Core→**포터블 MQTT(EMQX 등)**, 시크릿 IRSA→Vault+k8s SA 병기, EKS→임의 k8s, DB/캐시/관측도 AWS↔self-host 프로파일. SQS·IoT Core 비채택 명시(SRS §3.1.2·§2.1.2와 정합) |
| v0.8 | 2026-06-25 | Raymond | **GW=AWS 전용 확정(회의 결정)** — v0.7 포터빌리티 롤백, AWS-native 복귀(SQS·IoT Core·IRSA·Aurora·EKS). AWS 미지원국도 가까운 AWS GW 접속·storage는 Provider MinIO 중계(GW 비호스팅). SRS §3.1.2·§2.1.1과 정합 |
| v0.9 | 2026-06-26 | Raymond | §5 캐시 엔진 **Redis→Valkey** — Redis 오픈소스 종료(2024 초)·AWS는 ElastiCache for Valkey(저비용·Redis 호환) 제공. 제품=ElastiCache for Valkey, 엔진=Valkey(Redis 호환)(SRS §1.4·§3.1.2와 정합) |