Engineering One Pager

**Project Name**: PoC-01: 파일 포맷 전환 검증 (XML → JSON)

**Date**: 2026년 1월 6일

**Submitter Info**: Raymond

**Project Description**: 기존 Desktop 제품들(E2, E3, EzOrtho, CleverOne)에서 사용하는 XML 기반 리포트 파일 포맷을 JSON 기반으로 전환하는 것의 기술적 타당성을 검증하는 PoC입니다. XML과 JSON 모두 기술적으로 가능하지만, **웹 환경(TypeScript React)에서의 기술 스택 적합성과 개발 생산성 차이**를 정량적으로 측정하여 의사결정 근거를 제공합니다. Migration 가능성은 PoC-06에서 심도 있게 다루며, 본 PoC에서는 변환 가능성과 웹 개발 워크플로우에서의 차이점을 집중 검증합니다.

**Business and Marketing Justification**:

- **웹 표준 트렌드**: 현대 웹 프레임워크(React, Vue, Angular) 및 API 표준(REST, GraphQL)은 JSON을 기본 데이터 포맷으로 사용
- **TypeScript 생태계 적합성**: JSON Schema 기반 타입 자동 생성 도구 풍부 (quicktype, json-schema-to-typescript 등)
- **개발 생산성**: XML의 네임스페이스 복잡성 대비 JSON의 단순한 구조로 코드 작성 시간 단축
- **파싱 성능**: 브라우저 네이티브 JSON.parse() 활용 가능 (XML은 DOMParser 필요)
- **디버깅 편의성**: 브라우저 DevTools에서 JSON 구조 직관적 확인 가능
- **API 통합**: RESTful API, GraphQL 등 웹 표준과 자연스러운 연동
- **기존 투자 보호**: 모든 기존 파일의 완벽한 변환을 통한 데이터 자산 보존

**Risk Assessment**:

- **높은 리스크**:
  - 기존 XML의 복잡한 중첩 구조와 속성을 JSON으로 완전 변환 가능성 불확실
  - E2, E3, EzOrtho 각각 다른 XML 스키마 구조로 인한 변환 복잡성
- **중간 리스크**:
  - JSON 파일 크기 증가 가능성 (XML 압축률 vs JSON 압축률)
  - 기존 사용자의 백업 파일 호환성 이슈
- **저위험**:
  - JSON 파싱 라이브러리는 성숙한 기술로 안정성 확보
- **완화 방안**:
  - 단계별 변환 테스트로 리스크 조기 발견
  - XML↔JSON 양방향 변환 도구 개발로 호환성 보장

**Resource and Scheduling Details**:

- **기간**: 2주 (Week 1-2)
- **인력**:
  - Raymond (Backend 개발, Frontend 개발, QA 검증 역할 겸임)
    - 변환 로직 개발
    - 파싱 성능 테스트
    - 데이터 무결성 검증
- **환경**:
  - 기존 XML 샘플 파일 수집 (각 제품별 최소 10개 이상)
  - 성능 테스트 환경 (다양한 브라우저, 디바이스)

**Technical Description**:

**검증 범위**: 기존 제품별 XML 구조 분석

- E2 Report v3.0: .rpt 파일 (기본 ImageBox, TextBox 구조)
- E3 Report v4.0~v5.1: 복잡한 ItemBox 구조, Auto Fill 정보 포함
- RC Report v5.1: Annotation 데이터, Template 정보 포함 (현재 구현 범위 외, 추후 확장 대상)
- EzOrtho v1.0: 치료/히스토리 차트 데이터, Tooth Code 연동 (Analysis Chart는 현재 구현 범위 외, 추후 확장 대상)

**변환 설계 원칙**:

1. **데이터 무결성 보장**: 모든 XML 정보의 손실 없는 변환
2. **타입 안정성**: TypeScript interface 자동 생성 지원
3. **확장성**: 향후 새로운 Element 추가 고려한 스키마 설계
4. **호환성**: 기존 버전별 스키마 지원

**변환 예시**:

```xml
<!-- 기존 E3 XML 구조 -->
<ItemBox>
  <BoxID>IMG001</BoxID>
  <BoxType>Image</BoxType>
  <BoxPosition>
    <X>0.125</X>
    <Y>0.250</Y>
  </BoxPosition>
  <Image>
    <ImageFitMode>RealSize</ImageFitMode>
    <Scale>
      <ScaleX>1.0</ScaleX>
      <ScaleY>1.0</ScaleY>
    </Scale>
  </Image>
</ItemBox>
```

