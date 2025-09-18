# WADO 완전 가이드: 표준 분석부터 서버 구축까지

## 1. 개요

WADO는 **Web Access to DICOM Objects**의 약자로, 웹을 통해 DICOM 의료 영상 데이터에 접근하기 위한 국제 표준입니다.

### 1.1 WADO가 필요한 이유

**기존 문제점:**

- 병원마다 다른 방식으로 의료 영상 저장/전송
- DICOM 파일을 웹에서 직접 처리하기 어려움
- 의료 시스템 간 호환성 부족

**WADO 해결책:**

- **표준화된 웹 API**로 DICOM 데이터 접근
- **HTTP 기반**으로 웹 브라우저에서 직접 사용 가능
- **병원 시스템 간 상호 운용성** 확보

### 1.2 WADO 표준 발전 과정

```
2004년: WADO-URI (초기 버전)
2015년: WADO-RS (RESTful 버전)
2017년: DICOMweb (통합 표준)
```

## 2. WADO 표준 유형별 상세 분석

### 2.1 WADO-URI (Original WADO)

#### 2.1.1 특징

- **GET 방식의 단순한 HTTP 요청**
- **URL 파라미터**로 DICOM 객체 식별
- **가장 오래되고 널리 지원**되는 방식

#### 2.1.2 요청 형식

```http
GET /wado?requestType=WADO&studyUID={studyUID}&seriesUID={seriesUID}&objectUID={objectUID}&contentType={contentType}

# 실제 예시
GET /wado?requestType=WADO&studyUID=1.2.840.113619.2.55.3.604&seriesUID=1.3.46.670589.11.0.0.11.4.2.0.8743&objectUID=1.2.276.0.7230010.3.1.4.8323329.5576.1495927169.335276&contentType=application/dicom
```

#### 2.1.3 주요 파라미터

| 파라미터        | 설명                | 예시                                 |
| --------------- | ------------------- | ------------------------------------ |
| **requestType** | 요청 유형           | WADO                                 |
| **studyUID**    | Study Instance UID  | 1.2.840.113619.2.55.3.604            |
| **seriesUID**   | Series Instance UID | 1.3.46.670589.11.0.0.11.4.2.0.8743   |
| **objectUID**   | SOP Instance UID    | 1.2.276.0.7230010.3.1.4.8323329.5576 |
| **contentType** | 응답 형식           | application/dicom, image/jpeg        |

#### 2.1.4 응답 형식

```http
# DICOM 원본 데이터
Content-Type: application/dicom
Content-Length: 524288

# 변환된 이미지 (JPEG)
Content-Type: image/jpeg
Content-Length: 45612
```

### 2.2 WADO-RS (RESTful Services)

#### 2.2.1 특징

- **REST API 스타일**의 현대적 접근
- **URL 경로**로 리소스 계층 구조 표현
- **HTTP 메서드** 활용 (GET, POST, DELETE 등)
- **JSON 메타데이터** 지원

#### 2.2.2 URL 구조

```
/studies/{studyUID}
/studies/{studyUID}/series/{seriesUID}
/studies/{studyUID}/series/{seriesUID}/instances/{instanceUID}
/studies/{studyUID}/series/{seriesUID}/instances/{instanceUID}/frames/{frameNumber}
```

#### 2.2.3 실제 요청 예시

**1. Study 메타데이터 조회:**

```http
GET /studies/1.2.840.113619.2.55.3.604
Accept: application/dicom+json

Response:
{
  "0020000D": {"vr": "UI", "Value": ["1.2.840.113619.2.55.3.604"]},
  "00100010": {"vr": "PN", "Value": [{"Alphabetic": "PATIENT^TEST"}]},
  "00080020": {"vr": "DA", "Value": ["20231215"]}
}
```

**2. DICOM 인스턴스 다운로드:**

```http
GET /studies/1.2.840.113619.2.55.3.604/series/1.3.46.670589.11/instances/1.2.276.0.7230010.3.1.4
Accept: application/dicom

Response: (Binary DICOM data)
```

**3. 이미지 프레임 요청:**

```http
GET /studies/{studyUID}/series/{seriesUID}/instances/{instanceUID}/frames/1
Accept: image/jpeg

Response: (JPEG image data)
```

#### 2.2.4 고급 기능

**Multipart 응답:**

```http
GET /studies/1.2.840.113619.2.55.3.604/instances
Accept: multipart/related; type="application/dicom"

Response:
--boundary123
Content-Type: application/dicom

(DICOM data 1)
--boundary123
Content-Type: application/dicom

(DICOM data 2)
--boundary123--
```

**BulkData URI:**

```json
{
  "7FE00010": {
    "vr": "OW",
    "BulkDataURI": "/studies/1.2.3/series/4.5.6/instances/7.8.9/bulkdata/7fe00010"
  }
}
```

### 2.3 DICOMweb (통합 표준)

#### 2.3.1 구성 요소

**QIDO-RS (Query based on ID for DICOM Objects):**

```http
# 환자 검색
GET /qido/studies?PatientName=SMITH^JOHN&limit=10

# 날짜 범위 검색
GET /qido/studies?StudyDate=20231201-20231231
```

**WADO-RS (Web Access to DICOM Objects):**

```http
# 데이터 다운로드
GET /wado/studies/{studyUID}/instances
```

**STOW-RS (Store Over the Web):**

```http
# 데이터 업로드
POST /stow/studies
Content-Type: multipart/related; type="application/dicom"
```

## 3. OHIF에서의 WADO 구현 분석

### 3.1 핵심 패키지

#### 3.1.1 dicomweb-client

```javascript
// 메인 DICOMweb 클라이언트 라이브러리
import { api } from 'dicomweb-client';

const client = new api.DICOMwebClient({
  url: 'https://server.com/dicomweb',
  headers: { Authorization: 'Bearer token' },
});

// WADO-RS 사용
const instance = await client.retrieveInstance({
  studyInstanceUID: '1.2.3',
  seriesInstanceUID: '4.5.6',
  sopInstanceUID: '7.8.9',
});
```

#### 3.1.2 @cornerstonejs/dicom-image-loader

```javascript
// WADO-URI 지원
import dicomImageLoader from '@cornerstonejs/dicom-image-loader';

// WADO-URI 이미지 로딩
const imageId =
  'wadouri:https://server.com/wado?requestType=WADO&studyUID=1.2.3&seriesUID=4.5.6&objectUID=7.8.9';
const image = await dicomImageLoader.loadImage(imageId);
```

### 3.2 OHIF의 WADO 구현 코드 분석

#### 3.2.1 DicomWebDataSource 설정

```typescript
// extensions/default/src/DicomWebDataSource/index.ts
function createDicomWebApi(dicomWebConfig: DicomWebConfig, servicesManager) {
  const qidoDicomWebClient = new api.DICOMwebClient({
    url: dicomWebConfig.qidoRoot,
    headers: getAuthorizationHeader(),
    errorInterceptor: errorHandler.getHTTPErrorHandler(),
  });

  const wadoDicomWebClient = new api.DICOMwebClient({
    url: dicomWebConfig.wadoRoot,
    headers: getAuthorizationHeader(),
    singlepart: dicomWebConfig.singlepart,
  });
}
```

