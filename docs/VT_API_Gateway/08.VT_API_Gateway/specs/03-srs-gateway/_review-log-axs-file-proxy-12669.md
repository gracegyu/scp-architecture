# ③ GW SRS — 리뷰 코멘트 추적 (AXS 파일 전송 비대칭·업로드 토큰 위임 · PR #12669)

> **작업용 문서**. 각 스레드=코멘트 원문 전체 + 우리 판단·답변·조치. **처리 완료(2026-08-13)** — 스펙/handoff 반영(`0d5b185`)·답변 10건 게시·Nemesis 9건 resolve(fixed)·Thomas 질문(84373)은 답변만(본인 resolve 대기).

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12669
- **주제**: AXS 파일 전송 = 다운로드(presigned·Blob SAS)·업로드(GW 토큰 위임·fss auth-gated) 비대칭 정정 · v1.0 AXS 연동 전체(IO Scanner 한정 폐기·originator=EzServer+CleverOne) · §2.3.4·§2.3.6.3·§4.1.4·§7.4·§7.5.1·§7.5.2 + handoff 2종
- **리뷰어**: Nemesis(v0.6.0·민진우(Thomas) 계정) · 민진우(Thomas) 본인
- **브랜치·커밋**: `spec/axs-file-proxy-auth-gated` — 원안 `5c8f4c0` → **리뷰 반영 `0d5b185`**(push 완료)
- **fetch**: 2026-08-13 · 리뷰 스레드 10건(Nemesis 라인 8 = 🔧2·💡6 · 총평 2 · Thomas 본인 질문 1)
- **상태**: **처리 완료** — Nemesis 🔧2(PUT/POST 통일)·💡6 전건 수용·반영(`0d5b185`)·답변 게시·**9건 resolve(fixed)** · Thomas 질문(84373·AXS=Azure) 답변 게시(본인 resolve 대기)

---

## 처리 절차
1. fetch — PR threads 수집(`az devops invoke --area git --resource pullRequestThreads … pullRequestId=12669`).
2. 각 스레드를 `## C-NN · <file:line> · [thread <id>]`로 기록(원문 전체 인용).
3. 우리 판단 + 답변 초안 → 사용자 확인 후 게시.
4. 조치·반영은 `spec/axs-file-proxy-auth-gated`에 커밋·push.

> 답변 스타일: 서술문(개조식 지양)·내부 라벨(C-NN)은 로그 내부용(게시 안 함)·대외 이모지 없음·`#숫자` 오링크 회피·호칭 "님" 금지.

---

## 코멘트

### C-01 · docs/specs/SRS.md:856 · [thread 84364] · 🔧 수정 필요 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msqzyyxcc8]**
  > From Nemesis(v0.6.0, 🆔msqzyyxcc8),
  > **🔧 수정 필요**
  >
  > 업로드 바이트 전송의 HTTP 메서드가 문서 내부에서 상충한다. §2.3.4 "구현 계약" 비교표(856행)와 데이터 경로 다이어그램·§4.1.4 표(1451·1460행)·§7.4(2196행)는 모두 **`직접 PUT`**으로 기술하지만, 정작 실제 호출을 명시한 §2.3.4 시퀀스 3(878행 `EZ->>FSS: POST {storageUrl}/file`)과 §7.5.2 구현 계약(2241행 `표준 POST {storageUrl}/file`)은 **`POST`**로 명시한다. 이 문서는 EzServer(③-P-EZ) 구현의 정본이므로 PUT/POST 혼재는 실제 업로드 호출을 잘못 구현하게 만들 수 있다. 실 엔드포인트가 `POST {storageUrl}/file`라면 산문의 "직접 PUT" 표현을 모두 "직접 POST(=`POST {storageUrl}/file`)"로 통일해야 한다.

- **[전규현(우리)·답변 초안]**
  > 지적이 맞습니다. 실제 업로드 엔드포인트는 POST {storageUrl}/file이고(AXS Postman·실측 확인), 산문·비교표·§4.1.4·§7.4의 "직접 PUT" 표현이 시퀀스·§7.5.2의 POST와 어긋났습니다. 문서 전체를 실 엔드포인트인 "직접 POST(POST {storageUrl}/file)"로 통일했습니다.

