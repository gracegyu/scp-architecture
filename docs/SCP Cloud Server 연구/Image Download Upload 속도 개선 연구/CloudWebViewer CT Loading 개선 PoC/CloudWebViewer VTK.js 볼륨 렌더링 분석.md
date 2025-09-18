## 0. 빌드 체인 (Build Chain)

### **빌드 순서 및 의존성**

**중요**: 코드 변경 시 반드시 다음 순서대로 빌드해야 변경사항이 적용됩니다.

```
1. lib/vtkjs-wrapper 빌드
   cd lib/vtkjs-wrapper && pnpm build
   → dist/ 디렉토리에 빌드 결과 생성
   → loadVolume.ts 등 핵심 VTK 로직 포함

2. lib/react-vtkjs 빌드 (vtkjs-wrapper 사용)
   cd lib/react-vtkjs && pnpm build
   → dist/react-vtkjs.js 생성 (6.3MB)
   → CTViewerController.tsx 등 React 컴포넌트 포함

3. packages/core 빌드 (react-vtkjs 사용)
   cd packages/core && pnpm build
   → dist/assets/ 디렉토리에 빌드 결과 생성
   → CTContentHandler.ts 등 비즈니스 로직 포함

4. examples/host-app 실행 (core 사용)
   cd examples/host-app && pnpm dev
   → Module Federation으로 core 패키지 런타임 로드
   → POCTab.tsx에서 실제 테스트 수행

```

### **패키지 의존성 구조**

```
examples/host-app
  └── @cloudwebviewer/core-types (link:../../types/core)
  └── Module Federation → packages/core

packages/core
  └── @cloudwebviewer/react-vtkjs (workspace:^)
  └── @cloudwebviewer/core-types (workspace:^)

lib/react-vtkjs
  └── @cloudwebviewer/vtkjs-wrapper (workspace:^)

lib/vtkjs-wrapper
  └── @kitware/vtk.js (^17.3.0)
  └── @ewoosoft/es-dicom (^2.0.0-alpha.1)

```

### **빌드 실패 시 대처법**

**증상**: 코드 변경 후 로그가 출력되지 않거나 변경사항이 반영되지 않음

**원인**: 상위 패키지가 하위 패키지의 이전 빌드 결과를 사용하고 있음

**해결책**:

1. 변경된 패키지부터 상위 패키지까지 순차적으로 모두 다시 빌드
2. 특히 `lib/vtkjs-wrapper` 변경 시 → `lib/react-vtkjs` → `packages/core` 순서로 빌드
3. 필요시 `rm -rf dist/` 후 clean build 수행

### **빌드 자동화 스크립트**

프로젝트 루트에 빌드 자동화 스크립트가 제공됩니다:

**1. 전체 빌드 스크립트**

```bash
./build-all.sh

```

- 4단계 빌드를 순차적으로 자동 실행
- 각 단계별 소요 시간 측정 및 표시
- 에러 발생시 자동 중단
- 컬러 출력으로 진행 상황 시각화

**2. Clean Build 스크립트**

```bash
./build-clean.sh

```

- 모든 dist/ 디렉토리 삭제
- 전체 빌드 스크립트 자동 실행
- 완전한 새로운 빌드 보장

### **개발 시 주의사항**

- **Hot Reload 제한**: workspace 패키지 간 변경사항은 Hot Reload로 반영되지 않음
- **Module Federation**: host-app은 core를 런타임에 로드하므로 core 변경 시 재빌드 필요
- **TypeScript 타입**: 타입 변경 시에도 전체 빌드 체인 재실행 권장
- **빌드 스크립트 활용**: 수동 빌드 대신 `./build-all.sh` 또는 `./build-clean.sh` 사용 권장

## 1. 전체 호출 흐름

### **실제 CT 로딩 흐름 (Module Federation 기반)**

**실제 확인된 호출 흐름**:

