Engineering One Pager

**Project Name**: PoC-01: 파일 포맷 전환 검증 (XML → JSON)

**Date**: 2026년 1월 6일

**Submitter Info**: SCP Cloud 개발팀

**Project Description**: 기존 Desktop 제품들(E2, E3, EzOrtho, CleverOne)에서 사용하는 XML 기반 리포트 파일 포맷을 JSON 기반으로 전환하는 것의 기술적 타당성과 완전성을 검증하는 PoC입니다. 모든 기존 데이터 구조와 속성을 손실 없이 JSON으로 변환할 수 있는지, 그리고 성능상 이점이 있는지를 확인합니다.

**Business and Marketing Justification**:

- **웹 친화성**: JSON은 JavaScript 네이티브 형식으로 웹 개발 생산성 향상
- **개발 효율성**: TypeScript 타입 자동 생성, 스키마 검증 도구 풍부
- **파싱 성능**: 브라우저에서 XML 대비 빠른 파싱 속도 기대
- **유지보수성**: 복잡한 XML 네임스페이스 제거로 코드 가독성 향상
- **API 통합**: RESTful API와 자연스러운 연동
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
- EzOrtho v1.0: 치료/분석/히스토리 차트 데이터, Tooth Code 연동
- RC Report v5.1: Annotation 데이터, Template 정보 포함

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

**성능 테스트 계획**:

1. **파일 크기 비교**:
   - 원본 XML vs JSON vs gzip 압축된 JSON
   - 대용량 리포트 파일 (100+ 페이지) 테스트
2. **파싱 속도**: Chrome, Firefox, Safari에서 측정
3. **메모리 사용량**: 파싱 후 객체 메모리 오버헤드 비교

**검증 기준**:

- **변환 완전성**: 100% 데이터 손실 없는 변환
- **성능**: XML 대비 파싱 속도 20% 이상 향상
- **파일 크기**: 압축 시 XML 대비 크기 증가 20% 이내
- **개발 생산성**: 타입 정의 자동 생성 및 IDE 지원 확인

**산출물**:

1. XML→JSON 변환 라이브러리
2. JSON 스키마 정의 (JSON Schema)
3. TypeScript 타입 정의 자동 생성 도구
4. 성능 벤치마크 보고서
5. 변환 가이드라인 문서

**다음 단계**: 성공 시 PoC-02(좌표값 시스템)와 연계하여 통합 데이터 모델 설계
