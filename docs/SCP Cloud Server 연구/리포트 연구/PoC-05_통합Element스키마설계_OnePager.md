Engineering One Pager

**Project Name**: PoC-05: 통합 Element 스키마 설계

**Date**: 2026년 1월 6일

**Submitter Info**: Raymond

**Project Description**: 기존 4개 Desktop 제품(E2, E3, EzOrtho, CleverOne)의 서로 다른 리포트 Element 구조를 분석하여 모든 기능을 포괄하면서도 확장 가능한 통합 스키마를 설계합니다. 제품별 고유 기능을 유지하면서 공통 속성을 정규화하고, 향후 신규 기능 추가가 용이한 유연한 구조를 만듭니다.

**Business and Marketing Justification**:

- **완전한 기능 이전**: 기존 모든 제품 사용자가 기능 손실 없이 Cloud로 전환
- **개발 효율성**: 통일된 스키마로 개발 복잡도 감소 및 재사용성 향상
- **유지보수성**: 일관된 데이터 구조로 버그 수정 및 기능 추가 용이
- **확장성**: 미래 요구사항(AI 분석, VR 연동 등)에 대응 가능한 구조
- **데이터 품질**: 정규화된 스키마로 데이터 일관성 및 검증 강화
- **API 설계**: RESTful API 설계 시 명확한 데이터 모델 제공

**Risk Assessment**:

- **높은 리스크**:
  - 제품별 고유 기능의 일반화 과정에서 기능 손실 가능성
  - 과도한 일반화로 인한 성능 저하 또는 복잡성 증가
- **중간 리스크**:
  - EzOrtho의 특수한 Chart 구조 통합 복잡성
  - 기존 데이터 Migration 시 스키마 변경에 따른 호환성 문제
  - 향후 신규 제품 요구사항 예측 어려움
- **저위험**:
  - JSON Schema를 통한 검증 가능한 구조화된 설계
- **완화 방안**:
  - 단계적 통합 (공통 부분부터 시작)
  - 제품별 전용 속성 네임스페이스 분리
  - 확장 가능한 plugin 구조 도입

**Resource and Scheduling Details**:

- **기간**: 3주 (Week 6-8)
- **인력**:
  - Raymond (소프트웨어 아키텍트, 도메인 전문가, 데이터 모델링 전문가 역할 겸임)
    - 스키마 설계 리드
    - 제품별 요구사항 분석 (E2, E3, EzOrtho, CleverOne)
    - 데이터 정규화 및 최적화
- **환경**:
  - 모든 제품의 실제 파일 샘플 (각 제품별 100개 이상)
  - JSON Schema 검증 도구
  - TypeScript 컴파일러 및 타입 체커

**Technical Description**:

**기존 제품별 Element 분석**:

**E2 Report (v3.0)**:

- ImageBox: 기본 속성 (Position, Size, ImageFitMode)
- TextBox: Font, TextAlignment, TextData, TextMacro
- Paper: PaperSize, Orientation, Margin

**E3 Report (v4.0~v5.1)**:

- ItemBox: BoxType(Text/Image), Editable, Background, BorderLine
- Image 확장: Layout(Row/Column), Translation, Scale, ShowRuler, Invert
- Auto Fill: TabType, ViewType, GroupType, WithOverlay, ApplyFilter
- Annotation: 6가지 타입 + 다양한 Style 속성

**EzOrtho (v1.0)**:

- 특수 Chart: TreatmentChart, HistoryChart, AnalysisChart (Analysis Chart는 현재 구현 범위 외, 추후 확장 대상)
- ToothCode: 치아 번호 체계 연동
- ItemType: Chart 전용 Element 타입
- LineStyle: 의료 차트 전용 선 스타일

**RC Report (v5.1)** (현재 구현 범위 외, 추후 확장 대상):

