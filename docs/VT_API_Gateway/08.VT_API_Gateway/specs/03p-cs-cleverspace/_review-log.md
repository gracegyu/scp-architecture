# ③-P-CS CleverSpace GW 적응 OnePager — 리뷰 코멘트 추적 (_review-log)

> **작업용 문서**. 각 스레드=코멘트 원문 전체 + 우리 입장·처리 주체.
>
> **처리 방침(중요).** 이 OnePager는 **1차 초안**이고 **소유(완성·확정)는 CleverSpace 팀(Larry)으로 인계됨**(문서 헤더 명시 + Larry "Approve with comments·머지 진행"). 따라서:
> - **CleverSpace 실제 구현 관련 정정·상세**(v2 presigned·ObjectCreated·well-known·MinIO·범위·리전 echo·로깅·타임아웃 등)는 **Larry가 완성본에 직접 반영**한다 — 사실 정본이 CleverSpace라 GW가 추측으로 고치지 않는다.
> - **우리(GW)는 ① GW 계약 변경/확인이 필요한 항목만 처리**하고, **② PR엔 개별 답변 대신 '게시할 전체 코멘트' 1건**(맨 아래)만 올린다.
> - 아래 각 스레드의 "우리 입장"은 **동의/처리 방향 기록**이며 개별 게시하지 않는다. OnePager는 **우리가 재작성하지 않는다.**

- **PR**: https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud/pullrequest/12239 (docs/gw-adaptation-onepager → main)
- **리뷰어**: 고형용(Larry·CleverSpace 리드) · 우리=전규현(Raymond·GW)
- **판정**: Approve with comments(머지 진행 의견) · P0 3건 선결 요청
- **최종 fetch**: 2026-08-05 · thread 13건(비-system)
- **답변 스타일**: 서술문·이모지 없음·내부 라벨(C-NN) 미사용(로그 내부용만).

---

## C-01 · (총평) · [thread 81782] · P0 안내
- **[고형용(Larry) · 81782.1]**

  > **Approve with comments — 머지 진행 의견입니다.**
  >
  > 방향(GW 비발급·verbatim 중계, 발급/세션/storage = CleverSpace 소유, 리전 = 배포 상수)은 CleverSpace 현재 구조와 정합하고 되돌릴 것이 없습니다. 인계 문서로서 유효합니다.
  >
  > 다만 "CleverSpace 팀 상세로 위임" 으로 넘긴 항목 중 **3건은 위임 불가**입니다 — GW 계약이 먼저 정해지지 않으면 CleverSpace 가 상세를 쓸 수 없거나, 잘못 쓰면 데이터가 조용히 오염됩니다. §6·§7·§5 에 단 코멘트 3건(신원 전달 / device_id↔ezServerUid 매핑 / 인가 등급·행위자 신원)을 **§7 Open items 최상단에 P0 선결로** 올려주시면 좋겠습니다.
  >
  > **GW 측 확인 요청 1건**: SRS §6.2 보안표 2행의 "scope 기반 디바이스 권한" 과 §7.1.1 의 "scope v1.0 미사용·예약" 이 문면 충돌합니다. v1.0 실제 범위 확인 부탁드립니다.

- **[전규현(우리) · 답변 초안 · ↳81782.1]**

  > 승인 감사합니다. 위임 불가로 짚어주신 3건(GW→CleverSpace 신원 전달, device_id↔ezServerUid 매핑 소유, GW 경유 인가 등급·행위자 신원)을 §7 Open items 최상단에 P0 선결 항목으로 올리겠습니다. 세 건 모두 GW 계약이 선행돼야 CleverSpace가 상세를 쓸 수 있다는 지적이 맞습니다. GW 측 확인 요청(§6.2 "scope 기반 디바이스 권한" ↔ §7.1.1 "scope v1.0 미사용·예약")도 GW SRS의 문면 충돌이므로 확인해 정정하겠습니다 — v1.0은 scope 미사용이 실제 범위이고 §6.2 표현이 오해를 부르는 쪽입니다.

- 조치: (a) §7 Open items에 P0 3건 신설(신원 전달·device_id↔ezServerUid 매핑·인가 등급/행위자). (b) GW SRS §6.2 vs §7.1.1 scope 문면 충돌 별도 확인·정정(GW 트랙).
- 반영: 미반영
- 상태: Active

## C-02 · OnePager:116(§6 보안) · [thread 81785] · P0
- **[고형용(Larry) · 81785.1]**

  > **[P0] ③b hop 의 신원 전달 수단이 이 문서에 없습니다 — 현행 계약 그대로면 GW 경유 호출이 전건 401 입니다.**
  >
  > SRS §2.3.0 구간별 헤더 표는 ③b(GW→CleverSpace)의 `Authorization` 을 "내부 신뢰"로 두고, 예시 HTTP 블록에는 `Authorization` 을 아예 싣지 않았습니다. 그런데 CleverSpace 는 내부망 신뢰 모델이 아닙니다 — 모든 업로드/데이터 API 가 JWT 필수이고, **테넌트 스코프·쿼터·데이터 범위가 전부 토큰 클레임에서 나옵니다.** `Vatech-Clinic-Id` 헤더만으로는 어느 테넌트인지 확정할 수단이 현재 존재하지 않습니다(CleverSpace 에 clinic 개념 자체가 없음).
  >
  > 중요한 건 **SRS 가 이미 같은 결론을 적어뒀다**는 점입니다. §4.1.2 신뢰경계 문단이 "GW ingress 인증은 EzServer 가 정상 CleverOne 요청을 받았는지 구분하지 못한다 … **target 자신의 인증·입력검증이 최종 방어선이다(GW 가 대체하지 않는다)**" 라고 명시합니다. 즉 CleverSpace 가 자기 인증을 유지하는 것이 GW 의 설계 전제이고, 정정되어야 할 쪽은 ③b 표의 "내부 신뢰" 입니다.
  >
  > **결정해야 할 것은 신뢰 앵커 하나입니다.** SRS §7.1.1 은 device 토큰 클레임에 `device_id`·`region`·`aud`·TTL 만 강제 바인딩하고 `clinic_id` 는 헤더로만 옵니다(서명에 안 묶임). `scope` 는 v1.0 미사용·예약입니다. **서명에 묶인 식별자는 `device_id` 하나뿐**입니다. 후보:
  >
  > - **(권장) GW 서명 upstream 어서션** — `aud=cleverspace`, claim 에 `device_id`(+`clinic_id`). 서명이 clinic 까지 바인딩하고 `aud` 로 confused-deputy 를 피합니다(SRS 자신이 §7.1.4 Entra 항에서 같은 위험을 지적하며 `aud` 검증을 요구). GW 는 이미 RS256+`kid` 보유.
  > - **(차선) device 토큰 verbatim 보존** — GW 작업이 거의 0. 단 `clinic_id` 가 서명에 없어 결국 `device_id` 만 신뢰 가능 → 신원 해석을 device 기준으로 설계해야 함.
  > - mesh mTLS 는 단독 불충분(전달된 clinicId 진위는 여전히 GW 신뢰 의존), defense-in-depth 로 병행 권장.
  >
  > **어느 쪽이든 GW JWKS 공개가 필요하고, 이건 v1.0 계약에 없습니다.** §7.1.1 은 "v1.0 은 JWKS 엔드포인트를 두지 않는다(소비자 부재)" 라 하고 gw/1.2 예약으로 남겼는데, **CleverSpace GW Guard 가 정확히 그 '외부 검증자'** 이므로 전제가 깨집니다. 예약분의 승격 + **OpenAPI spec-change/CCB 리드타임**을 일정에 반영해 주세요.

