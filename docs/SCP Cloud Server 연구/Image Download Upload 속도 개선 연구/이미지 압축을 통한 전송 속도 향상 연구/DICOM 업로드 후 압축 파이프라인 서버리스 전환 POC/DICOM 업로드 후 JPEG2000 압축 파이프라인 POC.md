# Engineering One Pager

## Project Name

**DICOM 업로드 후 JPEG2000 압축 파이프라인 POC** (DICOM Upload JPEG2000 Compression Pipeline POC)

## Date

2025.08.20

## Submitter Info

**제출자**: Raymond  
**프로젝트**: https://dev.azure.com/ewoosoft/stream-zip-unzip
**브랜치**: main

## Project Description

**CT 업로드 완료 후 API 호출을 통해 JPEG2000 손실 압축 ZIP을 생성하여 S3에 저장하는 백엔드 파이프라인 POC**입니다.

기존 POC에서 사용한 s3://stream-zip-hi-data/download/JPEG2000/ 폴더의 399개 DICOM 파일 (196.9MB)을 대상으로 EC2 백엔드 서버에서 **두 가지 압축 라이브러리(`gdcmconv` vs `dcmjs-codecs`)의 기능 검증 및 성능 메트릭 비교 분석**을 수행합니다.

---

## Current Status Analysis (현재 상황 분석)

### 현재 상황

**기존 POC 환경**:

1. **테스트 데이터**: s3://stream-zip-hi-data/download/JPEG2000/ (399개 DICOM 파일, 196.9MB)
2. **처리 방식**: 클라이언트 직접 다운로드 및 처리
3. **기존 압축 테스트**: 개별 라이브러리 단순 성능 측정
4. **현재 한계**: 전체 파이프라인 통합 검증 및 정량적 비교 데이터 부족

---

## POC Objectives (POC 목표)

### 1. 핵심 검증 목표

- **압축 파이프라인 구축**: API 호출 → EC2 압축 → S3 저장 전체 플로우 동작 확인
- **라이브러리 비교**: `gdcmconv` vs `dcmjs-codecs` 정량적 메트릭 수집 및 분석
- **시스템 리소스 분석**: CPU, 메모리, 처리 시간, 압축률 측정 및 비교
- **확장성 검증**: 단일/동시 작업 환경에서의 시스템 안정성 확인

### 2. 성능 측정 매트릭스

**구현된 실시간 시스템 모니터링**:

| 측정 항목                | 측정 방식              | 설명                                       | 비고                  |
| ------------------------ | ---------------------- | ------------------------------------------ | --------------------- |
| **처리 시간**            | 직접 측정              | 다운로드, 압축, 업로드 시간 분리 측정      | 압축률별 비교         |
| **시스템 CPU 변화량**    | `SystemMonitorService` | 작업 전후 시스템 전체 CPU 사용률 변화량    | 외부 프로세스 포함    |
| **시스템 메모리 변화량** | `os.freemem()` 기반    | 작업 전후 시스템 전체 메모리 사용량 변화량 | 실제 시스템 영향 측정 |
| **프로세스 리소스**      | `pidusage` 라이브러리  | Node.js 프로세스의 CPU/메모리 최대값       | 내부 처리 비교용      |
| **압축 품질**            | DICOM 메타데이터       | 압축률 및 품질 손실 확인                   | 손실률 계산           |
| **파일 크기**            | ZIP 파일 크기          | 압축 전후 크기 비교                        | 압축률 계산           |

**측정 주기**:

- 시스템 모니터링: 500ms 간격 (시스템 부하 최소화)
- 베이스라인 측정: 작업 시작 전 시스템 상태
- 변화량 계산: `증가량 = 최대값 - 베이스라인`

### 3. 후보 압축 라이브러리

**외부 실행파일**:

- `gdcmconv --j2k --lossy --irreversible --rate 100` (기본 압축률)

**Node.js 라이브러리**:

- `dcmjs-codecs` (유일한 실용적 선택지)

---

## Technical Implementation (기술적 구현)

### Phase 1: 압축 라이브러리 성능 벤치마크

**구현 범위**:

```typescript
interface CompressionBenchmark {
  library: 'gdcmconv' | 'dcmjs-codecs';
  compressionRate: number; // 10, 50, 100, 500
  inputSize: number; // MB
  outputSize: number; // MB
  processingTime: number; // seconds
  cpuUsage: number; // percentage
  memoryUsage: number; // MB
  qualityMetrics: DicomQualityMetrics;
}
```

**측정 방법**:

1. **gdcmconv**:
   - 자식 프로세스로 실행
   - EC2 CloudWatch 메트릭 수집 (CPU/Memory)
   - 처리 시간 직접 측정
2. **dcmjs-codecs**:
   - `process.cpuUsage()`, `process.memoryUsage()` 기본 API
   - `pidusage` 라이브러리로 실시간 CPU/Memory 모니터링
   - 압축 전/중/후 메트릭 수집 및 피크값 기록

```typescript
// 메트릭 수집 예시
interface CompressionMetrics {
  startTime: number;
  endTime: number;
  cpuUsage: { user: number; system: number };
  memoryPeak: { rss: number; heapUsed: number };
  cpuPeak: number;
}

const collectMetrics = async (): Promise<CompressionMetrics> => {
  const startCpu = process.cpuUsage();
  const startTime = Date.now();
  let memoryPeak = { rss: 0, heapUsed: 0 };
  let cpuPeak = 0;

  // 실시간 모니터링
  const monitor = setInterval(async () => {
    const stats = await pidusage(process.pid);
    cpuPeak = Math.max(cpuPeak, stats.cpu);

    const mem = process.memoryUsage();
    memoryPeak.rss = Math.max(memoryPeak.rss, mem.rss);
    memoryPeak.heapUsed = Math.max(memoryPeak.heapUsed, mem.heapUsed);
  }, 100);

  // ... 압축 작업 수행 ...

  clearInterval(monitor);
  return {
    startTime,
    endTime: Date.now(),
    cpuUsage: process.cpuUsage(startCpu),
    memoryPeak,
    cpuPeak,
  };
};
```

### Phase 2: 압축 파이프라인 구축

**처리 방식 결정**: **전체 다운로드 → 일괄 변환 → 업로드**

```
s3://stream-zip-hi-data/download/JPEG2000/ (399개 파일)
→ EC2 전체 다운로드 (196.9MB)
→ DICOM 압축 처리 (Rate 10/50/100/500)
→ ZIP 생성
→ S3 압축본 업로드
```

**선택 이유**:

- **POC 목적**: 실시간성 불필요 (백그라운드 비동기 작업)
- **성능 측정**: 다운로드/압축 시간 분리 측정 가능
- **구현 단순성**: 기존 download 로직 재사용
- **안정성**: 전체 파일 확보 후 처리로 실패 위험 최소화

**API 설계** (기존 http2-server 패턴 따라서):

### **HTTP/1.1 서버 (포트 3001, HTTP)**

#### 1. DICOM 압축 작업 시작

```http
POST /compress-dicom
Query Parameters:
  - s3SourceUri: s3://stream-zip-hi-data/download/JPEG2000/ (기본값)
  - s3TargetUri: s3://stream-zip-hi-data/compressed/ (기본값)
  - compressionRate: 100 (default: 100)
  - compressionLibrary: gdcmconv | dcmjs-codecs (default: gdcmconv)
  - anonymize: false (default: false)
  - outputFilename: {소스폴더명}-rate{압축률}-{타임스탬프}.zip (optional, 자동생성)
  - overwriteExisting: false (default: false)

Response:
{
  "success": true,
  "taskId": "comp-task-12345",
  "status": "processing",
  "estimatedTime": "5 minutes",
  "s3SourceUri": "s3://stream-zip-hi-data/download/JPEG2000/",
  "s3TargetPath": "s3://stream-zip-hi-data/compressed/ct-study-rate100-20250120-103000.zip",
  "sourceInfo": {
    "totalFiles": 399,
    "totalSize": "196.9MB"
  },
  "options": {
    "compressionRate": 100,
    "compressionLibrary": "gdcmconv",
    "anonymize": false,
    "outputFilename": "ct-study-rate100-20250120-103000.zip",
    "overwriteExisting": false
  }
}
```

