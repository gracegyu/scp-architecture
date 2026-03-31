Engineering One Pager

**Project Name**: PoC-14: Element 렌더링 엔진 구현

**Date**: 2026년 1월 6일

**Submitter Info**: Raymond

**Project Description**: SCP Cloud Report의 핵심인 Element 렌더링 엔진을 TypeScript React 기반으로 구현합니다. 기존 ezorthoweb(Vue.js)의 Element 클래스 구조와 설계를 참고하여, Drawing Shape, Image, Text(HTML) 등 일반 리포트 Element를 렌더링하고 편집할 수 있는 시스템을 구축합니다. 각 Element의 Drag & Resize Handler(핸들러), 속성 편집, HTML 편집 등 완전한 편집 기능을 제공하는 렌더링 엔진을 설계하고 검증합니다. EzOrtho 분석 차트(Canvas 기반)는 현재 구현 범위 외이며, 추후 확장 대상입니다.

**Business and Marketing Justification**:

- **핵심 기능 구현**: 리포트 편집의 가장 중요한 기능으로 제품 성공의 핵심 요소
- **사용자 경험**: Desktop 제품과 동일한 편집 경험 제공으로 기존 사용자 만족도 확보
- **기술 경쟁력**: 웹에서 Desktop 수준의 고급 편집 기능 제공으로 경쟁 우위 확보
- **개발 효율성**: 기존 ezorthoweb의 검증된 클래스 구조 + **DragResizeDiv 700줄 완벽 Handler 시스템** 활용으로 개발 위험 최소화 및 개발 기간 대폭 단축
- **확장성**: 체계적인 Element 구조로 향후 신규 Element 추가 용이
- **플랫폼 통합**: Web/Desktop/Mobile에서 동일한 렌더링 엔진 사용으로 일관성 확보

**Risk Assessment**:

- **높은 리스크**:
  - Canvas vs SVG vs DOM 렌더링 방식별 성능 및 기능 제약
- **중간 리스크**:
  - 기존 Vue.js 구조의 TypeScript React 포팅 시 설계 변경 필요성
  - Element 간 상호 작용(z-index, 선택, 그룹핑) 복잡성
  - HTML 편집기 외부 컴포넌트 통합 이슈
- **저위험**:
  - 기존 ezorthoweb에서 검증된 Element 클래스 설계 존재
- **완화 방안**:
  - **DragResizeDiv.vue 완벽 포팅**: 700줄의 검증된 Handler 시스템 95% 재사용
  - ezorthoweb의 검증된 클래스 구조 최대한 활용
  - 단계적 Element 구현 (기본 Element부터 시작)
  - 렌더링 방식은 PoC-04 결과를 기반으로 결정

**Resource and Scheduling Details**:

- **기간**: 11주 (Week 6-16, 최장기 PoC)
  - **Phase 3 (Week 6-9)**: DragResizeDiv 포팅 + 기본 Element (PoC-06, PoC-07과 병행)
  - **Phase 4-5 (Week 10-14)**: 고급 Element + 통합 기능 (PoC-08~PoC-10와 병행)
  - **Phase 6 (Week 15-16)**: 최종 완성 + 검증 (PoC-11~PoC-13와 병행)
- **인력**:
  - Raymond (Frontend 아키텍트, Element 설계자, UI/UX 개발자 역할 겸임)
    - ezorthoweb Element 클래스 분석 및 TypeScript React 포팅 설계
    - Element 렌더링 엔진 구현
    - Drag & Resize Handler 시스템 구현
    - HTML 편집기 통합 및 검증
- **선행 요구사항**:
  - PoC-03 (DPI 및 렌더링 전략 결정) 완료
  - PoC-04 (렌더링 기술 선정) 완료
  - PoC-05 (외부 라이브러리 선정) 완료
- **Repository**: Monorepo로 개발, 완료 후 @ewoosoft/scp-report-library로 NPM Private Publish (PoC-08 반영)

**Technical Description**:

**선행 PoC 결과 반영 (PoC-01 ~ PoC-13)**:

| PoC    | 결정 사항                                           | PoC-14 반영                                                                             |
| ------ | --------------------------------------------------- | --------------------------------------------------------------------------------------- |
| PoC-01 | JSON 포맷, TypeScript 타입                          | document/element 구조 JSON, TS 인터페이스                                               |
| PoC-02 | mm 좌표, 소수점 3자리                               | position/size 단위 mm, 정밀도 #.###                                                     |
| PoC-03 | pt 폰트, 96 DPI 화면, @media print                  | 폰트 pt, mm2px 기준 96 DPI, 인쇄 스타일 분리                                            |
| PoC-04 | HTML DOM + SVG 렌더링                               | SVG 기반 Element 렌더링 확정 (Canvas 대안 제외)                                         |
| PoC-05 | Lexical(텍스트), Puppeteer(PDF), cornerstone(DICOM) | TextBox: Lexical 연동. PDF/이미지는 호스트 연동                                         |
| PoC-06 | 통합 Element 스키마 (document→paper→pages→elements) | 스키마 기반 렌더링. ElementType: imageBox, textBox, rectangle 등                        |
| PoC-07 | Migration 경로 (E2/E3/EzOrtho/CleverOne→Cloud)      | Migration 출력 JSON을 렌더링 엔진 입력으로 사용                                         |
| PoC-10 | window.print + @media print, 서버 Puppeteer PDF     | @media print CSS, mm/pt 단위로 출력 품질 보장                                           |
| PoC-11 | 입력 sanitization, 감사 콜백, XSS 방지              | TextBox HTML sanitization, onAuditEvent 콜백, dangerouslySetInnerHTML 금지(사용자 입력) |
| PoC-12 | 다국어(i18n), RTL                                   | 텍스트/레이블 i18n 키 연동, direction 속성                                              |
| PoC-13 | WCAG 2.1 AA, 접근성                                 | DOM+SVG 기반(PoC-04), ARIA, 키보드 네비게이션                                           |

**렌더링 엔진 입출력** (PoC-06 통합 스키마):

- **입력**: `Document` (schemaVersion, metadata, paper, pages). pages[].elements가 Element[]
- **출력**: React 컴포넌트 트리 (SVG/HTML). 인쇄 시 @media print (PoC-10)
- **설정** (PoC-11): `onAuditEvent?: (event: AuditEvent) => void` — OPEN/SAVE/DELETE/EXPORT/PRINT 시 호출

**기존 ezorthoweb Element 구조 분석**:

**1. 클래스 계층구조** (참고용):

```typescript
BaseModel (최상위 모델)
├── ChartBase (모든 chart element의 부모)
│   ├── TreatmentChart
│   ├── AnalysisChart (EzOrtho 분석 차트 전용 - 현재 구현 범위 외, 추후 확장)
│   └── HistoryChart
├── ChartArea (Header, Body, Footer 영역 관리)
├── ChartElementBase (모든 element의 부모 클래스)
│   ├── ChartElementLabel
│   ├── ChartElementTextBox
│   ├── ChartElementImageBox
│   ├── ChartElementToothBox (EzOrtho 특화)
│   ├── ChartElementTreatmentCategory (EzOrtho 특화)
│   ├── ChartElementRectangle (Annotation)
│   ├── ChartElementEllipse (Annotation)
│   ├── ChartElementFreeDraw (Annotation)
│   ├── ChartElementLine (Annotation)
│   ├── ChartElementLines (Multi Line)
│   ├── ChartElementBlock
│   ├── ChartElementRadioButton
│   ├── ChartElementCheckBox
│   ├── ChartElementButton
│   ├── ChartElementComboBox
│   ├── ChartElementImage
│   ├── ChartElementTextInput
│   ├── ChartElementTextArea
│   └── ChartElementCanvas (EzOrtho 분석 차트 전용 - 현재 구현 범위 외, 추후 확장)
└── 속성 클래스들
    ├── ChartFontAttr (폰트 속성)
    ├── ChartLineAttr (선 속성)
    ├── ChartFillAttr (채우기 속성)
    └── ChartPaperSetting (용지 설정)
```

**2. Element 타입 정의** (ezorthoweb 기준):

```typescript
export const ElementShape = {
  // 기본 Element
  Line: 'Line',
  Label: 'Label',
  TextBox: 'TextBox',
  ImageBox: 'ImageBox',

  // EzOrtho 특화 (일반 리포트용만)
  ToothBox: 'ToothBox',
  TreatmentCategory: 'TreatmentCategory',
  // Canvas Element는 현재 구현 범위 외: EzOrtho 분석 차트 전용, 추후 확장 대상

  // Annotation (E3 기준)
  Rectangle: 'Rectangle',
  Ellipse: 'Ellipse',
  FreeDraw: 'FreeDraw',
  Lines: 'Lines',

  // Form Controls (EzOrtho 특화)
  Block: 'Block',
  RadioButton: 'RadioButton',
  CheckBox: 'CheckBox',
  Button: 'Button',
  ComboBox: 'ComboBox',

  // 확장 Element
  Image: 'Image',
  TextArea: 'TextArea',
  TextInput: 'TextInput',
}
```

**기존 제품별 Element 매핑**:

**E2 Report v3.0**:

- ImageBox (기본 이미지 편집)
- TextBox (기본 텍스트 편집)

**E3 v5.1**:

- ItemBox (BoxType: Text, Image, Multi)
- Annotation (6가지 타입):
  - Rectangle
  - Ellipse
  - Line
  - Arrow (ezorthoweb에서 미구현 - 추가 필요)
  - FreeDraw
  - Memo (ezorthoweb에서 미구현 - 추가 필요)

**RC Report v5.1** (현재 구현 범위 외, 추후 확장 대상):

- ItemBox (BoxType: Text, Image, Multi)
- Annotation (6가지 타입): Rectangle, Ellipse, Line, Arrow, FreeDraw, Memo
- Template 시스템: 동적 Layout 지원
- Auto Fill: TabType, ViewType, GroupType, WithOverlay, ApplyFilter
- Capture & Fill Image: Image Box Capture 기능

**EzOrtho v1.0** (ezorthoweb에서 완전 구현):

- TextBox (다양한 Form Controls)
- ImageBox
- ToothBox (치아 선택 특화)
- TreatmentCategory (치료 분류)
- Form Controls: Label, RadioButton, CheckBox, Button, ComboBox, TextInput, TextArea
- Canvas (EzOrtho 분석 차트 전용 - 현재 구현 범위 외, 추후 확장 대상)
- Block (요소 그룹핑)
- Annotation: FreeDraw, Ellipse, Rectangle