```
1. 썸네일 클릭
   examples/host-app/src/Components/ThumbnailList.tsx
   → handleClickThumbnail (examples/host-app/src/Components/Viewer.tsx)

// 이후는 packages/core 라이브러리에서 처리

2. updateActivatedDialogContent (Module Federation을 통해 호출)
   packages/core/src/externalHandler/index.ts (expose된 함수)
   → packages/core/src/workSpace/store/handler.ts:updateActivatedDialogContent
   → packages/core/src/workSpace/content/handler/ContentHandlerFactory.ts:addHandler
   → packages/core/src/workSpace/content/handler/CTContentHandler.ts (생성자)
   → 스토어 업데이트

3. CTContent 컴포넌트 생성 및 렌더링
   packages/core/src/workSpace/content/components/ctContent/index.tsx
   → packages/core/src/workSpace/content/hooks/useCTContent.ts

4. CTContentHandler.load() 시작
   packages/core/src/workSpace/content/handler/CTContentHandler.ts:load
   → examples/host-app/src/mocks/ContentIODummy.ts:fetch
   → CTDataType.blobObject 결정 (기존 방식)
   → convertToBlob(image) + getMetaDataToString(metaData)

5. refApis.current.loadCT 호출 (명확히 추적 가능한 마지막 지점)
   packages/core/src/workSpace/content/handler/CTContentHandler.ts:241
   ```typescript
   await this.refApis.current.loadCT(
     imageBlob,                    // Blob 데이터
     CTDataType.blobObject,        // 기존 방식
     { onStepChanged, onProgressChanged },
     metaDataString,
   );

// 이후는 lib/react-vtkjs 라이브러리에서 처리

6. ESVtkCTViewerContainer.loadCT 호출
   lib/react-vtkjs/src/components/ESVtkCTViewerContainer.tsx:190-230
   → React ref를 통해 CTViewerController 인스턴스에 접근
   → ctrRef.current.loadCT() 호출

7. CTViewerController.loadCT 호출
   lib/react-vtkjs/src/components/CTViewerController.tsx:335-410
   → CTDataType에 따른 데이터 검증 (blobObject vs fileObject)
   → loadVolume(data, type, progressCB) 호출
   → 결과로 받은 imageData, volumeData를 viewerControllerCore.setVolume() 설정
   → viewerControllerCore.render() 실행
   → VolumeLoadingState.Finished 상태 변경

8. loadVolume 함수 호출
   lib/vtkjs-wrapper/src/common/utility/loadVolume.ts:285-310
   → CTDataType에 따른 분기 처리:
   - CTDataType.blobObject → loadVolumeZippedBlob(data, callbackAPIs)
   - CTDataType.fileObject → loadVolumeFileList(data, callbackAPIs)
     → IResultLoadingDicom 결과 반환

// 이후는 실제 VTK.js 처리

9. VTK.js 내부 처리 (실제 압축 해제 및 DICOM 로딩)
   lib/vtkjs-wrapper/src/common/utility/loadVolume.ts
   - CTDataType.blobObject: loadVolumeZippedBlob → unzipCT → LoadDicomFiles
   - CTDataType.fileObject: loadVolumeFileList → LoadDicomFiles (압축 해제 건너뛰기)
   - VolumeLoadingState: downloading → ready → decompressing → dicom loading → finished

10. LoadDicomFiles 호출 (VTK ImageData 생성)
    lib/vtkjs-wrapper/src/io/Dicoms/index.ts:LoadDicomFiles
    → for await 루프로 각 POC DICOM 파일 순차 처리 (399개)
    → **loadDicom(es-dicom 라이브러리)** 호출하여 DICOM 헤더 및 픽셀 데이터 파싱
    → DicomFile 객체 생성 및 dicomFiles 배열에 추가 (399개 DicomFile[])
    → selectDICOMSeries로 시리즈 선택, PatientInfo/AcquisitionInfo 생성

12. VolumeDataGenerator.generate 호출 (복셀 데이터 생성)
    lib/vtkjs-wrapper/src/io/Dicoms/generator/volumeData.ts:generateVolumeData
    → generateDICOMInfo, generateDataType, generatePixelValueTransformation
    → generatePixelOrientation, generatePixelSpacing, generatePixelDimension
    → **generateVoxelData**: 핵심 복셀 배열 생성 (512×512×399×2bytes = 200MB)
    → generateVOILUT로 윈도우 레벨/폭 설정

13. convertVolumeDataToVTKImageData 호출 (VTK 형식 변환)
    lib/vtkjs-wrapper/src/io/Dicoms/common/utils.ts:convertVolumeDataToVTKImageData
    → vtkImageData.newInstance() 생성
    → setDimensions([512, 512, 399]), setSpacing(픽셀간격) 설정
    → vtkDataArray.newInstance로 복셀 데이터 연결 (values: volumeData.voxel)
    → **최종 VTK ImageData 반환** (VTK 렌더링 준비 완료)