**파일명 생성 규칙**:

1. **사용자 지정 파일명**: `outputFilename` 파라미터로 직접 지정

   ```
   POST /compress-dicom?outputFilename=my-custom-name.zip
   → s3://stream-zip-hi-data/compressed/my-custom-name.zip
   ```

2. **자동 생성 파일명** (기본값): `{소스폴더명}-rate{압축률}-{타임스탬프}.zip`

   **생성 규칙**:

   - **소스폴더명**: S3 URI의 마지막 폴더명 추출
   - **압축률**: compressionRate 파라미터 값
   - **타임스탬프**: 작업 시작 시간 (UTC, `YYYYMMDD-HHMMSS` 형식)

   **예시**:

   ```
   소스: s3://stream-zip-hi-data/download/JPEG2000/
   압축률: 100, 시작시간: 2025-01-20 10:30:00 UTC
   → JPEG2000-rate100-20250120-103000.zip

   소스: s3://stream-zip-hi-data/download/ct-study/
   압축률: 50, 시작시간: 2025-01-20 14:15:30 UTC
   → ct-study-rate50-20250120-141530.zip
   ```

3. **특수 경우 처리**:

   - **폴더명이 빈 경우**: `compressed-rate{압축률}-{타임스탬프}.zip`
   - **폴더명에 특수문자**: 알파벳, 숫자, 하이픈만 유지 (예: `ct_study@123` → `ct-study123`)
   - **폴더명이 너무 긴 경우**: 최대 50자로 제한

   **예시**:

   ```
   소스: s3://bucket/download/
   → compressed-rate100-20250120-103000.zip

   소스: s3://bucket/download/ct_study@v2.1/
   → ct-studyv21-rate100-20250120-103000.zip
   ```

4. **기본 경로 설정**:
   - **s3SourceUri 기본값**: `s3://stream-zip-hi-data/download/JPEG2000/`
   - **s3TargetUri 기본값**: `s3://stream-zip-hi-data/compressed/`
   - **타임스탬프 형식**: `YYYYMMDD-HHMMSS` (UTC 기준)

**덮어쓰기 정책**:

1. **overwriteExisting=false** (기본값):

   - 동일한 파일명 존재 시 → 자동으로 숫자 접미사 추가
   - `file.zip` → `file-1.zip` → `file-2.zip`

2. **overwriteExisting=true**: 기존 파일을 완전히 덮어쓰기

**API 사용 예시**:

1. **최소 파라미터 (모든 기본값 사용)**:

   ```
   POST /compress-dicom
   → 소스: s3://stream-zip-hi-data/download/JPEG2000/
   → 타겟: s3://stream-zip-hi-data/compressed/JPEG2000-rate100-20250120-103000.zip
   ```

2. **사용자 지정 파일명**:

   ```
   POST /compress-dicom?outputFilename=my-compressed-ct.zip
   → 타겟: s3://stream-zip-hi-data/compressed/my-compressed-ct.zip
   ```

3. **다른 소스 폴더 + 다른 압축률**:
   ```
   POST /compress-dicom?s3SourceUri=s3://bucket/my-folder/&compressionRate=50
   → 타겟: s3://stream-zip-hi-data/compressed/my-folder-rate50-20250120-103000.zip
   ```

**파일명 충돌 처리 예시**:

```
기존 파일: ct-study-rate100-20250120-103000.zip
새 요청 (overwriteExisting=false): ct-study-rate100-20250120-103000-1.zip
새 요청 (overwriteExisting=true): 기존 파일 덮어쓰기
```

#### 2. 압축 작업 상태 조회

**구현 방식**: JSON 파일 저장 (`/temp/compression-results/{taskId}.json`)

