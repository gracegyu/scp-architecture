Engineering One Pager

**Project Name**: PoC-06: Migration 시스템 설계

**Date**: 2026년 1월 6일

**Submitter Info**: Raymond

**Project Description**: 기존 4개 Desktop 제품의 다양한 버전에서 생성된 리포트 파일들을 SCP Cloud 포맷으로 완벽하게 변환하는 Migration 시스템을 설계하고 검증합니다. 데이터 손실 없는 변환을 보장하며, 복잡한 버전별 호환성 문제를 해결하는 자동화된 Migration 프로세스를 구축합니다.

**Business and Marketing Justification**:

- **기존 고객 유지**: 수년간 축적된 리포트 자산의 완전한 보존으로 고객 이탈 방지
- **Cloud 전환 가속화**: 매끄러운 Migration으로 Desktop→Cloud 전환 장벽 제거
- **데이터 자산 가치**: 기존 의료 데이터의 지속적 활용으로 투자 보호
- **사용자 신뢰**: 완벽한 데이터 보존으로 Cloud 서비스 신뢰도 확보
- **시장 경쟁력**: 타 제품 대비 뛰어난 호환성으로 차별화
- **법적 요구사항**: 의료 데이터 보존 의무 준수

**Risk Assessment**:

- **높은 리스크**:
  - 복잡한 버전별 호환성으로 인한 일부 데이터 손실 가능성
  - E3 v1.x→v4.x→v5.1→Cloud 다단계 Migration 복잡성
  - EzOrtho 차트 데이터의 특수성으로 인한 변환 오류
  - 제품별 좌표 단위 차이로 인한 변환 오차 (비율값, 픽셀, mm 혼재)
  - 용지 크기 정보 누락 시 좌표 변환 정확도 저하
- **중간 리스크**:
  - Image Data 내장 파일 (E3 v1 Base64) 처리 복잡성
  - 손상된 파일 또는 비표준 구조 파일 처리 어려움
  - EzOrtho 좌표 정밀도 확인 필요 (실제 파일 구조 분석 필요)
  - 비율값 기반 파일의 용지 크기 변경 시 레이아웃 왜곡 가능성
- **저위험**:
  - 최신 버전(E3 v5.1) 파일은 명확한 변환 경로 존재
- **완화 방안**:
  - 단계별 Migration 검증으로 조기 문제 발견
  - 백업 및 롤백 메커니즘 구축
  - 예외 상황 처리를 위한 Manual Override 기능

**Resource and Scheduling Details**:

- **기간**: 3주 (Week 6-8)
- **인력**:
  - Raymond (Migration 개발자, 도메인 전문가, 데이터 분석가 역할 겸임)
    - 변환 엔진 및 검증 시스템 개발
    - 제품별 특수 로직 검토 (E2, E3, EzOrtho)
    - Migration 품질 분석
- **환경**:
  - 각 제품별 다양한 버전의 실제 파일 샘플 (최대한 많이, 가능한 범위 내에서)
    - 각 제품의 주요 버전별로 최소 3-5개씩, 가능하면 더 많이
    - 다양한 복잡도 (단순, 중간, 복잡) 포함
    - 예외 케이스 샘플 (손상된 파일, 비표준 구조) 포함
  - 데이터 무결성 검증 도구

**Technical Description**:

**기존 Migration 정책 분석**:

**E3 기존 Migration 경로**:

- v1.0.5 이하: Migration 미지원 (EEEN-1589)
- v1.1.4 → v1.1.5 → v4.0 → v5.1 (다단계)
- Image Data 처리: Base64 내장 → 파일 경로 참조

**E2 Migration 특징**:

- 상대적으로 단순한 구조
- Template 시스템 부재로 변환 복잡도 낮음

**EzOrtho Migration 도전과제**:

- 다중 Chart 구조 (UI에서 Treatment Chart, History Chart 등을 Tab 형태로 표시)
- 치아 번호 체계 (ToothCode) 매핑
- 시간축 기반 치료 이력 데이터

**Migration 시스템 아키텍처**:

**1. 파일 분석 엔진**:

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
}
```

**2. 단계별 변환 파이프라인**:

```
입력 파일 → 버전 감지 → 중간 포맷 변환 → 검증 → Cloud 포맷 → 출력
```

**3. 데이터 변환 엔진**:

- **좌표 단위 변환**: 제품별 좌표 단위 → mm (소수점 3자리)
  - E2/E3 Report (비율값) → mm: 용지 크기와 Margin 정보 필요
  - E3 RC Report v5.1 (mm 1자리) → mm 3자리: 정밀도 확장
  - EzOrtho (mm) → mm: 정밀도 확장 (실제 파일 구조 확인 결과 이미 mm 단위 사용)
- **이미지 처리**: Base64 → 파일 참조, 경로 정규화
- **속성 매핑**: 제품별 속성명 → 통합 속성명
- **구조 재편**: 중첩 XML → 평면적 JSON

**Migration 경로별 처리**:

**E2 v3.0 → Cloud**:

- 직접 변환 (가장 단순)
- Template 정보 없음 → Default Template 적용
- **좌표 변환**: 비율값 (3자리) → mm (3자리)
  - **용지 정보 포함 여부**: 확인 필요 (Template 시스템 부재로 추정, 파일에 용지 정보 미포함 가능성)
  - 용지 정보가 없는 경우: 기본값(A4 Portrait, Margin 10mm) 사용 또는 사용자 입력 요청
  - 용지 크기 정보 추출 (PaperSize, Orientation) - 파일에 포함된 경우
  - Margin 정보 추출 (Left, Right, Top, Bottom) - 파일에 포함된 경우
  - 비율값 × (용지크기 - Margin) + Margin → mm 변환

**E3 v1.x → Cloud**:

```
v1.x → v1.1.5 → v4.0 → v5.1 → Cloud
```

- 기존 VTE3Migration 도구 활용
- Base64 이미지 → 파일 추출 및 저장
- **좌표 변환**:
  - **E3 Report v4.0/v5.0**: 비율값 (3자리) → mm (3자리)
    - **용지 정보 포함**: 리포트 파일에 `<Paper>` 섹션 포함
      - `PaperSize`: String (예: "A4", "A3", "Letter", "8x10inch" 등)
      - `Orientation`: String ("Portrait" 또는 "Landscape")
      - `Margin`: Float (mm 단위, Left, Right, Top, Bottom, 소수점 2자리)
    - **주의**: PageSetting이 설정되지 않은 경우 Setting의 paper setting 정보 사용
    - 용지 크기와 Margin 정보 기반 변환
  - **E3 RC Report v5.1**: mm (1자리) → mm (3자리)
    - **용지 정보 포함**: PaperSize, Orientation, Margin 정보 포함 (v5.1 FileFormat 문서 확인)
    - 기존 mm 값 유지, 정밀도 확장 (0.1mm → 0.001mm)

**EzOrtho v1.0 → Cloud**:

- XML → JSON 변환 (Treatment Chart, History Chart 등)
- Chart 데이터 구조 분석 및 재구성
- ToothCode 매핑 테이블 적용
- **좌표 변환**: mm → mm (정밀도 확장)
  - 실제 파일 구조 확인 결과: 이미 mm 단위 사용 (주석에 `<!-- unit : mm -->` 명시)
  - 기존 mm 값 유지, 정밀도 확장 (필요시 소수점 3자리로 확장)

**CleverOne v5.1.0 → Cloud**:

- XML → JSON 변환
- **좌표 변환**: mm → mm (정밀도 확장)
  - 기존 mm 값 유지, 정밀도 확장 (1자리 → 3자리)
  - E3 RC Report v5.1과 동일한 변환 전략 적용
- Paper 정보 포함: PaperSize, Orientation, Margin 정보 활용
- Template 시스템: TemplateName 정보 변환
- Groups 기능: Element 그룹핑 정보 변환 (v1.5.0 이상)

**특수 데이터 처리**:

**1. 이미지 데이터 Migration**:

- E3 v1 Base64 → PNG 파일 추출
- 파일 경로 정규화 (상대→절대 경로)
- 이미지 무결성 검증 (체크썸)

**2. Template 정보**:

- E3 Template → Cloud Template 구조 변환
- Header/Footer 정보 통합
- Paper Setting 정규화

**3. Annotation 데이터**:

- 좌표 시스템 변환 (제품별 좌표 단위 → mm)
- Style 속성 정규화
- InputPoints 포맷 통일

**4. 좌표 단위 변환 (제품별 처리)**:

**E2 Report v3.0, E3 Report v4.0/v5.0 (비율값 → mm)**:

- **입력**: 비율값 (0~1 범위, 소수점 3자리)
- **필요 정보**: 용지 크기 (mm), Margin (mm), Orientation
- **변환 공식**: `mm = (비율값 × (용지크기 - Margin × 2)) + Margin`
- **정밀도**: 소수점 3자리로 반올림 (0.001mm = 1μm)
- **용지 정보 포함 여부**:
  - **E3 Report v4.0/v5.0**: 리포트 파일에 `<Paper>` 섹션 포함
    - `PaperSize`: String (예: "A4", "A3", "Letter", "8x10inch" 등)
    - `Orientation`: String ("Portrait" 또는 "Landscape")
    - `Margin`: Float (mm 단위, Left, Right, Top, Bottom, 소수점 2자리)
    - **주의**: PageSetting이 설정되지 않은 경우 Setting의 paper setting 정보 사용
  - **E2 Report v3.0**: 용지 정보 포함 여부 확인 필요 (Template 시스템 부재로 추정)
- **주의사항**:
  - 용지 크기와 방향에 따라 실제 mm 값이 달라짐
  - 가로/세로 비율값이 같아도 실제 mm 값이 다를 수 있음
  - **용지 정보가 없는 경우**: 기본값(A4 Portrait, Margin 10mm) 사용 또는 사용자 입력 요청

**E3 RC Report v5.1 (mm 1자리 → mm 3자리)**:

- **입력**: mm 단위 (소수점 1자리, ##.#)
- **변환**: 기존 mm 값 유지, 정밀도 확장
- **예시**: `105.5mm` → `105.500mm` (정밀도만 확장)
- **주의사항**: 기존 값의 정밀도 한계로 인한 오차는 허용

**EzOrtho v1.0 (mm → mm)**:

- **입력**: mm 단위 (실제 파일 구조 확인 결과: 주석에 `<!-- unit : mm -->` 명시)
- **변환**: 기존 mm 값 유지, 정밀도 확장 (필요시 소수점 3자리로 확장)
- **예시**: 기존 mm 값 그대로 유지
- **주의사항**: 실제 파일 구조 분석 결과 이미 mm 단위를 사용함

**CleverOne v5.1.0 (mm 1자리 → mm 3자리)**:

- **입력**: mm 단위 (소수점 1자리, ##.#)
- **변환**: 기존 mm 값 유지, 정밀도 확장
- **예시**: `105.5mm` → `105.500mm` (정밀도만 확장)
- **주의사항**: E3 RC Report v5.1과 동일한 변환 전략 적용, 기존 값의 정밀도 한계로 인한 오차는 허용

**좌표 변환 검증**:

- 변환 전후 Element 위치/크기 비교 (±0.1mm 이내 목표)
- 용지 크기별 일관성 검증 (A4, A3 등)
- 역변환 검증 (mm → 비율값 → mm, 원본과 비교)

**검증 시스템**:

**1. 자동 검증**:

- **구조 검증**: JSON Schema 기반
- **데이터 검증**: 필수 필드, 타입, 범위 체크
- **관계 검증**: Element 간 참조 무결성

**2. 시각적 검증**:

- **렌더링 비교**: 원본 vs 변환 결과 시각적 비교
- **PDF 출력 비교**: 인쇄 결과물 픽셀 단위 비교
- **측정값 검증**: 거리, 면적 측정 결과 비교
- **좌표 변환 검증**: Element 위치/크기 변환 정확도 검증 (±0.1mm 이내)

**3. 품질 메트릭**:

- **변환 성공률**: 파일별 변환 완료 비율
- **데이터 정확도**: 변환 전후 핵심 데이터 일치도
- **성능**: 파일 크기별 변환 시간

**처리 최적화**:

- **병렬 처리**: 다중 파일 동시 변환
- **진행 상황 추적**: 실시간 Migration 진행률 표시

**예외 상황 처리**:

- **손상된 파일**: 복구 가능한 부분까지 변환
- **비표준 구조**: Manual Override 옵션 제공
- **변환 실패**: 상세 오류 로그 및 수동 처리 가이드

**산출물**:

1. **Migration 엔진**: 자동화된 변환 시스템
2. **검증 도구**: 변환 품질 자동 검증 시스템
3. **Migration 가이드**: 사용자용 변환 절차서
   - 기존 데이터 변환 절차 (제품별/버전별 상세 절차)
   - 주의사항 및 제한사항
   - 변환 전후 검증 방법
   - 예외 상황 대응 방법
4. **호환성 보고서**: 제품별 변환 지원 범위
5. **예외 처리 매뉴얼**: 특수 상황 대응 방안
6. **성능 최적화 가이드**: 처리 베스트 프랙티스

**다음 단계**: 완성된 Migration 시스템을 PoC-13(Element 렌더링 엔진)과 통합하여 기존 파일의 완전한 웹 렌더링 지원
