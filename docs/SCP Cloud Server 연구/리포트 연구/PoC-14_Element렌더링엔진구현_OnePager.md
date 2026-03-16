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

| PoC | 결정 사항 | PoC-14 반영 |
|-----|-----------|-------------|
| PoC-01 | JSON 포맷, TypeScript 타입 | document/element 구조 JSON, TS 인터페이스 |
| PoC-02 | mm 좌표, 소수점 3자리 | position/size 단위 mm, 정밀도 #.### |
| PoC-03 | pt 폰트, 96 DPI 화면, @media print | 폰트 pt, mm2px 기준 96 DPI, 인쇄 스타일 분리 |
| PoC-04 | HTML DOM + SVG 렌더링 | SVG 기반 Element 렌더링 확정 (Canvas 대안 제외) |
| PoC-05 | Lexical(텍스트), Puppeteer(PDF), cornerstone(DICOM) | TextBox: Lexical 연동. PDF/이미지는 호스트 연동 |
| PoC-06 | 통합 Element 스키마 (document→paper→pages→elements) | 스키마 기반 렌더링. ElementType: imageBox, textBox, rectangle 등 |
| PoC-07 | Migration 경로 (E2/E3/EzOrtho/CleverOne→Cloud) | Migration 출력 JSON을 렌더링 엔진 입력으로 사용 |
| PoC-10 | window.print + @media print, 서버 Puppeteer PDF | @media print CSS, mm/pt 단위로 출력 품질 보장 |
| PoC-11 | 입력 sanitization, 감사 콜백, XSS 방지 | TextBox HTML sanitization, onAuditEvent 콜백, dangerouslySetInnerHTML 금지(사용자 입력) |
| PoC-12 | 다국어(i18n), RTL | 텍스트/레이블 i18n 키 연동, direction 속성 |
| PoC-13 | WCAG 2.1 AA, 접근성 | DOM+SVG 기반(PoC-04), ARIA, 키보드 네비게이션 |

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
  - Single ImageBox (기본, DragResizeDiv 8개 핸들러 활용)
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
- TextBox (기본 텍스트)
- HTML 편집기 통합

**Phase 3: 고급 Element**:

- Arrow, Memo 구현
- Multi ImageBox 구현
- FreeDraw 구현

**Phase 4: EzOrtho 특화** (일반 리포트용):

- ToothBox, TreatmentCategory
- Form Controls (RadioButton, CheckBox 등)
- EzOrtho 분석 차트(Canvas 기반)는 현재 구현 범위 외, 추후 확장 대상

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

**16. 로드맵 (체크리스트)**:

### Phase 1: 핵심 인프라 + 기본 Element **(P1)** - 2~3주

- [x] **Task 0**: 프로젝트 및 Repository 준비 (10h)
  - [x] Monorepo 루트 생성 (pnpm workspaces, Turborepo)
  - [x] packages/core, components, migration, library 초기화 (PoC-08 구조)
  - [x] apps/scp-cloud-demo Vite+React 앱 생성, workspace:* 링크
  - [x] PoC-06 통합 스키마 TypeScript 타입 정의 (core/types)
  - [x] 좌표 변환 유틸 (core/utils: mm2px, px2mm, DPMM=96/25.4)

- [x] **Task 1.1**: DragResizeDiv 포팅 (16h)
  - [x] DragResizeDivProps, DragResizeState 인터페이스 정의
  - [x] Vue 템플릿 → JSX 변환 (8개 핸들러 + Line 2개)
  - [x] 이벤트 처리 (onDragging, onResizing, onDragStop, onResizeStop)
  - [x] Grid Snap, Zoom, 경계 제한 로직 포팅
  - [x] 단위 테스트

- [ ] **Task 1.2**: BaseElement / ChartElementBase 구조 (8h)
  - [ ] BaseElement (mm2px, px2mm, _dpi=96)
  - [ ] ChartElementBase (position, size, fontAttr, lineAttr, fillAttr)
  - [ ] getDragResizeHandles(), getShape() 추상 메서드
  - [ ] Position, Size, ElementStyle 타입 (PoC-06 호환)

- [ ] **Task 1.3**: 기본 Shape Element (12h)
  - **의존**: Task 1.1, Task 1.2
  - [ ] RectangleElement (SVG rect, 8핸들러)
  - [ ] EllipseElement (SVG ellipse, 8핸들러)
  - [ ] LineElement (SVG line, tl/br 2핸들러)
  - [ ] ResizeHandlers 컴포넌트
  - [ ] 단위 테스트

- [ ] **Task 1.4**: Document/Paper/Page 렌더러 (8h)
  - **의존**: Task 1.3
  - [ ] ReportRenderer (document 입력, paper 크기)
  - [ ] Page 컴포넌트 (pages[].elements 순회)
  - [ ] Element 레지스트리 (type → 컴포넌트 매핑)
  - [ ] PoC-06 JSON 샘플 로딩 검증

- [ ] **Task 1.5**: 선택 및 편집 시스템 (8h)
  - **의존**: Task 1.4
  - [ ] 단일/다중 선택 (클릭, Shift+클릭)
  - [ ] 선택 시 Handler 표시, 테두리 표시
  - [ ] Delete 키 삭제
  - [ ] onAuditEvent 콜백 연동 (선택적)

**Phase 1 예상 시간**: 62h (약 2주)

### Phase 2: Content Element + 편집 **(P2)** - 2주

- [ ] **Task 2.1**: ImageBox (Single) (10h)
  - **의존**: Task 1.5
  - [ ] ImageBoxElement (fitMode: realSize/boxFit/modified)
  - [ ] imageRefs, source 매핑
  - [ ] 이미지 로딩 및 표시 (img 또는 cornerstone 연동은 호스트)
  - [ ] DragResizeDiv 래핑