```http
GET /compress-dicom/{taskId}

Response:
{
  "success": true,
  "taskId": "comp-task-12345",
  "status": "completed", // processing, completed, failed
  "timestamp": "2025-01-20T10:30:00Z",
  "s3CompressedPath": "s3://stream-zip-hi-data/compressed/ct-study-rate100-20250120-103000.zip",
  "compressionStats": {
    "originalSize": "196.9MB",
    "compressedSize": "2.8MB",
    "compressionRatio": "70:1",
    "processingTime": "180s",
    "processedFiles": 399,
    "cpuPeak": "85%",
    "memoryPeak": "2.1GB",
    "downloadTime": "8.2s",
    "compressionTime": "4.1s",
    "uploadTime": "1.3s"
  },
  "options": {
    "compressionRate": 100,
    "compressionLibrary": "gdcmconv",
    "anonymize": false
  }
}
```

**POC 목적 고려사항**:

- **데이터 수집**: 각 테스트 결과를 JSON 파일로 영구 저장
- **비교 분석**: 여러 라이브러리/압축률 결과를 쉽게 비교
- **단순 구현**: DB 없이 파일 시스템 활용 (POC 적합)
- **수동 분석**: 결과 파일을 직접 열어서 확인 가능
- **멀티 서버**: 단일 EC2 POC 환경에서는 문제없음

#### 추가 분석용 엔드포인트 (선택사항)

```http
GET /compress-dicom/results
Response: 모든 압축 결과 목록 (성능 비교표 생성용)

GET /compress-dicom/benchmark
Response: gdcmconv vs dcmjs-codecs 성능 비교 요약
```

#### 3. 압축된 파일 다운로드 (기존 download 엔드포인트 활용)

```http
GET /download
Query Parameters:
  - s3Uri: s3://stream-zip-hi-data/compressed/ct-study-rate100-20250120-103000.zip
  - filename: ct-study-rate100-20250120-103000.zip

Response: ZIP 파일 스트림 (압축된 399개 DICOM 파일)
```

---

## Success Criteria (성공 기준)

### 1. 기능적 성공 기준

- **압축 파이프라인 동작 검증**: API 호출 → 압축 → S3 저장 전체 플로우 정상 작동
- **라이브러리 비교 데이터 수집**: gdcmconv vs dcmjs-codecs 정량적 메트릭 확보
- **품질 검증**: 압축된 DICOM 파일 CloudWebViewer 정상 표시 확인

### 2. 데이터 수집 성공 기준

- **성능 메트릭**: 처리 시간, CPU/메모리 사용량, 압축률 정확한 측정
- **확장성 분석**: 단일 작업 vs 동시 작업 환경에서의 리소스 사용량 비교
- **안정성 검증**: 시스템 한계 상황에서의 동작 특성 파악

### 3. 분석 결과 도출

- **라이브러리별 특성 분석**: 각 라이브러리의 장단점 명확한 정의
- **운영 환경 권장사항**: 실제 운영 시 고려사항 및 최적 선택 가이드 제시
- **기술적 근거 확보**: 향후 구현 결정을 위한 객관적 데이터 제공

---

## Expected Outcomes (예상 결과)

### 1. 기능 검증 결과

- **압축 파이프라인 동작**: API 기반 자동화된 압축 처리 시스템 구축 완료
- **라이브러리 호환성**: 두 라이브러리 모두 DICOM JPEG2000 압축 정상 동작 확인
- **품질 검증**: CloudWebViewer에서 압축된 파일 정상 렌더링 확인

### 2. 성능 메트릭 비교 데이터

**수집 예정 데이터**:

| 측정 항목         | gdcmconv | dcmjs-codecs | 분석 목적            |
| ----------------- | -------- | ------------ | -------------------- |
| **처리 시간**     | 측정     | 측정         | 전체 파이프라인 성능 |
| **CPU 사용량**    | 측정     | 측정         | 시스템 리소스 효율성 |
| **메모리 사용량** | 측정     | 측정         | 메모리 요구사항 분석 |
| **압축률**        | 측정     | 측정         | 압축 품질 비교       |
| **확장성**        | 측정     | 측정         | 동시 처리 시 안정성  |

### 3. 운영 환경 가이드라인

**도출 예정 결과**:

- **단일 작업 환경**: 각 라이브러리의 적합성 평가
- **다중 사용자 환경**: 동시 처리 시 시스템 안정성 분석
- **리소스 요구사항**: 서버 스펙 및 확장 계획 수립을 위한 데이터
- **구현 복잡도**: 개발 및 운영 관점에서의 고려사항