- **[전규현(우리) · 답변 초안 · ↳81785.1]**

  > 정확한 지적이고 수용합니다. ③b를 "내부 신뢰"로 둔 것은 CleverSpace가 JWT 필수이고 테넌트 스코프·쿼터가 토큰 클레임에서 나온다는 실제 구조와 맞지 않으며, `Vatech-Clinic-Id`만으로는 테넌트를 확정할 수 없습니다. 말씀대로 SRS §4.1.2가 "target 자신의 인증이 최종 방어선"이라고 이미 규정하므로, 정정 대상은 ③b의 "내부 신뢰" 쪽입니다.
  >
  > 신뢰 앵커는 서명에 묶인 `device_id` 하나라는 점에 동의하며, 권장하신 **GW 서명 upstream 어서션(`aud=cleverspace`·claim에 `device_id`+`clinic_id`)** 을 1안으로 검토하겠습니다(confused-deputy를 `aud`로 차단하는 것이 §7.1.4 취지와도 정합). 다만 어느 안이든 **GW JWKS 공개**가 필요하고 v1.0 계약엔 없으므로, §7.1.1 JWKS 예약분 승격 + **OpenAPI spec-change/CCB 리드타임**을 일정에 반영하겠습니다. 이 건을 §7 Open items P0로 올리고, ③b 신원 전달 방식을 GW 트랙에서 확정해 회신하겠습니다.

- 조치: (a) OnePager §6/§4에 "③b 신원 전달=미정(P0)·CleverSpace 자기 인증 유지가 GW 전제(§4.1.2)" 명시. (b) §7 Open items P0. (c) GW 트랙: 신뢰 앵커안(GW 서명 upstream 어서션 vs device 토큰 verbatim) 결정 + JWKS 예약분 승격 spec-change/CCB.
- 반영: 미반영
- 상태: Active

## C-03 · OnePager:128(§7 Open items) · [thread 81786] · P0
- **[고형용(Larry) · 81786.1]**

  > **[P0] Open items 에 P0 2건을 선결 항목으로 올려주세요. 지금 목록은 전부 "상세" 성격이라, 정작 선행 계약이 빠져 있습니다.**
  >
  > **(1) GW→CleverSpace 신원 전달 = 미정** — §6 에 단 코멘트 참조. presigned 상세보다 **먼저** 닫아야 합니다.
  >
  > **(2) GW `device_id` ↔ OneID `ezServerUid` 1:1 매핑 — 소유자 미정**
  >
  > CleverSpace 의 `patient` 테이블은 `(ezserverUid, chartNo)` 유니크 키를 씁니다. 그리고 clinic ↔ EzServer 는 **1:N** 입니다. 따라서
  >
  > - GW 가 clinic 만 주고 CleverSpace 가 EzServer 를 임의로 고르면 → 같은 chartNo 환자가 EzServer 별로 갈리거나 서로 다른 환자가 **유니크 키 충돌** → 조용한 데이터 오염, 사후 복구 곤란
  > - GW `device_id` 를 그대로 `ezserverUid` 로 쓰면 → 전환 전후로 같은 EzServer 가 다른 키를 갖게 되어 **기존 환자 레코드 분기**. 반드시 **OneID 가 발급한 기존 값**으로 해석되어야 합니다.
  >
  > **이 매핑을 GW 에 요구하는 게 아닙니다** — SRS §7.1.4 가 "OneID 는 GW 와 무관하다(인증에도 라우팅에도 쓰지 않는다)" 로 선을 그었으므로 GW 는 OneID 식별자를 의도적으로 모르는 게 맞습니다. 다만 **매핑의 소유자·등록 시점·조회 수단이 어디인지**를 이 문서가 정해야 CleverSpace 가 상세를 쓸 수 있습니다.
  >
  > 권장: `device_id → (tenantUid, ezServerUid)` 를 **CleverSpace 또는 OneID 등록 레코드**가 보유, EzServer 프로비저닝 때 1회 등록(**GW enrollment 계약 변경 불요**), `clinic_id` 는 교차 검증용으로만 사용. 이러면 (1)의 앵커와 맞물려 **P0 2건이 하나로 닫힙니다** — 서명된 `device_id` 하나만 신뢰하면 나머지가 결정됩니다.
  >
  > 함께 명시 필요: **EzServer 유효성 권위 이원화.** 현재 EzServer 의 실체는 OneID 가 보증하는데(토큰 교환이 OneID 조회를 경유), GW 경로는 이 교환을 건너뛰고 GW device 레지스트리가 그 자리를 대신합니다. OneID 에서 해지된 EzServer 가 GW 에서 유효할 수 있으므로 **권위·해지 전파 경로**를 정해야 합니다.

