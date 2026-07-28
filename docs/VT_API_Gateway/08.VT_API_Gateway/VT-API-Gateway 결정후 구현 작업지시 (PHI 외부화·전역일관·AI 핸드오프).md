# VT API Gateway — 저장소 결정 후 구현 작업지시 (AI 핸드오프)

> **목적**: 「[GW 저장소 아키텍처 결정](<VT-API-Gateway 7-30 GW 저장소 전역일관 vs 리전분리 결정.md>)」이 **회의에서 확정**되면, 그 결정을 **코드·DB·테스트·문서에 반영**하는 작업을 AI(Claude Code) 세션에 넘기기 위한 지시서다. 회의에서 아래 **§1 결정값**만 채우면, **§7 붙여넣기용 지시 프롬프트**를 그대로 세션에 주면 된다.
>
> **왜 이 문서가 필요한가**: 이 결정은 **이미 만든 것(P0~P3 auth/enroll/device)** 이 아니라 **아직 안 만든 webhook(P8/P9)** 과 **소수의 데이터 계층 재배치**를 좌우한다. 지시 범위를 명확히 해 재작업을 0으로 만들고, 결정 종속 항목만 정확히 건드리게 한다.
>
> 작성 2026-07-28 · 대상 repo `vt-api-gateway`(Azure DevOps `ewoosoft/es-platforms`).

---

## 1. 회의에서 채울 결정값 (선결 입력) 🟨

> 회의 후 아래를 확정값으로 바꾼다. AI는 이 값에 따라 §3~§5를 분기 실행한다.

| # | 결정 | 확정값(회의 후 기입) | 기본 추천(문서 §7) |
|---|---|---|---|
| **D1** | webhook payload 저장소 | ☐ S3 / ☐ DynamoDB | 소형·저볼륨=DynamoDB · 대량 누적=S3 (Jack 볼륨·비용 견적) |
| **D2** | 관계형 토폴로지 | ☐ A(Aurora Global) / ☐ B(RDS+replica) / ☐ C(중앙 registry) | **A** |
| **D3** | v1.0 플랫폼 | ☐ Aurora / ☐ RDS | Aurora(마이그0·비용 근접) |
| **D4** | 멀티리전·failover | ☐ gw/1.2 멀티리전 O/X · failover 요건 ___ | 이월 #9 RTO/RPO 연계 |
| **D5** | audit_log·fleet_state 위치 | ☐ gw_global(전역 관계형) / ☐ gw_regional 유지 | **gw_global**(둘 다 non-PHI·문서 §3.3·§6) |
| **D6** | gw_regional 관계형 처분 | ☐ 소멸(리전 로컬=payload 저장소만) / ☐ 유지(webhook_event 메타만 잔류) | D1·D5 확정 후 파생 |

> **주의**: D3(Aurora vs RDS)는 **인프라 연결 문자열**만 바꾼다 — 앱/Prisma 코드 불변(③-I 몫). D1·D5·D6가 **코드에 실제 영향**을 준다.

---

## 2. 무엇을 건드리지 말 것 (재작업 금지 경계)

이 결정은 아래를 **바꾸지 않는다** — AI는 절대 재작업하지 말 것:

- **P0~P3 전체**(auth·enroll·device·operator·RBAC): 전부 `gw_global`(non-PHI 컨트롤플레인) 위라 A/B/C·S3/DynamoDB 무관하게 불변.
- `gw_global` 스키마의 device·clinic·region_catalog·target·org_mapping·policy·config·operator·operator_role·client_inventory.
- 그 위의 e2e(token·device-auth·operator-auth·admin-me·devices-lifecycle·enroll-*·pending-expiry) — **변경 없음**.

**바뀌는 것은 오직**: (a) PHI payload 저장(P8/P9·미구현), (b) audit_log·fleet_state 위치(D5), (c) gw_regional 관계형 처분(D6), (d) 그에 따른 문서/DBML.

---

## 3. 데이터 계층 변경 (D5·D6 확정 시)

