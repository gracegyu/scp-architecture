Engineering One Pager

**Project Name**: PoC-12: 접근성 (Accessibility) 준수

**Date**: 2026년 1월 6일

**Submitter Info**: Raymond

**Project Description**: SCP Cloud Report 시스템이 웹 접근성 표준(WCAG 2.1 AA)을 준수하기 위한 요구사항을 분석하고 정리합니다. 의료 소프트웨어의 특수성을 고려하여 스크린 리더 지원, 키보드 네비게이션, 고대비 모드 등 접근성 구현 설계를 수립하고, 기본 프로토타입으로 구현 가능성을 검증합니다. 완전한 구현은 본 개발(product) 단계에서 수행합니다.

**Business and Marketing Justification**:

- **법적 요구사항**: ADA(미국), DDA(호주), EN 301 549(EU) 등 접근성 법규 준수
- **시장 확대**: 장애인 의료진 및 고령 사용자층 포함한 사용자 기반 확대
- **사회적 가치**: 의료 접근성 향상으로 기업의 사회적 책임 이행
- **품질 향상**: 접근성 고려 설계로 전체 사용자 경험 개선
- **리스크 관리**: 접근성 관련 법적 분쟁 예방
- **경쟁 우위**: 접근성 우수 제품으로 공공 조달 입찰 시 가점

**Risk Assessment**:

- **높은 리스크**:
  - 복잡한 리포트 편집 기능의 접근성 구현 기술적 어려움
  - Canvas 기반 렌더링 시 스크린 리더 지원 복잡성
- **중간 리스크**:
  - 접근성 기능 구현으로 인한 성능 저하
  - 시각적 디자인과 접근성 요구사항 간 상충
  - 의료 이미지의 대체 텍스트 작성 복잡성
- **저위험**:
  - 웹 접근성 표준은 명확하고 검증된 가이드라인 존재
- **완화 방안**:
  - PoC 단계에서 요구사항 정리 및 설계에 집중
  - 기본 프로토타입으로 핵심 기능만 검증
  - 본 개발 단계에서 점진적 접근성 개선 (AA 등급부터 시작)
  - 본 개발 단계에서 사용자 피드백 기반 지속적 개선 및 접근성 전문가 협력

**Resource and Scheduling Details**:

- **기간**: 2주 (Week 16-17, PoC-11, PoC-12와 병렬 진행)
- **인력**:
  - Raymond (접근성 설계자, UX 전문가, 테스트 엔지니어 역할 겸임)
    - WCAG 2.1 AA 요구사항 분석 및 정리
    - 접근성 구현 설계 및 가이드라인 작성
    - 키보드 네비게이션 시스템 설계
    - 기본 프로토타입으로 핵심 기능 검증
    - 자동 접근성 테스트 도구 활용
- **PoC 범위**:
  - 완전한 구현은 본 개발(product) 단계에서 수행
  - PoC 단계에서는 요구사항 정리, 설계, 기본 검증에 집중

**Technical Description**:

**WCAG 2.1 AA 준수 요구사항**:

**1. 인식 가능성 (Perceivable)**:

- **대체 텍스트**: 모든 이미지에 의미 있는 alt 텍스트
- **색상 독립성**: 색상에만 의존하지 않는 정보 전달
- **명도 대비**: 텍스트와 배경 최소 4.5:1 대비
- **확대 가능**: 200% 확대 시에도 모든 기능 사용 가능

**2. 운용 가능성 (Operable)**:

- **키보드 접근**: 모든 기능이 키보드만으로 사용 가능
- **포커스 관리**: 논리적 탭 순서 및 시각적 포커스 표시
- **시간 제한**: 자동 로그아웃 등 시간 제한 조정 가능
- **발작 방지**: 번쩍임 효과 제거

**3. 이해 가능성 (Understandable)**:

- **언어 명시**: HTML lang 속성 정확한 설정
- **일관성**: 동일한 기능은 같은 방식으로 작동
- **오류 식별**: 입력 오류 시 명확한 메시지 제공
- **도움말**: 복잡한 기능에 대한 설명 제공

**4. 견고성 (Robust)**:

- **마크업 유효성**: 유효한 HTML/ARIA 구조
- **보조 기술 호환**: 스크린 리더, 음성 인식 소프트웨어 지원

**의료 소프트웨어 특화 접근성**:

**1. 의료 이미지 접근성**:

- **이미지 설명**: 방사선 이미지의 의학적 소견 텍스트 제공
- **측정 정보**: 거리, 면적 측정값의 음성 안내
- **구조화된 정보**: 해부학적 구조의 계층적 설명

```typescript
interface MedicalImageA11y {
  altText: string // 기본 대체 텍스트
  longDescription: string // 상세 의학적 설명
  measurements: Measurement[] // 측정값 정보
  findings: string[] // 주요 소견
}
```

**2. 리포트 편집 접근성**:

- **Element 선택**: 키보드 화살표로 Element 탐색
- **속성 편집**: 스크린 리더 친화적 폼 컨트롤
- **드래그 앤 드롭**: 키보드 대안 인터랙션 제공

