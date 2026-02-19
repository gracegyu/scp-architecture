# PoC-07 결과 보고서: Migration 시스템 설계

## 요약

- **목표**: E2, E3, EzOrtho, CleverOne 4개 제품의 다양한 버전 리포트 파일을 SCP Cloud 포맷(PoC-06 통합 스키마)으로 완벽 변환
- **Migration 경로**: 제품별/버전별 다단계 변환 파이프라인 설계 (E3: v1.x→v1.1.5→v4.0→v5.1→Cloud)
- **좌표 변환**: 비율값/픽셀/mm 혼재 → mm 통일 (소수점 3자리), 용지 크기·Margin 기반 정밀 변환
- **데이터 처리**: Base64 이미지 추출, Template 정보 변환, Annotation 좌표 정규화, 구조 재편(XML→JSON)
- **검증 시스템**: 구조 검증(JSON Schema), 시각적 검증(렌더링 비교), 좌표 정확도 검증(±0.1mm 이내)
- **산출물**: Migration 엔진, 검증 도구, 호환성 보고서, 예외 처리 매뉴얼, 사용자 가이드

---

## 1. 개요

### 1.1 검증 목표

기존 4개 Desktop 제품(E2, E3, EzOrtho, CleverOne)의 다양한 버전에서 생성된 리포트 파일들을 **데이터 손실 없이** SCP Cloud 포맷(PoC-06 통합 Element 스키마)으로 완벽하게 변환하는 자동화된 Migration 시스템을 설계하고 검증합니다.

**핵심 과제**:
- 제품별 다른 좌표 단위 시스템 (비율값, 픽셀, mm) 통일
- 버전별 복잡한 호환성 문제 해결 (E3 v1.x→v5.1 다단계 변환)
- 특수 데이터 처리 (Base64 이미지, Template, Annotation, Chart)
- 의료 데이터 무결성 보장 및 법적 요구사항 준수

### 1.2 선행 PoC 반영

| PoC    | 결정 사항                          | Migration 반영                                              |
| ------ | ---------------------------------- | ----------------------------------------------------------- |
| PoC-02 | mm 좌표, 소수점 3자리              | 모든 제품 좌표 → mm 변환, 정밀도 통일                       |
| PoC-03 | pt 폰트, 96/72 DPI                 | 폰트 단위 → pt 변환, DPI 정규화                             |
| PoC-06 | 통합 Element 스키마 (JSON)         | Migration 목표 포맷, 모든 Element 타입 매핑                 |
| 기존   | E3 VTE3Migration 도구              | 기존 v1.x→v5.1 변환 로직 활용 및 확장                       |

### 1.3 설계 원칙

1. **무손실 변환**: 모든 Element, 속성, 메타데이터 완전 보존
2. **정밀도 보장**: 좌표 변환 오차 ±0.1mm 이내 목표
3. **자동화 우선**: 수동 개입 최소화, 예외 상황만 Manual Override
4. **검증 가능**: 변환 전후 자동/시각적 검증 시스템 구축
5. **확장 가능**: 신규 제품/버전 추가 용이한 플러그인 구조

---

## 2. 제품별 Migration 경로 분석

### 2.1 E2 v3.0 → Cloud

**특징**:
- 가장 단순한 구조 (Template 시스템 부재)
- Paper, ImageBox, TextBox 중심

**좌표 시스템**:
- **입력**: 비율값 (0~1 범위, 소수점 3자리)
- **용지 정보**: 파일 포함 여부 **확인 필요** (Template 부재로 미포함 가능성)
- **변환 전략**:
  - 용지 정보 있음: `mm = (비율값 × (용지크기 - Margin × 2)) + Margin`
  - 용지 정보 없음: 기본값(A4 Portrait, Margin 10mm) 사용 또는 사용자 입력 요청

**Migration 단계**:
```
E2 v3.0 XML → 좌표 변환 (비율→mm) → Cloud JSON
```

**주요 변환 항목**:
| E2 Element      | Cloud Element | 변환 내용                          |
| --------------- | ------------- | ---------------------------------- |
| Paper           | paper         | 용지 크기, Orientation, Margin     |
| ImageBox        | imageBox      | 좌표·크기 변환, fitMode 매핑       |
| TextBox         | textBox       | 좌표·크기 변환, 평문→HTML 변환     |

**예외 처리**:
- 용지 정보 누락: 사용자에게 용지 크기 선택 UI 제공
- 손상된 XML: 복구 가능한 부분까지 변환, 오류 로그 생성

### 2.2 E3 v1.x → Cloud

**특징**:
- 가장 복잡한 다단계 변환 경로
- Base64 이미지 내장 (v1.x)
- 기존 VTE3Migration 도구 활용

**Migration 경로**:
```
E3 v1.x → v1.1.5 → v4.0 → v5.1 → Cloud
```

**버전별 처리**:

**v1.0.5 이하**:
- Migration 미지원 (EEEN-1589 정책)
- 사용자에게 업그레이드 안내

**v1.1.4 → v1.1.5**:
- 기존 VTE3Migration 도구 사용
- Base64 이미지 → 파일 추출 및 저장
- 이미지 무결성 검증 (체크썸)

**v1.1.5 → v4.0 → v5.1**:
- 기존 변환 로직 활용
- Template 정보 정규화
- Annotation 데이터 구조 변환

**v5.1 → Cloud**:
- **E3 Report v4.0/v5.0**: 비율값 → mm 변환
  - **용지 정보**: `<Paper>` 섹션 포함 (PaperSize, Orientation, Margin)
  - **주의**: PageSetting 미설정 시 Setting의 paper setting 사용
  - 변환 공식: `mm = (비율값 × (용지크기 - Margin × 2)) + Margin`
- **E3 RC Report v5.1**: mm (1자리) → mm (3자리)
  - 정밀도만 확장: `105.5mm` → `105.500mm`
  - 기존 값의 정밀도 한계로 인한 오차 허용

**주요 변환 항목**:
| E3 Element       | Cloud Element | 변환 내용                                 |
| ---------------- | ------------- | ----------------------------------------- |
| ItemBox(Text)    | textBox       | 좌표 변환, AutoFill 매크로 변환           |
| ItemBox(Image)   | imageBox      | 좌표 변환, CapturedImageInfo 매핑         |
| Layout           | -             | Row/Column 레이아웃 → 개별 Element 배치   |
| Annotation       | annotation    | 6종 타입 매핑, 좌표 변환                  |
| Template         | metadata      | templateName, Header/Footer 정보 변환     |

**Base64 이미지 처리**:
```typescript
interface ImageExtractor {
  extractBase64(xml: string): ImageData[]
  saveToPNG(imageData: ImageData): string  // 파일 경로 반환
  validateChecksum(file: string): boolean
}
```

### 2.3 EzOrtho v1.0 → Cloud

**특징**:
- 다중 Chart 구조 (Treatment Chart, History Chart 등)
- 치아 번호 체계 (ToothCode) 매핑 필요
- Block 구조 (Containment, 상대 좌표)

**좌표 시스템**:
- **입력**: mm 단위 (주석에 `<!-- unit : mm -->` 명시)
- **변환**: 기존 mm 값 유지, 정밀도 확장 (소수점 3자리)

**Migration 단계**:
```
EzOrtho v1.0 XML → Chart 분석 → Block 구조 변환 → Cloud JSON
```

**주요 변환 항목**:
| EzOrtho Element   | Cloud Element      | 변환 내용                                    |
| ----------------- | ------------------ | -------------------------------------------- |
| Label             | label              | 좌표·크기 유지, 정밀도 확장                  |
| TextBox           | textBox            | 좌표·크기 유지, 평문→HTML 변환               |
| ImageBox          | imageBox           | 좌표·크기 유지, source 매핑                  |
| ToothBox          | toothBox           | ToothCode 매핑 테이블 적용                   |
| TreatmentCategory | treatmentCategory  | 3단계 카테고리 구조 유지 (P2)                |
| Block             | block              | Containment 구조 유지, 상대→절대 좌표 변환   |
| Image             | image              | 앱 번들 리소스 → 클라우드 스토리지 경로 매핑 |
| Form Controls     | 해당 타입          | CheckBox, RadioButton, ComboBox 등 매핑      |

