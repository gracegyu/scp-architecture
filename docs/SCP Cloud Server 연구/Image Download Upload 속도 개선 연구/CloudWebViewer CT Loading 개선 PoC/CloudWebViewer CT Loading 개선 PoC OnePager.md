# Engineering One Pager

## Project Name

CloudWebViewer CT Loading 개선 POC (Streaming-based CT Data Loading)

## Date

2025.05.18

## Submitter Info

**제출자**: Jeon Gyuhyeon <raymond.jeon@ewoosoft.com>
**프로젝트**: https://dev.azure.com/ewoosoft/cloudwebviewer
**브랜치**: StreamPOC

## Project Description

CloudWebViewer에서 CT 데이터 로딩 성능을 개선하기 위한 스트리밍 기반 로딩 방식의 검증 및 구현 프로젝트입니다.

**현재 상황 (As-Is)**:

- 처리 과정: zip 다운로드 완료 → 압축 해제 → 볼륨 로딩 (순차 처리)
- 소요 시간: 약 30초
- 문제점: 메모리 사용량 증가, 로딩 지연, 사용자 대기 시간 길음

## POC 개선 목표

본 POC는 **"속도 개선"** 과 **"체감 개선"** 두 가지 핵심 목표로 구성됩니다.

### 목표 1: 속도 개선 (Performance Optimization)

**우선순위**: 최우선 (필수 달성)

#### POC1: Stream Unzip 방식 (메모리 15% 절약)

- **처리 과정**: 스트리밍 다운로드 + 실시간 압축 해제 (fflate) + 기존 DICOM 파싱
- **개선 효과**: 메모리 사용량 15% 절약, ZIP Blob 제거
- **목표 시간**: 약 25초 (17% 단축)

#### POC2: Stream Unzip + DICOM Parsing 방식 (메모리 40% 절약)

- **처리 과정**: 스트리밍 다운로드 + 실시간 압축 해제 + 실시간 DICOM 파싱
- **개선 효과**: 메모리 사용량 40% 절약, 중간 파일 버퍼 제거
- **목표 시간**: 약 20초 (33% 단축)

![POC 속도 개선 단계](images/poc.png)

### 목표 2: 체감 개선 (User Experience Enhancement)

**우선순위**: 상황에 따라 진행 (선택적 달성)

#### 1안: VTK 3D 볼륨이 자라는 효과 (최우선)

- **구현 방식**: VTK.js 네이티브 점진적 볼륨 로딩
- **사용자 체감**: CT 슬라이스가 Z축 방향으로 점진적으로 쌓이는 3D 효과
- **기술적 복잡도**: 높음
- **호환성**: 기존 VTK 시스템과 완벽 통합

#### 2안: Simple 3D 볼륨이 자라는 효과 (대안 1)

- **구현 방식**: Three.js 또는 별도 3D 엔진 사용
- **사용자 체감**: 단순한 3D 볼륨 점진적 표시 후 VTK로 전환
- **기술적 복잡도**: 중간
- **호환성**: 별도 Dialog 사용

#### 3안: 2.5D 볼륨이 자라는 효과 (대안 2)

- **구현 방식**: Canvas 2D + 기울임 효과로 3D 시뮬레이션
- **사용자 체감**: 2.5D 적층 효과로 3D처럼 보이는 시각적 피드백
- **기술적 복잡도**: 낮음
- **호환성**: 구현 안정성 높음

#### 4안: Gauge Bar (최후 대안)

- **구현 방식**: 기존 진행률 표시 개선
- **사용자 체감**: 상세한 단계별 진행률 표시
- **기술적 복잡도**: 매우 낮음
- **호환성**: 기존 시스템 그대로 사용

## 구현 계획 및 전략

### Phase 1: 속도 개선 (Performance Optimization) - 필수 달성

#### **POC1: Stream Unzip 방식**

**목표**: 기존 순차 처리 방식을 스트리밍 병렬 처리로 개선

**구현 내용**:

- CT Download → 스트리밍으로 압축 해제
- API 엔드포인트를 통한 실시간 zip 다운로드
- fflate streaming mode를 활용한 실시간 압축 해제
- X-Total-Files 헤더 기반 진행률 표시
- CTDataType.fileObject 방식으로 압축 해제 단계 건너뛰기

**기대 효과**:

- 스트리밍 다운로드 (399개 DICOM 파일)
- 실시간 압축 해제 및 DICOM 파일 추출
- 메모리 사용량 15% 절약 (ZIP Blob 제거)
- Stream 모드 vs Batch 모드 성능 비교 시스템