14. CTViewerControllerCore.setVolume 호출 (VTK 렌더링 파이프라인 초기화)
    lib/vtkjs-wrapper/src/core/CTViewerControllerCore.ts:setVolume
    → VolumeObjectManager.initialize(imageData, volumeData, patientInfo, acquisitionInfo)
    → VolumeObject3D.setInputData(imageData), VolumeObject2D.setInputData(imageData)
    → **vtkVolumeMapper.setInputData(imageData)** 호출로 VTK 파이프라인 연결
    → render() 호출로 **최종 CT 4분할 화면 렌더링 완료**

```

**6-9번 단계별 세부 설명**:

### **6번: ESVtkCTViewerContainer.loadCT**

- **역할**: React 컴포넌트와 VTK 컨트롤러 사이의 브리지
- **주요 기능**:
    - React ref를 통해 CTViewerController 인스턴스에 접근
    - 데이터와 타입을 하위 컨트롤러로 전달
    - 컴포넌트 생명주기 관리

### **7번: CTViewerController.loadCT**

- **역할**: VTK 데이터 로딩의 핵심 오케스트레이터
- **주요 기능**:
    - CTDataType에 따른 데이터 검증 (blobObject vs fileObject)
    - loadVolume 함수 호출 및 결과 처리
    - VTK 렌더링 파이프라인 초기화 (setVolume, render)
    - VolumeLoadingState 상태 관리

### **8번: loadVolume 함수**

- **역할**: CTDataType에 따른 로딩 방식 분기 처리
- **주요 기능**:
    - CTDataType.blobObject → loadVolumeZippedBlob (압축 해제 필요)
    - CTDataType.fileObject → loadVolumeFileList (압축 해제 불필요)
    - 통일된 IResultLoadingDicom 결과 반환

### **9번: VTK.js 내부 처리**

- **blobObject 경로**: ZIP → unzipCT → DICOM Blob[] → LoadDicomFiles → VTK ImageData
- **fileObject 경로**: FileList → LoadDicomFiles → VTK ImageData (압축 해제 건너뛰기)
- **상태 변화**: downloading → ready → [decompressing] → dicom loading → finished
- **최종 결과**: CT 4분할 화면 렌더링 완료

**핵심 발견**:

- **실제 호출 흐름이 명확히 추적됨** (6→7→8→9번 순서)
- **CTDataType에 따른 분기 처리가 핵심** (blobObject vs fileObject)
- **POC에서는 fileObject 경로로 압축 해제 단계 완전 건너뛰기**
- **VTK 렌더링 파이프라인이 체계적으로 구성됨** (setVolume → render)

### **POC1에서 download부터 VTK.js 렌더링까지 (Stream Unzip 방식)**

**POC1 실제 호출 흐름 (기존 1-5단계 완전 대체)**:

```
1. POC1 Download 버튼 클릭
   examples/host-app/src/Components/POCTab.tsx:handleDownload
   → StreamingDownloader.startDownload() (examples/host-app/src/utils/streamingDownload.ts)

2. 스트리밍 다운로드 + 실시간 압축 해제 (기존 시스템 우회)
   API 엔드포인트: http://api.stream-zip.poc.scp.esclouddev.com:3001/download
   → Fetch API ReadableStream으로 청크 단위 다운로드
   → fflate.Unzip으로 실시간 압축 해제
   → onFileExtracted 콜백으로 DICOM 파일들 수집
   → downloadedDicomFiles 배열 완성 (399개 파일)

3. FileList 변환 및 POC1 콘텐츠 생성
   examples/host-app/src/Components/POCTab.tsx:loadVTKVolumeWithFileObject
   → DICOM files → File[] → DataTransfer → FileList 변환
   → POC1 콘텐츠 생성 (id: POC_CT_STREAMUNZIP_${timestamp})
   → examples/host-app/src/mocks/ContentIODummy.ts:setPOCFileList

4. 기존 시스템과 연동 (updateActivatedDialogContent 호출)
   examples/host-app/src/Components/POCTab.tsx
   → updateActivatedDialogContent(pocContent) 호출
   → packages/core/src/workSpace/store/handler.ts:updateActivatedDialogContent
   → packages/core/src/workSpace/content/handler/ContentHandlerFactory.ts:addHandler
   → packages/core/src/workSpace/content/handler/CTContentHandler.ts (생성자)