```json
// 새로운 JSON 구조
{
  "elementType": "imageBox",
  "id": "IMG001",
  "position": { "x": 0.125, "y": 0.25 },
  "properties": {
    "fitMode": "realSize",
    "scale": { "x": 1.0, "y": 1.0 }
  },
  "metadata": {
    "sourceProduct": "e3",
    "version": "5.1"
  }
}
```

**검증 방법 및 테스트 계획**:

**1. 웹 개발 워크플로우 비교** (가중치 35%):

- **TypeScript 타입 자동 생성**:
  - XML (XSD) → TypeScript: 도구 및 복잡도 측정
  - JSON (JSON Schema) → TypeScript: quicktype, json-schema-to-typescript 등 도구 활용
  - 생성된 타입 코드 품질 비교 (타입 안정성, IDE 지원도)
- **코드 작성 시간 측정**:
  - 동일한 Element 구조를 XML/JSON 각각으로 파싱하는 코드 작성 시간 비교
  - IDE 자동완성 지원도 평가
- **스키마 변경 영향도**:
  - 필드 추가/삭제 시 코드 수정 범위 비교

**2. 변환 완전성 검증** (가중치 25%):

- 각 제품별 실제 샘플 파일 5~10개로 XML→JSON 변환 테스트
- JSON→XML 역변환 후 원본과 구조 일치 확인
- 데이터 손실 항목 체크리스트 작성
- **참고**: 실제 Migration 구현은 PoC-06에서 수행

**3. 런타임 성능 측정** (가중치 20%):

- **파싱 속도**: Chrome, Firefox, Safari에서 동일 파일 비교
  - XML: DOMParser 사용
  - JSON: JSON.parse() 사용
  - 반복 테스트(100회) 평균값 측정
- **메모리 사용량**: 파싱 후 객체 메모리 오버헤드 비교 (Chrome DevTools Memory Profiler)

**4. 파일 크기 비교** (가중치 10%):

- 원본 XML vs JSON 크기 비교
- gzip 압축 후 크기 비교 (웹 전송 시나리오)
- 다양한 복잡도의 파일 (단순, 중간, 복잡)로 측정

**5. 유지보수성 평가** (가중치 10%):

- 스키마 구조 복잡도 비교 (네임스페이스, 속성 처리 방식)
- 개발자 학습 곡선 평가

**검증 기준 및 평가 가중치**:

| 항목                          | 가중치 | 평가 기준                                                         |
| ----------------------------- | ------ | ----------------------------------------------------------------- |
| **웹 개발 워크플로우 적합성** | 35%    | TypeScript 타입 자동 생성 가능성, IDE 지원도, 코드 작성 시간 비교 |
| **변환 완전성**               | 25%    | 100% 데이터 손실 없는 변환 가능성 (실제 샘플 파일로 검증)         |
| **런타임 성능**               | 20%    | 브라우저 파싱 속도, 메모리 사용량 비교                            |
| **파일 크기**                 | 10%    | 압축 시 XML 대비 크기 증가율 (20% 이내 목표)                      |
| **유지보수성**                | 10%    | 스키마 변경 시 코드 영향도, 버그 발생 가능성                      |

**참고**: Migration 복잡성과 실제 변환 구현은 PoC-06에서 별도로 검증합니다. 본 PoC에서는 **웹 환경에서의 기술 스택 적합성**에 집중합니다.

**산출물**:

1. **XML→JSON 변환 프로토타입**: 실제 샘플 파일로 변환 가능성 검증 (양방향 변환)
2. **JSON Schema 초안**: 제품별 주요 Element 구조 정의
3. **TypeScript 타입 생성 데모**: JSON Schema → TypeScript 자동 생성 예시 코드
4. **성능 벤치마크 리포트**: 정량적 측정 데이터 (파싱 속도, 메모리, 파일 크기)
5. **개발 생산성 비교 리포트**: 코드 작성 시간, IDE 지원도 등 정량적 비교
6. **의사결정 보고서**: 평가 가중치 기반 종합 점수 및 권장 사항

**결과 보고서 작성 전략**:

- **정량적 데이터 중심**: 주관적 판단이 아닌 측정 가능한 지표 제공
- **실제 워크플로우 기반**: 이론적 장단점이 아닌 실제 개발 시나리오에서의 차이 측정
- **균형잡힌 평가**: JSON의 장점뿐만 아니라 XML 유지 시의 대응 방안도 제시
- **PoC-06 연계**: 본 PoC의 변환 가능성 검증 결과를 PoC-06 Migration 구현에 활용

**다음 단계**:

- 성공 시 PoC-02(좌표값 시스템), PoC-05(Element 스키마), PoC-13(Element 렌더링)과 연계하여 통합 데이터 모델 설계
- PoC-06(Migration 시스템)에서 실제 변환 도구 구현 시 본 PoC 결과 활용