**ToothCode 매핑**:
```typescript
// EzOrtho → FDI 치아 번호 체계
const toothCodeMap: Record<string, string> = {
  "UR8": "18", "UR7": "17", "UR6": "16", // ...
  "UL1": "21", "UL2": "22", // ...
  // 전체 매핑 테이블
}
```

**Block 구조 변환**:
- **입력**: 중첩 XML, 자식 요소 상대 좌표
- **출력**: JSON, 자식 요소 절대 좌표 또는 Containment 구조 유지
- **변환 전략**: PoC-06 Block 정의에 따라 `children: Element[]` 구조 유지

**Chart 데이터 처리**:
- Treatment Chart, History Chart 등 → 별도 페이지 또는 메타데이터로 변환
- 시간축 기반 치료 이력 → extensions 영역에 구조화

### 2.4 CleverOne v5.1.0 → Cloud

**특징**:
- E3 RC Report v5.1과 유사한 구조
- Groups 기능 (Reference 구조, ID 참조)
- Template 시스템 지원

**좌표 시스템**:
- **입력**: mm 단위 (소수점 1자리)
- **변환**: 정밀도 확장 (1자리 → 3자리)
- **예시**: `105.5mm` → `105.500mm`

**Migration 단계**:
```
CleverOne v5.1.0 XML → 좌표 변환 (정밀도 확장) → Groups 변환 → Cloud JSON
```

**주요 변환 항목**:
| CleverOne Element | Cloud Element | 변환 내용                                   |
| ----------------- | ------------- | ------------------------------------------- |
| TextBox           | textBox       | HTML 콘텐츠 유지, 좌표 정밀도 확장          |
| ImageBox          | imageBox      | BoxType 매핑 (Single/Multi/Reference)       |
| ToothBox          | toothBox      | ToothCode 매핑                              |
| Annotation        | annotation    | 6종 타입 매핑, Points 정밀도 확장 (4자리)   |
| Groups            | group         | Reference 구조 유지, memberIds 매핑         |
| Template          | metadata      | templateName 변환                           |

**Groups 변환**:
```xml
<!-- CleverOne XML -->
<Groups>
  <Gruop>60|61|59</Gruop>
</Groups>
```

```json
// Cloud JSON
{
  "type": "group",
  "memberIds": ["element-60", "element-61", "element-59"]
}
```

**Annotation Points 정밀도**:
- CleverOne: 소수점 4자리
- Cloud: 소수점 3자리로 반올림 (0.0001mm → 0.001mm 정밀도 허용)

---

## 3. 좌표 단위 변환 시스템

### 3.1 변환 전략 개요

| 제품              | 입력 단위                | 출력 단위         | 변환 방식                  |
| ----------------- | ------------------------ | ----------------- | -------------------------- |
| E2 v3.0           | 비율값 (0~1, 3자리)      | mm (3자리)        | 용지 크기 기반 계산        |
| E3 Report v4/v5   | 비율값 (0~1, 3자리)      | mm (3자리)        | 용지 크기 기반 계산        |
| E3 RC Report v5.1 | mm (1자리)               | mm (3자리)        | 정밀도 확장                |
| EzOrtho v1.0      | mm                       | mm (3자리)        | 정밀도 확장                |
| CleverOne v5.1.0  | mm (1자리)               | mm (3자리)        | 정밀도 확장                |

### 3.2 비율값 → mm 변환 (E2, E3 Report)

**변환 공식**:
```typescript
function ratioToMm(
  ratio: number,
  paperSize: PaperSize,
  orientation: Orientation,
  margin: Margin
): number {
  const paperDimension = getPaperDimension(paperSize, orientation)
  const effectiveSize = paperDimension - (margin.left + margin.right) // 또는 top + bottom
  const mm = (ratio * effectiveSize) + margin.left // 또는 margin.top
  return roundTo3Decimals(mm)
}
```

**용지 크기 정의**:
```typescript
const PAPER_SIZES: Record<string, {width: number, height: number}> = {
  "A4": { width: 210, height: 297 },
  "A3": { width: 297, height: 420 },
  "Letter": { width: 215.9, height: 279.4 },
  "8x10inch": { width: 203.2, height: 254 },
  // ...
}
```

**Orientation 처리**:
```typescript
function getPaperDimension(paperSize: string, orientation: string): {width: number, height: number} {
  const base = PAPER_SIZES[paperSize]
  if (orientation === "Landscape") {
    return { width: base.height, height: base.width }
  }
  return base
}
```

**예시**:
```typescript
// A4 Portrait, Margin 10mm, 비율값 0.500
const mm = ratioToMm(
  0.500,
  "A4",
  "Portrait",
  { left: 10, right: 10, top: 10, bottom: 10 }
)
// (0.500 × (210 - 10 - 10)) + 10 = 105.000mm
```

**용지 정보 누락 처리**:
```typescript
interface MigrationContext {
  defaultPaper?: PaperConfig
  userInputRequired?: boolean
}

function handleMissingPaperInfo(context: MigrationContext): PaperConfig {
  if (context.defaultPaper) {
    return context.defaultPaper
  }
  if (context.userInputRequired) {
    // UI에서 사용자 입력 요청
    return promptUserForPaperConfig()
  }
  // 최종 기본값
  return { paperSize: "A4", orientation: "Portrait", margin: { all: 10 } }
}
```

### 3.3 정밀도 확장 (E3 RC, EzOrtho, CleverOne)

**변환 로직**:
```typescript
function expandPrecision(mmValue: number, sourcePrecision: number): number {
  // 이미 mm 단위이므로 정밀도만 확장
  return roundTo3Decimals(mmValue)
}

function roundTo3Decimals(value: number): number {
  return Math.round(value * 1000) / 1000
}
```

**예시**:
```typescript
// E3 RC Report v5.1: 105.5mm (1자리)
expandPrecision(105.5, 1) // → 105.500mm

// CleverOne Annotation Points: 62.3654mm (4자리)
roundTo3Decimals(62.3654) // → 62.365mm (반올림)
```

### 3.4 좌표 변환 검증

**검증 항목**:
1. **절대 오차**: 변환 전후 ±0.1mm 이내
2. **상대 오차**: Element 간 거리 비율 유지
3. **역변환 검증**: mm → 비율값 → mm 일치 확인

**검증 코드**:
```typescript
interface CoordinateValidator {
  validateAbsoluteError(original: Point, converted: Point): boolean {
    const errorX = Math.abs(original.x - converted.x)
    const errorY = Math.abs(original.y - converted.y)
    return errorX <= 0.1 && errorY <= 0.1
  }

  validateRelativeDistance(
    elements: Element[],
    originalDistances: number[],
    convertedDistances: number[]
  ): boolean {
    for (let i = 0; i < originalDistances.length; i++) {
      const ratio = convertedDistances[i] / originalDistances[i]
      if (Math.abs(ratio - 1.0) > 0.001) { // 0.1% 오차 허용
        return false
      }
    }
    return true
  }

  validateReverseConversion(
    originalRatio: number,
    convertedMm: number,
    paperConfig: PaperConfig
  ): boolean {
    const reversedRatio = mmToRatio(convertedMm, paperConfig)
    return Math.abs(originalRatio - reversedRatio) < 0.001
  }
}
```

---

## 4. Migration 시스템 아키텍처

### 4.1 전체 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    Migration System                          │
├─────────────────────────────────────────────────────────────┤
│  1. File Analyzer (버전 감지, 구조 검증)                     │
│  2. Product-specific Parser (제품별 XML/데이터 파싱)         │
│  3. Coordinate Converter (좌표 단위 변환)                    │
│  4. Data Transformer (Element 변환, 구조 재편)               │
│  5. Validator (구조/데이터/시각적 검증)                      │
│  6. Output Generator (Cloud JSON 생성)                       │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 핵심 컴포넌트

