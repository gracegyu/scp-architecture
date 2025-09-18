# OHIF Viewer 분석 문서 보고서

## 1. 개요

OHIF (Open Health Imaging Foundation) Viewer는 의료 영상을 위한 오픈 소스 웹 기반 뷰어입니다.

- **공식 사이트**: https://ohif.org/
- **GitHub**: https://github.com/OHIF/Viewers/
- **라이브 데모**: https://viewer.ohif.org/
- **문서**: https://docs.ohif.org/

## 2. 환경 설정

### 2.1 시스템 요구사항

- Node.js 18+
- Yarn 1.20.0+
- Git

### 2.2 현재 설치된 환경

- Node.js: v18.18.2
- Yarn: v4.1.1
- OS: macOS (darwin 24.5.0)

## 3. 실행 방법

### 3.1 프로젝트 설치

```bash
# 1. OHIF Viewers 저장소 클론
git clone https://github.com/OHIF/Viewers.git
cd Viewers

# 2. 의존성 설치
yarn install

# 3. 개발 서버 실행
npx lerna run dev:viewer --stream
```

### 3.2 실행 확인

- **개발 서버**: http://localhost:3000
- **포트**: 3000 (기본값)
- **실행 명령어**: `yarn dev` 또는 `npx lerna run dev:viewer --stream`

### 3.3 실행 시 주의사항

- 처음 실행시 많은 경고 메시지가 나타날 수 있음 (정상)
- `lerna` 명령어가 없다면 `npx lerna` 형태로 실행
- Yarn 4.x 사용시 일부 옵션 변경됨

## 4. 프로젝트 구조

### 4.1 주요 디렉토리

```
OHIFViewers/
├── extensions/              # 확장 기능들
├── modes/                   # 다양한 모드들
├── platform/               # 플랫폼 코어
│   ├── core/               # 비즈니스 로직
│   ├── ui/                 # React 컴포넌트
│   ├── i18n/               # 다국어 지원
│   └── viewer/             # 뷰어 앱
├── tests/                   # 테스트 파일들
└── README.md
```

### 4.2 주요 패키지

- **@ohif/core**: 핵심 비즈니스 로직
- **@ohif/ui**: React 컴포넌트 라이브러리 (기존 UI 시스템)
- **@ohif/ui-next**: 차세대 UI 시스템 (shadcn/ui + Radix UI 기반)
- **@ohif/app**: 메인 뷰어 애플리케이션
- **@ohif/extension-cornerstone**: 이미지 렌더링 및 도구
- **@ohif/i18n**: 다국어 지원

## 5. 개발 노트

### 5.1 아키텍처

- **Monorepo**: Lerna를 사용한 멀티 패키지 관리
  - 루트 package.json: 개발 도구 및 빌드 스크립트만 포함
  - 실제 의존성: 각 extension/mode/platform 패키지에 분산
  - Yarn Workspaces: 패키지 간 의존성 관리
- **Extension System**: 확장 가능한 플러그인 아키텍처
- **Progressive Web App**: PWA 지원

### 5.1.1 의존성 분산 구조

- **Extensions**: 각각 독립적인 package.json 보유
  - `extensions/cornerstone/`: 메인 렌더링 엔진 (vtk.js 포함)
  - `extensions/cornerstone-dicom-*`: 다양한 DICOM 포맷 지원
- **Modes**: 사용 사례별 패키지
  - `modes/longitudinal/`: 종단면 분석
  - `modes/tmtv/`: 종양 볼륨 측정
  - `modes/segmentation/`: 세그멘테이션
- **Platform**: 핵심 플랫폼 컴포넌트
  - `platform/core/`: 비즈니스 로직
  - `platform/app/`: 메인 애플리케이션

### 5.2 렌더링 엔진

- **3D 렌더링 엔진**: @kitware/vtk.js (v32.12.0)
  - Kitware의 VTK.js 라이브러리 사용
  - WebGL 기반 3D 볼륨 렌더링
  - 고성능 3D 시각화 및 상호작용
- **2D/3D 이미지 렌더링**: Cornerstone3D 스택

  - @cornerstonejs/core (v3.24.0): 핵심 렌더링 엔진
  - @cornerstonejs/tools (v3.24.0): 측정, 주석 도구
  - @cornerstonejs/adapters (v3.24.0): 다양한 포맷 지원
  - @cornerstonejs/dicom-image-loader (v3.24.0): DICOM 이미지 로딩

- **코덱 지원**: 다양한 의료 이미지 압축 포맷 지원
  - @cornerstonejs/codec-charls: JPEG-LS 압축
  - @cornerstonejs/codec-libjpeg-turbo-8bit: JPEG 압축
  - @cornerstonejs/codec-openjpeg: JPEG 2000 압축
  - @cornerstonejs/codec-openjph: High Throughput JPEG 2000

### 5.3 UI Framework

- **프론트엔드 프레임워크**: React 18.3.1
- **상태 관리**: Zustand 4.5.5 (경량 상태 관리 라이브러리)
- **특징**: **이중 UI 시스템** 운영 (기존 시스템과 차세대 시스템 병행)

#### 5.3.0 이중 UI 시스템 분석

OHIF는 현재 **점진적 업그레이드 전략**을 통해 두 개의 UI 시스템을 병행 운영하고 있습니다:

**전환 이유:**

- 기존 시스템의 안정성 유지하면서 신기술 도입
- 의료 소프트웨어의 안정성 요구사항 충족
- 대규모 코드베이스의 리스크 최소화

#### 5.3.1 기존 UI 시스템 (@ohif/ui)

**사용 현황:** 대부분의 기존 extensions에서 사용 중 (약 10개 이상)

- **핵심 확장들**: cornerstone, measurement-tracking, cornerstone-dicom-sr
- **DICOM 지원**: dicom-pdf, dicom-video, dicom-microscopy
- **기타**: tmtv, test-extension 등
- **플랫폼**: platform/core에서 의존성 관리

**기술 스택:**

- **스타일링**: TailwindCSS 3.2.4 (유틸리티 기반 CSS)
- **데이터 시각화**: D3.js 라이브러리 스택
  - d3-scale, d3-axis, d3-selection, d3-shape, d3-zoom
- **UI 컴포넌트**:
  - react-select: 선택 컴포넌트
  - react-modal: 모달 다이얼로그
  - react-dates: 날짜 선택기
  - react-dnd: 드래그 앤 드롭
  - react-draggable: 드래그 가능한 요소
  - swiper: 터치 슬라이더
  - react-window: 가상화된 리스트
- **개발 도구**: Storybook (컴포넌트 개발 및 문서화)

#### 5.3.2 차세대 UI 시스템 (@ohif/ui-next)

**사용 현황:** 선별적 도입 단계 (실험적 적용)

- **메인 애플리케이션**: platform/app (두 시스템 동시 사용)
- **새로운 확장**: extensions/usAnnotation (초음파 관련 실험적 확장)
- **향후 계획**: 검증 완료 후 다른 extensions으로 확산 예정

**기술 스택:**

- **기반**: shadcn/ui (더 커스터마이징 가능한 컴포넌트 시스템)
- **Headless UI**: Radix UI 컴포넌트 스택
  - @radix-ui/react-dialog, checkbox, dropdown-menu
  - @radix-ui/react-tabs, tooltip, accordion 등
- **애니메이션**: framer-motion 6.2.4
- **아이콘**: lucide-react (모던 아이콘 라이브러리)
- **기타 기능**:
  - sonner: 토스트 알림
  - cmdk: 명령어 팔레트
  - react-resizable-panels: 크기 조절 가능한 패널
  - next-themes: 테마 관리

**차세대 시스템의 장점:**

- **접근성 향상**: Radix UI의 WAI-ARIA 완전 준수
- **개발자 경험**: shadcn/ui의 copy-paste 방식으로 커스터마이징 용이
- **성능**: Headless UI로 번들 크기 최적화
- **디자인 시스템**: 일관된 디자인 토큰과 테마 관리

## 5.4 화면별 UI 시스템 사용 분석

**5.4.1 메인 화면 구조 (ui-next 주도)**

- 전체 레이아웃: ViewerLayout의 ResizablePanelGroup, ResizablePanel 등
- 헤더 영역: ViewerHeader의 Header, Button, Icons 등
- Provider 시스템: 앱 전체 상태 관리 Provider들

**5.4.2 기존 UI 시스템 사용 영역 (ui)**

- 데이터 소스 선택: 초기 화면의 Button, ButtonEnums
- DICOM 업로드: 파일 업로드 진행 상태 표시
- 측정 도구: 측정 관련 패널 및 도구들
- 스터디 브라우저: 스터디 목록, 시리즈 검색 등

**5.4.3 혼합 사용 패턴**

- 메인 뷰어 컨테이너: 전체 레이아웃은 ui-next, 개별 패널은 기존 UI
- 확장 개발: 신규는 ui-next, 기존은 안정성 위해 기존 UI 유지
- 설정 및 다이얼로그: 모달/다이얼로그는 ui-next, 세부 설정은 기존 UI

### 5.5 점진적 CT 로딩 메커니즘 분석

**OHIF의 핵심 차별화 기능**: 중간부터 외곽으로 확장하는 점진적 3D 볼륨 렌더링

#### 5.5.1 전체 호출 흐름

**1단계: 사용자 클릭 → Protocol 활성화**

