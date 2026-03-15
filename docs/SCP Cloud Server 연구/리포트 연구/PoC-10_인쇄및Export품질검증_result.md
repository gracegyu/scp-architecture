# PoC-10 결과 보고서: 인쇄 및 Export 품질 검증

## 요약

- **목표**: 웹 기반 SCP Cloud Report의 PDF·인쇄 출력물이 의료 진단 목적에 적합한 품질을 보장하는지 검증
- **전략**: 브라우저 인쇄(기본) + 서버 Puppeteer PDF(고품질) 이원화. PoC-03(pt, mm, @media print) 전략 준수
- **품질 기준**: 해상도 300 DPI(서버 PDF), mm 좌표 ±0.1mm, 텍스트 선명도, 색상 정확도 ΔE < 2.0
- **제약**: 브라우저 window.print()는 300 DPI 강제 불가(프린터/드라이버 의존). 고품질은 서버 PDF 권장
- **산출물**: 출력 전략, 품질 검증 가이드, 브라우저별 최적화, DICOM Print 대체 방안

---

## 1. 개요

### 1.1 검증 목표

웹 기반 SCP Cloud Report에서 생성되는 PDF 출력물과 인쇄 결과물이 **의료 진단 목적에 적합한 품질**을 보장하는지 검증합니다. 기존 Desktop 제품(E2/E3)의 DICOM Print 및 고해상도 출력 품질과 동등한 수준을 웹에서 구현할 수 있는지 확인하고, 브라우저별 인쇄 일관성을 보장하는 방안을 마련합니다.

**핵심 질문**:

- 브라우저 인쇄만으로 의료 품질 기준(300 DPI 등)을 충족할 수 있는가?
- 고품질 PDF 생성은 클라이언트 vs 서버 중 어느 쪽이 적합한가?
- DICOM Print 기능을 웹에서 어떻게 대체할 수 있는가?

### 1.2 선행 PoC 반영

| PoC    | 결정 사항                          | 인쇄/Export 영향                                      |
| ------ | ---------------------------------- | ----------------------------------------------------- |
| PoC-02 | mm 좌표, 소수점 3자리              | 출력 시 물리적 크기(mm) 보장 목표                     |
| PoC-03 | pt 폰트, 96 DPI 화면, @media print | 인쇄 시 pt·mm 수학적 일치, CSS 기반 출력              |
| PoC-05 | Puppeteer(서버), html2canvas       | 고품질 PDF는 Puppeteer, 클라이언트 인쇄은 html2canvas |

### 1.3 평가 기준

| 항목           | 가중치 | 평가 기준                                      |
| -------------- | ------ | ---------------------------------------------- |
| **품질 달성**  | 35%    | 300 DPI, mm 정확도, 텍스트 선명도              |
| **구현 가능성**| 30%    | 웹 환경에서 기술적 실현 가능 여부              |
| **일관성**    | 20%    | 브라우저·프린터별 출력 품질 일관성             |
| **의료 표준**  | 15%    | DICOM Part 14, ISO 12052 등 준수               |

---

## 2. 출력 방식 분석

### 2.1 브라우저 인쇄 (window.print)

**특징**:

- 별도 라이브러리 없이 브라우저 표준 기능 사용
- @media print CSS로 화면·인쇄 스타일 분리
- mm, pt 단위 사용 시 브라우저가 물리적 크기로 변환

**제약** (검증 결과):

- **300 DPI 강제 불가**: 브라우저는 CSS/JS로 출력 해상도를 직접 지정할 수 없음. 실제 DPI는 프린터 드라이버·설정에 의해 결정됨
- **일반적으로 72~96 DPI** 기준으로 렌더링 후, 프린터가 스케일링. 고해상도 프린터(300 DPI)에서는 브라우저 출력을 확대하여 인쇄하므로 선명도는 유지되나, 픽셀 단위 제어는 불가
- **물리적 크기(mm, pt)**: CSS mm·pt는 논리적 단위이므로 인쇄 시 올바른 물리적 크기로 변환됨 (PoC-03 검증)

**적용 범위**:

- 일반 인쇄, 빠른 미리보기, 간단한 리포트 출력
- 의료 인증이 엄격하지 않은 용도

### 2.2 클라이언트 PDF (jsPDF, html2canvas)