### 3.1 audit_log·fleet_state 재배치 (D5 = gw_global 인 경우)
- **Prisma 스키마**: `prisma/regional/schema.prisma` 의 `audit_log`·`fleet_state` 모델을 `prisma/global/schema.prisma` 로 이동(append-only 트리거 마이그레이션 포함 — audit_log 불변성 트리거를 global 클러스터에 재적용).
- **AuditService**(`libs/common/src/audit/audit.service.ts`): `AUDIT_LOG_WRITER` DI 토큰 바인딩을 **리전 PrismaClient → 전역 PrismaClient** 로 변경(구조적 인터페이스는 동일, 배선만 변경). 각 앱의 audit 모듈 wiring 갱신.
- **마이그레이션**: 기존 리전 audit_log/fleet_state 데이터가 있으면 이관 스크립트(로컬/테스트는 재시드라 무관 · prod는 미배포라 데이터 없음).
- **영향받는 기구현**: T-DATA-1-5(AuditService)·T-DATA-1-1(2-datasource 스캐폴드). audit 는 현재 거의 미사용(P11 연기)이라 저-touch.

### 3.2 gw_regional 관계형 처분 (D6)
- **D6 = 소멸**: 리전 관계형에서 audit/fleet(→global)·webhook_event 메타 처리 확정 후, `gw_regional` datasource 를 **payload 저장소(S3/DynamoDB) port 로 대체**. Prisma regional schema 제거 또는 축소. `RUN_DB_INTEGRATION` e2e 하네스의 regional migrate 단계 조정.
- **D6 = webhook_event 메타 잔류**: webhook_event 의 **메타 컬럼은 전역 관계형**(§3.3), **payload 만 저장소**. webhook_event 모델을 global 로 옮기고 `payload_encrypted` 컬럼을 **저장소 참조 key** 로 교체.
- 어느 쪽이든 **claim-check port**(§4)로 payload 접근을 추상화해 저장 매체를 앱 경계에 가둔다.

---

## 4. claim-check port 신설 (P8/P9 착수 전 · 저장 매체 추상화)

- **위치**: `libs/common/src/ports/` (기존 queue.port·kms.port·mqtt.port 패턴 미러 — DI 토큰 겸 타입=abstract class).
- **인터페이스(개념)**: `putPayload(eventId, ciphertext): Promise<{ ref: string }>` · `getPayload(ref): Promise<Buffer | null>`. 반환 `ref` = S3 key 또는 DynamoDB PK(저장 매체 은닉).
- **어댑터**: D1 확정값에 따라 `s3-payload.adapter.ts` **또는** `dynamodb-payload.adapter.ts` 1종 구현 + inmemory 어댑터(unit/e2e 더블). 기존 `ports/adapters/inmemory/*` 패턴 재사용.
- **암호화**: payload 는 **GW가 KMS envelope 로 암호화한 ciphertext** 만 port 에 넘긴다(기존 `crypto/kms-envelope` 재사용) + 저장소 관리형 암호화 병행. "GW만 복호"(§7.6.3) 속성 불변.
- **크기 가드**(D1=DynamoDB 시): >400KB payload 거부+DLQ+경보 한 줄(§4.4).

---

## 5. P8/P9 구현 시 반영 (webhook 수신·분배 · 2단계)

> P8/P9 는 이 결정의 **핵심 타격점**이자 **미구현**이라, 결정 후 처음 만들 때 아래를 전제로 구현(뒤엎을 일 없음).

- **P8 Receiver**: webhook 수신 → 메타는 관계형(전역)에 insert, **payload 는 claim-check port.putPayload** 로 리전 로컬 저장소에. SQS enqueue 는 **eventId(+ref)만**(claim-check).
- **P9 Dispatcher**: SQS consume → **claim-check port.getPayload(ref)** 로 본문 복원 → 대상 해석 → MQTT 하행. DLQ.
- **Console break-glass**(§7.6.3): `GET /v1/admin/webhook-events/{eventId}/payload` = 해당 리전 GW 가 port 로 복호→마스킹→감사 후 반환.
- **주권(FR-RGN-03)**: payload 는 리전 로컬 저장소에만 · 복제/Global Tables 금지.