#### **POC2: Stream Unzip + DICOM Parsing 방식**

**목표**: DICOM 파싱도 스트리밍으로 처리하여 추가 성능 향상

**구현 내용**:

- 스트리밍 압축 해제와 동시에 DICOM 파싱 수행
- 중간 File 객체 생성 없이 직접 VTK ImageData로 변환
- 메모리 사용량 추가 절약 (File 버퍼 제거)
- 실시간 볼륨 데이터 구성

**기대 효과**:

- 메모리 사용량 40% 절약
- 처리 시간 33% 단축 (30초 → 20초)
- CPU 사용률 최적화

### Phase 2: 체감 개선 (User Experience Enhancement) - 상황에 따라 진행

**우선순위**: 속도 개선 완료 후 진행, 기술적 가능성에 따라 선택적 구현

#### **1안: VTK 3D 볼륨이 자라는 효과**

**구현 방식**: VTK.js 네이티브 점진적 볼륨 로딩

**플로우**:

```
스트리밍 DICOM 파싱 → 빈 3D 볼륨 사전 생성 (HU -1000)
→ 슬라이스별 VTK Volume 실시간 업데이트
→ modified() + render() 호출로 점진적 렌더링
→ VTK.js 3D 볼륨이 Z축 방향으로 점진적으로 자라는 효과
```

**장점**:

- 기존 뷰어 시스템과 완벽 통합
- 진정한 3D 점진적 렌더링
- 최고의 사용자 경험

**기술적 복잡도**: 높음 (VTK.js Volume 부분 업데이트, interactor 초기화 이슈)

#### **2안: Simple 3D 볼륨이 자라는 효과**

**구현 방식**: Three.js 또는 별도 3D 엔진 사용

**플로우**:

```
스트리밍 DICOM 파싱 → Three.js 3D 점진적 Preview
→ 완료 후 VTK.js 뷰어로 전환
→ 최종 CT 4분할 화면 표시
```

**장점**:

- 별도 Dialog에서 점진적 Preview 제공
- 최종 결과는 기존 VTK.js 뷰어 활용
- 구현 안정성 확보

**기술적 복잡도**: 중간 (별도 3D 엔진 연동)

#### **3안: 2.5D 볼륨이 자라는 효과**

**구현 방식**: Canvas 2D + 기울임 효과로 3D 시뮬레이션

**플로우**:

```
스트리밍 DICOM 파싱 → Canvas에 CT slice를 기울여서 적층 표시
→ Z축 방향으로 슬라이스가 점진적으로 추가
→ 2.5D 효과로 3D처럼 보이는 시각적 피드백
```

**장점**:

- Canvas 구현으로 안정성 확보
- 2.5D 효과로 3D처럼 보이는 시각적 효과
- 구현 복잡도 낮음

**기술적 복잡도**: 낮음 (Canvas 2D API 사용)

#### **4안: Gauge Bar**

**구현 방식**: 기존 진행률 표시 개선

**플로우**:

```
스트리밍 DICOM 파싱 → 상세한 단계별 진행률 표시
→ 다운로드/압축해제/DICOM파싱/VTK로딩 각 단계별 진행률
→ 사용자에게 명확한 진행 상황 전달
```

**장점**:

- 기존 시스템 그대로 사용
- 구현 안정성 매우 높음
- 즉시 적용 가능

**기술적 복잡도**: 매우 낮음 (UI 개선만)

## 구현 계획

### 우선순위 1: POC2 속도 개선 (필수 달성)

**목표**: 처리 시간 33% 단축 (30초 → 20초)

**구현 계획**:

1. **스트리밍 DICOM 파싱**

   - File 객체 생성 없이 직접 VTK ImageData 변환
   - 메모리 사용량 추가 40% 절약

2. **실시간 볼륨 구성**
   - DICOM 파싱과 동시에 VTK Volume 데이터 구성
   - 중간 버퍼 제거로 메모리 최적화

### 우선순위 2: 체감 개선 (선택적 달성)

**진행 방식**: 속도 개선 완료 후, 기술적 가능성에 따라 순차 시도

1. **1안 시도**: VTK 3D 볼륨이 자라는 효과

   - 기술적 복잡도 높음, 최고의 사용자 경험
   - VTK.js Volume 부분 업데이트 검증 필요

2. **대안 준비**: 2안 → 3안 → 4안 순서로 fallback
   - 구현 가능성에 따라 적절한 수준의 체감 개선 적용