**CleverOne v5.1.0**:

- TextBox: TextMacro (PatientInfo, ReportDate, ClinicName 등), Editable
- ImageBox: ImageFitMode, Invert, ImageMacro (ClinicLogo), BoxType (Single, Multi, Reference), Source (None, Capture, AutoFill), Layout (Row, Column), Translation (TransX, TransY), Scale (ScaleX, ScaleY), Ruler (Top, Bottom, Left, Right), CapturedImageInfo (NeedToDrawInfo, Thickness, Interval, TotalSliceNumber, DirectionTitle, SpacingX/Y, SliceNumbers)
- ToothBox: ToothCode (SelectedToothCode, SelectedOcclusionToothCode)
- Annotation: AnnotationType (Rectangle, Ellipse, Line, Arrow, FreeDraw, Memo), LineWidth, LineType, LineColor, Points
- Memo: FontSize, FontColor, BackgroundColor, BackgroundOpacity
- Groups: Group (BoxID 목록)

**누락된 Element (구현 필요)**:

**1. E3에서 누락**:

- **Arrow**: Line과 유사하지만 화살표 머리 표시 기능
- **Memo**: Text가 포함된 풍선형 Annotation

**2. E3 ImageBox 서브타입**:

- **Single ImageBox**: 단일 이미지 (ezorthoweb ImageBox와 유사)
- **Multi ImageBox**: 1~20 Row/Column 레이아웃 (ezorthoweb에서 미구현)
- **Reference ImageBox**: 다른 ImageBox 참조 (ezorthoweb에서 미구현)

**TypeScript React 기반 Element 렌더링 엔진 설계**:

**1. DragResizeDiv 기반 Core Architecture**:

```typescript
// DragResizeDiv.vue 포팅용 Element 인터페이스
interface ElementComponent {
  id: string
  shape: string // DragResizeDiv의 shape prop과 호환
  x1: number // DragResizeDiv의 x1, y1, x2, y2 구조 유지
  y1: number
  x2: number
  y2: number
  properties: ElementProperties
  editable: boolean
  selected: boolean
  getFixed: boolean // DragResizeDiv의 Fixed Element 처리
}

// DragResizeDiv Handler 시스템 (기존 구조 그대로)
type HandlePosition = 'tl' | 'tm' | 'tr' | 'ml' | 'mr' | 'bl' | 'bm' | 'br'

interface HandleStyle {
  position: 'absolute'
  left: string
  top: string
  width: string
  height: string
  background: string
  border: string
  cursor: string
  zIndex: number
}

// DragResizeDiv 이벤트 시스템 (ezorthoweb과 동일)
interface DragResizeEvents {
  onDragging: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onDragStop: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onResizing: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onResizeStop: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onActivated: () => void
  onDeactivated: () => void
}
```

**2. Element 렌더링 전략**:

**SVG 기반 렌더링** (PoC-04 선정: HTML DOM+SVG 확정):

```typescript
// Element 컴포넌트 예시
const RectangleElement: React.FC<ElementProps> = ({ element, selected, onUpdate }) => {
  return (
    <g>
      <rect
        x={element.position.x}
        y={element.position.y}
        width={element.size.width}
        height={element.size.height}
        fill={element.properties.fillColor}
        stroke={element.properties.borderColor}
        strokeWidth={element.properties.borderWidth}
      />
      {selected && <ResizeHandlers element={element} onResize={onUpdate} />}
    </g>
  )
}
```

(PoC-04에서 Canvas는 대안으로 검토되었으나 DOM+SVG 선정. 접근성·텍스트 품질·인쇄 품질 우수.)

**Canvas 기반 렌더링** (현재 범위 외, 대량 Element 100개 이상 시 하이브리드 검토):

```typescript
class CanvasElementRenderer {
  drawElement(ctx: CanvasRenderingContext2D, element: ElementComponent) {
    switch (element.type) {
      case 'rectangle':
        this.drawRectangle(ctx, element)
        break
      case 'ellipse':
        this.drawEllipse(ctx, element)
        break
      // ... 기타 타입들
    }
  }

  drawHandlers(ctx: CanvasRenderingContext2D, element: ElementComponent) {
    if (element.selected) {
      this.drawResizeHandlers(ctx, element)
    }
  }
}
```

**3. DragResizeDiv.vue Handler 시스템 포팅**:

**기존 DragResizeDiv 구조 TypeScript 타입 정의**:

```typescript
// DragResizeDiv.vue의 handles 시스템 포팅
type HandlePosition = 'tl' | 'tm' | 'tr' | 'ml' | 'mr' | 'bl' | 'bm' | 'br'

interface DragResizeDivProps {
  x1: number
  y1: number
  x2: number
  y2: number
  shape: string
  zoom: number
  handles: HandlePosition[]
  draggable: boolean
  resizable: boolean
  element: any
  parentWidth?: number
  parentHeight?: number
  parentHeader?: number
  parentFooter?: number
  onDragging?: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onDragStop?: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onResizing?: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onResizeStop?: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onActivated?: () => void
  onDeactivated?: () => void
}

// DragResizeDiv 상태 (ezorthoweb data 포팅)
interface DragResizeState {
  nx1: number
  ny1: number
  nx2: number
  ny2: number
  enabled: boolean
  resizing: boolean
  dragging: boolean
  isHover: boolean
  mouseClickPosition: {
    sx: number
    sy: number
    x1: number
    y1: number
    x2: number
    y2: number
  }
}

// Handle 설정 (ezorthoweb 기준)
const DEFAULT_HANDLES: HandlePosition[] = ['tl', 'tm', 'tr', 'mr', 'br', 'bm', 'bl', 'ml'] // 8개
const LINE_HANDLES: HandlePosition[] = ['tl', 'br'] // Line용 2개
```

**4. DragResizeDiv 기반 Element 구현 계획**:

**기본 Shape Elements** (DragResizeDiv 활용):

- **Rectangle**: 직사각형, DragResizeDiv의 8개 핸들러 (tl, tm, tr, ml, mr, bl, bm, br) 활용
- **Ellipse**: 타원형, DragResizeDiv의 8개 핸들러 활용
- **Line**: 선, DragResizeDiv의 Line 모드 (tl, br 2개 핸들러) 활용
- **Arrow**: Line + 화살표 머리, DragResizeDiv Line 모드(tl, br) 활용 (추가 구현 필요)

  ```typescript
  class ArrowElement extends ChartElementBase {
    public arrowHeadSize: number = 8
    public arrowHeadType: 'triangle' | 'diamond' = 'triangle'

    render(): React.ReactElement {
      return (
        <g>
          <line x1={this.x1} y1={this.y1} x2={this.x2} y2={this.y2} />
          <polygon points={this.getArrowHeadPoints()} fill={this.lineAttr.color} />
        </g>
      )
    }
  }
  ```

- **FreeDraw**: 자유 그리기, Path 기반

  ```typescript
  class FreeDrawElement extends ChartElementBase {
    public pathData: string // SVG path data
    public points: Coordinate[] // 그리기 점들

    render(): React.ReactElement {
      return <path d={this.pathData} fill='none' stroke={this.lineAttr.color} strokeWidth={this.lineAttr.thickness} />
    }
  }
  ```

- **Memo**: 풍선 텍스트 + 포인터, DragResizeDiv 8개 핸들러 + 포인터 이동 핸들러 (추가 구현 필요)

  ```typescript
  class MemoElement extends ChartElementBase {
    public text: string
    public pointerPosition: Coordinate
    public bubbleSize: Size

    render(): React.ReactElement {
      return (
        <g>
          {/* 풍선 배경 */}
          <rect {...this.bubbleSize} fill='white' stroke='black' />
          {/* 포인터 선 */}
          <line x1={this.position.x} y1={this.position.y} x2={this.pointerPosition.x} y2={this.pointerPosition.y} />
          {/* 텍스트 */}
          <foreignObject {...this.bubbleSize}>
            <div>{this.text}</div>
          </foreignObject>
        </g>
      )
    }

    // Memo는 DragResizeDiv 기본 8개 핸들러 + 포인터 별도 처리
    getDragResizeHandles(): HandlePosition[] {
      return ['tl', 'tm', 'tr', 'ml', 'mr', 'bl', 'bm', 'br'] // 풍선용 8개
    }

    getPointerHandle(): { x: number; y: number } {
      return this.pointerPosition // 포인터 위치는 별도 드래그 처리
    }
  }
  ```

**Content Elements** (DragResizeDiv 활용):

- **ImageBox**: DragResizeDiv로 감싼 이미지 표시 + 크기 조정
  - Single ImageBox: **구현됨** (`ImageBoxElement`, `Document.imageRefs` + `extensions.imageRef`/`fitMode`). 래스터 JPG·PNG 등은 `<img>`. DICOM은 현재 메타 패널 + 다운로드만; **리포트 내 픽셀 표시는 로드맵 Task 3.5**.
  - Multi ImageBox: 1~20 Row/Column 레이아웃 (추가 구현 필요, DragResizeDiv 활용)
  - Reference ImageBox: 다른 ImageBox 참조 (추가 구현 필요, DragResizeDiv 활용)
- **TextBox**: DragResizeDiv로 감싼 HTML 텍스트 편집
- **Label**: DragResizeDiv로 감싼 단순 텍스트

**EzOrtho 특화 Elements** (DragResizeDiv 활용):

- **ToothBox**: DragResizeDiv로 감싼 치아 선택 UI
- **TreatmentCategory**: DragResizeDiv로 감싼 치료 분류 선택
- **Form Controls**: 각각 DragResizeDiv로 감싼 RadioButton, CheckBox, Button, ComboBox, TextInput, TextArea
- **Block**: DragResizeDiv로 감싼 요소 그룹핑 컨테이너

**현재 구현 범위 외 사항** (추후 확장 대상):

- **Canvas Element**: EzOrtho 분석 차트 전용으로 별도 프로젝트에서 다룸 (추후 확장)
- **EzOrtho 분석 차트 관련 Element들**: 복잡한 분석 도구로 별도 개발 필요 (추후 확장)

**5. 좌표 시스템 통합** (PoC-02, PoC-03 연계):

```typescript
// PoC-06 통합 스키마와 동일 구조
interface Position {
  unit: 'mm'
  x: number // 소수점 3자리 (#.###)
  y: number
}

interface Size {
  unit: 'mm'
  width: number
  height: number
}

// PoC-03: 96 DPI 화면 기준
const DPMM = 96 / 25.4
class CoordinateSystem {
  static mm2px(val: number): number {
    return val * DPMM
  }
  static px2mm(val: number): number {
    return val / DPMM
  }
}
```