#### 3.2.2 QIDO-RS 검색 구현

```javascript
// QIDO-RS를 통한 Study 검색
const implementation = {
  query: {
    studies: {
      search: async (params) => {
        const { studyInstanceUid, patientId, patientName } = params;

        const searchParams = {};
        if (studyInstanceUid) searchParams.StudyInstanceUID = studyInstanceUid;
        if (patientId) searchParams.PatientID = patientId;
        if (patientName) searchParams.PatientName = patientName;

        return qidoDicomWebClient.searchForStudies(searchParams);
      },
    },
  },
};
```

#### 3.2.3 WADO-RS 데이터 다운로드

```javascript
// WADO-RS를 통한 인스턴스 다운로드
const wadorsRetriever = (url, studyUID, seriesUID, sopUID, headers) => {
  const config = {
    url,
    headers,
    errorInterceptor: errorHandler.getHTTPErrorHandler(),
  };
  const dicomWeb = new api.DICOMwebClient(config);

  return dicomWeb.retrieveInstance({
    studyInstanceUID: studyUID,
    seriesInstanceUID: seriesUID,
    sopInstanceUID: sopUID,
  });
};
```

#### 3.2.4 BulkData 처리

```javascript
// extensions/default/src/DicomWebDataSource/index.ts
bulkDataURI: async ({ StudyInstanceUID, BulkDataURI }) => {
  qidoDicomWebClient.headers = getAuthorizationHeader();
  const options = {
    multipart: false,
    BulkDataURI,
    StudyInstanceUID,
  };
  return qidoDicomWebClient.retrieveBulkData(options).then((val) => {
    const ret = (val && val[0]) || undefined;
    return ret;
  });
};
```

### 3.3 OHIF 설정 예시

#### 3.3.1 DICOMweb 설정

```javascript
// config/default.js
window.config = {
  dataSources: [
    {
      sourceName: 'dicomweb',
      configuration: {
        friendlyName: 'dcm4chee DICOM Server',
        name: 'DCM4CHEE',

        // WADO-RS 엔드포인트
        wadoRoot: 'https://server.com/dcm4chee-arc/aets/DCM4CHEE/rs',

        // QIDO-RS 엔드포인트
        qidoRoot: 'https://server.com/dcm4chee-arc/aets/DCM4CHEE/rs',

        // WADO-URI 엔드포인트
        wadoUri: 'https://server.com/dcm4chee-arc/aets/DCM4CHEE/wado',

        // 추가 설정
        singlepart: true,
        supportsInstanceMetadata: true,
        supportsFuzzyMatching: false,
        supportsWildcard: true,
      },
    },
  ],
};
```

#### 3.3.2 다중 WADO 서버 설정

```javascript
window.config = {
  dataSources: [
    {
      sourceName: 'dicomweb-dcm4chee',
      configuration: {
        name: 'DCM4CHEE',
        wadoRoot: 'https://dcm4chee.hospital.com/dicomweb',
        qidoRoot: 'https://dcm4chee.hospital.com/dicomweb',
      },
    },
    {
      sourceName: 'dicomweb-orthanc',
      configuration: {
        name: 'Orthanc',
        wadoRoot: 'https://orthanc.clinic.com/dicom-web',
        qidoRoot: 'https://orthanc.clinic.com/dicom-web',
      },
    },
  ],
};
```

### 3.4 OHIF의 ImageId 생성 방식

```javascript
// extensions/default/src/DicomWebDataSource/utils/getImageId.js
export default function getImageId({ instance, frame, config }) {
  const { StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID } = instance;

  if (config.wadoRoot) {
    // WADO-RS 방식
    let imageId = `wadors:${config.wadoRoot}/studies/${StudyInstanceUID}/series/${SeriesInstanceUID}/instances/${SOPInstanceUID}`;

    if (frame !== undefined) {
      imageId += `/frames/${frame}`;
    }

    return imageId;
  }

  if (config.wadoUri) {
    // WADO-URI 방식
    let imageId = `wadouri:${config.wadoUri}?requestType=WADO&studyUID=${StudyInstanceUID}&seriesUID=${SeriesInstanceUID}&objectUID=${SOPInstanceUID}`;

    if (frame !== undefined) {
      imageId += `&frameNumber=${frame}`;
    }

    return imageId;
  }
}
```

## 4. WADO vs POC2 비교 분석

### 4.1 접근 방식 차이

| 항목            | WADO (OHIF)               | POC2                   |
| --------------- | ------------------------- | ---------------------- |
| **표준 준수**   | DICOM 국제 표준 완전 준수 | 자체 프로토콜          |
| **병원 호환성** | 모든 DICOM 서버와 호환    | 전용 서버 필요         |
| **데이터 접근** | 개별 DICOM 객체 단위      | ZIP 압축 일괄 다운로드 |
| **메타데이터**  | 풍부한 DICOM 메타데이터   | 제한적 메타데이터      |
| **캐싱**        | 브라우저 HTTP 캐시 의존   | 자체 캐싱 전략         |
| **압축**        | 압축 미지원               | ZIP 압축으로 효율적    |
| **속도**        | 느림 (다중 HTTP 요청)     | 빠름 (스트림 압축)     |

### 4.2 사용 사례별 적합성

#### 4.2.1 WADO가 적합한 경우

- **병원 EMR/PACS 시스템 연동**
- **표준 준수가 중요한 의료 기관**
- **다양한 DICOM 서버와 호환 필요**
- **의료 인증이 필요한 시스템**

#### 4.2.2 POC2가 적합한 경우

- **클라우드 기반 빠른 뷰어**
- **대용량 CT 데이터 스트리밍**
- **사용자 경험 최적화 우선**
- **자체 인프라 구축 가능**

### 4.3 기술적 한계

#### 4.3.1 WADO 한계

```javascript
// 100개 슬라이스 = 100번의 개별 HTTP 요청
for (let i = 0; i < slices.length; i++) {
  const imageId = `wadors:${wadoRoot}/studies/${studyUID}/series/${seriesUID}/instances/${slices[i].sopInstanceUID}`;
  await loadImage(imageId); // 각각 별도 요청
}
```

#### 4.3.2 POC2 한계

```javascript
// WADO 표준 미준수로 병원 시스템 직접 연동 불가
// 별도 변환 서버 필요
const response = await fetch('/api/dicom-zip-stream'); // 전용 API
```

## 5. WADO 서버 구현 및 구축 방안

### 5.1 오픈소스 WADO 서버 솔루션

#### 5.1.1 DCM4CHEE (Enterprise급)

**특징:**

- 가장 성숙한 오픈소스 DICOM 서버
- 완전한 PACS 시스템 제공 (Archive, Web UI, HL7 연동)
- 병원 환경에서 검증된 안정성

**설치 및 구성:**