5. POC1 CTContentHandler.load() - CTDataType.fileObject 사용
   packages/core/src/workSpace/content/handler/CTContentHandler.ts:load
   → examples/host-app/src/mocks/ContentIODummy.ts:fetch (POC1 ID 감지)
   → CTDataType.fileObject 결정 (POC1 방식) ← 핵심 차이점!
   → FileList 직접 전달 (압축 해제 단계 건너뛰기)

6. refApis.current.loadCT 호출 (CTDataType.fileObject)
   packages/core/src/workSpace/content/handler/CTContentHandler.ts
   → pocFileList (FileList 데이터, 압축 해제 불필요!)
   → CTDataType.fileObject (POC1 방식)
   → { onStepChanged, onProgressChanged }, metaDataString

// 이후는 lib/react-vtkjs 라이브러리에서 처리

7. POC1 ESVtkCTViewerContainer.loadCT 호출
   lib/react-vtkjs/src/components/ESVtkCTViewerContainer.tsx:190-230
   → POC1 FileList (399개 DICOM 파일)와 CTDataType.fileObject로 호출
   → ctrRef.current.loadCT() 호출

8. POC1 CTViewerController.loadCT 호출
   lib/react-vtkjs/src/components/CTViewerController.tsx:335-410
   → POC1 FileList 데이터 검증 (length > 0)
   → loadVolume(pocFileList, CTDataType.fileObject, progressCB) 호출
   → 결과로 받은 imageData, volumeData를 viewerControllerCore.setVolume() 설정
   → viewerControllerCore.render() 실행

9. POC1 loadVolume 함수 호출 (CTDataType.fileObject 경로)
   lib/vtkjs-wrapper/src/common/utility/loadVolume.ts:285-310
   → CTDataType.fileObject 경로 선택
   → loadVolumeFileList(pocFileList, callbackAPIs) 호출

// 이후는 실제 VTK.js 처리

10. POC1 VTK.js 내부 처리 (압축 해제 건너뛰기)
    lib/vtkjs-wrapper/src/common/utility/loadVolume.ts
    → loadVolumeFileList → LoadDicomFiles (압축 해제 건너뛰기!)
    → VolumeLoadingState: downloading → ready → **dicom loading** (decompressing 건너뛰기!) → finished

11. POC1 readDICOMFiles 호출 (DICOM 파일별 파싱)
    lib/vtkjs-wrapper/src/io/Dicoms/index.ts:readDICOMFiles
    → for await 루프로 각 POC1 DICOM 파일 순차 처리 (399개)
    → **loadDicom(es-dicom 라이브러리)** 호출하여 DICOM 헤더 및 픽셀 데이터 파싱
    → DicomFile 객체 생성 및 dicomFiles 배열에 추가 (399개 DicomFile[])
    → selectDICOMSeries로 시리즈 선택, PatientInfo/AcquisitionInfo 생성

12. POC1 VolumeDataGenerator.generate 호출 (복셀 데이터 생성)
    lib/vtkjs-wrapper/src/io/Dicoms/generator/volumeData.ts:generateVolumeData
    → generateDICOMInfo, generateDataType, generatePixelValueTransformation
    → generatePixelOrientation, generatePixelSpacing, generatePixelDimension
    → **generateVoxelData**: 핵심 복셀 배열 생성 (512×512×399×2bytes = 200MB)
    → generateVOILUT로 윈도우 레벨/폭 설정

13. POC1 convertVolumeDataToVTKImageData 호출 (VTK 형식 변환)
    lib/vtkjs-wrapper/src/io/Dicoms/common/utils.ts:convertVolumeDataToVTKImageData
    → vtkImageData.newInstance() 생성
    → setDimensions([512, 512, 399]), setSpacing(픽셀간격) 설정
    → vtkDataArray.newInstance로 복셀 데이터 연결 (values: volumeData.voxel)
    → **최종 VTK ImageData 반환** (VTK 렌더링 준비 완료)

