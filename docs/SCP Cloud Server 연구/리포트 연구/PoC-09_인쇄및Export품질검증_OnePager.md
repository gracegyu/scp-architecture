Engineering One Pager

**Project Name**: PoC-09: 인쇄 및 Export 품질 검증

**Date**: 2026년 1월 6일

**Submitter Info**: SCP Cloud 개발팀

**Project Description**: 
웹 기반 SCP Cloud Report에서 생성되는 PDF 출력물과 인쇄 결과물이 의료 진단 목적에 적합한 품질을 보장하는지 검증합니다. 기존 Desktop 제품의 DICOM Print 및 고해상도 출력 품질과 동등한 수준을 웹에서 구현할 수 있는지 확인하고, 브라우저별 인쇄 일관성을 보장하는 방안을 마련합니다.

**Business and Marketing Justification**: 
- **의료 표준 준수**: 진단용 이미지 출력의 의료 품질 기준 충족 필수
- **규정 준수**: FDA, CE 등 의료기기 인증 시 출력 품질 요구사항 만족
- **사용자 신뢰**: 정확한 출력 품질로 의료진의 Cloud 서비스 신뢰도 확보
- **경쟁력**: Desktop 제품 대비 우수한 출력 품질로 차별화
- **워크플로우 통합**: 디지털 편집부터 물리적 출력까지 완전한 솔루션 제공
- **비용 효율성**: 고품질 출력으로 재인쇄 비용 및 시간 절약

**Risk Assessment**: 
- **높은 리스크**: 
  - 브라우저 인쇄 API 한계로 의료 표준 품질 달성 어려움
  - DICOM Print 기능의 웹 구현 기술적 한계
- **중간 리스크**:
  - 브라우저별 PDF 생성 품질 차이
  - 고해상도 이미지 처리 시 메모리 및 성능 이슈
  - 색상 프로파일 및 그레이스케일 정확도 문제
- **저위험**: 
  - PDF 생성 라이브러리는 성숙한 기술
- **완화 방안**: 
  - 서버 사이드 PDF 생성 백업 방안
  - 품질 검증 자동화 시스템 구축
  - 의료 표준 준수를 위한 별도 출력 경로

**Resource and Scheduling Details**: 
- **기간**: 2주 (Week 13-14, PoC-09와 병렬 진행)
- **인력**: 
  - Raymond (인쇄 시스템 개발자, 품질 검증 엔지니어, 의료 이미지 전문가 역할 겸임)
    - PDF 생성 엔진 구현 및 최적화
    - 브라우저별 인쇄 품질 테스트
    - 의료 이미지 색상 정확도 검증
    - DICOM Print 대체 방안 연구
- **환경**: 
  - 다양한 프린터 (레이저, 잉크젯, 의료용 프린터)
  - 색상 정확도 측정 도구 (컬러미터)
  - 고해상도 스캐너 (출력 품질 검증용)

**Technical Description**: 

**기존 Desktop 제품 출력 기능 분석**:

**E2/E3 출력 방식**:
- **일반 Print**: 시스템 프린터 다이얼로그 사용
- **DICOM Print**: VTDCMTK 라이브러리 활용
- **PDF Export**: 300DPI 고해상도 벡터 출력
- **Email 전송**: PDF + 개별 이미지 파일 첨부

**RC Report v5.1 출력 향상**:
- **출력 품질 개선**: Capture 시 출력 크기에 맞춰 해상도 조정
- **Overlay 최적화**: Line Thickness, Font Size 자동 조정
- **Multi Capture 개선**: Reference Image 가시성 향상

**웹 기반 출력 구현 전략**:

**1. PDF 생성 방식 비교**:

**클라이언트 사이드**:
```typescript
// jsPDF 활용
const pdf = new jsPDF({
  orientation: 'portrait',
  unit: 'mm',
  format: 'a4'
});

// 고해상도 설정
pdf.setProperties({
  title: 'Medical Report',
  author: 'SCP Cloud',
  creator: 'SCP Report System'
});
```

