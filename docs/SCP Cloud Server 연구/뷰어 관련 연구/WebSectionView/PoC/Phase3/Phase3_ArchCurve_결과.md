# Phase 3: 치열궁 곡선(Arch Curve) 연결 결과

## 개요

| 항목 | 내용 |
| --- | --- |
| 목표 | Scout View의 Axial Slice 위에서 치열궁을 따르는 Catmull-Rom Spline 곡선을 수동으로 정의하고, Section Cut 수직선을 표시 |
| 기간 | 2026-05-04 |
| 상태 | 구현 완료 |
| 데모 사이트 | http://scp-section-demo.test.scp.esclouddev.com/ (Phase 2 탭 -> CT 로드 후 Scout View) |
| 소스코드 | [Azure DevOps](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc) |

## 구현 결과

### 전체 화면 분할 (section-demo · Phase 2 탭)

Phase 1에서 정의한 **3영역 그리드**(좌상 Scout · 좌하 Panorama · 우측 Section 3×3)는 그대로 `SectionViewer`(`packages/components/src/SectionViewer.tsx`)의 CSS Grid로 유지한다. Phase 2·3에서는 그 **위에** 앱 수준 헤더와 CT 로드 UI를 둔다.

```
+------------------------------------------------------------------+
| [DOM] App 헤더 — 제목, Phase 1 / Phase 2 탭                       |
+------------------------------------------------------------------+
| [DOM] CTLoader — CT 선택, Load CT, 진행·완료·에러 메시지          |
+------------------------------------------------------------------+
| Scout 슬롯           | Section 슬롯 (세로 통합)                    |
| Axial + 곡선 + 슬라이더 | 3×3 WebGL Grid (9 Viewport)           |
+----------------------|                                           |
| Panorama 슬롯        |                                           |
| WebGL (더미)         |                                           |
+----------------------+-------------------------------------------+
```

| 영역 | 렌더링 | 구현 참고 |
| --- | --- | --- |
| 헤더·탭·CT 바 | **DOM만** (Canvas 없음) | `App.tsx`, `CTLoader.tsx` |
| Scout 뷰포트 | **Canvas 2D** ×2 (CT + 오버레이), Edit는 DOM 버튼 | `ScoutView.tsx` |
| Scout 하단 Slice/WC/WW/INT | **DOM** (`input range`) | `ScoutView.tsx` 하단 패널 |
| Panorama | **WebGL** | `PanoramaView.tsx` |
| Section Grid | **WebGL**, 9 Viewport | `SectionGrid.tsx` |

**WebGL Context 3개 전략**과의 관계: Panorama·Section은 각각 WebGL Canvas 1개( Section은 내부 9분할)를 쓴다. **Scout 슬롯은 현재 구현에서 Canvas 2D만 사용**하므로, “3 Canvas 모두 WebGL”인 Phase 1 더미 시나리오와 달리 **Scout 칸에는 WebGL Context가 없다**(메인 OnePager 「뷰별 렌더링 경로」와 동일). 상단 CT Loading·타이틀은 **어떤 Canvas에도 속하지 않는 일반 UI**이다.

### 렌더링 구조

Canvas 2겹 구조를 사용하여 CT Slice와 곡선 오버레이를 독립적으로 관리한다.

```
Scout View 영역
├── Canvas 1: CT Axial Slice (Canvas 2D)     ← Phase 2
├── Canvas 2: Curve Overlay (투명, Canvas 2D) ← Phase 3
└── "Edit Curve" 토글 버튼                    ← Phase 3
```

- CT Slice 변경(Slice/WC/WW)과 곡선 편집이 독립적으로 렌더링
- 오버레이 Canvas에서 마우스 이벤트를 받아 곡선 편집 처리
- screen 좌표를 CT slice pixel 좌표로 변환 (objectFit: contain 보정)

### UI 흐름

1. Phase 2에서 CT 로드 완료 -> 11-View 레이아웃의 Scout View에 Axial Slice 표시
2. Scout View 좌측 상단의 "Edit Curve" 버튼 클릭 -> 편집 모드 ON (녹색)
3. Scout View 위에서 클릭하여 Control Point 순차 배치
4. 3개 이상 배치 시 Catmull-Rom Spline 곡선 자동 표시 (녹색 실선)
5. 곡선을 따라 INT 간격(기본 1mm)으로 Section Cut 수직선 표시 (붉은 반투명)
6. 편집 조작:
   - 빈 영역 클릭: 곡선 끝에 점 추가
   - 곡선 근처 클릭: 해당 위치에 점 삽입
   - 기존 점 드래그: 이동
   - 기존 점 우클릭: 삭제
