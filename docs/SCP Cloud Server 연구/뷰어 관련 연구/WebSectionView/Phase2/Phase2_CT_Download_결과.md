# Phase 2: CT Data Download 및 Volume 구성 결과

## 개요

| 항목 | 내용 |
| --- | --- |
| 목표 | S3에서 CT ZIP 다운로드 + Stream Unzip + DICOM 파싱 + 3D Volume 메모리 구성 |
| 기간 | 2026-05-04 |
| 상태 | 구현 완료 |
| 데모 사이트 | http://scp-section-demo.test.scp.esclouddev.com/ (Phase 2 탭) |
| 소스코드 | [Azure DevOps](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc) |

## 구현 결과

### 아키텍처

```
S3 (scp-section-ct-data)
  └── ct-data/sample-ct-01.zip
         │
         ▼  fetch (ReadableStream)
  ┌──────────────────┐
  │  fflate           │  Stream Unzip (다운로드와 동시에 압축 해제)
  │  Unzip/UnzipInflate │
  └──────────────────┘
         │
         ▼  onfile 콜백 (DICOM 파일별)
  ┌──────────────────┐
  │  dicom-parser     │  DICOM 태그 파싱
  │  parseDicom()     │  Pixel Data + Metadata 추출
  └──────────────────┘
         │
         ▼  슬라이스 정렬 + 연결
  ┌──────────────────┐
  │  CTVolume         │  Int16Array 연속 3D Volume
  │  (메모리)          │  + VolumeMetadata
  └──────────────────┘
         │
         ▼  Axial Slice 추출 + Windowing
  ┌──────────────────┐
  │  AxialSliceViewer │  Canvas 2D 렌더링
  │  Slider UI        │  Slice/WC/WW 조절
  └──────────────────┘
```

### 주요 구현 모듈

#### 1. `packages/core/src/dicom/CTVolumeLoader.ts`

CT ZIP 다운로드부터 3D Volume 구성까지의 전체 파이프라인을 담당하는 핵심 모듈.

- **downloadAndBuildVolume(zipUrl, onProgress)**: 메인 진입점. S3 URL을 받아 CTVolume을 반환
- **Stream Unzip**: `fflate`의 `Unzip`/`UnzipInflate`를 사용하여 `fetch` ReadableStream에서 받은 청크를 즉시 `unzip.push()`로 전달. 다운로드와 압축 해제가 동시에 진행
- **DICOM 파싱**: 각 파일이 압축 해제되면 `dicom-parser`로 파싱. 추출하는 주요 태그:
  - Rows (0028,0010), Columns (0028,0011)
  - Pixel Spacing (0028,0030)
  - Image Position Patient (0020,0032)
  - Instance Number (0020,0013)
  - Window Center/Width (0028,1050/1051)
  - Bits Allocated (0028,0100)
  - Rescale Intercept/Slope (0028,1052/1053)
  - Pixel Data (7FE0,0010)
- **Volume 구성**: Instance Number 또는 Image Position Z 기준 정렬 후 연속 `Int16Array`로 합산
- **진행 상황 콜백**: downloading → parsing → building 3단계로 UI에 진행률 전달

#### 2. `packages/components/src/CTLoader.tsx`

CT 데이터 선택 및 다운로드 UI 컴포넌트.

- S3 버킷의 CT ZIP 파일 목록에서 선택 (sample-ct-01 ~ 04)
- "Load CT" 버튼으로 다운로드 시작
- 다운로드/파싱 진행률 프로그레스 바 표시
- 완료 시 소요 시간 표시
- 에러 발생 시 에러 메시지 표시

#### 3. `packages/components/src/AxialSliceViewer.tsx`

로드된 Volume의 Axial Slice를 Canvas 2D로 렌더링하는 검증용 컴포넌트.

- Slice Index Slider: 0 ~ (sliceCount-1) 범위에서 Axial Slice 탐색
- Window Center/Width Slider: CT Windowing 조절 (HU 기반)
- Volume 메타데이터 표시: dimensions, 메모리 크기, spacing
- Rescale Intercept/Slope 적용하여 HU 값 변환 후 Windowing

#### 4. `apps/section-demo/src/App.tsx`

Phase 1/2 탭 전환 UI 추가.

- Phase 1 탭: 기존 WebGL Multi-View (SectionViewer)
- Phase 2 탭: CT Download + AxialSliceViewer

### 기술 스택

| 라이브러리 | 버전 | 용도 |
| --- | --- | --- |
| fflate | ^0.8.2 | ZIP Stream Unzip (브라우저) |
| dicom-parser | ^1.8.21 | DICOM 파일 파싱 |

### CT Data 저장소

| 항목 | 내용 |
| --- | --- |
| S3 버킷 | scp-section-ct-data |
| 리전 | ap-northeast-2 (서울) |
| 데이터 | ct-data/sample-ct-01.zip ~ sample-ct-04.zip |
| 접근 | 퍼블릭 읽기 (PoC 전용) |
| CORS | Demo Site + localhost 허용 |

### 메모리 사용량 분석

치과 CT 기준 (512 x 512 x N slices, 16bit):

| 슬라이스 수 | Raw Volume 크기 | 비고 |
| --- | --- | --- |
| 200장 | ~100 MB | 소형 CT |
| 300장 | ~150 MB | 일반적 치과 CT |
| 500장 | ~250 MB | 대형 CT |

브라우저 메모리 한도(1~2GB) 내에 충분히 수용 가능. 연속 `Int16Array`로 구성하여 이후 WebGL 3D Texture 업로드에도 효율적.

### 참고: stream-zip-unzip PoC와의 관계

[stream-zip-unzip PoC](https://dev.azure.com/ewoosoft/prototypes/_git/stream-zip-unzip)의 `http2-client` 모듈에서 검증된 기술을 재활용:

- `fflate`의 `Unzip`/`UnzipInflate`를 이용한 브라우저 Stream Unzip 패턴
- `dicom-parser`를 이용한 DICOM 파일 파싱 패턴
- S3 공개 URL에서 `fetch` + ReadableStream 패턴

차이점:
- stream-zip-unzip은 DICOM 파일을 개별적으로 파싱하여 썸네일만 생성 (UI 미리보기 목적)
- 본 구현은 모든 DICOM 슬라이스를 파싱하여 **연속 3D Volume**으로 재구성 (Volume Reslice 목적)

## 성공 기준 달성 여부

| 기준 | 달성 여부 |
| --- | --- |
| CT ZIP 다운로드 정상 동작 | O (S3 CORS + 퍼블릭 읽기) |
| Stream Unzip 정상 동작 (다운로드와 동시 압축 해제) | O (fflate Unzip/UnzipInflate) |
| DICOM 파싱으로 픽셀 데이터 + 메타데이터 추출 | O (dicom-parser) |
| 3D Volume (Int16Array) 메모리 구성 | O (슬라이스 정렬 + 연속 배열) |
| 구성된 Volume에서 임의 Axial Slice 추출 및 화면 표시 | O (Canvas 2D + Windowing) |
| 다운로드 진행률 UI | O (3단계 진행 상황 콜백) |

## 다음 단계

Phase 3에서는 이 Volume을 기반으로 Scout View에 Axial Slice를 표시하고, Slider로 최적 Slice를 선택하는 UI를 구현한다. Phase 2의 `AxialSliceViewer`가 Phase 3의 기초가 된다.