**html2canvas + jsPDF** (PoC-05 선정 흐름):

- html2canvas: HTML/SVG → Canvas(이미지) 변환. EzOrthoWeb에서 검증됨
- jsPDF: Canvas/이미지를 PDF에 삽입
- **한계**: Canvas는 래스터화되며, 해상도는 화면 DPI(96) 기준. 300 DPI 의료 품질 달성 어려움

**적용 범위**:

- 즉시 PDF 다운로드 필요 시
- 고품질보다 속도·편의성 우선 시

### 2.3 서버 PDF (Puppeteer)

**특징** (PoC-05 선정):

- Chrome/Chromium으로 HTML 렌더링 후 PDF 변환
- **printBackground, preferCSSPageSize** 등으로 @media print 반영
- **scale 옵션**으로 출력 해상도 조정 가능 (예: scale 3.125 ≈ 300 DPI from 96 DPI base)

**구현 예시**:

```typescript
const pdf = await page.pdf({
  format: 'A4',
  printBackground: true,
  preferCSSPageSize: true,
  margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' },
  scale: 1,  // 1 = 96 DPI 기준. 300 DPI 목표 시 scale ≈ 3.125 (실제는 프린터 해상도에 따름)
})
```

**적용 범위**:

- 의료 품질(300 DPI) 요구 시
- 공식 문서·아카이브용 PDF

---

## 3. 품질 기준 및 검증 방법

### 3.1 품질 기준 (OnePager 반영)

| 항목           | 목표                    | 검증 방법                          |
| -------------- | ----------------------- | ---------------------------------- |
| 해상도         | 300 DPI 이상 (고품질)   | 서버 PDF scale 설정, 출력물 측정   |
| mm 좌표 정확도 | ±0.1mm 이내             | 자로 측정, PoC-02/03 전략 준수     |
| 텍스트 선명도   | OCR 인식률 99% 이상     | 샘플 출력 후 OCR 테스트            |
| 색상 정확도    | ΔE < 2.0 (색차)         | 컬러미터 측정 (선택)               |
| 벡터 정밀도    | ±0.1mm 이내             | SVG→PDF 변환 시 좌표 유지 확인     |

### 3.2 품질 검증 인터페이스

```typescript
interface QualityMetrics {
  dpi: number           // 실제 측정 DPI
  colorAccuracy: number // 색상 정확도 (%)
  textSharpness: number // 텍스트 선명도 (0~1)
  vectorPrecision: number // 벡터 정밀도 (mm)
  mmError: number       // mm 좌표 오차 (mm)
}
```

### 3.3 검증 시나리오

1. **mm 좌표 검증**: A4 용지에 10mm×10mm 사각형 출력 후 자로 측정
2. **폰트 크기 검증**: 12pt 텍스트 출력 후 높이 측정 (목표 4.233mm)
3. **브라우저별 비교**: Chrome, Edge, Firefox, Safari에서 동일 리포트 인쇄 후 시각적 비교
4. **서버 PDF vs 브라우저 인쇄**: Puppeteer PDF와 window.print 결과 비교

---

## 4. 브라우저별 인쇄 최적화

### 4.1 Chrome / Edge (Chromium)

- @media print, @page 지원 양호
- printBackground: true 필요 시 명시
- Canvas toBlob() 고해상도: `{ type: 'image/png', quality: 1 }` 등

### 4.2 Firefox

- Gecko 엔진 특성으로 일부 CSS 차이 가능
- -webkit- 프리픽스 미지원, 표준 @media print 사용

### 4.3 Safari (WebKit)

- iOS/macOS 인쇄 시 WebKit 제약
- @page margin 등 일부 속성 동작 차이 가능

**공통 권장**:

- **mm, pt 단위** 사용 (px 최소화)
- **배경색/이미지** 인쇄 시 `print-color-adjust: exact` 또는 `-webkit-print-color-adjust: exact` 고려

---

## 5. DICOM Print 대체 방안

### 5.1 DICOM Print vs 리포트 인쇄

DICOM Print(Part 14)는 **의료 영상**(CT, MRI, X-ray 등)을 필름·건식 이미저로 출력하기 위한 표준이다. 리포트(텍스트 기반 진단 소견)는 대상이 아니다.