**6. HTML 편집기 통합**:

**선정**: **Lexical** (PoC-05 결과). React 통합, 성능·아키텍처 우수.

**HTML 편집기 통합 인터페이스**:

```typescript
interface HTMLEditor {
  content: string
  onChange: (content: string) => void
  config: HTMLEditorConfig
}

interface HTMLEditorConfig {
  toolbar: string[]
  allowedTags: string[]
  medicalTerms: boolean // 의료 용어 자동 완성
  spellCheck: boolean
}
```

**7. ezorthoweb에서 React로 포팅할 주요 클래스들**:

**BaseModel 포팅**:

```typescript
// ezorthoweb의 BaseModel을 TypeScript로 포팅 (PoC-03: 96 DPI 화면 기준)
abstract class BaseElement {
  protected _dpi = 96
  protected _mmpinch = 25.4
  protected _dpmm = this._dpi / this._mmpinch

  mm2px(val: number): number {
    return val * this._dpmm
  }

  px2mm(val: number): number {
    return val / this._dpmm
  }

  abstract getClassModel(): Record<string, any>
}
```

**ChartElementBase 포팅**:

```typescript
abstract class ChartElementBase extends BaseElement {
  public id: string
  public shape: ElementShape
  public position: Coordinate
  public size: Size
  public fontAttr: ChartFontAttr
  public lineAttr: ChartLineAttr
  public fillAttr: ChartFillAttr
  public editable: boolean
  public selected: boolean

  constructor(
    elementShape: ElementShape,
    element: any,
    areaObj: ChartArea,
    fontAttr: ChartFontAttr | null = null,
    fixed: boolean = false,
    block: ChartElementBlock | null = null,
  ) {
    super()
    this.shape = elementShape
    this.setupElement(element, areaObj, fontAttr, fixed, block)
  }

  abstract render(): React.ReactElement
  abstract getDragResizeHandles(): HandlePosition[] // DragResizeDiv handles prop
  abstract getShape(): string // DragResizeDiv shape prop
  abstract updatePosition(newPosition: Coordinate): void
  abstract updateSize(newSize: Size): void

  // DragResizeDiv props 생성
  getDragResizeProps(): Partial<DragResizeDivProps> {
    return {
      x1: this.position.x,
      y1: this.position.y,
      x2: this.position.x + this.size.width,
      y2: this.position.y + this.size.height,
      shape: this.getShape(),
      handles: this.getDragResizeHandles(),
      element: this,
    }
  }
}
```

**8. Element별 세부 구현 방안**:

**Rectangle Element**:

```typescript
class RectangleElement extends ChartElementBase {
  render(): React.ReactElement {
    return (
      <rect
        x={this.position.x}
        y={this.position.y}
        width={this.size.width}
        height={this.size.height}
        fill={this.fillAttr.color}
        stroke={this.lineAttr.color}
        strokeWidth={this.lineAttr.thickness}
        onMouseDown={this.handleMouseDown}
      />
    )
  }

  // DragResizeDiv 기본 핸들러 사용 (8개)
  getDragResizeHandles(): HandlePosition[] {
    return ['tl', 'tm', 'tr', 'ml', 'mr', 'bl', 'bm', 'br']
  }

  // DragResizeDiv shape 속성
  getShape(): string {
    return 'Rectangle' // DragResizeDiv에서 isLine 체크용
  }
}
```

**ImageBox Element** (Multi 타입 추가 구현):

```typescript
class ImageBoxElement extends ChartElementBase {
  public imageType: 'single' | 'multi' | 'reference'
  public source: string
  public fitMode: 'realSize' | 'boxFit' | 'modified'
  public layout?: { row: number; column: number } // Multi용 (PoC-06: 1~20)
  public linkedBoxId?: string // Reference용

  render(): React.ReactElement {
    switch (this.imageType) {
      case 'single':
        return this.renderSingleImage()
      case 'multi':
        return this.renderMultiImage()
      case 'reference':
        return this.renderReferenceImage()
    }
  }

  private renderMultiImage(): React.ReactElement {
    // 1~20 Row/Column 레이아웃 구현 (PoC-06 layout.row, layout.column)
    const { row, column } = this.layout!
    // 구현 로직
  }
}
```

**HTML TextBox Element**:

```typescript
class HTMLTextBoxElement extends ChartElementBase {
  public htmlContent: string
  public editorConfig: HTMLEditorConfig

  render(): React.ReactElement {
    return (
      <foreignObject x={this.position.x} y={this.position.y} width={this.size.width} height={this.size.height}>
        <div className='html-textbox'>
          {this.isEditing ? (
            <LexicalEditor value={this.htmlContent} onChange={this.handleContentChange} />
          ) : (
            // PoC-11: 사용자 입력 HTML은 sanitization 필수. DOMPurify 등 사용
            <div dangerouslySetInnerHTML={{ __html: sanitizeHtml(this.htmlContent) }} />
          )}
        </div>
      </foreignObject>
    )
  }
}
```

**9. Drag & Resize Handler 시스템**:

**Handler 렌더링**:

```typescript
const ResizeHandlers: React.FC<{ element: ChartElementBase }> = ({ element }) => {
  const handlers = element.getHandlers()

  return (
    <>
      {handlers.map((handler, index) => (
        <rect
          key={index}
          className='resize-handler'
          x={getHandlerX(element, handler.position) - 3}
          y={getHandlerY(element, handler.position) - 3}
          width={6}
          height={6}
          fill='white'
          stroke='blue'
          strokeWidth={1}
          cursor={handler.cursor}
          onMouseDown={(e) => startResize(e, element, handler)}
        />
      ))}
    </>
  )
}
```

**Drag 시스템**:

```typescript
class DragSystem {
  private dragState: {
    isDragging: boolean
    element: ChartElementBase | null
    startPosition: Coordinate
    startElementPosition: Coordinate
  } = {
    isDragging: false,
    element: null,
    startPosition: { x: 0, y: 0, unit: 'mm' },
    startElementPosition: { x: 0, y: 0, unit: 'mm' },
  }

  onMouseDown(event: MouseEvent, element: ChartElementBase) {
    this.dragState.isDragging = true
    this.dragState.element = element
    this.dragState.startPosition = this.getMousePosition(event)
    this.dragState.startElementPosition = element.position
  }

  onMouseMove(event: MouseEvent) {
    if (!this.dragState.isDragging) return

    const currentPosition = this.getMousePosition(event)
    const deltaX = currentPosition.x - this.dragState.startPosition.x
    const deltaY = currentPosition.y - this.dragState.startPosition.y

    this.dragState.element!.updatePosition({
      x: this.dragState.startElementPosition.x + deltaX,
      y: this.dragState.startElementPosition.y + deltaY,
      unit: 'mm',
    })
  }
}
```

**10. 상태 관리 시스템**:

**Element Store (Redux Toolkit 기준)**:

```typescript
interface ElementState {
  elements: Record<string, ChartElementBase>
  selectedElements: string[]
  clipboard: ChartElementBase[]
  history: {
    past: ElementState[]
    present: ElementState
    future: ElementState[]
  }
}

const elementSlice = createSlice({
  name: 'elements',
  initialState,
  reducers: {
    addElement: (state, action) => {
      const element = action.payload
      state.elements[element.id] = element
    },
    updateElement: (state, action) => {
      const { id, updates } = action.payload
      Object.assign(state.elements[id], updates)
    },
    deleteElement: (state, action) => {
      const id = action.payload
      delete state.elements[id]
    },
    selectElements: (state, action) => {
      state.selectedElements = action.payload
    },
  },
})
```

**11. 이벤트 처리 시스템**:

**Mouse Event Handling**:

```typescript
interface ElementEventHandler {
  onMouseDown: (event: MouseEvent, element: ChartElementBase) => void
  onMouseMove: (event: MouseEvent) => void
  onMouseUp: (event: MouseEvent) => void
  onDoubleClick: (event: MouseEvent, element: ChartElementBase) => void
  onContextMenu: (event: MouseEvent, element: ChartElementBase) => void
}

// 키보드 단축키
interface KeyboardHandler {
  Delete: () => void
  'Ctrl+C': () => void
  'Ctrl+V': () => void
  'Ctrl+Z': () => void
  'Ctrl+Y': () => void
  Escape: () => void
  ArrowUp: () => void
  ArrowDown: () => void
  ArrowLeft: () => void
  ArrowRight: () => void
}
```

**12. 렌더링 최적화 전략**:

**Virtual Rendering**:

```typescript
// 화면에 보이는 Element만 렌더링
const useVisibleElements = (elements: ChartElementBase[], viewport: Viewport) => {
  return useMemo(() => {
    return elements.filter((element) => isElementInViewport(element, viewport))
  }, [elements, viewport])
}

// Element 메모이제이션
const MemoizedElement = React.memo(ElementComponent, (prev, next) => {
  return (
    prev.element.position === next.element.position &&
    prev.element.size === next.element.size &&
    prev.element.properties === next.element.properties &&
    prev.selected === next.selected
  )
})
```

**13. 프로토타입 개발 범위**:

**Phase 1: 기본 Element**:

- Rectangle, Ellipse, Line 구현
- 기본 Handler 시스템
- 선택, 이동, 크기 조정 기능

**Phase 2: Content Element**:

- ImageBox (Single 타입)
- **속성 패널**(오른쪽 Inspector, 공통·타입별 필드)
- TextBox (기본 텍스트)
- HTML 편집기 통합

**Phase 3: 고급 Element**:

- Arrow, Memo 구현
- Multi ImageBox 구현
- FreeDraw 구현
- **ImageBox DICOM 픽셀 표시**(Task 3.5): 리포트 박스 내 영상 디코드·뷰포트(Cornerstone 계열 등)

**Phase 4: EzOrtho 특화** (일반 리포트용):

- ToothBox, TreatmentCategory
- Form Controls (RadioButton, CheckBox 등)
- EzOrtho 분석 차트(Canvas 기반)는 현재 구현 범위 외, 추후 확장 대상

**PoC-06 연동 보조 스펙 (로드맵 §16과 분리)**:

구현 스펙·데모 샘플 정책만 정리한다. §16 Phase 2 Task 2.1·2.2 수행 시 이 절을 참조한다.

### 속성 패널 (Element Inspector) — 설계·스펙

