# 부모 GW SRS 반영 백로그

> **목적.** 부모 GW SRS(정본 = `vt-api-gateway` repo · `docs/specs/SRS.md`)에 반영해야 하나 아직 별도 spec PR로 묶지 않은 변경을 추적한다.
>
> **원칙.** 진행 중 PR에 무관한 변경을 섞지 않는다(diff 오염·리뷰 지저분·스코프 훼손 방지).
>
> **위치 근거.** 정본 SRS는 `vt-api-gateway` repo. 이 디렉터리(`scp-architecture/…/03-srs-gateway`)는 리다이렉트 stub이라 SRS 본문은 편집하지 않고 **추적 문서(리뷰 로그·백로그)만** 둔다.

---

## 완료·PR 반영 이력

baseline `spec-v1.0.11`(#12440·#12453). 이후 **4개 spec PR를 모두 병합**하고 **`spec-v1.0.12`(`79870c6`·2026-08-06)** 로 태깅했다 — 개별 백로그 항목(구 B-1·B-2·B-3·B-6·B-7·B-9)은 정리·삭제하고 이력만 보존한다.

| PR | 반영 내용 | 상태 |
| --- | --- | --- |
| **#12483** | (구 B-1·B-2·B-3 + B-4 안전분) §1.3 표기 범례·`aud={target}`·정보전략실 문구·동결 Roadmap 死링크 | ✅ **머지 완료** |
| **#12484** | (구 B-9) §2.3.6.3 IO Scanner 다운링크 시나리오+다이어그램 · Nemesis 반영(HMAC+timestamp·멱등 eventId·AXS 필드 ④ 위임) | ✅ **머지 완료** |
| **#12487** | (구 B-7) 멀티리전 authz §7.9.2 전역복제·§4.5.1 ZT 제거→S3+CloudFront+Entra·**Admin API 내부전용→Entra-gated 공개**(Jack 리뷰)·§2.1/§2.2 다이어그램·Appendix B #52. **`region_scope`는 리뷰 중 제거**(R1=전 리전 동일 sync·복제=gw/1.2) | ✅ **머지 완료** |
| **#12491** | (구 B-6) enroll CSR→IoT cert OpenAPI(`csr`·`iotCertificate`·`certificateId`)·§7.6.6 · Nemesis 반영(§7.2.4/§7.2.7 cert 폐기 갭·description) | ✅ **머지 완료** |

- URL: `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/{12483|12484|12487|12491}`. Nemesis 리뷰 8개 스레드 회신+resolve 완료.
- **B-5(apse4 멜버른→apse2 시드니 스윕)** — ✅ 완료(#12453·`spec-v1.0.11`). §4.5.1 내부 Admin API 도달 경로는 **#12487에서 Admin API Entra-gated 공개로 확정**(잔여=리전 전환 audience·Appendix B #52).
- **후속(스펙 세션 완료·spec-v1.0.12).** `spec-v1.0.12` 태그 · 구현세션 알림(v1.0.12 확정본) · IP 핀 갱신 + **T-ENR-3-6 신설**(enroll CSR→cert·게이팅·폐기) + Admin API CORS(P11 📌). → **구현세션 인계 준비 완료.**
- **잔여(gw/1.2·Appendix B #52).** 멀티리전 복제 계층(전역 seed·DynamoDB Global Table/Streams)·리전 전환 audience(§4.5.1 ⓒ). Console 반영 = Console 백로그 CB-1(부모 B-7 확정으로 트리거 met).
- **B-10 1차 batch** — ✅ 머지(PR #12632·`e865d77`·2026-08-12): DBML `org_mapping` 카디널리티 주석 + compat-matrix 범위(SRS §7.7/§7.7.5·Appendix B #8·DBML·well-known README·compat-matrix sample/yaml·config README/yaml·handoff)의 OnePager 철자·폐지된 ① 호환성 OnePager→제품 OnePager 정정. **계약/스키마 무변경**. *(범위 밖 잔여 = §1.2/§1.5·② Presigned OnePager 문안 → 아래 **B-10-2**로 이월.)*
- **B-4(주 범위)** — ✅ 머지(#12638·`spec-v1.0.20`·2026-08-12): '개발 Roadmap 결정' 문서 참조 **전체 제거**(§7.7.1/§2.3.0·일반명사 Roadmap 유지) + §7.7.1 식별 헤더 필수성 **2계층**(하드=Product·Version·Clinic-Id / best-effort=OS·UA·omit·누락 비오류) + §7.7.4 에러 정합 + §7.8.5 OS 부분 튜플·UA 원문 저장. 구현=T-CFG-5-1 헤더 미들웨어 조정(#12646). *(잔여=web-originator 헤더 세트·gated·비차단 → 진행 중 **B-4(잔여·web-originator)** 유지.)*
- **B-13** — ✅ 완료(#12714 `890c921`·후속 #12716·#12719·2026-08-18): 로컬 개발 DB / e2e DB 분리(`gw_test`·`make db-test-setup`·`make test-e2e-local`) + 멱등 `dev:operator` 시드. 구현=IP `T-DATA-1-8`. **SRS 무변경**(§3.5.2 위임·GW README).
- **B-14** — ✅ 해소(#12725·`spec-v1.0.25`·2026-08-18): AuditLog 리소스 축 `resourceType`/`resourceId` additive(SRS §7.9.3 + OpenAPI `AuditLog` 2필드/`GET /v1/admin/audit` 2필터 + DBML `audit_log` 2컬럼·복합 인덱스 + db-jsonb). 명명=resourceType(잠정 targetType 이탈·GW 프록시 대상 target 과 이름충돌 회피). 구현=IP `T-DATA-1-9`. Console 소비=`T-FE-6-6`.
- **B-15** — ✅ 해소(#12735·`spec-v1.0.26`·2026-08-18): AuditLog 응답에 `reason` 노출(정합화·OpenAPI+SRS §7.9.3+db-jsonb·**DBML 무변경**[컬럼 기존]·필터 없음). kill·거부·break-glass 사유를 감사 조회에서 되읽기 가능. 구현=`T-DATA-1-9`에 흡수. Console CB-4.
- **B-16** — ✅ 해소(#12740·`spec-v1.0.27`·2026-08-18): kill 엔드포인트에 `409` 선언(종단 재-kill=`assertTransition` 위반·PATCH와 정합·정합화). OpenAPI + SRS §7.2.3. **구현 무변경**(impl 이미 409 반환·계약만 정합). 연계 Console FR-CON-12 문구 정정=`spec-v1.0.2`(#12741).
- **현행 baseline = `spec-v1.0.27`(`927fc71`).** v1.0.13~1.0.27 누적. 상세 진행 이력 정본 = IP `projects/vt-api-gateway/ImplementationPlan.md` §2 노트.

---

## 진행 중 백로그

### B-4(잔여·web-originator). 웹 originator 헤더 세트·UA 기반 인벤토리 정식화 — gated·비차단
- **주 범위는 완료·이동.** Roadmap 死링크 제거 + §7.7.1 식별 헤더 2계층 + §7.7.4 + §7.8.5는 **#12638(`spec-v1.0.20`) 머지**로 완료(위 완료 이력). 여기 남는 건 web-originator 스코프뿐.
- **잔여(gated·비차단).** §2.3.0 웹 originator 헤더 세트 표 *세부* + **UA 기반 웹 클라 인벤토리 정식화**(product/version NOT NULL 완화·UA 파싱으로 식별키 소싱). **웹이 GW로 직접 originate 하는지(§2.3.0) 확정 후.** UA 원문은 이미 `client_inventory.user_agent`에 저장돼 원자료 손실 없음(파싱만 지연).
- **출처.** 헤더 정책=2026-08-12 사용자 · web-originator 스코프 gated.

### B-10-2. 저위험 문안 버킷 (2차·재사용) — 모아서 1 PR
- **방침**(B-10 1차 완료 후 승계·사용자 2026-08-10): 자잘한 주석·문안 정합은 건건 올리지 말고 여기 모아 **한꺼번에 1개 spec PR**로 처리한다(PR 노이즈·리뷰 부담 감소). 계약/스키마 무변경·저위험만(실질 변경은 별도).
- **항목:**
  - **OnePager 잔여 정정** — B-10 1차(PR #12632)가 compat-matrix 범위만 처리(§7.7·§7.7.5·Appendix B #8·compat 파일). **범위 밖 잔여**: SRS §1.2·§1.5·§4.1.4·§5 등의 `One Pager`(두 단어) 철자 통일 + **② Presigned OnePager** 참조(② 흡수 여부=제품 OnePager 반영 정리). 대상=SRS(§1.2·§1.5·§4.1.4·§5 등). [[onepager-terminology]].
- **트리거.** 항목이 몇 개 쌓이거나 다른 저위험 문안 PR을 올릴 때 함께. 대상 repo=vt-api-gateway(SRS).

### B-11. [gw/1.2] 멀티리전 확대 시 스펙 상세화 — roll-up 색인 (중복 기재 금지)
- **방침(사용자·2026-08-10).** gw/1.2(멀티리전 N리전 활성화) 착수 시 상세화·수정할 스펙을 **한 곳에 색인**한다. 대부분 **이미 개별 추적처가 있으므로 여기선 포인터만** 두고 내용은 정본에서 관리한다(중복 시 어긋남 방지). **트리거 = gw/1.2 설계 착수.**
- **부모 GW SRS(추적처 존재 — 포인터):**
  - 멀티리전 authz **복제 계층 구현**(DynamoDB Global Table + Streams·쓰기 권위 이관) → §7.9.2·**Appendix B #52**(모델·방식 확정·spec-v1.0.14). infra 예고=`03i-infra/_status.md` seed.
  - **(b) 리전 전환 운영자 토큰 audience** → Appendix B #52 (b)·§4.5.1 ⓒ (유일 잔여 미결).
  - **교차리전 webhook fallback(receiver-forward)·home 리전 discovery** → §2.3.6.2 TBD.
  - **리전 마이그레이션(클리닉 재홈)** 절차·API → Appendix B #50·§2.3.9·§7.3.4.
  - Region Directory N리전 행·GeoDNS 부재 확인 → §4.5.1·§7.3.6(대개 증분).
- **GW Console Sub-SRS(추적처=Console 백로그):**
  - 운영자 멀티리전 authz UX·리전 스위처·ZTNA 제거 등 → **Console 백로그 CB-1**·FR-CON-03a(v2.0/gw1.2). *Console SRS는 아직 draft(미승격)라 이 상세화는 baseline 후 CB-1로 흡수.*
- **신규(추적처 없던 것 — 여기서 관리):** *(현재 없음 — 생기면 이 아래 추가하고, 개별 추적처가 마련되면 포인터로 전환.)*
- **트리거.** gw/1.2 설계 착수. 그때 이 색인으로 상세화 대상을 일괄 점검.

### B-12. compat-matrix 8KB 초과 대응(S3 간접) — CI 크기 게이트 경고 시 착수
- **현재.** compat-matrix 렌더 JSON은 ~1KB로 SSM Advanced 상한(8KB)에 한참 못 미친다. **지금은 CI validate가 크기 게이트(≤8KB)로 조기 감지만** 한다(GW·`.azure-pipelines/compat-matrix.yml`). **S3 간접은 미구현**(불필요).
- **내용(착수 시).** `server-configuration.json`을 **S3 오브젝트**에 두고 Parameter Store엔 **S3 key만**, 앱은 그 key로 **S3 fetch·캐시**한다. SRS §7.7.5 ③에 **이미 provision**돼 있어 SRS 텍스트 변경은 최소(주로 구현·인프라).
- **소유.** 앱 S3 fetch 로직 + 파이프라인 = **GW** · **S3 버킷·IAM = ③-I**(handoff `docs/handoff/compat-matrix-infra.md`).
- **트리거.** CI 크기 게이트가 8KB(안전 임계) 임박/초과를 경고할 때. (그 전엔 착수 불요·YAGNI.)
- **출처.** 2026-08-11 사용자(백로그화).

### B-13. [gw/1.1] 정책(policy) 모델 재설계 + 집행 활성화
- **배경.** v1.0 정책은 **coarse(target 사용 허용)만** 집행하고 `allowed_endpoints`·`scopes`는 **미집행 예약**(코드 실측 확정 — `pdp.service.ts`가 읽기만 하고 무시). AXS가 Org-ID(데이터 격리)+consent(작업 권한)를 이미 집행하므로 v1.0 GW endpoint/scope 인가는 중복이라 미룸.
- **gw/1.1 설계 방향(업계 API GW 비교 결론·AWS/Istio/OPA).** endpoint 정책을 켠다면 **OPA(Rego) 기반 단일 default-deny + allow-grant + deny-override(deny 우선) + "둘 다 없음=deny"** 모델을 채택한다(spec이 이미 gw/1.1 OPA 예약). 이 모델이라야 **allow+deny 병존이 깔끔**(예: allow `/**` + deny `/x` = allow-all-except-x)하고, naive 병존(각 리스트가 반대 기본값)의 "둘 다 없음 모순"이 없다. `denied_endpoints`가 필요하면 이 규약으로 추가(둘 다 병존 금지 또는 deny-우선 명시)·또는 정책당 mode(allow XOR deny). **다만 실요구 나오기 전엔 endpoint 정책 자체가 과설계일 수 있음**(AXS 위임 유지 검토).
- **정책 테이블 재설계 가능성.** 위 모델 채택 시 `policy` 스키마가 바뀔 수 있다(denied_endpoints·mode·OPA 번들 참조 등). **v1.0 policy 테이블은 비어 있어(all-pass) 데이터 마이그레이션 부담이 사실상 없음** → gw/1.1에서 빈 테이블에 additive 재구성(저위험).
- **v1.0 처리(확정 2026-08-25·A안=유보).** 정책 테이블·PDP·CRUD **구조는 그대로**(DB 마이그레이션 0). core는 coarse 인가 기본값을 **뒤집어 "매칭 정책 없으면 allow(pass)"**(기존 "없으면 deny·target not authorized"를 flip)·**seed 정책 0개가 기본**·egress·PHI 리전·인증·AXS Org-ID는 그대로 집행. Console 정책 탭은 **보이되 클릭 시 "gw/1.1 지원 예정" 안내만**(CRUD·endpoint/scope 미노출). deny-by-default(WHO 인가)는 gw/1.1에서 복원. v1.0 policy 테이블은 비어 있어 gw/1.1 재구성은 빈 테이블 additive.

- **추천 정책 스펙(상세·gw/1.1 착수 시 참고).**
  1. **엔진**: OPA(Rego) PDP(현 앱 내부 모듈과 같은 PDP 포트 뒤로 전환·§3.1.2).
  2. **2계층 기본값**(핵심):
     - **target 차원(WHO) = deny-by-default 복원** — 정책 행 없으면 그 target 사용 불가. 멀티 target·클리닉 차등이 생기는 gw/1.1에서 의미. (v1.0은 이걸 유보=all-pass.)
     - **endpoint/scope 차원(narrowing) = allow-by-default-within-target** — target이 coarse 허용되면 기본은 전체 endpoint 허용, whitelist/blocklist로 **좁히는** opt-in.
  3. **endpoint 규칙**(`allowed_endpoints` + 선택 `denied_endpoints`·deny 우선):
     - 둘 다 empty/null → **전체 허용**(narrowing 없음). ← v1.0 `[]≡null` 모호성 자동 해소(둘 다 "제한 없음"으로 통일).
     - allow만 non-empty → **whitelist**(그것만).
     - deny만 non-empty → **blocklist**(그것 빼고 전부).
     - 둘 다 non-empty → **deny 우선**: 통과 = `E∈allow ∧ E∉deny`(allow에 없으면 deny). "둘 다 없음(∉allow,∉deny)" 모순 없음(allow 존재 시 whitelist 지배).
     - `pathPattern` glob(`*`=세그먼트1·`**`=0+), `methods` 배열(`*`=전체).
  4. **scope 규칙**: 토큰 scope ⊆ `policy.scopes`(non-empty 시)·empty=제한 없음. **단 AXS가 이미 scope/consent 집행 → 필요성 재검토(중복 가능).**
  5. **스코프 계층**(device→clinic→global): global=기본, clinic=상한(authoritative·global 대체 가능·소속 device 천장), device=clinic 상한 내 narrowing(⊆·권한상승 불가). 병합=OPA로 교집합 기반 명시.
  6. **별개 차원(그대로 유지)**: egress(`target.egress_allowlist`·fail-closed)·PHI 리전 경계는 정책과 독립 집행(v1.0에도 집행 중).
  7. **필요성 재검토(중요)**: AXS가 operation 인가(Org-ID 격리+consent) 소유 + verbatim 프록시라 GW endpoint/scope 정책은 **여전히 과설계일 수 있음**. **blast-radius 축소·클리닉별 권한 차등 같은 구체 실요구가 확인될 때만** endpoint/scope를 켠다. 그 전엔 coarse(target)+egress+region으로 충분.
  8. **마이그레이션**: v1.0 빈 테이블 → gw/1.1에서 `denied_endpoints`·`mode`(택1 방식 채택 시) 등 additive·저위험.
  9. **전환(활성화) 안전 — v1.0(정책 없으면 allow) → gw/1.1 (★기본 posture 결정에 종속)**:
     - **(a) deny-by-default 복원 시**: 활성화 순간 정책 0개면 **전 프록시 차단** → **정책 선-시드(기존 target/clinic 허용) 또는 dry-run(감사만) 모드로 실트래픽 확인 후 flip** 하는 무중단 롤아웃 필수(AWS/Istio 방식).
     - **(b) allow-by-default 유지 시**(정책=opt-in 제한): 전환 **무중단**(없는 곳은 계속 통과·정책 추가는 특정 케이스만 좁힘). v1.0→v1.1 매끄러움.
     - 스키마는 빈 테이블이라 무관. **gw/1.1 착수 시 기본 posture(a/b)를 의식적으로 결정**하고 그에 맞는 롤아웃을 잡는다. *(현재 v1.0=allow. (b) 유지가 가장 무중단·(a)는 보안↑이나 롤아웃 절차 비용.)*
- **병합 규칙.** device→clinic→global 상속의 정확한 병합(대체/교집합/패턴 우선순위)은 위 5번 방향으로 gw/1.1 OPA/LLD에서 확정(현재 under-spec).
- **출처.** 2026-08-25 사용자(정책 난해성 리뷰 → gw/1.1 재설계·v1.0 유보[A안] 확정 · 업계 API GW[AWS/Istio/OPA/Kong/Apigee] 비교 결론 반영).

---

## 참조 — 별도로 추적 중인 배치 (여기서 중복 기재하지 않음)
- **클라이언트 식별 헤더 제약(Thomas 헤더 배치)** — User-Agent 변경 불가·Vatech-OS 획득 불가·Vatech-Clinic-Id 자체 설정 불가(2026-08-06 주간회의 Thomas 안건). **방향 확정**: Clinic-Id=EzServer nginx 주입(결정 2) / **UA·OS=best-effort — 설정·획득 불가 시 omit(2026-08-12 확정)**. 주 범위는 **B-4(#12638) 머지 완료** · 잔여 §2.3.0 웹 originator 세트 표 세부는 웹의 GW 직접 originate 여부에 따라 달라지나 비차단(degrade·B-4 잔여).
- **Console SRS 자체 변경** — Console 백로그 `03c-subsrs-gw-console/_backlog-console.md`(CB-1 ZTNA 제거·운영자 멀티리전 authz UX / CB-2 v1·v2 분리·기술 스택 shadcn). **#12487 확정 후 CB-1 착수.**
- **Console → 부모 계약 변경** — 정본 추적 = Console SRS Appendix B "부모 SRS 반영 대상". **상태 점검(2026-08-12):**
  - ✅ **반영 완료(3)**: C-14(전역 bootstrap seed·§7.9.2·`spec-v1.0.12`·#12487) · C-15(사유 reason 저장·`audit_log.reason`+API·`spec-v1.0.15`·#12571) · C-16(enrollment Reject·`device_status=rejected`·`spec-v1.0.15`·#12571).
  - ⬜ **잔여(전부 비차단 · 계약 변경이라 저위험 문안과 분리·별도 부모 spec PR):**
    - **C-17**(실질적·구 목록 누락) — 역할×액션 권한 매트릭스 → 부모 §7.9.2 **명문화 + GW 코드/OPA 강제**. admin·cs 확정, **operator/developer 셀 = 보안/GW 확정 선결**. 신규 API 계약 아님(operatorAuth+OPA 기존). 트리거=Console baseline(met) + 보안/GW 결정.
    - **C-11**(선택·권고) — 서버 강제 낙관적 잠금(`expectedVersion`/If-Match+409) → 부모 OpenAPI. v1.0=클라측 stale-write(FR-CON-36) 우회.
    - **C-12**(확인·소규모) — 목록 기본/안정 정렬 계약 → 부모 OpenAPI. *(spec-v1.0.19 §7.9.1 커서 rationale로 페이지네이션 방식은 명문화됨 — 정렬 파라미터 계약만 잔여.)*
    - **C-8**(선택·성능 요구 시) — Admin API 전용 성능 SLA 절 → 부모 §5(현 §5=device control-plane 전용). v1.0 저 RPS·사내라 불요.

---

## (검토) 추가 후보 — 결정 대기
- **Dentbird 연동 (A 직접 vs B GW 경유) 결정 시 부모 반영** — B(GW 경유) 채택 시 부모 SRS/OpenAPI 델타 발생 가능(target discovery self-plane API·per-clinic 자격 custody·Connector 정적 자격 주입 등). **현재는 미결**(A/B 결정·PHI 여부·Dentbird API 미확인). 추적=`references/Dentbird연동/8-13-Thomas.md`. **결정+확인 후 정식 백로그 항목으로 승격**. *(아직 백로그 아님 — 조건부 후보.)*
