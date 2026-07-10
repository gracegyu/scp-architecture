Engineering One Pager

## Project Name

Phase 3: 치열궁 곡선(Dental Arch Curve) 연결 기술 검증

## Date

- **기획/제출(초안)**: 2026-05-04
- **상태**: 구현 완료 (결과 문서: `Phase3_ArchCurve_결과.md`)

## Submitter Info

Raymond

## Project Description

Phase 2에서 구축한 **Scout View Axial Slice** 위에, 치열궁을 따라가는 **Catmull-Rom Spline 곡선**을 사용자가 수동으로 정의하고, 곡선에 **Section Cut 위치**를 나타내는 **수직 짧은 선**을 표시하는 기능을 검증한다.

CleverOne Section View(`CleverOneSectionView.png`) 참고: Scout 화면에 Control Point와 Spline, 곡선에 수직인 샘플링 선이 표시되며, 사용자는 치열 경로에 맞게 곡선을 조정한다. 본 PoC는 **AI 자동 검출은 범위에서 제외**하고, **수동 Point 편집**만 구현한다.

**선행 조건**: Phase 2 완료(CT Volume 로드, Scout View에서 Axial Slice 표시).

**참조 문서**: 메인 로드맵 [`WebSectionView_PoC_OnePager.md`](../WebSectionView_PoC_OnePager.md).

### 데모 화면 레이아웃 (Phase 2 탭 · CleverOne 3영역 + 상단 도구줄)

Phase 1 OnePager의 **좌 2행 / 우 Section 한 덩어리** 구성([`Phase1_WebGL_MultiView_OnePager.md`](../Phase1/Phase1_WebGL_MultiView_OnePager.md) ASCII)과 동일하게, **뷰 11개를 담는 본문 그리드**는 세 영역으로 나뉜다. Phase 2·3 데모(`apps/section-demo`)에서는 그 **위에** CT 로드·모드 전환용 **HTML 레이어(DOM)** 가 올라가 있다. 이 영역은 **Canvas가 아니며 WebGL Context와도 무관**하다.

```
+------------------------------------------------------------------+
| [DOM] 제목 · Phase 1 / Phase 2 탭                                 |
+------------------------------------------------------------------+
| [DOM] CT Data Download — 샘플 CT 선택, Load CT, 진행률·완료 문구    |
+------------------------------------------------------------------+
|                                                                  |
|  Scout 영역 (Phase1 좌상과 동일 슬롯)   |  Section 3x3 (우, 통째) |
|  ┌ Axial 뷰포트 ──────────────────┐   |  [1] [2] [3]            |
|  │ Canvas 2D: CT 슬라이스           │   |  [4] [5] [6]            |
|  │ Canvas 2D: 곡선 오버레이         │   |  [7] [8] [9]            |
|  │ [DOM] Edit Curve 버튼            │   |  (WebGL · 9 Viewport)   |
|  └─────────────────────────────────┘   |                         |
|  [DOM] Slice / WC / WW / INT 슬라이더   |                         |
+------------------------------------------+                         |
|  Panorama 영역 (Phase1 좌하와 동일 슬롯) |                         |
|  (WebGL Canvas · Phase1 더미 패턴)      |                         |
+------------------------------------------+-------------------------+
```

| 구역 | 기술 | 비고 |
| --- | --- | --- |
| 상단 제목·탭 | DOM (React) | `App.tsx` 헤더 |
| CT Data Download 바 | DOM (React) | `CTLoader.tsx`, Canvas 밖 |
| Scout Axial + 곡선 | **Canvas 2D** 2겹 + **DOM** 버튼·슬라이더 | Phase 2·3 구현 기준; WebGL Context 없음 |
| Panorama | **WebGL** 1 Context | Phase 1과 동일한 텍스처 쿼드 데모 |
| Section 3×3 | **WebGL** 1 Context, **9 Viewport** | Phase 1 검증 구성 유지 |

**정리**: “WebGL Context 3개(Scout / Panorama / Section)”는 **본문 3영역**에 대응하는 **원칙적/Phase1 구성**이다. **현재(Phase 2·3) Scout 슬롯**은 실제 CT·곡선을 **Canvas 2D**로 그리므로, Scout 칸에는 **WebGL Context가 없을 수 있다**. 상단 CT Loading·타이틀은 **항상 DOM**이다. 자세한 렌더 경로 결정은 메인 [`WebSectionView_PoC_OnePager.md`](../WebSectionView_PoC_OnePager.md) 「뷰별 렌더링 경로」 참조.

## Business and Marketing Justification

- Section View 파이프라인에서 **파노라마/9개 Section 생성의 입력**이 되는 치열궁 곡선 정의가 필요하다. Web에서 동일 UX로 곡선을 편집할 수 있어야 제품 수준의 Section View와 비교 검증이 가능하다.
- Desktop(CleverOne 등)과 유사한 **Scout 상 곡선 + Section Cut 시각화**는 의사·기술 검토 시 이해 비용을 줄인다.
- Phase 4(파노라마 Reslice), Phase 5(9개 Section)로 이어지는 **데이터(곡선·샘플 위치)의 토대**가 된다.

## Risk Assessment

| 리스크 | 영향도 | 발생 가능성 | 대응 방안 |
|--------|--------|-------------|-----------|
| Axial Slice와 곡선 좌표 불일치(CSS `object-fit` 등) | 중간 | 중간 | CT Canvas와 Overlay Canvas 동일 레이아웃, 마우스 좌표를 Slice 픽셀 좌표로 변환 |
| Catmull-Rom 끝점/제어점 처리로 곡선이 튐 | 낮음 | 낮음 | 가상 제어점(반사) 또는 세그먼트 샘플링 밀도 조정 |
| Section Cut 간격(mm)과 픽셀 환산이 부정확 | 중간 | 낮음 | DICOM Pixel Spacing(`volume.metadata.spacing`) 기준으로 구간 길이 누적 |
| 점이 많아져 편집 UX 혼란 | 낮음 | 중간 | PoC에서는 점 개수 무제한, 실무 가이드(5~10개 권장)는 문서에 명시 |
| 우클릭 삭제가 브라우저 컨텍스트 메뉴와 충돌 | 낮음 | 낮음 | `preventDefault`로 처리, 이벤트는 Overlay Canvas에만 연결 |