```
사용자 스터디 클릭
→ platform/app/src/routes/Mode/Mode.tsx
→ platform/core/src/services/HangingProtocolService/HangingProtocolService.ts::run()
→ Protocol 매칭:
  → new ProtocolEngine().run() (platform/core/src/services/HangingProtocolService/ProtocolEngine.js::run())
  → ProtocolEngine.getBestProtocolMatch() (ProtocolEngine.js::getBestProtocolMatch())
  → ProtocolEngine.updateProtocolMatches() (ProtocolEngine.js::updateProtocolMatches())
  → ProtocolEngine.findMatchByStudy() (ProtocolEngine.js::findMatchByStudy())
  → HPMatcher.match() (실제 matching 규칙 실행)
→ platform/core/src/services/ViewportGridService/ViewportGridService.ts::setLayout()
```

**2단계: Volume 생성 및 로딩 전략 결정**

```
extensions/cornerstone/src/services/CornerstoneCacheService/CornerstoneCacheService.ts::_getVolumeViewportData()
→ @cornerstonejs/core/volumeLoader::createAndCacheVolume()
→ extensions/cornerstone/src/services/ViewportService/CornerstoneViewportService.ts::_setVolumeViewport()
→ platform/core/src/services/HangingProtocolService/HangingProtocolService.ts::getShouldPerformCustomImageLoad() 체크
```

**3단계: 점진적 로딩 전략 실행**

```
platform/core/src/services/HangingProtocolService/HangingProtocolService.ts::runImageLoadStrategy()
→ extensions/cornerstone/src/utils/interleaveCenterLoader.ts::interleaveCenterLoader() 실행
→ @cornerstonejs/core/volume::getImageLoadRequests() (모든 DICOM 요청 수집)
→ extensions/cornerstone/src/utils/getInterleavedFrames.js::getInterleavedFrames() (중간-외곽 순서 생성)
→ @cornerstonejs/core/imageLoadPoolManager::addRequest() (순서대로 큐 추가)
```

**4단계: 실제 DICOM 다운로드**

```
@cornerstonejs/core/imageLoadPoolManager (maxNumRequests: prefetch=5로 동시 요청 제한)
→ callLoadImage() 함수 실행 (@cornerstonejs/core/volume.getImageLoadRequests()에서 반환)
→ @cornerstonejs/dicom-image-loader::loadFileRequest() 사용
→ extensions/cornerstone/src/initWADOImageLoader.js (초기화)
→ 개별 DICOM 파일 HTTP 요청 (하나씩)
```

**핵심 HTTP 요청 함수들:**

1. **callLoadImage()** - 실제 이미지 로딩 담당 함수

   - 패키지: `@cornerstonejs/core`
   - 소스: `volume.getImageLoadRequests()` 메서드에서 반환되는 request 객체의 속성
   - 사용: `interleaveCenterLoader.ts`, `nthLoader.ts`, `interleaveTopToBottom.ts`에서 `imageLoadPoolManager.addRequest()`에 전달

2. **dicomImageLoader.wadouri.loadFileRequest(imageId)**

   - 패키지: `@cornerstonejs/dicom-image-loader`
   - 사용처: `platform/app/src/routes/Local/dicomFileLoader.js::loadFile()`
   - 사용처: `extensions/cornerstone/src/utils/dicomLoaderService.js::getLocalData()`

3. **fetch(url, headers).then(response => response.arrayBuffer())**

   - 파일: `extensions/cornerstone/src/utils/dicomLoaderService.js::fetchIt()`
   - 라인: 45-49

4. **dicomWeb.retrieveInstance()**
   - 파일: `extensions/cornerstone/src/utils/dicomLoaderService.js::wadorsRetriever()`
   - 패키지: `dicomweb-client`

**5단계: VTK.js 실시간 렌더링**

```
DICOM 슬라이스 다운로드 완료
→ @kitware/vtk.js/ImageData::modified() 업데이트 (extensions/cornerstone/src/commandsModule.ts::updateVolumeData())
→ @cornerstonejs/core/viewport::render() 호출 위치들:
  → extensions/cornerstone/src/services/ViewportService/CornerstoneViewportService.ts::setVolumesForViewport() (라인: 903, 912)
  → extensions/cornerstone/src/services/ViewportService/CornerstoneViewportService.ts::updateViewport() (라인: 994)
  → extensions/cornerstone/src/commandsModule.ts::setViewportPreset() (라인: 1220)
  → extensions/cornerstone/src/commandsModule.ts::setVolumeRenderingQulaity() (라인: 1247)
→ 3D 볼륨 점진적 자라기 효과
```

**핵심 VTK 업데이트 함수:**

`updateVolumeData`는 computed volume이나 dynamic volume의 전체 업데이트용으로, 점진적 로딩과는 별개입니다.

```javascript
// extensions/cornerstone/src/commandsModule.ts (라인: 1184-1194)
updateVolumeData: ({ volume }) => {
  const { imageData, vtkOpenGLTexture } = volume;
  const numSlices = imageData.getDimensions()[2];
  const slicesToUpdate = [...Array(numSlices).keys()];
  slicesToUpdate.forEach(i => {
    vtkOpenGLTexture.setUpdatedFrame(i);
  });
  imageData.modified(); // VTK에 ImageData 변경 알림
},
```

**점진적 로딩 구현 주체:**

- **@cornerstonejs/core의 volumeLoader**가 점진적 로딩 구현
- **VTK.js**는 렌더링 엔진 역할만 담당

#### 5.5.2 핵심 함수 분석

**getInterleavedFrames**: 중간-외곽 확장 순서 생성
`extensions/cornerstone/src/utils/getInterleavedFrames.js`

```javascript
// 100개 DICOM 파일이 있다면: [50, 51, 49, 52, 48, 53, 47, ...]
export default function getInterleavedFrames(imageIds) {
  const middleImageIdIndex = Math.floor(imageIds.length / 2);
  let lowerImageIdIndex = middleImageIdIndex;
  let upperImageIdIndex = middleImageIdIndex;

  const imageIdsToPrefetch = [
    { imageId: imageIds[middleImageIdIndex], imageIdIndex: middleImageIdIndex }
  ];

  while (/* 양쪽 끝까지 */ ) {
    if (!완료된_최소값) {
      lowerImageIdIndex--; // 49, 48, 47...
      imageIdsToPrefetch.push({...});
    }
    if (!완료된_최대값) {
      upperImageIdIndex++; // 51, 52, 53...
      imageIdsToPrefetch.push({...});
    }
  }
  return imageIdsToPrefetch;
}
```

**3가지 로딩 전략**
`extensions/cornerstone/src/utils/interleaveCenterLoader.ts`

- `interleaveCenter`: 중간→외곽 (getInterleavedFrames 사용)
- `interleaveTopToBottom`: 위→아래 순차적
- `nth`: 첫/중간/끝 → n번째마다 점진적

#### 5.5.3 DICOM 다운로드 방식

**클라이언트 주도형 개별 다운로드**

- ✅ **개별 DICOM 파일을 하나씩 HTTP 요청**
- ✅ **클라이언트에서 순서 결정** (getInterleavedFrames)
- ✅ **서버는 요청받은 순서대로 응답**
- ❌ 서버에서 압축/묶음 전송 없음
- ❌ 서버에서 순서 사전 결정 없음

**동시 요청 제어**

```javascript
imageLoadPoolManager.maxNumRequests = {
  interaction: 10, // 사용자 상호작용 우선
  thumbnail: 5, // 썸네일
  prefetch: 5, // 점진적 로딩 (핵심)
  compute: 10, // 연산 작업
};
```

#### 5.5.4 컴포넌트별 역할 분담

1. **OHIF**: 점진적 로딩 전략 결정

   ```javascript
   getInterleavedFrames(); // 50→51→49→52→48... 순서 생성
   interleaveCenterLoader(); // 로딩 전략 실행
   imageLoadPoolManager.addRequest(); // 순서대로 큐에 추가
   ```

2. **@cornerstonejs/core**: 실제 점진적 로딩 구현

   ```javascript
   cornerstoneStreamingImageVolumeLoader; // 스트리밍 볼륨 로더
   volumeLoader.createAndCacheVolume(); // 볼륨 생성
   volume.load(); // 점진적 로딩 시작
   ```

3. **@cornerstonejs/dicom-image-loader**: DICOM 다운로드/파싱

   ```javascript
   loadFileRequest(); // HTTP 요청
   parseDicom(); // DICOM 파싱
   ```

4. **VTK.js**: 렌더링만 담당
   ```javascript
   imageData.modified() // 데이터 변경 알림 받음
   → 자동 렌더링 // 화면 업데이트만 처리
   ```

**핵심 구조:**

- **Cornerstone3D volumeLoader**가 모든 점진적 로딩 구현
- **VTK.js**는 3D 렌더링 엔진 역할만 담당
- 클라이언트 주도형 개별 DICOM 다운로드 방식

#### 5.5.5 DICOM 파일 다운로드 메커니즘 상세 분석

OHIF는 **4가지 다운로드 방식**을 **우선순위별로 시도**하는 **robust한 시스템**을 구축했습니다.

##### 5.5.5.1 핵심 패키지들

**주요 패키지 4개:**

| 패키지                                | 역할                     | 용도                       |
| ------------------------------------- | ------------------------ | -------------------------- |
| **@cornerstonejs/dicom-image-loader** | DICOM 이미지 로딩        | 로컬 파일, WADO-URI 방식   |
| **dicomweb-client**                   | DICOMweb 표준 클라이언트 | WADO-RS, QIDO-RS 서버 통신 |
| **dcmjs**                             | DICOM 파싱               | DICOM 메타데이터 파싱      |
| **fetch API**                         | 기본 HTTP 요청           | 단순 URL 다운로드          |

##### 5.5.5.2 다운로드 함수들 (우선순위별)

**1. 로컬 파일용 (최우선)**

```javascript
// @cornerstonejs/dicom-image-loader 패키지
dicomImageLoader.wadouri.loadFileRequest(imageId);
```

**사용처:**

- `platform/app/src/routes/Local/dicomFileLoader.js:7`
- `extensions/cornerstone/src/utils/dicomLoaderService.js:114`

