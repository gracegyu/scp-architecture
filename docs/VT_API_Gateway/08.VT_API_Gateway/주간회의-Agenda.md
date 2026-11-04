# VT API Gateway — 11/05 주간회의 Agenda

> 이번 주는 **Target Policy** 하나만 다룬다. 이전 주차 내용은 `주간회의-Agenda-Archive.md`.
>
> 상세 = OnePager `docs/onepager/target-policy-onepager-2026-10-27.md` (스펙 PR 15814 안)

- 🔴 **결정 필요**

  | # | 안건 | 왜 지금 |
  | --- | --- | --- |
  | **1** | **Target Policy 스펙 승인** — [GW PR 15814](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15814) · [Console PR 15815](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/15815) | 구현은 일정을 맞추려고 미리 시작했다. **승인돼야** 구현 머지·dev 배포·Console 의 실제 API 연결로 이어진다 |

  - ⭐ 승인되면 머지 직전에 결정 기록(SRS Appendix B 56번)과 OnePager 상태에 **승인일**을 채운다

- **무엇을**
  - target 마다 **클리닉이 호출하면 안 되는 API**(메서드·경로)를 GW 에 등록해 두고, 클리닉 EzServer 가 호출하면 GW 가 거부한다
  - 첫 적용 = **AXS webhook 구독 관리 API**(`/v1/webhook/**`)
  - 이후 막아야 할 API 가 생기면 **운영자가 규칙 한 줄**을 추가한다 — EzServer·GW 배포가 필요 없다

- **왜 — AXS 의 권한은 두 단위로 나뉜다**

  | | 클리닉 단위 API | **연동사(Vatech) 단위 API** |
  | --- | --- | --- |
  | 예 | 환자·오더 | **webhook 구독 관리** |
  | AXS 가 범위를 정하는 방법 | `Organization-ID` 로 그 클리닉 데이터만 | **없음** — Vatech 자격이면 전부 |
  | 한 클리닉이 잘못 호출하면 | 그 클리닉만 영향 | **같은 리전의 Vatech 연동 클리닉 전부** |
  | 누가 막을 수 있나 | AXS | **GW 뿐** |

  - ⭐ **GW 프록시는 Vatech 의 자격을 모든 클리닉에 빌려주는 장치다**
    - 클리닉 단위 API 는 AXS 가 클리닉별로 가둬 주므로 빌려줘도 된다
    - 연동사 단위 API 는 AXS 가 클리닉을 구분하지 못한다 — **자격을 빌려주는 GW 가 막아야 한다**
  - AXS 만의 문제가 아니다 — 이후 붙일 target 에도 같은 빈틈이 생긴다. Target Policy 는 target 을 붙일 때마다 쓰는 표준 장치다

- **지금 막아야 할 것** — 클리닉 하나가 CleverOne → EzServer → GW 경로로 할 수 있는 일

  | 호출 | 결과 |
  | --- | --- |
  | 구독 삭제 | 리전 전 클리닉이 AXS 이벤트를 못 받는다(영상 다운로드 중단) |
  | 구독 주소 변경 | 리전 **전 클리닉의 환자 이벤트**가 임의 주소로 나간다 |
  | 구독 추가 | 위와 같다 |
  | 이벤트 조회 | 리전 전 클리닉의 이벤트를 본다 |

  - 정상 업무에는 영향이 없다 — 구독은 Vatech 운영이 거는 관리 API 다

- **계기**
  - EzServer GW 연동 설계 리뷰(Nemesis)가 "CleverOne 이 EzServer 를 거쳐 AXS 를 직접 호출한다"를 반복 지적
  - EzServer 안에서 막는 안은 기각 — 바꿀 때마다 **수천 사이트 재배포**가 필요하다
  - 📌 Raymond·Thomas 합의(10/27): EzServer 는 허용 + 감사 로그, **통제는 GW Target Policy**

- **어떻게 정했나**

  | 안 | 판정 | 이유 |
  | --- | --- | --- |
  | **target 레코드에 규칙(DB)** | ✅ 채택 | 새 target = 레지스트리 1행 원칙 유지 · 운영자가 배포 없이 수정 |
  | target 별 코드 하드코딩 | 기각 | 새 target·새 규칙마다 GW 배포 |
  | 기존 정책 테이블(Clinic Policy) 활성화 | 기각 | 복잡해서 gw/1.1 로 미룬 기능을 v1.0 에 당겨 온다 |

  - **저장 방식 = target 테이블의 컬럼 하나**(별도 테이블 아님)
    - 규칙은 target 당 몇 개, 바꾸는 일도 드물다
    - 규칙이 수십 개로 늘거나 규칙별 만료가 필요해지면 테이블로 옮긴다