**목적**: 다이얼로그 없이 **선택한 Element의 PoC-06 JSON 속성**을 편집한다. Google Slides·Figma류 **오른쪽 도킹 패널**, **표시/숨김 토글**을 기본 UX로 한다.

**데이터 흐름**: `ReportRenderer`의 `selectedIds`·`onDocumentChange`를 호스트(예: `scp-cloud-demo` `App`)에서 유지. 패널은 `document`, `selectedId`(단일 선택 1차 범위), `onPatchElement` 콜백으로 **불변 갱신**(`pages[].elements`에서 id 매칭 후 얕은 복사로 `position`/`size`/`style`/`extensions`만 교체).

**공통 속성 중복 제거(구현 연구)**:

1. **필드 디스크립터**: `{ path, label, kind, options? }` 형태 배열로 정의. `path`는 `position.x`, `style.borderColor`, `extensions.lineEndpoints.x1` 같이 점 경로 또는 커스텀 getter/setter. `kind`는 `number`, `text`, `color`, `select`, `checkbox` 등.
2. **공통 섹션 한 컴포넌트**: `CommonElementFields`가 `CommonElementBase` + `ElementStyle`에 해당하는 디스크립터만 렌더. 타입별로 **같은 배열을 필터**하거나 **섹션 등록표**로 노출 필드를 제한(예: `line`은 채움 관련 `style.backgroundColor` 숨김).
3. **타입별 오버레이**: `inspectorSections[type] = [...추가 디스크립터]`로 `rectangle`/`ellipse`/`line`/`imageBox` 전용 필드만 합성. 신규 Element 추가 시 공통 재사용 + 오버레이만 추가.
4. **(선택) 패키지 분리**: `@ewoosoft/scp-report-components`에 `ElementInspector`를 두고 데모는 레이아웃·토글만 두어 **호스트 앱 재사용**을 허용. 초기에는 데모 전용으로 시작해도 됨.
5. **단위**: 좌표·크기는 **JSON과 동일하게 mm** 입력; 내부 렌더는 기존 `mm2px` 유지.

**다중 선택(범위 외 명시)**: 1차는 **단일 선택**만 패널 편집. 다중 선택 시 “N개 선택됨”만 표시하거나 비활성 — 로드맵 Task 2.5(상태 관리) 이후 확장 가능.

---

#### A. 공통 (모든 Element, `CommonElementBase` + `style` 일부)

| 순번 | JSON 경로 | 스펙 의미 | UI 제안 |
|------|-----------|-----------|---------|
| A1 | `id` | Element 고유 id | 읽기 전용 텍스트(수정 시 참조 깨짐 방지 정책 별도) |
| A2 | `type` | Element 종류 | 읽기 전용 |
| A3 | `position.unit` | 좌표 단위 | 고정 `mm`, 표시만 또는 숨김 |
| A4 | `position.x` | 왼쪽 기준 x (mm) | 숫자 입력 |
| A5 | `position.y` | 상단 기준 y (mm) | 숫자 입력 |
| A6 | `size.unit` | 크기 단위 | 고정 `mm` |
| A7 | `size.width` | 너비 (mm) | 숫자 입력 |
| A8 | `size.height` | 높이 (mm) | 숫자 입력 |
| A9 | `locked` | 편집 잠금 | 체크박스 |
| A10 | `visible` | 표시 여부 | 체크박스 |
| A11 | `zIndex` | 쌓임 순서 | 정수 입력(선택) |

`style`(`ElementStyle`)은 타입별로 아래 B와 조합해 노출한다. 렌더러는 `elementStyleToLineAttr` / `elementStyleToFillAttr` 등으로 매핑하므로 **패널에서도 동일 키**를 쓴다.

---

#### B. 선·채움 (`ElementStyle` ↔ LineAttr / FillAttr 매핑)

| 순번 | JSON (`style.*`) | 렌더 매핑 | UI 제안 |
|------|------------------|-----------|---------|
| B1 | `borderColor` | `lineAttr.color` | color |
| B2 | `borderWidth` | `lineAttr.thickness` | 숫자 (≥0) |
| B3 | `borderStyle` | `lineAttr.style` | 선택: none, solid, dashed, dotted |
| B4 | `backgroundColor` | `fillAttr.color` | color |
| B5 | `backgroundColorOpacity` | `fillAttr.opacity` | 숫자 0~1 (또는 0~100% 표시 후 변환) |

타입별로 B4·B5를 숨길지는 아래 C~F에 따름.

---

#### C. `rectangle` (현재 구현)

| 순번 | 출처 | 비고 |
|------|------|------|
| C1 | A1~A11 전부 | 공통 |
| C2 | B1~B5 전부 | 테두리 + 면 채움 |

(텍스트 전용 `style.fontSize` 등은 현재 `RectangleElement`에서 미사용 — 패널에 **미노출** 또는 “향후 TextBox” 접기 섹션.)

---

#### D. `ellipse` (현재 구현)

| 순번 | 출처 | 비고 |
|------|------|------|
| D1 | A1~A11 | 공통 |
| D2 | B1~B5 | rectangle과 동일 |

---

#### E. `line` (현재 구현)

| 순번 | JSON 경로 | 스펙 의미 | UI 제안 |
|------|-----------|-----------|---------|
| E1 | A1~A11 | 공통(바운딩 박스는 DragResize와 동기) | 동일 |
| E2 | B1~B3 | 선 색·굵기·점선 | 채움(B4·B5) **미노출** |
| E3 | `extensions.lineEndpoints.x1` | 끝점1 x (mm) | 숫자 |
| E4 | `extensions.lineEndpoints.y1` | 끝점1 y (mm) | 숫자 |
| E5 | `extensions.lineEndpoints.x2` | 끝점2 x (mm) | 숫자 |
| E6 | `extensions.lineEndpoints.y2` | 끝점2 y (mm) | 숫자 |

`extensions` 없을 때 생성 규칙은 기존 `ElementRegistry`와 동일하게 패치 시 보장.

---

#### F. `imageBox` — Single (현재 구현)

| 순번 | JSON 경로 | 스펙 의미 | UI 제안 |
|------|-----------|-----------|---------|
| F1 | A1~A11 | 공통 | 동일 |
| F2 | B1~B3 | 박스 테두리(`ImageBoxElement` 외곽 rect) | color/굵기/스타일 |
| F3 | B4·B5 | 면 채움 | 현재 내부 foreignObject 위주라 **선택**: 숨기거나 향후 배경용 |
| F4 | `extensions.imageBoxType` | single/multi/reference | 1차 **single 고정** 또는 읽기 전용 |
| F5 | `extensions.imageRef` | `Document.imageRefs` 키 | `Object.keys(document.imageRefs)` 셀렉트 + 직접 입력(키 문자열) |
| F6 | `extensions.fitMode` | realSize / boxFit / modified | 셀렉트 |

`imageRefs` 본문 편집은 패널에서 **별도 “문서 이미지 맵” 접기**로 URL 편집(고급)하거나 2차 Task로 분리.

### ImageBox(Single) — 데모 샘플·이미지 소스

- **데모 샘플**: `scp-cloud-demo/public/sample.jpg`, `sample.png`, `sample.dcm`. `sample-report.json`의 `imageRefs`: `sampleJpg`→`/sample.jpg`, `samplePng`→`/sample.png`, `sampleDcm`→`/sample.dcm`, 각각 대응 `type: imageBox` + `extensions.imageBoxType: single` + `imageRef` + `fitMode`.
- **이미지 소스(결정)**: 문서에 **바이트 저장 위치는 규정하지 않음**. 렌더러는 `imageRefs`와 `extensions.imageRef`로 최종 URL을 만든다. **PoC·데모**는 위 public 정적 파일·동일 출처 URL. **운영**: 호스트가 동일 필드에 S3·API URL 등을 채움.

**14. 테스트 계획**:

**기능 테스트**:

1. **Element 생성**: 모든 타입별 생성 기능
2. **편집 기능**: 이동, 크기 조정, 회전, 속성 변경
3. **선택 시스템**: 단일 선택, 다중 선택, 영역 선택
4. **복사/붙여넣기**: 클립보드 기능
5. **Undo/Redo**: 편집 히스토리 관리

**성능 테스트**:

1. **렌더링 성능**: 50개 Element 렌더링 시간
2. **편집 반응성**: 실시간 Drag 시 60fps 유지
3. **메모리 사용량**: Element 메모리 효율성

**호환성 테스트**:

1. **ezorthoweb 파일 로딩**: 기존 Vue.js 생성 파일 React에서 렌더링
2. **편집 결과 비교**: 동일한 편집 작업 후 결과물 비교
3. **브라우저 호환성**: Chrome, Firefox, Safari, Edge 테스트

**15. DragResizeDiv.vue 포팅 가능성 분석**:

**핵심 발견**: `src/controls/Chart/DragResizeDiv.vue` (700줄)에서 완벽한 Drag & Resize Handler 시스템 이미 구현됨

**✅ 포팅 가능한 부분 (대부분)**:

**핵심 로직 (순수 JavaScript)**:

- Drag & Resize 계산 로직 (deltaX, deltaY 계산)
- 좌표 변환 및 경계 검사 (부모 영역 제한)
- Handler 위치 계산 (8개 핸들러 + Line용 2개)
- Grid Snap 기능 (격자 정렬)
- Zoom 지원 로직 (확대/축소 상태에서도 정확한 좌표)
- 모바일 Touch 이벤트 지원

**이벤트 처리 로직**:

- Mouse/Touch 이벤트 처리
- 전역 이벤트 리스너 관리 (`addEvent`, `removeEvent`)
- Handler별 커서 스타일 (`nw-resize`, `se-resize` 등)

**🔄 포팅 필요한 부분 (Vue → React 문법만)**:

**1. 템플릿 → JSX**:

```vue
<!-- Vue -->
<div v-for="handle in actualHandles" :key="'handle-' + handle">
```

```tsx
{/* React */}
{actualHandles.map((handle) => (
  <div key={`handle-${handle}`}>
))}
```

**2. Props 시스템**:

```typescript
// ezorthoweb 기존 Props → React Interface
interface DragResizeDivProps {
  x1: number
  y1: number
  x2: number
  y2: number
  shape: string
  zoom: number
  handles: string[] // ['tl', 'tm', 'tr', 'mr', 'br', 'bm', 'bl', 'ml']
  draggable: boolean
  resizable: boolean
  element: any
  parentWidth?: number
  parentHeight?: number
  onDragging?: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onDragStop?: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onResizing?: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onResizeStop?: (element: any, x1: number, y1: number, x2: number, y2: number) => void
  onActivated?: () => void
  onDeactivated?: () => void
}
```