14. POC1 CTViewerControllerCore.setVolume 호출 (VTK 렌더링 파이프라인 초기화)
    lib/vtkjs-wrapper/src/core/CTViewerControllerCore.ts:setVolume
    → VolumeObjectManager.initialize(imageData, volumeData, patientInfo, acquisitionInfo)
    → VolumeObject3D.setInputData(imageData), VolumeObject2D.setInputData(imageData)
    → **vtkVolumeMapper.setInputData(imageData)** 호출로 VTK 파이프라인 연결
    → render() 호출로 **최종 CT 4분할 화면 렌더링 완료**

```

### **POC2에서 download부터 VTK.js 렌더링까지 (Stream Unzip + DICOM Parsing 방식)**

**POC2 실제 호출 흐름 (POC1 대비 2,11번 단계 개선)**:

```
1. POC2 Download 버튼 클릭
   examples/host-app/src/Components/POCTab.tsx:handleDownloadPOC2
   → ProgressiveVolumeLoader.startDownload() (examples/host-app/src/utils/progressiveVolumeLoader.ts)

2. 스트리밍 다운로드 + 실시간 압축 해제 + 동시 DICOM 파싱 (기존 시스템 우회)
   API 엔드포인트: http://api.stream-zip.poc.scp.esclouddev.com:3001/download
   → Fetch API ReadableStream으로 청크 단위 다운로드
   → fflate.Unzip으로 실시간 압축 해제
   → **onFileExtracted 콜백에서 즉시 DICOM 파싱 수행** ← 핵심 개선!
   → loadDicom(es-dicom) 실시간 호출로 DicomFile 객체 생성
   → downloadedDicomFiles 배열 완성 (399개 DicomFile[])

3. DicomList 변환 및 POC2 콘텐츠 생성
   examples/host-app/src/Components/POCTab.tsx:loadVTKVolumeWithDicomObject
   → DicomFile[] → DicomList 변환
   → POC2 콘텐츠 생성 (id: POC_CT_STREAMDICOM_${timestamp})
   → examples/host-app/src/mocks/ContentIODummy.ts:setPOCDicomList

4. 기존 시스템과 연동 (updateActivatedDialogContent 호출)
   examples/host-app/src/Components/POCTab.tsx
   → updateActivatedDialogContent(poc2Content) 호출
   → packages/core/src/workSpace/store/handler.ts:updateActivatedDialogContent
   → packages/core/src/workSpace/content/handler/ContentHandlerFactory.ts:addHandler
   → packages/core/src/workSpace/content/handler/CTContentHandler.ts (생성자)

5. POC2 CTContentHandler.load() - CTDataType.dicomObject 사용
   packages/core/src/workSpace/content/handler/CTContentHandler.ts:load
   → examples/host-app/src/mocks/ContentIODummy.ts:fetch (POC2 ID 감지)
   → CTDataType.dicomObject 결정 (POC2 방식) ← 핵심 차이점!
   → DicomList 직접 전달 (압축 해제 + DICOM 파싱 단계 완전 건너뛰기)

6. refApis.current.loadCT 호출 (CTDataType.dicomObject)
   packages/core/src/workSpace/content/handler/CTContentHandler.ts
   → pocDicomList (DicomList 데이터, 압축 해제 + DICOM 파싱 불필요!)
   → CTDataType.dicomObject (POC2 방식)
   → { onStepChanged, onProgressChanged }, metaDataString

// 이후는 lib/react-vtkjs 라이브러리에서 처리

7. POC2 ESVtkCTViewerContainer.loadCT 호출
   lib/react-vtkjs/src/components/ESVtkCTViewerContainer.tsx:190-230
   → POC2 DicomList (399개 DicomFile)와 CTDataType.dicomObject로 호출
   → ctrRef.current.loadCT() 호출

8. POC2 CTViewerController.loadCT 호출
   lib/react-vtkjs/src/components/CTViewerController.tsx:335-410
   → POC2 DicomList 데이터 검증 (length > 0)
   → loadVolume(pocDicomList, CTDataType.dicomObject, progressCB) 호출
   → 결과로 받은 imageData, volumeData를 viewerControllerCore.setVolume() 설정
   → viewerControllerCore.render() 실행

9. POC2 loadVolume 함수 호출 (CTDataType.dicomObject 경로)
   lib/vtkjs-wrapper/src/common/utility/loadVolume.ts:285-310
   → CTDataType.dicomObject 경로 선택 (새로운 분기)
   → loadVolumeDicomList(pocDicomList, callbackAPIs) 호출