---

## 6. 문서·산출물 반영 (결정 직후)

- **ADR** 신설: 대안(payload 저장소 ①②③·토폴로지 A/B/C)·근거·결정 기록.
- **SRS**(baseline 통제·개정이력·승인·fixVersion): **§7.6.3**(payload=리전 로컬 저장소 claim-check·KMS·S3 lifecycle 또는 DynamoDB TTL) · **§2.1.1**(데이터 클래스·다이어그램) · **§3.1.2**(v1.0 플랫폼) · **§2.7.1**. *(SRS 는 사용자가 별도 커밋 — AI 는 초안·diff 제안만.)*
- **DBML**: `webhook_event.payload_encrypted` → payload 참조 key(S3 key/DynamoDB PK)+KMS 참조 · (D5 시)audit_log·fleet_state 를 global 스키마로 이동.
- **IP**(`abc-dev-assistant/projects/vt-api-gateway/ImplementationPlan.md`): **P8 Task 카드**의 payload 저장 대상 변경(관계형→리전 로컬 저장소·claim-check) · P9 getPayload 반영 · (D5)audit/fleet 위치. depends_on 갱신.

---

## 7. 붙여넣기용 지시 프롬프트 (회의 후 세션에 그대로 전달)

> 아래 `{ }` 를 §1 확정값으로 치환한 뒤, Claude Code(vt-api-gateway repo) 세션에 붙여넣는다.

```
GW 저장소 아키텍처 결정이 확정됐어. 결정값:
- D1 payload 저장소 = {S3 | DynamoDB}
- D2 토폴로지 = {A Aurora Global | B RDS+replica | C 중앙 registry}
- D3 플랫폼 = {Aurora | RDS}
- D5 audit_log·fleet_state 위치 = {gw_global | gw_regional 유지}
- D6 gw_regional 관계형 = {소멸 | webhook_event 메타 잔류}

이 결정을 반영해줘. 지시서 = docs/VT_API_Gateway/08.VT_API_Gateway/
"VT-API-Gateway 결정후 구현 작업지시 (PHI 외부화·전역일관·AI 핸드오프).md" (§2 재작업 금지 경계 준수).

순서:
1. (D5=gw_global 이면) audit_log·fleet_state 를 prisma/regional → prisma/global 로 이동 +
   AuditService 의 AUDIT_LOG_WRITER 바인딩을 전역 PrismaClient 로 변경. 트리거·마이그레이션 포함.
2. claim-check port(libs/common/src/ports/) 신설 + D1 어댑터 1종 + inmemory 더블.
3. DBML(webhook_event.payload_encrypted→저장소 key · audit/fleet 위치) diff 제안.
4. IP P8/P9 Task 카드 갱신(payload 저장=claim-check) — 실제 P8/P9 구현은 별 Task 로.
5. SRS §7.6.3·§2.1.1·§3.1.2·§2.7.1 반영 초안(diff만 — 내가 baseline 커밋).

제약: P0~P3(gw_global auth/enroll/device) 절대 재작업 금지(§2). 각 코드 변경은 검증 4종
(unit·e2e·curl·DB조회)+pre-pr-review 독립 리뷰 후 Task별 PR. repo 표준(CLAUDE.md)·dev-chain-backend 준수.
```

---

## 8. 요약 (한 줄)

**이 결정은 P0~P3(gw_global)이 아니라 webhook(P8/P9·미구현)과 audit/fleet 위치를 좌우한다.** 1단계(P4~P6)는 결정과 무관하게 계속 진행하고, 회의에서 §1을 확정하면 **§7 프롬프트**로 §3~§6(데이터 재배치·claim-check port·문서)만 국소 반영한 뒤 P8/P9 를 그 전제로 구현한다 — **재작업 0.**
