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
- **현행 baseline = `spec-v1.0.19`(`f762cb2`).** v1.0.13~1.0.19 누적(위 B-10 문안 + **#12634 admin 페이지네이션 응답 array→`*Page` 엔벨로프 통일**[구현 세션 지시서 처리·A·C 코드 무변경·B=신규 Task T-ADM-11-9]·SRS §7.9.1 커서 rationale 등). 상세 진행 이력 정본 = IP `projects/vt-api-gateway/ImplementationPlan.md` §2 노트.

---

## 진행 중 백로그

### B-4(잔여). 헤더 표준 Roadmap 死링크 흡수 + 식별 헤더 missing 정책 — **PR #12638 올림(머지 대기)**
- **범위(잔여만).** B-4의 Roadmap 死링크 안전분은 #12483 반영됨. 잔여 = §7.7.1·§2.3.0이 **폐기된 Roadmap을 위임 참조(死링크)** 하는 것 + 식별 헤더 missing 정책 명문화:
  - **§7.7.1** "규칙 상세는 Roadmap §5·§5.1" — 클라이언트 식별 헤더 규칙을 SRS §7.7.1로 **흡수**하고 위임 문구 삭제([[roadmap-file-deprecated]]·죽은 문서라 死링크 정합은 회의 무관·상시 가능). + **missing 정책 명문화(아래 확정 반영).**
  - **§7.8.5** — best-effort 헤더 누락 시 인벤토리 **부분 튜플 허용**.
  - **§2.3.0** "(Roadmap §5.1)" — "GW→외부로 내부 `Vatech-*` 미전달" 규칙을 SRS 자체로 자립.
- **✅ 헤더 취급 확정(사용자·2026-08-12).** 식별 헤더는 **best-effort(선택)** — 신뢰성 있게 설정 가능할 때만 전송, 불가 시 **생략(omit)**(허위·placeholder 값 금지):
  - **User-Agent** — 주입 불가 시 **미전송**.
  - **OS(`Vatech-OS`)** — 획득 불가 시 **미전송**.
  - **Clinic-Id** — 예외(EzServer nginx 주입=신뢰 소스라 계속 전송·결정 2).
  - GW는 누락을 **허용·degrade**(거부 금지) → §7.7.1 필수성 완화 + §7.8.5 부분 튜플로 명문화.
- **상태(2026-08-12).** **PR #12638**(`spec/roadmap-deref-hdr`) 올림 — '개발 Roadmap 결정' 문서 참조 **전체 제거**(§7.7.1/§2.3.0 포함·일반명사 Roadmap은 유지) + §7.7.1 필수성 **2계층**(Product·Version·Clinic-Id=하드 필수 / OS·UA=best-effort·omit) + §7.7.4 에러 정합 + §7.8.5 OS 부분 튜플·UA 원문 저장 전방 note. 머지 시 완료로 이동.
- **잔여(web-originator 스코프 gated·비차단).** §2.3.0 웹 originator 헤더 세트 표 *세부* + **UA 기반 웹 클라 인벤토리 정식화**(product/version NOT NULL 완화·UA 파싱으로 식별키 소싱). 웹이 GW로 직접 originate 하는지(§2.3.0) 확정 후. UA 원문은 이미 `client_inventory.user_agent`에 저장돼 원자료 손실 없음(파싱만 지연).
- **출처.** Roadmap 死링크=2026-08-05(Roadmap 동결) · 헤더 정책=2026-08-12 사용자.

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

### B-13. 로컬 개발 DB와 e2e DB 분리 + 운영자 시드 스크립트 — Console 로컬 실연동이 e2e에 지워진다

- **현상.** Console이 로컬에서 실 GW admin API를 붙여 쓰는데(2026-08-13 개통), **GW e2e를 한 번 돌리면 Console의 운영자 역할이 사라진다.** `test/harness/reset.ts`가 clean-slate를 위해 `operator`·`operator_role`을 포함한 **전 앱 테이블을 TRUNCATE … RESTART IDENTITY CASCADE** 하고, 로컬 개발과 e2e가 **같은 docker DB(`localhost:15432/gw`)를 공유**하기 때문이다. 증상은 Console이 `accessState=no_access`를 받아 권한 요청 화면으로 리다이렉트되는 것이다(FR-CON-02 정상 동작·데이터가 없어졌을 뿐).
- **방향(영향 없음 확인).** 반대 방향은 문제가 아니다 — 시드한 행은 e2e가 **시작할 때 truncate** 하므로 어떤 단언에도 영향을 주지 않는다(`reset.ts` 주석: "참조 시드가 없어 전 테이블을 무조건 truncate 한다"). 즉 **개발 시드 → e2e 영향 없음 / e2e → 개발 시드 소실**의 단방향이다.
- **해결안 (권장 순).**
  1. **e2e를 별도 DB로 분리** — ⭐ 가장 깨끗하다. **격리 경로가 이미 둘 다 있다.**

     | | 방식 A — 컨테이너 2개 | 방식 B — 데이터베이스 2개 |
     | --- | --- | --- |
     | 방법 | `TEST_USE_CONTAINERS=1` → `e2e-global-setup.ts`가 testcontainers로 임시 인스턴스 기동 후 `DATABASE_URL` 덮어씀 | 같은 컨테이너 안에 `gw`(개발) + `gw_test`(e2e) 두 데이터베이스 |
     | 격리 | 완벽(매 실행 새 인스턴스) | 충분 — `TRUNCATE`는 **데이터베이스 경계를 넘지 않는다** |
     | 비용 | 매 실행 컨테이너 기동 대기 | 없음(즉시) |
     | 현재 | **CI가 이미 이 모드** | 가드가 `*_test`를 **이미 허용**(`isLocalOrTestDbUrl`) |

     **로컬은 B, CI는 A**를 권한다. 컨테이너를 하나 더 띄울 이유가 없고(같은 Postgres 인스턴스 안에서 데이터베이스는 서로 완전히 격리된다), CI는 매번 깨끗한 인스턴스가 맞다. B의 절차는 3줄이다:

     ```bash
     PGPASSWORD=gwpass createdb -h localhost -p 15432 -U gw gw_test          # 1회
     DATABASE_URL=postgresql://gw:gwpass@localhost:15432/gw_test pnpm prisma:migrate:deploy
     DATABASE_URL=postgresql://gw:gwpass@localhost:15432/gw_test pnpm test:e2e
     ```

     남는 일은 **마이그레이션을 두 DB에 적용하는 절차를 어디에 둘지**(`Makefile`·`package.json` 스크립트·README) 정하는 것뿐이다. `seed-guard.ts`가 `/_test$/`를 허용하도록 이미 만들어져 있어 파괴적 작업 가드도 그대로 통과한다 — 이 구성을 염두에 둔 설계로 보인다.
  2. **멱등 운영자 시드 스크립트**(`pnpm dev:operator`) — 1과 **함께** 두는 것이 좋다. DB가 어떤 이유로든(수동 `prisma migrate reset`·볼륨 삭제) 비면 한 줄로 복구된다. 기존 `scripts/dev-device.ts`(clinic·device idempotent upsert)의 **형제**이고, `assertDestructiveDbAllowed()` 가드를 그대로 재사용한다. 필요 입력은 subject UUID·role·scope뿐이다. ⚠ `operator_role.requested_at`·`decided_at`은 timestamp가 아니라 **epoch ms(bigint)** 다(Console 세션이 처음에 `now()`로 넣어 실패).
  3. **e2e 종료 후 재시드**(사용자 최초 제안) — 동작은 하지만 1·2보다 약하다: ① `resetState`가 **테스트 사이마다** 돌아 e2e 실행 **도중 내내** 개발 데이터가 없다(수 분간 Console이 no_access) ② e2e가 중단·크래시하면 teardown이 안 돈다 ③ **테스트 하네스가 개발 편의 데이터를 쓰게 되는 결합**이 생긴다.
- **산출물 = GW README + 스크립트. SRS 변경 없음**(2026-08-13 판단·재론 불요). 근거 세 가지다. ① SRS **§3.5 Test Environment는 staging AWS 환경**(EKS·RDS·AXS sandbox·PHI 금지)을 규정할 뿐 로컬 개발 DB 토폴로지를 다루지 않고, **§3.5.2가 "단위(Jest)·E2E·부하 테스트 도구 = 구현 착수 시(LLD) 확정"으로 명시 위임**한다 — `TEST_USE_CONTAINERS`·`gw_test`·`reset.ts`가 이미 SRS 없이 만들어진 것도 같은 이유다. ② 유일한 후보 자리인 **§6.3.5 Remaining Attributes는 `그 외 None`으로 닫혀 있고** SRS 전체에 Testability라는 단어가 없다 — 게다가 품질특성 Testability는 *제품이 테스트 가능하게 설계됐는가*(관측성·결정론)를 뜻해, **개발 중 로컬 워크로드 충돌**인 이 건과 층이 다르다. ③ **운영 시스템은 무관**하다(리전 사일로 = 리전당 DB 1개, 프로덕션에 test DB가 없다) — FR·계약·데이터 모델·배포 토폴로지 어느 것도 안 바뀐다. 따라서 적을 곳은 **GW `README.md`의 로컬 실행 절**(이미 `cp .env.example .env`·`make dev-up`·admin fail-closed 안내가 있는 곳)이다.
- **소유.** **GW.** DB 스키마·`seed-guard`·`dev-device.ts` 선례가 모두 GW에 있고, Console 레포에는 Postgres 클라이언트 의존성이 아예 없다(프론트 레포에 `pg`를 넣는 건 잘못된 방향). Console은 로컬 OIDC 발급자(`pnpm dev:oidc`)까지만 소유한다.
- **트리거.** Console이 로컬 실 GW로 P2 이후 화면을 개발하는 동안 계속 겪는다 — **지금 착수 가치가 있다**. 다만 SQL 한 줄로 복구되므로 차단은 아니다.
- **출처.** 2026-08-13 Console 세션 실측(로컬 실연동 개통 중 발견) · 사용자 지시로 백로그화.

---

## 참조 — 별도로 추적 중인 배치 (여기서 중복 기재하지 않음)
- **클라이언트 식별 헤더 제약(Thomas 헤더 배치)** — User-Agent 변경 불가·Vatech-OS 획득 불가·Vatech-Clinic-Id 자체 설정 불가(2026-08-06 주간회의 Thomas 안건). **방향 확정**: Clinic-Id=EzServer nginx 주입(결정 2) / **UA·OS=best-effort — 설정·획득 불가 시 omit(2026-08-12 확정)**. SRS 반영(§7.7.1 필수성 완화+missing=omit 정책·§7.8.5 부분 튜플·§2.3.0 헤더 세트 표)은 위 **B-4(잔여)와 동일 PR로 착수 가능**(회의 대기 없음). §2.3.0 웹 originator 세트 표 세부는 웹의 GW 직접 originate 여부에 따라 달라지나 비차단(degrade).
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
- **Dentbird 연동 (A 직접 vs B GW 경유) 결정 시 부모 반영** — B(GW 경유) 채택 시 부모 SRS/OpenAPI 델타 발생 가능(target discovery self-plane API·per-clinic 자격 custody·Connector 정적 자격 주입 등). **현재는 미결**(A/B 결정·PHI 여부·Dentbird API 미확인). 추적=`references/Dentbird연동/8-13-Thomas.md`. **결정+확인 후 정식 백로그 항목(B-13)으로 승격**. *(아직 백로그 아님 — 조건부 후보.)*