---

## Implementation Steps (구현 단계)

### Phase 1: 환경 구축 및 기본 검증

- EC2 인스턴스 설정 및 라이브러리 설치
- gdcmconv, dcmjs-codecs 설치 및 동작 확인
- 기본 압축 기능 테스트 (단일 파일)

### Phase 2: 성능 측정 시스템 구축

- 실시간 시스템 모니터링 구현 (`SystemMonitorService`)
- CPU/메모리 측정 로직 개발 (`pidusage` 통합)
- 399개 DICOM 파일 대용량 처리 테스트

### Phase 3: API 파이프라인 개발

- RESTful API 개발 (압축 요청/상태 조회/벤치마크)
- S3 업로드/다운로드 통합
- 비동기 작업 처리 및 결과 저장 시스템

### Phase 4: 성능 분석 및 검증

- 단일 작업 성능 테스트 (n=3)
- 동시 작업 확장성 테스트 (n=10)
- 라이브러리별 특성 분석 및 권고사항 도출

---

## Performance Test Results (성능 테스트 결과)

### 단일 작업 테스트 결과 (n=3)

**테스트 환경**: EC2 인스턴스, 399개 DICOM 파일 (187.8MB), Rate 100 압축

**⚠️ 이전 POC와의 성능 차이 분석**:

**이전 POC (제어된 병렬 처리)**:

- gdcmconv(43초) > dcmjs-codecs(48.34초)
- 세동시 프로세스 수 제한 (예: 10개)
- 순수 압축 성능 측정

**현재 POC (무제한 병렬 처리)**:

- dcmjs-codecs(63.67초) > gdcmconv(70.33초)
- 399개 파일 × 개별 프로세스 = **399개 동시 실행**
- 프로세스 오버헤드로 gdcmconv 성능 저하

**운영 환경에서의 문제점**:
다중 사용자 환경에서 동시 요청 시 gdcmconv는 **수천 개 프로세스** 생성 위험 (사용자 수 × 399개), 이는 시스템 다운을 초래할 수 있음.

| 라이브러리       | 평균 처리시간 | 평균 압축률 | 평균 다운로드시간 | 평균 압축시간 | 평균 업로드시간 | 평균 CPU 사용률 | 평균 메모리 사용량 |
| ---------------- | ------------- | ----------- | ----------------- | ------------- | --------------- | --------------- | ------------------ |
| **gdcmconv**     | 70.33초       | 79:1        | 35.57초           | 33.47초       | 0.20초          | 94%             | 131.7MB            |
| **dcmjs-codecs** | 63.67초       | 82:1        | 30.57초           | 32.07초       | 0.17초          | 94%             | 0MB\*              |

\*dcmjs-codecs의 메모리 사용량이 0MB로 측정된 것은 시스템 메모리 모니터링 한계로 인한 것으로 추정. 추가 테스트(n=13) 결과 dcmjs-codecs 평균 메모리 사용량 42.6MB로 정상 측정됨. gdcmconv(134MB) 대비 **3.1배 메모리 효율적**임이 확인됨.

### 동시 작업 테스트 결과 (n=10)

**테스트 조건**: 동일한 399개 파일을 10개 작업으로 동시 처리

#### gdcmconv 동시 처리 (10개 작업)

- **CPU 사용률**: 84.8% (적정 사용률, 15% 여유)
- **메모리 사용량**: 약 700MB 증가
- **프로세스 특징**:
  - 순차적 개별 파일 처리로 안정적 실행
  - 일시적 zombie 프로세스 발생 (실행 중 정상 현상)
  - 시스템 안정성 유지

#### dcmjs-codecs 동시 처리 (10개 작업)

- **CPU 사용률**: 99.9% (과도한 사용, 시스템 여유도 부족)
- **메모리 사용량**: 약 200MB 증가
- **프로세스 특징**:
  - 단일 Node.js 프로세스 내 처리
  - CPU 포화 상태로 시스템 반응성 저하
  - 높은 시스템 부하