**1. File Analyzer**:
```typescript
interface FileAnalyzer {
  detectVersion(file: Buffer): ProductVersion
  validateStructure(file: Buffer): ValidationResult
  extractMetadata(file: Buffer): FileMetadata
}

interface ProductVersion {
  product: 'E2' | 'E3' | 'EzOrtho' | 'CleverOne'
  version: string
  migrationPath: MigrationStep[]
  coordinateSystem: 'ratio' | 'mm' | 'pixel'
}

interface ValidationResult {
  isValid: boolean
  errors: ValidationError[]
  warnings: ValidationWarning[]
  recoverable: boolean
}
```

**2. Product-specific Parser**:
```typescript
interface ProductParser {
  parse(xml: string): IntermediateFormat
  extractPaperInfo(xml: string): PaperConfig | null
  extractElements(xml: string): RawElement[]
}

// 제품별 구현
class E2Parser implements ProductParser { /* ... */ }
class E3Parser implements ProductParser { /* ... */ }
class EzOrthoParser implements ProductParser { /* ... */ }
class CleverOneParser implements ProductParser { /* ... */ }
```

**3. Coordinate Converter**:
```typescript
interface CoordinateConverter {
  convert(
    element: RawElement,
    sourceSystem: CoordinateSystem,
    paperConfig: PaperConfig
  ): ConvertedElement

  ratioToMm(ratio: number, paperConfig: PaperConfig): number
  expandPrecision(mm: number, sourcePrecision: number): number
  validateConversion(original: RawElement, converted: ConvertedElement): boolean
}
```

**4. Data Transformer**:
```typescript
interface DataTransformer {
  transformElement(raw: RawElement, product: string): CloudElement
  transformAnnotation(raw: RawAnnotation): CloudAnnotation
  transformBlock(raw: RawBlock): CloudBlock
  transformGroup(raw: RawGroup): CloudGroup
  extractImages(raw: RawElement): ImageData[]
}
```

**5. Validator**:
```typescript
interface Validator {
  // 구조 검증
  validateSchema(json: CloudDocument): SchemaValidationResult
  
  // 데이터 검증
  validateDataIntegrity(
    original: IntermediateFormat,
    converted: CloudDocument
  ): DataValidationResult
  
  // 시각적 검증
  compareRendering(
    originalPdf: Buffer,
    convertedPdf: Buffer
  ): VisualComparisonResult
}
```

**6. Output Generator**:
```typescript
interface OutputGenerator {
  generate(transformed: CloudDocument): string // JSON
  prettify(json: string): string
  compress(json: string): string
}
```

### 4.3 Migration 파이프라인

```typescript
class MigrationPipeline {
  async migrate(inputFile: Buffer): Promise<MigrationResult> {
    // 1. 파일 분석
    const version = await this.analyzer.detectVersion(inputFile)
    const validation = await this.analyzer.validateStructure(inputFile)
    
    if (!validation.isValid && !validation.recoverable) {
      throw new MigrationError('Unrecoverable file structure')
    }

    // 2. 파싱
    const parser = this.getParser(version.product)
    const intermediate = await parser.parse(inputFile.toString())
    const paperConfig = await parser.extractPaperInfo(inputFile.toString())

    // 3. 좌표 변환
    const converted = await this.converter.convertAll(
      intermediate.elements,
      version.coordinateSystem,
      paperConfig || this.getDefaultPaperConfig()
    )

    // 4. 데이터 변환
    const transformed = await this.transformer.transformAll(
      converted,
      version.product
    )

    // 5. 검증
    const schemaResult = await this.validator.validateSchema(transformed)
    const dataResult = await this.validator.validateDataIntegrity(
      intermediate,
      transformed
    )

    if (!schemaResult.isValid || !dataResult.isValid) {
      throw new MigrationError('Validation failed', {
        schemaErrors: schemaResult.errors,
        dataErrors: dataResult.errors
      })
    }

    // 6. 출력 생성
    const output = await this.generator.generate(transformed)

    return {
      success: true,
      output,
      metadata: {
        sourceProduct: version.product,
        sourceVersion: version.version,
        conversionTime: Date.now(),
        warnings: validation.warnings
      }
    }
  }
}
```

---

## 5. 특수 데이터 처리

### 5.1 Base64 이미지 추출 (E3 v1.x)

**처리 흐름**:
```typescript
class ImageExtractor {
  async extractBase64Images(xml: string): Promise<ImageData[]> {
    const images: ImageData[] = []
    const regex = /<ImageData[^>]*>(.*?)<\/ImageData>/gs
    
    let match
    while ((match = regex.exec(xml)) !== null) {
      const base64 = match[1].trim()
      const imageData = {
        id: generateImageId(),
        base64,
        format: this.detectFormat(base64),
        checksum: this.calculateChecksum(base64)
      }
      images.push(imageData)
    }
    
    return images
  }

  async saveToPNG(imageData: ImageData, outputDir: string): Promise<string> {
    const buffer = Buffer.from(imageData.base64, 'base64')
    const filename = `${imageData.id}.${imageData.format}`
    const filepath = path.join(outputDir, filename)
    
    await fs.writeFile(filepath, buffer)
    
    // 무결성 검증
    const savedChecksum = await this.calculateFileChecksum(filepath)
    if (savedChecksum !== imageData.checksum) {
      throw new Error('Image checksum mismatch')
    }
    
    return filepath
  }

  private detectFormat(base64: string): string {
    const header = base64.substring(0, 20)
    if (header.startsWith('iVBOR')) return 'png'
    if (header.startsWith('/9j/')) return 'jpg'
    return 'unknown'
  }

  private calculateChecksum(data: string): string {
    return crypto.createHash('sha256').update(data).digest('hex')
  }
}
```

**변환 매핑**:
```xml
<!-- E3 v1.x -->
<ImageData>iVBORw0KGgoAAAANSUhEUgAA...</ImageData>
```

```json
// Cloud JSON
{
  "type": "imageBox",
  "imageRefs": ["extracted-image-001.png"],
  "source": "file"
}
```

### 5.2 Template 정보 변환

**E3 Template 구조**:
```xml
<Template>
  <TemplateName>Orthodontic Report</TemplateName>
  <Header>
    <TextBox>Clinic Name</TextBox>
  </Header>
  <Footer>
    <TextBox>Page {PageNumber}</TextBox>
  </Footer>
  <Paper>
    <PaperSize>A4</PaperSize>
    <Orientation>Portrait</Orientation>
    <Margin Left="10" Right="10" Top="15" Bottom="15"/>
  </Paper>
</Template>
```

**Cloud 변환**:
```json
{
  "metadata": {
    "templateName": "Orthodontic Report"
  },
  "paper": {
    "size": "A4",
    "orientation": "portrait",
    "margin": {
      "unit": "mm",
      "left": 10,
      "right": 10,
      "top": 15,
      "bottom": 15
    }
  },
  "pages": [
    {
      "header": {
        "elements": [
          {
            "type": "textBox",
            "content": "Clinic Name"
          }
        ]
      },
      "footer": {
        "elements": [
          {
            "type": "textBox",
            "content": "Page {PageNumber}"
          }
        ]
      }
    }
  ]
}
```

### 5.3 Annotation 좌표 변환

**CleverOne Annotation (Points 4자리)**:
```xml
<Annotation AnnotationType="FreeDraw">
  <Points>62.3654,51.0892|65.1234,52.4567|68.9876,54.3210</Points>
</Annotation>
```

**Cloud 변환 (3자리로 반올림)**:
```json
{
  "type": "freeDraw",
  "points": [
    {"x": 62.365, "y": 51.089},
    {"x": 65.123, "y": 52.457},
    {"x": 68.988, "y": 54.321}
  ]
}
```