```bash
# Docker Compose로 DCM4CHEE 설치
# docker-compose.yml
version: '3.8'
services:
  ldap:
    image: dcm4che/slapd-dcm4chee:2.6.3-31.0
    ports:
      - "389:389"
    env_file: docker-compose.env

  db:
    image: dcm4che/postgres-dcm4chee:15.4-31
    ports:
      - "5432:5432"
    env_file: docker-compose.env
    volumes:
      - dcm4chee-db-data:/var/lib/postgresql/data

  arc:
    image: dcm4che/dcm4chee-arc-psql:5.31.0
    ports:
      - "8080:8080"
      - "8443:8443"
      - "9990:9990"
      - "9993:9993"
      - "11112:11112"
      - "2762:2762"
      - "2575:2575"
      - "12575:12575"
    env_file: docker-compose.env
    depends_on:
      - ldap
      - db
    volumes:
      - dcm4chee-arc-wildfly:/opt/wildfly/standalone
      - dcm4chee-arc-storage:/storage

volumes:
  dcm4chee-db-data:
  dcm4chee-arc-wildfly:
  dcm4chee-arc-storage:

# 실행
docker-compose up -d

# WADO-RS 엔드포인트
http://localhost:8080/dcm4chee-arc/aets/DCM4CHEE/rs/studies
# QIDO-RS 엔드포인트
http://localhost:8080/dcm4chee-arc/aets/DCM4CHEE/rs/studies?PatientName=SMITH
# STOW-RS 엔드포인트
http://localhost:8080/dcm4chee-arc/aets/DCM4CHEE/rs/studies
```

**OHIF 연동 설정:**

```javascript
// OHIF config for DCM4CHEE
window.config = {
  dataSources: [
    {
      sourceName: 'dicomweb',
      configuration: {
        friendlyName: 'DCM4CHEE Archive',
        name: 'DCM4CHEE',
        wadoRoot: 'http://localhost:8080/dcm4chee-arc/aets/DCM4CHEE/rs',
        qidoRoot: 'http://localhost:8080/dcm4chee-arc/aets/DCM4CHEE/rs',
        wadoUri: 'http://localhost:8080/dcm4chee-arc/aets/DCM4CHEE/wado',
        singlepart: false,
        supportsInstanceMetadata: true,
        supportsFuzzyMatching: true,
        supportsWildcard: true,
      },
    },
  ],
};
```

#### 5.1.2 Orthanc (경량급)

**특징:**

- 가벼운 설치 및 관리
- RESTful API 제공
- C++로 작성되어 고성능
- 다양한 플러그인 지원

**설치 및 구성:**

```bash
# Docker로 Orthanc 설치
docker run -p 4242:4242 -p 8042:8042 \
  -e ORTHANC__REGISTERED_USERS='{"ohif": "ohif"}' \
  -e ORTHANC__DICOM_WEB__ENABLE=true \
  -e ORTHANC__DICOM_WEB__ROOT="/dicom-web/" \
  --name orthanc \
  jodogne/orthanc-plugins

# DICOMweb 엔드포인트
http://localhost:8042/dicom-web/studies
```

**Orthanc 설정 파일 (orthanc.json):**

```json
{
  "Name": "Orthanc DICOM Server",
  "HttpPort": 8042,
  "DicomPort": 4242,

  "Plugins": ["/usr/local/lib/orthanc/plugins"],

  "DicomWeb": {
    "Enable": true,
    "Root": "/dicom-web/",
    "EnableWado": true,
    "WadoRoot": "/wado",
    "Ssl": false,
    "StowMaxInstances": 10,
    "StowMaxPatients": 10
  },

  "RegisteredUsers": {
    "ohif": "password123"
  },

  "RemoteAccessAllowed": true,
  "AuthenticationEnabled": false
}
```

#### 5.1.3 OHIF 전용 정적 DICOMweb 서버

**AWS Static DICOMweb 프로젝트:**

병원 기존 PACS 없이도 OHIF를 테스트할 수 있는 서버리스 솔루션입니다.

```bash
# AWS Static DICOMweb 프로젝트 클론
git clone https://github.com/aws-samples/dicomweb-wado-qido-stow-serverless.git
cd dicomweb-wado-qido-stow-serverless

# CDK 배포
cd cdk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# config.py 설정
CERTIFICATE = {
    "certificate_arn": "arn:aws:acm:region:account:certificate/certificate-id",
    "stow_fqdn": "dicom.yourdomain.com",
    "certificate_auth_mode": "anonymous",
    "certificate_mode": "ACM",
    "certificate_bucket": "",
}

# AWS에 배포
cdk deploy
```

**아키텍처:**

- **S3**: DICOM 파일 저장
- **Lambda**: DICOM → DICOMweb 변환
- **DynamoDB**: 메타데이터 인덱스
- **Aurora Serverless**: QIDO 검색 엔진
- **CloudFront**: 글로벌 CDN 배포

### 5.2 클라우드 매니지드 WADO 서비스

#### 5.2.1 AWS HealthImaging (신규)

**핵심 특징:**

- **DICOMweb API 완전 호환**: WADO-RS, QIDO-RS, STOW-RS 지원
- **HIPAA 적격 서비스**: 의료 데이터 보안 규정 준수
- **페타바이트 규모**: 클라우드 네이티브 확장성
- **HTJ2K 압축**: 기존 JPEG2000보다 10배 빠른 디코딩
- **서브세컨드 응답**: 밀리세컨드 단위 이미지 접근

**OHIF 연동 예시:**

```javascript
// AWS HealthImaging용 OHIF 설정
window.config = {
  dataSources: [
    {
      sourceName: 'aws-healthimaging',
      configuration: {
        friendlyName: 'AWS HealthImaging',
        name: 'AWS-HI',
        wadoRoot:
          'https://medical-imaging.us-east-1.amazonaws.com/dicomWeb/datastore/12345678901234567890123456789012',
        qidoRoot:
          'https://medical-imaging.us-east-1.amazonaws.com/dicomWeb/datastore/12345678901234567890123456789012',

        // AWS 인증 설정
        headers: {
          Authorization: 'AWS4-HMAC-SHA256 Credential=...',
          'X-Amz-Date': '20231215T143000Z',
        },

        singlepart: true,
        supportsInstanceMetadata: true,
        supportsFuzzyMatching: true,
        supportsWildcard: false,
      },
    },
  ],
};
```

**AWS HealthImaging API 사용법:**

```javascript
// AWS SDK를 사용한 HealthImaging 접근
import {
  MedicalImagingClient,
  SearchImageSetsCommand,
} from '@aws-sdk/client-medical-imaging';

const client = new MedicalImagingClient({ region: 'us-east-1' });

// QIDO-RS와 동일한 검색
const command = new SearchImageSetsCommand({
  datastoreId: '12345678901234567890123456789012',
  searchCriteria: {
    filters: [
      {
        values: [
          {
            DICOMPatientId: 'PATIENT001',
            DICOMStudyDate: {
              DICOMStudyDateAndTime: '20231215',
            },
          },
        ],
        operator: 'EQUAL',
      },
    ],
  },
});

const response = await client.send(command);
```