**3. Annotation 접근성**:

```typescript
interface AnnotationA11y {
  type: AnnotationType
  description: string // 도형 설명
  coordinates: string // 좌표 정보 음성 안내
  measurement?: string // 측정값 (있는 경우)
}
```

**스크린 리더 지원**:

**ARIA (Accessible Rich Internet Applications) 구현**:

```typescript
// 리포트 편집기 ARIA 구조
<div role='application' aria-label='Medical Report Editor'>
  <div role='toolbar' aria-label='Editing Tools'>
    <button aria-pressed='false' aria-describedby='tool-help'>
      Rectangle Tool
    </button>
  </div>

  <div role='main' aria-label='Report Canvas'>
    <div role='group' aria-label='Page 1 of 5'>
      <div role='img' aria-describedby='img-desc'>
        <div id='img-desc' class='sr-only'>
          CT scan showing normal dental structures
        </div>
      </div>
    </div>
  </div>
</div>
```

**키보드 네비게이션 시스템**:

**단축키 체계**:

- **Tab**: Element 간 이동
- **Arrow Keys**: Element 내부 탐색, 미세 조정
- **Enter/Space**: Element 활성화/편집
- **Esc**: 편집 모드 종료
- **Ctrl+Z/Y**: Undo/Redo
- **Delete**: Element 삭제

**포커스 관리**:

- 논리적 탭 순서 (Top-to-Bottom, Left-to-Right)
- 포커스 트랩 (모달 다이얼로그)
- 시각적 포커스 인디케이터 (2px outline)

**고대비 모드 지원**:

**시스템 설정 감지**:

```css
@media (prefers-contrast: high) {
  .report-element {
    border: 2px solid black;
    background: white;
    color: black;
  }
}

@media (prefers-color-scheme: dark) {
  /* 다크 모드 최적화 */
}
```

**커스텀 테마**:

- 사용자 정의 색상 조합
- 텍스트 크기 조정 (120%, 150%, 200%)
- 애니메이션 감소 옵션

**접근성 검증 계획 (PoC 단계)**:

**1. 자동 테스트** (PoC 단계에서 수행):

- **axe-core**: 자동 접근성 위반 감지
- **Pa11y**: 페이지별 접근성 스캔
- **Lighthouse**: 접근성 점수 측정
- 기본 프로토타입에 대한 자동 검증

**2. 기본 수동 검증** (PoC 단계에서 수행):

- **스크린 리더**: 기본 기능에 대한 NVDA/VoiceOver 테스트 (핵심 기능만)
- **키보드 전용**: 마우스 없이 핵심 기능 사용 가능 여부 확인
- **고대비 모드**: 기본 CSS 미디어 쿼리 적용 확인

**3. 사용자 테스트** (본 개발 단계에서 수행):

- 시각 장애인 의료진 실제 사용 테스트
- 운동 장애인 키보드 사용 테스트
- 고령 사용자 사용성 평가
- 접근성 검증 전문기관 표준 준수 확인

**의료 특화 접근성 고려사항**:

**1. 의료 이미지 설명**:

- 표준화된 의료 영상 설명 체계 구축
- AI 기반 자동 이미지 분석 및 설명 생성 (향후)
- 의료진 검토 및 승인 워크플로우

**2. 측정 도구 접근성**:

- 거리/면적 측정 시 음성 피드백
- 키보드로 측정점 정확히 지정하는 방법
- 측정 결과의 구조화된 데이터 제공

**성능 영향 분석**:

- 접근성 기능으로 인한 추가 DOM 노드: < 10% 증가
- ARIA 속성 처리 오버헤드: < 5% 성능 저하
- 고대비 모드 CSS 로딩: < 50ms 추가 시간

**산출물 (PoC 단계)**:

1. **WCAG 2.1 AA 요구사항 분석서**: SCP Cloud Report에 적용할 접근성 요구사항 정리
2. **접근성 구현 설계 문서**: ARIA 구조, 키보드 네비게이션 설계
3. **접근성 구현 가이드라인**: 본 개발 단계에서 참고할 구현 가이드
4. **기본 프로토타입**: 핵심 기능의 접근성 검증용 프로토타입
5. **자동 테스트 결과**: axe-core, Lighthouse 등 자동 검증 결과
6. **구현 우선순위**: 본 개발 단계에서 구현할 접근성 기능의 우선순위

**본 개발 단계 산출물** (참고):

- 완전한 ARIA 컴포넌트 라이브러리
- 완전한 키보드 네비게이션 시스템 구현
- 사용자 테스트 결과 및 개선 사항
- 접근성 준수 인증서

**PoC 목표**: WCAG 2.1 AA 준수를 위한 요구사항 정리 및 구현 가능성 검증

**본 개발 단계 목표**: 모든 사용자가 동등하게 의료 리포트 편집 기능을 활용할 수 있는 포괄적 웹 애플리케이션 구현
