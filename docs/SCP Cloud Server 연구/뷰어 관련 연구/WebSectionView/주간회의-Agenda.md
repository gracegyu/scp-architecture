# Web Section View / Cloud Web Viewer v1.3.2 Section 모듈 — 주간회의 Agenda

> **용도:** Section Layout(Section 모듈) 개발·Spec·인계 진행을 주간 회의에서 공유·결정할 때 사용한다.  
> **참고 형식:** [VT API Gateway 주간회의 Agenda](../../VT_API_Gateway/08.VT_API_Gateway/주간회의-Agenda.md)  
> **정본 문서:** `Cloud Web Viewer v1.3.2/` — [OnePager Spec]({VKS}) · [개발계획](./Cloud%20Web%20Viewer%20v1.3.2/Section-Module-개발계획.md) · [작업 가이드](./Cloud%20Web%20Viewer%20v1.3.2/Claude%20Code%20작업%20가이드.md)  
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
    - (결정) 이슈로 등록해서 지원한다 (Scott)
  - **R2. 국제화(i18n) 정책 — 지원 언어·한국어 지원** — 언어 선택은 **CleverSpace(en/ko)가 소유**하는데 CW는 en/es/fr/ko/pt로 목록이 달라 **CW의 es/fr/pt는 선택 불가·죽은 번역**, 한국어는 CW 비어있음. 우리 모듈은 i18n 미적용(§S7·OnePager §D23). **결정 요청:** ① **지원 언어를 셋 모두 한/영(en/ko)으로 통일 + CleverSpace 연동 국제화** — 추천(Section=Lingui·한국어 통일, CW=ko 채우고 es/fr/pt 정리), vs ② 현행 유지. **언어/시장 정책이라 기획(Scott) 판단.** (프레임워크 정합=Lingui는 기술적 당연.) 결정 후 IP 국제화 Task 착수.
    - **성격:** [논의] · 결정: **기획(Scott)**. CW 한국어 카탈로그 누락·언어목록 정리도 함께 권고(CW 팀).
    - (결정) 한/영으로 3개 제품 모두 통일한다. → OnePager §D23·§9.11·IP T-P4-7 "결정됨/착수 가능"으로 반영 완료. CW 팀엔 ko 채우기·es/fr/pt 정리 권고.
  - **R3. 향후 진행 계획 & 버그 리포트 채널** — 제안 순서: **① 담주 초 구현 완료 → ② 기획팀 테스트(전달 = [데모 사이트](http://scp-section-demo.test.scp.esclouddev.com)) → ③ CW 팀이 CloudWebViewer에 접목(소스 병합, §9.9)**. **결정 요청:** 기획팀 테스트에서 나온 **버그/이슈를 [PLAN-1287](https://vts.vatech.com/browse/PLAN-1287) Sub-Task로 하나씩 등록**하는 방식으로 할지(각 Sub-Task = 1 버그, 상태·담당 추적). 대안: 별도 QA 이슈타입/스프레드시트.
    - **성격:** [논의] · 결정: **팀 합의**(기획·개발). 확정 시 기획팀에 데모사이트 URL + 리포트 템플릿(재현·기대·실제·스샷) 공유.
    - **참고:** 접목은 CW 팀 소관(우리는 인계·지원). 데모는 접목 전 기능·UX 확인용(§OnePager Resource).
    - https://vts.vatech.com/browse/ESCV-138 이슈 이하의 sub task로 bug report를 하게 한다.

- 공유 사항
  - **S1. 현재 단계** — `PoC 완료 → Spec·VKS 리뷰(공유됨) → 구현 대부분 완료(~90%) [지금] → 담주 초 완료 → 기획팀 테스트(데모사이트) → CW embed·접목(CW 팀)` (→ R3).
  - **S2. 문서 상태** — [**OnePager (VKS)**](https://vks.vatech.com/x/UecSEw) **v1.51**(Pan/Zoom §3.7·Pointer §3.8·계측 편집 §3.9·D19~D29 등)·개발계획 v0.9. 커밋 시점은 별도 관리.
  - **S3. 폰트 설정 불일치 발견 (CleverSpace ≠ CW)** — Section 구현 중 소스 대조로 발견. **현재 문제는 CW 하나**이고, 그 결과 **상황(OS·환경)에 따라 폰트가 다르게 렌더됨**(맞음). 결정은 **R1**. 상세: [OnePager §9.11]({VKS}).

    | 대상 | 폰트 스택 | 웹폰트 로드 | `!important` | 맥 | Windows | ChromeOS |
    | --- | --- | :-: | :-: | --- | --- | --- |
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

    | 대상                    | i18n    | 지원 locale                       | 한국어                                                |
    | ----------------------- | ------- | --------------------------------- | ----------------------------------------------------- |
    | **CleverSpace**(호스트) | Lingui  | en_US, ko_KR                      | ✅ 번역됨                                             |
    | **CW**                  | Lingui  | en_US, es_MX, fr_FR, ko_KR, pt_BR | ❌ **ko_KR 카탈로그 비어 영어 폴백**(es/fr/pt는 번역) |
    | **우리 Section 모듈**   | ❌ 없음 | —                                 | ❌ 미적용·한영 혼재                                   |
    - **문제점:** ①우리 모듈 i18n 미적용·한영 혼재 ②CW **한국어 번역 누락**(CleverSpace는 한국어 되는데 CW만 영어) ③**지원 언어 목록 불일치** — **언어 선택은 CleverSpace(en/ko)가 소유**하니 CW의 es/fr/pt는 **선택조차 못 하는 죽은 번역**이고 정작 한국어는 CW 비어있음.
    - **추천안:** **지원 언어를 셋 모두 한/영(en/ko)으로 통일 + CleverSpace 연동 국제화** — Section=CW 동일 Lingui 구조·한국어 통일(IP Task), CW=ko 채우고 es/fr/pt 정리 권고. (선택 불가한 언어는 무의미하니 CleverSpace 기준으로 맞춤.)

- 이월 논의 사항 (7/16 기준 · 재정리)

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 1 | CW 폰트 override 수정(CW-1) | [논의] | **활성** — CW 팀 수정·styleguide 단일화 (→ R1·§9.11) |
  | 2 | 국제화(i18n) 정책·지원 언어 | [논의] | **활성** — 추천: 한/영(en/ko) 통일·CleverSpace 연동. CW es/fr/pt 죽은 번역·ko 누락. 기획(Scott) 결정 (→ R2·§D23) |
  | 3 | Save Project — CW prj 필드 | [정보] | 방향 확정. CW 소스 분석해 진행, 정확 필드는 접목 시 CW팀 확인(§D5) |
  | 4 | 향후 계획·버그 리포트 채널 | [논의] | **신규** — 구현완료→기획 테스트(데모)→CW 접목. 버그=PLAN-1287 Sub-Task? (→ R3) |
  | 5 | 문서(OnePager·개발계획) 커밋 | [정보] | 구현 대부분 완료 — 적절 시점 커밋 |
  - **확정·정리됨:** B/L 자동판정(§5) · 접목=소스병합(§D4) · R/L 방향(§D19) · WASM 기본·GPU 숙제(§D20) · 계측 3뷰(§D21) · Single/Dual·View Original 범위(§D22) · Slice NFR 측정(§8) · Show/Hide Grid · **Pan/Zoom/Reset/Pointer(§D27·§3.7)** · **Pointer 주석(§D28·§3.8)** · **계측 편집·Property(§D29·§3.9)** · **적응형 Ruler·Grid/Ruler 고정(§D27b)**.
  - **해소(이전 이월):** Section Slice 스크롤 NFR(측정 완료) · Spec 리뷰·착수 gate·구현 착수(진행 중이라 논의 불요).

---

# Cloud Web Viewer v1.3.2 Section 모듈 — 7/23 주간회의 Agenda

> **🎉 구현 완료(2026-07-16) 스냅샷.** MMI 전 기능 + **Save Project 전체 흐름·국제화(i18n)·Initialize All**까지 구현·검증 완료(빌드 5/5·단위테스트 142 통과). **이번 주부터 기획팀 데모 테스트·버그 리포트(ESCV-138 Sub-task) → CW 팀 접목** 시작. **남은 코드 작업 없음**(GPU 리슬라이스 숙제·CW 접목부·기획 시각검증 제외).

- 참조 정보
  - [OnePager (VKS)](https://vks.vatech.com/x/UecSEw)
  - [Demo 사이트](http://scp-section-demo.test.scp.esclouddev.com)
  - Repository: [Azure DevOps `scp-section-poc`](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc)
  - VTS: [PLAN-1287](https://vts.vatech.com/browse/PLAN-1287) · 버그: [ESCV-138](https://vts.vatech.com/browse/ESCV-138)

- 이번 주 진행 (**구현 완료** · scp-section-poc) — _지난 스냅샷(~90%) 이후 잔여 전부 완료_
  - **Save Project 전체 흐름 완성(§7·T-P5-2/3/4)** — Save 버튼 → 현재 상태 수집 → **CT별 키(PatientID+StudyDate) localStorage 저장** → **CW `MessageDialog` 파리티**(로딩→"Your changes have been saved.") → **동일 CT 재오픈 시 자동 복원**(커브·계측·파노라마·섹션·뷰별 Pan/Zoom·WL·Grid/Overlay 가시성). **CW 필드 어댑터**(`CurveList`·`SectionInfo`·`PanoSliceInfo`·`OverlayList`), 계측⑨·뷰별 Pan/Zoom③ 저장 모델. StrictMode 복원·좀비 파노라마 버그 수정.
  - **Initialize All(§3.10·T-P5-5)** — 데이터·값(커브/계측/Pan-Zoom/WL/파라미터)만 default로, **뷰 모드(도구·Grid·Overlay 토글)는 유지**(CW 정합). **Reset Cloud Work=CW 셸 소유·미구현 → 클릭 시 "접목 시 지원" 안내**.
  - **국제화(i18n)(§3.11·T-P4-7)** — 회의 결정(한/영 통일)대로 **CW와 동일한 Lingui 매크로**(`i18n._(t\`\`)`·`msg\`\``·`<Trans>`) 채택, 소스 영어로 통일 래핑(App·툴바·뷰·다이얼로그·메뉴). 데모 **EN/한 토글** 시연. 추출·번역은 접목 시 CW 몫.
  - **Arrow 전용 커서 자체 제작(§11 해결)** — CW에 없어 기획 대기 없이 **개발실이 직접 SVG 제작**(계측군 정합). **계측 크로스뷰 연속 추적(§11 해결)** — 드래그·미리보기가 뷰 경계 밖에서도 끊기지 않음.
  - **(이전 완료 유지)** Pan/Zoom/Reset/Pointer(§3.7)·Pointer 주석(§3.8)·계측 편집·Property(§3.9)·계측 생성(Length/Angle/FreeDraw/Arrow, 3뷰)·Overlay 호장 앵커(§4)·Show/Hide Grid·Slice 벤치마크(WASM-resident+JS 폴백)·환자정보 실데이터·CW UI 통일·접목 설계(§9.9/9.10).
  - **잔여(코드 아님)** — ① **기획팀 시각 검증**(데모, MT-\*) ② **CW 접목부**(클라우드 Save I/O·Reset Cloud Work·i18n 추출/번역·소스 병합) ③ **GPU 리슬라이스 숙제**(§11·D20, 빠른 출시 우선 이연).

- 논의 사항 — **이번 주 결정 필요 항목 없음**
  - 지난 회의(7/16)에서 **폰트 override(옛 R1)·국제화 i18n(옛 R2)·버그 리포트 채널(옛 R3)** 모두 결정 완료. 이번 주는 신규 논의 없이 **결정사항 진행**만 진행. → 진행 현황은 **공유 사항**(S1 단계·S5 일정)·**이월 논의 사항 표** 참조.

- 공유 사항
  - **S1. 현재 단계** — `PoC 완료 → Spec·VKS 리뷰(공유됨) → 구현 완료(7/16 ✅) → 기획팀 테스트·버그 리포트(데모사이트) [지금] → CW embed·접목(CW 팀)` (이월 #2).
  - **S2. baseline 정리** — **OnePager(정본 Spec)를 코드와 함께 baseline 관리하도록 구현 저장소 `scp-section-poc/docs/`로 이동**(2026-07-16).

  - **S3. 구현 완료 항목 전체 (Task 정리 · scp-section-poc)** — MMI 전 기능 + Save·i18n·Initialize All. **총 41개 Task 완료**(빌드 5/5·단위테스트 142 통과, 실제 CT로 검증).

    | 영역             | Task     | 내용(요약)                                                                                               | 상태 |
    | ---------------- | -------- | -------------------------------------------------------------------------------------------------------- | :--: |
    | **기반(P0)**     | T-P0-1~5 | 버전 핀 · UI 스택(MUI·zustand·Lingui) · CW 계약 미러 store+Toolbar · 데모 셸 · CT 공급 추상화(외부 패널) |  ✅  |
    | **Curve(P1)**    | T-P1-1   | Draw Curve(제어점·Catmull-Rom·실시간 미리보기)                                                           |  ✅  |
    |                  | T-P1-2   | Edit Curve·컨텍스트 메뉴(점 추가/삭제·L/B Switching·Curve 삭제)                                          |  ✅  |
    |                  | T-P1-3   | B/L 극성 자동 판정(단일 규칙)                                                                            |  ✅  |
    |                  | T-P1-4   | BL/LB 기준점(삼각형·이동)                                                                                |  ✅  |
    | **Slice(P2)**    | T-P2-1   | 전체 slice 인덱싱·9-window 페이징                                                                        |  ✅  |
    |                  | T-P2-2   | Slice 이동·동기(휠·slider, 임계값 필터)                                                                  |  ✅  |
    |                  | T-P2-3   | 재생성 성능(캐싱·디바운스·표시 분리)                                                                     |  ✅  |
    |                  | T-P2-4   | 뷰/타일 최대화                                                                                           |  ✅  |
    | **생성(P3)**     | T-P3-1   | Scout Active line 이동·폭 조절                                                                           |  ✅  |
    |                  | T-P3-2   | Panorama 경계선·중심선 이동                                                                              |  ✅  |
    |                  | T-P3-3   | Panorama thickness line                                                                                  |  ✅  |
    |                  | T-P3-4   | Thickness 0mm·Setting UI·ruler                                                                           |  ✅  |
    |                  | T-P3-5   | 파노라마 생성 모델(thin 재슬라이스+B/L 스윕)                                                             |  ✅  |
    |                  | T-P3-6   | 뷰별 독립 Interval(Scout/Pano/Section)                                                                   |  ✅  |
    | **도구(P4)**     | T-P4-1   | Image Filter(Smooth/Sharpen/MaxSharpen/Inverse/MIP)                                                      |  ✅  |
    |                  | T-P4-2   | 계측 Length/Angle·Free Draw                                                                              |  ✅  |
    |                  | T-P4-3   | **Arrow 툴 신규 + 전용 커서 자체 제작**                                                                  |  ✅  |
    |                  | T-P4-4   | Overlay 표시 규칙(호장 앵커·scroll/interval 재표시)                                                      |  ✅  |
    |                  | T-P4-5   | Show/Hide Grid(물리 10mm 격자)                                                                           |  ✅  |
    |                  | T-P4-6   | **Pan/Zoom/Reset View/Pointer**(뷰별 독립·Grid 고정·적응형 Ruler·CW 커서)                                |  ✅  |
    |                  | T-P4-7   | **국제화 i18n**(CW 동일 Lingui 매크로·영어 소스·EN/한 토글)                                              |  ✅  |
    |                  | T-P4-8   | **Pointer 주석**(CW `PointerDialog`/`PointerCanvas` 포트·모달)                                           |  ✅  |
    |                  | T-P4-9   | **계측/주석 편집**(선택·이동·핸들 점편집·Property/Delete 다이얼로그)                                     |  ✅  |
    | **Save(P5)**     | T-P5-1   | 데이터 모델·CW prj 스키마 매핑                                                                           |  ✅  |
    |                  | T-P5-2   | 직렬화 API·CT키 localStorage·재오픈 자동복원·**Save 버튼·MessageDialog**                                 |  ✅  |
    |                  | T-P5-3   | **CW prj 필드 어댑터**(CurveList/SectionInfo/PanoSliceInfo/OverlayList·XML 미리보기)                     |  ✅  |
    |                  | T-P5-4   | 저장 모델 갭(⑨ 계측·③ 뷰별 Pan/Zoom)                                                                     |  ✅  |
    |                  | T-P5-5   | **Initialize All**(default 복귀·모드 유지) · Reset Cloud Work(접목 시 지원 안내)                         |  ✅  |
    | **NFR·인계(P6)** | T-P6-1   | Slice 스크롤 벤치마크→NFR(WASM-resident+JS 폴백)                                                         |  ✅  |
    |                  | T-P6-2   | 공개 API·인계 패키지                                                                                     |  ✅  |
    | **UI(P7)**       | T-P7-1   | 글로벌 상단 바(환자·MPR/Section·Save)                                                                    |  ✅  |
    |                  | T-P7-2   | 3-뷰 Title Bar(라벨·Curve 관리·아이콘 클러스터)                                                          |  ✅  |
    |                  | T-P7-3   | Per-panel Slice Slider(H/F·P/A·R/L)                                                                      |  ✅  |
    |                  | T-P7-4   | Image Information Overlay(3뷰)                                                                           |  ✅  |
    |                  | T-P7-5   | Scout Curve 렌더 스타일 정합(MMI §1.3)                                                                   |  ✅  |
    |                  | T-P7-6   | Panorama 렌더 스타일 정합(MMI §1.4)                                                                      |  ✅  |
    - **추가 성과(요청/스펙 밖까지 자체 해결):** ① **CW에 없던 Arrow 커서 자체 제작**(기획 대기 없이) ② **계측 크로스뷰 연속 드래그/미리보기** ③ **CW 폰트·i18n 현황 불일치 발견·정리**(§9.11·§D23) ④ **접목 절차·중복 제거 설계**(§9.9/9.10) ⑤ Save 복원 StrictMode·좀비 파노라마 등 엣지 버그 수정 ⑥ 죽은 코드 정리·locale 무관 레이아웃 고정.
    - **소유 구분(접목 시 CW):** Save 실제 `.e3prj`/S3 I/O · Reset Cloud Work 클라우드 리셋 · i18n 추출/번역 · Single/Dual·View Original · Pointer 셸 제공 — 우리는 **기여 조각·소스**를 준비, CW가 완성.

  - **S4. 버그 리포트 요약 (ESCV-138 Sub-Task)** — 기획팀 데모 테스트 접수 현황(각 행 = ESCV-138 하위 1건). **접수 25건 전부 수정 완료**(ESCV-144~169, 158 결번). 일부는 **기획 시각 확인만 대기**(ESCV-150 반전 방향, 152·154 조작감). 확인 후 **Resolved→Close는 기획팀**.

    | 이슈번호 | 유형 | 화면·기능 | 요약 | 상태 |
    | --- | --- | --- | --- | --- |
    | [ESCV-144](https://vts.vatech.com/browse/ESCV-144) | 버그 | UI 라벨(i18n) | 일부 UI 라벨 텍스트가 정상 표시되지 않음(배포 빌드에서 다국어 문자열 미해석) | ✅ **수정 완료** |
    | [ESCV-145](https://vts.vatech.com/browse/ESCV-145) | 개선 | Section 세로폭 | Z 구간 기본값 60→**50mm**(당초 40 → ESCV-153과 통일해 50mm, 기획 확정) | ✅ **수정 완료** |
    | [ESCV-146](https://vts.vatech.com/browse/ESCV-146) | 개선 | Panorama | Active section line 드래그 이동을 **Interval 기준**으로 | ✅ **수정 완료** |
    | [ESCV-147](https://vts.vatech.com/browse/ESCV-147) | 개선 | Panorama | Active section line **회전 컨트롤러(연두 동그라미) 삭제** | ✅ **수정 완료** |
    | [ESCV-148](https://vts.vatech.com/browse/ESCV-148) | 개선 | Initialize All | 실행 시 Pan/Zoom **도구 선택 상태도 해제**(CleverSpace MPR 정책) | ✅ **수정 완료** |
    | [ESCV-149](https://vts.vatech.com/browse/ESCV-149) | 개선 | Edit 모드 | BL/LB 기준점(삼각형)·끝점 겹칠 때 **클릭 히트타겟 분리** | ✅ **수정 완료** |
    | [ESCV-150](https://vts.vatech.com/browse/ESCV-150) | 누락 | Section slice | BL/LB 기준점에 따른 **상단 B/L 표기 좌우 반전** 미반영 | ✅ **수정 완료**(방향 시각확인 대기) |
    | [ESCV-151](https://vts.vatech.com/browse/ESCV-151) | 버그 | Panorama | 우상단 **W/L 값과 방향(R/L·B/L) 라벨 텍스트 겹침·가려짐** | ✅ **수정 완료** |
    | [ESCV-152](https://vts.vatech.com/browse/ESCV-152) | 버그 | Panorama | 이미지가 **경계선(노란 실선) 밖까지 렌더**·경계 기준 crop fit 안 됨 | ✅ **수정 완료**(시각검증 권장) |
    | [ESCV-153](https://vts.vatech.com/browse/ESCV-153) | 개선 | Panorama | 세로폭(경계선 간격) 기본 →**50mm** — **Section 세로폭과 동일 값이라 50mm로 통일**(기획 확정) | ✅ **수정 완료** |
    | [ESCV-154](https://vts.vatech.com/browse/ESCV-154) | 버그 | Panorama | 중심선 드래그 **drop 시 중심선이 세로축 중심으로 오도록 영상 갱신 안 됨** | ✅ **수정 완료**(시각검증 권장) |
    | [ESCV-155](https://vts.vatech.com/browse/ESCV-155) | 버그 | Draw Curve | 실시간 미리보기가 **점선·직선 연결**(Spline 아님) | ✅ **수정 완료** |
    | [ESCV-156](https://vts.vatech.com/browse/ESCV-156) | 버그 | Draw Curve | **B/L 판정이 P1→P2→C 외적이 아니라 "진행방향 오른쪽=L" 고정규칙으로 추정** | ✅ **수정 완료** |
    | [ESCV-157](https://vts.vatech.com/browse/ESCV-157) | 버그 | Draw Curve | **Active section line이 곡선 완료 후에만 반영**(드로잉 중 실시간 갱신 안 됨) | ✅ **수정 완료** |
    | [ESCV-159](https://vts.vatech.com/browse/ESCV-159) | 버그 | Edit Curve | 커브 위 드래그가 **전체 이동이 아니라 Add Point로 동작** | ✅ **수정 완료** |
    | [ESCV-160](https://vts.vatech.com/browse/ESCV-160) | 버그 | Edit Curve | Curve 편집 시 **Section view 영상 갱신 안 됨** | ✅ **수정 완료** |
    | [ESCV-161](https://vts.vatech.com/browse/ESCV-161) | 버그 | Scout·Panorama | **마우스 휠 slice 변경 미동작**(Scout→축 slice, Panorama→navigator; Section만 됐음) | ✅ **수정 완료** |
    | [ESCV-162](https://vts.vatech.com/browse/ESCV-162) | 버그 | 전 뷰 | **Curve 삭제 시 계측/주석(Overlay)이 남음** — Curve 삭제 시 전 뷰 Overlay 함께 제거 | ✅ **수정 완료** |
    | [ESCV-163](https://vts.vatech.com/browse/ESCV-163) | 버그 | Section 계측 | **Section 가로폭(W)·밴드높이(H) 변경 시 계측값·위치 어긋남** — 오버레이 contain letterbox 정합 + W·H 변경 시 u·v 재정규화(물리 mm 보존·해부 추종); 재정규화를 **이미지 재생성 시점에 동기화**해 조절 중 깜빡임·끝점 튐 제거 | ✅ **수정 완료** |
    | [ESCV-164](https://vts.vatech.com/browse/ESCV-164) | 버그 | Section 계측 | **한 tile 내 Length가 가로/세로/대각선 방향별로 다르게 측정** — ESCV-163의 contain letterbox 정합으로 축척 등방성(가로·세로 mm/픽셀 일치) 확보되어 **함께 해결**(별도 코드 변경 없음) | ✅ **수정 완료**(ESCV-163에서 해결) |
    | [ESCV-165](https://vts.vatech.com/browse/ESCV-165) | 버그 | Section·Scout·Pano | **휠 1노치에 slice가 5칸씩 이동**(Windows) — 이벤트당 최대 1스텝(while→if+누적 리셋)으로 1노치=1 interval. deltaY 크기가 OS차(Win 노치≈100~120px vs macOS 작음)라 macOS에선 미재현. Scout·Pano 동일 패턴 함께 정정 | ✅ **수정 완료**(Windows 검증 권장) |
    | [ESCV-166](https://vts.vatech.com/browse/ESCV-166) | 버그 | Section 최대화 | **개별 slice 최대화 후 마우스 안 움직이고 재더블클릭 시 최소화 안 됨** — 네이티브 dblclick의 연속클릭 카운터가 정지 시 3,4…로 쌓여 2번째에서만 발생하는 문제. 클릭 시각·위치로 더블클릭 직접 판정(판정 후 리셋)해 이동 여부와 무관하게 토글. 매직마우스는 미세이동으로 리셋돼 미재현 | ✅ **수정 완료** |
    | [ESCV-167](https://vts.vatech.com/browse/ESCV-167) | 개선 | 계측 Property | **Property 필드를 kind별로 분기** — Length·Angle=Line Color+Font Color+Font Size, Arrow·FreeDraw=Line Color+**Line Style**. Line Style은 MMI 미명시라 **CW 정합**(Thin=1·Middle=3·Thick=5, 기본 Thin), 저장·로드는 선굵기 숫자. 렌더에 선굵기 반영. **화살촉은 채운 삼각형**(굵은 선에서도 뾰족, 샤프트는 촉 밑변까지만·둥근 조인) | ✅ **수정 완료**(CW 동일 구현) |
    | [ESCV-169](https://vts.vatech.com/browse/ESCV-169) | 버그 | 확인 다이얼로그 | **Curve 삭제 확인 message box 버튼 좌우 반대** — 확인(OK)이 우·취소가 좌였음 → MMI·Clever Space 정합으로 **확인 좌·취소 우**로 순서 교체 | ✅ **수정 완료** |
    | [ESCV-168](https://vts.vatech.com/browse/ESCV-168) | 버그 | Section 최대화 | **개별 slice 최대화 시 계측/주석(Overlay)이 안 보임** — 최대화 div(zIndex 20, 불투명)가 계측 오버레이(z5)·격자(z4)를 가림. 오버레이를 최대화 div 위로(격자 21·계측 22) 올려 최대화 시에도 표시(격자도 함께). 오버레이 표시는 Show/Hide로만 제어(최대화와 독립) | ✅ **수정 완료** |
    - **리포트 템플릿(기획팀 전달):** 화면·기능 / 재현 절차 / 기대 결과 / 실제 결과 / 스크린샷 / 심각도. **채널 = ESCV-138 하위 Sub-Task 1건씩.**

  - **S5. 일정 — 구현 완료(7/16), 일정 앞당김.** 구현 **100%**(MMI 전 기능 + Save·i18n·Initialize All) → **이번 주 기획팀 테스트·버그 리포트(데모사이트)** → **CW 팀 접목**(소스 병합·§9.9). Raymond VT API Gateway 병행(부분투입).

    ```mermaid
    gantt
        title Section 모듈 — 일정 (7/23 기준 · 구현 완료)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:2px,stroke:#d33,opacity:0.5

        section 문서·Spec
        OnePager Spec 완성·VKS·리뷰       :done, spec, 2026-07-10, 9d

        section 구현 (scp-section-poc)
        모듈 구현 완료(계측·Pan/Zoom·Pointer·편집·Save·i18n·Initialize All)  :done, impl, 2026-07-13, 2026-07-19

        section 기획팀 테스트 (7/20~)
        데모 테스트·버그 리포트(ESCV-138 Sub-Task)   :active, qa, 2026-07-20, 10d

        section 접목 (CW 팀 · 일정 미정)
        인계(핸드오프)                          :milestone, ho, after qa, 0d
        접목·소스 병합 — 일정 미정(TBD)          :crit, integ, after ho, 5d
    ```

    - ※ **접목(CW embed·소스 병합)은 CW 팀 소관 · 일정 미정(TBD).** Gantt의 접목 바는 위치 예시일 뿐 확정 일정이 아니며, 확정된 것은 **인계(핸드오프) 시점**까지다.

  - **S6. Known gaps (구현 완료 후 잔여 = 접목·숙제만)** — **✅ 해소:** Save Project 전체·CW 필드 어댑터·⑨계측/③Pan-Zoom 저장·국제화(i18n)·Initialize All·Arrow 전용 커서·크로스뷰 연속 추적. **접목 시 CW(우리 코드 아님):** Save 실제 `.e3prj`/S3 I/O·Reset Cloud Work 클라우드부·i18n 추출/번역·Arrow `InteractionType` core 역머지(§9.6)·Scout=MPR Th/INT·Image Adjust 동기(§D18)·Single/Dual·View Original(§D22). **숙제(빠른 출시 우선 이연):** GPU 리슬라이스(§11·D20).

- 이월 논의 사항 (7/16 기준 · 재정리)

  | #   | 항목                         | 타입   | 상태                                                                             |
  | --- | ---------------------------- | ------ | -------------------------------------------------------------------------------- |
  | 1   | CW 폰트 override 수정(CW-1)  | [확정] | **진행** — 이슈 등록 지원(Scott) 결정, CW 팀 수정·styleguide 단일화 추적 (§9.11) |
  | 2   | 향후 계획·버그 리포트 채널   | [확정] | **진행** — 구현 완료→기획 테스트(데모)→CW 접목. 버그=ESCV-138 Sub-Task           |
  | 3   | 문서(OnePager·개발계획) 커밋 | [정보] | **구현 완료** — 적절 시점 커밋                                                   |
  - **금주 확정·완료:** **Save Project 전체(§7·T-P5-2/3/4)** · **국제화 i18n(§3.11·T-P4-7·한/영 Lingui)** · **Initialize All(§3.10·T-P5-5)** · **Arrow 전용 커서·크로스뷰 추적(§11)**.
  - **확정·정리됨(기존):** B/L 자동판정(§5) · 접목=소스병합(§D4·§9.9/9.10) · R/L 방향(§D19) · WASM 기본·GPU 숙제(§D20) · 계측 3뷰(§D21) · Single/Dual·View Original 범위(§D22) · Slice NFR(§8) · Show/Hide Grid · Pan/Zoom/Reset/Pointer(§D27·§3.7) · Pointer 주석(§D28·§3.8) · 계측 편집·Property(§D29·§3.9) · 적응형 Ruler·Grid/Ruler 고정(§D27b) · 초기화 명령·default 기준(§D30·§3.10).
  - **해소:** Section Slice NFR(측정) · Spec 리뷰·착수 gate · **구현(전부 완료)**.

---

<!-- 다음 주부터: 위 「작성 규칙」템플릿 블록을 복사해 아래에 # M/D 주간회의 Agenda 를 추가 -->
