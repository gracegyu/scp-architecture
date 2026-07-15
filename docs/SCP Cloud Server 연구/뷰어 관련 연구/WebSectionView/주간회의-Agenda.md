# Web Section View / Cloud Web Viewer v1.3.2 Section 모듈 — 주간회의 Agenda

> **용도:** Section Layout(Section 모듈) 개발·Spec·인계 진행을 주간 회의에서 공유·결정할 때 사용한다.  
> **참고 형식:** [VT API Gateway 주간회의 Agenda](../../VT_API_Gateway/08.VT_API_Gateway/주간회의-Agenda.md)  
> **정본 문서:** `Cloud Web Viewer v1.3.2/` — [OnePager Spec](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-Spec-v1.3.2-OnePager.md) · [개발계획](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-개발계획.md) · [구현계획서(IP)](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-ImplementationPlan.md) · [작업 가이드](./Cloud%20Web%20Viewer%20v1.3.2/Claude%20Code%20작업%20가이드.md)  
> **공유(리뷰):** [OnePager — VKS](https://vks.vatech.com/spaces/ESDEVELOPER/pages/320005969/Cloud+Web+Viewer+v1.3.2+%E2%80%94+Section+Module+%EA%B0%9C%EB%B0%9C+OnePager)

---

## 작성 규칙 (템플릿)

매주 **회의 직전**에 아래 블록을 **파일 맨 아래에 추가**한다. 이전 주 스냅샷은 **삭제하지 않고 보존**(GW Agenda와 동일).

### 주차 블록 구조

| 섹션               | 용도                                             |
| ------------------ | ------------------------------------------------ |
| **이번 주 진행**   | 지난 주 이후 완료·진행 중 작업 (불릿)            |
| **논의 사항**      | 결정·확인이 필요한 항목 — `R1`, `R2` …           |
| **공유 사항**      | 결정 아님 — 진행·일정·리스크 공유 — `S1`, `S2` … |
| **이월 논의 사항** | 미결 표 — `#` · 항목 · 타입 · 상태               |

### 타입 (논의·이월 표)

| 타입   | 의미                          |
| ------ | ----------------------------- |
| [확정] | 기결정 공식 확정·승인         |
| [논의] | 방향·범위 결정 필요           |
| [정보] | 추가 입력·자료·담당자 확보    |
| [선결] | 구현·Spec 착수 전 반드시 필요 |

### 논의 항목 작성 패턴 (복사용)

```markdown
# Cloud Web Viewer v1.3.2 Section 모듈 — M/D 주간회의 Agenda

> 이전 주(M/D) 스냅샷은 위에 보존. 아래는 이번 주 최신 스냅샷.

- 이번 주 진행 (M/D 이후)
  - (완료·진행 항목)
  -

- 논의 사항 (신규 · 이전 주 후속)
  - **R1. (제목)** — (한 줄 요약). **결정 요청:** …
    - (결정) …
    - **성격:** [논의] / [확정] / [정보]

- 공유 사항 (결정 아님)
  - **S1. (제목)** — …

- 이월 논의 사항 (미결 — 계속)

  | #   | 항목 | 타입   | 상태 |
  | --- | ---- | ------ | ---- |
  | 1   | …    | [논의] | …    |
  - **차주 이월 후보:** R1 미확정 시 다음 주 이월.
```

### 관련 링크 (회의 전 확인)

| 항목                      | 위치                                                                         |
| ------------------------- | ---------------------------------------------------------------------------- |
| MMI v0.9.1                | `Cloud Web Viewer v1.3.2/기획·요구사항/MMI/MMI.md`                           |
| UI 시각 정본              | `.../기획·요구사항/MMI/media/image23.png`                                    |
| 기획 답변                 | [PLAN-1287.md](./Cloud%20Web%20Viewer%20v1.3.2/기획·요구사항/PLAN-1287.md)   |
| 개발실 리뷰               | [MMI\_개발실리뷰.md](./Cloud%20Web%20Viewer%20v1.3.2/검토/MMI_개발실리뷰.md) |
| PoC 결과                  | `PoC/Phase1/` … `Phase5/`                                                    |
| 구현 레포                 | `scp-section-poc`                                                            |
| Cloud Web Viewer(CW) 참조 | `cloudwebviewer`                                                             |
| EzCloud Test (MPR·툴바)   | https://container.test.ezcloud.ezcld.net/                                    |

---

# Cloud Web Viewer v1.3.2 Section 모듈 — 7/23 주간회의 Agenda

> **구현 진행(~70%) 스냅샷.** (이전 7/16 = Spec 완성·VKS 리뷰 요청 시점 — 완료 항목은 아래 "확정·정리됨"에 반영.)

- 참조 정보
  - [OnePager (VKS)](https://vks.vatech.com/x/UecSEw)
  - [Demo 사이트](http://scp-section-demo.test.scp.esclouddev.com)
  - Repository: [Azure DevOps `scp-section-poc`](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc)
  - VTS: [PLAN-1287](https://vts.vatech.com/browse/PLAN-1287)

- 이번 주 진행 (구현 ~70% · scp-section-poc)
  - **계측·주석** — Length/Angle/Free Draw(T-P4-2)·**Arrow 신규**(T-P4-3). **3뷰 확장**(Scout·Panorama·Section, 기획 Jessi 확정 §D21). 각 뷰 영역/슬라이스 스코프.
  - **Overlay 3D 평면 귀속(T-P4-4 핵심)** — 생성 시점 평면(거리≤±INT/2·normal≤5°)에 귀속·slice 스크롤 시 재표시(core `overlayPlane`).
  - **Show/Hide Grid(T-P4-5)** — CW `es-view-info` GridView 정합(물리 10mm·점선·뷰 전체·ruler 정렬). Grid 기능이 초기 미배선이던 것 보완.
  - **Slice 스크롤 벤치마크(T-P6-1)** — Th30mm worst-case **JS 1484 / WASM-resident 1225ms**(둘 다 30FPS 초과). → **기본 연산 = WASM-resident + JS 폴백(§D20)**. 실시간 근본해결(GPU 리슬라이스)은 **범위 밖·숙제(§11)** — 빠른 출시 우선.
  - **환자정보/타이틀 실데이터**(DICOM Sex/Age/ID/Name·촬영일)·R/L 방향, 렌더 스타일 토큰화(T-P7-5/6).
  - **CW UI 통일** — 색 팔레트(§3.4.1a)·아이콘 크기·HQ(View Original) 위치·Arrow 아이콘·커브 편집버튼·폰트 정합(§9.11).
  - **접목 설계 정리** — 접목 방식 **소스 병합으로 개정(§D4)**·§9.9 접목 절차(10단계)·§9.10 중복 제거·§9.11 CW 폰트 버그. **Single/Dual·View Original = CW 컨테이너 몫 확정(§D22)**. 저장소·데모 사이트 OnePager 명시.
  - **미구현/잔여(~30%)** — Pan/Zoom/Reset/Pointer(T-P4-6, 커서 에셋만 준비)·계측 삭제 UI·Overlay normal의 UI 배선·시각 폴리시·GPU 리슬라이스(숙제).

- 논의 사항
  - **R1. CW 폰트 override 수정 (누가/어떻게)** — CW `index.css`의 `* {font-family:'Segoe UI','Roboto' !important}`가 **호스트(CleverSpace) Noto Sans를 덮어쓰고 CW는 그 폰트를 로드하지 않아**, 접목 시 Section/CW 텍스트가 나머지 CleverSpace UI와 다르고 **환경(OS)별로 제각각**이 됨(§S3·OnePager §9.11). **결정 요청:** ① CW가 override 제거→호스트 폰트 상속(권장·주 원인 해소), ② styleguide(VT UI/UX)가 org 전역 단일 폰트 확정. (최소한 미제공 폰트를 `!important`로 강제 금지.)
    - **성격:** [논의] · 수정 주체 = **CW 팀**(override 제거) + **styleguide**(단일 폰트). CleverSpace·우리 모듈은 정상.
    - **전제:** CW-1 미수정 시 CW가 우리 텍스트까지 덮어써 폰트 일관성 불가.

- 공유 사항
  - **S1. 현재 단계** — `PoC 완료 → Spec·VKS 리뷰(공유됨) → 구현 진행 중(~70%) [지금] → 잔여 구현·인계 → CW embed·접목`.
  - **S2. 문서 상태** — [**OnePager (VKS)**](https://vks.vatech.com/x/UecSEw) **v1.37**(구현 반영·§9.9~9.11·D19~D22 등). 개발계획 v0.9 / IP 갱신(P4·P6·P7-5/6 진행). 커밋 시점은 별도 관리.
  - **S3. 폰트 설정 불일치 발견 (CleverSpace ≠ CW)** — Section 구현 중 소스 대조로 발견. **현재 문제는 CW 하나**이고, 그 결과 **상황(OS·환경)에 따라 폰트가 다르게 렌더됨**(맞음). 결정은 **R1**. 상세: [OnePager §9.11](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-Spec-v1.3.2-OnePager.md).

    | 대상 | 폰트 스택 | 웹폰트 로드 | `!important` | 맥 | Windows | ChromeOS |
    | --- | --- | :---: | :---: | --- | --- | --- |
    | **CleverSpace**(호스트) | `'Noto Sans','Noto Sans KR','Segoe UI',sans-serif` | ✅ Google Fonts | ✗ | Noto Sans | Noto Sans | Noto Sans |
    | **CW** | `'Segoe UI','Roboto'` | ❌ 없음 | ✅ `* !important` | **Helvetica**(폴백) | Segoe UI | Roboto |
    | **우리 Section/데모** | `= CleverSpace 스택` | ✅(데모) | ✗ | Noto Sans | Noto Sans | Noto Sans |

    - **문제점:** ①**CW만 문제**(호스트·우리 모듈은 폰트 로드·일관) ②**환경(OS)별 제각각**(Win=Segoe UI·ChromeOS=Roboto·맥=Helvetica) ③**호스트 UI와 불일치**(CW `!important`가 Noto Sans 덮어씀) ④**접목 파급**(CW-1 미수정 시 우리 텍스트까지 강제).
    - **근거:** CW `index.css:24` · ezcloud `container-app/index.html`(Noto Sans Google Fonts)·`common-ui/customTheme.ts`.
    - **우리 대응:** 합집합 아님 — **호스트(CleverSpace) 스택(Noto Sans)에 정렬**(폰트 소유는 호스트 몫).
  - **S4. GPU 리슬라이스 = 숙제(빠른 출시 우선)** — 두꺼운 슬랩 실시간 스크롤 근본해결은 WebGL2 GPU 리슬라이스이나 공수 커서 이번 범위 밖(§11·D20). 완충책(캐시·디바운스·표시분리)+WASM으로 체감 유지.
  - **S5. 일정** — 구현 7/13~ 2주 중 **~70% 진행**. 이후 잔여 구현·**CW 팀 접목**(소스 병합·§9.9). Raymond VT API Gateway 병행(부분투입).

    ```mermaid
    gantt
        title Section 모듈 — 잠정 일정 (7/23 스냅샷)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:2px,stroke:#d33,opacity:0.5

        section 문서·Spec
        OnePager Spec 완성·VKS·리뷰       :done, spec, 2026-07-10, 10d

        section 구현 (scp-section-poc)
        모듈 구현(계측·Grid·벤치마크·CW통일) ~70%→완료  :active, impl, 2026-07-13, 2026-07-23

        section 접목 (CW 팀)
        인계 → CW embed·접목(소스 병합)      :integ, after impl, 14d
    ```

  - **S6. Known gaps** — Pan/Zoom/Reset/Pointer 미구현(T-P4-6, 커서 준비) · Arrow 툴 CW `InteractionType` 미포함(접목 시 core 반영) · Scout=MPR Th/INT·Image Adjust 동기 접목 시 배선(§D18) · 계측 삭제 UI·크로스뷰 트래킹(§11) · GPU 리슬라이스(숙제).

- 이월 논의 사항 (7/23 기준 · 재정리)

  | #   | 항목                            | 타입   | 상태                                         |
  | --- | ------------------------------- | ------ | -------------------------------------------- |
  | 1   | CW 폰트 override 수정(CW-1)      | [논의] | **활성** — CW 팀 수정·styleguide 단일화 (→ R1·§9.11) |
  | 2   | Save Project — CW prj 필드      | [정보] | 방향 확정. CW 소스 분석해 진행, 정확 필드는 접목 시 CW팀 확인(§D5) |
  | 3   | Overlay Normal 허용 오차(°)     | [정보] | **구현됨**(기본 5° 상수, T-P4-4) — 실사용 튜닝만 |
  | 4   | 문서 커밋·IP baseline           | [선결] | 구현 진행 중 — 적절 시점 커밋·baseline 동결   |
  - **확정·정리됨:** B/L 자동판정(§5) · 접목=소스병합(§D4) · R/L 방향(§D19) · WASM 기본·GPU 숙제(§D20) · 계측 3뷰(§D21) · Single/Dual·View Original 범위(§D22) · **Slice 스크롤 NFR 측정 완료(§8, JS 1484/WASM 1225ms)** · Show/Hide Grid 구현.
  - **해소(이전 이월):** Section Slice 스크롤 NFR(측정 완료) · Spec 리뷰/착수 gate/구현 착수(진행 중이라 논의 불요).
  - **확정·정리됨 (이번 주):** B/L 자동 판정(확정, OnePager §5) · 접목 방식(D1 — CW vtk 미접목·WebGL embed) · 개발 레포 방안 1 · Scout 명칭 유지(D8) · MMI drift(OnePager 반영).
  - **차주 이월 후보:** R1(리뷰 기한) 미확정 · R2(CW 필드) 회신 지연 시 Save 구현 순연.

---

<!-- 다음 주부터: 위 「작성 규칙」템플릿 블록을 복사해 아래에 # M/D 주간회의 Agenda 를 추가 -->