**3. Computed → useMemo**:

```typescript
// ezorthoweb 기존 로직 그대로 활용
const actualHandles = useMemo(() => {
  if (!resizable) return []
  if (shape === 'Line' || shape === 'Lines') return ['tl', 'br'] // Line용 2개
  return handles // 일반 Element용 8개
}, [resizable, shape, handles])

const styleHandle = useCallback(
  (handle: string) => {
    const size = 5 // 핸들러 크기
    let ret = {
      position: 'absolute' as const,
      width: `${size * 2}px`,
      height: `${size * 2}px`,
      background: 'green',
      border: '1px solid green',
      display: enabled ? 'block' : 'none',
      zIndex: 100,
    }

    // ezorthoweb의 Handler 위치 계산 로직 그대로 활용
    if (isLine) {
      switch (handle) {
        case 'tl':
          ret.left = `${calcX1 - size}px`
          ret.top = `${calcY1 - size}px`
          ret.cursor = 'move'
          break
        case 'br':
          ret.left = `${calcX2 - size}px`
          ret.top = `${calcY2 - size}px`
          ret.cursor = 'move'
          break
      }
    } else {
      // 8개 핸들러 위치 계산 (기존 로직과 완전 동일)
      switch (handle) {
        case 'tl': // Top-Left
          ret.left = `${calcX1 - size}px`
          ret.top = `${calcY1 - size}px`
          ret.cursor = 'nw-resize'
          break
        case 'tm': // Top-Middle
          ret.left = `${(calcX1 + calcX2) / 2 - size}px`
          ret.top = `${calcY1 - size}px`
          ret.cursor = 'n-resize'
          break
        case 'tr': // Top-Right
          ret.left = `${calcX2 - size}px`
          ret.top = `${calcY1 - size}px`
          ret.cursor = 'ne-resize'
          break
        case 'ml': // Middle-Left
          ret.left = `${calcX1 - size}px`
          ret.top = `${(calcY1 + calcY2) / 2 - size}px`
          ret.cursor = 'w-resize'
          break
        case 'mr': // Middle-Right
          ret.left = `${calcX2 - size}px`
          ret.top = `${(calcY1 + calcY2) / 2 - size}px`
          ret.cursor = 'e-resize'
          break
        case 'bl': // Bottom-Left
          ret.left = `${calcX1 - size}px`
          ret.top = `${calcY2 - size}px`
          ret.cursor = 'sw-resize'
          break
        case 'bm': // Bottom-Middle
          ret.left = `${(calcX1 + calcX2) / 2 - size}px`
          ret.top = `${calcY2 - size}px`
          ret.cursor = 's-resize'
          break
        case 'br': // Bottom-Right
          ret.left = `${calcX2 - size}px`
          ret.top = `${calcY2 - size}px`
          ret.cursor = 'se-resize'
          break
      }
    }
    return ret
  },
  [enabled, calcX1, calcY1, calcX2, calcY2, isLine],
)
```

**4. 이벤트 처리 포팅**:

```typescript
// ezorthoweb의 드래그 로직 포팅
const handleElementMove = useCallback(
  (e: MouseEvent) => {
    const ex = e.pageX
    const ey = e.pageY
    const deltaX = ((ex - mouseClickPosition.sx) * 100) / zoom
    const deltaY = ((ey - mouseClickPosition.sy) * 100) / zoom

    // 기존 경계 제한 로직 그대로 활용
    let nx1 = Math.min(nx1 + deltaX, nx2 + deltaX)
    let ny1 = Math.min(ny1 + deltaY, ny2 + deltaY)
    let nx2 = Math.max(nx1 + deltaX, nx2 + deltaX)
    let ny2 = Math.max(ny1 + deltaY, ny2 + deltaY)

    // 부모 영역 경계 검사 (ezorthoweb 로직 동일)
    if (parentWidth > 0 && parentHeight > 0) {
      if (nx1 < 0) dx = -nx1
      else if (nx2 > parentWidth) dx = parentWidth - nx2
      if (ny1 < -parentHeader) dy = -parentHeader - ny1
      else if (ny2 > parentHeight + parentFooter) dy = parentHeight + parentFooter - ny2
    }

    // Grid Snap 적용 (ezorthoweb 로직 동일)
    if (grid) {
      dx = getGridSnap(nx1) - nx1
      dy = getGridSnap(ny1) - ny1
    }

    // 최종 좌표 업데이트
    onDragging?.(element, calcX1, calcY1, calcX2, calcY2)
  },
  [zoom, mouseClickPosition, parentWidth, parentHeight, grid],
)
```

**5. 라이프사이클 → useEffect**:

```typescript
// ezorthoweb의 mounted/beforeDestroy → useEffect
useEffect(() => {
  // 전역 이벤트 리스너 등록 (ezorthoweb와 동일)
  const handleGlobalMouseDown = (e: MouseEvent) => deselect(e)
  const handleGlobalMouseUp = () => handleUp()

  document.documentElement.addEventListener('mousedown', handleGlobalMouseDown)
  document.documentElement.addEventListener('mouseup', handleGlobalMouseUp)
  document.documentElement.addEventListener('touchend', handleGlobalMouseDown)

  return () => {
    // cleanup (beforeDestroy와 동일)
    document.documentElement.removeEventListener('mousedown', handleGlobalMouseDown)
    document.documentElement.removeEventListener('mouseup', handleGlobalMouseUp)
    document.documentElement.removeEventListener('touchend', handleGlobalMouseDown)
  }
}, [])
```

**TypeScript React 포팅 완성 예시**:

```tsx
const DragResizeDiv: React.FC<DragResizeDivProps> = ({
  x1,
  y1,
  x2,
  y2,
  shape,
  zoom = 100,
  element,
  handles = ['tl', 'tm', 'tr', 'mr', 'br', 'bm', 'bl', 'ml'],
  draggable = true,
  resizable = true,
  onDragging,
  onDragStop,
  onResizing,
  onResizeStop,
  children,
}) => {
  // ezorthoweb state 포팅
  const [nx1, setNx1] = useState(x1)
  const [ny1, setNy1] = useState(y1)
  const [nx2, setNx2] = useState(x2)
  const [ny2, setNy2] = useState(y2)
  const [enabled, setEnabled] = useState(false)
  const [resizing, setResizing] = useState(false)
  const [dragging, setDragging] = useState(false)
  const [isHover, setIsHover] = useState(false)

  // ezorthoweb computed 포팅
  const isLine = useMemo(() => shape === 'Line' || shape === 'Lines', [shape])
  const actualHandles = useMemo(() => {
    if (!resizable) return []
    if (isLine) return ['tl', 'br']
    return handles
  }, [resizable, isLine, handles])

  // ezorthoweb methods 포팅 (핵심 로직은 동일)
  const handleDown = useCallback(
    (handle: string, e: React.MouseEvent) => {
      e.stopPropagation()
      e.preventDefault()

      // ezorthoweb 로직 그대로 활용
      setResizing(true)
      mouseClickPosition.current = {
        sx: e.pageX,
        sy: e.pageY,
        x1: nx1,
        y1: ny1,
        x2: nx2,
        y2: ny2,
      }

      // 전역 이벤트 리스너 등록
      document.addEventListener('mousemove', handleMove)
      document.addEventListener('mouseup', handleUp)
    },
    [nx1, ny1, nx2, ny2],
  )

  return (
    <div>
      {element.getFixed ? (
        // Fixed Element 렌더링
        <div
          style={{
            position: 'absolute',
            left: `${element.left}px`,
            top: `${element.top}px`,
            width: `${element.width}px`,
            height: `${element.height}px`,
          }}
        >
          {children}
        </div>
      ) : (
        <>
          {/* 메인 Element Div */}
          <div style={styleDiv} onMouseDown={handleElementDown} onMouseOver={() => setIsHover(true)} onMouseLeave={() => setIsHover(false)}>
            {children}
            {/* 선택 시 테두리 표시 (Line 제외) */}
            {(isHover || enabled) && !isLine && (
              <div
                style={{
                  position: 'absolute',
                  left: '0px',
                  top: '0px',
                  width: '100%',
                  height: '100%',
                  border: '1px solid green',
                  pointerEvents: 'none',
                  zIndex: 99,
                }}
              />
            )}
          </div>

          {/* Resize Handlers */}
          {actualHandles.map((handle) => (
            <div
              key={`handle-${handle}`}
              style={styleHandle(handle)}
              onMouseDown={(e) => handleDown(handle, e)}
              onTouchStart={(e) => handleTouchDown(handle, e)}
            />
          ))}
        </>
      )}
    </div>
  )
}
```

**포팅 장점**:

- **검증된 700줄 코드**: 완성도 높은 Handler 시스템
- **모든 고급 기능 포함**: Grid Snap, Zoom, 경계 제한, 모바일 지원
- **핵심 로직 재사용**: 순수 JavaScript 로직은 그대로 활용 가능
- **개발 리스크 최소화**: 이미 검증된 로직 활용

**포팅 시 주요 변경사항**:

1. **Vue 템플릿 → JSX**: 문법 변경만 필요
2. **Props 시스템**: Vue props → React interface
3. **Computed → useMemo/useCallback**: 반응형 데이터 처리
4. **Vuex 의존성 제거**: Redux/Context 또는 props로 대체
5. **라이프사이클**: mounted/beforeDestroy → useEffect

**결론**: **완전히 포팅 가능**, Handler 시스템의 95% 이상 재사용 가능

**16. ezorthoweb 기존 코드 활용 계획**:

**재사용 가능한 부분**:

- **클래스 구조 설계**: Element 계층구조와 속성 설계 그대로 활용
- **DragResizeDiv 핵심 로직**: 700줄의 검증된 Handler 시스템 (95% 재사용)
- **좌표 변환 로직**: mm2px, px2mm 등 단위 변환 함수
- **속성 클래스**: FontAttr, LineAttr, FillAttr 구조
- **Element 타입 정의**: ElementShape enum 활용

**포팅 필요한 부분**:

- **Vue 컴포넌트 → TypeScript React 컴포넌트**: 렌더링 로직 변경 (문법적 변경만)
- **Vuex → Redux**: 상태 관리 시스템 변경
- **이벤트 처리**: Vue 이벤트 시스템 → React 이벤트 시스템

### scp-cloud-demo 정적 호스팅 및 CI (Phase 1)