- **Target Policy 와 Clinic Policy**

  | | **Target Policy (신설)** | **Clinic Policy (기존 정책)** |
  | --- | --- | --- |
  | 묻는 것 | 이 target 에서 **어떤 API 를** 막나 | **누가** 이 target 을 써도 되나 |
  | v1.0 | **집행** | 유보 |
  | 이후 | 그대로 | gw/1.1 재설계 |

  - ⭐ Target Policy 는 **하한**이다 — Clinic Policy 가 허용해도 막힌다

- **큰 설계**
  - 판정 순서: 인증 → 비정규 경로 거부 → 리전 → **Target Policy** → Clinic Policy → egress
  - 막으면 `403`, 판정과 상류 해석이 갈릴 수 있는 경로는 `400`
  - **감사 필수**
    - 막을 때: 누가·무엇을(원문 경로)·어느 규칙으로 — 정상 업무로는 나올 수 없어 기록 자체가 침해 신호다
    - 바꿀 때: 규칙 목록 전체의 전후 — 규칙 삭제 = 차단 해제라서
  - 저장된 규칙이 깨져 있으면 **막는다**(fail-closed)
  - Console 은 규칙을 지울 때 **확인을 받는다**

- **진행 현황**

  - 🟡 **스펙** — PR 15814(GW)·15815(Console) 리뷰 중
    - Nemesis 리뷰 5라운드: 7건 → 1 → 1 → 1 → 1, **전부 반영·스레드 18개 resolve**
    - Scott 리뷰: GW 1건(방향 격리 문자)·Console 3건(해제 확인 범위·감사 키·기본 규칙 적용 경로) **전부 반영**
    - ⭐ 2~5라운드는 한 부류였다 — 운영자가 입력하는 규칙 패턴에 보이지 않는 문자 등이 섞이는 경우. 마지막에 패턴 글자를 **ASCII 허용 목록**으로 바꿔 구조적으로 닫았다
  - **구현** — 일정을 맞추려고 GW·Console 모두 스펙 리뷰와 병행해 **미리 시작했다**. 머지는 스펙 승인 뒤
    - ⭐ 미리 시작한 구현의 사전 리뷰가 **실제 우회 두 건**을 찾아 스펙에 반영했다
      - `#` 를 붙이면 판정과 전달 경로가 달라져 차단을 통과
      - NUL 문자로 감사 기록을 60초씩 비울 수 있었음
    - 스펙 결함도 여럿 미리 잡았다(마이그레이션 대상·정규식 등)

- **일정**

  | 날짜 | 마일스톤 |
  | --- | --- |
  | 스펙 승인 직후 | 스펙 머지 → GW 관리 API dev 배포 · Console 실제 API 연결 (실제 차단은 프록시 판정 배포부터) |
  | 11/10(화) | GW·Console 구현 완료 |
  | 11/11(수) | 테스트 완료 — dev 차단·감사 실측 · Console 화면 · AXS sandbox |

  - ⚠ 스펙 승인이 하루 밀리면 이후도 하루씩 밀린다
  - ⚠ 테스트는 dev 와 AXS sandbox 다 — test 환경은 아직 없다

- **리스크**

  | 리스크 | 대응 |
  | --- | --- |
  | 위험이 실재하는지 실측 전 | AXS sandbox 에서 이벤트 조회 1회로 확인(11/11) |
  | ⚠ **규칙 계약을 좁히면 target 전체가 막힌다** — 깨진 규칙은 차단이라 | 계약을 좁힐 때는 배포 전에 기존 규칙을 점검(runbook) |
  | 비정규 경로 거부가 모든 target 에 걸린다 | AXS 정상 경로엔 영향 없음 · CleverSpace 연동(v1.1) 때 재확인 |
  | 운영자 실수로 규칙 삭제 | Console 확인 대화상자 · 감사 기록 |

- **범위 밖 · 후속**
  - Clinic Policy 재설계 — gw/1.1
  - AXS 조직 연동 API 의 고객번호 검증 — 클리닉이 정당하게 쓰는 API 라 막지 않고 검증 필요(backlog)
  - 쿼리로 하는 메서드 재정의(`_method`) — AXS 지원 여부 확인 후(backlog)