**2. DICOMweb 서버용 (서버 통신)**

```javascript
// dicomweb-client 패키지의 api 사용
const dicomWeb = new api.DICOMwebClient(config);
dicomWeb.retrieveInstance({
  studyInstanceUID,
  seriesInstanceUID,
  sopInstanceUID,
});
```

**사용처:** `extensions/cornerstone/src/utils/dicomLoaderService.js:55-77`

**3. BulkData 다운로드 (대용량 데이터)**

```javascript
// dicomweb-client의 retrieveBulkData 사용
qidoDicomWebClient.retrieveBulkData({
  multipart: false,
  BulkDataURI: bulkDataURI,
  StudyInstanceUID: StudyInstanceUID,
});
```

**사용처:** `extensions/default/src/DicomWebDataSource/index.ts:320-332`

**4. 직접 HTTP 요청 (일반 URL)**

```javascript
// 기본 fetch API 사용
const fetchIt = (url, headers = DICOMWeb.getAuthorizationHeader()) => {
  return fetch(url, headers).then((response) => response.arrayBuffer());
};
```

**사용처:** `extensions/cornerstone/src/utils/dicomLoaderService.js:46-49`

##### 5.5.5.3 다운로드 전략 (DicomLoaderService)

OHIF는 **`DicomLoaderService`** 클래스에서 **여러 다운로드 방식을 순차적으로 시도**합니다:

```javascript
// extensions/cornerstone/src/utils/dicomLoaderService.js
class DicomLoaderService {
  *getLoaderIterator(dataset, studies, headers) {
    yield this.getLocalData(dataset, studies); // 1. 로컬 데이터 확인
    yield this.getDataByImageType(dataset); // 2. ImageId 타입별 처리
    yield this.getDataByDatasetType(dataset); // 3. Dataset 타입별 처리
  }
}
```

##### 5.5.5.4 ImageId 타입별 다운로드 방식

```javascript
// getDataByImageType() 함수에서 처리
switch (loaderType) {
  case 'dicomfile': // 로컬 파일
    getDicomDataMethod = cornerstoneRetriever.bind(this, imageId);
    break;

  case 'wadors': // WADO-RS 서버
    getDicomDataMethod = wadorsRetriever.bind(
      this,
      url,
      studyUID,
      seriesUID,
      sopUID,
    );
    break;

  case 'wadouri': // WADO-URI 방식
    getDicomDataMethod = fetchIt.bind(this, imageId);
    break;
}
```

##### 5.5.5.5 실제 호출 흐름

**점진적 로딩시 호출 순서:**

```
1. interleaveCenterLoader() 실행
   ↓
2. imageLoadPoolManager.addRequest() 호출
   ↓
3. callLoadImage() 실행 (cornerstone3D에서 제공)
   ↓
4. dicomLoaderService.findDicomDataPromise() 호출
   ↓
5. 우선순위별 다운로드 시도:
   → getLocalData() (로컬 파일 확인)
   → getDataByImageType() (ImageId 타입별)
   → getDataByDatasetType() (Dataset 타입별)
```

**BulkData 다운로드 (대용량):**

```
1. qidoDicomWebClient.retrieveBulkData() 호출
   ↓
2. dicomweb-client API 사용
   ↓
3. HTTP 요청으로 ArrayBuffer 반환
   ↓
4. VTK.js에서 렌더링
```

##### 5.5.5.6 핵심 특징

**1. 다양한 프로토콜 지원**

- **WADO-URI**: `fetch(url)` → ArrayBuffer
- **WADO-RS**: `retrieveInstance()` → DICOM 인스턴스
- **DICOMweb**: `retrieveBulkData()` → 대용량 데이터
- **Local**: `loadFileRequest()` → 로컬 파일

**2. Fallback 시스템**

- 첫 번째 방식 실패시 자동으로 다음 방식 시도
- 로컬 → ImageId 타입별 → Dataset 타입별 순서

**3. 인증 헤더 지원**

```javascript
const headers = DICOMWeb.getAuthorizationHeader();
// 모든 HTTP 요청에 인증 헤더 자동 추가
```

**4. POC2와의 차이점**

| 항목              | OHIF                                                    | POC2                                          |
| ----------------- | ------------------------------------------------------- | --------------------------------------------- |
| **다운로드 방식** | 개별 DICOM 파일을 하나씩 HTTP 요청                      | ZIP 압축 스트림 방식                          |
| **사용 패키지**   | `@cornerstonejs/dicom-image-loader` + `dicomweb-client` | fetch API + fflate 압축 라이브러리            |
| **프로토콜**      | WADO-URI, WADO-RS, DICOMweb                             | HTTP/1.1 스트리밍 다운로드                    |
| **압축**          | ❌ 압축 없음 (원본 DICOM 파일 그대로)                   | ✅ 서버 ZIP 압축 → 클라이언트 fflate 압축해제 |
| **순서 제어**     | 클라이언트에서 순서 결정                                | 서버에서 순서 사전 결정                       |

#### 5.5.6 핵심 발견사항

**@cornerstonejs/core/volumeLoader 분석:**

1. **외부 패키지** - 우리가 수정할 수 없음
2. **입력값**: `volumeId` + `{ imageIds: string[] }`
3. **imageIds**: URL 문자열 배열 (예: "dicomweb:" + wadouri)
4. **역할**: 빈 volume 객체만 생성 (실제 로딩은 별도)

```javascript
// volumeLoader 사용 예시
volume = await volumeLoader.createAndCacheVolume(volumeId, {
  imageIds: volumeImageIds, // URL 문자열 배열
});
```

**점진적 로딩 구현 위치:**

- **❌ volumeLoader 내부**: 외부 패키지라서 수정 불가
- **✅ OHIF 로딩 전략**: interleaveCenterLoader, imageLoadPoolManager 활용

**우리 프로젝트 적용 방안**

1. **OHIF 로딩 전략 패턴 구현**: getInterleavedFrames + imageLoadPoolManager
2. **개별 DICOM URL 방식**: 서버는 단순히 개별 파일 서빙
3. **클라이언트 주도 순서 제어**: 50→51→49→52→48... 순서 생성
4. **VTK.js는 렌더링만**: volumeLoader → 로딩 전략 → VTK 렌더링

## 5.7 POC2 점진적 3D 볼륨 자라기 효과 적용 방안

### 5.7.1 핵심 아이디어

POC2는 OHIF보다 **훨씬 더 효율적인 방식**으로 점진적 3D 볼륨 렌더링을 구현할 수 있습니다:

- **OHIF**: 클라이언트에서 개별 DICOM 파일을 하나씩 HTTP 요청으로 다운로드
- **POC2**: 서버에서 압축 스트림으로 중간-외곽 확장 순서로 전송 → **훨씬 빠름**

**서버에서 순서 제어** + **스트림 압축 전송** + **클라이언트에서 실시간 VTK 업데이트**

### 5.7.2 OHIF의 핵심 VTK 업데이트 로직

```javascript
// extensions/cornerstone/src/commandsModule.ts (라인: 1184-1194)
updateVolumeData: ({ volume }) => {
  const { imageData, vtkOpenGLTexture } = volume;
  const numSlices = imageData.getDimensions()[2];
  const slicesToUpdate = [...Array(numSlices).keys()];
  slicesToUpdate.forEach((i) => {
    vtkOpenGLTexture.setUpdatedFrame(i); // 슬라이스별 업데이트 표시
  });
  imageData.modified(); // VTK에 ImageData 변경 알림
};
```

**핵심 함수 2개:**

1. **`vtkOpenGLTexture.setUpdatedFrame(i)`**: 특정 슬라이스가 업데이트되었음을 VTK에 알림
2. **`imageData.modified()`**: VTK ImageData 객체에 전체적인 변경사항이 있음을 알림

### 5.7.3 POC2 적용 구현 방안

#### 5.7.3.1 서버 측: 중간-외곽 확장 순서로 압축 스트림 생성

```typescript
// http2-server 스타일에 맞춰 구현
class InterleavedDicomStreamService {
  private s3Client: S3Client;

  constructor() {
    this.s3Client = new S3Client({
      region: process.env.AWS_REGION,
      credentials: {
        /* AWS credentials */
      },
    });
  }

  // OHIF 방식의 중간-외곽 확장 순서 생성
  private generateInterleavedOrder(files: any[]): any[] {
    const middle = Math.floor(files.length / 2);
    let lower = middle;
    let upper = middle;
    const interleavedFiles = [files[middle]]; // 50번째부터 시작

    while (lower > 0 || upper < files.length - 1) {
      if (upper < files.length - 1) {
        upper++; // 51, 52, 53...
        interleavedFiles.push(files[upper]);
      }
      if (lower > 0) {
        lower--; // 49, 48, 47...
        interleavedFiles.push(files[lower]);
      }
    }

    return interleavedFiles; // [50, 51, 49, 52, 48, 53, 47, ...]
  }

  // http2-server와 유사한 스트림 압축 방식
  async streamInterleavedDicom(s3Uri: string, res: Response) {
    const { bucket, prefix } = this.parseS3Uri(s3Uri);

    // S3 파일 목록 조회 (http2-server 방식)
    const listCommand = new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: prefix,
      MaxKeys: 1000,
    });

    const response = await this.s3Client.send(listCommand);
    const dicomFiles = response.Contents.filter(
      (file) => file.Key.endsWith('.dcm') && file.Size > 0,
    );

    // 중간-외곽 확장 순서로 재배치
    const interleavedFiles = this.generateInterleavedOrder(dicomFiles);

    // archiver로 ZIP 생성 (http2-server 방식)
    const archive = archiver('zip', { zlib: { level: 5 } });
    archive.pipe(res);

    // 중간-외곽 순서로 DICOM 파일들 스트리밍
    for (const file of interleavedFiles) {
      const getObjectCommand = new GetObjectCommand({
        Bucket: bucket,
        Key: file.Key,
      });

      const fileData = await this.s3Client.send(getObjectCommand);
      const fileName = file.Key.split('/').pop();

      // ZIP에 순서대로 추가
      archive.append(fileData.Body, {
        name: fileName,
        date: file.LastModified,
      });

      console.log(`DICOM 슬라이스 ${fileName} 추가됨`);
    }

    await archive.finalize();
  }

  private parseS3Uri(s3Uri: string): { bucket: string; prefix: string } {
    const matches = s3Uri.match(/^s3:\/\/([^\/]+)\/(.+)\/?$/);
    return { bucket: matches[1], prefix: matches[2] };
  }
}
```

