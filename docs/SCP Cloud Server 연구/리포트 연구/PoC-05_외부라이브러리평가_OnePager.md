Engineering One Pager

**Project Name**: PoC-05: 외부 라이브러리 평가

**Date**: 2026년 1월 6일

**Submitter Info**: Raymond

**Project Description**: PoC-04에서 선정된 렌더링 기술(HTML DOM+SVG)을 기반으로 SCP Cloud Report 시스템 개발에 필요한 외부 라이브러리들을 평가하고 선정합니다. HTML DOM+SVG에 특화된 그래픽 라이브러리, PDF 생성, 이미지 처리, DICOM 지원 등 핵심 영역별로 최적의 라이브러리를 비교 분석하여 기술 스택을 구성합니다.

**Business and Marketing Justification**:

- **개발 속도**: 검증된 라이브러리 활용으로 개발 기간 단축
- **안정성**: 커뮤니티 지원이 활발한 라이브러리로 장기적 안정성 확보
- **라이센스 비용**: 오픈소스 우선으로 라이센스 비용 최소화
- **기능 완성도**: 기존 Desktop 제품 대비 기능 격차 최소화
- **성능 최적화**: 특화된 라이브러리 조합으로 최고 성능 달성
- **커뮤니티 생태계**: 활발한 커뮤니티로 문제 해결 및 확장성 확보

**Risk Assessment**:

- **높은 리스크**:
  - 잘못된 라이브러리 선택 시 중간 변경 어려움 (기술 종속성)
  - 의료용 DICOM 처리의 특수성으로 일반 라이브러리 한계 가능성
- **중간 리스크**:
  - 라이브러리 간 호환성 문제
  - 라이센스 변경으로 인한 법적 리스크
  - 라이브러리 업데이트 중단 리스크
- **저위험**:
  - 대부분 검증된 오픈소스 라이브러리 활용
- **완화 방안**:
  - 다중 대안 라이브러리 평가로 선택권 확보
  - 핵심 기능의 자체 구현 백업 계획

**Resource and Scheduling Details**:

- **기간**: 2주 (Week 3-4, PoC-03과 병렬 진행)
- **인력**:
  - Raymond (Frontend 개발, DevOps, 의료 이미지 전문가 역할 겸임)
    - 라이브러리별 프로토타입 구현
    - 번들 크기 및 성능 최적화
    - DICOM 처리 검증
- **도구**:
  - 번들 분석기 (Webpack Bundle Analyzer)
  - 성능 프로파일링 도구
  - 라이브러리 호환성 테스트 환경

**Technical Description**:

**평가 영역별 후보 라이브러리**:

**1. 그래픽 렌더링 라이브러리** (PoC-04에서 HTML DOM + SVG 선정):

**SVG/DOM 기반 라이브러리**:

- **D3.js**: 데이터 시각화, SVG 조작 강력
- **Snap.svg**: SVG 전용 라이브러리
- **React-Spring**: 애니메이션 및 상호작용

**참고**: PoC-04에서 HTML DOM + SVG 방식이 선정되었으므로, Canvas 기반 라이브러리(Fabric.js, Konva.js, Paper.js)는 평가 대상에서 제외됩니다.

**공통 고려 사항**:

- **Three.js**: 3D 지원, WebGL 가속 (향후 3D 리포트 고려)
- **DragResizeDiv 포팅 결과**: PoC-13에서 포팅된 Handler 시스템과 호환성 우선

**2. PDF 생성 라이브러리**:

- **jsPDF**: 클라이언트 사이드 PDF 생성
- **PDFKit**: 고품질 PDF, 복잡한 레이아웃 지원
- **Puppeteer**: HTML→PDF, 높은 품질
- **React-PDF**: React 컴포넌트 기반

**3. 이미지 처리 라이브러리**:

- **Sharp**: 서버 사이드 이미지 처리 (Node.js)
- **ImageMagick**: 강력한 이미지 변환 기능
- **Pixi.js**: WebGL 기반 이미지 처리
- **Canvas API**: 브라우저 네이티브

**4. DICOM 지원 라이브러리**:

- **cornerstone.js**: DICOM 이미지 뷰어, 의료 특화
- **OHIF**: 완전한 DICOM 뷰어 플랫폼
- **dcmjs**: DICOM 파일 파싱 및 조작
- **dicom-parser**: 경량 DICOM 파서

**평가 기준 및 방법**:

**1. 성능 평가**:

- **번들 크기**: 최종 JavaScript 번들 크기 영향
- **초기 로딩**: First Contentful Paint (FCP) 시간
- **메모리 효율성**: 장시간 사용 시 메모리 리크 여부
- **PoC-14 호환성**: DragResizeDiv 포팅 Handler 시스템과 통합 용이성

**2. 기능 완성도**: 기존 제품 기능 구현 가능성 체크리스트:

- E3 Auto Fill 기능
- EzOrtho 차트 렌더링 (Treatment/History Chart, Analysis Chart는 현재 구현 범위 외, 추후 확장 대상)
- E2/E3 Multi Image Layout (1~20 Row/Column)
- 6가지 Annotation 타입 완전 지원
- 실시간 편집 반응성

**3. 개발 친화성**:

- **TypeScript 지원**: 타입 안전성, IDE 지원
- **React 통합**: 컴포넌트 기반 개발 용이성
- **문서화 품질**: 학습 곡선, 예제 코드 풍부함
- **커뮤니티**: GitHub Stars, 이슈 대응 속도, 업데이트 빈도

**4. 의료 특화 요구사항**:

- **DICOM 호환성**: 다양한 DICOM 포맷 지원
- **색상 정확도**: 16bit Grayscale 정확한 표시
- **측정 도구**: Pixel Spacing 기반 정확한 거리 측정
- **HIPAA 준수**: 클라이언트 데이터 보안 정책

**프로토타입 개발 범위**: 각 라이브러리 조합으로 동일한 기능 구현:

1. **기본 리포트**: A4 용지, ImageBox 4개, TextBox 2개
2. **편집 기능**: 선택, 이동, 크기 조절, 회전
3. **Annotation**: Rectangle, FreeDraw 구현
4. **PDF 출력**: 300DPI 품질 출력
5. **DICOM 이미지**: 실제 의료 이미지 로드 및 표시

**벤치마크 테스트**:

- **E3 복잡도 리포트**: 50개 ImageBox, 20개 TextBox, 100개 Annotation
- **실시간 편집**: 1초에 10회 Element 조작 시 반응성
- **대용량 이미지**: 4K DICOM 이미지 5개 동시 표시
- **메모리 테스트**: 8시간 연속 편집 작업 메모리 안정성

**선정 기준 가중치**:

- 성능 (40%): 의료용 실시간 편집 필수
- 기능 완성도 (30%): 기존 제품 기능 대체 가능성
- 개발 효율성 (20%): 개발 기간 및 유지보수
- 커뮤니티/지속성 (10%): 장기적 지원 가능성

**산출물**:

1. **라이브러리 평가 매트릭스**: 정량적 비교표
2. **권장 기술 스택**: 영역별 최적 라이브러리 조합
3. **프로토타입 코드**: 각 라이브러리별 구현 예제
4. **성능 벤치마크 리포트**: 상세 성능 데이터
5. **라이센스 분석 보고서**: 상용 이용 시 법적 검토 결과
6. **마이그레이션 가이드**: 선정 라이브러리 적용 방안

**다음 단계**: 선정된 라이브러리 기반으로 PoC-06(Element 스키마 설계) 진행
