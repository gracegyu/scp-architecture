# Cloud Web Viewer v1.3.2 — Section 모듈 개발계획

| 항목 | 내용 |
|------|------|
| 문서 버전 | 0.6 |
| 작성일 | 2026-07-09 |
| 작성 | Raymond |
| 상태 | Spec OnePager v0.3. **CW UI = pnpm link 확정(§9.4). 다음: scp-section-poc 환경 정렬 적용** |

---

## 1. 이 문서의 역할

MMI 검토·기획 답변·PoC 결과를 바탕으로, **Section 모듈**을 무엇으로 부르고 어디까지 만들며 어떤 순서로 진행할지 정리한 **개발 계획 참고 문서**이다.

- 구현 코드베이스는 **`scp-section-poc`에서 이어서 개발**한다. `cloudwebviewer` 레포에 Section을 직접 넣지 않는다.
- CW 툴바·공통 UI는 **소스 복사 없이** `pnpm link:` 로 `@cloudwebviewer/core`를 참조한다 (§9.4).
- **개발 환경·UI 스택·툴바 look&feel** 은 `cloudwebviewer`와 **통일**한다 (§9). 정본 레포는 참조·link 의존용.
- Spec(SRS) 본문은 **OnePager Spec** (`Section-Module-Spec-v1.3.2-OnePager.md`). 환경 정렬 요구도 Spec에 명시한다.

---

## 2. 명칭 정의

### 2.1 Section 모듈

| 구분 | 명칭 | 설명 |
|------|------|------|
| 본 작업 | **Section 모듈** | MMI v1.3.2 Section Layout 기능을 **제품 접목 전**에 구현·검증한 독립 구현체 |
| 선행 검증 | **Web Section View PoC** (`scp-section-poc`) | 기술 타당성 검증 완료. Section 모듈의 **출발점** |
| 최종 제품 | **Cloud Web Viewer** (Clever Space CT Viewer) | Section 모듈을 **접목**하는 대상 |

PoC와 Section 모듈의 차이:

| | PoC | Section 모듈 |
|---|-----|--------------|
| 목적 | WebGL·곡선·9단면 등 **기술 검증** | MMI v1.3.2 **동작·UX·데이터 규칙** 구현 |
| 범위 | 단계별 최소 기능 | MMI 1.1~1.13 + Overlay 규칙. **UI: image23 3영역 + CW Top Toolbar** (§7) |
| 품질 | 데모·실험 수준 | 인계 가능 수준 (API·데모·Known gaps 문서) |
| 제품 연동 | 없음 | 인계 후 CW Viewer 팀이 접목 |

대외·영문 표기가 필요할 때: **Section Module (v1.3.2)** 또는 **Section RI (Reference Implementation)** 로 병기 가능.

### 2.2 하지 않는 명칭

- **PoC** — 타당성 검증은 끝났으므로 이후 단계에 PoC라고 부르지 않는다.
- **Prototype** — 버릴 코드 느낌. 인계 목적과 맞지 않음.

---

## 3. 전체 진행 절차

```
[완료] MMI v0.9.1
    ↓
[완료] MMI 개발실 리뷰 (VKS)
    ↓
[완료] 기획 답변 (PLAN-1287) + MMI 보강 (Overlay, 회전 스펙아웃 등)
    ↓
[진행] B/L 자동 판정 — 개발실 알고리즘 초안 → 기획 Jira confirm
    ↓
[완료] OnePager Spec 초안 (B/L 알고리즘 포함)
    ↓
[다음] scp-section-poc — cloudwebviewer와 개발 환경·UI 스택 정렬 (§9)  ← **구현 착수 전 필수**
    ↓
Spec 리뷰 (기획 + Cloud Web Viewer 담당자 권장) — 환경 정렬과 병행 가능
    ↓
Section 모듈 구현 (scp-section-poc에서 MMI 정합)
    + Section Slice 스크롤 성능 수치 검증 (구현 초기, 별도 PoC 아님)
    ↓
인계 (패키지·API·데모·Known gaps)
    ↓
[Cloud Web Viewer 팀] 접목 (Scout↔MPR Axial, Layout, prj, 공통 툴)
    ↓
통합 테스트 → 출시
```

주의:

- **Spec 리뷰 ≠ PoC.** 성능 검증은 Section 모듈 구현 초기에 벤치마크로 병행한다.
- **Save Project(1.14)** 는 MMI 포함이나, Section 모듈 단독 완성 vs 접목 시 완성을 Spec에서 나눈다.

---

## 4. 참조 문서·산출물 맵