## Resource and Scheduling Details

- **기간**: 1주 (5일) — 간소화 PoC 기준
- **인력**: 1명 (Web 프론트 + 좌표/곡선 수학)
- **선행 요구사항**: Phase 2(CT ZIP → Volume, Scout Axial 표시) 완료

| Day | 작업 | 산출물 |
|-----|------|--------|
| 1 | Catmull-Rom·샘플링·mm 간격 유틸(`packages/core/src/curve/`) | Core 모듈 |
| 2 | 곡선 편집 상태/마우스 Hook(`useCurveEditor`) | 편집 로직 |
| 3 | Scout View 이중 Canvas(CT + Overlay), Edit Curve 토글, INT 슬라이더 | UI 통합 |
| 4 | 히트 테스트(점/곡선), 삽입·이동·삭제 검증 | 상호작용 안정화 |
| 5 | 결과 문서·메인 OnePager Phase 표 갱신 | 문서 |

### 소스코드 저장소

- **Repository**: Azure DevOps `prototypes/scp-section-poc` (Monorepo)
- **구조**: pnpm workspaces + Turborepo (상세는 메인 `WebSectionView_PoC_OnePager.md` 참조)

**Phase 3 관련 경로 (요약)**:

```
packages/core/src/curve/          # Catmull-Rom, 간격 샘플링, 히트 테스트
packages/components/src/hooks/useCurveEditor.ts
packages/components/src/ScoutView.tsx   # Axial Slice + 곡선 오버레이
```

### Demo Site

- **URL**: `http://scp-section-demo.test.scp.esclouddev.com/` — Phase 2 탭에서 CT 로드 후 Scout View에서 검증
- **로컬**: `pnpm --filter section-demo dev` (포트는 환경에 따라 5173 등)

## Technical Description

### 목표 범위

| 포함 | 미포함 (후속 Phase) |
|------|---------------------|
| Scout에서 Control Point 배치·이동·삭제·삽입 | Section 위치 하이라이트 사각형 등 고급 내비게이션 |
| Catmull-Rom Spline 렌더링 | 실제 Section 이미지 Reslice (Phase 5) |
| INT(mm) 간격에 따른 Section Cut 수직선 표시 | Panorama 이미지 생성 (Phase 4) |
| Edit Curve ON/OFF, Pixel Spacing 기반 mm 환산 | 치아 Segmentation 오버레이 (Phase 7) |

### UI 스펙

**편집 모드**

- Scout View 좌측 상단 **"Edit Curve"** 토글: ON이면 클릭/드래그로 편집, OFF면 곡선은 유지하되 입력 무시(뷰 전용).

**Control Point**

- 빈 영역 클릭: 끝에 점 추가
- 곡선 근처 클릭: 해당 위치에 점 삽입
- 점 드래그: 이동
- 점 우클릭: 삭제
- 최소 **3개** 이상일 때 Spline 전체 표시(2개만일 때는 세그먼트만 표시하는 정책은 구현체에 따름)

**Spline·표시**

- 알고리즘: **Catmull-Rom** (모든 Control Point 통과)
- 곡선: 녹색 실선, Control Point: 녹색 원 + 테두리
- Section Cut 수직선: 곡선에 수직, **INT** 슬라이더로 간격 조절(기본 1mm 근처), 길이는 PoC에서 양쪽 합 ~20mm 등으로 고정 가능

**좌표계**

- Slice 픽셀 좌표 `(0 … cols, 0 … rows)`에서 편집
- 물리 길이: `volume.metadata.spacing[0]`(열), `spacing[1]`(행) mm/pixel

### 렌더링 구조

- **Canvas 2겹**: 하단 CT Slice용 Canvas + 상단 투명 Overlay Canvas(곡선·점·수직선)
- Slice(WC/WW/Slice index) 변경과 곡선 편집을 분리하여 불필요한 전면 재렌더를 줄임
- 마우스 좌표는 표시 영역(`object-fit: contain`)에 맞게 Slice 좌표로 역투영

### 구현 모듈 (요약)

| 모듈 | 역할 |
|------|------|
| `curve/catmullRom.ts` | 보간, 접선/수직, 균등 샘플, mm 간격 샘플, 곡선 근접 거리 |
| `useCurveEditor` | controlPoints, editMode, sectionInterval, 히트/드래그/삽입/삭제 |
| `ScoutView` | CT 렌더 + Overlay 그리기 + INT 슬라이더 + Edit 버튼 |

### Phase 3 성공 기준

1. 사용자가 Scout Axial 상에서 치열궁을 따라 곡선을 **수동으로** 정의할 수 있다.
2. 정의된 **Spline**과 **Control Point**가 시각적으로 구분되어 표시된다.
3. **추가·삽입·이동·삭제**가 PoC 수준에서 안정적으로 동작한다.
4. **INT** 설정에 따라 곡선을 따라 **Section Cut 수직선**이 표시된다.
5. Edit 모드 OFF 시 **조작 없이 곡선만 유지**된다.

### Phase 3 산출물

1. Core curve 모듈 및 `useCurveEditor` Hook
2. Scout View 통합 데모(section-demo, Phase 2 플로우 내)
3. `Phase3_ArchCurve_결과.md` 및 본 OnePager