**장점:**

- 인프라 관리 불필요 (서버리스)
- AWS 생태계와 완전 통합
- 자동 백업, 모니터링, 보안
- AI/ML 서비스와 바로 연동 (SageMaker, Comprehend Medical)

**고려사항:**

- 비용: 저장량과 요청량에 따른 과금
- 리전 제한: 특정 AWS 리전에서만 제공
- AWS 종속성: AWS 생태계에 강하게 결합

#### 5.2.2 Google Cloud Healthcare API

**특징:**

- **완전 관리형 DICOM 저장소**
- **FHIR와 HL7v2 통합** 지원
- **자동 스케일링** 및 고가용성

**핵심 장점:**

- Google Cloud AI/ML 서비스와 네이티브 연동 (AutoML, Vertex AI)
- 글로벌 네트워크 인프라로 뛰어난 성능
- BigQuery와 직접 연동으로 강력한 데이터 분석
- 업계 최고 수준의 보안 및 규정 준수 (HIPAA, FedRAMP)

**고려사항:**

- 비용: 네트워크 Egress 비용이 상대적으로 높음
- Google Cloud 생태계 종속성
- 복잡한 IAM 및 권한 관리

```javascript
// Google Cloud Healthcare API 설정
const endpoint =
  'https://healthcare.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/datasets/DATASET_ID/dicomStores/DICOM_STORE_ID/dicomWeb';

window.config = {
  dataSources: [
    {
      sourceName: 'gcp-healthcare',
      configuration: {
        friendlyName: 'GCP Healthcare API',
        name: 'GCP-HCA',
        wadoRoot: `${endpoint}`,
        qidoRoot: `${endpoint}`,
        headers: {
          Authorization:
            'Bearer ' +
            gapi.auth2.getAuthInstance().currentUser.get().getAuthResponse()
              .access_token,
        },
      },
    },
  ],
};
```

#### 5.2.3 Microsoft Azure DICOM Service

**특징:**

- **완전 관리형 DICOM 서비스**
- **Azure Health Data Services의 일부**로 통합 의료 데이터 플랫폼 제공
- **자동 스케일링** 및 엔터프라이즈급 보안

**핵심 장점:**

- Microsoft 생태계와 완벽 통합 (Azure AD, Office 365, Teams)
- FHIR 서비스와 네이티브 연동
- 글로벌 Azure 리전 배포로 낮은 지연시간
- 엔터프라이즈 보안 및 규정 준수 (HIPAA, SOC2, ISO 27001)

**고려사항:**

- 비용: 스토리지와 네트워크 사용량에 따른 과금
- Azure 생태계 종속성
- 상대적으로 신규 서비스 (2021년 GA)

```javascript
// Azure DICOM Service 설정
window.config = {
  dataSources: [
    {
      sourceName: 'azure-dicom',
      configuration: {
        friendlyName: 'Azure DICOM Service',
        name: 'AZURE-DICOM',
        wadoRoot: 'https://workspace-dicom.dicom.azurehealthcareapis.com/v1',
        qidoRoot: 'https://workspace-dicom.dicom.azurehealthcareapis.com/v1',
        headers: {
          Authorization: 'Bearer ' + azureAccessToken,
        },
      },
    },
  ],
};
```

### 5.3 WADO 서버 구축 방식별 종합 비용 분석

#### 5.3.1 규모별 비용 분석 기준 시나리오

### 소형 치과 (Small Dental Clinic)

**기본 현황:**

- **총 환자**: 1,000명 (누적 등록 환자)
- **저장 데이터**: 1,000명 × 100MB = **100GB**
- **환자당 평균 데이터**: 100MB (파노라마, 구강 X-Ray 위주)

**일일 진료 패턴:**

- **진료 환자**: 하루 10명 (총 환자의 **1%**)
- **월간 진료**: 10명 × 30일 = **300명**
- **일일 조회**: 10명 × 100MB = 1GB/일
- **월간 조회량**: **30GB/월**

### 중형 치과 (Medium Dental Clinic)

**기본 현황:**

- **총 환자**: 10,000명 (누적 등록 환자)
- **저장 데이터**: 10,000명 × 100MB = **1TB**
- **환자당 평균 데이터**: 100MB (파노라마, 구강 X-Ray, 구강 CT 포함)

**일일 진료 패턴:**

- **진료 환자**: 하루 100명 (총 환자의 **1%**)
- **월간 진료**: 100명 × 30일 = **3,000명**
- **일일 조회**: 100명 × 100MB = 10GB/일
- **월간 조회량**: **300GB/월**

### Public 서비스 (Public Dental Imaging Service)

**기본 현황:**

- **총 환자**: 1,000,000명 (누적 등록 환자)
- **저장 데이터**: 1,000,000명 × 100MB = **100TB**
- **환자당 평균 데이터**: 100MB (모든 치과 이미지 타입)

**일일 진료 패턴:**

- **진료 환자**: 하루 10,000명 (총 환자의 **1%**)
- **월간 진료**: 10,000명 × 30일 = **300,000명**
- **일일 조회**: 10,000명 × 100MB = 1TB/일
- **월간 조회량**: **30TB/월**

#### 5.3.2 클라우드 매니지드 서비스 비용 분석 (3가지 규모별)

### 소형 치과 비용 분석

**AWS HealthImaging (US East-1 버지니아 리전):**

```
스토리지 비용: 100GB × $0.07 = $7/월
Import Job 비용:
  - 배치 방식: 월 30개 Job (일 1회) × $0.15 = $4.5/월
  - 개별 방식: 월 300명 × $0.15 = $45/월
이미지 프레임 조회: 30GB × $0.01 = $0.3/월
메타데이터 조회: 300회 × $0.001 = $0.3/월

총 월간 비용:
  - 배치 방식: $12.1/월 ($145.2/년)
  - 개별 방식: $52.6/월 ($631.2/년)
```

**Google Cloud Healthcare API:**

```
스토리지 비용: 100GB × $0.04 = $4/월
Import 비용: 30GB × $0.10 = $3/월
Egress 비용: 30GB × $0.12 = $3.6/월
API 작업: 300회 × $2/1K = $0.6/월
총 월간 비용: $11.2/월 ($134.4/년)
```

**Azure DICOM Service:**

```
스토리지 비용: 100GB × $0.05 = $5/월
Import 트랜잭션: 30GB × $0.065 = $1.95/월
아웃바운드: 30GB × $0.087 = $2.61/월
API 요청: 300회 × $2/1K = $0.6/월
총 월간 비용: $10.16/월 ($121.9/년)
```

### 중형 치과 비용 분석

**AWS HealthImaging (US East-1 버지니아 리전):**

```
스토리지 비용: 1,000GB × $0.07 = $70/월
Import Job 비용:
  - 배치 방식: 월 30개 Job (일 1회) × $0.15 = $4.5/월
  - 개별 방식: 월 3,000명 × $0.15 = $450/월
이미지 프레임 조회: 300GB × $0.01 = $3/월
메타데이터 조회: 3,000회 × $0.001 = $3/월

총 월간 비용:
  - 배치 방식: $80.5/월 ($966/년)
  - 개별 방식: $526/월 ($6,312/년)
```

