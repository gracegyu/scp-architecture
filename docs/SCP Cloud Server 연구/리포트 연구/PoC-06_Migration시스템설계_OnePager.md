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
- **중간 리스크**:
  - 대용량 파일 Migration 시 성능 이슈
  - Image Data 내장 파일 (E3 v1 Base64) 처리 복잡성
  - 손상된 파일 또는 비표준 구조 파일 처리 어려움
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
  - 대용량 파일 처리 테스트 환경
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

- Excel 기반 다중 시트 구조
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

- **좌표 변환**: 비율값 → mm 실측값
- **이미지 처리**: Base64 → 파일 참조, 경로 정규화
- **속성 매핑**: 제품별 속성명 → 통합 속성명
- **구조 재편**: 중첩 XML → 평면적 JSON

**Migration 경로별 처리**:

**E2 v3.0 → Cloud**:

- 직접 변환 (가장 단순)
- Template 정보 없음 → Default Template 적용

**E3 v1.x → Cloud**:

```
v1.x → v1.1.5 → v4.0 → v5.1 → Cloud
```

- 기존 VTE3Migration 도구 활용
- Base64 이미지 → 파일 추출 및 저장

**EzOrtho v1.0 → Cloud**:

- Excel HTML → JSON 변환
- Chart 데이터 구조 분석 및 재구성
- ToothCode 매핑 테이블 적용

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

- 좌표 시스템 변환
- Style 속성 정규화
- InputPoints 포맷 통일

**검증 시스템**:

**1. 자동 검증**:

- **구조 검증**: JSON Schema 기반
- **데이터 검증**: 필수 필드, 타입, 범위 체크
- **관계 검증**: Element 간 참조 무결성

**2. 시각적 검증**:

- **렌더링 비교**: 원본 vs 변환 결과 시각적 비교
- **PDF 출력 비교**: 인쇄 결과물 픽셀 단위 비교
- **측정값 검증**: 거리, 면적 측정 결과 비교

**3. 품질 메트릭**:

- **변환 성공률**: 파일별 변환 완료 비율
- **데이터 정확도**: 변환 전후 핵심 데이터 일치도
- **성능**: 파일 크기별 변환 시간

**대용량 처리 최적화**:

- **스트리밍 처리**: 메모리 효율적인 대용량 파일 처리
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
4. **호환성 보고서**: 제품별 변환 지원 범위
5. **예외 처리 매뉴얼**: 특수 상황 대응 방안
6. **성능 최적화 가이드**: 대용량 처리 베스트 프랙티스

**다음 단계**: 완성된 Migration 시스템을 기반으로 PoC-07(아키텍처 전략) 수립