**Memo Annotation 개선**:
```xml
<!-- CleverOne (2개 점) -->
<Annotation AnnotationType="Memo">
  <Points>160,115|175,133</Points>
  <Memo>메모 텍스트</Memo>
</Annotation>
```

```json
// Cloud (bubblePosition 추가)
{
  "type": "memo",
  "position": {"x": 160, "y": 115},
  "size": {"width": 30, "height": 18},
  "anchorPoint": {"x": 175, "y": 133},
  "bubblePosition": "left",
  "content": "메모 텍스트"
}
```

### 5.4 Block 구조 변환 (EzOrtho)

**EzOrtho Block (중첩 XML, 상대 좌표)**:
```xml
<Block Name="Face" IsVisible="true" Left="20" Top="50">
  <Image Source="Face.png" Left="0" Top="0" Width="80" Height="100"/>
  <TextBox Content="1" Left="10" Top="30" Width="20" Height="10"/>
</Block>
```

**Cloud 변환 (Containment 구조 유지)**:
```json
{
  "type": "block",
  "position": {"unit": "mm", "x": 20, "y": 50},
  "size": {"unit": "mm", "width": 80, "height": 100},
  "name": "Face",
  "visible": true,
  "children": [
    {
      "type": "image",
      "position": {"unit": "mm", "x": 0, "y": 0},
      "size": {"unit": "mm", "width": 80, "height": 100},
      "source": "Face.png"
    },
    {
      "type": "textBox",
      "position": {"unit": "mm", "x": 10, "y": 30},
      "size": {"unit": "mm", "width": 20, "height": 10},
      "content": "1"
    }
  ]
}
```

**상대→절대 좌표 변환 옵션**:
```typescript
function convertBlockToAbsolute(block: CloudBlock): CloudElement[] {
  const elements: CloudElement[] = []
  
  for (const child of block.children) {
    elements.push({
      ...child,
      position: {
        x: block.position.x + child.position.x,
        y: block.position.y + child.position.y
      }
    })
  }
  
  return elements
}
```

### 5.5 Group 구조 변환 (CleverOne)

**CleverOne Groups (ID 참조)**:
```xml
<Groups>
  <Gruop>60|61|59</Gruop>
  <Gruop>62|63</Gruop>
</Groups>
```

**Cloud 변환**:
```json
{
  "pages": [
    {
      "elements": [
        {
          "id": "group-1",
          "type": "group",
          "memberIds": ["element-60", "element-61", "element-59"]
        },
        {
          "id": "group-2",
          "type": "group",
          "memberIds": ["element-62", "element-63"]
        }
      ]
    }
  ]
}
```

---

## 6. 검증 시스템

### 6.1 구조 검증 (JSON Schema)

**검증 항목**:
- 필수 필드 존재 여부
- 데이터 타입 일치
- Enum 값 유효성
- 참조 무결성 (Element ID, imageRefs 등)

**구현**:
```typescript
import Ajv from 'ajv'

class SchemaValidator {
  private ajv: Ajv
  private schema: object

  constructor() {
    this.ajv = new Ajv({ allErrors: true })
    this.schema = require('./cloud-report-schema.json')
  }

  validate(document: CloudDocument): SchemaValidationResult {
    const valid = this.ajv.validate(this.schema, document)
    
    if (!valid) {
      return {
        isValid: false,
        errors: this.ajv.errors.map(err => ({
          path: err.instancePath,
          message: err.message,
          params: err.params
        }))
      }
    }

    // 추가 검증: 참조 무결성
    const refErrors = this.validateReferences(document)
    
    return {
      isValid: refErrors.length === 0,
      errors: refErrors
    }
  }

  private validateReferences(document: CloudDocument): ValidationError[] {
    const errors: ValidationError[] = []
    const elementIds = new Set<string>()

    // 모든 Element ID 수집
    for (const page of document.pages) {
      for (const element of page.elements) {
        if (elementIds.has(element.id)) {
          errors.push({
            path: `/pages/${page.number}/elements/${element.id}`,
            message: 'Duplicate element ID'
          })
        }
        elementIds.add(element.id)
      }
    }

    // 참조 검증
    for (const page of document.pages) {
      for (const element of page.elements) {
        // ImageBox linkedBoxId 검증
        if (element.type === 'imageBox' && element.linkedBoxId) {
          if (!elementIds.has(element.linkedBoxId)) {
            errors.push({
              path: `/pages/${page.number}/elements/${element.id}/linkedBoxId`,
              message: `Referenced element '${element.linkedBoxId}' not found`
            })
          }
        }

        // Group memberIds 검증
        if (element.type === 'group') {
          for (const memberId of element.memberIds) {
            if (!elementIds.has(memberId)) {
              errors.push({
                path: `/pages/${page.number}/elements/${element.id}/memberIds`,
                message: `Referenced element '${memberId}' not found`
              })
            }
          }
        }
      }
    }

    return errors
  }
}
```

### 6.2 데이터 무결성 검증

**검증 항목**:
- Element 개수 일치
- 좌표 변환 정확도 (±0.1mm)
- 속성 값 보존 (content, style 등)
- 이미지 체크썸 일치

**구현**:
```typescript
class DataIntegrityValidator {
  validate(
    original: IntermediateFormat,
    converted: CloudDocument
  ): DataValidationResult {
    const errors: ValidationError[] = []

    // Element 개수 검증
    const originalCount = this.countElements(original)
    const convertedCount = this.countElements(converted)
    if (originalCount !== convertedCount) {
      errors.push({
        message: `Element count mismatch: ${originalCount} → ${convertedCount}`
      })
    }

    // 좌표 정확도 검증
    const coordErrors = this.validateCoordinates(original, converted)
    errors.push(...coordErrors)

    // 속성 보존 검증
    const attrErrors = this.validateAttributes(original, converted)
    errors.push(...attrErrors)

    return {
      isValid: errors.length === 0,
      errors
    }
  }

  private validateCoordinates(
    original: IntermediateFormat,
    converted: CloudDocument
  ): ValidationError[] {
    const errors: ValidationError[] = []
    const tolerance = 0.1 // mm

    // Element별 좌표 비교
    for (let i = 0; i < original.elements.length; i++) {
      const orig = original.elements[i]
      const conv = converted.pages[0].elements[i] // 단순화

      const errorX = Math.abs(orig.position.x - conv.position.x)
      const errorY = Math.abs(orig.position.y - conv.position.y)

      if (errorX > tolerance || errorY > tolerance) {
        errors.push({
          path: `/elements/${conv.id}/position`,
          message: `Coordinate error exceeds tolerance: (${errorX.toFixed(3)}, ${errorY.toFixed(3)})mm`
        })
      }
    }

    return errors
  }

  private validateAttributes(
    original: IntermediateFormat,
    converted: CloudDocument
  ): ValidationError[] {
    const errors: ValidationError[] = []

    // 주요 속성 비교 (content, style 등)
    for (let i = 0; i < original.elements.length; i++) {
      const orig = original.elements[i]
      const conv = converted.pages[0].elements[i]

      if (orig.content !== conv.content) {
        errors.push({
          path: `/elements/${conv.id}/content`,
          message: 'Content mismatch'
        })
      }

      // style 속성 비교
      if (orig.style?.fontSize !== conv.style?.fontSize) {
        errors.push({
          path: `/elements/${conv.id}/style/fontSize`,
          message: 'Font size mismatch'
        })
      }
    }

    return errors
  }
}
```

### 6.3 시각적 검증