- **[전규현(우리) · 답변 초안 · ↳81786.1]**

  > 두 건 모두 P0로 올리겠습니다. (2) device_id↔ezServerUid 매핑은 `(ezserverUid, chartNo)` 유니크 키 + clinic↔EzServer 1:N 구조상 임의 선택이 유니크 키 충돌·환자 레코드 분기를 부른다는 지적이 정확합니다. 매핑을 GW에 요구하지 않는다는 것도 맞습니다 — SRS §7.1.4가 "OneID는 GW와 무관"으로 못박았으므로 GW는 OneID 식별자를 모르는 것이 설계 의도입니다. 권장하신 대로 `device_id → (tenantUid, ezServerUid)`를 CleverSpace/OneID 등록 레코드가 보유하고 EzServer 프로비저닝 때 1회 등록, `clinic_id`는 교차검증용으로 두는 방향을 문서에 명시하겠습니다(GW enrollment 계약 변경 없음). 이러면 (1) 신뢰 앵커와 맞물려 서명된 `device_id` 하나로 나머지가 결정되어 두 P0가 함께 닫힙니다. EzServer 유효성 권위 이원화(OneID 보증 ↔ GW device 레지스트리·해지 전파 경로)도 Open item으로 함께 명시하겠습니다.

- 조치: §7 Open items P0 (2): device_id↔ezServerUid 매핑 소유=CleverSpace/OneID 등록 레코드·1회 등록·clinic_id 교차검증 + EzServer 유효성 권위/해지 전파.
- 반영: 미반영
- 상태: Active

## C-04 · OnePager:108(§5 인증·게이트) · [thread 81787] · P0
- **[고형용(Larry) · 81787.1]**

  > **[P0] "GW 경유 트래픽의 인가(authz) 등급" 이 계약 표에 없습니다.**
  >
  > SRS 를 확인한 결과 v1.0 GW 인가는 의도적으로 coarse 합니다 — 토큰 `scope` 미사용(§7.1.1), PDP 는 앱 내부 모듈(OPA 는 gw/1.1+), policy 는 clinic→global 만 평가하며 실사용 범위는 "이 device/clinic 이 target 을 쓸 수 있다" 수준(§7.5.3). **CleverSpace 리소스 권한을 대체할 의도가 없다는 게 명확합니다.**
  >
  > 이건 좋은 소식이고 충돌도 없습니다. 다만 **문서에 이 문장이 없어서 "GW 가 인가까지 해준다"는 오해 여지**가 있습니다. 이 행 또는 §6 에 한 줄 넣어주세요:
  >
  > > "GW v1.0 인가는 coarse(target 도달 허용) 이며 **CleverSpace 리소스 권한을 대체하지 않는다.** 인가 권위는 CleverSpace."
  >
  > 덧붙여 **gw/1.1+ 표류 리스크**도 지금 못 박아두는 게 좋습니다. §7.5.3 이 endpoint·scope 세분화를 예고하는데, 그때 GW policy 에 CleverSpace endpoint allowlist 가 수기로 생기면 우리가 엔드포인트를 추가·폐기해도 GW 는 모릅니다(정상 요청 차단 / 폐기 경로 계속 허용). → "GW 가 endpoint 단위 정책을 켤 경우 **CleverSpace OpenAPI 를 소스로 자동 생성**, 수기 목록 금지" 를 명시.
  >
  > 마지막으로 **행위자(member) 신원**이 계약에서 빠져 있습니다. GW hop 은 device/clinic 만 알고(`Vatech-*` = 제품·버전·OS·clinic) member 식별자가 없습니다. 현재 업로드는 body 의 `requestMemberEmail`(토큰 미대조 클라이언트 입력)로 감사 로그의 행위자를 채웁니다 → GW 시대에도 PHI 접근 기록의 행위자 귀속이 클라이언트 입력에 의존합니다. Open item 으로 추가하고 선택지를 적어주세요: ① 현행 유지(한계 명시) ② `Vatech-*` 에 member 추가(GW 계약 변경·범위 큼) ③ **대리 업로드의 행위자를 "EzServer" 로 기록하고 member 는 참고값으로 강등**(③이 가장 정직하고 컴플라이언스 답변 가능).

- **[전규현(우리) · 답변 초안 · ↳81787.1]**

  > 동의합니다. v1.0 GW 인가가 coarse(scope 미사용·PDP 앱 내부·policy는 "이 device/clinic이 target 도달 가능" 수준)이고 CleverSpace 리소스 권한을 대체하지 않는다는 점을 §5 계약표(및 §6)에 명시하겠습니다 — "인가 권위는 CleverSpace"를 한 줄로 못박겠습니다. gw/1.1+에서 endpoint 정책을 켤 경우 **CleverSpace OpenAPI를 소스로 자동 생성하고 수기 allowlist를 두지 않는다**는 원칙도 함께 넣겠습니다(수기 목록이 엔드포인트 추가/폐기와 표류하는 위험 방지). 행위자(member) 신원은 Open item으로 추가하고 세 선택지(①현행 유지·한계 명시 ②`Vatech-*`에 member 추가 ③대리 업로드 행위자=EzServer·member는 참고값 강등)를 적겠습니다 — 컴플라이언스 정직성 측면에서 ③을 유력안으로 봅니다.

- 조치: §5/§6에 "GW v1.0 인가=coarse·CleverSpace 권한 미대체·인가 권위=CleverSpace" + "gw/1.1+ endpoint 정책은 CleverSpace OpenAPI 소스 자동생성·수기 금지". §7 Open item: 행위자(member) 신원 3선택지(③ 유력).
- 반영: 미반영
- 상태: Active