## Business and Marketing Justification

None

## Risk Assessment

### 기술적 위험 (Medium)

**위험**: VTK.js에서 Volume 점진적 업데이트 미지원 가능성

- **확률**: 50%
- **영향도**: Medium (대안 방식으로 대응 가능)
- **대응 방안**: 4단계 대안 방식 순차 적용

### 전체 위험도: **Medium**

- 1단계는 검증된 기술로 위험도 낮음
- 2단계는 4개 대안으로 실패 위험 최소화
- 최악의 경우에도 대안으로 최소 목표 달성 가능

## Resource and Scheduling Details

### 인력 계획

- **개발자**: 1명 (Full-time)
- **기간**: 3주

### 일정 계획

**1주차 (POC1: Stream Unzip 방식)**:

- Day 1-2: 스트리밍 다운로드 시스템 구현
- Day 3-4: 실시간 압축 해제 및 FileList 변환 구현
- Day 5: POC1 성능 측정 및 검증

**2주차 (POC2: Stream Unzip + DICOM Parsing 방식)**:

- Day 1-2: 스트리밍 DICOM 파싱 시스템 구현
- Day 3-4: 실시간 볼륨 구성 및 메모리 최적화
- Day 5: POC2 성능 측정 및 POC1 대비 개선 효과 검증

**3주차 (체감 개선 및 완성)**:

- Day 1-2: VTK 점진적 볼륨 렌더링 구현 (1안 시도)
- Day 3-4: 1안 실패 시 대안 구현, 성공 시 최적화
- Day 5: 최종 성능 검증 및 문서화

## Technical Description

### 시스템 아키텍처

**현재 호출 흐름**:

```
core/CTContentHandler:load
→ examples/host-app/ioInstance:fetch
→ lib/react-vtkjs/CTViewerControllerFN:loadCT
→ lib/vtkjs-wrapper/loadVolume
```

**개선된 호출 흐름**:

```
core/CTContentHandler:load
→ examples/host-app/ioInstance:streamingFetch (NEW)
→ lib/react-vtkjs/CTViewerControllerFN:progressiveLoadCT (MODIFIED)
→ lib/vtkjs-wrapper/progressiveLoadVolume (NEW)
```

### 기술 스택

- **Frontend**: React, TypeScript, VTK.js
- **Streaming**: Fetch API with ReadableStream
- **Compression**: fflate (streaming mode)
- **Data Format**: DICOM
- **Rendering**: VTK.js Volume Rendering (1안), Three.js/Canvas (대안)

### 데이터 소스

**API 엔드포인트** (실제 사용):

- CT01: http://api.stream-zip.poc.scp.esclouddev.com:3002/download?filename=download20250618-115114.zip&s3Uri=s3%3A%2F%2Fstream-zip-hi-data%2Fdownload%2FCT01%2F
- CT02: http://api.stream-zip.poc.scp.esclouddev.com:3002/download?filename=download20250618-115114.zip&s3Uri=s3%3A%2F%2Fstream-zip-hi-data%2Fdownload%2FCT02%2F

**중요 기술 요소**:

- HTTP Header `X-Total-Files`를 통한 전체 파일 개수 확인
- ReadableStream을 활용한 청크 단위 데이터 처리
- fflate streaming mode를 통한 실시간 압축 해제
- VTK.js Volume의 점진적 업데이트 검증

### 구현 세부사항

**1단계: 스트리밍 다운로드**

- http2-client/DownloadPage.tsx의 검증된 로직 활용
- Fetch API ReadableStream으로 청크 단위 다운로드
- fflate를 통한 실시간 압축 해제
- 진행률 표시 UI 구현

**2단계: 점진적 렌더링** (4개 대안 중 선택)

**2-1안 구현 방법**:

- DICOM 파일 순차 로딩 및 Volume 데이터 점진적 구성
- VTK.js Renderer의 실시간 업데이트
- 메모리 사용량 최적화 및 성능 튜닝

**대안 구현 방법**:

- 2-2안: Three.js 기반 3D Preview + VTK.js 최종 렌더링
- 2-3안: Canvas 2.5D Preview + VTK.js 최종 렌더링
- 2-4안: 스트리밍 압축 해제 + 기존 VTK.js 일괄 로딩

### 점진적 CT 로딩 구현 플로우

**1단계: 초기 Volume 구조 파악**