**렌더링 비교**:
```typescript
class VisualValidator {
  async compareRendering(
    originalFile: Buffer,
    convertedDocument: CloudDocument
  ): Promise<VisualComparisonResult> {
    // 1. 원본 파일 → PDF 렌더링 (기존 제품 사용)
    const originalPdf = await this.renderOriginal(originalFile)

    // 2. 변환 문서 → PDF 렌더링 (Cloud 렌더링 엔진 사용)
    const convertedPdf = await this.renderConverted(convertedDocument)

    // 3. 픽셀 단위 비교
    const comparison = await this.comparePixels(originalPdf, convertedPdf)

    return {
      similarity: comparison.similarity, // 0~1
      differences: comparison.differences,
      thumbnails: {
        original: comparison.originalThumbnail,
        converted: comparison.convertedThumbnail,
        diff: comparison.diffThumbnail
      }
    }
  }

  private async comparePixels(
    pdf1: Buffer,
    pdf2: Buffer
  ): Promise<PixelComparison> {
    const image1 = await this.pdfToImage(pdf1)
    const image2 = await this.pdfToImage(pdf2)

    // Pixel-by-pixel comparison
    const { width, height } = image1
    let differentPixels = 0
    const totalPixels = width * height

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const pixel1 = image1.getPixel(x, y)
        const pixel2 = image2.getPixel(x, y)

        if (!this.pixelsEqual(pixel1, pixel2)) {
          differentPixels++
        }
      }
    }

    const similarity = 1 - (differentPixels / totalPixels)

    return {
      similarity,
      differences: differentPixels,
      totalPixels
    }
  }
}
```

**측정값 검증**:
```typescript
class MeasurementValidator {
  validateDistances(
    original: IntermediateFormat,
    converted: CloudDocument
  ): MeasurementResult {
    const results: MeasurementComparison[] = []

    // Element 간 거리 측정
    for (let i = 0; i < original.elements.length - 1; i++) {
      for (let j = i + 1; j < original.elements.length; j++) {
        const origDist = this.calculateDistance(
          original.elements[i].position,
          original.elements[j].position
        )

        const convDist = this.calculateDistance(
          converted.pages[0].elements[i].position,
          converted.pages[0].elements[j].position
        )

        const error = Math.abs(origDist - convDist)
        const relativeError = error / origDist

        results.push({
          elementPair: [original.elements[i].id, original.elements[j].id],
          originalDistance: origDist,
          convertedDistance: convDist,
          absoluteError: error,
          relativeError
        })
      }
    }

    return {
      comparisons: results,
      maxAbsoluteError: Math.max(...results.map(r => r.absoluteError)),
      maxRelativeError: Math.max(...results.map(r => r.relativeError))
    }
  }

  private calculateDistance(p1: Point, p2: Point): number {
    return Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2))
  }
}
```

### 6.4 품질 메트릭

**변환 성공률**:
```typescript
interface MigrationMetrics {
  totalFiles: number
  successfulConversions: number
  failedConversions: number
  partialConversions: number // 일부 Element 누락
  successRate: number // 0~1
}

class MetricsCollector {
  private metrics: MigrationMetrics = {
    totalFiles: 0,
    successfulConversions: 0,
    failedConversions: 0,
    partialConversions: 0,
    successRate: 0
  }

  recordConversion(result: MigrationResult) {
    this.metrics.totalFiles++

    if (result.success && result.warnings.length === 0) {
      this.metrics.successfulConversions++
    } else if (result.success && result.warnings.length > 0) {
      this.metrics.partialConversions++
    } else {
      this.metrics.failedConversions++
    }

    this.metrics.successRate =
      (this.metrics.successfulConversions + this.metrics.partialConversions) /
      this.metrics.totalFiles
  }

  getReport(): MigrationMetrics {
    return { ...this.metrics }
  }
}
```

---

## 7. 예외 상황 처리

### 7.1 손상된 파일

**복구 전략**:
```typescript
class FileRecovery {
  async recoverPartial(file: Buffer): Promise<RecoveryResult> {
    try {
      // XML 구조 복구 시도
      const xml = file.toString()
      const recovered = this.repairXml(xml)

      // 복구된 부분 파싱
      const parser = new DOMParser()
      const doc = parser.parseFromString(recovered, 'text/xml')

      // 유효한 Element만 추출
      const validElements = this.extractValidElements(doc)

      return {
        recoverable: true,
        elements: validElements,
        lostElements: this.countLostElements(doc),
        warnings: ['Some elements could not be recovered']
      }
    } catch (error) {
      return {
        recoverable: false,
        error: error.message
      }
    }
  }

  private repairXml(xml: string): string {
    // 닫히지 않은 태그 복구
    xml = this.closeUnclosedTags(xml)

    // 잘못된 인코딩 수정
    xml = this.fixEncoding(xml)

    // 특수 문자 이스케이프
    xml = this.escapeSpecialChars(xml)

    return xml
  }
}
```

### 7.2 비표준 구조

**Manual Override**:
```typescript
interface ManualOverride {
  elementId: string
  overrideType: 'coordinate' | 'attribute' | 'structure'
  originalValue: any
  correctedValue: any
  reason: string
}

class ManualOverrideHandler {
  private overrides: Map<string, ManualOverride[]> = new Map()

  registerOverride(fileId: string, override: ManualOverride) {
    if (!this.overrides.has(fileId)) {
      this.overrides.set(fileId, [])
    }
    this.overrides.get(fileId).push(override)
  }

  applyOverrides(
    fileId: string,
    document: CloudDocument
  ): CloudDocument {
    const overrides = this.overrides.get(fileId) || []

    for (const override of overrides) {
      const element = this.findElement(document, override.elementId)

      if (element) {
        switch (override.overrideType) {
          case 'coordinate':
            element.position = override.correctedValue
            break
          case 'attribute':
            Object.assign(element, override.correctedValue)
            break
          case 'structure':
            // 구조적 변경 (복잡한 로직)
            this.applyStructuralChange(element, override)
            break
        }
      }
    }

    return document
  }
}
```

### 7.3 변환 실패 로깅

**상세 오류 로그**:
```typescript
interface MigrationError {
  timestamp: string
  fileId: string
  product: string
  version: string
  stage: 'parsing' | 'conversion' | 'validation' | 'output'
  errorType: string
  message: string
  stack?: string
  context?: any
}

class ErrorLogger {
  private errors: MigrationError[] = []

  logError(error: MigrationError) {
    this.errors.push(error)

    // 파일로 저장
    fs.appendFileSync(
      'migration-errors.log',
      JSON.stringify(error, null, 2) + '\n'
    )

    // 심각한 오류는 즉시 알림
    if (this.isCritical(error)) {
      this.notifyAdmin(error)
    }
  }

  generateReport(): ErrorReport {
    return {
      totalErrors: this.errors.length,
      errorsByStage: this.groupByStage(),
      errorsByProduct: this.groupByProduct(),
      topErrors: this.getTopErrors(10)
    }
  }

  private groupByStage(): Record<string, number> {
    const grouped: Record<string, number> = {}
    for (const error of this.errors) {
      grouped[error.stage] = (grouped[error.stage] || 0) + 1
    }
    return grouped
  }
}
```

---

## 8. 성능 최적화

### 8.1 병렬 처리

**다중 파일 동시 변환**:
```typescript
class ParallelMigrator {
  private maxConcurrency: number = 4

  async migrateMultiple(files: Buffer[]): Promise<MigrationResult[]> {
    const results: MigrationResult[] = []
    const queue = [...files]

    // Worker pool 생성
    const workers = Array.from({ length: this.maxConcurrency }, () =>
      this.createWorker()
    )

    // 병렬 처리
    const promises = workers.map(async (worker) => {
      while (queue.length > 0) {
        const file = queue.shift()
        if (file) {
          const result = await worker.migrate(file)
          results.push(result)
        }
      }
    })

    await Promise.all(promises)

    return results
  }

  private createWorker(): MigrationWorker {
    return new MigrationPipeline()
  }
}
```

### 8.2 진행 상황 추적