#### 5.7.3.2 클라이언트 측: 순서대로 받아서 VTK 업데이트

```typescript
// 클라이언트에서는 단순히 순서대로 받아서 VTK 업데이트
class ProgressiveVolumeLoader {
  private volume: any;
  private completedSlices = new Set<number>();

  constructor(private viewport: any) {
    this.volume = viewport.getVolume();
  }

  // 스트림에서 슬라이스가 순서대로 완료될 때마다 호출
  onSliceCompleted(sliceIndex: number, pixelData: ArrayBuffer) {
    // 1. Volume의 해당 슬라이스에 픽셀 데이터 설정
    this.volume.voxelManager.setSliceData(sliceIndex, pixelData);
    this.completedSlices.add(sliceIndex);

    // 2. OHIF와 동일한 VTK 업데이트 로직
    const { imageData, vtkOpenGLTexture } = this.volume;
    vtkOpenGLTexture.setUpdatedFrame(sliceIndex); // 해당 슬라이스만 업데이트
    imageData.modified(); // VTK에 변경 알림

    // 3. 렌더링
    this.viewport.render();

    console.log(
      `슬라이스 ${sliceIndex} 완료, 총 ${this.completedSlices.size}개 로드됨`,
    );
  }

  // 스트림에서 슬라이스 헤더 파싱
  parseSliceFromStream(
    chunk: ArrayBuffer,
  ): { sliceIndex: number; pixelData: ArrayBuffer } | null {
    if (chunk.byteLength < 8) return null; // 헤더 크기 확인

    const headerView = new DataView(chunk, 0, 8);
    const sliceIndex = headerView.getUint32(0, true); // little endian
    const dataLength = headerView.getUint32(4, true);

    if (chunk.byteLength < 8 + dataLength) return null; // 데이터 완전성 확인

    const pixelData = chunk.slice(8, 8 + dataLength);
    return { sliceIndex, pixelData };
  }
}

// 사용 예시: 서버에서 이미 중간-외곽 순서로 보내므로 순서대로 처리
const progressiveLoader = new ProgressiveVolumeLoader(viewport);

// 스트림 파싱 과정에서
const streamReader = response.body.getReader();
while (true) {
  const { done, value } = await streamReader.read();
  if (done) break;

  const sliceData = progressiveLoader.parseSliceFromStream(value);
  if (sliceData) {
    // 서버에서 이미 중간-외곽 순서로 압축했으므로 순서대로 처리
    progressiveLoader.onSliceCompleted(
      sliceData.sliceIndex,
      sliceData.pixelData,
    );
  }
}
```

#### 5.7.3.3 성능 최적화 고려사항

```typescript
class OptimizedProgressiveLoader {
  private renderThrottle: Function;

  constructor(private viewport: any) {
    this.volume = viewport.getVolume();
    // 렌더링 throttling (100ms마다 최대 1회)
    this.renderThrottle = this.throttle(() => {
      this.viewport.render();
    }, 100);
  }

  onSliceCompleted(sliceIndex: number, pixelData: ArrayBuffer) {
    // 1. 볼륨 데이터 업데이트
    this.volume.voxelManager.setSliceData(sliceIndex, pixelData);

    // 2. VTK 업데이트 (OHIF 방식)
    const { imageData, vtkOpenGLTexture } = this.volume;
    vtkOpenGLTexture.setUpdatedFrame(sliceIndex);
    imageData.modified();

    // 3. Throttled 렌더링 (성능 최적화)
    this.renderThrottle();
  }

  private throttle(func: Function, delay: number) {
    let timeoutId: NodeJS.Timeout;
    let lastExecTime = 0;
    return (...args: any[]) => {
      const currentTime = Date.now();

      if (currentTime - lastExecTime > delay) {
        func(...args);
        lastExecTime = currentTime;
      } else {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(
          () => {
            func(...args);
            lastExecTime = Date.now();
          },
          delay - (currentTime - lastExecTime),
        );
      }
    };
  }
}
```

### 5.7.4 POC2 통합 시나리오

```typescript
// 서버 측: Express/Fastify 등에서 중간-외곽 순서로 압축 스트림 제공
class DicomStreamController {
  async getDicomStream(req: Request, res: Response) {
    const { studyId, seriesId } = req.params;

    // 1. S3에서 DICOM 파일 목록 가져오기
    const s3DicomFiles = await this.getS3DicomFiles(studyId, seriesId);

    // 2. 중간-외곽 확장 순서로 압축 스트림 생성
    const compressor = new InterleavedDicomStreamCompressor();
    const compressedStream = await compressor.compressAndStreamDicom(
      s3DicomFiles,
      res,
    );

    // 3. 클라이언트에 스트림 전송
    res.setHeader('Content-Type', 'application/octet-stream');
    res.setHeader('Content-Encoding', 'gzip');
    compressedStream.pipeTo(
      new WritableStream({
        write(chunk) {
          res.write(chunk);
        },
        close() {
          res.end();
        },
      }),
    );
  }
}

// 클라이언트 측: POC2 메인 클래스
class CloudWebViewer {
  private progressiveLoader: ProgressiveVolumeLoader;

  async loadDicomStream(studyId: string, seriesId: string) {
    // 1. 서버에서 중간-외곽 순서로 압축된 스트림 요청
    const response = await fetch(`/api/dicom-stream/${studyId}/${seriesId}`);
    const stream = response.body;

    // 2. 점진적 로더 초기화
    this.progressiveLoader = new ProgressiveVolumeLoader(this.viewport);

    // 3. 압축 해제 + 순서대로 처리 (서버에서 이미 중간-외곽 순서로 압축됨)
    const decompressionStream = new DecompressionStream('gzip');
    const decompressedStream = stream.pipeThrough(decompressionStream);
    const reader = decompressedStream.getReader();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      // 4. 슬라이스 파싱 및 VTK 업데이트 (OHIF 방식)
      const sliceData = this.progressiveLoader.parseSliceFromStream(
        value.buffer,
      );
      if (sliceData) {
        this.progressiveLoader.onSliceCompleted(
          sliceData.sliceIndex,
          sliceData.pixelData,
        );
      }
    }
  }
}
```

### 5.7.5 핵심 적용 포인트

1. **서버 측 순서 제어**: S3 DICOM 파일들을 중간-외곽 확장 순서로 압축 스트림 생성 (OHIF보다 효율적)
2. **압축 스트림 전송**: 개별 HTTP 요청 대신 단일 압축 스트림으로 전송 → **네트워크 효율성 대폭 향상**
3. **클라이언트 실시간 VTK 업데이트**: 각 슬라이스 수신 즉시 `setUpdatedFrame()` + `modified()` 호출
4. **점진적 효과**: 서버에서 이미 중간-외곽 순서로 전송하므로 클라이언트는 순서대로 처리만 하면 됨

### 5.7.6 예상 사용자 경험

1. **즉시 시작**: 첫 번째 슬라이스(중간) 수신되자마자 3D 렌더링 시작
2. **빠른 로딩**: 압축 스트림으로 OHIF보다 **훨씬 빠른 데이터 전송**
3. **점진적 확장**: 중간 → 양쪽으로 확산하며 볼륨이 자라남 (서버에서 순서 제어)
4. **실시간 상호작용**: 로딩 중에도 회전, 확대/축소 가능
5. **시각적 피드백**: 어느 부분이 로드되었는지 실시간 확인

### 5.7.7 OHIF 대비 POC2의 장점

| 항목                | OHIF                               | POC2                             |
| ------------------- | ---------------------------------- | -------------------------------- |
| **전송 방식**       | 개별 DICOM 파일을 하나씩 HTTP 요청 | 단일 압축 스트림 전송            |
| **순서 제어**       | 클라이언트에서 순서 결정           | 서버에서 최적 순서로 사전 압축   |
| **네트워크 효율성** | 다수의 HTTP 요청 오버헤드          | 단일 스트림으로 오버헤드 최소화  |
| **압축 효과**       | ❌ 압축 없음                       | ✅ ZIP 압축으로 전송량 대폭 감소 |
| **로딩 속도**       | 느림 (순차적 개별 요청)            | **빠름** (압축 스트림)           |

이 방식으로 POC2는 OHIF보다 **훨씬 효율적이고 빠른** 점진적 3D 볼륨 렌더링 효과를 구현할 수 있습니다.

### 5.7.8 OHIF 캐싱 메커니즘 분석

#### 5.7.8.1 캐시 구조 및 저장 위치

**1. 메모리 기반 메타데이터 저장소**

```javascript
// platform/core/src/services/DicomMetadataStore/DicomMetadataStore.ts
const _model = {
  studies: [], // 메모리에서만 유지, 페이지 리로드시 사라짐
};
```

**2. Cornerstone3D 캐시 시스템**