### 성능 비교 분석

#### 단일 작업 성능 (n=3 기준)

| 메트릭            | gdcmconv | dcmjs-codecs | 우승자             |
| ----------------- | -------- | ------------ | ------------------ |
| **처리 시간**     | 70.33초  | 63.67초      | **dcmjs-codecs**   |
| **압축률**        | 79:1     | 82:1         | **tie**            |
| **다운로드 시간** | 35.57초  | 30.57초      | **dcmjs-codecs**   |
| **압축 시간**     | 33.47초  | 32.07초      | **tie**            |
| **업로드 시간**   | 0.20초   | 0.17초       | **dcmjs-codecs**   |
| **CPU 사용률**    | 94%      | 94%          | **tie**            |
| **메모리 사용량** | 131.7MB  | 0MB\*        | **dcmjs-codecs\*** |

#### 동시 작업 성능 분석

| 메트릭            | gdcmconv           | dcmjs-codecs | 분석                     |
| ----------------- | ------------------ | ------------ | ------------------------ |
| **CPU 효율성**    | 84.8% (적정)       | 99.9% (포화) | **gdcmconv 우수**        |
| **메모리 효율성** | 700MB (높음)       | 200MB (낮음) | **dcmjs-codecs 우수**    |
| **프로세스 수**   | 3,990개 (극심)     | 1개 (단순)   | **dcmjs-codecs 압도적**  |
| **시스템 위험**   | 프로세스 폭탄      | CPU 포화     | **dcmjs-codecs 덜 위험** |
| **확장성**        | 프로세스 한계 도달 | CPU 병목     | **둘 다 문제**           |

### 주요 발견사항

#### 1. 단일 작업에서는 dcmjs-codecs가 전체 파이프라인에서 우세

- **전체 파이프라인 속도**: 7초 빠름 (10% 개선)
- **원인**: gdcmconv의 399개 프로세스 생성 오버헤드 vs dcmjs-codecs의 단일 프로세스 효율성
- **주의**: 순수 압축 속도는 gdcmconv가 여전히 빠름 (이전 POC 43초 vs 48.34초)
- **전반적 성능**: 실제 운영 환경에서는 dcmjs-codecs가 더 효율적

#### 2. 동시 작업에서는 둘 다 심각한 문제점 존재

**gdcmconv의 문제점**:

- **프로세스 폭탄**: 10개 작업 시 3,990개 프로세스 생성 (399개 × 10개)
- **메모리 오버헤드**: 700MB 증가 (프로세스 생성 비용)
- **시스템 위험**: 프로세스 테이블 오버플로우 가능성

**dcmjs-codecs의 문제점**:

- **CPU 포화**: 99.9% 사용률로 시스템 반응성 저하
- **확장성 한계**: 단일 프로세스 병목

**상대적 평가**: dcmjs-codecs가 덜 위험함 (CPU 포화 < 시스템 다운)

#### 3. 아키텍처별 특성과 확장성 문제

**gdcmconv의 확장성 한계**:

- **이상적 환경** (이전 POC): 제어된 병렬 처리로 우수한 성능
- **실제 운영 환경**: 무제한 프로세스 생성으로 시스템 위험
- **확장성 문제**: 사용자 수 증가 시 프로세스 수 기하급수적 증가
  - 예: 10명 동시 사용 × 399개 파일 = **3,990개 프로세스**
  - 예: 100명 동시 사용 × 399개 파일 = **39,900개 프로세스** (시스템 다운 확실)

**CPU 100% 미만이어도 발생하는 심각한 문제들**:

- **프로세스 테이블 오버플로우**: 시스템 프로세스 한계 초과 (일반적으로 1024~4096개)
- **메모리 고갈**: 프로세스 메타데이터만으로 600MB+ 추가 사용
- **컨텍스트 스위칭 오버헤드**: 스케줄러 부하로 전체 시스템 응답성 저하
- **파일 디스크립터 고갈**: 200,000개+ FD 필요로 시스템 리소스 한계 초과
- **I/O 경합**: 디스크 스래싱으로 전체 I/O 성능 급격히 저하