`scp-report-poc/apps/scp-cloud-demo` Vite 빌드 산출물(`dist/`)을 AWS S3에 올려 정적 호스팅한다. AWS 계정 **767397951498 (SCPSharedDev)**.

- **데모 사이트 URL**: `http://scp-report-demo.test.scp.esclouddev.com/` — 배포·DNS 적용 후 브라우저에서 접속하는 주소다. (HTTP, Route 53 → S3 웹 사이트 호스팅.)

**자격 증명**

- Access Key / Secret Key는 **Azure DevOps Variable Group 또는 Pipeline variables**에만 둔다. Git·본 문서에 평문 기입 금지.
- 문서 예시: Access Key ID `AKIA********` 수준만 기재. Secret은 기재하지 않음. 외부 노출 시 IAM에서 즉시 비활성화·교체.

**S3**

- S3 버킷은 **사이트 FQDN과 동일한 이름**으로 생성해 관리한다: **`scp-report-demo.test.scp.esclouddev.com`** (전역 유일·S3 명명 규칙 준수).

**버킷·권한·DNS: AWS 콘솔 기준(초기 1회)**

버킷 생성 이후 **퍼블릭 공개, 웹 호스팅, 버킷 정책, Route 53, CI용 IAM**은 **AWS Management Console**에서 설정한다. 리전은 **ap-northeast-2(서울)** 로 통일하고, 파이프라인 `AWS_REGION`과 맞춘다.

**S3 콘솔**

1. **서비스** → **S3** → **버킷 만들기**. AWS 리전(오른쪽 상단)이 **서울**인지 확인. 버킷 이름 `scp-report-demo.test.scp.esclouddev.com`, 나머지는 팀 규칙에 맞게 두고 생성한다.
2. 만든 버킷 선택 → **권한** 탭 → **퍼블릭 액세스 차단** → **편집**. 데모용으로 객체를 URL로 열 수 있게 하려면, 콘솔에 표시되는 네 가지 항목 중 **버킷 정책으로 부여되는 퍼블릭 액세스** 등 필요한 것만 해제하고 저장한다(경고 문구 확인). **SCPSharedDev 데모 전용**이며 운영 버킷과 동일하게 두지 않는다.
3. 같은 **권한** 탭 → **버킷 정책** → **편집**. 아래 JSON **전체**를 복사해 붙여넣고 **변경 사항 저장**한다(다른 버킷 이름을 쓰면 `Resource`의 ARN만 맞게 고친다).

4. **속성** 탭 → 맨 아래 **정적 웹 사이트 호스팅** → **편집** → **활성화**. 인덱스 문서·오류 문서 모두 `index.html`. 저장 후 표시되는 **버킷 웹 사이트 엔드포인트**(예: `http://scp-report-demo.test.scp.esclouddev.com.s3-website.ap-northeast-2.amazonaws.com`)로 동작을 확인한다. 객체를 아직 안 올렸으면 `NoSuchKey` / `index.html` **404**가 나온다. 설정 오류가 아니라 **빈 버킷**이므로, 아래 배포(sync)로 `dist`를 버킷 **루트**에 올리면 된다.

**Route 53 콘솔**

5. **서비스** → **Route 53** → **호스팅 영역** → `test.scp.esclouddev.com` → **레코드 생성**(또는 기존 레코드 편집). 레코드 이름 `scp-report-demo`, FQDN이 `scp-report-demo.test.scp.esclouddev.com` 이 되게 한다. 레코드 유형은 **A**이고 **별칭(Alias)** 을 켠 뒤, 트래픽 대상으로 **S3 웹 사이트 엔드포인트**·리전 **ap-northeast-2**·위 버킷을 고른다. (IPv6이 필요하면 **AAAA** 별칭을 추가한다.) 이 경로는 **HTTP**이다.

**자격 증명(IAM)**

6. **새 IAM 사용자를 꼭 만들 필요는 없다.** 이미 Variable Group 등에 넣은 `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`에 해당 버킷에 대한 `s3:ListBucket`, `s3:PutObject`, `s3:DeleteObject`(파이프라인 `sync --delete` 시)가 포함되어 있으면 그대로 쓰면 된다. 관리자 권한 등 넓은 권한으로도 동작하지만, **가능하면 이 버킷에만 최소 권한**을 주는 편이 안전하다. 키를 새로 띄울 때만 IAM 콘솔에서 **사용자** → **보안 자격 증명**에서 액세스 키를 발급하고, 위 S3 권한만 붙인 정책을 연결한다.

**참고(CLI)**

버킷만 CLI로 만들고 나머지는 전부 콘솔에서 해도 된다.

```bash
aws s3api create-bucket \
  --bucket scp-report-demo.test.scp.esclouddev.com \
  --region ap-northeast-2 \
  --create-bucket-configuration LocationConstraint=ap-northeast-2
```

- 배포: `aws s3 sync apps/scp-cloud-demo/dist s3://scp-report-demo.test.scp.esclouddev.com/ --delete` (저장소 루트 `azure-pipelines.yml` 참고).

**DNS(요약)**

- 호스팅 영역 `test.scp.esclouddev.com`, 레코드 `scp-report-demo` → FQDN **`scp-report-demo.test.scp.esclouddev.com`**. 사용자 접속 URL은 **`http://scp-report-demo.test.scp.esclouddev.com/`** (위 데모 사이트 URL과 동일). 상세는 **Route 53 콘솔** 단계. HTTPS가 필요하면 이후 **CloudFront + ACM**으로 전환한다.

**Azure DevOps**