// 이후는 실제 VTK.js 처리

10. POC2 VTK.js 내부 처리 (압축 해제 + DICOM 파싱 모두 건너뛰기)
    lib/vtkjs-wrapper/src/common/utility/loadVolume.ts
    → loadVolumeDicomList → LoadDicomFiles (압축 해제 + DICOM 파싱 모두 건너뛰기!)
    → VolumeLoadingState: downloading → ready → **volume generating** (decompressing, dicom loading 모두 건너뛰기!) → finished

11. POC2 readDICOMFiles 호출 (DICOM 파싱 스킵)
    lib/vtkjs-wrapper/src/io/Dicoms/index.ts:readDICOMFiles
    → CTDataType.dicomObject 감지 시 **파싱 과정 완전 스킵**
    → 이미 파싱된 DicomFile[] 직접 사용 (399개)
    → selectDICOMSeries로 시리즈 선택, PatientInfo/AcquisitionInfo 생성

12. POC2 VolumeDataGenerator.generate 호출 (복셀 데이터 생성)
    lib/vtkjs-wrapper/src/io/Dicoms/generator/volumeData.ts:generateVolumeData
    → generateDICOMInfo, generateDataType, generatePixelValueTransformation
    → generatePixelOrientation, generatePixelSpacing, generatePixelDimension
    → **generateVoxelData**: 핵심 복셀 배열 생성 (512×512×399×2bytes = 200MB)
    → generateVOILUT로 윈도우 레벨/폭 설정

13. POC2 convertVolumeDataToVTKImageData 호출 (VTK 형식 변환)
    lib/vtkjs-wrapper/src/io/Dicoms/common/utils.ts:convertVolumeDataToVTKImageData
    → vtkImageData.newInstance() 생성
    → setDimensions([512, 512, 399]), setSpacing(픽셀간격) 설정
    → vtkDataArray.newInstance로 복셀 데이터 연결 (values: volumeData.voxel)
    → **최종 VTK ImageData 반환** (VTK 렌더링 준비 완료)

14. POC2 CTViewerControllerCore.setVolume 호출 (VTK 렌더링 파이프라인 초기화)
    lib/vtkjs-wrapper/src/core/CTViewerControllerCore.ts:setVolume
    → VolumeObjectManager.initialize(imageData, volumeData, patientInfo, acquisitionInfo)
    → VolumeObject3D.setInputData(imageData), VolumeObject2D.setInputData(imageData)
    → **vtkVolumeMapper.setInputData(imageData)** 호출로 VTK 파이프라인 연결
    → render() 호출로 **최종 CT 4분할 화면 렌더링 완료**

