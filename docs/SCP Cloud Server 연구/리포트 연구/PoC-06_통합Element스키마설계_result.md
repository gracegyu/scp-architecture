# PoC-06 결과 보고서: 통합 Element 스키마 설계

## 요약

- **통합 스키마**: JSON 기반, mm 좌표·pt 폰트, 문서→용지→페이지→요소 계층 구조
- **공통 속성**: `id`, `position`, `size`, `style`, `unit: 'mm'` (PoC-02·PoC-03 반영)
- **Element 타입**: ImageBox, TextBox, Label, ToothBox, Annotation(6종), Block, Form Controls 등 20+ 타입 통합
- **확장성**: `extensions` 네임스페이스로 제품별·버전별 속성 분리, 스키마 버전 관리
- **호환성**: E2, E3, EzOrtho, CleverOne 전 제품 매핑 가능, Migration 매핑 테이블 정의
- **산출물**: JSON Schema 초안, TypeScript 타입 정의, 호환성 매트릭스, 확장 가이드라인

---

## 1. 개요

### 1.1 검증 목표

기존 4개 제품(E2, E3, EzOrtho, CleverOne)의 서로 다른 리포트 Element 구조를 하나의 통합 JSON 스키마로 설계합니다. PoC-01~05의 결정(mm 좌표, pt 폰트, HTML DOM+SVG, 선정 라이브러리)을 반영하고, Migration(PoC-07)과 렌더링 엔진(PoC-14)에서 그대로 사용할 수 있도록 합니다.

### 1.2 선행 PoC 결정 사항 반영