- **조치(초안):** §2.3.4 비교표·산문·§4.1.4 표/데이터플레인 다이어그램·§7.4의 "직접 PUT"·"직접 PUT" → "직접 POST(`POST {storageUrl}/file`)"로 통일.
- **반영:** (미반영·사용자 확인 후)
- **상태:** 초안

### C-02 · docs/handoff/axs-file-transfer-ezserver.md:20 · [thread 84365] · 🔧 수정 필요 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msqzyyxcc8]**
  > From Nemesis(v0.6.0, 🆔msqzyyxcc8),
  > **🔧 수정 필요**
  >
  > 같은 PUT/POST 상충이 handoff 문서에도 있다. 비교표(20행 `EZ→AXS 직접 PUT`)와 본문 delta 1항(`표준 POST {storageUrl}/file`)이 어긋난다. EzServer 담당(Thomas)이 이 표를 근거로 구현하므로 SRS와 동일하게 메서드를 통일해야 한다.

- **[전규현(우리)·답변 초안]**
  > 같은 지적입니다. handoff도 동일하게 통일했습니다. EzServer 담당이 이 표를 근거로 구현하므로 SRS와 메서드를 일치시켜 비교표의 "직접 PUT"을 "직접 POST(POST {storageUrl}/file)"로 맞췄습니다.

- **조치(초안):** axs-file-transfer-ezserver.md 비교표·본문의 "직접 PUT" → "직접 POST(`POST {storageUrl}/file`)".
- **반영:** (미반영)
- **상태:** 초안

### C-03 · docs/specs/SRS.md:1459 · [thread 84366] · 💡 권장 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msqzyyxcc8]**
  > From Nemesis(v0.6.0, 🆔msqzyyxcc8),
  > **💡 권장**
  >
  > 데이터 경로 다이어그램에서 CleverSpace 업로드와 AXS 다운로드를 `SAS·self-auth`로 함께 묶었다. 그러나 `SAS`(Shared Access Signature)는 Azure Blob 전용 개념으로 AXS 다운로드(`storageDownloadUri`·Blob SAS)에만 해당하고, CleverSpace 스토리지는 §5 인프라 표상 S3/MinIO(presigned URL)라 SAS가 아니다. "SAS·self-auth"를 "presigned·self-auth"처럼 스토리지 중립 표현으로 바꾸면 CleverSpace를 SAS로 오인하지 않는다.

- **[전규현(우리)·답변 초안]**
  > 수용합니다. SAS는 Azure Blob 전용이라 CleverSpace(S3/MinIO presigned)를 SAS로 묶으면 오인됩니다. 공유 표현을 "presigned·self-auth"로 중립화하고, AXS 다운로드만 "Blob SAS(presigned의 일종)"로 구체화했습니다.

- **조치(초안):** §4.1.4 데이터플레인 다이어그램/표의 "SAS·self-auth"(CleverSpace/AXS 다운로드 공통) → "presigned·self-auth", AXS 다운로드는 "Blob SAS"로 별도 명시.
- **반영:** (미반영)
- **상태:** 초안