- CapturedImgInfo: SpacingX/Y, Thickness, Interval
- Reference Image: LinkedMultiBoxID, ImageType
- Template 시스템: 동적 Layout 지원
- Annotation: 6가지 타입 (Rectangle, Ellipse, Line, Arrow, FreeDraw, Memo)

**전체 통합 Element 목록** (PoC-13 구현 대상과 동일):

**기본 Shape Elements (E3 기준)**:

- **Rectangle**: 직사각형 Annotation, 8개 핸들러 ✅ (ezorthoweb 구현됨)
- **Ellipse**: 타원형 Annotation, 8개 핸들러 ✅ (ezorthoweb 구현됨)
- **Line**: 직선 Annotation, 2개 핸들러 ✅ (ezorthoweb 구현됨)
- **Arrow**: Line + 화살표 머리, 2개 핸들러 ❌ (추가 구현 필요)
- **FreeDraw**: 자유 그리기, Path 기반 ✅ (ezorthoweb 구현됨)
- **Memo**: 풍선 텍스트 + 포인터 ❌ (추가 구현 필요)

**Content Elements (E2/E3 기준)**:

- **ImageBox**: ✅ (ezorthoweb 구현됨, Single 타입만)
  - Single ImageBox: 단일 이미지 ✅
  - Multi ImageBox: 1~20 Row/Column 레이아웃 ❌ (추가 구현 필요)
  - Reference ImageBox: 다른 ImageBox 참조 ❌ (추가 구현 필요)
- **TextBox**: HTML 텍스트 편집 ✅ (ezorthoweb 구현됨)
- **Label**: 단순 텍스트 ✅ (ezorthoweb 구현됨)

**EzOrtho 특화 Elements**:

- **ToothBox**: 치아 선택 UI ✅ (ezorthoweb 구현됨)
- **TreatmentCategory**: 치료 분류 선택 ✅ (ezorthoweb 구현됨)
- **Form Controls**: ✅ (ezorthoweb 구현됨)
  - RadioButton, CheckBox, Button, ComboBox, TextInput, TextArea
- **Block**: 요소 그룹핑 컨테이너 ✅ (ezorthoweb 구현됨)
- **Image**: 단순 이미지 표시 ✅ (ezorthoweb 구현됨)

**현재 구현 범위 외 Element** (추후 확장 대상):

- **Canvas**: EzOrtho 분석 차트 전용 (별도 프로젝트, 추후 확장)

**구현 현황 요약**:

- **구현 완료**: 18개 Element (ezorthoweb에서 검증됨)
- **추가 구현 필요**: 4개 Element (Arrow, Memo, Multi ImageBox, Reference ImageBox)
- **현재 구현 범위 외**: 1개 Element (Canvas - EzOrtho 분석 차트 전용, 추후 확장 대상)

**통합 스키마 설계 원칙**:

**1. 계층적 구조**:

```json
{
  "document": {
    "metadata": { "version", "product", "created" },
    "paper": { "size", "orientation", "margin" },
    "pages": [
      {
        "elements": [
          {
            "type": "imageBox|textBox|annotation",
            "common": { "id", "position", "size", "style" },
            "specific": { /* 타입별 고유 속성 */ }
          }
        ]
      }
    ]
  }
}
```

**2. 통합 Element 타입 정의**:

**기본 Shape Elements (E3 기준)**:

- **Rectangle**: 직사각형 Annotation, 8개 핸들러
- **Ellipse**: 타원형 Annotation, 8개 핸들러
- **Line**: 직선 Annotation, 2개 핸들러 (시작점, 끝점)
- **Arrow**: Line + 화살표 머리, 2개 핸들러 (ezorthoweb 미구현 - 추가 필요)
- **FreeDraw**: 자유 그리기, Path 기반
- **Memo**: 풍선 텍스트 + 포인터, 복합 핸들러 (ezorthoweb 미구현 - 추가 필요)

**Content Elements (E2/E3 기준)**:

- **ImageBox**: 이미지 표시 + 크기 조정, 8개 핸들러
  - Single ImageBox: 단일 이미지 (기본)
  - Multi ImageBox: 1~20 Row/Column 레이아웃 (추가 구현 필요)
  - Reference ImageBox: 다른 ImageBox 참조 (추가 구현 필요)
- **TextBox**: HTML 텍스트 편집, 8개 핸들러
- **Label**: 단순 텍스트, 8개 핸들러

**EzOrtho 특화 Elements (일반 리포트용)**:

- **ToothBox**: 치아 선택 UI, 8개 핸들러
- **TreatmentCategory**: 치료 분류 선택, 8개 핸들러
- **Form Controls**: RadioButton, CheckBox, Button, ComboBox, TextInput, TextArea
- **Block**: 요소 그룹핑 컨테이너
- **Image**: 단순 이미지 표시

**현재 구현 범위 외 Element** (추후 확장 대상):

- **Canvas**: EzOrtho 분석 차트 전용 (별도 프로젝트, 추후 확장)

**3. 확장성 고려**:

- **Plugin 시스템**: 제품별 특수 기능 플러그인으로 확장
- **Custom Properties**: 자유로운 속성 추가 지원
- **Version 관리**: 스키마 버전별 Migration 경로

**호환성 매트릭스 작성**:

```typescript
interface CompatibilityMatrix {
  element: ElementType
  e2: CompatibilityLevel // full | partial | none
  e3: CompatibilityLevel
  ezortho: CompatibilityLevel
  cleverone: CompatibilityLevel
  migrationPath?: string
  limitations?: string[]
}
```

**스키마 검증 시나리오**:

1. **완전성 검증**:
   - 각 제품의 모든 기능이 새 스키마로 표현 가능한지
   - 기존 파일의 100% 정보 보존 가능성
2. **확장성 검증**:
   - 새로운 Element 타입 추가 시뮬레이션
   - 기존 스키마 호환성 유지하며 확장 가능성
3. **성능 검증**:
   - 복잡한 리포트의 스키마 검증 시간
   - TypeScript 컴파일 시간 영향

**특수 요구사항 처리**:

**EzOrtho Chart 시스템**:

- ToothCode 매핑 테이블
- 시간 축 기반 Treatment 기록
- 3D 모델 연동 정보

**E3 Auto Fill 시스템**:

- Source Tab/View 정보 구조화
- 실시간 Image Capture 메타데이터
- Multi Image Reference 관계

**Migration 호환성**:

- 버전별 스키마 변경 이력 관리
- 자동 Migration 규칙 정의
- 손실 데이터 복구 메커니즘

**검증 방법**:

1. **실제 데이터 테스트**: 각 제품별 100개 실제 파일로 변환 테스트
2. **Round-trip 테스트**: 기존→새스키마→기존 변환 후 동일성 확인
3. **ezorthoweb 호환성 테스트**: 기존 Vue.js 생성 파일의 스키마 호환성 확인
4. **성능 테스트**: 스키마 처리 성능
5. **확장성 테스트**: 가상의 새 기능 추가 시뮬레이션
6. **PoC-13 연계 테스트**: 설계된 스키마가 React Element 렌더링 엔진과 호환되는지 확인

**산출물**:

1. **통합 JSON Schema**: 전체 Element 구조 정의
2. **TypeScript 타입 정의**: 개발용 타입 시스템
3. **호환성 매트릭스**: 제품별 지원 범위 명세서
4. **Migration 매핑 테이블**: 기존→신규 스키마 변환 규칙
5. **확장 가이드라인**: 향후 Element 추가 시 준수 사항
6. **검증 도구**: 스키마 유효성 검사 라이브러리

**다음 단계**: 설계된 통합 스키마를 기반으로 PoC-06(Migration 시스템) 및 PoC-13(Element 렌더링 엔진) 병행 구현, DragResizeDiv Handler 시스템과 스키마 호환성 보장