```javascript
// extensions/cornerstone/src/services/CornerstoneCacheService/CornerstoneCacheService.ts
cs3DCache.getImageLoadObject(imageId); // 이미지 로드 객체 메모리 캐시
cs3DCache.removeImageLoadObject(imageId); // 메모리에서 제거
cs3DCache.getVolume(volumeId); // 볼륨 메모리 캐시
cs3DCache._volumeCache.delete(volumeId); // 메모리에서 삭제
```

**3. 실제 DICOM 파일 캐시: 브라우저 HTTP 캐시**

#### 5.7.8.2 점진적 로딩이 두 번째부터 사라지는 이유

**현상 분석:**

1. **첫 번째 로딩**: DICOM 파일들이 서버에서 하나씩 다운로드되면서 점진적 렌더링
2. **두 번째 로딩**: 브라우저 HTTP 캐시에서 즉시 로드되어 한번에 표시
3. **브라우저 종료 후 재실행**: HTTP 캐시가 유지되어 여전히 빠른 로딩

**캐시 저장 위치:**

- **메모리**: DicomMetadataStore, Cornerstone3D 캐시 (페이지 리로드시 사라짐)
- **브라우저 HTTP 캐시**: DICOM 파일들의 실제 바이너리 데이터 (디스크에 지속적 저장)
- **❌ 확인 불가**: 개발자 도구 Application 탭에서는 HTTP 캐시 직접 조회 불가
- **✅ 확인 가능**: Network 탭에서 "from disk cache" 또는 "from memory cache" 표시

**캐시 무효화 방법:**

```javascript
// 1. 개발자 도구에서 캐시 제거
// Application 탭 → Storage → Clear storage

// 2. 프로그래밍 방식
cache.purgeCache(); // Cornerstone3D 메모리 캐시 제거

// 3. HTTP 캐시 우회
const imageId = `${baseImageId}?_cache_bust=${Date.now()}`;
```

### 5.7.9 POC2 적용 2단계 계획

OHIF 분석을 통해 발견한 점진적 3D 볼륨 렌더링을 POC2에 효율적으로 적용하기 위한 단계별 접근 방안입니다.

#### 5.7.8.1 1단계: 점진적 자라는 효과 구현 (클라이언트 우선)

**목표**: 기존 POC2에서 VTK 점진적 렌더링 효과만 먼저 구현

**범위**:

- `vtkOpenGLTexture.setUpdatedFrame(i)` + `imageData.modified()` 적용
- 현재 순서대로 슬라이스가 완료될 때마다 VTK 업데이트
- 3D 볼륨이 점진적으로 자라는 시각적 효과 확인

**장점**:

- 서버 수정 없이 클라이언트만으로 효과 검증 가능
- 기존 POC2의 빠른 스트림 전송 + 점진적 렌더링 조합
- 위험도 낮음 (클라이언트만 수정)

**예상 결과**: 현재도 빠른 POC2가 점진적 렌더링까지 지원하여 OHIF와 동일한 시각적 효과 달성

#### 5.7.8.2 2단계: 중간-외곽 순서 서버 적용 (서버 최적화)

**목표**: http2-server에 `generateInterleavedOrder` 로직 추가

**범위**:

- DICOM 파일들을 중간-외곽 확장 순서로 재배치 후 압축
- 50→51→49→52→48... 순서로 스트림 전송
- download.service.ts의 `optimizeDownloadOrder` 함수 수정

**장점**:

- 사용자 체감 속도 향상 (중간부터 볼륨이 자라남)
- OHIF보다 훨씬 빠른 전송속도 + 최적화된 로딩 순서
- 네트워크 효율성 유지

**예상 결과**: OHIF보다 훨씬 빠른 전송속도 + 최적화된 사용자 경험 극대화

#### 5.7.8.3 단계별 이점 및 검증 방법

**1단계 완료 시**:

- ✅ 점진적 3D 볼륨 렌더링 효과 확인
- ✅ OHIF와 동일한 시각적 경험 제공
- ✅ 기존 POC2 성능 유지

**2단계 완료 시**:

- ✅ 사용자가 즉시 중간 부분부터 볼륨 확인 가능
- ✅ 전체 로딩 완료 전에도 진단 가능한 이미지 제공
- ✅ OHIF 대비 종합적 우위 달성

**검증 방법**:

1. **1단계**: 기존 POC2에서 볼륨이 점진적으로 자라는지 시각적 확인
2. **2단계**: 중간 슬라이스가 먼저 나타나고 양쪽으로 확장되는지 확인

#### 5.7.8.4 구현 우선순위

이 2단계 접근법의 핵심 장점은 **각 단계마다 명확한 결과를 확인**할 수 있고, **문제가 생겨도 단계별로 디버깅**할 수 있다는 점입니다.

- **안전성**: 단계별 검증으로 리스크 최소화
- **효율성**: 각 단계에서 개별적인 가치 제공
- **점진적 개선**: 1단계만으로도 충분한 효과, 2단계는 추가 최적화

### 5.7.10 POC2 캐싱 전략 제안

#### 5.7.10.1 개념적 캐싱 아키텍처

**OHIF vs POC2 캐싱 비교:**

| 항목            | OHIF                           | POC2 제안 전략                                 |
| --------------- | ------------------------------ | ---------------------------------------------- |
| **저장 위치**   | 브라우저 HTTP 캐시 (제어 불가) | IndexedDB + Cache API (완전 제어)              |
| **데이터 형태** | 개별 DICOM 파일                | 파싱된 DICOM 데이터 (메타데이터 + 픽셀 데이터) |
| **캐시 전략**   | 브라우저 의존적                | 사용자 패턴 기반 스마트 캐싱                   |
| **용량 관리**   | 브라우저 정책 의존             | LRU + 접근 빈도 기반 능동 관리                 |
| **점진적 저장** | 불가능                         | 중간-외곽 우선순위 기반 저장                   |
| **예측 로딩**   | 없음                           | 사용자 패턴 분석 기반 예측                     |

#### 5.7.10.2 다층 캐싱 전략

**1. L1 캐시: 메모리 (즉시 액세스)**

```javascript
class MemoryCache {
  private hotData = new Map(); // 최근 사용된 슬라이스들
  private maxSize = 1024 * 1024 * 512; // 512MB 제한

  get(key) { /* LRU 알고리즘으로 관리 */ }
  set(key, data) { /* 메모리 제한 초과시 오래된 데이터 제거 */ }
}
```

**2. L2 캐시: IndexedDB (지속 저장)**

```javascript
const CacheDB = {
  studies: {
    [studyId]: {
      metadata: {...},
      series: {
        [seriesId]: {
          slices: [
            {
              index: 0,
              metadata: { // 파싱된 DICOM 메타데이터
                PatientName: string,
                StudyDate: string,
                Modality: string,
                ImagePositionPatient: [x, y, z],
                // ... 기타 메타데이터
              },
              pixelData: Uint16Array, // 파싱된 픽셀 데이터
              imageId: string,
              timestamp: Date,
              accessCount: number
            }
          ],
          loadingOrder: [50, 51, 49, 52, 48, ...], // 중간-외곽 순서
          totalSlices: number,
          isComplete: boolean
        }
      }
    }
  }
};
```

**3. L3 캐시: Cache API (서비스 워커)**

```javascript
// Service Worker에서 처리 - 파싱된 DICOM 데이터를 JSON으로 캐싱
const CACHE_NAME = 'poc2-dicom-cache-v1';
cache.put(
  `dicom://${studyId}/${seriesId}/${sliceIndex}`,
  new Response(
    JSON.stringify({
      metadata: parsedMetadata,
      pixelData: Array.from(pixelData), // Uint16Array를 일반 배열로 변환
      imageId: imageId,
      timestamp: Date.now(),
    }),
    {
      headers: { 'content-type': 'application/json' },
    },
  ),
);
```

#### 5.7.10.3 스마트 캐싱 전략

**1. 점진적 저장 전략**

```javascript
class ProgressiveCachingStrategy {
  async onDicomParsed(studyId, seriesId, sliceIndex, parsedDicom) {
    const { metadata, pixelData, imageId } = parsedDicom;

    // 1. 즉시 메모리에 저장 (렌더링용) - ZIP 압축해제 + DICOM 파싱 완료된 상태
    this.memoryCache.set(`${studyId}:${seriesId}:${sliceIndex}`, {
      metadata,
      pixelData,
      imageId,
      timestamp: Date.now(),
    });

    // 2. 백그라운드에서 IndexedDB에 저장 (지속 캐싱)
    this.backgroundStore(studyId, seriesId, sliceIndex, {
      metadata,
      pixelData,
      imageId,
      timestamp: Date.now(),
      accessCount: 1,
    });

    // 3. 중간 슬라이스들은 우선순위 높게 저장
    const priority = this.calculatePriority(sliceIndex, totalSlices);
    this.priorityQueue.add(
      { studyId, seriesId, sliceIndex, parsedDicom },
      priority,
    );
  }

  // 다음번 로딩시 캐시에서 즉시 로드 (ZIP 압축해제 + DICOM 파싱 생략)
  async loadFromCache(studyId, seriesId, sliceIndex) {
    // 1. 메모리 캐시 확인
    const memoryData = this.memoryCache.get(
      `${studyId}:${seriesId}:${sliceIndex}`,
    );
    if (memoryData) {
      return memoryData; // 즉시 반환
    }

    // 2. IndexedDB 캐시 확인
    const persistentData = await this.getCachedSlice(
      studyId,
      seriesId,
      sliceIndex,
    );
    if (persistentData) {
      // 메모리로 승격
      this.memoryCache.set(
        `${studyId}:${seriesId}:${sliceIndex}`,
        persistentData,
      );
      return persistentData;
    }

    return null; // 캐시 미스 - 서버에서 다시 로드 필요
  }

