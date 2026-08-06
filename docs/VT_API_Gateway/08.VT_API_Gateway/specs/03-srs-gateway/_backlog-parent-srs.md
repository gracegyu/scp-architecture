# 부모 GW SRS 반영 백로그

> **목적.** 부모 GW SRS(정본 = `vt-api-gateway` repo · `docs/specs/SRS.md`)에 반영해야 하나 **지금 당장 손대면 안 되는** 변경을 모아 추적한다.
>
> **원칙.** 진행 중 PR에 무관한 변경을 섞지 않는다(diff 오염·리뷰 지저분·스코프 훼손 방지). 아래 항목은 별도 spec PR로 묶어 처리한다.
>
> **2026-08-06 상태:** **#12440·#12453 병합 완료·baseline 태그 `spec-v1.0.11` 부여.** → **B-1~B-4는 트리거(#12440 병합) 충족 = 준비됨**(별도 spec PR로 묶어 처리·**사용자 확인 대기**). **B-5는 완료**(스윕·태그·핀).
>
> **위치 근거.** 정본 SRS는 `vt-api-gateway` repo. 이 디렉터리(`scp-architecture/…/03-srs-gateway`)는 리다이렉트 stub이라 SRS 본문은 편집하지 않고, **추적 문서(리뷰 로그·백로그)만** 둔다.