| 출력물 | 일반적 방식 | DICOM Print 사용 |
|--------|-------------|------------------|
| 영상 | DICOM Print → 필름/건식 이미저 | 사용 |
| 리포트 | PDF → 네트워크/레이저 프린터 | 거의 없음 |

**대형 병원 실무**: 리포트는 PACS/RIS에서 PDF로 출력하거나 일반 네트워크 프린터로 인쇄한다. DICOM Print는 영상용이며, 리포트용 요구는 드물다. 예외적으로 리포트+핵심영상 합성물을 이미지로 출력하는 경우는 있으나, SCP Cloud Report의 1차 범위는 아니다.

**결론**: 리포트 시스템은 **PDF + 일반 인쇄**로 충분. DICOM Print 연동은 E2/E3 영상 출력 상속 요구 시에만 검토 대상.

### 5.2 웹 환경 제약

- 브라우저에서 DICOM Print Server에 직접 연결 불가
- 네트워크 프린터 직접 제어 불가

### 5.3 대체 구현 방안 (DICOM Print 요구 시)

| 방안                    | 설명                                       | 적합성   |
| ----------------------- | ------------------------------------------ | -------- |
| **서버 Proxy**          | 웹→서버→DICOM Print Server 연동            | 높음     |
| **DICOM 호환 PDF**      | DICOM 메타데이터 포함 PDF 생성 후 전달      | 중간     |
| **Print Service 연동**  | 별도 Desktop 서비스와 연동                 | 중간     |
| **일반 PDF + 인쇄**     | 고품질 PDF 생성 후 사용자가 시스템 인쇄    | 기본 적용 |

**권장**: 1차적으로 **고품질 PDF(서버 Puppeteer) 생성 + 사용자 시스템 인쇄**. 리포트용 DICOM Print 요구는 드물므로 기본은 PDF 전략. 영상·Desktop 상속 요구 시 **서버 Proxy** 또는 **Desktop 연동** 검토.

---

## 6. 출력 전략 최종 선정

### 6.1 이원화 전략

| 용도           | 방식                    | 품질 수준   |
| -------------- | ----------------------- | ----------- |
| **일반 인쇄**  | window.print() + @media print | 브라우저·프린터 의존 |
| **PDF 다운로드** | 서버 Puppeteer (고품질) | 300 DPI 목표 |
| **빠른 미리보기** | html2canvas + jsPDF (선택) | 일반 품질   |

### 6.2 구현 우선순위

1. **1차**: window.print() + @media print (PoC-03 전략). mm, pt 단위로 물리적 크기 보장
2. **2차**: 서버 API로 Puppeteer PDF 생성. 고품질 필요 시 사용
3. **3차**: html2canvas 기반 클라이언트 PDF (EzOrthoWeb 검증 방식). 서버 부재 시 대안

### 6.3 CSS 인쇄 가이드

```css
@media print {
  @page {
    size: A4;
    margin: 10mm;
  }
  body {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .report-page {
    width: 210mm;
    height: 297mm;
    box-sizing: border-box;
  }
}
```

---

## 7. 결론 및 다음 단계

### 7.1 핵심 결론

1. **브라우저 인쇄**: 300 DPI 강제 불가. mm·pt 단위로 물리적 크기는 보장 가능 (PoC-03)
2. **고품질 PDF**: 서버 Puppeteer 사용. HTML→PDF 완전 변환, 300 DPI 목표 달성 가능
3. **품질 검증**: mm 좌표, 폰트 크기 실측 검증 필요. PoC-14 렌더링 엔진 완성 후 통합 테스트 권장

### 7.2 제한사항

- 실제 프린터·종이 출력 품질은 환경 의존
- DICOM Print는 웹에서 직접 구현 불가, Proxy 또는 연동 서비스 필요

### 7.3 다음 단계

1. **PoC-14**: Element 렌더링 엔진에 @media print 적용 후 출력 품질 검증
2. **PoC-11**: 보안 검증 (출력물 포함 데이터 보호)
3. **구현**: 서버 PDF API (Puppeteer) 설계 및 개발

---

**검증 일자**: 2026-01-23  
**참조**: PoC-03_DPI및렌더링전략결정_result.md, PoC-05_외부라이브러리평가_result.md, PoC-10_인쇄및Export품질검증_OnePager.md