**실시간 진행률 표시**:
```typescript
interface ProgressTracker {
  totalFiles: number
  processedFiles: number
  currentFile: string
  currentStage: string
  estimatedTimeRemaining: number
}

class MigrationProgress {
  private tracker: ProgressTracker = {
    totalFiles: 0,
    processedFiles: 0,
    currentFile: '',
    currentStage: '',
    estimatedTimeRemaining: 0
  }

  private startTime: number = 0
  private listeners: ((progress: ProgressTracker) => void)[] = []

  start(totalFiles: number) {
    this.tracker.totalFiles = totalFiles
    this.startTime = Date.now()
  }

  updateProgress(fileId: string, stage: string) {
    this.tracker.currentFile = fileId
    this.tracker.currentStage = stage

    if (stage === 'completed') {
      this.tracker.processedFiles++
    }

    // 남은 시간 추정
    const elapsed = Date.now() - this.startTime
    const avgTimePerFile = elapsed / this.tracker.processedFiles
    const remainingFiles = this.tracker.totalFiles - this.tracker.processedFiles
    this.tracker.estimatedTimeRemaining = avgTimePerFile * remainingFiles

    // 리스너에게 알림
    this.notifyListeners()
  }

  onProgress(callback: (progress: ProgressTracker) => void) {
    this.listeners.push(callback)
  }

  private notifyListeners() {
    for (const listener of this.listeners) {
      listener({ ...this.tracker })
    }
  }
}
```

### 8.3 캐싱 전략

**중간 결과 캐싱**:
```typescript
class MigrationCache {
  private cache: Map<string, CachedResult> = new Map()

  async getOrMigrate(
    fileId: string,
    file: Buffer,
    migrator: MigrationPipeline
  ): Promise<MigrationResult> {
    // 캐시 확인
    const cached = this.cache.get(fileId)
    if (cached && this.isValid(cached)) {
      return cached.result
    }

    // Migration 수행
    const result = await migrator.migrate(file)

    // 캐시 저장
    this.cache.set(fileId, {
      result,
      timestamp: Date.now(),
      fileHash: this.calculateHash(file)
    })

    return result
  }

  private isValid(cached: CachedResult): boolean {
    const maxAge = 24 * 60 * 60 * 1000 // 24시간
    return Date.now() - cached.timestamp < maxAge
  }

  private calculateHash(file: Buffer): string {
    return crypto.createHash('sha256').update(file).digest('hex')
  }
}
```

---

## 9. Migration 매핑 테이블 (상세)

### 9.1 E2 Element 매핑

| E2 Element | Cloud Element | 변환 규칙                                                    |
| ---------- | ------------- | ------------------------------------------------------------ |
| Paper      | paper         | PaperSize, Orientation, Margin 직접 매핑                     |
| ImageBox   | imageBox      | 비율값→mm 변환, fitMode 매핑 (Fit→boxFit, Real→realSize)    |
| TextBox    | textBox       | 비율값→mm 변환, 평문→`<html><body>...</body></html>` 변환   |

### 9.2 E3 Element 매핑

| E3 Element         | Cloud Element | 변환 규칙                                                         |
| ------------------ | ------------- | ----------------------------------------------------------------- |
| ItemBox(Text)      | textBox       | 비율값→mm, AutoFill→textMacro 매핑                                |
| ItemBox(Image)     | imageBox      | 비율값→mm, CapturedImageInfo→imageRefs 매핑                       |
| Layout(Row/Column) | -             | 레이아웃 계산 후 개별 Element로 분해                              |
| Annotation         | annotation    | 6종 타입 매핑, Points 비율값→mm 변환                              |
| Template           | metadata      | templateName, Header/Footer → metadata 및 page.header/footer 매핑 |

**Annotation 타입 매핑**:
| E3 AnnotationType | Cloud type    |
| ----------------- | ------------- |
| Rectangle         | rectangle     |
| Ellipse           | ellipse       |
| Line              | line          |
| Arrow             | arrow         |
| FreeDraw          | freeDraw      |
| Memo              | memo          |

### 9.3 EzOrtho Element 매핑

| EzOrtho Element   | Cloud Element      | 변환 규칙                                                 |
| ----------------- | ------------------ | --------------------------------------------------------- |
| Label             | label              | mm 유지, 정밀도 확장                                      |
| TextBox           | textBox            | mm 유지, 평문→HTML 변환                                   |
| ImageBox          | imageBox           | mm 유지, source 매핑                                      |
| ToothBox          | toothBox           | mm 유지, ToothCode 매핑 테이블 적용                       |
| TreatmentCategory | treatmentCategory  | mm 유지, 3단계 카테고리 구조 유지 (P2)                    |
| Block             | block              | mm 유지, Containment 구조 유지, children 상대 좌표 유지   |
| Image             | image              | mm 유지, `:/images/img/` → 클라우드 스토리지 경로 매핑    |
| CheckBox          | checkBox           | mm 유지, checked 상태 매핑                                |
| RadioButton       | radioButton        | mm 유지, selected 상태 매핑                               |
| ComboBox          | comboBox           | mm 유지, items 및 selectedIndex 매핑                      |

**ToothCode 매핑 (FDI 체계)**:
```typescript
const TOOTH_CODE_MAP: Record<string, string> = {
  // Upper Right (UR)
  "UR8": "18", "UR7": "17", "UR6": "16", "UR5": "15",
  "UR4": "14", "UR3": "13", "UR2": "12", "UR1": "11",
  // Upper Left (UL)
  "UL1": "21", "UL2": "22", "UL3": "23", "UL4": "24",
  "UL5": "25", "UL6": "26", "UL7": "27", "UL8": "28",
  // Lower Left (LL)
  "LL8": "38", "LL7": "37", "LL6": "36", "LL5": "35",
  "LL4": "34", "LL3": "33", "LL2": "32", "LL1": "31",
  // Lower Right (LR)
  "LR1": "41", "LR2": "42", "LR3": "43", "LR4": "44",
  "LR5": "45", "LR6": "46", "LR7": "47", "LR8": "48",
  // Deciduous teeth...
}
```

### 9.4 CleverOne Element 매핑

| CleverOne Element | Cloud Element | 변환 규칙                                              |
| ----------------- | ------------- | ------------------------------------------------------ |
| TextBox           | textBox       | mm 정밀도 확장, HTML 콘텐츠 유지                       |
| ImageBox          | imageBox      | mm 정밀도 확장, BoxType 매핑 (Single/Multi/Reference)  |
| ToothBox          | toothBox      | mm 정밀도 확장, ToothCode 매핑                         |
| Annotation        | annotation    | mm 정밀도 확장 (4자리→3자리 반올림), 6종 타입 매핑     |
| Groups            | group         | Reference 구조 유지, memberIds 매핑                    |
| Template          | metadata      | templateName 매핑                                      |

**ImageBox BoxType 매핑**:
| CleverOne BoxType | Cloud 구조                                       |
| ----------------- | ------------------------------------------------ |
| Single            | `layout` 생략 또는 `{row: 1, column: 1}`         |
| Multi             | `layout: {row: N, column: M}`, `imageRefs` 배열  |
| Reference         | `source: "reference"`, `linkedBoxId` 지정        |

---

## 10. 호환성 보고서

### 10.1 제품별 지원 범위

| 제품              | 지원 버전                | 변환 경로                          | 지원 Element 수 | 비고                          |
| ----------------- | ------------------------ | ---------------------------------- | --------------- | ----------------------------- |
| E2                | v3.0                     | 직접 변환                          | 3               | Template 부재, 단순 구조      |
| E3                | v1.1.4 이상              | v1.1.5→v4.0→v5.1→Cloud (다단계)    | 10+             | Base64 이미지 처리 필요       |
| EzOrtho           | v1.0                     | 직접 변환                          | 15+             | Chart 구조, ToothCode 매핑    |
| CleverOne         | v5.1.0                   | 직접 변환                          | 8+              | E3 RC Report와 유사           |

### 10.2 Element 타입별 지원 현황