| 단계 | 문서·위치 | 비고 |
|------|-----------|------|
| 요구사항 | [MMI.md](./Confidential_CloudWebViewer_v1.3.2_MMI_Kor/MMI.md) | v0.9.1, Overlay §775–791 반영 |
| 개발실 리뷰 | [MMI_개발실리뷰.md](./Confidential_CloudWebViewer_v1.3.2_MMI_개발실리뷰.md) | VKS 업로드본 |
| 기획 답변 스레드 | [PLAN-1287.md](../PLAN-1287.md) | Jira comment 정리 |
| PoC OnePager | [WebSectionView_PoC_OnePager.md](../WebSectionView_PoC_OnePager.md) | 기술 검증 배경 |
| PoC 구현 | `scp-section-poc` 레포 | Section 모듈 출발 코드베이스 |
| Spec | [Section-Module-Spec-v1.3.2-OnePager.md](./Section-Module-Spec-v1.3.2-OnePager.md) | **OnePager** — B/L 알고리즘 §Technical Description 2절 |
| cloudwebviewer 레포 | `~/Documents/Azure/cloudwebviewer` | 툴바·공통 UI·개발 환경 정본 (§8) |
| 인계 (미작성) | TBD | README, API, 데모 URL, Known gaps |

---

## 5. 기획 확정 사항 (Spec에 그대로 반영)

PLAN-1287 Jessi 회신 및 MMI 업데이트 기준.

| MMI | 항목 | 확정 내용 |
|-----|------|-----------|
| 1.14 | Save Project | Clever Space MPR과 동일. Desktop→Web 최초 업로드만. 이후 Clever One sync 없음. proj에 Curve 있으면 초기 세팅, 없으면 blank |
| 1.11·1.12 | 계측·주석 | prj 저장. Clever One 규칙 + MMI Overlay §6 (775–791) |
| 1.8 | Active section line 회전 ±45° | **v1.3.2 스펙아웃** (임플란트 시뮬 재검토) |
| 1.6·1.7 | BL/LB 기준점 이동 | **포함** |
| 1.5 | B/L 자동 판정 | 개발실 알고리즘 제안 → 기획 confirm. 폴백: L/B Switching |
| 1.10 | Thickness | 기본 0mm. combo 상한 30mm(Clever One 동일). drag 시 상한 없음 정책(Ez3D-i·Clever One 동일). 개발실 판단 시 drag에도 30mm cap 가능 |
| 1.10 | Draw curve 중 Thickness/Interval | curve 취소 없음, 값 즉시 적용 |
| 1.5 | Draw curve 표시 | Active line: 점 추가마다 갱신. Section 이미지: curve 완료 후 1회 |
| 1.9 | slice 더블클릭 최대화 | **포함** |
| — | 모바일/터치 | v1.3.2 **마우스 전용** |
| — | Scout 명칭 | 당분간 Scout. 7/10 기획 검토 후 변경 시 공유 |

### 5.1 Overlay 표시 규칙 (MMI EP01_F013 §6)

- Overlay는 **Curve + 생성 시점 평면(point, normal)** 에 귀속.
- Section view 표시 조건: (1) 현재 슬라이스 평면과의 **거리** ≤ 저장 interval의 ±Interval/2, (2) **Normal** 허용 오차 — MMI상 "별도 정의" → **Spec에서 수치 확정**.
- Curve point 변경: normal 변경으로 일시 미표시 가능. 데이터 삭제 아님.
- Interval 변경: normal 유지, 원위치 복귀 시 재표시.
- Thickness 변경: Overlay 표시 조건에 영향 없음.
- Overlay는 **MPR 레이아웃과 공유하지 않음**.

---

## 6. Spec에서 확정할 항목

| 항목 | 현재 상태 | Spec에서 할 일 |
|------|-----------|----------------|
| B/L 자동 판정 | PLAN-1287 Raymond 초안 | **OnePager Spec §2** 작성 완료 → 기획 confirm 후 버전 고정 |
| Overlay Normal 허용 오차 | MMI "별도 정의" | 각도(°) 또는 dot product 임계값 |
| Section Slice 스크롤 성능 | 개발실 리뷰 리스크 | 디바운스·캐싱·NFR 수치. 구현 초기 벤치마크 |
| Section 모듈 ↔ CW Viewer 경계 | PoC는 Scout 2D 독립 | API·이벤트·데이터 모델. Scout는 접목 시 MPR Axial |
| Save Project 저장 필드 | 회전 각도 항목 삭제(MMI 반영) | curve·interval·thickness·overlay·B/L 극성 등 목록 |
| Image Filter / 계측 툴 | MPR→Section | Top Toolbar 연동 시 CW `InteractionType`·Handler 패턴 따름. Arrow는 MMI 1.12 신규 — CW에 아직 없음 |
| Section 모듈 UI 스택 | PoC: plain React+Vite6 | **cloudwebviewer와 버전·MUI·툴바 정렬** (§9) |
| 툴바 look&feel | MMI 1.12·1.13 | `@cloudwebviewer/core` **pnpm link** 로 `toolbar/`·`ContentTitleBar` import (§9.4). 복사·포크 금지 |
| CW UI 의존 방식 | PoC: 자체 React UI | **link 확정** — `packages/core`·`common/` 통째 복사 금지. link 실패 시 design token만 임시 |