## C-05 · OnePager:72(CS-2) · [thread 81788] · 정정
- **[고형용(Larry) · 81788.1]**

  > **[정정] "presigned 발급 API 신규" 는 절반만 맞습니다 — 발급 API 자체는 운영 중이고, 진짜 신규는 업로드 세션입니다. 그리고 기준 경로는 v2(S3) 하나입니다.**
  >
  > **(1) 기준 경로 = v2(S3) 단일.** 업로드용 CloudFront presigned(v1)는 **CloudFront + S3 업로드 비용이 이중 청구되는 구조**라 사용하지 않는 방향이 확정돼 있습니다. GW 경유 업로드 발급은 **v2 S3 presigned PUT 기준**으로 잡아주세요. v1 은 델타 대상이 아니라 **EOS 대상**입니다. (v1 의 미사용 결정이 CleverSpace OpenAPI 에 표기돼 있지 않아 정본을 읽으면 v1/v2 가 동등해 보이는 문제는 **우리 쪽에서 Swagger 표기로 처리**하겠습니다.)
  >
  > **(2) 발급 API 는 이미 있습니다** — `POST /api/v2/organization-data/upload/presigned-url`(S3 presigned PUT) 외에 파일 GET 용 2개(`organization-data/files/presigned-url`·`shared-data/files/presigned-url`)가 운영 중입니다. 따라서 CS-2 는 "API 전체 신규" 가 아니라 **"기존 v2 발급 API + 델타 6종"** 입니다.
  >
  > **(3) 그중 업로드 세션은 진짜 신규 개발이 맞습니다.** CleverSpace 에 `session → commit/close` 형태가 있긴 하지만 그건 **CT 조회 횟수 쿼터를 계량하는 뷰 세션**이라, 업로드 세션과 도메인·수명주기·실패 모드가 전부 다릅니다. 상태 전이 이름이 비슷할 뿐 로직 재사용 근거가 아니므로 **업로드 세션은 백지 설계로 잡습니다** — 6개 델타 중 가장 큰 항목입니다.
  >
  > | 문서 전제 | 현재(v2 기준) | 델타 |
  > |---|---|---|
  > | `start`/`commit` 세션 리소스 | 업로드용 세션 **없음**. 발급 시 s3Key 반환 + 일일 업로드 바이트 예약(TTL 300s) → 업무 API 호출로 완료 | **전부 신설**(가장 큰 항목) |
  > | resumable/multipart | 클라이언트 경로는 단일 PUT 만(multipart 는 서버 워커 내부 전용) | 발급 API 로서는 미구현 |
  > | presigned TTL | 서명 만료와 쿼터 예약 만료가 **같은 상수 300s 에 묶임** | GW hop 얹히면 둘을 분리해 재산정 |
  > | 크기·개수 한도 | 1GB / 10개, 단일 PUT 전제 | CT 대용량을 resumable 없이 유지할지 결정 |
  > | `Idempotency-Key` | HTTP 멱등 계층 없음(MQ 이벤트 멱등만) | 발급·commit 양쪽 신설 |
  > | ETag 검증 | commit 시 크기>0 만 확인 | ETag 대조 신설 |
  > | 완료처리 = 콜백 + ObjectCreated | ObjectCreated/SQS/SNS **코드 0건** | 53줄·74줄 코멘트 참조 |
  >
  > **요청**: ① 표제를 "**기존 v2(S3) 발급 API + 델타 6종**" 으로 정정하되 **업로드 세션은 신규 개발**임을 명시(이 부분은 문서 표현이 맞습니다) ② **v1(CloudFront)은 이중 청구로 미사용 확정** → GW 경유 업로드 기준 경로에서 제외 ③ **resumable 도입 여부**와 **완료처리 모델**은 CleverOne/EzServer 클라이언트 계약에 영향이 있으므로 상세 위임이 아니라 **§7 결정 항목**으로.

- **[전규현(우리) · 답변 초안 · ↳81788.1]**

  > 정정 수용합니다. CS-2 표제를 "presigned 발급 API 신규"에서 **"기존 v2(S3) 발급 API + 델타 6종"** 으로 고치고, 그중 업로드 세션(`start→commit`)만 신규 개발임을 명시하겠습니다(뷰 세션과 도메인·수명주기가 달라 재사용 근거 아님). 기준 경로는 **v2(S3) presigned PUT 단일**로 고정하고 v1(CloudFront)은 이중 청구로 미사용·EOS 대상임을 CS-2/CS-4에 명시하겠습니다. resumable 도입 여부와 완료처리 모델은 클라이언트(CleverOne/EzServer) 계약에 영향이 있으므로 상세 위임이 아니라 §7 결정 항목으로 올리겠습니다. 델타 6종(세션·resumable·TTL 분리·크기한도·Idempotency-Key·ETag)의 상세는 CleverSpace OpenAPI를 정본으로 두겠습니다.

- 조치: CS-2 표제 정정("기존 v2 + 델타 6종")·업로드 세션=신규 명시·v1 미사용/EOS·resumable/완료처리=§7 결정 항목. presigned TTL을 쿼터 예약과 분리(GW hop) 언급.
- 반영: 미반영
- 상태: Active

## C-06 · OnePager:53(§4 다이어그램) · [thread 81789] · 정정
- **[고형용(Larry) · 81789.1]**

  > **[정정] "ObjectCreated 연계" 는 현재 CleverSpace 구현이 아닙니다.** (74줄도 동일)
  >
  > 코드베이스에 `ObjectCreated`/SQS/SNS 가 **0건**입니다. 현재 완료처리는 ① 클라이언트의 명시적 업무 API 호출 ② RabbitMQ 잡 ③ 보정 스케줄러 구조입니다. 시퀀스 다이어그램이 현재 사실로 읽히면 GW·EzServer 쪽에서 잘못된 전제를 세웁니다.
  >
  > "(신설 검토)" 표기를 붙이고, **완료처리 모델(명시 commit vs storage 이벤트)** 을 결정 항목으로 올려주세요 — 어느 쪽이냐에 따라 EzServer 의 commit 호출 여부가 달라집니다.

- **[전규현(우리) · 답변 초안 · ↳81789.1]**

  > 정정 수용합니다. `ObjectCreated`/SQS/SNS가 코드 0건이고 현재 완료처리가 명시 업무 API 호출 + RabbitMQ 잡 + 보정 스케줄러 구조라는 점을 반영해, §4 다이어그램(53줄)과 CS-2(74줄)의 "ObjectCreated 연계"를 **"(신설 검토)"** 로 표기하겠습니다. 완료처리 모델(명시 commit vs storage 이벤트)을 §7 결정 항목으로 올리겠습니다 — 이 선택이 EzServer의 commit 호출 여부를 좌우한다는 점을 함께 적겠습니다.

- 조치: §4 다이어그램·CS-2에서 "ObjectCreated 연계"→"(신설 검토)". §7 결정 항목: 완료처리 모델(명시 commit vs storage 이벤트)·EzServer commit 호출 여부 연동.
- 반영: 미반영
- 상태: Active