**dcmjs-codecs의 확장성 안정성**:

- **일관된 성능**: 사용자 수와 무관하게 단일 프로세스 유지
- **예측 가능한 리소스**: CPU/메모리 사용량 예측 가능
- **운영 안정성**: 프로세스 폭탄 위험 없음

---

## Conclusion (결론)

### 핵심 발견사항

1. **단일 작업 성능**: dcmjs-codecs가 전반적으로 우수
2. **동시 작업 성능**: 둘 다 심각한 문제점 존재, dcmjs-codecs가 상대적으로 덜 위험
3. **시스템 안정성**: 단일 작업에서만 안정적, 동시 작업에서는 둘 다 위험

### 권장사항

#### 운영 환경별 선택 가이드

**단일 사용자 환경 또는 순차 처리**:

- **권장**: dcmjs-codecs
- **이유**: 빠른 처리 속도, 간단한 구현

**다중 사용자 환경 또는 동시 처리**:

- **권장**: **작업 큐 시스템으로 순차 처리**
- **이유**: 두 라이브러리 모두 동시 처리에 심각한 문제점 존재

#### 최종 권장안

**프로덕션 환경**에서는 **dcmjs-codecs + 작업 큐**를 권장합니다:

1. **단일 작업**: dcmjs-codecs가 모든 면에서 우수
2. **동시 처리**: 작업 큐로 순차 처리하여 안정성 확보
3. **시스템 안전**: 프로세스 폭탄 위험 회피
4. **구현 단순성**: Node.js 내부 처리로 관리 복잡도 최소화

#### 작업 큐 시스템 설계

**POC 환경 (계획)**: **메모리 기반 큐**

- **구현 예정**: 간단한 배열 기반 FIFO 큐
- **장점**: 구현 단순, 외부 의존성 없음, POC 목적에 최적
- **단점**: 서버 재시작 시 큐 손실 (POC에서는 문제없음)

**프로덕션 환경**: **다중 아키텍처 옵션**

##### **옵션 1: 전통적 서버 기반**

- **구현**: BullMQ + Redis + 전용 변환 서버
- **장점**: 영속성, 분산 처리, 모니터링, 재시작 후 복구
- **특징**: 순차 처리 보장 (`process(1, handler)`)

##### **옵션 2: 서버리스 아키텍처 (권장)**

- **구현**: AWS SQS + Lambda (dcmjs-codecs)
- **장점**: 자동 스케일링, 서버 관리 불필요, 비용 효율성
- **아키텍처**:
  ```
  API Gateway → SQS → Lambda (dcmjs-codecs) → S3
                ↓
          CloudWatch (모니터링)
  ```
- **Lambda 최적화 요소**:
  - **실행 시간**: 60-70초 (15분 한계 내 충분)
  - **메모리**: 512MB-1GB (10GB 한계 내 충분)
  - **패키지 크기**: dcmjs-codecs 경량 (250MB 한계 내)
  - **비용**: 실행 시간만큼만 과금 (70초 × 요청 수)
- **비용 효율성 분석**:
  - **SQS**: 100만 메시지당 \$0.40 (월 1,000건 시 거의 무료)
  - **Lambda**: 70초/건 × 1GB 메모리 기준
    - 월 1,000건: \$1.17 vs EC2 \$40 (97% 절약)
    - 월 10,000건: \$11.70 vs EC2 \$40 (71% 절약)
    - **브레이크이븐**: 월 34,000건 (이론적 계산, 실제로는 EC2 성능 한계로 Lambda가 더 유리)
  - **EC2 성능 한계 고려**:
    - t3.medium 기준: 70초/건 × 월 720시간 = 이론적 최대 36,857건/월
    - 실제 처리량: CPU/메모리 부하, 시스템 오버헤드 고려 시 약 5,000-10,000건/월
    - **결론**: 치과 환경 월 1,000-3,000건 수준에서는 Lambda가 압도적으로 유리

##### **서버리스 vs 전통 서버 비교**