### C-04 · docs/specs/SRS.md:2247 · [thread 84367] · 💡 권장 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msqzyyxcc8]**
  > From Nemesis(v0.6.0, 🆔msqzyyxcc8),
  > **💡 권장**
  >
  > 위임 토큰 TTL을 "현행 30분"으로 고정하면서, 대용량 의료영상(CT 등) 단일 `POST {storageUrl}/file` 전송이 30분을 넘길 경우의 취급이 §7.5.2에 없다. handoff 문서는 "만료 시 create-document부터 재수행"만 언급하는데, 이는 이미 올린 대용량 바이트의 재전송을 의미할 수 있다. 세션·resumable을 AXS 계약(④)에 위임하더라도, 단일 PUT/POST가 토큰 수명을 초과할 때 resumable 재개 중 토큰 재발급이 가능한지(§Appendix B #50 열린 항목과 연결) 최소한 참조로 명시해 두는 편이 구현 리스크를 줄인다.

- **[전규현(우리)·답변 초안]**
  > 타당합니다. 대용량 단일 전송이 토큰 TTL(30분)을 넘길 때의 취급을 §7.5.2에 참조로 명시했습니다. 세션·resumable은 AXS 계약(④) 소관이며, 재개 중 새 토큰이 필요하면 create-document 재호출로 fresh 토큰을 다시 받습니다(전체 재전송이 아니라 resumable 재개는 AXS 계약이 정함). 토큰 수명 초과 전송의 resumable·재발급 세부는 ④에서 확정합니다.

- **조치(초안):** §7.5.2에 "단일 전송이 토큰 TTL을 초과하는 경우 — resumable 재개·재개 중 토큰 재취득(create-document 재호출)은 AXS 계약(④) 소관" 참조 note 추가.
- **반영:** (미반영)
- **상태:** 초안

### C-05 · docs/specs/SRS.md:876 · [thread 84375] · 💡 권장 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msr192fmc9]**
  > From Nemesis(v0.6.0, 🆔msr192fmc9),
  > **💡 권장**
  >
  > §2.3.4 시퀀스 3의 GW 내부 스텝을 `GW->>GW: 업로드 위임 토큰 발급(fresh · AXS client_credentials …)`로 적어, GW가 위임 토큰을 **발급(mint)**하는 것처럼 읽힌다. 그러나 §7.5.2(2245행)는 "발급자는 AXS이며 GW는 더 좁은 스코프·더 짧은 TTL의 토큰을 스스로 만들 수 없다 … 위임 토큰은 반드시 AXS 발급 토큰"이라고 못박는다. 시퀀스만 보고 구현하면 GW가 자체 토큰을 서명·발급하는 것으로 오해할 수 있으니, "발급"을 "AXS에서 fresh 취득" 같은 표현으로 바꿔 §7.5.2와 일치시키는 편이 안전하다.

- **[전규현(우리)·답변 초안]**
  > 수용합니다. 시퀀스 3의 "위임 토큰 발급"이 GW가 토큰을 만드는 것처럼 읽혀 §7.5.2(발급자=AXS·GW는 취득만)와 어긋났습니다. "AXS에서 fresh 취득"으로 바꿔 일치시켰습니다.

- **조치(초안):** §2.3.4 시퀀스 3 "업로드 위임 토큰 발급(fresh · AXS client_credentials)" → "업로드 위임 토큰 AXS에서 fresh 취득(client_credentials)".
- **반영:** (미반영)
- **상태:** 초안

### C-06 · docs/specs/SRS.md:983 · [thread 84376] · 💡 권장 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msr192fmc9]**
  > From Nemesis(v0.6.0, 🆔msr192fmc9),
  > **💡 권장**
  >
  > §2.3.6.3 이중 저장 방지 규칙이 `files[].id`가 자기 문서 id와 **일치하면 무조건 다운로드 skip**으로 정의돼 있는데, 같은 절(981행)이 webhook 이벤트를 `patient.file.uploaded`/**`updated`** 둘 다로 명시한다. 자기가 originate한 문서를 **Straumann 측이 이후에 수정**해 `patient.file.updated`가 오는 경우에도 `files[].id`는 자기 문서 id와 일치하므로 skip 판정되어, 외부에서 갱신된 내용을 받지 못한다(대사만 하고 최신 바이트 미반영). 판정을 id 일치뿐 아니라 이벤트 종류(uploaded vs updated)·버전/ETag까지 고려하도록 하거나, 최소한 "updated 이벤트의 갱신 반영 여부는 ③-P-EZ/④에서 확정" 정도의 단서를 남겨 두는 편이 좋다.

- **[전규현(우리)·답변 초안]**
  > 좋은 지적입니다. 자기 문서 id 일치 시 무조건 skip이면, 자기가 올린 문서를 Straumann이 이후 수정(patient.file.updated)한 경우에도 skip돼 외부 갱신을 놓칩니다. skip은 자기 업로드의 즉시 echo(첫 uploaded·이미 보유한 버전)에 한하도록 하고, 이후 외부 수정(updated·더 최신 lastModifiedAt/버전)은 id가 일치해도 fetch하도록 단서를 넣었습니다. 정확한 판정(이벤트 종류·lastModifiedAt/버전/ETag)은 ③-P-EZ/④ 소관으로 명시했습니다.

- **조치(초안):** §2.3.6.3 대사 규칙에 "skip은 자기 업로드의 즉시 echo(이미 보유 버전)에 한함 · 외부 수정(`updated`·더 최신 `lastModifiedAt`/버전)은 id 일치라도 fetch · 정확한 판정 기준=③-P-EZ/④ 확정" 단서 추가.
- **반영:** (미반영)
- **상태:** 초안

### C-07 · docs/specs/SRS.md:2221 · [thread 84377] · 💡 권장 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msr192fmc9]**
  > From Nemesis(v0.6.0, 🆔msr192fmc9),
  > **💡 권장**
  >
  > §7.5.1 전략 파생 규칙을 `profile=internal`→`internal_bypass`, `profile=external`+credential 유무→`oauth2_cc`로 기술했는데, `oauth2_cc`는 client_credentials 토큰 취득에 credential(client_id/secret)이 반드시 필요하다. "credential 유무"라는 표현은 credential이 **없는** external target도 `oauth2_cc`로 파생된다는 읽기를 허용하며, 그 경우 자격 없이 OAuth 토큰 취득을 시도해 실패한다. 의도가 "external+credential 有→oauth2_cc"라면 "유무"를 "有(존재 시)"로 정정하고, credential 없는 external target의 취급(허용 안 함/에러)을 명시하는 편이 파생 로직 구현 오류를 막는다.

- **[전규현(우리)·답변 초안]**
  > 맞습니다. "credential 유무"는 credential 없는 external도 oauth2_cc로 파생되는 오독을 허용하고, 그 경우 자격 없이 OAuth 취득을 시도해 실패합니다. "external + credential 有(존재 시) → oauth2_cc"로 정정하고, credential 없는 external target은 허용하지 않음(설정 오류·거부)을 명시했습니다.

- **조치(초안):** §7.5.1 파생 규칙 "`profile=external`+credential 유무→`oauth2_cc`" → "`profile=external` + credential 有 → `oauth2_cc`"; credential 없는 external = 허용 안 함(fail-closed·설정 오류) 명시.
- **반영:** (미반영)
- **상태:** 초안

### C-08 · docs/handoff/axs-file-transfer-ezserver.md:5 · [thread 84373] · 질문(Thomas 본인) · Active
- **[민진우(Thomas)·본인]**
  > Azure Blob SAS라고 명시되어 있는데요. AXS에서 Azure를 쓰는 곳이 있나요?

- **[전규현(우리)·답변 초안]**
  > 네, 실측(probe)으로 확인했습니다. AXS 다운로드 URL(storageDownloadUri)의 호스트가 ppr.blob.eu.axs.straumann.com 으로 Azure Blob Storage이고, 무인증 GET이 200(SAS 자체 인증)입니다. 업로드용 fss 호스트도 ppr-api-weu-fss.straumann.com 으로 Azure 리전 네이밍(weu=West Europe)입니다. 즉 AXS는 Azure 기반이며 다운로드 전달에 Azure Blob SAS를 씁니다. "Azure Blob SAS" 표기는 실측 근거에 따른 정확한 표현입니다.

- **조치(초안):** 문서 변경 없음(표기 정확). 필요 시 근거로 다운로드 호스트(`…blob…axs.straumann.com`)를 각주로 남길 수 있음 — 사용자 판단.
- **반영:** (해당 없음)
- **상태:** 초안(답변만)

### C-09 · (일반·총평) · [thread 84368] · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msqzyyxcc8]**
  > From Nemesis(v0.6.0, 🆔msqzyyxcc8, ⏱3m28s, 🔢424.8k in/8.8k out),
  > ## Code Review (Other)
  >
  > 본 PR은 코드 변경 없이 SRS 및 크로스팀 handoff 문서만 개정한 것으로, 핵심은 AXS 파일 전송을 "다운로드=presigned(Blob SAS)·업로드=GW 토큰 위임(fss auth-gated)"의 비대칭 모델로 정정하고, v1.0 AXS 연동 범위를 (IO Scanner 한정 폐기 → 업로드·다운로드·webhook·org 링크 전체)로 확대하며 originator에 CleverOne을 포함시킨 것이다. 전반적으로 §2.3.4·§2.3.6.3·§4.1.4·§7.4·§7.5.1·§7.5.2와 두 handoff 문서 간 서사·경계 설정이 일관되고 근거(2026-04-30/08-06/08-13 회의·probe 실측)도 잘 추적된다. `ConnectorStrategy` 전략 모델(`internal_bypass`/`oauth2_cc` + capability 플래그)로 ADR-11 "1행" 확장 규칙을 정밀화한 것도 적절하다.
  >
  > 가장 중요한 지적은 업로드 바이트 전송 메서드가 문서 전반에서 "PUT"(산문·표)과 "POST {storageUrl}/file"(시퀀스·구현 계약)로 혼재한다는 점이다. 이 문서가 EzServer 구현의 정본이므로 반드시 한쪽으로 통일해야 한다.
  >
  > 구조적으로 유의할 점: webhook 이중 저장 방지 로직(§2.3.6.3)이 `webhook files[].id` = `create-document documentId` 대조에 의존하는데, 두 식별자의 동일성 자체는 "④ AXS Sub-SRS·AXS OpenAPI 정본"으로 위임되어 있다. 문서가 이를 명시적으로 ④ 소관으로 인지·표기하고 있어 결함으로 보진 않으나, 실제 두 id가 동일하지 않을 경우 자기 업로드를 외부 파일로 오판해 되받거나(이중 저장) 그 반대(다운로드 누락)가 발생할 수 있으므로, ④ 착수 시 이 대응 관계를 최우선으로 확정할 필요가 있다. 사이드카 토큰(`X-Vatech-Upload-*`) 헤더명이 baseline 확정 전 draft임을 명시한 점, 토큰 마스킹·TLS 보안 규칙을 둔 점은 적절하다.
  >
  > 4 line-specific finding(s) were posted as inline comments.

- **[전규현(우리)·답변 초안]**
  > 총평 감사합니다. 핵심 지적인 업로드 메서드 혼재(PUT/POST)를 실 엔드포인트 POST({storageUrl}/file)로 문서 전반에 통일했습니다. 이중 저장 방지가 의존하는 files[].id ↔ documentId 동일성은 ④ AXS Sub-SRS/③-P-EZ 소관으로 표기돼 있으며, 지적대로 ④ 착수 시 이 대응 확정을 최우선으로 두겠습니다(자기 파일 되받기·외부 파일 누락 오판 방지). 라인 지적은 각 스레드에 개별 답변했습니다.

- **조치(초안):** C-01/C-02(메서드 통일)로 반영. 나머지 라인 지적은 각 스레드.
- **상태:** 초안

### C-10 · (일반·총평 Update 1) · [thread 84378] · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msr192fmc9]**
  > From Nemesis(v0.6.0, 🆔msr192fmc9, ⏱3m17s, 🔢368.6k in/12.2k out),
  > ## Code Review (Other) — Update 1
  >
  > 이번 증분은 코드 변경 없이 SRS 문서만 개정한 것으로, 핵심은 (1) §2.3.4에 AXS 파일 전송 다운로드·업로드 비대칭 비교표와 업로드 토큰 위임 시퀀스(시퀀스 3)를 신설하고, (2) §2.3.6.3을 "IO Scanner 다운링크"에서 "AXS 파일 다운링크 + 이중 저장 방지(reconciliation)"로 재구성했으며, (3) v1.0 범위를 "IO Scanner 한정 → AXS 연동 전체(업로드·다운로드·webhook·org 링크) + originator=EzServer+CleverOne"로 확대(2026-08-13)하고, (4) §7.5.1을 `ConnectorStrategy` 전략 모델(`internal_bypass`/`oauth2_cc` + capability, v1.0=파생·DB 컬럼 무변경)로, §7.5.2를 업로드 토큰 위임 구현 계약으로 정밀화한 것이다. 전반적으로 §2.3.4·§2.3.5·§2.3.6.3·§4.1.4·§7.4·§7.5와 범위·리전 표 간 서사가 일관되게 갱신됐고, webhook을 '다운로드 명령'이 아닌 '대사 신호'로 규정해 자기 업로드 되받기(이중 저장)를 명시적으로 차단한 설계는 적절하다. 중국 파티션·리전 배치 항목의 불릿화 등 가독성 개선도 무해하다.
  >
  > 이전 리뷰 지적의 해소 여부: 이전 must_fix였던 **업로드 바이트 전송 메서드(PUT/POST) 혼재는 이번 증분에서 해소되지 않았다.** 오히려 새로 작성된 §2.3.4 비교표(856행 "EZ→AXS 직접 PUT")·산문(862행 "직접 PUT")·§4.1.4 표/데이터플레인 다이어그램이 "직접 PUT"을 유지하는 반면, 같은 PR에서 신설된 §2.3.4 시퀀스 3(878행 `POST {storageUrl}/file`)·§7.5.2(2241행 "표준 `POST {storageUrl}/file`")는 여전히 "POST"로 명시해, 새 내용 안에서 표와 시퀀스가 서로 충돌한다. 이 문서가 EzServer 구현의 정본이므로 한쪽(POST 실 엔드포인트로 보임)으로 반드시 통일이 필요하다(증분 리뷰 규칙상 이전 미해소 지적은 라인 코멘트로 재게시하지 않으나, 재확인 차원에서 상태만 명시).
  >
  > 구조적으로 유의할 점: 이중 저장 방지 로직이 `webhook files[].id` = `create-document documentId` 대조에 의존하는데, 두 식별자의 동일성은 여전히 ④ AXS Sub-SRS·AXS OpenAPI 소관으로 위임돼 있다. 문서가 이를 명시적으로 ④/③-P-EZ 소관으로 표기하고 있어 결함으로 보진 않으나, ④ 착수 시 이 대응 관계 확정을 최우선으로 두어야 오판(자기 파일 되받기/외부 파일 다운로드 누락)을 막을 수 있다. 위임 토큰 TTL(30분)이 대용량 단일 업로드를 초과할 때의 취급이 여전히 명시되지 않은 점(이전 recommendation)도 미해소 상태로 남아 있다.
  >
  > 3 line-specific finding(s) were posted as inline comments.

- **[전규현(우리)·답변 초안]**
  > 재확인 감사합니다. 미해소로 지적된 업로드 메서드(PUT/POST)를 이번에 실 엔드포인트 POST({storageUrl}/file)로 문서 전반에 통일했습니다. 토큰 TTL 초과 대용량 전송의 취급도 §7.5.2에 resumable·재취득은 AXS 계약(④) 소관으로 참조 명시했습니다. files[].id ↔ documentId 동일성은 ④ 착수 시 최우선 확정 대상으로 두겠습니다.

- **조치(초안):** C-01(메서드 통일)·C-04(TTL 초과 참조)로 반영.
- **상태:** 초안

---

## 조치 요약 (반영 예정 · 사용자 확인 후)
- **C-01/C-02/C-09/C-10 (🔧·must-fix):** 업로드 메서드 "직접 PUT" → "직접 POST(`POST {storageUrl}/file`)" 전면 통일 — SRS §2.3.4 비교표·산문·§4.1.4·§7.4 + handoff.
- **C-03:** §4.1.4 "SAS·self-auth" → "presigned·self-auth"(중립)·AXS 다운로드만 "Blob SAS".
- **C-04:** §7.5.2 토큰 TTL 초과 시 resumable·재취득=AXS 계약(④) 참조 note.
- **C-05:** §2.3.4 시퀀스 3 "발급" → "AXS에서 fresh 취득".
- **C-06:** §2.3.6.3 대사 규칙에 updated(외부 수정) fetch 단서(판정=③-P-EZ/④).
- **C-07:** §7.5.1 "credential 유무" → "credential 有"·credential 없는 external=허용 안 함.
- **C-08:** 답변만(문서 정확·AXS=Azure Blob 실측 확인).

---

## Update 2 (2026-08-13) — 추가 스레드 2건 + C-07 verbatim 정정

### C-11 · docs/handoff/axs-file-transfer-ezserver.md:48 · [thread 84383] · 🔧 수정 필요 · **fixed**
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msr2hys0cb]**
  > 이 줄은 업로드 전용 **축소 스코프·더 짧은 TTL 토큰 발급 가능 여부**의 열린 항목을 `SRS Appendix B #50`으로 참조하는데, SRS Appendix B #50은 실제로는 **리전 마이그레이션(클리닉 재홈) 절차·툴·전용 API**(§2.3.9·§7.3.4, gw/1.2 이후)로 전혀 다른 항목이다. … 이 handoff가 안내하는 추적 번호가 잘못되어, 이 문서를 받는 Thomas(③-P-EZ)가 근거를 확인하려고 #50을 열면 무관한 리전 마이그레이션 항목에 도달한다. … (a) Appendix B에 신규 미결 항목을 추가하고 그 번호로 정정하거나, (b) 정확한 참조로 교체해야 한다.
- **[전규현·답변·게시완료]** 정확한 지적. #50은 실제로 리전 마이그레이션 항목이라 참조가 틀렸음. '축소 스코프 토큰 문의'는 재검토 결과 불필요로 정리됨(위임 모델 확립·4/30 §2-3·probe). 해당 줄을 'TTL 초과 대용량=resumable·재취득 AXS 계약(④·§7.5.2)'로 교체·잘못된 #50 제거.
- **조치·반영:** handoff line 48 교체 (`6daa159`) · **상태: fixed·resolved**

### C-12 · (일반·총평 Update 2) · [thread 84384] · **fixed**
- **[민진우(Thomas)·Nemesis v0.6.0 · 🆔msr2hys0cb]**
  > … 이전 리뷰 지적의 해소: **[해소]** 업로드 메서드 PUT/POST 혼재 · **[해소]** 위임 토큰 발급(mint)→AXS fresh 취득 · **[해소]** 이중 저장 무조건 skip→updated fetch 단서 · **[해소]** §7.5.1 credential 유무 모호성. 구조적 유의점(결함 아님): mermaid alt는 id 일치→skip/불일치→다운로드 이분만 그리나 산문이 보완. ④ 착수 시 files[].id=documentId 대응·updated 버전 판정 최우선 확정. 축소 스코프 토큰 결론 미결(라인 지적 추적 정정 필요).
- **[전규현·답변·게시완료]** 4건 해소 확인 감사. §7.5.1 credential 없는 external은 '거부'→'oauth2_cc 아님·verbatim 유지'로 재완화(C-07/84377 후속). mermaid/산문·④ 우선사항 동의. 축소 스코프 항목=C-11로 참조 정정.
- **상태: fixed·resolved**

### C-07 후속 (thread 84377) — verbatim 재정정
- Raymond 결정(2026-08-13): credential 없는 external = **거부 → verbatim passthrough 유지**(기존 7-3 계약과 정합·동작 변경 0). §7.5.1 완화(`9ed2cb2`) + 84377에 정정 후속 코멘트 게시. 구현 T-CONN-7-6(PR #12673·main `eb73264`)이 이미 verbatim이라 무영향.

## Update 2 조치 요약
- **C-11:** handoff #50 오참조 제거 → TTL 초과=④ 참조 (`6daa159`)·resolved.
- **C-12:** 총평 확인·resolved.
- **C-07 후속:** §7.5.1 verbatim 완화 (`9ed2cb2`)·84377 후속 코멘트.
- **별건(이번 PR 밖):** 구현 세션 발견 — SRS §7.6.7 "하행 MQTT=얇은 envelope"가 실제 구현(무-envelope verbatim)과 불일치. 별도 정합화 필요(추적 = 아래).