**Google Cloud Healthcare API:**

```
스토리지 비용: 1,000GB × $0.04 = $40/월
Import 비용: 300GB × $0.10 = $30/월
Egress 비용: 300GB × $0.12 = $36/월
API 작업: 3,000회 × $2/1K = $6/월
총 월간 비용: $112/월 ($1,344/년)
```

**Azure DICOM Service:**

```
스토리지 비용: 1,000GB × $0.05 = $50/월
Import 트랜잭션: 300GB × $0.065 = $19.5/월
아웃바운드: 300GB × $0.087 = $26.1/월
API 요청: 3,000회 × $2/1K = $6/월
총 월간 비용: $101.6/월 ($1,219.2/년)
```

### Public 서비스 비용 분석

**AWS HealthImaging (US East-1 버지니아 리전):**

```
스토리지 비용: 100,000GB × $0.07 = $7,000/월
Import Job 비용:
  - 현실적 배치 방식: 100명씩 묶어서 처리
    → 10,000명/일 ÷ 100명/배치 = 100개 Job/일
    → 월 3,000개 Job (100개/일 × 30일) × $0.15 = $450/월
  - 개별 방식: 월 300,000명 × $0.15 = $45,000/월
이미지 프레임 조회: 30,000GB × $0.01 = $300/월
메타데이터 조회: 300,000회 × $0.001 = $300/월

총 월간 비용:
  - 현실적 배치 방식: $8,050/월 ($96,600/년)
  - 개별 방식: $52,600/월 ($631,200/년)
```

**Google Cloud Healthcare API:**

```
스토리지 비용: 100,000GB × $0.04 = $4,000/월
Import 비용: 30,000GB × $0.10 = $3,000/월
Egress 비용: 30,000GB × $0.12 = $3,600/월
API 작업: 300,000회 × $2/1K = $600/월
총 월간 비용: $11,200/월 ($134,400/년)
```

**Azure DICOM Service:**

```
스토리지 비용: 100,000GB × $0.05 = $5,000/월
Import 트랜잭션: 30,000GB × $0.065 = $1,950/월
아웃바운드: 30,000GB × $0.087 = $2,610/월
API 요청: 300,000회 × $2/1K = $600/월
총 월간 비용: $10,160/월 ($121,920/년)
```

#### 5.3.3 오픈소스 솔루션 AWS 기반 월간 운영 비용 (3가지 규모별)

### 소형 치과 오픈소스 솔루션

**DCM4CHEE on AWS (소형 치과 구성):**

```
EC2 인스턴스:
- c5.small × 1 = $17/월 (소형 치과 규모)

스토리지:
- S3 Standard: 100GB × $0.023 = $2.3/월
- S3 백업: 100GB × $0.004 = $0.4/월 (IA 백업)

데이터베이스:
- RDS PostgreSQL (db.t3.small): $15/월 (소형 치과 적합)

네트워크:
- 아웃바운드: 30GB × $0.09 = $2.7/월

관리 비용 (추정):
- 시스템 관리자 10% = $600/월

총 월간 비용: $637.4/월 ($7,648.8/년)
```

**Orthanc on AWS (소형 치과 구성):**

```
EC2 인스턴스:
- c5.small = $17/월 (100GB 데이터에 적합)

스토리지:
- S3 Standard: 100GB × $0.023 = $2.3/월
- EBS 백업: 100GB × $0.05 = $5/월

네트워크:
- 아웃바운드: 30GB × $0.09 = $2.7/월

관리 비용 (추정):
- 시스템 관리자 10% = $600/월

총 월간 비용: $627/월 ($7,524/년)
```

### 중형 치과 오픈소스 솔루션

**DCM4CHEE on AWS (중형 치과 구성):**

```
EC2 인스턴스 (2대):
- c5.large × 2 = $153/월 (중형 치과 규모에 맞게 조정)
- Load Balancer = $23/월

스토리지:
- S3 Standard: 1,000GB × $0.023 = $23/월
- S3 백업: 1,000GB × $0.004 = $4/월 (IA 백업)

데이터베이스:
- RDS PostgreSQL (db.r5.large): $211/월 (중형 치과 적합)

네트워크:
- 아웃바운드: 300GB × $0.09 = $27/월

관리 비용 (추정):
- DevOps 엔지니어 25% = $1,500/월

총 월간 비용: $1,941/월 ($23,292/년)
```

**Orthanc on AWS (중형 치과 구성):**

```
EC2 인스턴스:
- c5.medium = $38/월 (1TB 데이터에 적합)

스토리지:
- S3 Standard: 1,000GB × $0.023 = $23/월
- EBS 백업: 1,000GB × $0.05 = $50/월

네트워크:
- 아웃바운드: 300GB × $0.09 = $27/월

관리 비용 (추정):
- 시스템 관리자 15% = $900/월

총 월간 비용: $1,038/월 ($12,456/년)
```

### Public 서비스 오픈소스 솔루션

**DCM4CHEE on AWS (Public 서비스 클러스터):**

```
EC2 인스턴스 (대규모 클러스터):
- c5.4xlarge × 10 = $1,536/월 (고성능 클러스터)
- Load Balancer = $23/월

스토리지:
- S3 Standard: 100,000GB × $0.023 = $2,300/월
- S3 백업: 100,000GB × $0.004 = $400/월 (IA 백업)

데이터베이스:
- RDS PostgreSQL (db.r5.12xlarge): $2,900/월 (대규모 용량)

네트워크:
- 아웃바운드: 30,000GB × $0.09 = $2,700/월

관리 비용 (추정):
- DevOps 엔지니어 167% = $10,000/월

총 월간 비용: $19,859/월 ($238,308/년)
```

**Orthanc on AWS (Public 서비스 클러스터):**

```
EC2 인스턴스:
- c5.4xlarge × 8 = $1,229/월 (대규모 클러스터)
- Load Balancer = $23/월

스토리지:
- S3 Standard: 100,000GB × $0.023 = $2,300/월
- EBS 백업: 100,000GB × $0.05 = $5,000/월

네트워크:
- 아웃바운드: 30,000GB × $0.09 = $2,700/월

관리 비용 (추정):
- 시스템 관리자 133% = $8,000/월

총 월간 비용: $19,252/월 ($231,024/년)
```

#### 5.3.4 종합 비교표 (3가지 규모별 - AWS HI 배치 방식 기준 100%)

### 소형 치과 (1,000명 환자)