---

## 7. Section 모듈 범위 (Spec에 고정)

### 7.1 권장 범위 — image23 + Top Toolbar (합의안)

MMI 시각 정본 `image23.png`는 **Scout + Panorama + Section 3×3** 만 담는다. MMI 1.12·1.13의 **Top Toolbar** 는 image23 밖이지만, Section 레이아웃에서 **동일 look&feel** 이 요구되므로 Section 모듈 범위에 **포함**하는 것이 타당하다.

| UI 계층 | MMI | Section 모듈 | 근거 |
|---------|-----|--------------|------|
| **3영역 뷰어 본문** | 1.2~1.9 | **포함** | image23 정본. PoC SectionViewer 계승 |
| **뷰별 타이틀 바** | 1.7~1.9 (W/L, Setting, 최대화) | **포함** | image23 각 영역 상단. CW `ContentTitleBar` 패턴 |
| **Top Toolbar** | 1.12·1.13 (Pan, Zoom, Length, Grid, Overlay…) | **포함** | MMI "MPR과 동일하게 동작". CW `Toolbar` 재사용 |
| **MPR/Section 토글** | 1.1 | 제외 (접목) | `Slide7.jpg` — Clever Space 셸 |
| **Clever Space 셸** | LNB, Back, 환자 목록 | 제외 (접목) | `cloudwebviewer` `BackBtn`·host 연동 |
| **CT 로드·prj I/O** | 1.14 | 데이터 모델만 / 데모 stub | 실제 prj는 CW 팀 (§7.4) |

구현 원칙:

- 툴바·버튼·다이얼로그는 **CW 소스를 scp-section-poc로 복사하지 않는다.** `@cloudwebviewer/core`를 **pnpm `link:`** 로 연결해 `toolbar/`, `workSpace/content/components/common/` 등을 **import** 한다 (§9.4).
- Section 엔진·WebGL·수학은 **`@ewoosoft/scp-section-*`** 패키지에 유지한다. CW `packages/core`와 **역할·네임스페이스를 분리**한다.
- 스타일: link된 CW 컴포넌트가 MUI 5 + Emotion + `#141414` 배경, 36px 아이콘, hover `rgba(0,190,165,0.4)` (`Toolbar.tsx` customCSS)를 제공. link 불가 시에만 동일 토큰으로 임시 UI.
- MMI 1.12 **Arrow** 툴은 현재 CW `InteractionType`에 없음 — Section 모듈에서 CW 패턴으로 **신규 추가** 후 접목 시 core에 역머지 검토.

### 7.2 다른 의견 (Spec 리뷰 시 선택지)

| 안 | 범위 | 장점 | 단점 |
|----|------|------|------|
| **A (권장)** | image23 + Top Toolbar + 뷰 타이틀 바 | MMI 1.12·1.13 데모 가능, 인계 시 UI 갭 최소 | CW 레포 분석·환경 정렬 선행 필요 |
| B (최소) | image23 3영역만 | PoC에서 빠르게 확장 | 툴바 L&F 불일치, 계측·Grid 데모 불가, 접목 시 UI 재작업 |
| C (확대) | A + MPR/Section 토글 + `host-app` 셸 | 제품에 가장 근접 | Clever Space 라우팅·권한 범위 침범, 공수 증가 |
| D (레포 통합) | `cloudwebviewer` 내 `packages/section` 신규 | 툴바·타입·빌드 완전 공유 | "별도 레포 인계" 전제와 충돌 — CW 팀 합의 필수 |

**결론:** Spec에는 **안 A**를 기본으로 쓰고, Integration(접목) 범위는 §7.3에 분리한다.

### 7.3 Integration Spec — Cloud Web Viewer 담당 (접목)