| Element Type      | E2  | E3  | EzOrtho | CleverOne | 변환 난이도 |
| ----------------- | --- | --- | ------- | --------- | ----------- |
| label             | X   | X   | O       | X         | 낮음        |
| textBox           | O   | O   | O       | O         | 중간        |
| imageBox          | O   | O   | O       | O         | 중간        |
| toothBox          | X   | X   | O       | O         | 중간        |
| treatmentCategory | X   | X   | O (P2)  | X         | 낮음        |
| annotation        | X   | O   | O       | O         | 높음        |
| block             | X   | X   | O       | X         | 중간        |
| group             | X   | X   | X       | O         | 낮음        |
| image             | X   | X   | O       | X         | 낮음        |
| checkBox          | X   | X   | O       | X         | 낮음        |
| radioButton       | X   | X   | O       | X         | 낮음        |
| comboBox          | X   | X   | O       | X         | 낮음        |

### 10.3 좌표 변환 정확도

| 제품              | 입력 정밀도 | 출력 정밀도 | 예상 오차     | 검증 결과   |
| ----------------- | ----------- | ----------- | ------------- | ----------- |
| E2 v3.0           | 3자리       | 3자리       | ±0.1mm        | 검증 필요   |
| E3 Report v4/v5   | 3자리       | 3자리       | ±0.1mm        | 검증 필요   |
| E3 RC Report v5.1 | 1자리       | 3자리       | ±0.05mm       | 검증 필요   |
| EzOrtho v1.0      | 가변        | 3자리       | ±0.05mm       | 검증 필요   |
| CleverOne v5.1.0  | 1자리       | 3자리       | ±0.05mm       | 검증 필요   |

**검증 방법**:
- 샘플 파일 변환 후 좌표 측정
- 원본 PDF vs 변환 PDF 시각적 비교
- Element 간 거리 측정 및 비교

---

## 11. 사용자 가이드

### 11.1 Migration 실행 절차

**1. 사전 준비**:
```bash
# Migration 도구 설치
npm install -g scp-migration-tool

# 작업 디렉토리 생성
mkdir migration-workspace
cd migration-workspace
```

**2. 파일 준비**:
```bash
# 원본 파일 복사
cp /path/to/original/reports/*.xml ./input/

# 백업 생성
cp -r ./input ./backup
```

**3. Migration 실행**:
```bash
# 단일 파일 변환
scp-migrate --input ./input/report.xml --output ./output/report.json

# 다중 파일 일괄 변환
scp-migrate --input-dir ./input --output-dir ./output --parallel 4

# 검증 포함 변환
scp-migrate --input-dir ./input --output-dir ./output --validate --visual-check
```

**4. 결과 확인**:
```bash
# 변환 로그 확인
cat migration.log

# 오류 보고서 확인
cat migration-errors.log

# 통계 확인
scp-migrate --report
```

### 11.2 제품별 주의사항

**E2 v3.0**:
- 용지 정보가 없는 경우 기본값(A4 Portrait) 사용
- 사용자 지정 용지 크기는 수동 입력 필요

**E3 v1.x**:
- v1.0.5 이하는 Migration 불가, 업그레이드 필요
- Base64 이미지 추출 시 디스크 공간 확인 (파일당 수 MB)
- 다단계 변환으로 시간 소요 (파일당 1-2분)

**EzOrtho v1.0**:
- Chart 데이터 구조 확인 필요
- ToothCode 매핑 테이블 커스터마이징 가능
- Block 구조는 Containment로 유지 권장

**CleverOne v5.1.0**:
- Annotation Points 정밀도 손실 허용 (4자리→3자리)
- Groups 구조는 Reference로 유지

### 11.3 예외 상황 대응

**손상된 파일**:
```bash
# 복구 시도
scp-migrate --input damaged.xml --output recovered.json --recover

# 부분 변환 허용
scp-migrate --input damaged.xml --output partial.json --allow-partial
```

**변환 실패**:
```bash
# 상세 로그 활성화
scp-migrate --input report.xml --output report.json --verbose --debug

# Manual Override 적용
scp-migrate --input report.xml --output report.json --override overrides.json
```

**Manual Override 파일 예시**:
```json
{
  "fileId": "report-001",
  "overrides": [
    {
      "elementId": "element-123",
      "overrideType": "coordinate",
      "originalValue": {"x": 100, "y": 50},
      "correctedValue": {"x": 105, "y": 52},
      "reason": "Coordinate conversion error"
    }
  ]
}
```

---

## 12. 테스트 계획

### 12.1 테스트 범위

**단위 테스트**:
- 좌표 변환 함수 (비율값→mm, 정밀도 확장)
- Element 변환 함수 (제품별)
- 검증 함수 (구조, 데이터, 시각적)

**통합 테스트**:
- 전체 Migration 파이프라인
- 제품별 변환 경로
- 예외 처리 시나리오

**성능 테스트**:
- 대용량 파일 처리 (100+ pages)
- 다중 파일 병렬 처리
- 메모리 사용량 측정

**검증 테스트**:
- 샘플 파일 변환 후 시각적 비교
- 좌표 정확도 측정
- 데이터 무결성 확인

### 12.2 테스트 케이스

**좌표 변환 테스트**:
```typescript
describe('Coordinate Conversion', () => {
  it('should convert ratio to mm correctly', () => {
    const result = ratioToMm(0.5, 'A4', 'Portrait', { all: 10 })
    expect(result).toBeCloseTo(105.0, 3)
  })

  it('should handle landscape orientation', () => {
    const result = ratioToMm(0.5, 'A4', 'Landscape', { all: 10 })
    expect(result).toBeCloseTo(148.5, 3)
  })

  it('should expand precision correctly', () => {
    const result = expandPrecision(105.5, 1)
    expect(result).toBe(105.500)
  })
})
```

**Element 변환 테스트**:
```typescript
describe('Element Transformation', () => {
  it('should transform E2 ImageBox correctly', () => {
    const e2Element = {
      type: 'ImageBox',
      left: 0.5,
      top: 0.3,
      width: 0.2,
      height: 0.15
    }

    const cloudElement = transformE2Element(e2Element, paperConfig)

    expect(cloudElement.type).toBe('imageBox')
    expect(cloudElement.position.x).toBeCloseTo(105.0, 1)
    expect(cloudElement.position.y).toBeCloseTo(94.1, 1)
  })

  it('should transform EzOrtho Block correctly', () => {
    const ezOrthoBlock = {
      type: 'Block',
      name: 'Face',
      left: 20,
      top: 50,
      children: [
        { type: 'Image', left: 0, top: 0, width: 80, height: 100 }
      ]
    }

    const cloudBlock = transformEzOrthoElement(ezOrthoBlock)

    expect(cloudBlock.type).toBe('block')
    expect(cloudBlock.name).toBe('Face')
    expect(cloudBlock.children).toHaveLength(1)
    expect(cloudBlock.children[0].position.x).toBe(0)
  })
})
```

**검증 테스트**:
```typescript
describe('Validation', () => {
  it('should validate schema correctly', () => {
    const document = createValidCloudDocument()
    const result = validator.validateSchema(document)
    expect(result.isValid).toBe(true)
  })

  it('should detect coordinate errors', () => {
    const original = createOriginalDocument()
    const converted = createConvertedDocumentWithError()
    const result = validator.validateCoordinates(original, converted)
    expect(result.errors.length).toBeGreaterThan(0)
  })

  it('should detect reference integrity errors', () => {
    const document = createDocumentWithBrokenReference()
    const result = validator.validateReferences(document)
    expect(result.errors).toContainEqual(
      expect.objectContaining({ message: expect.stringContaining('not found') })
    )
  })
})
```

### 12.3 샘플 파일 목록

**E2 v3.0** (확보 필요):
- 단순 리포트 (ImageBox + TextBox 2-3개)
- 중간 복잡도 (5-10개 Element)
- 복잡한 리포트 (20+ Element, 다중 페이지)

**E3**:
- v1.1.4 샘플 (Base64 이미지 포함)
- v4.0 샘플 (Template 포함)
- v5.1 RC Report 샘플 (Annotation 포함)