## C-07 · OnePager:66(CS-1 well-known) · [thread 81790] · 충돌
- **[고형용(Larry) · 81790.1]**

  > **[충돌] well-known 은 경로 형태가 다르고, 더 중요한 건 내용이 CS-3 목표와 정면으로 부딪힌다는 점입니다.** (61줄 앵커 문단과 함께)
  >
  > 사실 관계: CleverSpace 는 `.well-known` 을 이미 서빙 중이지만 **env 를 URL 이 아니라 `NODE_ENV` 로 고릅니다** → 실제 경로는 `/.well-known/server-configuration.json`(env 세그먼트 없음). GW 의 `/.well-known/<env>/...` 와 형태가 다릅니다. 소비자도 전부 env 없는 경로를 씁니다(comment-server·api-client·container-app·OneID 도 동일 관례).
  >
  > **진짜 문제는 그 파일의 내용입니다** — 직접 접속 엔드포인트를 광고하는 discovery 문서입니다:
  >
  > ```json
  > { "version": "v1", "api-endpoint": "https://server.cleverspacecloud.com", ... }
  > ```
  >
  > GW 가 verbatim 중계하면 `cleverspace.<region>.gw.<도메인>/.well-known/server-configuration.json` 이 **"직접 접속하면 된다"는 주소를 되돌려줍니다.** CS-3(Direct→GW 전환)의 목표와 상충합니다.
  >
  > 제안 — 충돌이 아니라 **소유 경계 + 전환 계획**으로 3줄 정리:
  >
  > 1. CleverSpace `.well-known` = **엔드포인트 discovery**, 현행 유지(경로·스키마 변경 없음)
  > 2. GW 호환성 매트릭스 서빙본 = **GW 호스트 소유**. CleverSpace 가 주는 건 파일이 아니라 `config/compat-matrix.yaml` 에 들어갈 **값**(SRS §7.7.5 가 SSOT = GW repo 소스로 못 박음)
  > 3. **discovery 문서가 GW 호스트를 가리키게 바꾸는 시점 = 경로 B EOS 의 실질적 커트오버 스위치** — CS-3 에 명시

- **[전규현(우리) · 답변 초안 · ↳81790.1]**

  > 정확한 지적이라 반영하겠습니다. CleverSpace의 `.well-known`은 env를 `NODE_ENV`로 고르고 경로에 env 세그먼트가 없어 GW의 `/.well-known/<env>/...`와 형태가 다르고, 더 중요하게 그 파일이 직접 접속 엔드포인트를 광고하는 discovery 문서라 CS-3(Direct→GW)와 충돌한다는 점이 맞습니다. 제안하신 소유 경계 3줄을 그대로 반영하겠습니다 — (1) CleverSpace `.well-known`=엔드포인트 discovery, 현행 경로·스키마 유지 (2) GW 호환성 매트릭스 서빙본=GW 호스트 소유, CleverSpace는 파일이 아니라 `config/compat-matrix.yaml`에 들어갈 값만 제공(§7.7.5가 GW repo 소스를 SSOT로 규정) (3) discovery 문서가 GW 호스트를 가리키게 바꾸는 시점을 경로 B EOS 커트오버 스위치로 CS-3에 명시. 즉 GW의 well-known 공시와 CleverSpace의 discovery는 별개 산출물로 분리하겠습니다.

- 조치: CS-1에서 "GW well-known 공시 ↔ CleverSpace가 값 제공" 경계 명확화(CleverSpace .well-known은 별개·현행 유지). CS-3에 discovery 재지정=경로 B EOS 커트오버 스위치 명시.
- 반영: 미반영
- 상태: Active

## C-08 · OnePager:65(CS-1 오류코드) · [thread 81791] · 방향 재고
- **[고형용(Larry) · 81791.1]**

  > **[방향 재고] "오류 body 형식·코드 어휘를 GW 표준 envelope 의미론과 정합" 은 불필요하고 breaking 입니다.**
  >
  > SRS §7.7.4 가 **target 오류는 body verbatim 통과**(`Vatech-Error-Origin: target`)로 규정하므로 GW 는 CleverSpace envelope 형식을 알 필요가 없습니다. 반대로 형식을 바꾸면 `container-app`·`api-client`·EzServer 를 전부 breaking change 로 끌고 갑니다(현재 envelope = 숫자 문자열 `errorCode` 기반, 심볼릭 카탈로그는 컨트롤러에 이미 선언돼 있음).
  >
  > → "**오류코드 카탈로그 공개 + GW 표준 의미론 매핑 표 제공(형식 유지)**" 으로 축소 제안. 산출물이 훨씬 작고 실제로 유용합니다.

- **[전규현(우리) · 답변 초안 · ↳81791.1]**

  > 수용합니다. SRS §7.7.4가 target 오류 body를 verbatim 통과(`Vatech-Error-Origin: target`)로 규정하므로 GW가 CleverSpace envelope 형식을 알 필요가 없고, 형식을 바꾸면 기존 소비자(container-app·api-client·EzServer)에 breaking change가 된다는 지적이 맞습니다. CS-1의 "오류 body 형식·코드 어휘를 GW 표준 envelope 의미론과 정합"을 **"오류코드 카탈로그 공개 + GW 표준 의미론 매핑 표 제공(형식 유지)"** 으로 축소하겠습니다.

- 조치: CS-1 오류코드 항목을 "형식 유지 + 카탈로그 공개 + GW 표준 의미론 매핑 표"로 수정(형식 변경 요구 삭제).
- 반영: 미반영
- 상태: Active

## C-09 · OnePager:89(CS-3 EOS) · [thread 81792] · 범위 한정
- **[고형용(Larry) · 81792.1]**

  > **[범위 한정 필요] CleverSpace 트래픽의 상당 부분은 GW 경유가 구조적으로 불가능합니다. 이게 빠지면 EOS 일정 논의가 전제부터 틀어집니다.**
  >
  > - **브라우저 SPA**(container-app·policy-app) — 사용자 JWT 기반. device 토큰이 없어 GW edge 인증(private_key_jwt)을 통과할 수 없고 CORS origin allowlist·쿠키 전제도 다름
  > - **게스트 공유 링크** — 별도 게스트 인증 코드 플로우 + `share-guest` 토큰 타입. 무인 디바이스 모델과 무관
  > - **presigned data plane** — 애초에 GW 미경유(설계상 정상)
  > - **comment-server** — 별도 서비스(yjs 실시간). GW 프록시의 WebSocket upgrade 처리 언급이 SRS 에 없음
  > - **바이트 스트리밍 다운로드** — 공유 케이스 zip 다운로드가 API 서버를 통해 바이트를 흘립니다. GW 경유 대상이 되면 "GW 는 바이트를 경유하지 않는다"는 전제가 깨지고 §7.5.4 timeout 에도 걸림
  >
  > → CS-3 범위를 "**EzServer/CleverOne 발 device 인증 API 트래픽**" 으로 한정하고, 위 5종은 **EOS 대상 제외**로 못 박아주세요.