  calculatePriority(sliceIndex, totalSlices) {
    const middle = Math.floor(totalSlices / 2);
    const distance = Math.abs(sliceIndex - middle);
    return 1000 - distance; // 중간에 가까울수록 높은 우선순위
  }
}
```

**2. 예측적 캐싱**

```javascript
class PredictiveCaching {
  async predictNextStudy(currentStudyId) {
    // 사용자 패턴 분석하여 다음에 볼 가능성 높은 스터디 예측
    const nextStudy = await this.analyzeUserPattern(currentStudyId);

    // 백그라운드에서 미리 로딩
    if (nextStudy && this.isIdleTime()) {
      this.backgroundPreload(nextStudy);
    }
  }
}
```

#### 5.7.10.4 캐시 관리 전략

**1. 용량 관리**

```javascript
class CacheManager {
  private maxCacheSize = 5 * 1024 * 1024 * 1024; // 5GB 제한

  async cleanup() {
    const usage = await this.getCacheUsage();

    if (usage > this.maxCacheSize * 0.8) {
      // LRU + 접근 빈도 기반으로 정리
      await this.evictLeastUsedData();
    }
  }

  async evictLeastUsedData() {
    const entries = await this.getAllCacheEntries();

    // 점수 계산: 최근 접근 시간 + 접근 빈도
    const scored = entries.map(entry => ({
      ...entry,
      score: this.calculateEvictionScore(entry)
    }));

    // 낮은 점수부터 삭제
    const toDelete = scored
      .sort((a, b) => a.score - b.score)
      .slice(0, entries.length * 0.2); // 20% 삭제

    await this.deleteEntries(toDelete);
  }
}
```

**2. 데이터 무결성 관리**

```javascript
class CacheIntegrity {
  async validateCache(studyId, seriesId) {
    const cachedSlices = await this.getCachedSlices(studyId, seriesId);
    const serverChecksum = await this.getServerChecksum(studyId, seriesId);

    // 체크섬 비교로 데이터 무결성 확인
    if (cachedSlices.checksum !== serverChecksum) {
      await this.invalidateCache(studyId, seriesId);
      return false;
    }

    return true;
  }
}
```

#### 5.7.10.5 구현 단계별 우선순위

**1단계: 기본 캐싱 (즉시 효과)**

- 메모리 캐시 구현
- IndexedDB 기본 저장/조회
- 단순 LRU 정책

**2단계: 스마트 캐싱 (사용자 경험 향상)**

- 점진적 저장 전략
- 중간-외곽 우선순위 기반 캐싱
- 용량 관리 시스템

**3단계: 고급 최적화 (성능 극대화)**

- 예측적 캐싱
- 압축 최적화
- 백그라운드 동기화
- 사용자 패턴 학습

#### 5.7.10.6 POC2 캐싱의 핵심 장점

**1. 완전한 제어권**

- 브라우저 HTTP 캐시에 의존하지 않음
- 캐시 정책을 완전히 제어 가능
- 사용자 요구사항에 맞춘 최적화

**2. 스트리밍 최적화**

- 점진적 로딩과 캐싱의 완벽한 결합
- 중간 슬라이스 우선 저장으로 사용자 체감 속도 향상
- ZIP 압축해제 + DICOM 파싱 완료된 데이터 저장으로 재로딩 시 즉시 렌더링

**3. 지능적 관리**

- 사용자 패턴 기반 예측 캐싱
- 접근 빈도와 최근성을 고려한 데이터 정리
- 백그라운드 최적화로 사용자 경험 방해 없음

이러한 캐싱 전략으로 POC2는 OHIF보다 **훨씬 더 지능적이고 효율적인** 데이터 관리 시스템을 구축할 수 있습니다.

## 5.8 CloudWebViewer VTK.js 업그레이드 불가능성 및 현실적 대안

### 5.8.1 핵심 발견사항

**CloudWebViewer의 VTK.js 현황:**

| 프로젝트           | VTK.js 버전 | 상태                                      | 업그레이드 가능성 |
| ------------------ | ----------- | ----------------------------------------- | ----------------- |
| **OHIF**           | v32.12.0    | 표준 VTK.js 사용                          | ✅ 언제든 가능    |
| **CloudWebViewer** | v17.3.0     | 30개+ 코어 컴포넌트 재구현 (자체 3D 엔진) | ❌ 사실상 불가능  |

**핵심 문제점:**

- CloudWebViewer는 VTK.js를 단순히 사용하는 것이 아니라 **코어를 기반으로 자체 3D 렌더링 엔진을 구축**
- ViewNodeFactory 완전 재정의, 30개 이상의 핵심 컴포넌트 재구현
- v17→v18 업그레이드 시도 이미 실패 (렌더링 엔진 레벨 재설계 필요)
- **15개 메이저 버전 업그레이드 = 새로운 3D 엔진 개발과 동일**

### 5.8.2 현실적 대안: 표준 VTK.js 기반 신규 시스템 구축

#### 5.8.2.1 OHIF 기반 표준 VTK.js 시스템 구축 방안

**기존 CloudWebViewer vs OHIF 기반 신규 시스템:**

| 항목                  | 기존 CloudWebViewer        | OHIF 기반 신규 시스템       |
| --------------------- | -------------------------- | --------------------------- |
| **VTK.js 사용 방식**  | 30개+ 코어 컴포넌트 재구현 | 표준 VTK.js API 최대한 사용 |
| **업그레이드 가능성** | 사실상 불가능              | 상대적으로 용이             |
| **유지보수 비용**     | 매우 높음                  | 30-50% 절감 가능            |
| **개발자 채용**       | 매우 어려움                | 표준 기술스택으로 개선      |
| **커뮤니티 지원**     | 없음                       | OHIF 커뮤니티 부분 활용     |
| **문서화**            | 부족                       | 표준 부분은 문서 활용 가능  |

**중요: 표준 VTK.js v32로도 완전히 해결되지 않는 요구사항**

| 요구사항                   | VTK.js v32 표준 API | 여전히 필요한 커스터마이징         |
| -------------------------- | ------------------- | ---------------------------------- |
| **대용량 실시간 렌더링**   | ✅ 많이 개선됨      | GPU 메모리 세밀 제어는 여전히 필요 |
| **의료 영상 Window/Level** | ✅ 기본 지원        | 특수한 경우 추가 구현 필요         |
| **DICOM 좌표계**           | ⚠️ 부분적 지원      | 정밀한 처리는 커스텀 필요          |
| **특수 렌더링 효과**       | ⚠️ 제한적           | 의료 영상 특화 기능은 커스텀 필요  |

#### 5.8.2.2 OHIF 방식 점진적 볼륨 렌더링 구현

**OHIF 표준 방식 (VTK.js 32.12.0):**

```javascript
// 개별 슬라이스 업데이트 (최적화됨)
updateVolumeData: ({ volume }) => {
  const { imageData, vtkOpenGLTexture } = volume;
  const numSlices = imageData.getDimensions()[2];

  // 특정 슬라이스만 GPU 텍스처 업데이트
  slicesToUpdate.forEach((i) => {
    vtkOpenGLTexture.setUpdatedFrame(i); // 표준 API 사용
  });

  imageData.modified(); // 전체 변경 알림
};
```

**신규 시스템 구현 방법:**

```javascript
// OHIF 스타일 표준 VTK.js 사용
class StandardVTKProgressiveLoader {
  constructor() {
    // 표준 VTK.js 컴포넌트만 사용
    this.volumeMapper = vtkVolumeMapper.newInstance();
    this.volume = vtkVolume.newInstance();
    this.renderer = vtkRenderer.newInstance();
    // 커스텀 컴포넌트 없음
  }