| 구축 방식          | 초기 비용 | 월간 운영 비용 | 연간 총 비용 | AWS HI 대비 | 운영 복잡도 | 확장성 | 커스터마이징 |
| ------------------ | --------- | -------------- | ------------ | ----------- | ----------- | ------ | ------------ |
| **AWS HI (배치)**  | $0        | $12            | $145         | **100%**    | 낮음        | 자동   | 제한적       |
| **AWS HI (개별)**  | $0        | $53            | $631         | **435%**    | 낮음        | 자동   | 제한적       |
| **Azure DICOM**    | $0        | $10            | $122         | **84%**     | 낮음        | 자동   | 제한적       |
| **GCP Healthcare** | $0        | $11            | $134         | **93%**     | 낮음        | 자동   | 제한적       |
| **Orthanc (AWS)**  | $500      | $627           | $7,524       | **5,183%**  | 중간        | 수동   | 높음         |
| **DCM4CHEE (AWS)** | $1,000    | $637           | $7,649       | **5,269%**  | 높음        | 수동   | 높음         |

### 중형 치과 (10,000명 환자)

| 구축 방식          | 초기 비용 | 월간 운영 비용 | 연간 총 비용 | AWS HI 대비 | 운영 복잡도 | 확장성 | 커스터마이징 |
| ------------------ | --------- | -------------- | ------------ | ----------- | ----------- | ------ | ------------ |
| **AWS HI (배치)**  | $0        | $81            | $966         | **100%**    | 낮음        | 자동   | 제한적       |
| **AWS HI (개별)**  | $0        | $526           | $6,312       | **653%**    | 낮음        | 자동   | 제한적       |
| **Azure DICOM**    | $0        | $102           | $1,219       | **126%**    | 낮음        | 자동   | 제한적       |
| **GCP Healthcare** | $0        | $112           | $1,344       | **139%**    | 낮음        | 자동   | 제한적       |
| **Orthanc (AWS)**  | $500      | $1,038         | $12,456      | **1,289%**  | 중간        | 수동   | 높음         |
| **DCM4CHEE (AWS)** | $2,000    | $1,941         | $23,292      | **2,410%**  | 높음        | 수동   | 높음         |

### Public 서비스 (1,000,000명 환자)

| 구축 방식          | 초기 비용 | 월간 운영 비용 | 연간 총 비용 | AWS HI 대비 | 운영 복잡도 | 확장성 | 커스터마이징 |
| ------------------ | --------- | -------------- | ------------ | ----------- | ----------- | ------ | ------------ |
| **AWS HI (배치)**  | $0        | $8,050         | $96,600      | **100%**    | 낮음        | 자동   | 제한적       |
| **AWS HI (개별)**  | $0        | $52,600        | $631,200     | **653%**    | 낮음        | 자동   | 제한적       |
| **Azure DICOM**    | $0        | $10,160        | $121,920     | **126%**    | 낮음        | 자동   | 제한적       |
| **GCP Healthcare** | $0        | $11,200        | $134,400     | **139%**    | 낮음        | 자동   | 제한적       |
| **Orthanc (AWS)**  | $5,000    | $19,252        | $231,024     | **239%**    | 중간        | 수동   | 높음         |
| **DCM4CHEE (AWS)** | $10,000   | $19,859        | $238,308     | **247%**    | 높음        | 수동   | 높음         |

**핵심 발견사항 (3가지 규모별):**

### 소형 치과 (1,000명 환자)

1. **AWS HealthImaging 배치 방식이 압도적 우위**

   - 연간 $145로 가장 경제적
   - 오픈소스 솔루션 대비 **50배 저렴**
   - 클라우드 서비스 간 차이 적음 (84%-93%)

2. **Import Job 전략의 중요성**
   - 배치 방식: **연간 $145**
   - 개별 방식: **연간 $631** → **4배 비용 증가**

### 중형 치과 (10,000명 환자)

1. **AWS HealthImaging의 Import Job 전략이 비용에 결정적 영향**

   - 배치 방식: **연간 $966** → 가장 경제적
   - 개별 방식: **연간 $6,312** → **7배 비용 증가**

2. **클라우드 서비스 간 비용 차이**

   - AWS HI (배치): **연간 $966** (100%)
   - Azure DICOM: **연간 $1,219** (126%)
   - GCP Healthcare: **연간 $1,344** (139%)

3. **오픈소스 솔루션과의 비교**
   - Orthanc: **연간 $12,456** (1,289%)
   - DCM4CHEE: **연간 $23,292** (2,410%)

### Public 서비스 (1,000,000명 환자)

1. **AWS HealthImaging 현실적 배치 방식이 여전히 최고**

   - 연간 $96,600으로 가장 경제적 (100명씩 묶어서 처리)
   - 대규모에서도 클라우드 서비스가 우위

2. **오픈소스 솔루션의 경쟁력 향상**

   - Orthanc: **연간 $231,024** (239%)
   - DCM4CHEE: **연간 $238,308** (247%)
   - 규모가 클수록 격차 축소

3. **Import Job 전략의 극대화된 중요성**
   - 현실적 배치 vs 개별: 연간 $534,600 차이 (**6.5배 증가**)
   - 100명 단위 배치 처리로 시스템 안정성과 비용 효율성 균형

#### 5.3.6 숨겨진 비용 요소

**클라우드 매니지드 서비스:**

- 장점: 관리 비용 없음, 자동 백업, 보안 패치
- 단점: 데이터 전송 비용 높음, 벤더 종속성

**오픈소스 솔루션:**

- 장점: 데이터 완전 제어, 커스터마이징 자유
- 단점: 높은 관리 비용, 보안 책임, 장애 대응

#### 5.3.7 비용 최적화 전략

**AWS HealthImaging 최적화:**

```javascript
// 지역별 데이터 계층화
const optimizeCosts = {
  hotData: '최근 30일 - 빠른 접근',
  coldData: '30-90일 - 느린 접근 (-60% 비용)',
  archiveData: '90일+ - 아카이브 (-80% 비용)',
};
```

**오픈소스 솔루션 최적화:**

```bash
# 스토리지 계층화
aws s3 cp --storage-class STANDARD_IA  # 30일 후
aws s3 cp --storage-class GLACIER     # 90일 후
aws s3 cp --storage-class DEEP_ARCHIVE # 1년 후
```

#### 5.3.7 권장사항 (3가지 규모별)

### 소형 치과 (< 1TB) 권장사항

**1순위: AWS HealthImaging (배치 방식)**

- 연간 $145 (가장 저렴)
- 초기 비용 없음, 관리 불필요
- 자동 스케일링 및 백업

**2순위: Azure DICOM Service**

- 연간 $122 (AWS 대비 84%)
- Microsoft 생태계 기업에 적합

### 중형 치과 (1-10TB) 권장사항

**1순위: AWS HealthImaging (배치 방식)**

- 연간 $966 (최고 효율성)
- Import Job 전략 중요 (일일 배치 처리)
- 치과 특화 설정 (PANORAMIC, INTRAORAL, CBCT)

**2순위: Azure DICOM Service**

- 연간 $1,219 (AWS 대비 126%)
- 기존 Microsoft 인프라 활용시

### Public 서비스 (100TB+) 권장사항

**1순위: AWS HealthImaging (현실적 배치 방식)**

- 연간 $96,600 (여전히 최고)
- 100명 단위 배치 처리로 시스템 안정성 확보
- 대규모 트래픽 자동 처리
- Import Job 최적화 필수