## 상태 범례
- **대기** — 트리거(예: #12440 병합) 전
- **준비됨** — 트리거 충족·PR 대기
- **완료** — 반영·병합

---

## 백로그 항목

### B-1. 도메인 표기 범례 추가 (`<>` vs `{}`)
- **내용.** **§1.3 Document Conventions(문서규칙)** 표기 블록(우선순위/버전/변경/시간 표기 옆)에 bullet 한 줄 추가:
  - `<...>` = **배포 시 1회 고정되는 상수**(리전·루트 도메인 — stack/환경마다 하나)
  - `{...}` = **요청 시 레지스트리로 해석되는 와일드카드 변수**(target — `*.<region>.gw.<도메인>` 와일드카드 DNS·미등록=404)
- **근거.** 지금은 관례로만 존재(명문 범례 없음)라 외부 독자가 혼동. 실제 사용은 이미 일관: `<region>` 76 / `{region}` 0, `<도메인>` 86 / `{도메인}` 0, `{target}` 22.
- **출처.** 2026-08-05 Jack(전규현) Region Directory 도메인 질문.
- **상태.** 대기 (트리거 = #12440 병합)

### B-2. 오타 통일 `<target>` → `{target}`
- **내용.** 유일하게 `<target>`로 쓴 곳(`aud=<target>`을 못박은 단명 upstream 어서션 문장·현재 ~line 1888)을 `{target}`로 통일. target은 요청/연동별 변수라 규약상 `{}`가 맞음. DNS host가 아니라 JWT `aud` claim 값 문맥이라 저위험.
- **출처.** 2026-08-05 B-1 검토 중 발견.
- **상태.** 대기 (트리거 = #12440 병합 · B-1과 동일 PR로 묶음)

### B-3. 운영 루트 도메인 결정 프로세스 문구 정정
- **내용.** SRS가 운영 루트 도메인을 **"정보전략실 도메인 위임 대기"** 로 서술한 곳(현재 ~line 1410 위임 zone note "prod=`gw.<도메인>`·정보전략실 위임 대기", ~line 1447 미확정 note "prod=정보전략실 도메인 위임 대기")을 실제 프로세스로 정정: **운영 루트 도메인은 회의에서 확정한 뒤 인프라(Jack)가 등록**한다 — 별도 조직 위임 대기가 아니다. (도메인 값 자체는 여전히 미확정·vatech.com 아님.)
- **출처.** 2026-08-05 사용자 정정.
- **상태.** 대기 (트리거 = #12440 병합 · B-1/B-2와 동일 PR로 묶음)

### B-4. Roadmap 위임 참조 제거·SRS 자기완결화 (Roadmap 문서 동결)
- **배경.** 개발 Roadmap 문서는 **더 이상 업데이트되지 않음**(2026-08-05 확인). SRS는 §1.3에서 "자기완결"을 표방하나 실제로는 규칙 상세를 Roadmap에 위임한 곳이 있어 죽은 링크가 됨.
- **대상.**
  - **§7.7.1** (현재 ~line 2247) "규칙 상세는 **Roadmap §5·§5.1**" — 클라이언트 식별 헤더 규칙 상세를 Roadmap에 위임. **Roadmap §5가 Thomas가 인용한 헤더 표준 위치.** → **SRS §7.7.1을 정본으로** 만들도록 필요한 상세를 흡수하고 위임 문구 삭제.
  - **§2.3.0** (현재 ~line 586·599·635) "(Roadmap §5.1)" — "GW→외부로 내부 `Vatech-*` 미전달" 근거를 Roadmap에 걺 → SRS 자체 규칙으로 자립.
  - **§7.6** (현재 ~line 945) "(Roadmap §3.7.1)" 역방향 이벤트 목록 위임 → ④ Sub-SRS로만.
  - **§1.5 Related Documents·§2 배경 링크** (현재 ~line 106·468·236, `https://vks.vatech.com/x/r9iSEg`) — 동결 문서 링크. 제거하거나 "(동결·이력)"로 표기.
- **출처.** 2026-08-05 사용자("Roadmap 파일 더 이상 업데이트 안 함·사용 말 것").
- **상태.** 대기 (트리거 = #12440 병합 · 헤더 관련분은 Thomas 헤더 배치와 동일 PR)

### B-5. [watch] apse4(멜버른) → apse2(시드니) 리전 교정 다운스트림 스윕
- **배경.** Jack 브랜치 `origin/docs/region-apse2-iot-core`가 v1.0 prod 리전을 **멜버른(ap-southeast-4) → 시드니(ap-southeast-2)로 교정**(사유: `ap-southeast-4`는 AWS IoT Core 미지원 · GW 엣지 MQTT=IoT Core §7.6.6). 그 브랜치는 내부 스윕 완료(apse2 8회 · 잔재는 교정 note 1줄뿐). 코드는 `config.schema.ts` 리전 라벨 예시 주석 1곳.
- **트리거.** Jack의 해당 PR이 부모 SRS `main`에 병합될 때. (그 전엔 우리 쪽 변경 금지 — `main`이 baseline.)
- **우리 아티팩트 스윕 대상.**
  - **Console SRS `03c-subsrs-gw-console/SRS.md` §2.1.1** 다이어그램 `GW 백엔드 (v1.0 · 멜버른 apse4)` → 시드니 apse2.
  - 부모 SRS 우리 편집분(#12440)에 apse4/멜버른 참조가 있으면 정합.
  - 세션 문맥/메모리의 "prod=Melbourne apse4" 갱신.
- **[해소] Console 전역 단일 유지 — 2026-08-05 Jack 구두 합의.** PR 12453 초안이 Console을 리전별(`console.<region>.gw`)로 바꿨으나, 구두 논의 결과 **전역 단일(`console.gw.<도메인>`) 유지로 합의**(Jack이 해당 변경을 되돌리는 수정 커밋 게시 예정). 근거: SPA 호스팅 위치는 기능·주권과 무관 · 보안은 Cloudflare ZT + 리전별 Admin API Entra RBAC가 집행 · CF 단일 zone이면 도메인 스코프 Access 세션+CORS로 전역 성립 · 폐쇄국은 기존 격리 존 별도 배포 예외로 처리. → **§2.3.6 리전 스위처·호스트 규약 리워크 불요**(③-C 현행 유지). #12417 유지.
- **[③-C·③-I 잔여] 전역 Console → 리전별 내부 Admin API 도달 경로 정의** — PR 12453 `4b8acca`가 Console을 전역 단일로 확정하며 §4.5.1에 미결로 남긴 항목. 전역 SPA라 운영자 브라우저가 **내부 전용** `admin.<region>.gw`(공개 route 미등록·mesh DENY)를 직접 호출 → 정의 필요:
  - ⓐ **브라우저 도달 경로** — Cloudflare ZT 뒤 노출 / 사설망·VPN / Console 오리진 경유 프록시 중 택1
  - ⓑ **CORS** — 전역 Console origin ↔ 리전별 Admin API
  - ⓒ **리전 전환 시 운영자 토큰 audience** 취급
  - + **Cloudflare ZT(엣지 접근) ↔ Entra OIDC operatorAuth(앱 authN/authz) 층 관계** 반영.
  - 소유=③-I + ③-C(§7.9·③-C Sub-SRS). **정의 전에는 Console↔Admin 경로 구축 불가**(Jack 명시). PR 병합 자체는 이 미결과 무관(설계 시점 항목).
- **거버넌스 메모.** SRS PR은 GW 스펙 소유자를 **필수 리뷰어**로 걸어 문서 전체 정합을 항상 리뷰(다인 편집의 위험=섹션 간 불일치).
- **출처.** 2026-08-05 브랜치 히스토리 검토.
- **상태.** ✅ **완료(2026-08-06)** — #12453 병합·`spec-v1.0.11` 태그·Console SRS `apse4→apse2` 스윕·부모 핀 v1.0.10→v1.0.11 완료(Console v0.13). **잔여(§4.5.1 도달 경로·ZT↔Entra 층)는 2026-08-06 주간회의 R1 결정으로 정리** → ZT **제거**·Entra only·S3+CloudFront 확정. 멀티리전 authz 반영은 **B-7(부모 GW SRS)·Console 백로그(`03c-subsrs-gw-console/_backlog-console.md` CB-1·③-C)** 로 이관. §4.5.1 내부 Admin API 도달 경로는 ZT 제거로 **재정의 필요**(B-7 미결).

### B-6. enroll 시 CSR → 인증서(IoT Core mTLS) OpenAPI 갭
- **배경.** SRS **§7.6.6**은 "enroll 시 EzServer가 키페어 생성 → **CSR 제출** → GW가 `CreateCertificateFromCsr`로 서명·반환"을 명시하나, **OpenAPI가 이를 반영 못 함** — `EnrollCompleteRequest`에 `csr` 필드 없음 · enroll/complete 202 응답에 인증서 없음(2026-08-06 Teddy(③-P-EZ) 질의로 발견).
- **방향(우리 답).** 전용 endpoint 신설이 아니라 **enroll/complete 확장** — `EnrollCompleteRequest`에 `csr` 추가 + complete 응답에 `CreateCertificateFromCsr` 서명 인증서 반환(IoT Core 접속 정보는 `GET /v1/clinics/me` enrollment config로 하달). enrollment 한 번으로 GW 인증(private_key_jwt)+IoT Core mTLS 인증서 확립.
- **선결 결정 2건(Teddy/GW 회신 대기).** ① 발급 시점 — complete(pending) 발급·active 전 IoT Core 접속·하행 수신 불가로 게이팅(권장) vs C/S 승인(active) 시 발급 · ② CSR 대상 키 = enroll 키페어(`clientPublicKey`)와 동일 vs 별도 cert 키페어.
- **대상.** OpenAPI(`EnrollCompleteRequest.csr` + complete 응답 인증서 필드) · SRS §7.2(enroll)·§7.6.6 교차참조.
- **출처.** 2026-08-06 Teddy Teams 질의(SRS §7.6.6 ↔ OpenAPI 불일치).
- **상태.** 대기 — 결정 2건 확정 후 **spec PR**(spec 세션 소유·구현 아님). v1.0 계약(MQTT 하행)이라 계약 정의 필요(구현은 P8/P9·IoT slice와 함께).

### B-7. [gw/1.2] 멀티리전 운영자 authz — 부모 GW SRS §7.9.2·DBML·§4.5.1 (R1 결정·2026-08-06)
- **결정(주간회의 8/6 R1).** ① 운영자 역할을 **모든 리전에 동일하게 sync**(리전별 재부여·리전별 첫-admin bootstrap 데드락 제거). ② **DynamoDB Global Table = sync(복제) 전용** — **GW는 DynamoDB를 직접 읽지 않고** 각 리전 로컬 스토어(`operator_role`)를 읽는다(기존 per-request 읽기 경로 유지). ③ **Zero Trust 제거** — Console 접근 통제 = **Entra only**(ZTNA/Cloudflare ZT 폐기), 호스팅 = **S3 + CloudFront**. (#12453 §4.5.1의 "S3+Cloudflare ZT·CloudFront 미사용"을 되돌림.)
- **부모 반영 대상.** **§7.9.2** — 전역 복제 모델·grant별 `regionScope`(all/특정)·admin·dev 기본 all-regions·**전역 bootstrap seed**(리전별 데드락 해소·C-14 갱신). **DBML** — `operator_role` 저장·복제 토폴로지(Global Table sync → 리전 로컬 스토어 materialize). **§4.5.1/§6.2** — Console 접근 = S3+CloudFront+Entra(ZT 제거)·내부 Admin API 도달 경로 재정의.
- **미결(설계 확정 필요).** (a) **sync 실시간성** — 리전 간 복제는 DynamoDB Global Table로 준실시간(sub-second·push). 로컬 스토어 materialize는 **DynamoDB Streams(이벤트·준실시간) 권장 / polling(지연)은 대안**. 최종 일관성(수 초)·revocation 지연 창은 bounded. (b) **ZT 제거 후 내부 Admin API 도달 경로**(§4.5.1 ⓐ) — "Entra only"는 인증만 답하고 네트워크 도달은 미정(사내망/VPN vs 공개+Entra-gated). (c) 리전 전환 토큰 audience(§4.5.1 ⓒ).
- **구현 시점 — v1.0 / gw1.2 분리 (중요·구현세션 주의).** R1 구조상 **GW 읽기 경로는 단일이든 멀티든 항상 리전 로컬 스토어**(`operator_role`·Postgres)이고, **복제 계층(DynamoDB Global Table + Streams→로컬 materialize)은 gw/1.2에 additive로 얹는다.** → **v1.0은 현행 단일 리전 구현(Postgres·로컬 읽기)을 유지하고 복제 계층을 미리 만들지 않는다**(단일 리전이라 복제 대상 0·YAGNI·operator_role은 이미 P11 구현됨). 미뤄도 GW 읽기 경로가 안 바뀌므로 **재작업이 아니라 계층 추가**(region-silo "스택 증분"과 동일 성격). **선반영 권장(저비용)**: `operator_role.regionScope` 컬럼을 **지금 스키마에 추가**(단일 리전이라 값=`all`)해 두면 gw/1.2가 **스키마 마이그레이션 0**. **금기**: v1.0을 "리전 영구 단일"로 하드코딩(리전=배포 상수 유지).
- **트리거.** **스펙(모델 정의)=지금 확정**(§7.9.2·DBML·regionScope) · **복제 계층 구현=gw/1.2**(v1.0 단일 리전이라 미발생). → 부모 spec PR(spec 세션 소유).
- **출처.** 2026-08-06 주간회의 R1(아카이브 「8/6 결정사항」).

> **③-C(Console) 반영분은 Console 백로그로 이관** — `03c-subsrs-gw-console/_backlog-console.md` **CB-1**(ZTNA 제거·운영자 멀티리전 authz UX). 이 파일은 부모 GW SRS 백로그이므로 Console 자체 변경은 두지 않는다.

### B-9. IO Scanner 연동 (AXS webhook→GW→EzServer) — GW 영향 확인 (주간회의 8/6)
- **배경(방향 반전).** 원래 계획 = **IOScanner→EzServer→GW→AXS**(갈래 A 업링크·GW가 AXS로 프록시). Straumann 협상 불발로 **AXS 원래 프로토콜 채택** = **IOScanner→AXS 직접 업로드 + AXS→GW webhook(다운)**. → GW의 스캔-데이터 역할이 **업링크 프록시(§4.1.4·§7.4) → webhook 다운링크 + 인증 fetch 중계**로 이동(둘 다 v1.0 설계·**신규 능력 여전히 불요**·GW가 업로드 병목에서 빠져 단순). ④ AXS 1차 스코프도 업링크→webhook 인제스트로 이동(아웃바운드 프록시는 다른 AXS 작업용으로 유효·기구축).
- **흐름(Straumann 제안 · AXS_docs 확인).** IOScanner → **AXS 직접** → AXS webhook(`patient.file.uploaded` 등)이 GW로 push — **`organizationId` 최상위 필드**·`data.patient.files[].storageUri`·**HMAC-SHA512 + `Signature` 헤더**·`messageId` 멱등 → GW가 **`organizationId → org_mapping → clinic → EzServer` 역조회로 MQTT 하행 분배** → EzServer 수신·저장(**신규 구현·③-P-EZ**). 스캔 파일 바이트는 AXS **presigned(`storageDownloadUri`)로 EzServer↔AXS 직접**(GW 미경유), presigned 발급 호출만 GW OAuth 프록시(§4.1.4).
- **GW 영향 = 신규 능력 불요(기존으로 수용).** 기존 **webhook 수신→org_id 역조회 분배**(§2.3.6·§7.6·"org_mapping 역조회" line 504)·**MQTT 하행**(§7.6.7)·**presigned 중계**(§7.4·§4.1.4)로 커버. 역방향 하행은 v1.0 범위(WH-06·§7.6.6).
- **확인/정합 대상(GW SRS·소소·대개 무변경).** §7.6 AXS webhook 계약이 실제와 일치하는지: `organizationId`(최상위·라우팅)·`messageId`(멱등, GW `eventId`↔ 매핑)·**HMAC-SHA512·`Signature` 헤더**(GW §7.6.2 "HMAC+timestamp" 서술과 실제 AXS 스킴 정합 확인). downlink로 EzServer에 넘길 필드(patient·org·storageUri). **상세 AXS webhook 이벤트 계약 = ④ AXS Sub-SRS** · EzServer 수신/저장 = ③-P-EZ.
- **GW SRS §2.3 시나리오 추가 (사용자 요청·확정 GW 변경).** 일반 프록시 bypass(업링크)와 **방향·데이터 흐름이 달라** IO Scanner를 **§2.3에 별도 대표 시나리오**로 추가한다: IOScanner→AXS **직접 업로드** → AXS webhook(`patient.file.uploaded`·`organizationId`·`data.patient.files[].storageUri`) → GW **org 라우팅**(org_mapping→clinic) → **MQTT 다운링크** → EzServer가 presigned(`storageDownloadUri`)로 스캔 **fetch**(인증 발급 호출=GW OAuth 프록시·바이트는 EzServer↔AXS 직접)·**저장**. **시퀀스 다이어그램 권장.** (기존 §2.3.6 webhook 분배의 IO Scanner 구체 인스턴스이나, 업링크 bypass와 대비되는 다운링크 인제스트라 별도 케이스로 명시.)
- **이월-R1 해소.** "IO Scanner↔EzServer 연동 방식"(그간 미정)은 Straumann 제안(IOScanner→AXS · EzServer는 GW webhook 하행 수신)으로 방향 확정.
- **트리거.** ④ AXS Sub-SRS 착수 시 §7.6 정합 확인(대개 무변경). 역할: 프로토콜 검토=Raymond · EzServer SRS=Thomas/Teddy.
- **출처.** 2026-08-06 주간회의 IO-Scanner 결정 + AXS_docs(webhooks·fileevents·patients.yml presigned) 분석.

---

## 참조 — 별도로 추적 중인 배치 (여기서 중복 기재하지 않음)
- **Console SRS 자체 변경** — **Console 백로그 `03c-subsrs-gw-console/_backlog-console.md`**(CB-1 등·ZTNA 제거·운영자 authz UX).
- **Console → 부모 계약 변경**(부모 반영 필요) — 상세는 **Console SRS Appendix B "부모 SRS 반영 대상"**(C-8·C-11·C-12·C-14·C-15·C-16). Console SRS baseline 후 반영.
- **클라이언트 식별 헤더 제약**(User-Agent 변경 불가·Vatech-OS 획득 불가·Vatech-Clinic-Id 자체 설정 불가) — **2026-08-06 주간회의 Thomas 안건**. 회의에서 방향 확정 후 승격(대상: §7.7.1 필수성 완화 + missing 헤더 정책 · §7.8.5 인벤토리 튜플 부분 허용 · §2.3.0 헤더 세트 표에 웹 originator 케이스 · 뿌리 표준 Roadmap §5). **선결 확정 필요**: 웹 프론트엔드가 GW로 직접 originate 하는지 여부.