```

## 🔑 핵심 차이점 비교표

| **1-2단계** | 썸네일 클릭 → 즉시 핸들러 생성 | POC1 버튼 → 스트리밍 다운로드 + 실시간 압축 해제 | POC2 버튼 → 스트리밍 다운로드 + 실시간 압축 해제 + 동시 DICOM 파싱 |
| --- | --- | --- | --- |
| **3단계** | ContentIODummy에서 Blob 로딩 | FileList 변환 + POC1 콘텐츠 생성 | DicomList 변환 + POC2 콘텐츠 생성 |
| **4-5단계** | 기존 콘텐츠로 핸들러 생성 → CTDataType.blobObject | POC1 콘텐츠로 핸들러 생성 → **CTDataType.fileObject** | POC2 콘텐츠로 핸들러 생성 → **CTDataType.dicomObject** |
| **6단계** | refApis.loadCT(blob, blobObject) | refApis.loadCT(fileList, fileObject) | refApis.loadCT(dicomList, dicomObject) |
| **7-8단계** | ESVtkCTViewerContainer → CTViewerController | 동일한 경로 | 동일한 경로 |
| **9단계** | loadVolume → loadVolumeZippedBlob | loadVolume → **loadVolumeFileList** | loadVolume → **loadVolumeDicomList** |
| **10단계 (VTK 내부)** | unzipCT → LoadDicomFiles | **LoadDicomFiles 직접 호출** (압축 해제 건너뛰기!) | **LoadDicomFiles 직접 호출** (압축 해제 + DICOM 파싱 건너뛰기!) |
| **11단계 (DICOM 파싱)** | readDICOMFiles로 DICOM 파싱 수행 | readDICOMFiles로 DICOM 파싱 수행 | **파싱 과정 완전 스킵** (이미 파싱 완료) |
| **12-14단계** | VolumeDataGenerator → convertVolumeDataToVTKImageData → setVolume | 동일한 경로 | 동일한 경로 |
| **VolumeLoadingState** | downloading → ready → **decompressing** → dicom loading → finished | downloading → ready → **dicom loading** → finished (decompressing 스킵!) | downloading → ready → **volume generating** → finished (decompressing, dicom loading 모두 스킵!) |
| **압축 해제 처리** | VTK 내부에서 ZIP 압축 해제 수행 | **사전에 스트리밍으로 압축 해제 완료** | **사전에 스트리밍으로 압축 해제 완료** |
| **DICOM 파싱 처리** | VTK 내부에서 DICOM 파싱 수행 | VTK 내부에서 DICOM 파싱 수행 | **사전에 스트리밍과 동시에 DICOM 파싱 완료** |
| **메모리 사용** | **ZIP Blob + 압축해제 Blob[] + 파싱 DicomFile[] + VTK Volume** | **압축해제 File[] + 파싱 DicomFile[] + VTK Volume** | **파싱 DicomFile[] + VTK Volume** |
| **성능 개선** | 기준점 (약 30초) | 목표 33% 단축 (약 20초) | 목표 40% 단축 (약 18초) |

**핵심 차이점**:

- **기존**: ZIP 다운로드 → VTK 내부 압축 해제 → VTK 내부 DICOM 파싱 → VTK 볼륨 생성 (순차 처리)
- **POC1**: 스트리밍 압축 해제 → FileList 직접 전달 → VTK 내부 DICOM 파싱 → VTK 볼륨 생성 (압축 해제 단계 건너뛰기)
- **POC2**: 스트리밍 압축 해제와 동시 DICOM 파싱 → DicomList 직접 전달 → VTK 볼륨 생성 (압축 해제 + DICOM 파싱 단계 모두 건너뛰기)

### **메모리 사용 패턴 상세 분석**

**기존 방식 (4단계 메모리 중첩)**:

1. **ZIP Blob** (148MB) - 전체 ZIP 파일
2. **압축해제된 Blob[]** (399개 × 평균 500KB = 200MB) - unzipCT 결과
3. **파싱된 DicomFile[]** (399개 × 평균 600KB = 240MB) - loadDicom(es-dicom) 결과
4. **최종 VTK Volume** (512×512×399×2bytes = 200MB) - vtkImageData

**총 메모리 사용량**: ~788MB (동시 보유)

**POC1 방식 (3단계 메모리 중첩)**:

1. ~~ZIP Blob~~ (스트리밍으로 제거)
2. **압축해제된 File[]** (399개 × 평균 500KB = 200MB) - 스트리밍 압축해제 결과
3. **파싱된 DicomFile[]** (399개 × 평균 600KB = 240MB) - loadDicom(es-dicom) 결과
4. **최종 VTK Volume** (512×512×399×2bytes = 200MB) - vtkImageData

**총 메모리 사용량**: ~640MB (동시 보유)

**메모리 절약량**: 148MB (ZIP Blob 제거) = **약 19% 절약**

**POC2 방식 (2단계 메모리 중첩)**:

1. ~~ZIP Blob~~ (스트리밍으로 제거)
2. ~~압축해제된 File[]~~ (스트리밍과 동시에 DICOM 파싱으로 제거)
3. **파싱된 DicomFile[]** (399개 × 평균 600KB = 240MB) - 스트리밍 중 실시간 DICOM 파싱 결과
4. **최종 VTK Volume** (512×512×399×2bytes = 200MB) - vtkImageData

**총 메모리 사용량**: ~440MB (동시 보유)

**메모리 절약량**: 348MB (ZIP Blob + File[] 제거) = **약 44% 절약**

### **미래 최적화 가능성**

**이론적 완전 스트리밍 처리 (1단계 메모리만 사용)**:

- 스트리밍 압축해제 → 즉시 DICOM 파싱 → 즉시 VTK Volume 업데이트 → 점진적 렌더링
- **최종 VTK Volume**만 메모리에 보유 (200MB)
- **총 메모리 절약량**: 588MB = **약 75% 절약**