**서버 사이드**:
```typescript
// Puppeteer 활용
const pdf = await page.pdf({
  format: 'A4',
  printBackground: true,
  preferCSSPageSize: true,
  displayHeaderFooter: false,
  margin: { top: '20mm', bottom: '20mm', left: '20mm', right: '20mm' }
});
```

**2. 이미지 품질 보장**:
- **해상도**: 300 DPI 이상 (의료 표준)
- **색상 공간**: sRGB, Adobe RGB 지원
- **압축**: 무손실 압축 또는 높은 품질 설정
- **DICOM 특화**: 16-bit Grayscale 정확한 표현

**3. 벡터 그래픽 처리**:
- **SVG → PDF**: 벡터 정보 손실 없는 변환
- **Text 렌더링**: 폰트 임베딩으로 일관성 보장
- **Shape 정확도**: Annotation 도형의 정밀한 변환

**품질 검증 시스템**:

**1. 자동 품질 검증**:
```typescript
interface QualityMetrics {
  dpi: number;              // 실제 DPI
  colorAccuracy: number;    // 색상 정확도 (%)
  textSharpness: number;    // 텍스트 선명도
  vectorPrecision: number;  // 벡터 정밀도 (mm)
}
```

**2. 시각적 회귀 테스트**:
- PDF 출력물을 이미지로 변환 후 픽셀 단위 비교
- 기존 Desktop 출력물과 차이점 분석
- 자동화된 시각적 차이 감지 시스템

**3. 의료 표준 준수 검증**:
- **DICOM Part 14**: Grayscale 표시 기준
- **IHE Profile**: 의료 영상 출력 프로파일
- **ISO 12052**: 의료 영상 하드카피 품질

**브라우저별 인쇄 최적화**:

**Chrome/Edge**:
- @media print CSS 최적화
- Canvas toBlob() 고해상도 설정
- Print Preview API 활용

**Firefox**:
- Gecko 엔진 특성 고려한 CSS 조정
- 메모리 효율적 이미지 처리

**Safari**:
- WebKit 인쇄 제약사항 대응
- iOS/macOS 플랫폼 특성 반영

**DICOM Print 대체 방안**:

**웹 환경 제약사항**:
- 직접적인 DICOM Print Server 연결 불가
- 네트워크 프린터 직접 제어 불가

**대체 구현 방안**:
1. **서버 Proxy**: 웹→서버→DICOM Print Server
2. **DICOM 호환 PDF**: DICOM 메타데이터 포함된 PDF 생성
3. **Print Service**: 별도 Desktop 서비스와 연동

**테스트 시나리오**:

**1. 품질 비교 테스트**:
- 동일 리포트를 Desktop vs Web에서 출력
- 픽셀 단위 비교 분석
- 의료진 blind 테스트

**2. 성능 테스트**:
- 대용량 리포트 (100페이지) PDF 생성 시간
- 고해상도 이미지 (4K DICOM) 포함 시 처리 시간
- 메모리 사용량 및 안정성

**3. 호환성 테스트**:
- 다양한 프린터 모델에서 출력 품질
- PDF 뷰어별 (Adobe Reader, 브라우저 내장) 표시 일관성
- 모바일 기기에서의 인쇄 품질

**품질 기준**:
- **해상도**: 300 DPI 이상 보장
- **색상 정확도**: ΔE < 2.0 (색차 허용 범위)
- **텍스트 선명도**: OCR 인식률 99% 이상
- **벡터 정밀도**: ±0.1mm 이내 오차
- **파일 크기**: Desktop 출력물 대비 +30% 이내

**산출물**:
1. **PDF 생성 엔진**: 의료용 고품질 PDF 생성 라이브러리
2. **품질 검증 시스템**: 자동화된 출력 품질 검사 도구
3. **브라우저별 최적화 가이드**: 플랫폼별 인쇄 설정 방안
4. **의료 표준 준수 가이드**: 규정 요구사항 충족 방법
5. **DICOM Print 대체 솔루션**: 웹 환경에서의 DICOM 인쇄 방안
6. **품질 비교 보고서**: Desktop vs Web 출력 품질 분석

**다음 단계**: 고품질 출력이 보장된 시스템을 기반으로 PoC-11(보안 검증) 진행