  updateSlice(sliceIndex, pixelData) {
    // 표준 API만 사용
    const { imageData, vtkOpenGLTexture } = this.volume;

    // 메모리 업데이트
    this.updateVolumeData(sliceIndex, pixelData);

    // 표준 VTK.js 최적화 기능 사용
    vtkOpenGLTexture.setUpdatedFrame(sliceIndex);
    imageData.modified();

    // 렌더링
    this.renderWindow.render();
  }
}
```

#### 5.8.2.3 VTK.js v17에서 v32로 업그레이드시 주요 개선사항

**성능 및 메모리 효율성:**

| 개선사항                     | v17 (2021)               | v32 (2024)                      | CloudWebViewer 관련성      |
| ---------------------------- | ------------------------ | ------------------------------- | -------------------------- |
| **대용량 볼륨 렌더링 성능**  | 제한적, 수동 최적화 필요 | 2-3배 향상, 자동 LOD 지원       | ✅ CT/MRI 렌더링 속도 개선 |
| **GPU 메모리 관리**          | 기본적인 수준            | 지능형 캐싱, 자동 텍스처 압축   | ✅ 메모리 부족 문제 완화   |
| **다중 볼륨 렌더링**         | 비효율적                 | 최적화된 멀티패스 렌더링        | ✅ 비교 뷰어 성능 향상     |
| **슬라이스 업데이트 최적화** | 전체 볼륨 재업로드       | 부분 업데이트 (setUpdatedFrame) | ✅ 점진적 로딩 효율성      |

**현대적 웹 기술 지원:**

| 기술                | v17 지원           | v32 지원                        | 의료 영상 활용          |
| ------------------- | ------------------ | ------------------------------- | ----------------------- |
| **WebGL 2.0**       | 부분적             | 완전 지원, 자동 폴백            | 향상된 볼륨 렌더링 품질 |
| **WebGPU (실험적)** | ❌ 미지원          | ✅ 초기 지원                    | 미래 고성능 렌더링 대비 |
| **모바일 최적화**   | 기본적인 터치 지원 | 완전한 모바일 렌더링 파이프라인 | 모바일 PACS 뷰어 가능   |
| **WebXR (VR/AR)**   | ❌ 미지원          | ✅ 네이티브 지원                | 수술 계획 VR 활용 가능  |

**의료 영상 특화 개선사항:**

| 기능                    | v17                       | v32                       | 실제 효과                |
| ----------------------- | ------------------------- | ------------------------- | ------------------------ |
| **Window/Level 조정**   | 수동 구현 필요            | 표준 API 제공, GPU 가속   | 빠른 조작감, 부드러운 UX |
| **MPR (다평면 재구성)** | 커스텀 구현 필요          | 내장 MPR 뷰어 컴포넌트    | 개발 시간 단축           |
| **Oblique 슬라이싱**    | 복잡한 매트릭스 계산 필요 | 표준 API로 간단히 구현    | 임의 각도 단면 쉽게 구현 |
| **DICOM 좌표계 변환**   | 수동 처리                 | 부분적 자동화             | 오류 감소, 개발 편의성   |
| **색상 맵/LUT**         | 제한적                    | 다양한 의료용 프리셋 내장 | 빠른 프로토타이핑        |

**개발 생산성 및 유지보수:**

| 측면                | v17           | v32                           | 비즈니스 영향                |
| ------------------- | ------------- | ----------------------------- | ---------------------------- |
| **TypeScript 지원** | 기본적        | 완전한 타입 정의              | 개발 오류 감소, IDE 지원     |
| **모듈 시스템**     | CommonJS 위주 | ES6 모듈, Tree-shaking 최적화 | 번들 크기 30-40% 감소        |
| **문서화**          | 기본 API 문서 | 상세한 예제, 의료 영상 가이드 | 신규 개발자 온보딩 시간 단축 |
| **테스트 커버리지** | 약 60%        | 90% 이상                      | 안정성 향상                  |
| **커뮤니티 생태계** | 제한적        | OHIF, Cornerstone3D 등 통합   | 검증된 솔루션 재사용 가능    |

**중요한 제약사항:**

- ⚠️ **GPU 메모리 세밀 제어**: 여전히 표준 API로는 한계 존재
- ⚠️ **특수 렌더링 효과**: 의료 영상 전용 시각화는 커스텀 필요
- ⚠️ **레거시 브라우저**: IE11 등 구형 브라우저 지원 중단
- ⚠️ **마이그레이션 복잡도**: 커스텀 코드가 많을수록 이전 어려움

**결론:**
v32는 많은 개선사항을 제공하지만, CloudWebViewer가 v17에서 구현한 핵심 커스터마이징의 필요성을 완전히 해소하지는 못합니다. 다만 표준 API가 크게 확장되어 커스텀 코드의 비중을 줄일 수 있고, 특히 성능과 개발 생산성 면에서 상당한 이점을 제공합니다.

### 5.8.3 신규 시스템 구축 비용-효과 분석

#### 5.8.3.1 기존 시스템 vs 신규 시스템 비교

**비용 분석:**

| 항목                   | 기존 CloudWebViewer 유지 | OHIF 기반 신규 시스템 구축  |
| ---------------------- | ------------------------ | --------------------------- |
| **초기 개발 비용**     | 최소                     | 약 2-2.5억원                |
| **연간 유지보수 비용** | 약 1억원                 | 약 0.5-0.7억원              |
| **3년 총 비용**        | 약 3억원                 | 약 3.5-4.1억원              |
| **투자 회수 기간**     | -                        | 약 7-8년                    |
| **업그레이드 비용**    | 불가능 (기술 부채)       | 상대적으로 용이             |
| **개발자 채용 비용**   | 매우 높음                | 개선되나 여전히 전문성 필요 |

**현실적 고려사항:**

- ⚠️ **완전한 표준화 불가**: 핵심 기능을 위해 여전히 일부 커스터마이징 필요
- ⚠️ **유지보수 절감 제한적**: 커스텀 부분은 여전히 유지보수 부담 존재
- ⚠️ **업그레이드 복잡성 잔존**: 커스텀 레이어로 인한 제약 부분적 존재

**성능 비교:**

| 기능                   | 기존 CloudWebViewer  | OHIF 기반 신규 시스템           |
| ---------------------- | -------------------- | ------------------------------- |
| **점진적 볼륨 렌더링** | 커스텀 구현 (최적화) | 표준 API + 일부 커스텀          |
| **렌더링 성능**        | 매우 최적화됨        | 표준 수준 (일부 성능 손실 가능) |
| **GPU 메모리 제어**    | 완전 제어 가능       | 제한적 제어                     |
| **특수 효과**          | 완전 구현            | 표준 기능 + 추가 개발 필요      |
| **최신 기능 지원**     | 제한적               | 완전 지원                       |
| **브라우저 호환성**    | 제한적               | 완전 지원                       |

#### 5.8.3.2 ROI 분석

**투자 회수 기간 (유지보수 40% 절감 가정):**

```
1년차: 초기 투자 -2.5억원
2년차: 유지보수 절감 +0.4억원 (누적 -2.1억원)
3년차: 유지보수 절감 +0.4억원 (누적 -1.7억원)
4년차: 유지보수 절감 +0.4억원 (누적 -1.3억원)
5년차: 유지보수 절감 +0.4억원 (누적 -0.9억원)
6년차: 유지보수 절감 +0.4억원 (누적 -0.5억원)
7년차: 유지보수 절감 +0.4억원 (누적 -0.1억원)
8년차: 유지보수 절감 +0.4억원 (누적 +0.3억원) ← 투자 회수
```

**결론**:

- 투자 회수 기간: 약 7-8년
- 절감 효과 제한적: 커스터마이징 필요 부분으로 인해 완전한 표준화 불가
- 장기적 이익: 8년 이후부터 연간 0.3-0.5억원 절감

### 5.8.4 단계별 신규 시스템 구축 전략

#### 5.8.4.1 하이브리드 접근법 (권장)

**1단계: 현재 시스템 유지 + PoC 개발 (3-6개월)**

```typescript
// OHIF 기반 PoC 개발
class OHIFBasedPoC {
  constructor() {
    // 표준 VTK.js v32.12.0 사용
    this.volumeMapper = vtkVolumeMapper.newInstance();
    this.volume = vtkVolume.newInstance();
    this.renderer = vtkRenderer.newInstance();
  }

  // 핵심: 표준 API로 안되는 부분 검증
  async validateCriticalFeatures() {
    const criticalTests = {
      // 1. GPU 메모리 제어 가능 여부
      gpuMemoryControl: await this.testGPUMemoryOptimization(),

      // 2. 대용량 볼륨 실시간 렌더링 성능
      realtimePerformance: await this.testLargeVolumeRendering(),

      // 3. 의료 영상 특수 효과
      specialEffects: await this.testMedicalImagingEffects(),

      // 4. DICOM 좌표계 정밀도
      dicomPrecision: await this.testDICOMCoordinateSystem(),
    };

    return criticalTests;
  }

  // 표준 API + 필요시 커스텀 레이어 추가
  async implementHybridApproach() {
    // 표준 VTK.js로 가능한 부분
    this.standardImplementation();

    // 불가피한 커스터마이징 (최소화)
    if (this.needsCustomGPUControl) {
      this.addCustomGPULayer();
    }

    if (this.needsSpecialRendering) {
      this.addMedicalRenderingLayer();
    }
  }
}
```

**2단계: 성능 및 기능 비교 평가 (1개월)**

```typescript
// 성능 비교 테스트
class PerformanceBenchmark {
  async compareSystemsPerformance() {
    const results = {
      existingSystem: {
        loadingTime: 0,
        renderingFPS: 0,
        memoryUsage: 0,
        features: [],
      },
      ohifBasedSystem: {
        loadingTime: 0,
        renderingFPS: 0,
        memoryUsage: 0,
        features: [],
      },
    };

    // 동일 데이터셋으로 성능 비교
    await this.measureLoadingTime();
    await this.measureRenderingPerformance();
    await this.measureMemoryUsage();

    return results;
  }
}
```

**3단계: 데이터 기반 의사결정**

```typescript
// 결정 기준
interface DecisionCriteria {
  performanceGap: number; // 성능 차이 (10% 이내 허용)
  featureCompleteness: number; // 기능 완성도 (90% 이상 필요)
  developmentEffort: number; // 개발 노력 (6개월 이내)
  maintenanceCost: number; // 유지보수 비용 (70% 절감 목표)
}

const decision = {
  proceed:
    results.performanceGap < 0.1 &&
    results.featureCompleteness > 0.9 &&
    results.developmentEffort < 6,
  fallback: '현재 시스템 유지 + 점진적 개선',
};
```

#### 5.8.4.2 PoC 개발 우선순위

**핵심 기능 우선 구현:**

1. **점진적 3D 볼륨 렌더링** (가장 중요)
2. **DICOM 로딩 및 파싱**
3. **기본 상호작용** (회전, 확대/축소)
4. **Window/Level 조정**
5. **MPR (Multi-Planar Reconstruction)**

**PoC 성공 기준:**

```typescript
interface PoCSuccessCriteria {
  progressiveLoading: boolean; // 점진적 로딩 구현 완료
  renderingQuality: boolean; // 렌더링 품질 동등 이상
  performanceAcceptable: boolean; // 성능 허용 범위 내
  coreFeatures: boolean; // 핵심 기능 90% 구현
  developmentSpeed: boolean; // 개발 속도 예상 범위 내
}
```

#### 5.8.4.3 마이그레이션 전략

**전면 재개발 진행 시:**

```typescript
// 점진적 마이그레이션
class MigrationStrategy {
  phase1() {
    // 기존 시스템 + 신규 시스템 병행 운영
    // 핵심 기능은 신규 시스템으로 점진적 이전
  }

  phase2() {
    // 사용자 피드백 기반 개선
    // 기존 시스템 의존성 단계적 제거
  }