**2순위: DCM4CHEE 클러스터 (특수 요구사항시)**

- 연간 $238,308 (AWS 대비 261%)
- 완전한 커스터마이징 필요시
- 데이터 완전 제어 필요시

### 규모별 Break-even 포인트

- **< 1TB**: 클라우드 서비스 압도적 우위 (50배 차이)
- **1-10TB**: AWS HI 배치 방식 절대 우위 (12-24배 차이)
- **10-100TB**: 클라우드 서비스 여전히 우위 (2-3배 차이)
- **100TB+**: 특수 요구사항 고려하여 선택적 검토

#### 5.3.8 AWS HealthImaging Import Job 최적화 전략

**Import Job 비용 구조의 핵심:**

AWS HealthImaging에서 **Import Job 비용이 전체 비용을 좌우**하는 핵심 요소입니다.

| Import 전략         | Job 수 (월) | Job 비용 | 총 월간 비용 | 비용 차이 |
| ------------------- | ----------- | -------- | ------------ | --------- |
| **실시간 (환자별)** | 1,000건     | $150     | $335         | 기준      |
| **일일 배치**       | 30건        | $4.5     | $190         | **-43%**  |
| **주간 배치**       | 4건         | $0.6     | $186         | **-44%**  |

**최적화 전략:**

```javascript
// 소형/중형 치과: 일일 배치 처리 (권장)
const dailyBatch = {
  schedule: '매일 오전 2시',
  patients: '하루 신규 환자 50명',
  dicomFiles: '평균 200-300개 파일',
  jobCost: '$0.15',
  advantages: ['비용 최적화 (43% 절약)', '안정적인 처리', '관리 용이성'],
};

// Public 서비스: 100명 단위 배치 처리 (권장)
const publicServiceBatch = {
  schedule: '하루 100회 처리 (100명씩)',
  batchSize: '100명/배치',
  patients: '하루 10,000명',
  jobCost: '$0.15 × 3,000개/월 = $450/월',
  advantages: [
    '시스템 안정성 (적정 배치 크기)',
    '에러 처리 용이성',
    '네트워크 부하 분산',
    '실시간성과 효율성의 균형',
  ],
};

// 비권장: 실시간 처리
const realtimeProcessing = {
  schedule: '환자별 즉시',
  trigger: '촬영 완료시마다',
  jobCost: '$0.15 × 300,000명 = $45,000/월',
  disadvantages: [
    '높은 비용 (100배 증가)',
    'API 호출량 급증',
    '네트워크 부하',
    '시스템 안정성 리스크',
  ],
};
```

**하이브리드 전략 (권장):**

1. **S3 버퍼링**: 실시간 촬영 → S3 즉시 저장
2. **배치 Import**: S3 → AWS HI (일일 1회)
3. **즉시 조회**: S3에서 임시 조회, HI에서 장기 조회

이 전략으로 **실시간성과 비용 효율성을 동시에** 확보할 수 있습니다.

#### 5.3.9 프로덕션 배포 고려사항

**보안 및 인증:**

```javascript
// JWT 토큰 기반 인증
const getAuthorizationHeader = () => {
  const token = localStorage.getItem('authToken');
  return {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
};

// OHIF에서 인증 헤더 사용
window.config = {
  dataSources: [
    {
      configuration: {
        headers: getAuthorizationHeader(),
        requestInterceptor: (request) => {
          // 토큰 만료 체크 및 갱신
          if (isTokenExpired()) {
            request.headers.Authorization = `Bearer ${refreshToken()}`;
          }
          return request;
        },
      },
    },
  ],
};
```

**고가용성 구성:**

**DCM4CHEE 클러스터링:**

```yaml
# Docker Swarm을 이용한 DCM4CHEE 클러스터
version: '3.8'
services:
  dcm4chee-arc:
    image: dcm4che/dcm4chee-arc-psql:5.31.0
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.role == worker
    networks:
      - dcm4chee-network

  nginx-lb:
    image: nginx:alpine
    ports:
      - '80:80'
      - '443:443'
    deploy:
      replicas: 2
    configs:
      - source: nginx-config
        target: /etc/nginx/nginx.conf

configs:
  nginx-config:
    external: true

networks:
  dcm4chee-network:
    driver: overlay
```

**모니터링 및 로깅:**

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'dcm4chee'
    static_configs:
      - targets: ['dcm4chee:9990']
    metrics_path: '/metrics'

  - job_name: 'orthanc'
    static_configs:
      - targets: ['orthanc:8042']
    metrics_path: '/plugins/prometheus/metrics'
```

**데이터 백업 전략:**

**자동 백업 스크립트:**

```bash
#!/bin/bash
# dcm4chee-backup.sh

# 데이터베이스 백업
docker exec dcm4chee-db pg_dump -U dcm4chee dcm4chee > /backup/db/dcm4chee_$(date +%Y%m%d_%H%M%S).sql

# DICOM 파일 백업 (증분)
rsync -av --backup --backup-dir=/backup/dicom/incremental_$(date +%Y%m%d) \
  /var/lib/docker/volumes/dcm4chee_storage/_data/ \
  /backup/dicom/latest/

# S3로 오프사이트 백업
aws s3 sync /backup/ s3://hospital-dicom-backup/$(date +%Y%m%d)/
```

#### 5.3.10 치과 환경별 권장 구성

**소규모 치과 (< 1TB):**

```bash
# 권장 솔루션: Orthanc + Docker
docker-compose.yml:
  orthanc:
    image: jodogne/orthanc-plugins
    ports: ["8042:8042", "4242:4242"]
    volumes:
      - orthanc-db:/var/lib/orthanc/db
      - orthanc-storage:/var/lib/orthanc/storage
    environment:
      - ORTHANC__DICOM_WEB__ENABLE=true