- **[전규현(우리) · 답변 초안 · ↳81792.1]**

  > 동의합니다. CleverSpace 트래픽 중 브라우저 SPA(사용자 JWT·device 토큰 없음), 게스트 공유 링크(`share-guest` 토큰), presigned data plane(설계상 GW 미경유), comment-server(WebSocket 실시간), 바이트 스트리밍 다운로드는 GW edge(device private_key_jwt)·"바이트 미경유"·§7.5.4 timeout 전제상 GW 경유가 구조적으로 불가능하다는 지적이 맞습니다. CS-3 범위를 **"EzServer/CleverOne 발 device 인증 API 트래픽"** 으로 한정하고 위 5종을 EOS 대상 제외로 §2 비범위·CS-3에 명시하겠습니다 — 이래야 경로 B EOS 일정 논의가 올바른 전제 위에 섭니다.

- 조치: §2 비범위·CS-3에 "CS-3 범위=EzServer/CleverOne 발 device 인증 API 트래픽" 한정 + 5종(브라우저 SPA·게스트 링크·presigned data plane·comment-server WS·스트리밍 다운로드) EOS 제외 명시.
- 반영: 미반영
- 상태: Active

## C-10 · OnePager:76(CS-2 리전) · [thread 81793] · 방향 수정
- **[고형용(Larry) · 81793.1]**

  > **[방향 수정] 발급 요청단 리전 파라미터는 불필요하고 오히려 위험합니다 — echo + guardrail 로 닫는 걸 제안합니다.** (101줄·123줄 Open item 과 함께)
  >
  > CleverSpace 는 배포당 단일 리전·단일 버킷 세트이고, GW 도 §7.3.1 에서 region = 배포 상수("런타임 리전 해석은 없다")입니다. `cleverspace.<region>.gw.<도메인>` 이 그 리전 배포로 라우팅하므로 **리전은 이미 목적지로 결정돼 있습니다.** 여기에 요청 body/헤더의 리전 파라미터를 넣으면 "요청이 자기 리전 밖 storage 를 지정할 수 있는" 경로를 새로 만드는 셈이고, 우리는 그 능력을 의도적으로 갖고 있지 않습니다.
  >
  > 제안:
  >
  > 1. 발급 요청에 리전 파라미터를 **넣지 않는다**
  > 2. CleverSpace 는 자기 배포 리전을 **응답에 echo**(예 `region: "apse2"`)
  > 3. GW 는 §7.3.3 이 이미 허용한 **guardrail**(응답 리전/호스트가 이 리전과 다르면 거부)로 검증
  >
  > 계약은 CleverSpace 신규 필드 1개로 끝나고, 주권은 라우팅 위상이 보장하며 검증은 GW 가 합니다. **보너스**: device 토큰 클레임에 `region` 이 이미 있으므로(§7.1.1), CleverSpace 쪽 Guard 가 이를 자기 배포 리전과 대조하면 같은 guardrail 을 공짜로 얻습니다 — 리전 파라미터 신설이 불필요해지는 또 하나의 근거입니다.

- **[전규현(우리) · 답변 초안 · ↳81793.1]**

  > 수용합니다. CleverSpace가 배포당 단일 리전·단일 버킷이고 GW도 §7.3.1에서 리전=배포 상수(런타임 리전 해석 없음)이므로, `cleverspace.<region>.gw.<도메인>` 라우팅이 이미 리전을 목적지로 결정합니다. 발급 요청에 리전 파라미터를 넣으면 자기 리전 밖 storage를 지정할 수 있는 경로를 새로 만드는 셈이라는 지적이 맞습니다. 제안하신 **echo + guardrail** 로 바꾸겠습니다 — (1) 발급 요청에 리전 파라미터 없음 (2) CleverSpace가 배포 리전을 응답에 echo (3) GW가 §7.3.3 guardrail(응답 리전이 이 리전과 다르면 거부)로 검증. device 토큰의 `region` 클레임(§7.1.1)을 CleverSpace Guard가 자기 배포 리전과 대조하는 defense-in-depth도 함께 적겠습니다. CS-2 "GW→CleverSpace 리전 전달"과 §7 Open item(리전 파라미터 형식)을 이 방향으로 정정합니다.

- 조치: CS-2 리전 준수를 "요청 파라미터 없음 + CleverSpace 응답 echo + GW §7.3.3 guardrail 검증"으로 수정. §7 Open item(리전 파라미터 형식) 삭제/대체. device 토큰 region claim 대조 note.
- 반영: 미반영
- 상태: Active

## C-11 · OnePager:98(CS-4) · [thread 81794] · 전제 정리·규모
- **[고형용(Larry) · 81794.1]**

  > **[전제 정리 + 규모 재산정]** (97줄 "리전별 storage 구축" 과 함께)
  >
  > **(1) 업로드 측은 이미 닫힙니다.** GW 를 통해 요청되는 presigned 는 **업로드용뿐**이고, 업로드용 CloudFront presigned(v1)는 **CloudFront + S3 업로드 비용이 이중 청구되는 구조**라 **사용하지 않는 방향이 확정**돼 있습니다. 대체로 구현한 **S3 presigned(v2)** 는 버킷 직결이라 §7.3.1 `sovereigntyPolicy.storage`(`regionBound=true`) 모델과 그대로 맞습니다. → CS-4 에 "**GW 경유 업로드 발급 = v2(S3) 고정, v1(CloudFront)은 이중 청구로 미사용·EOS 대상**" 을 한 줄 명시해 주세요. (v1 미사용 결정이 CleverSpace OpenAPI 에 표기돼 있지 않아 정본을 읽으면 v1/v2 가 동등해 보이는 문제는 **우리 쪽에서 표기 처리**하겠습니다.)
  >
  > **(2) View/Download 는 CloudFront 유지**(다운로드 속도 이점). PHI 바이트가 리전 밖 엣지를 경유·캐시하므로 "PHI 는 리전 밖 미이동" 과의 관계 판단은 필요하지만, 이 경로는 브라우저 SPA·게스트 트래픽이라 89줄 코멘트에서 EOS 제외로 한정한 범위와 겹칩니다 → **GW 적응과 분리된 CleverSpace 트랙**으로 표기해 주세요. GW 일정을 붙잡지 않습니다.
  >
  > **(3) MinIO 는 "동일 계약 충족" 한 줄로 처리할 규모가 아닙니다.** 코드베이스에 `minio`·`forcePathStyle` **0건**, `S3Client` 가 endpoint override 없이 생성되어 MinIO 를 가리킬 수 없고, View/Download 의 CloudFront 서명은 AWS 전용이라 대체 체계가 필요하며, lifecycle·zip 스트리밍 등 S3 기능 의존이 서비스·워커 전반에 퍼져 있습니다. → "**계약은 동일하게 유지하되 구현은 별도 트랙(storage 추상화 포트 + CDN 대체)**" 으로 수정 제안. **4단계 우선순위가 1~3단계보다 낮다는 판단에는 동의합니다.**