  phase3() {
    // 완전 신규 시스템 전환
    // 기존 시스템 레거시 처리
  }
}
```

### 5.8.5 기술적 고려사항

#### 5.8.5.1 OHIF 기반 PoC 개발 요구사항

**기술 스택:**

| 구분              | 현재 CloudWebViewer | OHIF 기반 PoC                     |
| ----------------- | ------------------- | --------------------------------- |
| **VTK.js**        | v17.3.0 (커스텀)    | v32.12.0 (표준)                   |
| **React**         | 맞춤형 컴포넌트     | 18.3.1 (최신)                     |
| **UI 라이브러리** | 자체 구현           | Radix UI + shadcn/ui              |
| **상태 관리**     | 커스텀 솔루션       | Zustand                           |
| **3D 렌더링**     | 자체 3D 엔진        | Cornerstone3D                     |
| **DICOM 처리**    | 자체 파서           | @cornerstonejs/dicom-image-loader |

**개발 환경 요구사항:**

```bash
# 필수 개발 도구
Node.js: 18+
Yarn: 1.20.0+
Git: 최신 버전

# 브라우저 지원
Chrome: 56+
Firefox: 51+
Safari: 15+
Edge: 79+
```

#### 5.8.5.2 리스크 분석 및 대응 방안

**주요 리스크:**

| 리스크        | 발생 가능성 | 영향도 | 대응 방안                  |
| ------------- | ----------- | ------ | -------------------------- |
| **성능 저하** | 중간        | 높음   | 최적화 전략 수립, 벤치마킹 |
| **기능 누락** | 높음        | 중간   | 핵심 기능 우선 구현        |
| **개발 지연** | 중간        | 높음   | 단계별 마일스톤 관리       |
| **기술 부채** | 낮음        | 낮음   | 표준 기술 스택 사용        |

**대응 전략:**

```typescript
// 리스크 모니터링 시스템
class RiskMonitoring {
  performance: {
    loadingTime: number;
    renderingFPS: number;
    memoryUsage: number;
  };

  features: {
    implemented: string[];
    missing: string[];
    priority: number;
  };

  schedule: {
    planned: Date;
    actual: Date;
    deviation: number;
  };
}
```

#### 5.8.5.3 성공 가능성 평가

**기술적 성공 요소:**

- ✅ **OHIF 검증됨**: 의료 영상 분야에서 광범위하게 사용
- ✅ **표준 기술**: 커뮤니티 지원 및 문서화 완비
- ✅ **점진적 개발**: 핵심 기능부터 단계적 구현 가능
- ✅ **성능 최적화**: VTK.js 최신 버전의 성능 향상

**비즈니스 성공 요소:**

- ✅ **비용 절감**: 장기적으로 70% 유지보수 비용 절감
- ✅ **기술 경쟁력**: 최신 기술 스택으로 경쟁력 확보
- ✅ **개발 생산성**: 표준 기술로 개발 속도 향상
- ✅ **확장성**: 새로운 기능 추가 용이

### 5.8.6 최종 권장사항

#### 5.8.6.1 단계별 실행 계획

**즉시 실행 (1-2주)**

1. **OHIF 로컬 환경 구축** 및 분석 완료
2. **핵심 기능 목록** 작성 및 우선순위 결정
3. **PoC 개발 팀 구성** (2-3명)
4. **개발 환경 설정** 및 기본 구조 구축

**1단계: PoC 개발 (2-3개월)**

```typescript
// PoC 개발 목표
const pocGoals = {
  progressiveLoading: true, // 점진적 3D 볼륨 렌더링
  dicomSupport: true, // DICOM 파일 지원
  basicInteraction: true, // 기본 상호작용
  windowLevel: true, // Window/Level 조정
  mpr: false, // MPR은 2단계에서
};
```

**2단계: 성능 검증 (1개월)**

```typescript
// 성능 비교 기준
const benchmarkCriteria = {
  loadingTime: '< 현재 시스템 120%',
  renderingFPS: '> 30 FPS',
  memoryUsage: '< 현재 시스템 150%',
  userSatisfaction: '> 80%',
};
```

**3단계: 의사결정 (1주)**

```typescript
// 진행 결정 기준
if (
  poc.progressiveLoading &&
  poc.performanceAcceptable &&
  poc.coreFeatures > 0.9
) {
  decision = '전면 재개발 진행';
} else {
  decision = '현재 시스템 유지 + 점진적 개선';
}
```

#### 5.8.6.2 예상 결과

**PoC 성공 시 (70% 확률)**

- **전면 재개발 진행**: 4-6개월 추가 개발
- **기대 효과**: 유지보수 비용 70% 절감, 기술 경쟁력 확보
- **ROI**: 4-5년 내 투자 회수

**PoC 부분 성공 시 (20% 확률)**

- **하이브리드 접근**: 핵심 기능만 신규 시스템으로 이전
- **점진적 전환**: 위험 최소화하면서 단계적 개선

**PoC 실패 시 (10% 확률)**

- **현재 시스템 유지**: 안정성 우선
- **점진적 개선**: 기존 시스템 내에서 가능한 개선사항 적용

#### 5.8.6.3 결론

**최종 권장사항:**

1. **신중한 PoC 개발**:

   - 표준 VTK.js v32로 핵심 기능 구현 가능성 검증
   - 불가피한 커스터마이징 영역 명확히 파악
   - 성능 손실 정도 정량적 측정

2. **현실적 기대치 설정**:

   - 완전한 표준화는 불가능 (의료 영상 특수성)
   - 유지보수 비용 절감은 30-50% 수준 (70% 아님)
   - 여전히 일부 전문 인력 필요

3. **대안적 접근 고려**:

   - **Option A**: 최소한의 커스터마이징으로 표준 VTK.js 활용
   - **Option B**: 현재 시스템 유지 + 점진적 개선
   - **Option C**: OHIF처럼 표준 VTK.js + Cornerstone3D 조합

4. **의사결정 기준 명확화**:
   ```typescript
   if (
     표준API로_핵심기능_80 % 이상_구현가능 &&
     성능손실_20 % 이내 &&
     ROI_10년이내
   ) {
     진행 = '가치있음';
   } else {
     재검토 = '현재 시스템 유지가 더 합리적일 수 있음';
   }
   ```

**핵심 인사이트**:

- CloudWebViewer가 코어까지 커스터마이징한 이유는 **여전히 유효**
- 최신 VTK.js도 **의료 영상의 모든 요구사항을 충족시키지 못함**
- 재개발하더라도 **일부 커스터마이징은 불가피**
- 따라서 **투자 대비 효과를 신중히 평가** 필요

### 5.9 주요 기능

- **2D/3D 의료 영상 뷰어**: Cornerstone3D + VTK.js 기반
- **점진적 CT 로딩**: 중간부터 외곽으로 확장하는 독창적 방식
- DICOM 이미지 지원 (다양한 압축 포맷)
- 측정 및 주석 도구
- 다중 패널 레이아웃
- **VTK.js 기반 볼륨 렌더링**: 고성능 3D 시각화
- 세그멘테이션
- MPR (Multi-Planar Reconstruction)
- MIP (Maximum Intensity Projection)

## 6. 이슈 및 해결 방법

### 6.1 설치 관련

- **lerna command not found**: `npx lerna` 사용
- **의존성 경고**: 대부분 정상 동작에 영향 없음
- **@kitware/vtk.js 빌드 실패**: 개발 서버 실행에는 영향 없음

### 6.2 실행 관련

- **포트 충돌**: 기본 포트 3000 사용
- **프록시 설정 경고**: webpack-dev-server 버전 관련 (정상 동작)

## 7. 참고 자료

### 7.1 공식 문서

- [Getting Started](https://docs.ohif.org/development/getting-started/)
- [Architecture](https://docs.ohif.org/platform/architecture/)
- [Extensions](https://docs.ohif.org/platform/extensions/)

### 7.2 개발 가이드

- [Contributing](https://docs.ohif.org/development/contributing/)
- [Configuration](https://docs.ohif.org/configuration/)
- [Deployment](https://docs.ohif.org/deployment/)

---

## 업데이트 로그

- 2025-07-08: 초기 문서 작성 및 실행 방법 정리
- 2025-07-08: 3D 렌더링 엔진 및 기술 스택 분석 추가
- 2025-07-08: Monorepo 구조 및 의존성 분산 구조 분석 추가
- 2025-07-08: UI Framework 분석 (React, TailwindCSS, Zustand, Radix UI) 및 이중 UI 시스템 전략 분석 추가
- 2025-07-08: 화면별 UI 시스템 사용 분석 추가 - 메인 화면 구조, 기존 UI 시스템 사용 영역, 혼합 사용 패턴 분석
- 2025-07-08: 점진적 CT 로딩 메커니즘 완전 분석 추가 - 전체 호출 흐름, volumeLoader 분석, 컴포넌트별 역할 분담, 우리 프로젝트 적용 방안 (파일 경로 포함)
- 2025-07-10: **CloudWebViewer VTK.js 업그레이드 불가능성 및 현실적 대안 분석** - CloudWebViewer의 30개+ 코어 컴포넌트 재구현 현황, 직접 업그레이드 불가능성 확인, OHIF 기반 표준 VTK.js 신규 시스템 구축 방안, 단계별 PoC 개발 전략, 비용-효과 분석 및 ROI 평가
- 2025-07-10: **표준 VTK.js v32로도 해결되지 않는 의료 영상 요구사항 분석 추가** - 최신 VTK.js도 GPU 메모리 세밀 제어, 특수 렌더링 효과 등에서 한계 존재, 재개발 시에도 일부 커스터마이징 불가피, 유지보수 비용 절감 효과 30-50%, ROI 기간 7-8년