**EzOrtho v1.0**:
- Treatment Chart 샘플
- History Chart 샘플
- Block 구조 포함 샘플

**CleverOne v5.1.0**:
- 기본 리포트 샘플
- Groups 기능 포함 샘플
- Multi ImageBox 포함 샘플

---

## 13. 결론 및 다음 단계

### 13.1 주요 성과

1. **완전한 Migration 경로 설계**: 4개 제품, 다양한 버전 → Cloud 포맷 변환 경로 확립
2. **정밀한 좌표 변환 시스템**: 비율값/픽셀/mm 혼재 → mm 통일, ±0.1mm 정확도 목표
3. **자동화된 검증 시스템**: 구조/데이터/시각적 검증으로 무손실 변환 보장
4. **예외 처리 메커니즘**: 손상된 파일, 비표준 구조 대응 방안 수립
5. **확장 가능한 아키텍처**: 신규 제품/버전 추가 용이한 플러그인 구조

### 13.2 제한사항 및 리스크

**기술적 제한**:
- E3 v1.0.5 이하 Migration 미지원 (기존 정책)
- 용지 정보 누락 시 기본값 사용 또는 사용자 입력 필요
- CleverOne Annotation Points 정밀도 손실 (4자리→3자리)

**검증 필요 사항**:
- E2 v3.0 용지 정보 포함 여부 확인 (실제 파일 분석 필요)
- EzOrtho 좌표 정밀도 확인 (실제 파일 분석 완료, mm 단위 확인)
- 좌표 변환 정확도 실측 (샘플 파일 변환 후 검증)

**운영 리스크**:
- 대용량 파일 처리 시 메모리 부족 가능성
- 다단계 변환(E3 v1.x) 시간 소요
- 예외 상황 발생 시 수동 개입 필요

### 13.3 다음 단계

**즉시 실행**:
1. **샘플 파일 확보**: 각 제품별 다양한 버전의 실제 파일 수집
2. **좌표 변환 검증**: 샘플 파일 변환 후 정확도 실측
3. **E2 용지 정보 확인**: E2 v3.0 파일 구조 분석

**단기 (1-2주)**:
4. **Migration 엔진 구현**: 핵심 변환 로직 개발
5. **검증 도구 개발**: 자동 검증 시스템 구축
6. **단위 테스트 작성**: 주요 함수 테스트 커버리지 80% 이상

**중기 (3-4주)**:
7. **통합 테스트**: 전체 파이프라인 검증
8. **성능 최적화**: 병렬 처리, 캐싱 적용
9. **사용자 가이드 작성**: 상세 매뉴얼 및 예제

**PoC-14 연계**:
10. **렌더링 엔진 통합**: Migration 결과를 PoC-14 Element 렌더링 엔진으로 렌더링
11. **시각적 검증 자동화**: 원본 vs 변환 결과 자동 비교 시스템
12. **End-to-End 테스트**: 기존 파일 → Migration → 웹 렌더링 전체 흐름 검증

### 13.4 기대 효과

**기술적 효과**:
- 기존 리포트 자산의 완전한 보존 및 Cloud 전환
- 데이터 무결성 보장으로 의료 데이터 법적 요구사항 준수
- 자동화된 변환으로 수동 작업 최소화

**비즈니스 효과**:
- 기존 고객의 Cloud 전환 장벽 제거
- 수년간 축적된 리포트 자산 가치 보존
- 타 제품 대비 뛰어난 호환성으로 시장 경쟁력 확보

---

## 부록 A. Migration API 명세

### A.1 REST API

**파일 업로드 및 변환**:
```http
POST /api/migration/convert
Content-Type: multipart/form-data

file: [binary]
product: "E3"
version: "v5.1"
options: {
  "validate": true,
  "visualCheck": false,
  "allowPartial": false
}

Response:
{
  "success": true,
  "output": {...},
  "metadata": {
    "sourceProduct": "E3",
    "sourceVersion": "v5.1",
    "conversionTime": 1234567890,
    "warnings": []
  }
}
```

**일괄 변환**:
```http
POST /api/migration/batch
Content-Type: application/json

{
  "files": ["file-id-1", "file-id-2", ...],
  "options": {...}
}

Response:
{
  "jobId": "batch-job-123",
  "totalFiles": 10,
  "status": "processing"
}
```

**진행 상황 조회**:
```http
GET /api/migration/batch/{jobId}/progress

Response:
{
  "jobId": "batch-job-123",
  "totalFiles": 10,
  "processedFiles": 5,
  "currentFile": "report-006.xml",
  "currentStage": "validation",
  "estimatedTimeRemaining": 300000
}
```

### A.2 CLI 명령어

```bash
# 단일 파일 변환
scp-migrate convert --input report.xml --output report.json

# 일괄 변환
scp-migrate batch --input-dir ./input --output-dir ./output

# 검증 포함
scp-migrate convert --input report.xml --output report.json --validate

# 시각적 검증
scp-migrate convert --input report.xml --output report.json --visual-check

# 진행 상황 표시
scp-migrate batch --input-dir ./input --output-dir ./output --progress

# 통계 보고서
scp-migrate report --input-dir ./output
```

---

## 부록 B. 좌표 변환 공식 상세

### B.1 비율값 → mm 변환 (E2, E3 Report)

**가로 좌표 (X축)**:
```
X_mm = (X_ratio × (PaperWidth - MarginLeft - MarginRight)) + MarginLeft
```

**세로 좌표 (Y축)**:
```
Y_mm = (Y_ratio × (PaperHeight - MarginTop - MarginBottom)) + MarginTop
```

**예시 (A4 Portrait, Margin 10mm)**:
```
PaperWidth = 210mm
PaperHeight = 297mm
MarginLeft = MarginRight = MarginTop = MarginBottom = 10mm

X_ratio = 0.500
X_mm = (0.500 × (210 - 10 - 10)) + 10
     = (0.500 × 190) + 10
     = 95 + 10
     = 105.000mm

Y_ratio = 0.300
Y_mm = (0.300 × (297 - 10 - 10)) + 10
     = (0.300 × 277) + 10
     = 83.1 + 10
     = 93.100mm
```

### B.2 Landscape 처리

**Orientation이 Landscape인 경우 Width와 Height 교환**:
```typescript
if (orientation === 'Landscape') {
  [paperWidth, paperHeight] = [paperHeight, paperWidth]
}
```

**예시 (A4 Landscape)**:
```
PaperWidth = 297mm (원래 Height)
PaperHeight = 210mm (원래 Width)

X_ratio = 0.500
X_mm = (0.500 × (297 - 10 - 10)) + 10
     = (0.500 × 277) + 10
     = 138.5 + 10
     = 148.500mm
```

### B.3 정밀도 반올림

**소수점 3자리 반올림**:
```typescript
function roundTo3Decimals(value: number): number {
  return Math.round(value * 1000) / 1000
}

// 예시
roundTo3Decimals(105.4567) // → 105.457
roundTo3Decimals(105.4564) // → 105.456
```

---

## 부록 C. 참고 문서

1. **PoC-06 통합 Element 스키마 설계**: Migration 목표 포맷
2. **PoC-02 좌표 단위 표준화**: mm 단위, 소수점 3자리 정밀도
3. **PoC-03 폰트 단위 표준화**: pt 단위, DPI 전략
4. **E3 v5.1 RC Report FileFormat**: E3 RC Report 파일 구조
5. **CleverOne Report Format**: CleverOne 파일 구조
6. **EzOrtho v1.0 SRS**: EzOrtho 파일 구조 및 Chart 정의
7. **E2 Report Format**: E2 파일 구조 (확보 필요)
8. **VTE3Migration 도구 문서**: 기존 E3 Migration 로직

---

**문서 버전**: 1.0
**작성일**: 2026년 1월 23일
**작성자**: Raymond
**검토자**: (검토 필요)
**승인자**: (승인 필요)