- 파이프라인: `scp-report-poc/azure-pipelines.yml`.
- 변수(Secret 권장: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`): `AWS_REGION`은 **ap-northeast-2**, `S3_BUCKET`은 **`scp-report-demo.test.scp.esclouddev.com`**(YAML 기본값과 동일). 상세는 YAML 주석.

**16. 로드맵 (체크리스트)**:

### Phase 1: 핵심 인프라 + 기본 Element **(P1)** - 2~3주

- [x] **Task 0**: 프로젝트 및 Repository 준비 (10h)
  - [x] Monorepo 루트 생성 (pnpm workspaces, Turborepo)
  - [x] packages/core, components, migration, library 초기화 (PoC-08 구조)
  - [x] apps/scp-cloud-demo Vite+React 앱 생성, workspace:\* 링크
  - [x] PoC-06 통합 스키마 TypeScript 타입 정의 (core/types)
  - [x] 좌표 변환 유틸 (core/utils: mm2px, px2mm, DPMM=96/25.4)

- [x] **Task 1.1**: DragResizeDiv 포팅 (16h)
  - [x] DragResizeDivProps, DragResizeState 인터페이스 정의
  - [x] Vue 템플릿 → JSX 변환 (8개 핸들러 + Line 2개)
  - [x] 이벤트 처리 (onDragging, onResizing, onDragStop, onResizeStop)
  - [x] Grid Snap, Zoom, 경계 제한 로직 포팅
  - [x] 단위 테스트

- [x] **Task 1.2**: BaseElement / ChartElementBase 구조 (8h)
  - [x] BaseElement (mm2px, px2mm, \_dpi=96)
  - [x] ChartElementBase (position, size, fontAttr, lineAttr, fillAttr)
  - [x] getDragResizeHandles(), getShape() 추상 메서드
  - [x] Position, Size, ElementStyle 타입 (PoC-06 호환)

- [x] **Task 1.3**: 기본 Shape Element (12h)
  - **의존**: Task 1.1, Task 1.2
  - [x] RectangleElement (SVG rect, 8핸들러)
  - [x] EllipseElement (SVG ellipse, 8핸들러)
  - [x] LineElement (SVG line, tl/br 2핸들러)
  - [x] ResizeHandlers 컴포넌트
  - [x] 단위 테스트

- [x] **Task 1.4**: Document/Paper/Page 렌더러 (8h)
  - **의존**: Task 1.3
  - [x] ReportRenderer (document 입력, paper 크기)
  - [x] Page 컴포넌트 (pages[].elements 순회)
  - [x] Element 레지스트리 (type → 컴포넌트 매핑)
  - [x] PoC-06 JSON 샘플 로딩 검증

- [x] **Task 1.5**: 선택 및 편집 시스템 (8h)
  - **의존**: Task 1.4
  - [x] 단일/다중 선택 (클릭, Shift+클릭)
  - [x] 선택 시 Handler 표시, 테두리 표시
  - [x] Delete 키 삭제
  - [x] onAuditEvent 콜백 연동 (선택적)

- [x] **Task 1.6**: scp-cloud-demo S3 호스팅 및 CI 배포 (SCPSharedDev)

**Phase 1 예상 시간**: 62h (약 2주) — Task 1.6은 인프라·DNS 설정 포함 시 별도 가산

### Phase 2: Content Element + 편집 **(P2)** - 2주

- [x] **Task 2.1**: ImageBox (Single) (10h)
  - **의존**: Task 1.5
  - [x] ImageBoxElement (fitMode: realSize/boxFit/modified)
  - [x] imageRefs, `extensions.imageRef` 매핑 (`Document.imageRefs`, PoC-06 `ImageBoxElementExtensions`)
  - [x] 래스터: `<img>` + foreignObject. DICOM(`.dcm`): `dicom-parser`로 메타(모달리티·행/열 등) 표시, 픽셀 표시는 **Task 3.5**에서 구현(현재는 안내 문구 + 다운로드).
  - [x] DragResizeDiv 래핑 (`ResizeHandlers` / `ImageBoxElement`)
  - 데모 샘플·`imageRefs`·이미지 소스 정책: **PoC-06 연동 보조 스펙** 절의 **ImageBox(Single) — 데모 샘플·이미지 소스**.

- [x] **Task 2.2**: 속성 패널 (Element Inspector) (18h)
  - **의존**: Task 1.5
  - **참조**: **PoC-06 연동 보조 스펙** 절 — **속성 패널 (Element Inspector) — 설계·스펙**(A~F 표).
  - [x] 데모(또는 components) **오른쪽 도킹 패널** + show/hide 토글; 단일 선택 시에만 편집 활성.
  - [x] `onDocumentChange`와 연동하는 **불변 `patchElement`**(pageIndex·elementId·deep partial).
  - [x] **공통 필드 컴포넌트**: A1~A11을 디스크립터 또는 공통 폼 한 벌로 구현(중복 JSX 금지).
  - [x] **선·채움 공통**: B1~B5를 한 서브섹션으로 구현; 타입별 표시 필터(`line`은 B4·B5 숨김 등).
  - [x] **rectangle**: C1·C2 — A 전부 + B 전부 연결 검증.
  - [x] **ellipse**: D1·D2 — rectangle과 동일 조합 재사용.
  - [x] **line**: E1~E6 — 공통 + B1~B3 + `extensions.lineEndpoints` 네 좌표(mm); 패치 후 렌더·핸들 동기.
  - [x] **imageBox**: F1~F6 — 공통 + B1~B3 + `imageRef` 셀렉트(`document.imageRefs` 키) + `fitMode` 셀렉트; F3(B4·B5) 정책은 스펙 표와 동일.
  - [x] 단위 테스트: 패치 유틸·(선택) 디스크립터 순회 렌더 스냅샷.

- [x] **Task 2.3**: TextBox + Label (8h)
  - **의존**: Task 1.5
  - [x] LabelElement (평문 텍스트)
  - [x] TextBoxElement 기본 구조 (content, editable)
  - [x] style.fontSize(pt), fontFamily 적용
  - [x] 읽기 전용 렌더링 (편집 모드 전)
  - [x] (후속) Task 2.2 패널에 TextBox/Label 전용 필드 — Label: G1~G7·`extensions.text` / TextBox: `extensions.html`·`editable`만(타이포는 Lexical·HTML).

- [ ] **Task 2.4**: Lexical 연동 (12h)
  - **의존**: Task 2.3
  - [ ] Lexical 에디터 컴포넌트 래퍼
  - [ ] HTML ↔ Lexical 직렬화
  - [ ] foreignObject 내 편집기 배치
  - [ ] sanitizeHtml 적용 (PoC-11, DOMPurify 등)

- [ ] **Task 2.5**: 상태 관리 (10h)
  - **의존**: Task 2.4
  - [ ] ElementState (elements, selectedElements, clipboard, history)
  - [ ] addElement, updateElement, deleteElement, selectElements
  - [ ] Redux Toolkit slice 또는 Context

- [ ] **Task 2.6**: 복사/붙여넣기, Undo/Redo (8h)
  - **의존**: Task 2.5
  - [ ] Ctrl+C, Ctrl+V
  - [ ] Ctrl+Z, Ctrl+Y (history.past/future)
  - [ ] Arrow 키 이동 (선택 시)

**Phase 2 예상 시간**: 약 66h (2.1의 10h 포함 시 Phase 2 누적) — 속성 패널(Task 2.2) 18h 반영, Task 번호 2.3~2.6으로 이동

### Phase 3: 고급 Element **(P3)** - 2주

- [ ] **Task 3.1**: Arrow, Memo (12h)
  - **의존**: Task 2.6
  - [ ] ArrowElement (Line + 화살표 머리, points)
  - [ ] MemoElement (anchorPoint, bubblePosition, content)
  - [ ] Memo 풍선+포인터 렌더링 (PoC-06 스키마)

- [ ] **Task 3.2**: Multi / Reference ImageBox (10h)
  - **의존**: Task 2.1
  - [ ] layout.row, layout.column (1~20)
  - [ ] Multi ImageBox 그리드 렌더링
  - [ ] Reference ImageBox (linkedBoxId 참조)

- [ ] **Task 3.3**: FreeDraw (6h)
  - **의존**: Task 2.6
  - [ ] FreeDrawElement (points → SVG path)
  - [ ] Path 데이터 직렬화

- [ ] **Task 3.4**: 인쇄 및 @media print (8h)
  - **의존**: Task 3.3
  - [ ] @media print CSS (PoC-10)
  - [ ] @page size, margin
  - [ ] mm, pt 단위 출력 검증
  - [ ] window.print() 연동

- [ ] **Task 3.5**: ImageBox DICOM 픽셀 표시 (리포트 내 뷰) (14h)
  - **의존**: Task 2.1
  - **목표**: `.dcm`을 리포트 ImageBox 박스 안에서 **실제 영상 픽셀**으로 표시(메타 전용 패널에서 전환 또는 병행). PoC-05·ezortho의 Cornerstone 계열 연동 방향과 맞출 것.
  - [ ] **디코딩 스택 선정**: `@cornerstonejs/core`(또는 후속 권장 스택) + DICOM Part 10 바이트 로드(기존 `imageRefs` URL·ArrayBuffer). 전송 문법(JPEG, JPEG-LS, RLE, 미압축 등) 지원 범위를 문서화.
  - [ ] **ImageBox 통합**: `ImageBoxElement`의 DICOM 분기에서 `foreignObject` 내 **Canvas/WebGL 뷰포트** 또는 Cornerstone 래퍼 컴포넌트로 렌더. `fitMode`(realSize/boxFit/modified)와 박스 리사이즈 시 뷰포트 크기 동기화.
  - [ ] **윈도/레벨·VOI**: 기본값(자동 또는 DICOM 태그) 및 추후 슬라이더는 선택; 1차는 읽기 가능한 기본 창이면 됨.
  - [ ] **멀티프레임**: 1차는 단일 프레임(또는 첫 프레임); 필요 시 프레임 인덱스 `extensions` 확장 검토.
  - [ ] **번들·의존성**: Cornerstone 계열은 용량이 크므로 **peerDependency** 또는 **동적 import**(호스트 앱에서 프리로드) 여부 결정. `@ewoosoft/scp-report-components` 기본 번들에 항상 넣지 않을지 검토.
  - [ ] **실패 시**: 디코딩 실패·미지원 전송 문법 시 현행과 같이 메타 + 다운로드 폴백.
  - [ ] **데모**: `sample.dcm`으로 scp-cloud-demo에서 픽셀 확인. 인쇄(Task 3.4)와 겹치면 캔버스 스냅샷 또는 인쇄 시 경고 문구 정책 정리.

**DICOM 픽셀 표시 — 구현 시 정리할 기술 요약**(Task 3.5 산출 기준):

| 항목 | 내용 |
|------|------|
| 입력 | `Document.imageRefs`의 `.dcm` URL(동일 출처·CORS) 또는 호스트가 넘기는 `ArrayBuffer` 콜백(선택 설계) |
| 디코드 | DICOM 파서 + 이미지 로더 코덱; 샘플·운영에서 쓰는 전송 문법 목록을 명시 |
| 출력 | 2D 그레이스케일/컬러를 박스 크기에 맞게 표시; `DragResizeDiv`와 충돌 없게 포인터 이벤트 처리 |
| 성능 | 대용량 시 Web Worker·캐시 키(instance URL); 페이지 전환 시 리소스 dispose |
| 보안 | 리포트 JSON만으로는 민감정보 최소화; 픽셀 데이터는 기존 URL 접근 정책 따름 |

**Phase 3 예상 시간**: 50h (약 1.5주) — Task 3.5 포함

### Phase 4: EzOrtho 특화 + 통합 검증 **(P4)** - 2주

- [ ] **Task 4.1**: ToothBox, TreatmentCategory (10h)
  - [ ] ToothBoxElement (selectedToothCodes, selectedOcclusionToothCodes)
  - [ ] TreatmentCategoryElement (category1/2/3, P2 우선순위 낮음)

- [ ] **Task 4.2**: Form Controls (12h)
  - [ ] formControl + controlType (radio, checkbox, button, comboBox, textInput, textArea)
  - [ ] 각 controlType별 렌더링

- [ ] **Task 4.3**: Block, Group (10h)
  - [ ] BlockElement (children: Element[], 상대 좌표)
  - [ ] GroupElement (memberIds: string[])
  - [ ] 그룹 선택 시 일괄 이동/삭제

- [ ] **Task 4.4**: 보안 및 감사 (6h)
  - [ ] onAuditEvent 콜백 (OPEN, SAVE, DELETE, EXPORT, PRINT)
  - [ ] ReportLibraryConfig 인터페이스
  - [ ] TextBox sanitization 최종 검증

- [ ] **Task 4.5**: 통합 테스트 및 검증 (12h)
  - [ ] Migration 출력 JSON → 렌더링 검증 (PoC-07 연계)
  - [ ] 브라우저 호환성 (Chrome, Firefox, Safari, Edge)
  - [ ] 성능 테스트 (50개 Element 목표)
  - [ ] 호환성 검증 리포트 작성

**Phase 4 예상 시간**: 50h (약 1.5주)

**총 예상 시간**: 228h (약 7~8주) — Task 3.5·속성 패널(Task 2.2) 반영

**산출물**:

1. **React DragResizeDiv 컴포넌트**: ezorthoweb의 700줄 Handler 시스템 완벽 포팅
2. **Element 클래스 라이브러리**: TypeScript React 기반 Element 시스템
3. **렌더링 엔진**: SVG/Canvas 기반 Element 렌더러
4. **Handler 시스템**: 완전한 Drag & Resize 핸들러 (8개 + Line용 2개)
5. **HTML 편집기 통합**: 의료용 텍스트 편집 시스템
6. **상태 관리 시스템**: Element 편집 상태 관리
7. **속성 패널**(Task 2.2): 공통·타입별 필드 디스크립터 기반 Inspector
8. **DragResizeDiv 포팅 가이드**: Vue → TypeScript React 포팅 상세 방법론 (핵심 자산)
9. **성능 벤치마크**: Element 렌더링 성능 분석
10. **호환성 검증 리포트**: 기존 파일 호환성 확인
11. **DICOM 뷰 통합**(Task 3.5 완료 시): ImageBox 내 픽셀 렌더링·지원 전송 문법·번들 전략 문서

**다음 단계**: 구현된 Element 렌더링 엔진을 PoC-08(아키텍처 전략)에 통합하여 전체 시스템 검증

---

**17. Repository 구성** (PoC-08 반영):

### 17.1 개발 전략: Monorepo 우선, Publish는 완료 시점

**권장**: Monorepo로 개발하고, SCP Cloud 통합 준비 시점에 @ewoosoft/scp-report-library로 NPM Private Publish.

| 방식                     | 장점                                               | 단점                                       |
| ------------------------ | -------------------------------------------------- | ------------------------------------------ |
| **Monorepo + workspace** | 즉시 반영 테스트, publish 없이 개발, atomic commit | 초기 설정 필요                             |
| 처음부터 NPM publish     | 단순                                               | 매 변경마다 publish 필요, 피드백 루프 느림 |

**이유**: `workspace:*`로 데모 앱이 로컬 패키지를 참조하면, 코드 수정 시 저장만으로 HMR 적용. NPM publish 방식은 변경마다 `npm run build && npm publish` 후 소비 앱에서 `npm update` 필요하여 개발 속도 저하.

### 17.2 Repository 구조 (PoC-08 4.1절과 동일)

```
scp-report-poc/
├── packages/
│   ├── core/                            # @ewoosoft/scp-report-core
│   │   ├── src/
│   │   │   ├── engine/                  # 렌더링 엔진 (ReportRenderer, Page)
│   │   │   ├── elements/                # Element 클래스 (BaseElement, Rectangle 등)
│   │   │   ├── utils/                   # mm2px, px2mm, sanitize
│   │   │   └── types/                   # PoC-06 스키마 타입
│   │   └── package.json
│   │
│   ├── components/                      # @ewoosoft/scp-report-components
│   │   ├── src/
│   │   │   ├── ReportEditor/
│   │   │   ├── ReportViewer/
│   │   │   ├── Elements/                # Element React 컴포넌트 (DragResizeDiv 래핑)
│   │   │   └── Toolbar/
│   │   └── package.json
│   │
│   ├── migration/                       # @ewoosoft/scp-report-migration (PoC-07)
│   │   ├── src/
│   │   │   ├── parsers/
│   │   │   ├── converters/
│   │   │   └── validators/
│   │   └── package.json
│   │
│   └── library/                         # @ewoosoft/scp-report-library (publish 대상)
│       ├── src/
│       │   └── index.ts                 # core, components, migration re-export
│       └── package.json
│
├── apps/
│   ├── scp-cloud-demo/                  # SCP Cloud 통합 데모 (주 개발용)
│   └── playground/                      # 최소 테스트 앱 (선택)
│
├── package.json
├── turbo.json                           # Turborepo
└── tsconfig.json
```

**패키지 역할** (PoC-08 4.1절):

- `core`: 핵심 로직만 필요한 경우 (Headless)
- `components`: React 컴포넌트만 필요한 경우
- `migration`: Migration 도구만 필요한 경우 (PoC-07 범위)
- `library`: 전체 기능 통합, SCP Cloud 등에서 `npm install @ewoosoft/scp-report-library`로 사용

**PoC-14 구현 배치**:

- core: types, utils, attrs (Task 1.2·PoC-06 등); components: engine, Elements, ReportRenderer, **속성 패널(Task 2.2)**, ImageBox(Task 2.1) 및 Task 2.3~2.6·Phase 3 범위
- components: ReportEditor, ReportViewer, Elements, Toolbar (Task 1.4~4.4)
- migration: PoC-07에서 구현, PoC-14에서는 빈 껍데기 또는 placeholder

### 17.3 개발 플로우

1. **초기 설정**

   ```bash
   pnpm install
   pnpm --filter scp-cloud-demo dev
   ```

2. **일상 개발**
   - `packages/core`, `packages/components` 수정
   - `apps/scp-cloud-demo`에서 즉시 반영 (workspace 링크)
   - publish 불필요

3. **로컬 통합 테스트** (SCP Cloud 연동 전)
   - `apps/scp-cloud-demo`에 Migration 출력 JSON 로드
   - Element 렌더링, 편집, 인쇄 검증

4. **Publish 시점** (Phase 4 완료 또는 SCP Cloud 통합 직전)
   ```bash
   pnpm --filter @ewoosoft/scp-report-library build
   pnpm --filter @ewoosoft/scp-report-library publish
   ```

### 17.4 package.json 예시

**Root (package.json)**:

```json
{
  "name": "scp-report-poc",
  "private": true,
  "workspaces": ["packages/*", "apps/*"],
  "scripts": {
    "dev": "pnpm --filter scp-cloud-demo dev",
    "build": "turbo run build",
    "test": "pnpm -r test"
  },
  "devDependencies": {
    "turbo": "^2.0.0"
  }
}
```

**packages/core/package.json**:

```json
{
  "name": "@ewoosoft/scp-report-core",
  "version": "0.1.0",
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts"
}
```

**packages/components/package.json**:

```json
{
  "name": "@ewoosoft/scp-report-components",
  "version": "0.1.0",
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "peerDependencies": {
    "@ewoosoft/scp-report-core": "workspace:*",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

**packages/library/package.json** (re-export):

```json
{
  "name": "@ewoosoft/scp-report-library",
  "version": "0.1.0",
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./styles.css": "./dist/styles.css"
  },
  "dependencies": {
    "@ewoosoft/scp-report-core": "workspace:*",
    "@ewoosoft/scp-report-components": "workspace:*",
    "@ewoosoft/scp-report-migration": "workspace:*"
  },
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "files": ["dist"]
}
```

**apps/scp-cloud-demo/package.json**:

```json
{
  "name": "scp-cloud-demo",
  "private": true,
  "dependencies": {
    "@ewoosoft/scp-report-library": "workspace:*",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

### 17.5 @ewoosoft NPM Private Publish 절차

**사전 조건**:

- Phase 4 완료 또는 SCP Cloud 통합 직전
- `pnpm build` 성공, `pnpm test` 통과

**1. Registry 및 .npmrc 설정** (Azure DevOps Artifacts)

```bash
# 프로젝트 루트 또는 packages/library/.npmrc
registry=https://pkgs.dev.azure.com/ewoosoft/_packaging/scp-packages/npm/registry/
always-auth=true
```

**2. 인증**

- **Azure DevOps**: Project Settings → Artifacts → Connect to Feed → npm → "Get the tools"에서 .npmrc 및 Personal Access Token(PAT) 발급
- PAT 권한: Packaging (Read & write)
- 토큰은 환경변수 또는 Pipeline Variable에 저장. 로컬 `.npmrc`에 평문 저장 금지

**3. Publish 순서** (의존성 순)

```bash
# 1) core → 2) components → 3) migration → 4) library
pnpm --filter @ewoosoft/scp-report-core build
pnpm --filter @ewoosoft/scp-report-core publish --no-git-checks

pnpm --filter @ewoosoft/scp-report-components build
pnpm --filter @ewoosoft/scp-report-components publish --no-git-checks

pnpm --filter @ewoosoft/scp-report-migration build
pnpm --filter @ewoosoft/scp-report-migration publish --no-git-checks

pnpm --filter @ewoosoft/scp-report-library build
pnpm --filter @ewoosoft/scp-report-library publish --no-git-checks
```

**주의**: `workspace:*`는 publish 시 해당 workspace 패키지의 실제 버전으로 치환됨. 모든 패키지 `version`을 동일하게 맞춘 후 publish.

**4. Changeset (버전 관리, 권장)**

```bash
pnpm add -Dw @changesets/cli
pnpm changeset init

# 변경 시
pnpm changeset          # 변경 내용 기록
pnpm changeset version  # 버전 bump
pnpm changeset publish  # 순차 publish
```

**5. CI/CD 파이프라인** (Azure DevOps, 선택)

```yaml
# azure-pipelines.yml
trigger:
  tags:
    include:
      - v*

pool:
  vmImage: 'ubuntu-latest'

variables:
  npmRegistry: 'https://pkgs.dev.azure.com/ewoosoft/_packaging/scp-packages/npm/registry/'

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: '20.x'
  - script: |
      corepack enable
      corepack prepare pnpm@9 --activate
  - script: pnpm install --frozen-lockfile
    displayName: 'Install'
  - script: pnpm build
    displayName: 'Build'
  - script: pnpm test
    displayName: 'Test'
  - script: |
      echo "//pkgs.dev.azure.com/ewoosoft/_packaging/scp-packages/npm/registry/:_authToken=$(System.AccessToken)" > .npmrc
      echo "registry=$(npmRegistry)" >> .npmrc
      pnpm -r publish --no-git-checks
    displayName: 'Publish'
    condition: and(succeeded(), startsWith(variables['Build.SourceBranch'], 'refs/tags/'))
```

Pipeline 설정: "Allow scripts to access the OAuth token" 활성화. Artifacts publish 권한이 없으면 PAT를 Variable(secret)로 등록 후 `_authToken=$(AZURE_ARTIFACTS_TOKEN)` 사용.

**6. SCP Cloud에서 사용**

```bash
npm install @ewoosoft/scp-report-library
# 또는
pnpm add @ewoosoft/scp-report-library
```

소비 프로젝트 `.npmrc`에 동일 registry 설정 필요.

**상세**: PoC-08\_아키텍처전략검증\_result.md 4.4절

### 17.6 Task 0 반영

로드맵 Phase 1 Task 0에 Repository 초기화 포함 (PoC-08 구조):

- [x] Monorepo 루트 생성 (pnpm workspaces + Turborepo)
- [x] packages/core, packages/components, packages/migration, packages/library 초기화
- [x] apps/scp-cloud-demo Vite+React 앱 생성
- [x] workspace 링크 설정 (core → components → library → scp-cloud-demo)
- [x] `pnpm dev` 실행 시 scp-cloud-demo에서 library 사용 검증

---

**참조 문서** (구현 시 필수 확인):

- PoC-06\_통합Element스키마설계\_result.md: Element 타입, position/size 구조, Memo anchorPoint, Block/Group
- PoC-08\_아키텍처전략검증\_result.md: Repository 구조, Monorepo, NPM Private Registry, 패키지 설계
- PoC-10\_인쇄및Export품질검증\_result.md: @media print, mm/pt 단위, CSS 인쇄 가이드
- PoC-11\_의료데이터보안검증\_result.md: sanitizeHtml, onAuditEvent, XSS 방지

**ezorthoweb 코드 분석 완료 현황**:

- ✅ BaseModel 구조 분석 (단위 변환, XML/JSON 처리)
- ✅ ChartElementBase 구조 분석 (Element 기본 클래스)
- ✅ 18개 Element 타입 확인 (일반 리포트용)
- ✅ 속성 클래스 4개 확인 (Font, Line, Fill, Paper)
- ✅ 좌표 변환 시스템 확인 (mm2px, px2mm)
- ✅ **DragResizeDiv.vue 분석 완료**: 700줄의 완벽한 Handler 시스템 (95% 재사용 가능)
- ✅ Vue 컴포넌트 구조 확인 (PatientChartElements 등)
- 🔄 추가 구현 필요: Arrow, Memo, Multi ImageBox, Reference ImageBox
- 🔄 현재 구현 범위 외: Canvas Element (EzOrtho 분석 차트 전용, 추후 확장 대상)

**핵심 자산**: DragResizeDiv.vue는 PoC-14의 가장 중요한 참고 자료로, 이 컴포넌트만 완벽히 포팅하면 모든 Element의 Drag & Resize 기능이 해결됨