- MPR 레이아웃 ↔ Section Layout 토글·라우팅 (MMI 1.1)
- Scout view = MPR Axial 컴포넌트 재사용 (Section 모듈 2D Scout 교체)
- Save Project prj 읽기/쓰기 (MPR 기존 구현 통합)
- Desktop→Web 최초 업로드, Curve 유무에 따른 초기 세팅
- Clever Space `host-app` 연동, Back·권한·환자 컨텍스트
- Module Federation 배포 (`@cloudwebviewer/core` remote)

### 7.4 Save Project — Section 모듈에서 어디까지?

| 옵션 | 설명 |
|------|------|
| A. 데이터 모델 + 직렬화만 | prj JSON 스키마·좌표계 Spec 정의. Section 모듈은 export/import API만. 실제 CW prj 파일 I/O는 접목 |
| B. 데모용 로컬 저장 | Section 모듈 데모에서 localStorage 등으로 저장/로드 검증. CW prj와 바이너리 호환은 접목 |

기획 답변상 Save는 MPR과 동일 처리이므로, **A + 데모용 B** 조합을 Spec 리뷰 시 CW Viewer 팀과 합의한다.

---

## 8. cloudwebviewer 레포 분석 (선행 필수)

로컬 경로: `~/Documents/Azure/cloudwebviewer`  
원격: https://dev.azure.com/ewoosoft/cloudwebviewer/_git/cloudwebviewer

### 8.1 레포 구조

```
cloudwebviewer/
├── packages/core          # @cloudwebviewer/core — 뷰어 본체 (MFE)
├── packages/comment       # @cloudwebviewer/comment — 댓글 애드온
├── types/core             # @cloudwebviewer/core-types
├── lib/react-vtkjs, vtkjs-wrapper
├── examples/host-app      # Clever Space 연동 데모 (pnpm dev 진입점)
└── package.json           # pnpm workspace 루트
```

현재 **Section Layout 코드는 없음.** CT는 `CTViewerLayout.LayoutMPR` 만 존재 (`ctContent/index.tsx`).

### 8.2 Section 모듈이 참조할 핵심 경로

**소비 방식:** 아래 경로의 파일을 scp-section-poc로 **복사하지 않고**, `@cloudwebviewer/core` link 후 **named import** 한다.

| 영역 | 경로 | Section 모듈 용도 |
|------|------|-------------------|
| Top Toolbar | `packages/core/src/toolbar/` | `Toolbar.tsx`, `ToolBtn.tsx`, `InteractionToolBtnContainer`, `CommandToolBtnContainer`, `WorkspaceViewFeatureToolBtnContainer` |
| 툴 타입 | `packages/core/src/toolbar/type.ts` | `InteractionType`, `CommandType`, `WorkspaceViewFeatureType` |
| 툴 상태 | `packages/core/src/toolbar/store/` | zustand slice — Section에서 활성 뷰·슬라이스별 정책 연동 |
| 뷰 타이틀 바 | `packages/core/src/workSpace/layout/components/ContentTitleBar.tsx` | Scout/Pano/Section 헤더 (W/L, 최대화) |
| 공통 다이얼로그 | `workSpace/content/components/common/` | `ImageAdjustDialog`, `LoadingOverlay`, `OverlayPropertyDialog` |
| 앱 골격 | `packages/core/src/App.tsx` | `Toolbar` + `WorkSpace` 세로 배치 |
| MPR 설정 | `packages/core/src/setting/` | Thickness/Interval combo (`MPR_VIEW_THICKNESSES` 등) |
| 외부 타입 | `@ewoosoft/es-common-types`, `@ewoosoft/vpopviewer-common-types` | Overlay·좌표·Modality |

### 8.3 Toolbar 구성 (현재 MPR 기준)

`App.tsx`: 상단 `Toolbar` → 하단 `WorkSpace`.

`Toolbar.tsx` 그룹:

1. `BackBtn` — Clever Space 연동 (Section 모듈 데모에서는 stub)
2. Interaction: pan, zoom, pointer, length, freeDraw, angle
3. Command: resetView, resetCloudWork, initializeAll, viewOrigin
4. Workspace: showGrid, showOverlays
5. PatInfo: showPatInfo
6. Layout: singleLayout / dualLayout (Section에서는 비적용 가능)
7. `SettingBtn`

MMI 1.12 **Arrow** — 아직 `InteractionType` 미포함. Section Spec에 신규 타입·아이콘·Handler 추가 필요.

### 8.4 워크스페이스 내 cloudwebviewer 관련 문서 조사

