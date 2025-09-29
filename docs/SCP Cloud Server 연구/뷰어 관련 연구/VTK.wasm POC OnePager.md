## Project Name

VTK.wasm 기반 3D CT Web 뷰어 POC

## Date

2025-09-29

## Submitter Info

작성자: Raymond

## Project Description

- VTK.wasm이 브라우저에서 의료용 3D CT 볼륨을 원활하게 렌더링/상호작용할 수 있는지 검증한다.
- 대상: DICOM CT 스택 → `vtkImageData` → 볼륨 렌더링(전이함수/카메라/조작), 슬라이스 탐색(옵션)
- 환경: 최신 크롬/엣지(데스크톱/모바일), 기본 WASM 번들 우선(필요 시 커스텀 번들 검토)

## Business and Marketing Justification

- 모바일 최적화된 3D 웹 뷰어 제공은 경쟁력과 사용자 만족도 향상에 핵심
- 클라이언트 사이드 렌더링 고도화로 서버 비용 절감 및 응답성 개선 기대
- VTK.js 대비 성능/기능 이점 확인 시 차세대 뷰어 기반 기술로 채택 가능성

## Risk Assessment

- 볼륨 렌더링 클래스가 번들에 포함되지 않았을 수 있음(기능 간극)
- 초기 로드/초기화 시간 및 메모리 사용량이 클 수 있음(특히 모바일)
- 생태계/문서 성숙도에 따른 통합 복잡도 및 유지보수 리스크
- 대응: 커스텀 빌드/하이브리드 전략(VTK.js 병행), 전처리(Rate10+binning), 단계적 범위 확장

## Resource and Scheduling Details

- 데이터: `CT20130424_213559_8924_40274191/` (약 196MB, 무압축 DICOM) + 50~80MB 소형 CT 1세트 추가 권장
- 기간(초안): 1~2주 (통합 2~3일, 측정/튜닝 3~5일, 정리 1~2일)
- 인력: 프론트엔드 1, 영상 처리/도구 1, QA 0.5

## Technical Description

- 목표/성공 기준

  - 기능: 브라우저에서 3D 볼륨 로드/렌더/조작 성공(크래시/아티팩트 없음)
  - 성능: 데스크톱 30 FPS+, 모바일 15 FPS+ (512³ 기준), 초기 로드 < 5s(고속망)
  - 안정성: 10분 상호작용 동안 메모리 증가 최소, 성능 열화/오류 무

- 작업 항목(체크리스트)

  1. 데이터 로딩: DICOM → `vtkImageData` 경로(브라우저 디코딩 vs 사전 변환), 멀티파일/정렬 확인
  2. 렌더 파이프라인: 볼륨 매퍼/액터/전이함수, 카메라/조작(마우스·터치), FPS 로깅
  3. 번들/통합: VTK.wasm JS API로 렌더러/윈도우/인터랙터 구성, 번들 크기/초기화 시간 측정 및 캐싱/압축 전략
  4. 성능/안정성: 데스크톱/모바일 FPS·메모리·로드 시간, 장시간 조작 안정성 검증
  5. 결과/판단: 기준 충족 시 파일럿 적용, 미달 시 VTK.js 유지 + VTK.wasm 한정 적용/커스텀 빌드 검토

- UI 범위(최소)

  - 캔버스 1개 + FPS 표시/로딩 상태 노출(최소 UI)
  - 카메라 조작: 회전/줌/패닝, 모바일 터치 제스처 지원
  - 전이함수 프리셋 3종 및 윈도우/레벨 슬라이더(간단 UI)
  - 데이터셋 전환(대/소 세트 토글)과 오류/메모리 경고 토스트

- 제외(UI)

  - 주석/측정/세그멘테이션/세부 위젯/동시 편집 등 고급 기능
  - 완성형 UX, 저장/공유, 다국어/i18n, 접근성 고도화(POC 범위 외)

## 개발 환경/도구(명시)

- UI 프레임워크: React 18 + TypeScript
- 패키지 매니저: pnpm
- 번들러: Vite(ESM, WASM 로딩 지원)
- 브라우저 대상: 데스크톱/모바일 Chrome, Edge
- WASM 자산: `.wasm` MIME 서빙 및 publicPath 설정(필요 시 vite-plugin-wasm/자산 복사)
- Node 런타임: 20 LTS 권장

- 참고 링크
  - Activities | VTK.wasm: https://kitware.github.io/vtk-wasm/
  - VTK.wasm from the JavaScript side: https://kitware.github.io/vtk-wasm/guide/js/