- **[전규현(우리) · 답변 초안 · ↳81794.1]**

  > 세 건 모두 수용합니다. (1) GW 경유 presigned는 업로드용뿐이고 v2(S3)가 §7.3.1 `sovereigntyPolicy.storage`(regionBound)와 그대로 맞으므로, CS-4에 "GW 경유 업로드 발급=v2(S3) 고정·v1(CloudFront)은 이중 청구로 미사용·EOS 대상"을 명시하겠습니다. (2) View/Download의 CloudFront 유지와 PHI 엣지 경유 판단은 브라우저 SPA·게스트 트래픽(EOS 제외 범위)과 겹치므로 **GW 적응과 분리된 CleverSpace 트랙**으로 표기해 GW 일정과 분리하겠습니다. (3) MinIO는 `minio`/`forcePathStyle` 0건·`S3Client` endpoint override 없음·CloudFront 서명 AWS 전용 등 규모가 커서 "한 줄 충족"이 아니라 **"계약 동일 유지·구현은 별도 트랙(storage 추상화 포트 + CDN 대체)"** 으로 수정하겠습니다. 4단계 우선순위가 1~3단계보다 낮다는 데 동의해 주셔서 그 기조로 유지합니다.

- 조치: CS-4를 (1) 업로드=v2 고정·v1 EOS (2) View/Download CloudFront=별도 CleverSpace 트랙(GW 분리) (3) MinIO=계약 동일·구현 별도 트랙(storage 추상화 포트+CDN 대체)로 재작성. 우선순위 낮음 유지.
- 반영: 미반영
- 상태: Active

## C-12 · OnePager:87(CS-3 로깅) · [thread 81795] · 동의
- **[고형용(Larry) · 81795.1]**

  > **[동의] 지적이 정확하고, GW 없이도 선행 가능한 항목입니다.**
  >
  > 현재 접근/서비스 로그는 `req.ip` 와 `User-Agent` 만 남기고 `Vatech-*` 파싱은 **코드 0건**, Express `trust proxy` 설정도 없습니다. GW hop 이 추가되면 `req.ip` 가 GW/ingress 를 가리켜 originator 를 식별할 수 없습니다. `Vatech-Product/Version/OS/Clinic-Id/Via` 캡처 미들웨어 + 감사로그 반영을 **1단계 선행 작업으로 확정**하겠습니다.

- **[전규현(우리) · 답변 초안 · ↳81795.1]**

  > 감사합니다. GW hop이 추가되면 `req.ip`가 GW/ingress를 가리켜 originator 식별이 안 되므로, `Vatech-Product/Version/OS/Clinic-Id/Via` 캡처 미들웨어 + 감사로그 반영이 GW 없이도 선행 가능한 1단계 작업이라는 점을 CS-3에 명시하겠습니다(`trust proxy` 설정 포함). 이 항목은 CleverSpace가 GW 일정과 무관하게 먼저 진행하는 것으로 정리합니다.

- 조치: CS-3 헤더 규약에 "Vatech-* 캡처 미들웨어+감사로그+trust proxy = GW 무관 1단계 선행 작업" 명시.
- 반영: 미반영
- 상태: Active

## C-13 · OnePager:88(CS-3 타임아웃) · [thread 81796] · 선후 관계
- **[고형용(Larry) · 81796.1]**

  > **[선후 관계 명시 요청] CleverSpace 가 지금 이 값을 채울 수 없습니다.**
  >
  > §7.5.4 의 `response_timeout_ms`≈10s / `total_deadline_ms`≤24s 불변식에 넣을 값이 필요한데, CleverSpace 에는 현재 요청 단위 타임아웃 설정도 엔드포인트별 latency SLO 도 없습니다. 값을 주려면 **GW 경유 대상 엔드포인트(89줄 코멘트에서 한정한 소수)를 먼저 확정하고 p99 를 측정**해야 합니다. 문서에 "**대상 확정 → 측정 → 값 제공**" 선후 관계를 적어주세요. 발급·commit 은 control plane 이라 10s 안에 무난할 것으로 보이나, 측정 없이 계약값을 드리는 건 피하겠습니다.

- **[전규현(우리) · 답변 초안 · ↳81796.1]**

  > 수용합니다. `response_timeout_ms`/`total_deadline_ms`(§7.5.4) 값은 요청 단위 타임아웃·엔드포인트 SLO가 아직 없어 지금 채울 수 없다는 점이 맞습니다. CS-3에 "**GW 경유 대상 엔드포인트 확정 → p99 측정 → 값 제공**"의 선후 관계를 명시하고, 그때까지는 계약값을 잠정 공란으로 두겠습니다. 발급·commit은 control plane이라 10s 내 무난할 것으로 보이나 측정 전 확정값은 넣지 않는 데 동의합니다.

- 조치: CS-3 오류·타임아웃 계약에 "대상 엔드포인트 확정→p99 측정→값 제공" 선후 관계 명시·잠정 공란.
- 반영: 미반영
- 상태: Active

---

## 처리 구분

### A. Larry(CleverSpace)가 완성본에 직접 반영 — 우리는 동의만
CleverSpace 실제 구현 정본이라 Larry 소유. C-05(presigned v2+델타6·업로드 세션 신규) · C-06(ObjectCreated 아님→신설 검토·완료처리 모델 결정) · C-07(well-known 소유 경계·discovery 재지정=경로B EOS) · C-08(오류 형식 유지·카탈로그+매핑 표) · C-09(CS-3 범위 한정·5종 EOS 제외) · C-10(리전 echo+guardrail) · C-11(업로드 v2·View/MinIO 별도 트랙) · C-12(로깅 1단계 선행) · C-13(타임아웃 측정 선후).