7. "Edit Curve" 다시 클릭 -> 편집 모드 OFF (곡선 유지, 편집 불가)
8. 하단 컨트롤: Slice/WC/WW + INT(mm) 간격 슬라이더

### 주요 구현 모듈

#### 1. `packages/core/src/curve/catmullRom.ts`

Catmull-Rom Spline 수학 유틸리티 모듈.

- **catmullRomPoint()**: 4개 제어점 사이 보간 (표준 Catmull-Rom 행렬 방식)
- **catmullRomTangent()**: 보간 위치에서의 접선 벡터 (1차 미분)
- **sampleSpline()**: 전체 곡선을 균등 샘플링. 양 끝에 가상 제어점(반사 방식)을 추가하여 끝 구간까지 부드러운 곡선 보장
- **sampleAtInterval()**: mm 단위 간격으로 곡선을 재샘플링. DICOM Pixel Spacing으로 mm<->pixel 변환. 각 위치에서 수직(perpendicular) 단위 벡터 함께 반환
- **findClosestPointOnCurve()**: 마우스 위치에서 곡선까지의 최소 거리 + 삽입할 Control Point 인덱스 계산

#### 2. `packages/components/src/hooks/useCurveEditor.ts`

곡선 편집 상태 및 마우스 상호작용 로직을 관리하는 React Hook.

- **State**: controlPoints[], editMode, sectionInterval, splineSamples[], sectionSamples[]
- **자동 재계산**: controlPoints 또는 sectionInterval 변경 시 spline/section 샘플 자동 업데이트
- **Hit Test**: 점 히트(반경 8px), 곡선 히트(거리 10px) 판별
- **드래그 처리**: 3px 이상 움직여야 드래그 시작 (클릭과 구분)

#### 3. `packages/components/src/ScoutView.tsx`

Scout View 컴포넌트. Phase 3 기능 통합.

- **Canvas 2겹**: CT Canvas + Overlay Canvas (absolute position, 동일 크기)
- **좌표 변환**: screenToSliceCoords() - objectFit: contain의 오프셋/스케일을 보정하여 마우스 좌표를 CT pixel 좌표로 변환
- **오버레이 렌더링**: Spline 곡선(녹색), Control Point(녹색 원+흰 테두리), Section Cut 수직선(붉은 반투명)
- **Edit Curve 버튼**: 좌측 상단 토글 (ON=녹색, OFF=회색)
- **INT 슬라이더**: 하단 컨트롤에 0.5~5.0mm 범위, 0.1mm 단위

### Catmull-Rom Spline 알고리즘

- 모든 Control Point를 통과하는 C1 연속 곡선
- 양 끝 가상 제어점: 반사(reflection) 방식으로 생성하여 끝 구간이 자연스럽게 연장
- 세그먼트당 20~50개 샘플로 부드러운 곡선 표현
- Section Cut 간격: 곡선 위 누적 거리 기반으로 mm 단위 균등 재샘플링

### 좌표계

| 좌표계 | 설명 |
| --- | --- |
| Screen | 브라우저 viewport 기준 (clientX, clientY) |
| Canvas | Canvas element의 bounding rect 기준 |
| Slice | CT 이미지 pixel 좌표 (0~cols, 0~rows) |
| Physical | mm 단위 (Pixel Spacing 변환) |

objectFit: contain에 의해 Canvas 표시 영역이 실제 Canvas 크기와 다를 수 있으므로, 마우스 이벤트 처리 시 스케일과 오프셋을 보정한다.

## 성공 기준 달성 여부

| 기준 | 달성 여부 |
| --- | --- |
| 치열궁 곡선 수동 정의 가능 | O (클릭으로 Control Point 배치) |
| Spline 곡선 시각적 표시 | O (Catmull-Rom, 녹색 실선) |
| Control Point 추가 | O (빈 영역 클릭) |
| Control Point 삽입 | O (곡선 근처 클릭) |
| Control Point 이동 | O (드래그) |
| Control Point 삭제 | O (우클릭) |
| Section Cut 수직선 표시 | O (INT 간격으로 붉은 수직선) |
| INT 간격 조절 | O (0.5~5.0mm 슬라이더) |
| Edit Curve 토글 | O (ON=편집, OFF=뷰 전용) |

## 다음 단계

Phase 4에서는 이 치열궁 곡선을 따라 CT Volume을 Reslice하여 Panorama 이미지를 생성한다.