| PoC    | 결정 사항                                 | 스키마 반영                                             |
| ------ | ----------------------------------------- | ------------------------------------------------------- |
| PoC-01 | JSON 포맷, TypeScript 타입 생성           | JSON Schema + TS 인터페이스                             |
| PoC-02 | mm 좌표, 소수점 3자리(#.###)              | `position`, `size`, `margin` 단위 `mm`, 정밀도 명시     |
| PoC-03 | pt 폰트, 96/72 DPI 전략                   | `style.fontSize` 단위 `pt`, 단위 필드 명시              |
| PoC-04 | HTML DOM + SVG 렌더링                     | 요소 타입을 DOM/SVG 컴포넌트와 1:1 매핑 가능하도록 설계 |
| PoC-05 | React-Spring, html2canvas, cornerstone 등 | 이미지·DICOM·텍스트 필드 구조와 연동 가능하도록 설계    |

### 1.3 설계 원칙

1. **단일 진실 공급원**: 좌표·크기·폰트는 mm·pt만 사용, 단위 필드로 명시
2. **공통 우선**: 모든 요소에 공통 속성(id, position, size, style) 적용 후 타입별 확장
3. **제품 중립**: 제품명/버전은 메타데이터로만 두고, 스키마는 제품 비의존
4. **확장 가능**: 신규 타입·속성은 `extensions` 또는 `type` 디스크리미네이터로 추가
5. **Migration 친화**: 기존 XML/제품별 필드명과 1:1 매핑 가능한 이름·구조 우선

### 1.4 고려한 모든 요소 (심층 검토)

**데이터 및 단위**

- PoC-02: mm 단위, 소수점 3자리(#.###), 비율값→mm 변환 시 용지·margin 정보 필요
- PoC-03: 폰트는 pt만 사용, CSS/인쇄와 일치
- CleverOne 정밀도: Position/Size 1자리, Spacing/Thickness 등 3자리, Annotation Points 4자리 → 통합 시 3자리로 수용·반올림 정책 명시

**렌더링 및 UI**

- PoC-04: HTML DOM + SVG이므로 요소 타입이 DOM 노드(div, img, svg)와 1:1 대응 가능하도록 설계
- PoC-05: ImageBox는 html2canvas·cornerstone 연동, TextBox는 Lexical 연동을 전제로 content 구조 확장 가능하도록 유지
- DragResizeDiv 호환: position/size 기반이므로 px 변환은 렌더 시 mm→px만 수행

**제품별 특수성**

- E2: Paper, ImageBox, TextBox 중심, Template 없음
- E3: ItemBox(Text/Image), AutoFill, Layout(Row/Column), 6종 Annotation, CapturedImageInfo
- EzOrtho: Label, TextBox, ImageBox, ToothBox, TreatmentCategory, Block, Form Controls, Annotations(FreeDraw, Lines, Ellipse, Rectangle)
- CleverOne: TextBox(HTML), ImageBox(동일 확장), ToothBox(ToothCode), Annotations 4종, Groups

**Migration 및 버전**

- PoC-07: E2/E3/EzOrtho/CleverOne→Cloud 변환 시 본 스키마가 목표 포맷이 됨
- 스키마 버전(schemaVersion)으로 하위 호환·마이그레이션 경로 관리
- 제품별 확장은 `extensions.e2`, `extensions.cleverOne` 등으로 분리해 스키마 안정성 유지

**확장 및 미래**

- 신규 Annotation 타입(예: 폴리라인), 신규 Content 타입(차트·테이블) 추가 시 type enum 확장 + 선택적 공통 베이스
- AI 분석·VR 연동 등은 메타데이터 또는 extensions로 첨부 가능하도록 설계

---

## 2. 통합 문서 스키마 (최상위)

### 2.1 문서 구조

```
document
├── schemaVersion      string   (예: "1.0.0")
├── metadata           DocumentMetadata
├── paper              Paper
├── pages              Page[]
└── [extensions]       제품/버전별 확장
```

### 2.2 DocumentMetadata

| 필드           | 타입              | 필수 | 설명                                   |
| -------------- | ----------------- | ---- | -------------------------------------- |
| version        | string            | Y    | 스키마 버전 (시맨틱 버저닝)            |
| product        | string            | N    | 출처 제품 (E2, E3, EzOrtho, CleverOne) |
| productVersion | string            | N    | 제품 버전                              |
| createdAt      | string (ISO 8601) | N    | 생성 일시                              |
| updatedAt      | string (ISO 8601) | N    | 수정 일시                              |
| locale         | string            | N    | 로케일 (예: ko_KR)                     |
| templateName   | string            | N    | 템플릿 이름                            |

### 2.3 Paper

| 필드        | 타입                      | 필수 | 설명      |
| ----------- | ------------------------- | ---- | --------- |
| size        | "A4" \| "A3" \| "Letter"  | Y    | 용지 크기 |
| orientation | "portrait" \| "landscape" | Y    | 방향      |
| margin      | Margin                    | Y    | 여백 (mm) |

**Margin** (단위 mm, PoC-02):

```typescript
interface Margin {
  unit: 'mm'
  left: number // #.###
  right: number
  top: number
  bottom: number
}
```

### 2.4 Page

| 필드         | 타입      | 필수 | 설명                  |
| ------------ | --------- | ---- | --------------------- |
| number       | number    | Y    | 페이지 번호 (1-based) |
| templateName | string    | N    | 페이지 템플릿 이름    |
| elements     | Element[] | Y    | 요소 목록             |
| [extensions] | object    | N    | 제품별 확장           |

---

## 3. 공통 Element 속성

모든 요소는 **공통 필드**를 가지며, `type`으로 구체 타입이 결정됩니다.

### 3.1 공통 필드 (CommonElementBase)

| 필드       | 타입                    | 필수 | 설명                         |
| ---------- | ----------------------- | ---- | ---------------------------- |
| id         | string                  | Y    | 문서 내 유일 ID              |
| type       | ElementType             | Y    | 요소 타입 (디스크리미네이터) |
| position   | Position                | Y    | 좌표 (mm)                    |
| size       | Size                    | Y    | 크기 (mm)                    |
| style      | ElementStyle            | N    | 공통 스타일                  |
| locked     | boolean                 | N    | 편집 잠금                    |
| visible    | boolean                 | N    | 기본 true                    |
| zIndex     | number                  | N    | 겹침 순서                    |
| extensions | Record<string, unknown> | N    | 제품/기능별 확장             |

### 3.2 Position & Size (PoC-02 반영)

```typescript
interface Position {
  unit: 'mm'
  x: number // 소수점 3자리
  y: number
}

interface Size {
  unit: 'mm'
  width: number
  height: number
}
```

- 단위는 항상 `mm`, 정밀도는 0.001mm(1μm) 권장.

### 3.3 ElementStyle (PoC-03 반영)

| 필드                   | 타입                                      | 단위 | 설명             |
| ---------------------- | ----------------------------------------- | ---- | ---------------- |
| fontSize               | number                                    | pt   | 폰트 크기        |
| fontFamily             | string                                    | -    | 폰트명           |
| fontStyle              | "normal" \| "italic"                      | -    | 스타일           |
| fontWeight             | number \| string                          | -    | 굵기             |
| color                  | string                                    | -    | 전경색 (#RRGGBB) |
| backgroundColor        | string                                    | -    | 배경색           |
| backgroundColorOpacity | number                                    | 0~1  | 배경 불투명도    |
| borderColor            | string                                    | -    | 테두리 색        |
| borderWidth            | number                                    | mm   | 테두리 두께      |
| borderStyle            | "none" \| "solid" \| "dashed" \| "dotted" | -    | 테두리 스타일    |
| textAlign              | "left" \| "center" \| "right"             | -    | 텍스트 정렬      |
| verticalAlign          | "top" \| "middle" \| "bottom"             | -    | 세로 정렬        |

- `fontSize`만 pt, 나머지 길이는 mm 또는 단위 없음.

### 3.4 ElementType (통합 타입 목록)

```typescript
type ElementType =
  | 'imageBox'
  | 'textBox'
  | 'label'
  | 'toothBox'
  | 'treatmentCategory'
  | 'block'
  | 'rectangle'
  | 'ellipse'
  | 'line'
  | 'arrow'
  | 'freeDraw'
  | 'memo'
  | 'formControl' // 하위 타입으로 구체화
  | 'image' // 단순 이미지 (EzOrtho)
  | 'group' // CleverOne Groups
```

### 3.5 애플리케이션별 ElementType 지원 현황

| ElementType          | E2  | E3  | EzOrtho | CleverOne      |
| -------------------- | --- | --- | ------- | -------------- |
| imageBox (Single)    | O   | O   | O       | O              |
| imageBox (Multi)     | X   | O   | X       | O              |
| imageBox (Reference) | X   | O   | X       | O              |
| textBox              | O   | O   | O       | O              |
| label                | O   | O   | O       | textBox로 대체 |
| toothBox             | X   | X   | O       | O              |
| treatmentCategory    | X   | X   | O       | X [P2]         |
| block                | X   | X   | O       | X              |
| rectangle            | X   | O   | O       | O              |
| ellipse              | X   | O   | O       | X              |
| line                 | X   | O   | O       | O              |
| arrow                | X   | O   | X       | X              |
| freeDraw             | X   | O   | O       | O              |
| memo                 | X   | O   | X       | O              |
| formControl          | X   | X   | O       | X              |
| image                | X   | X   | O       | X              |
| group                | X   | X   | X       | O              |

- O: 지원, X: 미지원. 셀에 설명이 있는 경우 해당 앱에서의 대체 표현 또는 비고.
- [P2]: Priority 2 구현 요소. 스키마에 포함하되 구현 우선순위 낮음 (전문적/특수 용도).

---

## 4. 타입별 Element 스키마

### 4.1 ImageBox

| 필드                 | 타입                                    | 필수 | 설명                                                   |
| -------------------- | --------------------------------------- | ---- | ------------------------------------------------------ |
| ...CommonElementBase |                                         | Y    | 공통 속성                                              |
| type                 | "imageBox"                              | Y    |                                                        |
| fitMode              | "realSize" \| "boxFit" \| "modified"    | Y    | 이미지 맞춤 방식                                       |
| source               | "upload" \| "capture" \| "reference"    | N    | 이미지 출처                                            |
| imageRefs            | string[]                                | N    | 이미지 ID 또는 URL 목록 (Multi 시)                     |
| layout               | { row: number, column: number }         | N    | Multi 시 행/열 (1~20). Single은 생략 가능(생략 시 1×1) |
| translation          | { x: number, y: number }                | N    | mm 단위 이동                                           |
| scale                | { x: number, y: number }                | N    | 배율                                                   |
| invert               | boolean                                 | N    | 색 반전                                                |
| showRuler            | boolean \| { top, bottom, left, right } | N    | 눈금 표시                                              |
| capturedImageInfo    | CapturedImageInfo                       | N    | DICOM/캡처 메타 (CleverOne)                            |
| autoFill             | AutoFill                                | N    | E3/CleverOne 자동 채우기                               |
| linkedBoxId          | string                                  | N    | Reference ImageBox인 경우 참조 Box ID                  |

**Multi ImageBox란?**

- **한 번에 여러 장을 격자로 표시**한다. 박스를 Row×Column **셀**로 나누고, 각 셀에 `imageRefs`의 이미지를 하나씩 배치한다. 예: layout 2×3 → 6개 셀, 6장을 2행 3열로 동시에 표시.
- **기존 문서**: E3 RC Report는 "Image의 Cell 분할(Row & Column)", CleverOne은 "Multi Layout인 경우 Image File이 layout 갯수만큼 입력"으로 정의. **한 장씩 넘겨 보는 슬라이더/좌우 버튼은 포맷에 없음.** 필요 시 렌더링 단계에서 슬라이더·페이징 등을 추가할 수 있음.

**Reference ImageBox란?**

- **자신은 이미지 소스를 가지지 않는다.** 다른 ImageBox 하나를 `linkedBoxId`로 가리키고, 그 박스가 보여 주는 이미지를 그대로(또는 동기화된 뷰로) 표시한다.
- **용도**: 메인 이미지 박스(보통 Multi) 옆에 "참조용" 작은 뷰를 두는 경우. 예: MPR 메인 뷰 + Reference MPR, Scout 메인 + Reference Scout. CleverOne 포맷 문서에는 "Reference: Multi Image Box와 함께 Insert되는 Reference Image Box"로 정의되어 있음.
- **정리**: Single/Multi는 각자 이미지 목록을 갖고, Reference는 `linkedBoxId`가 가리키는 **한 개의 ImageBox**와 같은 소스를 공유하는 "연결된 뷰"이다.

**CapturedImageInfo** (CleverOne 호환):

```typescript
interface CapturedImageInfo {
  needToDrawInfo?: boolean
  spacing?: { x: number; y: number } // mm, 소수점 3자리
  thickness?: number
  interval?: number
  totalSliceNumber?: number
  directionTitle?: string
  sliceNumbers?: number[]
}
```

**AutoFill** (E3/CleverOne):

```typescript
interface AutoFill {
  tabType?: string // MPR 등
  viewType?: string
  groupType?: string
  withOverlay?: boolean
  applyFilter?: boolean
}
```

### 4.2 TextBox

| 필드                 | 타입      | 필수 | 설명                                   |
| -------------------- | --------- | ---- | -------------------------------------- |
| ...CommonElementBase |           | Y    |                                        |
| type                 | "textBox" | Y    |                                        |
| content              | string    | Y    | HTML 문자열 (Lexical/리치 텍스트 호환) |
| textMacro            | string    | N    | 매크로 이름 (PatientInfo 등)           |
| editable             | boolean   | N    | 기본 true                              |
| placeholder          | string    | N    | placeholder 텍스트                     |

### 4.3 Label

| 필드                 | 타입    | 필수 | 설명        |
| -------------------- | ------- | ---- | ----------- |
| ...CommonElementBase |         | Y    |             |
| type                 | "label" | Y    |             |
| content              | string  | Y    | 평문 텍스트 |

### 4.4 ToothBox

| 필드                        | 타입       | 필수 | 설명                      |
| --------------------------- | ---------- | ---- | ------------------------- |
| ...CommonElementBase        |            | Y    |                           |
| type                        | "toothBox" | Y    |                           |
| selectedToothCodes          | string[]   | N    | 선택된 치아 코드 (FDI 등) |
| selectedOcclusionToothCodes | string[]   | N    | 교합 측 치아 (예: "21_2") |

### 4.5 TreatmentCategory (EzOrtho) **[P2]**

| 필드                 | 타입                | 필수 | 설명       |
| -------------------- | ------------------- | ---- | ---------- |
| ...CommonElementBase |                     | Y    |            |
| type                 | "treatmentCategory" | Y    |            |
| category1            | string              | N    | 1단계 분류 |
| category2            | string              | N    | 2단계 분류 |
| category3            | string              | N    | 3단계 분류 |
| placeholder          | string              | N    |            |

**P2 (구현 우선순위 낮음)**: 매우 전문적인 EzOrtho 구강외과 수술 분류 전용 요소. 일반 리포트에서는 사용되지 않으며, EzOrtho Treatment Chart Migration 시에만 필요. 스키마 완성도를 위해 포함하되, 구현 우선순위는 낮음.

### 4.6 Annotation 공통 및 타입별

공통: `type`, `position`, `size`(또는 points), `style`(선 색·두께·스타일).

| type      | 추가 필드                  | 설명                   |
| --------- | -------------------------- | ---------------------- |
| rectangle | -                          | 직사각형, size 사용    |
| ellipse   | -                          | 타원, size 사용        |
| line      | points: [x1,y1, x2,y2]     | 직선, mm 좌표          |
| arrow     | points: [x1,y1, x2,y2]     | 화살표, points로 방향  |
| freeDraw  | points: string \| number[] | path 또는 점 배열 (mm) |
| memo      | points, content: string    | 풍선 텍스트 + 포인터   |

**points** 형식: `"x1,y1|x2,y2|..."` 또는 `[x1,y1,x2,y2,...]`, 단위 mm, 소수점 3자리.

### 4.7 Block (EzOrtho)

| 필드                 | 타입     | 필수 | 설명                              |
| -------------------- | -------- | ---- | --------------------------------- |
| ...CommonElementBase |          | Y    |                                   |
| type                 | "block"  | Y    |                                   |
| children             | string[] | N    | 자식 요소 ID 목록 (중첩 레이아웃) |

### 4.8 Group (CleverOne)

여러 요소를 하나의 단위로 다루기 위한 컨테이너. 그룹 선택 시 멤버 전체가 함께 이동·삭제·잠금 처리되며, 편집기에서 일괄 선택/해제에 사용한다.

**CleverOne 포맷 문서 출처** (Confidential_CleverOne_Report Format, Example.xml)

- **목적**: "Group 동작을 지원하기 위해" Groups/Group 요소가 추가됨 (v1.5.0). 포맷 문서에는 "함께 이동" 등 구체적 UI 동작은 없고, 데이터 구조만 정의됨.
- **구조**: `Groups`는 Group 요소들의 컨테이너. 각 `Group`은 **Content(텍스트 노드)** 로 그룹에 포함된 element의 **BoxID**를 `|`로 구분해 가짐. 예: `<Gruop>60|61|59</Gruop>` (예제 XML에는 Gruop 오타 있음).
- **통합 스키마 매핑**: BoxID 목록 → `memberIds` (string[]).

| 필드                 | 타입     | 필수 | 설명                       |
| -------------------- | -------- | ---- | -------------------------- |
| ...CommonElementBase |          | Y    |                            |
| type                 | "group"  | Y    |                            |
| memberIds            | string[] | Y    | 그룹에 포함된 요소 ID 목록 |

### 4.9 Form Controls (EzOrtho)

`type: "formControl"` + `controlType`으로 구분.

| controlType | 추가 필드                            | 설명         |
| ----------- | ------------------------------------ | ------------ |
| radio       | options: string[], value?: string    | 라디오 버튼  |
| checkbox    | checked?: boolean, label?: string    | 체크박스     |
| button      | label: string, action?: string       | 버튼         |
| comboBox    | options: string[], value?: string    | 콤보박스     |
| textInput   | value?: string, placeholder?: string | 한 줄 입력   |
| textArea    | value?: string, placeholder?: string | 여러 줄 입력 |

### 4.10 Image (EzOrtho 단순 이미지)

| 필드                 | 타입    | 필수 | 설명                                                  |
| -------------------- | ------- | ---- | ----------------------------------------------------- |
| ...CommonElementBase |         | Y    |                                                       |
| type                 | "image" | Y    |                                                       |
| source               | string  | Y    | 앱 번들 리소스 경로 (예: `:/images/img/img_face.png`) |

**Image 요소란?**

- **ImageBox와 구분**: ImageBox는 캡처/DICOM/자동채우기 등 **의료 이미지**를 다루고, Image는 **위치·크기만 있는 단순 이미지** 한 장을 표시한다. 편집·윈도잉·레이아웃 등은 없음.
- **고정 요소**: EzOrthoWeb에서 `fixed: true`로 구현되어 **사용자가 이동·크기조정 불가**. 템플릿에 포함된 정적 장식/참조 이미지용.

**EzOrthoWeb 소스코드 분석 결과**:

- **클래스**: `ChartElementImage extends ChartElementBase`
- **Source 형식**: `":/images/img/img_face.png"` (특별한 경로 포맷)
- **로딩 방식**: webpack의 `require.context('@/assets/images/img/', false, /\.png$/)`로 앱 번들 정적 리소스 로딩
- **제한사항**:
  - 현재 `:/images/img/` 경로만 지원
  - PNG 파일만 지원 (`/\.png$/`)
  - 런타임 동적 이미지 추가 불가
- **사용 예시**:

  ```xml
  <!-- 단독 사용 -->
  <Image Source=":/images/img/img_face.png" Left="0" Top="0" Width="60" Height="80"/>

  <!-- Block 내부 사용 (주요 패턴) -->
  <Block Name="Face" IsVisible="true" Left="5" Top="12">
    <Image Source=":/images/img/img_face.png" Left="0" Top="0" Width="60" Height="80"/>
    <Lines>...</Lines>
    <TextBox>...</TextBox>
  </Block>
  ```

- **fallback**: 이미지 로딩 실패 시 `@/assets/img/img_yet.png` 표시

**통합 스키마 고려사항**:

- **현재 구현**: 앱 번들 정적 리소스만 지원 (제한적)
- **향후 확장**: URL/동적 파일 경로 지원 가능하도록 설계
- **Migration**: EzOrtho → Cloud 시 정적 리소스 → 클라우드 스토리지 경로로 변환 필요

---

## 5. JSON Schema 요약 (핵심만)

- **document**: `schemaVersion`, `metadata`, `paper`, `pages` 필수.
- **paper**: `size`, `orientation`, `margin` 필수; `margin`은 `{ unit: "mm", left, right, top, bottom }`.
- **page**: `number`, `elements` 필수; `elements`는 배열.
- **element**: `id`, `type`, `position`, `size` 필수; `position`/`size`는 `{ unit: "mm", x, y }` / `{ unit: "mm", width, height }`.
- **style**: `fontSize`(number, pt), `fontFamily`, `color`, `backgroundColor`, `borderColor`, `borderWidth`, `borderStyle` 등 선택.
- **타입별**: `type` enum으로 oneOf/디스크리미네이터 적용 후, 타입별 추가 속성 정의.

(전체 JSON Schema는 별도 파일 `report-schema-v1.json` 등으로 두고, 여기서는 구조만 명시.)

---

## 6. TypeScript 타입 정의 (핵심)

```typescript
// 단위 명시 (PoC-02, PoC-03)
type UnitMm = { unit: 'mm'; x: number; y: number }
type SizeMm = { unit: 'mm'; width: number; height: number }
type MarginMm = { unit: 'mm'; left: number; right: number; top: number; bottom: number }

// 공통
interface Position extends UnitMm {
  x: number // #.###
  y: number
}
interface Size extends SizeMm {}
interface ElementStyle {
  fontSize?: number // pt
  fontFamily?: string
  color?: string
  backgroundColor?: string
  borderColor?: string
  borderWidth?: number
  borderStyle?: 'none' | 'solid' | 'dashed' | 'dotted'
  textAlign?: 'left' | 'center' | 'right'
  // ...
}

interface CommonElementBase {
  id: string
  type: ElementType
  position: Position
  size: Size
  style?: ElementStyle
  locked?: boolean
  visible?: boolean
  zIndex?: number
  extensions?: Record<string, unknown>
}

// 타입별 (유니온)
interface ImageBoxElement extends CommonElementBase {
  type: 'imageBox'
  fitMode: 'realSize' | 'boxFit' | 'modified'
  imageRefs?: string[]
  layout?: { row: number; column: number }
  translation?: { x: number; y: number }
  scale?: { x: number; y: number }
  capturedImageInfo?: CapturedImageInfo
  autoFill?: AutoFill
  // ...
}

interface TextBoxElement extends CommonElementBase {
  type: 'textBox'
  content: string
  textMacro?: string
  editable?: boolean
}

// ... (나머지 타입 동일 패턴)

type Element =
  | ImageBoxElement
  | TextBoxElement
  | LabelElement
  | ToothBoxElement
  | TreatmentCategoryElement
  | BlockElement
  | RectangleAnnotation
  | EllipseAnnotation
  | LineAnnotation
  | ArrowAnnotation
  | FreeDrawAnnotation
  | MemoAnnotation
  | FormControlElement
  | ImageElement
  | GroupElement

interface Page {
  number: number
  templateName?: string
  elements: Element[]
  extensions?: Record<string, unknown>
}

interface Document {
  schemaVersion: string
  metadata: DocumentMetadata
  paper: Paper
  pages: Page[]
  extensions?: Record<string, unknown>
}
```

---

## 7. 호환성 매트릭스

| Element 타입         | E2  | E3  | EzOrtho | CleverOne | 비고                  |
| -------------------- | --- | --- | ------- | --------- | --------------------- |
| imageBox (Single)    | O   | O   | O       | O         | 공통                  |
| imageBox (Multi)     | -   | O   | -       | O         | layout.row/column     |
| imageBox (Reference) | -   | O   | -       | O         | linkedBoxId           |
| textBox              | O   | O   | O       | O         | content HTML          |
| label                | O   | O   | O       | -         | CleverOne는 textBox로 |
| toothBox             | -   | -   | O       | O         | toothCode 호환        |
| treatmentCategory    | -   | -   | O       | -         | EzOrtho 전용          |
| block                | -   | -   | O       | -         | EzOrtho               |
| group                | -   | -   | -       | O         | memberIds             |
| rectangle            | -   | O   | O       | O         | Annotation            |
| ellipse              | -   | O   | O       | -         | CleverOne는 미지원    |
| line                 | -   | O   | O       | O         |                       |
| arrow                | -   | O   | -       | -         | CleverOne 미지원      |
| freeDraw             | -   | O   | O       | O         |                       |
| memo                 | -   | O   | -       | O         |                       |
| formControl          | -   | -   | O       | -         | EzOrtho               |
| image                | -   | -   | O       | -         | 단순 이미지           |

- O: 지원, -: 해당 제품에 해당 타입 없음 또는 대체 요소로 표현.

---

## 8. Migration 매핑 테이블 (요약)

| 출처                          | 대상 필드                                       | 변환 규칙                                     |
| ----------------------------- | ----------------------------------------------- | --------------------------------------------- |
| E2/E3 BoxPosition (비율)      | position                                        | 비율→mm (paper.size, margin 사용)             |
| E3 RC/CleverOne Position      | position                                        | mm→mm, 정밀도 3자리로 확장                    |
| EzOrtho Left/Top/Width/Height | position, size                                  | mm→mm, 정밀도 확장                            |
| 공통 BorderLine/Background    | style                                           | borderColor, borderWidth, backgroundColor 등  |
| E3/CleverOne Font             | style.fontSize                                  | pt 유지 (PoC-03)                              |
| CleverOne ToothCode           | selectedToothCodes, selectedOcclusionToothCodes | 그대로 매핑                                   |
| CleverOne CapturedImageInfo   | imageBox.capturedImageInfo                      | 구조 그대로                                   |
| CleverOne Groups              | group.memberIds                                 | Gruop→group, ID 목록                          |
| EzOrtho Image Source          | image.source                                    | `:/images/img/` → 클라우드 스토리지 경로 매핑 |

(상세 변환 규칙은 PoC-07 산출물과 연동.)

---

## 9. 확장 가이드라인

1. **신규 Element 타입**: `ElementType`에 값 추가 후, 공통 베이스 + 타입 전용 필드 정의. 기존 타입과 동일한 `position`/`size`/`style` 규칙 유지.
2. **제품 전용 속성**: `extensions.<product>` 또는 `extensions.<feature>` 아래에 두어 스키마 버전과 무관하게 확장.
3. **스키마 버전**: `metadata.version` 또는 `document.schemaVersion` 올리고, Migration 경로를 PoC-07에 등록.
4. **하위 호환**: 새 필드는 optional, 기존 필드 삭제/이름 변경은 deprecated 경로를 거쳐 단계적 제거.
5. **구현 우선순위**:
   - **P1**: 범용적이고 필수적인 요소 (textBox, imageBox, annotation 등)
   - **P2**: 전문적/특수 용도 요소 (treatmentCategory 등). 스키마 포함하되 구현 우선순위 낮음. Migration 호환성 목적.

---

## 10. 검증 시나리오

1. **완전성**: E2/E3/EzOrtho/CleverOne 샘플 각 1건 이상을 통합 스키마로 변환했을 때 모든 필드가 매핑 가능한지 확인.
2. **Round-trip**: 기존 포맷→통합 JSON→(필요 시) 기존 포맷으로 복원 시 의미적 동등성 검증.
3. **JSON Schema 검증**: Ajv 등으로 문서 인스턴스 검증.
4. **TypeScript**: 위 타입으로 렌더러/마이그레이션 코드 컴파일 및 타입 체크.
5. **PoC-14 연계**: 통합 스키마 기반 React Element 렌더링 엔진과 연동 테스트.

---

## 11. 통합 스키마 JSON 예시 (모든 Element 타입 포함)

아래 예시는 통합 스키마에 정의된 **모든 Element 타입**을 한 페이지에 포함한 참고용 인스턴스입니다.

```json
{
  "schemaVersion": "1.0.0",
  "metadata": {
    "version": "1.0.0",
    "product": "SCP Cloud",
    "productVersion": "1.0",
    "createdAt": "2026-01-23T00:00:00Z",
    "locale": "ko_KR",
    "templateName": "AllElementsSample"
  },
  "paper": {
    "size": "A4",
    "orientation": "portrait",
    "margin": { "unit": "mm", "left": 10, "right": 10, "top": 15, "bottom": 10 }
  },
  "pages": [
    {
      "number": 1,
      "templateName": "AllElementsSample",
      "elements": [
        {
          "id": "label-1",
          "type": "label",
          "position": { "unit": "mm", "x": 10, "y": 10 },
          "size": { "unit": "mm", "width": 40, "height": 6 },
          "style": { "fontSize": 14, "fontFamily": "Arial", "fontWeight": "bold" },
          "content": "제목 라벨"
        },
        {
          "id": "textBox-1",
          "type": "textBox",
          "position": { "unit": "mm", "x": 10, "y": 18 },
          "size": { "unit": "mm", "width": 60, "height": 12 },
          "style": { "fontSize": 12, "fontFamily": "Arial", "backgroundColor": "#ffffff", "borderWidth": 1, "borderStyle": "solid" },
          "content": "<html><body>리치 텍스트 본문</body></html>",
          "textMacro": "PatientInfo",
          "editable": true
        },
        {
          "id": "imageBox-single",
          "type": "imageBox",
          "position": { "unit": "mm", "x": 10, "y": 32 },
          "size": { "unit": "mm", "width": 30, "height": 25 },
          "fitMode": "modified",
          "source": "capture",
          "imageRefs": ["image-ref-1"],
          "translation": { "x": 0, "y": 0 },
          "scale": { "x": 1, "y": 1 }
        },
        {
          "id": "imageBox-multi",
          "type": "imageBox",
          "position": { "unit": "mm", "x": 45, "y": 32 },
          "size": { "unit": "mm", "width": 60, "height": 25 },
          "fitMode": "boxFit",
          "source": "capture",
          "imageRefs": ["img-1", "img-2", "img-3", "img-4"],
          "layout": { "row": 2, "column": 2 }
        },
        {
          "id": "imageBox-reference",
          "type": "imageBox",
          "position": { "unit": "mm", "x": 110, "y": 32 },
          "size": { "unit": "mm", "width": 30, "height": 25 },
          "fitMode": "realSize",
          "source": "reference",
          "linkedBoxId": "imageBox-single"
        },
        {
          "id": "toothBox-1",
          "type": "toothBox",
          "position": { "unit": "mm", "x": 10, "y": 60 },
          "size": { "unit": "mm", "width": 50, "height": 15 },
          "selectedToothCodes": ["11", "12", "21", "22"],
          "selectedOcclusionToothCodes": ["15_2", "21_3"]
        },
        {
          "id": "treatmentCategory-1",
          "type": "treatmentCategory",
          "position": { "unit": "mm", "x": 65, "y": 60 },
          "size": { "unit": "mm", "width": 75, "height": 15 },
          "category1": "Orthognathic Surgery",
          "category2": "Mandibular Surgery",
          "category3": "Sagittal Split Ramus Osteotomy",
          "placeholder": "Treatment Category"
        },
        {
          "id": "image-1",
          "type": "image",
          "position": { "unit": "mm", "x": 145, "y": 60 },
          "size": { "unit": "mm", "width": 25, "height": 15 },
          "source": ":/images/img/img_face.png"
        },
        {
          "id": "block-1",
          "type": "block",
          "position": { "unit": "mm", "x": 10, "y": 78 },
          "size": { "unit": "mm", "width": 80, "height": 20 },
          "children": ["label-1", "textBox-1"]
        },
        {
          "id": "form-radio",
          "type": "formControl",
          "position": { "unit": "mm", "x": 10, "y": 100 },
          "size": { "unit": "mm", "width": 40, "height": 8 },
          "controlType": "radio",
          "options": ["옵션 A", "옵션 B", "옵션 C"],
          "value": "옵션 A"
        },
        {
          "id": "form-checkbox",
          "type": "formControl",
          "position": { "unit": "mm", "x": 55, "y": 100 },
          "size": { "unit": "mm", "width": 30, "height": 8 },
          "controlType": "checkbox",
          "label": "동의함",
          "checked": true
        },
        {
          "id": "form-button",
          "type": "formControl",
          "position": { "unit": "mm", "x": 90, "y": 100 },
          "size": { "unit": "mm", "width": 25, "height": 8 },
          "controlType": "button",
          "label": "확인",
          "action": "submit"
        },
        {
          "id": "form-comboBox",
          "type": "formControl",
          "position": { "unit": "mm", "x": 120, "y": 100 },
          "size": { "unit": "mm", "width": 30, "height": 8 },
          "controlType": "comboBox",
          "options": ["항목1", "항목2"],
          "value": "항목1"
        },
        {
          "id": "form-textInput",
          "type": "formControl",
          "position": { "unit": "mm", "x": 155, "y": 100 },
          "size": { "unit": "mm", "width": 25, "height": 8 },
          "controlType": "textInput",
          "value": "",
          "placeholder": "입력"
        },
        {
          "id": "form-textArea",
          "type": "formControl",
          "position": { "unit": "mm", "x": 185, "y": 100 },
          "size": { "unit": "mm", "width": 15, "height": 15 },
          "controlType": "textArea",
          "value": "",
          "placeholder": "여러 줄"
        },
        {
          "id": "ann-rectangle",
          "type": "rectangle",
          "position": { "unit": "mm", "x": 10, "y": 115 },
          "size": { "unit": "mm", "width": 25, "height": 15 },
          "style": { "borderColor": "#000000", "borderWidth": 1, "borderStyle": "solid" }
        },
        {
          "id": "ann-ellipse",
          "type": "ellipse",
          "position": { "unit": "mm", "x": 40, "y": 115 },
          "size": { "unit": "mm", "width": 25, "height": 15 },
          "style": { "borderColor": "#000000", "borderWidth": 1, "borderStyle": "solid" }
        },
        {
          "id": "ann-line",
          "type": "line",
          "position": { "unit": "mm", "x": 70, "y": 115 },
          "size": { "unit": "mm", "width": 25, "height": 0 },
          "points": "70,122.5|95,122.5",
          "style": { "borderColor": "#000000", "borderWidth": 1, "borderStyle": "solid" }
        },
        {
          "id": "ann-arrow",
          "type": "arrow",
          "position": { "unit": "mm", "x": 100, "y": 115 },
          "size": { "unit": "mm", "width": 25, "height": 5 },
          "points": "100,117.5|125,117.5",
          "style": { "borderColor": "#000000", "borderWidth": 1, "borderStyle": "solid" }
        },
        {
          "id": "ann-freeDraw",
          "type": "freeDraw",
          "position": { "unit": "mm", "x": 130, "y": 115 },
          "size": { "unit": "mm", "width": 25, "height": 15 },
          "points": "130,115|135,120|140,118|145,125|150,122",
          "style": { "borderColor": "#000000", "borderWidth": 1, "borderStyle": "solid" }
        },
        {
          "id": "ann-memo",
          "type": "memo",
          "position": { "unit": "mm", "x": 160, "y": 115 },
          "size": { "unit": "mm", "width": 30, "height": 18 },
          "points": "160,133|175,133",
          "content": "메모 텍스트",
          "style": { "borderColor": "#000000", "borderWidth": 1, "borderStyle": "solid", "backgroundColor": "#ffffcc" }
        },
        {
          "id": "group-1",
          "type": "group",
          "position": { "unit": "mm", "x": 10, "y": 135 },
          "size": { "unit": "mm", "width": 50, "height": 20 },
          "memberIds": ["ann-rectangle", "ann-ellipse", "ann-line"]
        }
      ]
    }
  ]
}
```

**포함된 Element 타입 요약**: label, textBox, imageBox(Single/Multi/Reference), toothBox, treatmentCategory, image, block, formControl(radio/checkbox/button/comboBox/textInput/textArea), rectangle, ellipse, line, arrow, freeDraw, memo, group.

---

## 12. 검증 도구 및 활용

1. **JSON Schema 검증**: `report-schema-v1.json` 작성 후 Ajv(`ajv`), `jsonschema` 등으로 `document` 객체 검증
2. **TypeScript**: 위 인터페이스를 `report-types.ts`로 두고, Migration·렌더러 코드에서 import 후 타입 체크
3. **스키마 생성**: `json-schema-to-typescript`로 JSON Schema → TS 타입 자동 생성 (PoC-01 워크플로와 동일)
4. **Round-trip 테스트**: 기존 XML → 통합 JSON (PoC-07 변환기) → JSON Schema 검증 → (선택) 역변환 후 동등성 비교

---

## 13. 결론 및 다음 단계

- **통합 Element 스키마**는 mm·pt 단위와 공통/타입별 구조를 명확히 하고, 제품별·기능별 확장은 `extensions`로 분리해 설계되었습니다.
- **구현 우선순위**: P1(범용 필수 요소)과 P2(전문/특수 요소) 구분으로 단계별 개발 가능. P2 요소(treatmentCategory 등)는 Migration 호환성을 위해 스키마 포함하되 구현 우선순위 낮음.
- **산출물**: (1) 통합 JSON Schema 초안(별도 파일 권장), (2) TypeScript 타입 정의(본 문서 6절), (3) 호환성 매트릭스(7절), (4) Migration 매핑 요약(8절), (5) 확장 가이드라인(9절), (6) 검증 시나리오(10절), (7) JSON 예시(11절), (8) 검증 도구 안내(12절).
- **다음 단계**: PoC-07(Migration 시스템)에서 상세 변환 규칙 및 검증, PoC-14(Element 렌더링 엔진)에서 위 스키마 기반 렌더링 및 DragResizeDiv Handler와의 호환성 보장.

---

**작성일**: 2026년 1월 23일  
**작성자**: Raymond  
**검토자**: -  
**승인자**: -