```
다운로드 시작 → X-Total-Files 헤더로 총 파일 수 확인 (예: 399개)
첫 번째 DICOM 파일 압축 해제 → DICOM 헤더에서 가로×세로 크기 파악 (예: 512×512)
전체 3D 볼륨 크기 계산: 512×512×399
VTK.js에서 빈 3D 볼륨 사전 생성 (HU -1000으로 초기화)
```

**2단계: 순차적 점진적 로딩**

```
DICOM 파일 압축 해제: 1, 2, 3... 순차적으로 Queue에 적재
동시에 VTK.js 3D 볼륨에 슬라이스별 데이터 실시간 업데이트:
  - 슬라이스 1 → VTK Volume[0] 업데이트 → 렌더링
  - 슬라이스 2 → VTK Volume[1] 업데이트 → 렌더링
  - 슬라이스 3 → VTK Volume[2] 업데이트 → 렌더링
  - ...
  - 슬라이스 399 → VTK Volume[398] 업데이트 → 최종 렌더링
```

**3단계: 사용자 체감 효과**

```
사용자가 화면에서 CT가 점진적으로 "자라나는" 것을 실시간으로 확인
Z축 방향으로 슬라이스가 하나씩 추가되면서 3D 볼륨이 완성되는 시각적 효과
```

**핵심 기술 요소**:

- VTK.js `vtkImageData` 사전 할당
- `scalars.set(sliceData, sliceOffset)` 슬라이스별 업데이트
- `volumeData.modified()` + `renderWindow.render()` 실시간 렌더링

### 성능 목표

- **전체 로딩 시간**: 30초 → 20초 (33% 개선)
- **첫 번째 이미지 표시**: 5초 이내
- **메모리 사용량**: 현재 대비 50% 이하 유지
- **사용자 인터페이스 반응성**: 로딩 중에도 유지

### 검증 기준

**기능 검증**:

- API 엔드포인트에서 zip 파일 스트리밍 다운로드 성공
- X-Total-Files 헤더를 통한 진행률 계산 정확성
- 실시간 압축 해제 및 DICOM 파일 순차 로딩
- CTDataType.fileObject 방식으로 VTK 연동
- 기존 기능과의 호환성 유지

**성능 검증**:

- Stream 모드 vs Batch 모드 성능 비교 시스템
- VolumeLoadingState 모니터링을 통한 정확한 측정 체계
- 메모리 사용량 절약 효과 측정
- 압축 해제 단계 건너뛰기로 성능 개선 효과 확인
- 최종 성능 목표 달성 여부 측정

### 구현 위치

- **대상 애플리케이션**: `/examples/host-app`
- **POC 구현**: `examples/host-app/Viewer.tsx` 좌측에 "POC" 탭 추가
- **기존 기능 유지**: 현재 더미 데이터 로딩 기능은 그대로 유지

**POC 탭 UI 구성 및 플로우**:

1. **CT 데이터 선택**: CT01, CT02 중 하나를 선택할 수 있는 라디오 버튼
2. **POC 모드 선택**: Stream 모드 vs Batch 모드 성능 비교
3. **실행 버튼**: 선택된 CT 데이터와 모드로 POC 실행 시작
4. **진행 상황 표시**:
   - 스트리밍 다운로드 진행률 (X-Total-Files 헤더 기반)
   - 실시간 압축 해제 진행률 (해제된 DICOM 파일 수)
   - VTK 로딩 상태 모니터링
5. **성능 측정 결과**: 단계별 소요 시간 및 메모리 사용량 표시
6. **VTK 렌더링**: CT 4분할 화면이 오른쪽 Viewer에 표시

**실행 플로우**:

```
사용자 액션: CT 선택 → Download 버튼 클릭
↓
시스템 처리: API 엔드포인트 스트리밍 다운로드 시작
↓
실시간 처리: zip 압축 해제 + DICOM 파일 순차 로딩
↓
점진적 렌더링: 선택된 방식으로 CT 이미지가 슬라이스별로 점진적 표시
↓
완료: 전체 CT 데이터 로딩 및 렌더링 완료
```

### 참고 자료

- **프로젝트 저장소**: https://dev.azure.com/ewoosoft/cloudwebviewer
- **선행 검증**: http2-client/DownloadPage.tsx
- **주요 스펙**: [Confidential_CloudWebViewer_v1.0_SRS.docx](./srs.md)
- **README**: https://dev.azure.com/ewoosoft/cloudwebviewer/_git/cloudwebviewer?path=/README.md&_a=preview