- [ ] **Task 2.2**: TextBox + Label (8h)
  - **의존**: Task 1.5
  - [ ] LabelElement (평문 텍스트)
  - [ ] TextBoxElement 기본 구조 (content, editable)
  - [ ] style.fontSize(pt), fontFamily 적용
  - [ ] 읽기 전용 렌더링 (편집 모드 전)

- [ ] **Task 2.3**: Lexical 연동 (12h)
  - **의존**: Task 2.2
  - [ ] Lexical 에디터 컴포넌트 래퍼
  - [ ] HTML ↔ Lexical 직렬화
  - [ ] foreignObject 내 편집기 배치
  - [ ] sanitizeHtml 적용 (PoC-11, DOMPurify 등)

- [ ] **Task 2.4**: 상태 관리 (10h)
  - **의존**: Task 2.3
  - [ ] ElementState (elements, selectedElements, clipboard, history)
  - [ ] addElement, updateElement, deleteElement, selectElements
  - [ ] Redux Toolkit slice 또는 Context

- [ ] **Task 2.5**: 복사/붙여넣기, Undo/Redo (8h)
  - **의존**: Task 2.4
  - [ ] Ctrl+C, Ctrl+V
  - [ ] Ctrl+Z, Ctrl+Y (history.past/future)
  - [ ] Arrow 키 이동 (선택 시)

**Phase 2 예상 시간**: 48h (약 1.5주)

### Phase 3: 고급 Element **(P3)** - 2주

- [ ] **Task 3.1**: Arrow, Memo (12h)
  - **의존**: Task 2.5
  - [ ] ArrowElement (Line + 화살표 머리, points)
  - [ ] MemoElement (anchorPoint, bubblePosition, content)
  - [ ] Memo 풍선+포인터 렌더링 (PoC-06 스키마)

- [ ] **Task 3.2**: Multi / Reference ImageBox (10h)
  - **의존**: Task 2.1
  - [ ] layout.row, layout.column (1~20)
  - [ ] Multi ImageBox 그리드 렌더링
  - [ ] Reference ImageBox (linkedBoxId 참조)

- [ ] **Task 3.3**: FreeDraw (6h)
  - **의존**: Task 2.5
  - [ ] FreeDrawElement (points → SVG path)
  - [ ] Path 데이터 직렬화

- [ ] **Task 3.4**: 인쇄 및 @media print (8h)
  - **의존**: Task 3.3
  - [ ] @media print CSS (PoC-10)
  - [ ] @page size, margin
  - [ ] mm, pt 단위 출력 검증
  - [ ] window.print() 연동

**Phase 3 예상 시간**: 36h (약 1주)

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

**총 예상 시간**: 196h (약 7주)

**산출물**:

1. **React DragResizeDiv 컴포넌트**: ezorthoweb의 700줄 Handler 시스템 완벽 포팅
2. **Element 클래스 라이브러리**: TypeScript React 기반 Element 시스템
3. **렌더링 엔진**: SVG/Canvas 기반 Element 렌더러
4. **Handler 시스템**: 완전한 Drag & Resize 핸들러 (8개 + Line용 2개)
5. **HTML 편집기 통합**: 의료용 텍스트 편집 시스템
6. **상태 관리 시스템**: Element 편집 상태 관리
7. **DragResizeDiv 포팅 가이드**: Vue → TypeScript React 포팅 상세 방법론 (핵심 자산)
8. **성능 벤치마크**: Element 렌더링 성능 분석
9. **호환성 검증 리포트**: 기존 파일 호환성 확인

**다음 단계**: 구현된 Element 렌더링 엔진을 PoC-08(아키텍처 전략)에 통합하여 전체 시스템 검증

---

**17. Repository 구성** (PoC-08 반영):

### 17.1 개발 전략: Monorepo 우선, Publish는 완료 시점

**권장**: Monorepo로 개발하고, SCP Cloud 통합 준비 시점에 @ewoosoft/scp-report-library로 NPM Private Publish.

| 방식 | 장점 | 단점 |
|------|------|------|
| **Monorepo + workspace** | 즉시 반영 테스트, publish 없이 개발, atomic commit | 초기 설정 필요 |
| 처음부터 NPM publish | 단순 | 매 변경마다 publish 필요, 피드백 루프 느림 |

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
- core: engine, elements, utils, types (Task 1.1~1.5, 2.1~2.2, 3.1~3.3)
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

**상세**: PoC-08_아키텍처전략검증_result.md 4.4절

### 17.6 Task 0 반영

로드맵 Phase 1 Task 0에 Repository 초기화 포함 (PoC-08 구조):
- [x] Monorepo 루트 생성 (pnpm workspaces + Turborepo)
- [x] packages/core, packages/components, packages/migration, packages/library 초기화
- [x] apps/scp-cloud-demo Vite+React 앱 생성
- [x] workspace 링크 설정 (core → components → library → scp-cloud-demo)
- [x] `pnpm dev` 실행 시 scp-cloud-demo에서 library 사용 검증

---

**참조 문서** (구현 시 필수 확인):

- PoC-06_통합Element스키마설계_result.md: Element 타입, position/size 구조, Memo anchorPoint, Block/Group
- PoC-08_아키텍처전략검증_result.md: Repository 구조, Monorepo, NPM Private Registry, 패키지 설계
- PoC-10_인쇄및Export품질검증_result.md: @media print, mm/pt 단위, CSS 인쇄 가이드
- PoC-11_의료데이터보안검증_result.md: sanitizeHtml, onAuditEvent, XSS 방지

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