```

**중형 치과 (1-10TB):**

```javascript
// 권장 솔루션: AWS HealthImaging (배치 방식)
window.config = {
  dataSources: [
    {
      sourceName: 'aws-healthimaging',
      configuration: {
        friendlyName: '치과 AWS HealthImaging',
        wadoRoot:
          'https://medical-imaging.amazonaws.com/datastore/dental-clinic',
        qidoRoot:
          'https://medical-imaging.amazonaws.com/datastore/dental-clinic',
        headers: {
          Authorization: 'Bearer ' + awsCredentials.accessToken,
        },
        // 치과 특화 설정
        imageTypes: ['PANORAMIC', 'INTRAORAL', 'CBCT'],
        batchImport: true, // 일일 배치 처리로 비용 최적화
      },
    },
  ],
};
```

**Public 서비스 (> 50TB):**

```javascript
// 권장 솔루션: AWS HealthImaging + 하이브리드 구성
window.config = {
  dataSources: [
    {
      sourceName: 'onprem-primary',
      configuration: {
        friendlyName: '치과 PACS (최근 6개월)',
        wadoRoot: 'https://pacs.dental-clinic.com/dcm4chee/rs',
        priority: 1, // 우선순위 높음
      },
    },
    {
      sourceName: 'cloud-archive',
      configuration: {
        friendlyName: 'AWS 아카이브 (6개월 이전)',
        wadoRoot: 'https://medical-imaging.amazonaws.com/datastore/archive',
        priority: 2, // 우선순위 낮음
      },
    },
  ],
};
```

### 최종 결론

**3가지 규모 모든 치과 환경에서 AWS HealthImaging 현실적 배치 방식이 최고의 효율성**을 보여줍니다:

- **소형 치과**: 연간 $145 (오픈소스 대비 50배 저렴)
- **중형 치과**: 연간 $966 (오픈소스 대비 12배 저렴)
- **Public 서비스**: 연간 $96,600 (오픈소스 대비 2.4배 저렴)

**핵심 성공 요소**: Import Job 현실적 배치 처리 (4-6.5배 절약) + 치과 진료 패턴 최적화 (1% 활동률) + 100명 단위 배치로 시스템 안정성 확보

### 5.2 WADO 서버 응답 예시

#### 5.2.1 QIDO-RS Study 검색 응답

```json
[
  {
    "0008,0020": { "vr": "DA", "Value": ["20231215"] },
    "0008,0030": { "vr": "TM", "Value": ["143000.000000"] },
    "0008,0050": { "vr": "SH", "Value": ["ACC12345"] },
    "0008,0061": { "vr": "CS", "Value": ["CT"] },
    "0010,0010": { "vr": "PN", "Value": [{ "Alphabetic": "PATIENT^TEST" }] },
    "0010,0020": { "vr": "LO", "Value": ["PID12345"] },
    "0020,000D": { "vr": "UI", "Value": ["1.2.840.113619.2.55.3.604"] },
    "0020,0010": { "vr": "SH", "Value": ["STU12345"] }
  }
]
```

#### 5.2.2 WADO-RS 메타데이터 응답

```json
{
  "00080016": { "vr": "UI", "Value": ["1.2.840.10008.5.1.4.1.1.2"] },
  "00080018": { "vr": "UI", "Value": ["1.2.276.0.7230010.3.1.4.8323329.5576"] },
  "00280010": { "vr": "US", "Value": [512] },
  "00280011": { "vr": "US", "Value": [512] },
  "7FE00010": {
    "vr": "OW",
    "BulkDataURI": "/studies/1.2.3/series/4.5.6/instances/7.8.9/bulkdata/7fe00010"
  }
}
```

## 6. 실제 병원에서의 WADO 활용

### 6.1 의료 워크플로우

```
1. 환자 CT 촬영
   ↓
2. DICOM 파일 PACS 서버 저장
   ↓
3. WADO 서버에서 DICOMweb API 제공
   ↓
4. OHIF 뷰어에서 QIDO-RS로 검색
   ↓
5. WADO-RS로 이미지 데이터 다운로드
   ↓
6. 웹 브라우저에서 3D 렌더링
```

### 6.2 보안 및 인증

```javascript
// OHIF에서 인증 헤더 설정
const authHeader = {
  Authorization: `Bearer ${jwt_token}`,
  'X-Api-Key': api_key,
};

const client = new api.DICOMwebClient({
  url: wadoRoot,
  headers: authHeader,
});
```

## 7. 향후 WADO 발전 방향

### 7.1 새로운 기능들

- **FHIR 연동**: HL7 FHIR와 DICOMweb 통합
- **AI 모델 연동**: WADO + AI 분석 결과 제공
- **실시간 스트리밍**: WebRTC를 활용한 실시간 의료 영상 전송

### 7.2 성능 개선

- **HTTP/2 Push**: 예측 기반 데이터 전송
- **압축 최적화**: DICOM 전용 압축 알고리즘
- **엣지 캐싱**: CDN을 활용한 글로벌 의료 영상 캐싱

## 8. 결론

**치과 DICOM 환경의 핵심 발견:**

- **AWS HealthImaging 배치 방식**이 모든 규모에서 압도적 우위
- **Import Job 전략**이 비용에 결정적 영향 (59-62% 차이)
- **100MB/환자 데이터**로 병원 대비 절반 수준의 효율성
- **클라우드 서비스**가 오픈소스 대비 2-45배 경제적

**치과 환경 특화 WADO 장점:**

- **치과 이미지 타입 최적화**: PANORAMIC, INTRAORAL, CBCT 지원
- **국제 표준 준수**로 치과 PACS 시스템과 완벽 호환
- **풍부한 메타데이터**로 정확한 치과 진료 정보 제공
- **성숙한 생태계**와 다양한 치과 특화 도구 지원

**POC2의 장점:**

- **압축 스트리밍**으로 빠른 사용자 경험
- **단순한 구조**로 개발 및 유지보수 용이
- **자유로운 최적화** 가능

### 8.1 권장사항

**의료 기관용 시스템**: WADO 표준 준수 (OHIF 방식)
**클라우드 뷰어 서비스**: POC2 방식으로 사용자 경험 최적화

두 방식 모두 각각의 장점이 있으며, **사용 목적과 환경**에 따라 선택하는 것이 중요합니다!

---

## 업데이트 로그

- 2025-01-08: 초기 문서 작성 및 WADO 표준 개요, OHIF 구현 분석 완료
- 2025-01-08: **WADO 서버 구축 방안 대폭 확장** - DCM4CHEE, Orthanc 상세 설치 가이드 추가
- 2025-01-08: **AWS HealthImaging 분석 추가** - DICOMweb API 호환성, HIPAA 적격성, HTJ2K 압축 기술 분석
- 2025-01-08: **클라우드 매니지드 WADO 서비스** - AWS HealthImaging, Google Cloud Healthcare API, Azure DICOM Service 비교 분석
- 2025-01-08: **프로덕션 배포 가이드** - 보안/인증, 고가용성, 모니터링, 백업 전략 및 병원 규모별 권장 구성 추가
- 2025-01-08: **비용 분석 정확성 대폭 개선** - AWS HI Import Job 비용 구조 정정 (GB당 → Job당 $0.15), 중형 병원 기준 시나리오 재정의, Azure/GCP 비용 재계산, Import Job 최적화 전략 추가
- 2025-01-08: **통합 시나리오 기준 비용 분석 완료** - 기존+신규 환자 통합 시나리오 적용, 클라우드 서비스 간 비용 격차 현실적 조정 (Azure 1.9배, GCP 2.2배)
- 2025-01-10: **현실적 진료 패턴 반영 및 구조 단순화** - 신규 환자 → 진료 환자로 용어 변경, 환자 수 고정 (성장 모델 제거), 진료 환자수를 총 환자의 1%로 현실적 조정, 월간/연간 비용 중심 분석, Import Job 전략의 비용 영향 극대화 (4-7배 차이) 분석 완료
- 2025-01-10: **Public 서비스 Import Job 전략 현실화** - 하루 10,000명을 1회 처리에서 100명씩 100회 처리로 변경 (월 30개 Job → 3,000개 Job), 시스템 안정성과 비용 효율성 균형 맞춤, 연간 비용 $91,254 → $96,600으로 조정, 현실적 배치 처리 전략 수립