| 위치 | 문서 | 내용 |
|------|------|------|
| **cloudwebviewer 레포** | `README.md` | monorepo 구조, node 20 / pnpm 8(구식) / react 18 / vite 5 |
| | `build-and-deploy.md` | 빌드·배포 절차 |
| | `packages/core/docs/*.pu` | PlantUML (setting, CT load flow) |
| | `examples/host-app/README.md` | host 데모 |
| **scp-architecture** | `WebSectionView/Cloud Web Viewer v1.3.2/*` | MMI, 개발계획, Claude Code 가이드 |
| | `WebSectionView/PLAN-1287.md` | 기획 답변 |
| | `Image Download…/CloudWebViewer CT Loading 개선 PoC OnePager.md` | CT 스트리밍 로딩 PoC (cloudwebviewer 브랜치 StreamPOC) |
| | `Image Download…/CloudWebViewer VTK.js 볼륨 렌더링 분석.md` | VTK 분석 |
| | `VT_API_Gateway/참조-카탈로그.md` | cloudwebviewer 레포 링크 |
| | `VT_API_Gateway/references/CleverSpace/Confidential_EzCloud_v1.0_SRS.md` | EzCloud↔CW Viewer 연동 |
| **EzCloud Test (런타임)** | [container.test.ezcloud.ezcld.net](https://container.test.ezcloud.ezcld.net/) | Clever Space Test — **내장 Cloud Web Viewer**(MPR·툴바 UX 참고, §9.3.1) |
| **cloudwebviewer/.cursor/rules** | `excution_command.md`, `common.md` | host-app에서 `pnpm dev`. `docs/srs.md` 참조 규칙 — **현재 레포에 `docs/` 폴더 없음** (미동기화 또는 미클론) |

v1.3.2 Section 전용 SRS는 **아직 레포에 없음.** 정본은 scp-architecture의 MMI + 본 OnePager Spec이 된다.

---

## 9. 개발 환경 정렬 — scp-section-poc ↔ cloudwebviewer

### 9.0 정책 (확정)

| 항목 | 결정 |
|------|------|
| **구현 레포** | `scp-section-poc` — PoC 이후 Section 모듈도 **동일 레포에서 계속** 개발 |
| **정본(참조) 레포** | `~/Documents/Azure/cloudwebviewer` — 툴바·MUI·버전·`.npmrc` **정본** |
| **CW UI 소비** | `@cloudwebviewer/core` **pnpm `link:`** (§9.4). toolbar·common **소스 복사·포크 금지** |
| **Section 엔진** | `@ewoosoft/scp-section-core` 등 **scp-section-poc 패키지 유지** — CW core와 혼합 금지 |
| **하지 않는 것** | Section 초기 구현을 `cloudwebviewer` monorepo로 옮기지 않음 (접목은 인계 후 CW 팀) |
| **CW 로컬 빌드** | link 설정·최초 `pnpm i` 시 1회. 일상 개발은 **scp-section-poc `pnpm dev`만**으로 충분 |
| **CW 동작 참고** | MPR·툴바 UX는 **EzCloud Test** [https://container.test.ezcloud.ezcld.net/](https://container.test.ezcloud.ezcld.net/) 내 **Cloud Web Viewer**로 확인 — CW 로컬 `host-app` 필수 아님 |
| **문서 정본** | Spec·MMI·개발계획은 **scp-architecture** `Cloud Web Viewer v1.3.2/` 유지. poc에는 README 인덱스만 |
| **해야 하는 것** | `scp-section-poc`의 Node/pnpm/React/Vite/TS/MUI 등을 **cloudwebviewer와 동일**하게 맞춤 |
| **목적** | Top Toolbar·공통 UI 재사용, 인계 시 의존성·빌드 갭 최소화, look&feel 일치 |

환경 정렬은 **MMI 기능 구현 착수 전 게이트**이다. Spec(OnePager §3)과 동일 요구.

### 9.1 버전 차이 (현재 → 목표)

| 항목 | cloudwebviewer (정본) | scp-section-poc (현재) | scp-section-poc 목표 |
|------|----------------------|------------------------|----------------------|
| Node.js | 20.x | engines `>=18` | **20.x** |
| pnpm | `packageManager` **9.15.9** | 9.1.1 | **9.15.9** (lock 동기) |
| React | 18.2.0 | ^18.0.0 | **18.2.x** |
| TypeScript | 5.2.2 | ^5.0.0 | **5.2.x** |
| Vite | 5.0.8 | **6.0.0** | **5.0.x** (`section-demo` 다운그레이드) |
| UI | MUI 5.15 + Emotion + Lingui | 없음 | **동일 도입** |
| 상태 | zustand 4.4 | React state only | **zustand** (또는 CW store 패턴) |
| ESLint/Prettier | airbnb + prettier 3.2 | 최소 | CW와 유사 규칙 (선택) |
| registry | `.npmrc` (private) | 없음 | **CW `.npmrc` 공유** (`@ewoosoft/*`) |
| 패키지 스코프 | `@cloudwebviewer/*` | `@ewoosoft/scp-section-*` | **유지** — 인계 시 API만 문서화 |

### 9.2 scp-section-poc 적용 체크리스트

구현 레포 `scp-section-poc`에서 수행:

1. 루트 `package.json` — `packageManager: "pnpm@9.15.9…"`, `engines.node: "20.x"`.
2. `apps/section-demo` — vite **5.0.8**, react/react-dom **18.2**, typescript **5.2**.
3. MUI·Emotion·(필요 시 Lingui) — CW core link와 동일 major로 맞춤 (`section-demo` 또는 `packages/components`).
4. `.npmrc` — `cloudwebviewer/.npmrc`와 동일 registry 설정 (**설정 파일만** 복사).
5. **§9.4** — `@cloudwebviewer/core`·`@cloudwebviewer/core-types` pnpm `link:` 설정.
6. `section-demo`에서 `Toolbar`·`ContentTitleBar` import 후 상단 렌더 — link 성공 검증.
7. `pnpm i` / `pnpm build` / `pnpm dev` — 정렬 후 빌드·데모 기동 검증.
8. README — Node 20·pnpm 9.15.9·CW clone 경로·link 전제 명시.

완료 기준: §9.1 표 목표 충족 + `section-demo` dev 기동 + CW Toolbar link 렌더(또는 Known gap 문서화).

### 9.3 cloudwebviewer 측 (참조만)

- 레포 분석: §8 (Toolbar, ContentTitleBar, host-app).
- link 선행: CW 레포 clone 후 `pnpm i` 1회(의존 해석). **일상 Section 개발마다 CW 빌드·`host-app` 기동은 필수 아님.**
- MPR·툴바 동작·look&feel 확인: **§9.3.1 EzCloud Test** 우선. 로컬 `examples/host-app`은 link 디버깅 시에만.
- Module Federation·접목은 Integration Spec(§7.3) — 환경 정렬과 별도.

#### 9.3.1 EzCloud Test — Cloud Web Viewer 런타임 참고

Section 모듈 개발 시 MPR 레이아웃·Top Toolbar·뷰 타이틀 바 등 **제품 동작·look&feel** 을 확인하는 기본 환경이다. 로컬 `cloudwebviewer` 빌드 없이도 사용한다.

| 항목 | 내용 |
|------|------|
| EzCloud (Clever Space) Test URL | [https://container.test.ezcloud.ezcld.net/](https://container.test.ezcloud.ezcld.net/) |
| Cloud Web Viewer 위치 | 위 EzCloud **컨테이너 앱 안**에 탑재. CT 케이스 열면 MPR 레이아웃·툴바 확인 |
| 용도 | MMI 1.12·1.13 툴바 동작, Pan/Zoom/Length/Grid/Overlay UX, ContentTitleBar, MPR↔Section 토글(접목 범위) **참고** |
| 전제 | 조직 계정 로그인 필요. 테스트 CT·환자 데이터는 Clever Space Test 환경 정책 따름 |
| Section 모듈과의 관계 | Section Layout은 아직 미탑재 — **MPR 레이아웃만** 참고. Section 데모는 `scp-section-poc` `section-demo` |
| 로컬 대안 | `cloudwebviewer/examples/host-app` `pnpm dev` — link·Toolbar import 디버깅 시에만 |

PoC 데모(`scp-section-demo`)와 구분: PoC는 Section 엔진 검증, EzCloud Test는 **CW 제품 UI·MPR 워크플로** 정본 참고.

### 9.4 CW UI 의존 — pnpm link (확정, 복사 금지)

#### 9.4.1 패키지 역할 분리

| 패키지 | 레포 | 역할 | Section 모듈에서 |
|--------|------|------|------------------|
| `@ewoosoft/scp-section-core` | scp-section-poc | WebGL·수학·curve·section slice | **유지·확장** |
| `@ewoosoft/scp-section-components` | scp-section-poc | SectionViewer·Scout·Pano·SectionGrid | **유지·확장** |
| `@cloudwebviewer/core` | cloudwebviewer | Toolbar·WorkSpace shell·공통 다이얼로그 | **link로 import만** |
| `@cloudwebviewer/core-types` | cloudwebviewer | IContent·Overlay·Lock 타입 | **link로 import만** |

`@ewoosoft/scp-section-core` ≠ `@cloudwebviewer/core`. 이름이 비슷해도 **합치거나 scp 쪽에 CW toolbar 소스를 넣지 않는다.**

#### 9.4.2 link 설정 예시

레포가 `~/Documents/Azure/` 아래 나란히 clone 되어 있다고 가정:

```json
// apps/section-demo/package.json (또는 packages/components)
{
  "dependencies": {
    "@cloudwebviewer/core": "link:../../../cloudwebviewer/packages/core",
    "@cloudwebviewer/core-types": "link:../../../cloudwebviewer/types/core"
  }
}
```

- 상대 경로는 **scp-section-poc 내 소비 패키지 기준**으로 조정한다.
- `examples/host-app`의 `core-types` link 패턴과 동일 계열이다. Section은 **UI 컴포넌트**를 위해 `packages/core`를 직접 link한다.

#### 9.4.3 import 범위 (허용)

| import 대상 | 용도 |
|-------------|------|
| `toolbar/Toolbar`, `ToolBtn`, store | Top Toolbar (MMI 1.12·1.13) |
| `workSpace/layout/components/ContentTitleBar` | Scout·Pano·Section 뷰 타이틀 바 |
| `workSpace/content/components/common/*` | ImageAdjust·OverlayProperty·Loading 등 (필요 시) |
| `toolbar/type` | `InteractionType`·`CommandType` (Arrow 신규 시 확장) |

Section 전용 로직(Draw curve, B/L, 9단면 생성)은 **`@ewoosoft/scp-section-*`** 에만 둔다.

#### 9.4.4 금지·폴백

| 금지 | 이유 |
|------|------|
| `cloudwebviewer/packages/core/src/toolbar/` 등을 scp-section-poc로 **복사** | CW 업데이트와 drift, 인계 시 이중 유지보수 |
| `@cloudwebviewer/core`를 scp monorepo **내부 패키지로 포크** | 접목 전제(모듈 인계)와 충돌 |
| Section 엔진을 CW `packages/core`에 **선행 머지** | 레포 통합(§7.2 안 D) — CW 팀 합의 없이 진행 금지 |

link·registry 오류로 Toolbar를 당장 쓸 수 없을 때:

1. Known gap으로 문서화.
2. MUI + §7.1 스타일 토큰으로 **임시** 상단 바만 구현 (기능 우선).
3. link 해결 후 CW 컴포넌트로 **교체** — 임시 UI를 정본으로 고정하지 않음.

---

## 10. PoC 없이 바로 Section 모듈 구현 가능 여부

**결론: 별도 PoC 프로젝트 없이 Section 모듈 구현을 시작해도 된다.**

근거:

- `scp-section-poc`에서 WebGL 3 Context, 곡선, 파노라마, 9단면, 기본 UI가 검증됨.
- 기획 미확정 항목 대부분이 PLAN-1287·MMI에 반영됨.
- 남은 불확실성(성능, Overlay normal, B/L confirm)은 **Spec + 구현 초기 벤치마크**로 처리 가능.

구현 시 유의:

1. **scp-section-poc ↔ cloudwebviewer 환경 정렬** — §9 선행. 툴바·MUI 없이 기능만 먼저 넣지 않음.
2. **Section Slice 스크롤** — 개발실 리뷰 최대 리스크. 구현 착수 직후 첫 주에 수치 측정.
3. **Scout** — Section 모듈에서는 PoC 방식 유지 가능. 접목 시 MPR Axial로 교체한다는 전제를 Spec에 명시.
4. **B/L** — 기획 Jira confirm 전까지 알고리즘을 feature flag 또는 문서 draft로 두고, confirm 후 고정.

---

## 11. 구현·인계 계획 (요약)

| 항목 | 내용 |
|------|------|
| 코드베이스 | `scp-section-poc` + **`@cloudwebviewer/core` pnpm link** (복사 없음) |
| UI 정본 | `image23.png` + link된 CW Toolbar/ContentTitleBar |
| 목표 | MMI v1.3.2 Section Layout을 **CW look&feel 데모**에서 재현 |
| 인계물 | npm 패키지 또는 monorepo 패키지, 공개 API, 데모 URL, Known gaps, Integration Spec 초안 |
| 인계 대상 | Cloud Web Viewer (Clever Space CT Viewer) 담당 개발자 |
| 접목 | 인계 수신 팀이 CW Viewer 레포에서 수행 |

---

## 12. 다음 작업 체크리스트

| 순서 | 작업 | 담당 | 상태 |
|------|------|------|------|
| 0 | **cloudwebviewer 레포 분석** (§8) | Raymond | 완료(문서) |
| 0b | **scp-section-poc 환경 정렬** (§9) — 버전 통일 + **CW core link** (§9.4) | Raymond | **다음 (필수)** |
| 1 | Section 모듈 **OnePager Spec** v1.3.2 (B/L §2 포함) | Raymond | **초안 완료** — 리뷰 대기 |
| 2 | Integration 범위 — §7.3을 Spec Technical Description에 반영 | Raymond + CW Viewer | 대기 |
| 3 | B/L 알고리즘 기획 confirm (PLAN-1287) | Jessi | 진행 |
| 4 | Spec 리뷰 | 기획 + CW Viewer | 대기 |
| 5 | Section 모듈 구현 (CW 툴바 연동 포함) | Raymond | 대기 |
| 6 | Slice 스크롤 성능 벤치마크 | Raymond | 구현 초기 |
| 7 | 인계 패키지 정리 | Raymond | 구현 완료 후 |

---

## 13. Spec 산출물 — OnePager 형식

Section 모듈 Spec은 **SRS 장문이 아니라 OnePager** 로 작성한다. 팀 OnePager 템플릿 필드를 따른다.

파일명 예: `Section-Module-Spec-v1.3.2-OnePager.md` (본 폴더)

### 13.1 OnePager 필드 매핑

| 템플릿 필드 | Section 모듈 Spec에 넣을 내용 |
|-------------|------------------------------|
| **Project Name** | Cloud Web Viewer v1.3.2 — Section Module |
| **Date** | 작성일 |
| **Submitter Info** | Raymond / 담당자 |
| **Project Description** | MMI Section Layout을 CW look&feel로 구현하는 Section 모듈. PoC 계승, 인계 후 CW 접목 |
| **Business and Marketing Justification** | Clever Space CT Section 진단 워크플로. v1.3.2 출시 범위 |
| **Risk Assessment** | Slice 스크롤 성능, B/L 미확정, CW 툴바 의존·Arrow 신규, Scout 접목 |
| **Resource and Scheduling Details** | Spec → 구현 → 인계 일정, CW 팀 협의 시점 |
| **Technical Description** | **핵심** — 아래 §13.2 항목을 이 절에 집약 |

### 13.2 Technical Description에 포함할 상세 (OnePager 본문)

1. **범위 표** — §7.1 (image23 + Toolbar + 타이틀 바 / 제외 항목)
2. **MMI 1.1~1.14 매핑 표** — PoC 갭, 스펙아웃(±45°)
3. **UI 정본** — `image23.png`, CW `Toolbar`·`ContentTitleBar` 참조 경로
4. **Overlay §6** + Normal 허용 오차 (수치 TBD)
5. **B/L 자동 판정** — [OnePager Spec §2](./Section-Module-Spec-v1.3.2-OnePager.md) (PLAN-1287 전문). confirm 3항 미결
6. **Draw Curve** — §4.2 PPT comments (ESC 없음, 1점 더블클릭)
7. **Save Project** — 데이터 모델, proj Curve 없음 시 blank
8. **공개 API·패키지 경계** — `@ewoosoft/scp-section-*` export, CW 연동 포인트
9. **Integration 요약** — §7.3 (접목 책임, Spec 리뷰 시 CW 팀 합의)
10. **NFR** — 9단면 생성 ms, 마우스 전용, 브라우저
11. **개발 환경** — §9 scp-section-poc ↔ cloudwebviewer 정렬 (Spec §3)
12. **DoD** — MMI 체크리스트

장문 SRS가 필요해지면 OnePager 승인 후 별도 문서로 확장한다. v1.3.2 1차 산출물은 **OnePager만**.

---

## 14. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1 | 2026-07-09 | 초안 작성. PoC→Section 모듈 명칭·절차·범위 정리 |
| 0.2 | 2026-07-09 | Spec OnePager 형식. 범위(image23+Toolbar). cloudwebviewer 분석·환경 정렬·문서 조사 |
| 0.3 | 2026-07-09 | OnePager Spec 초안. B/L 알고리즘 Spec 반영 |
| 0.4 | 2026-07-09 | §9 정책 확정: **scp-section-poc에서 계속 개발**, CW와 환경 통일. Spec 연동 |
| 0.5 | 2026-07-09 | §9.4 **pnpm link 확정** — CW toolbar/common 복사 금지, 패키지 역할 분리, Dev 서비스 참고, 문서 정본 위치 |
| 0.6 | 2026-07-09 | §9.3.1 **EzCloud Test URL** — `container.test.ezcloud.ezcld.net` 내 Cloud Web Viewer 런타임 참고 |