### B. GW가 처리 (변경/확인 필요)
| # | 항목 | GW 변경? | 처리 |
| --- | --- | --- | --- |
| C-02 | **③b hop 신원 전달** — "내부 신뢰" 정정 + 신뢰 앵커(GW 서명 upstream 어서션 vs device 토큰 verbatim) + **GW JWKS 공개(v1.0 미도입) 승격** | **예 — 실질 변경(GW SRS §7.1.1 + OpenAPI)·spec-change/CCB·결정 필요** | GW 트랙: 앵커안 결정 → spec-change PR → CCB. 리드타임 일정 반영 |
| C-01 | GW SRS **§6.2 "scope 기반 디바이스 권한" ↔ §7.1.1 "scope v1.0 미사용"** 문면 충돌 | **예 — 작은 GW SRS 정정**(v1.0=scope 미사용이 맞음) | GW SRS 정정(작은 spec PR) |
| C-04 | GW v1.0 인가=coarse·CleverSpace 권한 미대체 문장 · gw/1.1+ endpoint 정책=CleverSpace OpenAPI 소스 자동생성·수기 금지 · 행위자(member) 신원 선택지 | **아니오(문서 반영은 Larry)** — GW는 **확정 문구만 제공** | 문구 제공, 반영은 Larry |
| C-03 | device_id↔ezServerUid 매핑 | **아니오** — "GW enrollment 계약 변경 불요" 확인만(§7.1.4 OneID GW 무관) | 확인 답변, 소유·등록 시점은 CleverSpace/OneID |

**→ 진짜 GW 변경 = C-02(③b 인증·JWKS 승격·spec-change·결정 필요) + C-01(SRS scope 문면·작은 정정) 둘뿐. 나머지는 Larry 반영 또는 GW 답변만.**

---

## 게시한 전체 코멘트 (PR #12239 · 통합 답변) — **게시완료 · thread 83069 · 2026-08-05**

> 서술문·이모지 없음·내부 라벨 없음. 개별 스레드엔 이 코멘트로 갈음.

```
Larry님, 꼼꼼한 리뷰 감사합니다. 방향에 동의해 주셨으니(Approve with comments) 이 초안은 그대로 머지하고, 문서 소유를 CleverSpace 팀으로 인계하는 것으로 진행하겠습니다.

이 OnePager는 GW가 계약을 추출한 1차 초안이고 완성·확정 소유는 CleverSpace 팀입니다(문서 헤더에 명시). 그래서 CleverSpace 실제 구현에 관한 정정·상세는 Larry님이 완성본에 직접 반영해 주시면 됩니다 — 사실 관계의 정본이 CleverSpace 쪽이라 GW가 추측으로 고치지 않는 것이 맞다고 봅니다. 지적해 주신 내용은 모두 동의합니다. presigned는 기존 v2(S3) 발급 API에 델타 6종이고 업로드 세션만 신규이며 v1(CloudFront)은 이중 청구로 미사용·EOS라는 점, 완료처리가 ObjectCreated가 아니라 명시 commit+RabbitMQ 구조라 "(신설 검토)"로 두고 완료처리 모델을 결정 항목으로 올려야 한다는 점, well-known은 CleverSpace discovery를 현행 유지하고 GW 호환성 매트릭스 서빙본은 GW 호스트 소유이며 discovery 재지정 시점이 경로 B EOS 커트오버라는 점, 오류는 SRS가 target 오류를 verbatim 통과시키므로 형식을 유지하고 코드 카탈로그+GW 표준 의미론 매핑 표만 제공한다는 점, CS-3 범위를 EzServer/CleverOne 발 device 인증 API 트래픽으로 한정하고 브라우저 SPA·게스트 링크·presigned data plane·comment-server·스트리밍 다운로드 5종을 EOS 제외한다는 점, 리전은 요청 파라미터 없이 CleverSpace 응답 echo와 GW guardrail로 닫는다는 점, CS-4에서 업로드는 v2 고정이고 View/Download와 MinIO는 GW와 분리된 CleverSpace 트랙이라는 점, 로깅은 GW 무관 1단계 선행이고 타임아웃은 대상 확정 후 p99를 측정해 값을 준다는 점 — 이 정정들을 완성본에 반영해 주시면 됩니다.

반대로 GW 계약 변경이나 확인이 필요한 항목은 GW 트랙에서 저희가 처리해 회신하겠습니다. 가장 중요한 것은 ③b hop(GW→CleverSpace) 신원 전달입니다. "내부 신뢰"는 CleverSpace가 JWT 필수인 구조와 맞지 않아 정정하며, 신뢰 앵커가 서명된 device_id 하나라는 점에 동의합니다. GW 서명 upstream 어서션(aud=cleverspace·device_id+clinic_id)과 device 토큰 verbatim 중 택일이 필요하고 어느 쪽이든 GW JWKS 공개(v1.0 미도입)를 요구하므로, 이건 OpenAPI spec-change/CCB 대상이라 결정과 리드타임을 확정해 별도로 회신하겠습니다. 그 밖에 GW v1.0 인가가 coarse이고 CleverSpace 리소스 권한을 대체하지 않는다는 문장, gw/1.1+에서 endpoint 정책을 켤 경우 CleverSpace OpenAPI를 소스로 자동 생성하고 수기 목록을 두지 않는다는 원칙, 행위자 신원 선택지의 확정 문구는 GW가 정리해 드릴 테니 완성본에 반영해 주세요. device_id와 ezServerUid 매핑은 GW enrollment 계약 변경이 필요 없음을 확인하며(SRS가 OneID를 GW와 무관으로 규정), 매핑 소유·등록 시점과 EzServer 유효성 권위·해지 전파는 CleverSpace/OneID 쪽에서 정리해 주시면 됩니다. 끝으로 GW SRS 내부의 문면 충돌(§6.2 "scope 기반 디바이스 권한"과 §7.1.1 "scope v1.0 미사용")은 GW SRS에서 정정하겠습니다 — v1.0은 scope 미사용이 맞습니다.

요약하면 이 문서의 이후 편집 소유는 CleverSpace 팀이고, GW는 위 GW 측 항목(특히 ③b 신원 전달 = JWKS 공개·spec-change)만 확정해 회신하겠습니다. 감사합니다.
```