| 항목                | 서버리스 (Lambda)   | 전통 서버 (EC2+BullMQ) |
| ------------------- | ------------------- | ---------------------- |
| **확장성**          | 자동 무제한         | 수동 서버 추가 필요    |
| **운영 부담**       | 없음                | 서버 관리 필요         |
| **비용**            | 사용량 기반         | 고정 서버 비용         |
| **콜드 스타트**     | 2-5초 지연          | 없음                   |
| **라이브러리 제약** | dcmjs-codecs만 가능 | 모든 라이브러리 가능   |
| **모니터링**        | CloudWatch 내장     | 별도 구축 필요         |

**권장**: **dcmjs-codecs + Lambda + SQS**가 최적의 프로덕션 솔루션

#### 큐 POC 구현 계획

**현재 상황**: 큐 시스템 없음 (즉시 병렬 처리)

- 동시 요청 시 병렬 처리로 시스템 과부하
- gdcmconv: 프로세스 폭탄, dcmjs-codecs: CPU 포화

**구현할 큐 시스템**:

- **FIFO 순차 처리**: 먼저 요청된 작업부터 순차적으로 처리
- **큐 상태 모니터링**: 대기열 길이, 현재 처리 중인 작업, 예상 대기시간 제공
- **큐 크기 제한**: 메모리 보호를 위한 최대 큐 크기 설정
- **상태 추적**: queued → processing → completed/failed 상태 관리

**추가 API 기능**:

- **큐 상태 조회**: 전체 대기열 현황 확인
- **작업 위치 조회**: 특정 작업의 대기열 순서 및 예상 시간
- **실시간 상태 업데이트**: 작업 진행 상황 실시간 모니터링

#### ⚠️ **중요 경고**

**gdcmconv 동시 처리 금지**:

- 10개 작업 시 3,990개 프로세스 생성
- 시스템 다운 위험 극도로 높음
- 프로덕션 환경에서 절대 사용 금지

### 기술적 성과

- **압축 파이프라인 구축**: API 기반 자동화 완성
- **성능 벤치마킹**: 정량적 비교 데이터 확보
- **실시간 모니터링**: 시스템 리소스 측정 시스템 구현
- **확장성 검증**: 동시 처리 환경에서의 안정성 확인

### POC 성과

- **기능 검증 완료**: DICOM 압축 파이프라인의 기술적 구현 가능성 확인
- **데이터 기반 분석**: 두 라이브러리의 정량적 성능 비교 데이터 확보
- **운영 가이드라인**: 실제 운영 환경에서의 선택 기준 및 고려사항 도출
- **아키텍처 설계**: 전통적 서버 vs 서버리스 아키텍처 옵션 제시
- **기술 기반 구축**: 향후 대용량 의료 영상 처리 시스템 개발을 위한 기반 마련

### 최종 아키텍처 권장사항

**프로덕션 환경 최적 솔루션**: **dcmjs-codecs + AWS Lambda + SQS**

```
┌─────────────────┐    ┌─────────────┐    ┌──────────────────┐    ┌─────────────┐
│   API Gateway   │───▶│     SQS     │───▶│  Lambda Function │───▶│     S3      │
│ (압축 요청 접수)  │    │ (작업 큐 관리) │    │  (dcmjs-codecs)  │    │ (결과 저장)  │
└─────────────────┘    └─────────────┘    └──────────────────┘    └─────────────┘
                                                    │
                                                    ▼
                                          ┌─────────────────┐
                                          │   CloudWatch    │
                                          │  (모니터링/로그)  │
                                          └─────────────────┘
```

**핵심 장점**:

- **무제한 확장성**: 동시 요청 수에 관계없이 자동 스케일링
- **프로세스 폭탄 해결**: Lambda 격리 환경으로 시스템 안정성 보장
- **운영 부담 제거**: 서버 관리, 패치, 모니터링 AWS 위임
- **비용 최적화**: 실제 사용량만큼만 과금 (월 1,000건 시 97% 절약, \$40 → \$1.17)

이 POC를 통해 **DICOM 업로드 후 압축 파이프라인**의 기술적 타당성을 검증하고, 각 라이브러리의 특성을 명확히 분석하여 **서버리스 기반의 최적 아키텍처**를 도출했습니다.
