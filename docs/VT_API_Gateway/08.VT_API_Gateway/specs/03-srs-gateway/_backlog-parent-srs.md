# 부모 GW SRS 반영 백로그

> **목적.** 부모 GW SRS(정본 = `vt-api-gateway` repo · `docs/specs/SRS.md`)에 반영해야 하나 아직 별도 spec PR로 묶지 않은 변경을 추적한다.
>
> **원칙.** 진행 중 PR에 무관한 변경을 섞지 않는다(diff 오염·리뷰 지저분·스코프 훼손 방지).
>
> **위치 근거.** 정본 SRS는 `vt-api-gateway` repo. 이 디렉터리(`scp-architecture/…/03-srs-gateway`)는 리다이렉트 stub이라 SRS 본문은 편집하지 않고 **추적 문서(리뷰 로그·백로그)만** 둔다.

---

## 완료·PR 반영 이력 (2026-08-06)

baseline `spec-v1.0.11`(#12440·#12453). 이후 **4개 spec PR를 모두 병합**하고 **`spec-v1.0.12`(`79870c6`·2026-08-06)** 로 태깅했다 — 개별 백로그 항목(구 B-1·B-2·B-3·B-6·B-7·B-9)은 정리·삭제하고 이력만 보존한다.

| PR | 반영 내용 | 상태 |
| --- | --- | --- |
| **#12483** | (구 B-1·B-2·B-3 + B-4 안전분) §1.3 표기 범례·`aud={target}`·정보전략실 문구·동결 Roadmap 死링크 | ✅ **머지 완료** |
| **#12484** | (구 B-9) §2.3.6.3 IO Scanner 다운링크 시나리오+다이어그램 · Nemesis 반영(HMAC+timestamp·멱등 eventId·AXS 필드 ④ 위임) | ✅ **머지 완료** |
| **#12487** | (구 B-7) 멀티리전 authz §7.9.2 전역복제·§4.5.1 ZT 제거→S3+CloudFront+Entra·**Admin API 내부전용→Entra-gated 공개**(Jack 리뷰)·§2.1/§2.2 다이어그램·Appendix B #52. **`region_scope`는 리뷰 중 제거**(R1=전 리전 동일 sync·복제=gw/1.2) | ✅ **머지 완료** |
| **#12491** | (구 B-6) enroll CSR→IoT cert OpenAPI(`csr`·`iotCertificate`·`certificateId`)·§7.6.6 · Nemesis 반영(§7.2.4/§7.2.7 cert 폐기 갭·description) | ✅ **머지 완료** |

- URL: `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/{12483|12484|12487|12491}`. Nemesis 리뷰 8개 스레드 회신+resolve 완료.
- **B-5(apse4 멜버른→apse2 시드니 스윕)** — ✅ 완료(#12453·`spec-v1.0.11`). §4.5.1 내부 Admin API 도달 경로는 **#12487에서 Admin API Entra-gated 공개로 확정**(잔여=리전 전환 audience·Appendix B #52).
- **후속(스펙 세션 완료).** `spec-v1.0.12` 태그 · 구현세션 알림(v1.0.12 확정본) · IP 핀 갱신 + **T-ENR-3-6 신설**(enroll CSR→cert·게이팅·폐기) + Admin API CORS(P11 📌). → **구현세션 인계 준비 완료.**
- **잔여(gw/1.2·Appendix B #52).** 멀티리전 복제 계층(전역 seed·DynamoDB Global Table/Streams)·리전 전환 audience(§4.5.1 ⓒ). Console 반영 = Console 백로그 CB-1(부모 B-7 확정으로 트리거 met).

---

## 진행 중 백로그

### B-4(잔여). 헤더 표준 Roadmap 참조 흡수 — 헤더 배치 PR
- **범위(잔여만).** B-4의 Roadmap 死링크 안전분은 #12483에 반영됨. 남은 것은 **헤더 표준 자체를 다루는 부분**이라 헤더 배치와 함께 처리:
  - **§7.7.1** "규칙 상세는 Roadmap §5·§5.1" — 클라이언트 식별 헤더 규칙 상세를 SRS §7.7.1로 **흡수**하고 위임 문구 삭제(Roadmap §5가 Thomas 인용 헤더 표준 위치).
  - **§2.3.0** "(Roadmap §5.1)" — "GW→외부로 내부 `Vatech-*` 미전달" 규칙을 SRS 자체로 자립.
- **묶음.** 아래 참조의 **클라이언트 식별 헤더 제약(Thomas 헤더 배치)** 와 **동일 PR** — User-Agent/OS 회의 결정 후 착수.
- **출처.** 2026-08-05 사용자(Roadmap 동결).

### B-10. 문서 정합 묶음 (저위험 주석·문안 — 모아서 1 PR)
- **방침(사용자·2026-08-10).** 자잘한 주석·문안 정합은 건건 PR로 올리지 말고 **여기 모아 두었다가 한꺼번에 1개 spec PR**로 처리한다(PR 노이즈·리뷰 부담 감소). 계약/스키마 무변경·저위험만 해당(실질 변경은 별도).
- **항목:**
  - **(1) `org_mapping` 카디널리티 명시** — DBML `org_mapping` 주석에 한 줄: **희소(sparse)·clinic × target 전조합 아님·실제 연동한 (clinic,target) 쌍당 1행(연결 시 생성)·미연동 클리닉=0행·클리닉당=연동 target 수(0..N)·enrollment과 직교·org_id→clinic은 N:1 허용.** 현재 "연결 시 자가 등록"만 있어 카디널리티가 암묵(리뷰어 반복 질문 유발). 대상=DBML `org_mapping` 주석. 출처=2026-08-10 사용자 질의.
- **트리거.** 항목이 몇 개 쌓이거나 다른 저위험 문안 PR을 올릴 때 함께. 대상 repo=vt-api-gateway(DBML·SRS).

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

---

## 참조 — 별도로 추적 중인 배치 (여기서 중복 기재하지 않음)
- **클라이언트 식별 헤더 제약(Thomas 헤더 배치)** — User-Agent 변경 불가·Vatech-OS 획득 불가·Vatech-Clinic-Id 자체 설정 불가(2026-08-06 주간회의 Thomas 안건). 일부 방향 확정(Clinic-Id=EzServer nginx 주입=결정 2 / UA=자체 헤더·OS=best-effort). **SRS 반영(§7.7.1 필수성 완화+missing 헤더 정책·§7.8.5 인벤토리 튜플 부분 허용·§2.3.0 헤더 세트 표 웹 originator 케이스)은 헤더 PR로**, 위 **B-4(잔여)와 동일 PR**. 선결: 웹 프론트엔드가 GW로 직접 originate 하는지.
- **Console SRS 자체 변경** — Console 백로그 `03c-subsrs-gw-console/_backlog-console.md`(CB-1 ZTNA 제거·운영자 멀티리전 authz UX / CB-2 v1·v2 분리·기술 스택 shadcn). **#12487 확정 후 CB-1 착수.**
- **Console → 부모 계약 변경** — Console SRS Appendix B "부모 SRS 반영 대상"(C-8·C-11·C-12·C-14·C-15·C-16). Console SRS baseline 후 반영.
