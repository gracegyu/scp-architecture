# Web Section View / Cloud Web Viewer v1.3.2 Section 모듈 — 주간회의 Agenda

> **용도:** Section Layout(Section 모듈) 개발·Spec·인계 진행을 주간 회의에서 공유·결정할 때 사용한다.  
> **참고 형식:** [VT API Gateway 주간회의 Agenda](../../VT_API_Gateway/08.VT_API_Gateway/주간회의-Agenda.md)  
> **정본 문서:** `Cloud Web Viewer v1.3.2/` — [OnePager Spec](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-Spec-v1.3.2-OnePager.md) · [개발계획](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-개발계획.md) · [작업 가이드](./Cloud%20Web%20Viewer%20v1.3.2/Claude%20Code%20작업%20가이드.md)  
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

# Cloud Web Viewer v1.3.2 Section 모듈 — 7/16 주간회의 Agenda

> **구현 대부분 완료(~90%) 스냅샷.** MMI 전 기능 구현 완료, 잔여는 Save 배선·i18n(회의 결정 대기)·시각 폴리시. **담주 초 구현 완료 예정 → 기획팀 테스트(데모사이트) → CW 팀 접목** 순서(→ R3).

- 참조 정보
  - [OnePager (VKS)](https://vks.vatech.com/x/UecSEw)
  - [Demo 사이트](http://scp-section-demo.test.scp.esclouddev.com)
  - Repository: [Azure DevOps `scp-section-poc`](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc)
  - VTS: [PLAN-1287](https://vts.vatech.com/browse/PLAN-1287)

- 이번 주 진행 (구현 ~90% · scp-section-poc)
  - **Pan/Zoom/Reset View/Pointer(공통 뷰 조작, §3.7·T-P4-6)** — 뷰별 독립 transform. 이미지·계측만 변환, **Grid는 고정·Ruler는 위치 고정+눈금 단위/표시 mm는 배율 반영**(적응형 `chooseRulerSteps`). Zoom=우클릭·X+Y 합산(위·우=확대). Section 3×3은 9뷰가 하나로 함께(§D27). CW 커서 정본.
  - **Pointer 주석(§3.8·T-P4-8)** — CW `PointerDialog`/`PointerCanvas` 포트(FreeDraw식 다중·Eraser·두께·색·Reset·Close=소거). **모달**(Toolbar 등 차단). Pointer는 CW 셸 소유 → 접목 시 CW 것 사용(§9.9-8b).
  - **계측/주석 편집(§3.9·T-P4-9)** — 생성 후 **선택·통째 이동·속빈 네모 핸들로 점 편집(각도/길이 실시간)·단일 선택**. 우클릭→**컨텍스트 메뉴(Property/Delete)**. **Property 다이얼로그**(선색·글자색·글자크기, CW `OverlayPropertyDialog` 포트). 편집 커서=CW `overlaySelectedCursor`. 속성은 Save ⑨로 저장.
  - **계측·주석 생성** — Length/Angle/Free Draw·**Arrow 신규**. **3뷰 확장**(§D21). 도구별 CW 커서(length/angle/freeDraw). 라벨 흰 글씨(박스 제거).
  - **Overlay 3D 평면 귀속**·**Show/Hide Grid**(CW GridView 정합)·**Slice 스크롤 벤치마크**(JS 1484/WASM-resident 1225ms → 기본 WASM-resident+JS 폴백 §D20).
  - **환자정보/타이틀 실데이터**·R/L 방향·**CW UI 통일**(색·아이콘·폰트 §9.11)·**접목 설계**(소스 병합 §D4·§9.9 접목 절차·§9.10 중복 제거·Single/Dual·View Original CW 몫 §D22).
  - **잔여(~10%)** — Save Project 배선·CW 필드 어댑터·⑨계측/③카메라 저장(T-P5-2/3/4)·국제화(회의 결정 대기 R2/T-P4-7)·시각 폴리시·GPU 리슬라이스(숙제 §11)·Arrow 전용 커서(기획 §11).

- 논의 사항
  - **R1. CW 폰트 override 수정 (누가/어떻게)** — CW `index.css`의 `* {font-family:'Segoe UI','Roboto' !important}`가 **호스트(CleverSpace) Noto Sans를 덮어쓰고 CW는 그 폰트를 로드하지 않아**, 접목 시 Section/CW 텍스트가 나머지 CleverSpace UI와 다르고 **환경(OS)별로 제각각**이 됨(§S3·OnePager §9.11). **결정 요청:** ① CW가 override 제거→호스트 폰트 상속(권장·주 원인 해소), ② styleguide(VT UI/UX)가 org 전역 단일 폰트 확정. (최소한 미제공 폰트를 `!important`로 강제 금지.)
    - **성격:** [논의] · 수정 주체 = **CW 팀**(override 제거) + **styleguide**(단일 폰트). CleverSpace·우리 모듈은 정상.
    - **전제:** CW-1 미수정 시 CW가 우리 텍스트까지 덮어써 폰트 일관성 불가.
  - **R2. 국제화(i18n) 정책 — 지원 언어·한국어 지원** — 언어 선택은 **CleverSpace(en/ko)가 소유**하는데 CW는 en/es/fr/ko/pt로 목록이 달라 **CW의 es/fr/pt는 선택 불가·죽은 번역**, 한국어는 CW 비어있음. 우리 모듈은 i18n 미적용(§S7·OnePager §D23). **결정 요청:** ① **지원 언어를 셋 모두 한/영(en/ko)으로 통일 + CleverSpace 연동 국제화** — 추천(Section=Lingui·한국어 통일, CW=ko 채우고 es/fr/pt 정리), vs ② 현행 유지. **언어/시장 정책이라 기획(Scott) 판단.** (프레임워크 정합=Lingui는 기술적 당연.) 결정 후 IP 국제화 Task 착수.
    - **성격:** [논의] · 결정: **기획(Scott)**. CW 한국어 카탈로그 누락·언어목록 정리도 함께 권고(CW 팀).
  - **R3. 향후 진행 계획 & 버그 리포트 채널** — 제안 순서: **① 담주 초 구현 완료 → ② 기획팀 테스트(전달 = [데모 사이트](http://scp-section-demo.test.scp.esclouddev.com)) → ③ CW 팀이 CloudWebViewer에 접목(소스 병합, §9.9)**. **결정 요청:** 기획팀 테스트에서 나온 **버그/이슈를 [PLAN-1287](https://vts.vatech.com/browse/PLAN-1287) Sub-Task로 하나씩 등록**하는 방식으로 할지(각 Sub-Task = 1 버그, 상태·담당 추적). 대안: 별도 QA 이슈타입/스프레드시트.
    - **성격:** [논의] · 결정: **팀 합의**(기획·개발). 확정 시 기획팀에 데모사이트 URL + 리포트 템플릿(재현·기대·실제·스샷) 공유.
    - **참고:** 접목은 CW 팀 소관(우리는 인계·지원). 데모는 접목 전 기능·UX 확인용(§OnePager Resource).
    - https://vts.vatech.com/browse/ESCV-138 이슈 이하의 sub task로 bug report를 하게 한다.

- 공유 사항
  - **S1. 현재 단계** — `PoC 완료 → Spec·VKS 리뷰(공유됨) → 구현 대부분 완료(~90%) [지금] → 담주 초 완료 → 기획팀 테스트(데모사이트) → CW embed·접목(CW 팀)` (→ R3).
  - **S2. 문서 상태** — [**OnePager (VKS)**](https://vks.vatech.com/x/UecSEw) **v1.51**(Pan/Zoom §3.7·Pointer §3.8·계측 편집 §3.9·D19~D29 등)·개발계획 v0.9. 커밋 시점은 별도 관리.
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
  - **S5. 일정** — 구현 **~90%**(MMI 전 기능 완료), **담주 초 마무리**(Save 배선·폴리시) → **기획팀 테스트(데모사이트)** → **CW 팀 접목**(소스 병합·§9.9). Raymond VT API Gateway 병행(부분투입).

    ```mermaid
    gantt
        title Section 모듈 — 잠정 일정 (7/16 스냅샷)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:2px,stroke:#d33,opacity:0.5

        section 문서·Spec
        OnePager Spec 완성·VKS·리뷰       :done, spec, 2026-07-10, 10d

        section 구현 (scp-section-poc)
        모듈 구현(계측·Pan/Zoom·Pointer·편집) ~90%   :active, impl, 2026-07-13, 2026-07-21
        Save 배선·폴리시 마무리                        :impl2, 2026-07-21, 2d

        section 기획팀 테스트
        데모사이트 테스트·버그 리포트(R3)              :qa, after impl2, 5d

        section 접목 (CW 팀)
        인계 → CW embed·접목(소스 병합)      :integ, after qa, 14d
    ```

  - **S6. Known gaps** — Save Project 배선·CW 필드 어댑터·⑨계측/③카메라 저장(T-P5) · 국제화(R2 결정 대기) · Arrow 툴 CW `InteractionType` 미포함(접목 시 core 반영)·Arrow 전용 커서(기획 §11) · Scout=MPR Th/INT·Image Adjust 동기 접목 시 배선(§D18) · 크로스뷰 트래킹·GPU 리슬라이스(숙제 §11). **Pan/Zoom/Pointer/계측 편집은 구현 완료.**
  - **S7. 국제화(i18n) 현황 불일치 발견** — CleverSpace·CW 모두 **Lingui**이나 **CW 한국어 카탈로그가 비어** 한국어에서 영어로 폴백, 우리 모듈은 i18n 미적용·한영 혼재. 결정은 **R2**. 상세: [OnePager §9.11-CW-2·§D23](https://vks.vatech.com/x/UecSEw).

    | 대상 | i18n | 지원 locale | 한국어 |
    | --- | --- | --- | --- |
    | **CleverSpace**(호스트) | Lingui | en_US, ko_KR | ✅ 번역됨 |
    | **CW** | Lingui | en_US, es_MX, fr_FR, ko_KR, pt_BR | ❌ **ko_KR 카탈로그 비어 영어 폴백**(es/fr/pt는 번역) |
    | **우리 Section 모듈** | ❌ 없음 | — | ❌ 미적용·한영 혼재 |

    - **문제점:** ①우리 모듈 i18n 미적용·한영 혼재 ②CW **한국어 번역 누락**(CleverSpace는 한국어 되는데 CW만 영어) ③**지원 언어 목록 불일치** — **언어 선택은 CleverSpace(en/ko)가 소유**하니 CW의 es/fr/pt는 **선택조차 못 하는 죽은 번역**이고 정작 한국어는 CW 비어있음.
    - **추천안:** **지원 언어를 셋 모두 한/영(en/ko)으로 통일 + CleverSpace 연동 국제화** — Section=CW 동일 Lingui 구조·한국어 통일(IP Task), CW=ko 채우고 es/fr/pt 정리 권고. (선택 불가한 언어는 무의미하니 CleverSpace 기준으로 맞춤.)

- 이월 논의 사항 (7/16 기준 · 재정리)

  | #   | 항목                            | 타입   | 상태                                         |
  | --- | ------------------------------- | ------ | -------------------------------------------- |
  | 1   | CW 폰트 override 수정(CW-1)      | [논의] | **활성** — CW 팀 수정·styleguide 단일화 (→ R1·§9.11) |
  | 2   | 국제화(i18n) 정책·지원 언어      | [논의] | **활성** — 추천: 한/영(en/ko) 통일·CleverSpace 연동. CW es/fr/pt 죽은 번역·ko 누락. 기획(Scott) 결정 (→ R2·§D23) |
  | 3   | Save Project — CW prj 필드      | [정보] | 방향 확정. CW 소스 분석해 진행, 정확 필드는 접목 시 CW팀 확인(§D5) |
  | 4   | 향후 계획·버그 리포트 채널       | [논의] | **신규** — 구현완료→기획 테스트(데모)→CW 접목. 버그=PLAN-1287 Sub-Task? (→ R3) |
  | 5   | 문서(OnePager·개발계획) 커밋    | [정보] | 구현 대부분 완료 — 적절 시점 커밋                 |
  - **확정·정리됨:** B/L 자동판정(§5) · 접목=소스병합(§D4) · R/L 방향(§D19) · WASM 기본·GPU 숙제(§D20) · 계측 3뷰(§D21) · Single/Dual·View Original 범위(§D22) · Slice NFR 측정(§8) · Show/Hide Grid · **Pan/Zoom/Reset/Pointer(§D27·§3.7)** · **Pointer 주석(§D28·§3.8)** · **계측 편집·Property(§D29·§3.9)** · **적응형 Ruler·Grid/Ruler 고정(§D27b)**.
  - **해소(이전 이월):** Section Slice 스크롤 NFR(측정 완료) · Spec 리뷰·착수 gate·구현 착수(진행 중이라 논의 불요).

---

<!-- 다음 주부터: 위 「작성 규칙」템플릿 블록을 복사해 아래에 # M/D 주간회의 Agenda 를 추가 -->
