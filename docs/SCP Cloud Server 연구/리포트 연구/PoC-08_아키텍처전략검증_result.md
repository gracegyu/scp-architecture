# PoC-08 결과 보고서: 아키텍처 전략 검증 (내부 서비스 통합 방식)

## 요약

- **목표**: Ewoosoft 내부 Cloud 서비스들(SCP Cloud, Imaging Cloud, Analytics Cloud 등)에 통합할 리포트 시스템의 최적 아키텍처 결정
- **전제 조건**: **내부 Cloud 서비스 전용** - 외부 고객사 판매 계획 없음, 자사 Cloud 서비스에만 통합
- **주 사용처**: **SCP Cloud** (Desktop 제품 E2, E3, EzOrtho, CleverOne 리포트 import 및 통합 관리)
- **비교 분석**: Shared Library vs Microservice vs Monolithic 통합 방식
- **권장 방식**: **Shared Library (NPM Private Package)** - TypeScript React 컴포넌트 라이브러리
- **핵심 근거**: 내부 Cloud 서비스 간 코드 공유 + 각 서비스별 독립 배포 + 최소 운영 비용 + 중복 개발 제거
- **비용 효율**: 단일 개발 + 다중 활용, 추가 인프라 불필요, 개발 리소스 최소화
- **산출물**: Shared Library 아키텍처 설계, 통합 가이드, 버전 관리 전략, Monorepo 구조

---

## 1. 개요

### 1.1 검증 목표

SCP Cloud Report 시스템을 **Ewoosoft 내부 Cloud 서비스들**(SCP Cloud, Imaging Cloud, Analytics Cloud 등)에 통합하기 위한 최적 아키텍처를 결정합니다. 외부 고객사 판매가 아닌 **자사 Cloud 서비스 내부 통합**이므로, 개발 효율성과 유지보수성을 최우선으로 고려합니다.

**핵심 질문**:
- SCP Cloud 및 향후 신규 Cloud 서비스들이 리포트 기능을 어떻게 통합할 것인가?
- 공통 코드를 어떻게 효율적으로 공유할 것인가?
- 각 Cloud 서비스의 독립적인 배포 주기를 어떻게 보장할 것인가?
- 추가 인프라 비용 없이 어떻게 구현할 것인가?
- 중복 개발을 어떻게 최소화할 것인가?

**사용 시나리오**:
- **SCP Cloud**: 기존 E2, E3, EzOrtho, CleverOne 리포트를 import하여 편집/관리
- **Imaging Cloud** (가상): 의료 영상 분석 리포트 생성 및 관리
- **Analytics Cloud** (가상): 진료 데이터 분석 리포트 생성 및 관리

### 1.2 내부 서비스 전용의 의미

**외부 판매 없음**:
- NPM Public Registry 배포 불필요
- 외부 고객사 지원 불필요
- 라이센스 관리 시스템 불필요
- 외부 문서화 최소화

**내부 통합 목적**:
- **SCP Cloud**: 기존 Desktop 제품(E2, E3, EzOrtho, CleverOne)의 리포트를 import하여 통합 관리
- **신규 Cloud 서비스**: Imaging Cloud, Analytics Cloud 등 향후 개발될 서비스에서 리포트 기능 활용
- 각 Cloud 서비스는 독립적이지만 공통 리포트 엔진 공유
- 통일된 리포트 편집 경험 제공
- 개발 리소스 효율화

**Desktop 제품과의 관계**:
- E2, E3, EzOrtho, CleverOne은 **Cloud 전환 계획 없음** (Desktop 제품으로 유지)
- 이들 제품에서 생성된 리포트 파일을 SCP Cloud로 **Migration/Import**
- SCP Cloud에서 통합 편집 및 관리

### 1.3 선행 PoC 반영

| PoC    | 결정 사항                          | 아키텍처 영향                                              |
| ------ | ---------------------------------- | ---------------------------------------------------------- |
| PoC-01 | JSON 포맷, TypeScript              | Shared Library로 타입 정의 공유 용이                       |
| PoC-04 | React 기반 렌더링                  | React 컴포넌트 라이브러리 형태로 배포                      |
| PoC-05 | 외부 라이브러리 의존성             | Shared Library의 peerDependencies로 관리                   |
| PoC-06 | 통합 Element 스키마                | 모든 내부 서비스가 동일한 데이터 포맷 사용                 |
| PoC-07 | Migration 시스템                   | Shared Library에 Migration 유틸리티 포함                   |

### 1.4 평가 기준

**1. 개발 효율성**:
- 중복 개발 제거
- 코드 재사용성
- 개발 생산성

**2. 운영 효율성**:
- 배포 복잡도
- 버전 관리
- 유지보수 비용

**3. 기술적 독립성**:
- 각 서비스의 독립 배포
- 기술 스택 유연성
- 장애 격리

---

## 2. 아키텍처 비교 분석

### 2.1 Shared Library 방식 (권장)

**개념**: NPM Private Package로 배포, 각 서비스가 라이브러리로 통합

**아키텍처**:
```
┌─────────────────────────────────────────────────────────┐
│              NPM Private Registry                        │
│         @ewoosoft/scp-report-library                     │
│                                                           │
│  - Report Editor Components                              │
│  - Report Viewer Components                              │
│  - Element Rendering Engine                              │
│  - Migration Tools (E2/E3/EzOrtho/CleverOne)            │
│  - TypeScript Types                                      │
└─────────────────────────────────────────────────────────┘
         │                │                │
         ↓                ↓                ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  SCP Cloud   │  │Imaging Cloud │  │Analytics Cloud│
│  (주 사용처) │  │  (가상)      │  │  (가상)       │
│              │  │              │  │              │
│ npm install  │  │ npm install  │  │ npm install  │
│ @ewoosoft/   │  │ @ewoosoft/   │  │ @ewoosoft/   │
│ scp-report   │  │ scp-report   │  │ scp-report   │
│              │  │              │  │              │
│ 독립 배포    │  │ 독립 배포    │  │ 독립 배포    │
└──────────────┘  └──────────────┘  └──────────────┘
         ↑
         │ Import/Migration
         │
┌────────────────────────────────────────────────────────┐
│        Desktop 제품 (Cloud 전환 계획 없음)             │
│  E2, E3, EzOrtho, CleverOne                            │
│  → 리포트 파일 생성 → SCP Cloud로 Import               │
└────────────────────────────────────────────────────────┘
```

**사용 예시**:

```typescript
// SCP Cloud에서 사용 (주 사용처)
import { ReportEditor, ReportViewer } from '@ewoosoft/scp-report-library'
import '@ewoosoft/scp-report-library/dist/styles.css'

function SCPReportPage() {
  return (
    <div>
      <h1>SCP Cloud Report</h1>
      <ReportEditor
        reportId={reportId}
        onSave={handleSave}
        theme="scp-theme"
        // 모든 Element 타입 지원 (E2, E3, EzOrtho, CleverOne import)
        enabledElements={['imageBox', 'textBox', 'toothBox', 'annotation']}
      />
    </div>
  )
}
```

```typescript
// Imaging Cloud에서 사용 (가상 예시)
import { ReportEditor } from '@ewoosoft/scp-report-library'

function ImagingReportPage() {
  return (
    <div>
      <h1>Imaging Analysis Report</h1>
      <ReportEditor
        reportId={reportId}
        onSave={handleSave}
        theme="imaging-theme"
        // 의료 영상 분석에 필요한 Element만 활성화
        enabledElements={['imageBox', 'annotation', 'textBox']}
      />
    </div>
  )
}
```

```typescript
// Analytics Cloud에서 사용 (가상 예시)
import { ReportViewer } from '@ewoosoft/scp-report-library'

function AnalyticsReportPage() {
  return (
    <div>
      <h1>Analytics Report</h1>
      <ReportViewer
        report={analyticsReport}
        theme="analytics-theme"
        // 분석 결과 리포트 뷰어
      />
    </div>
  )
}
```

**패키지 구조**:
```
@ewoosoft/scp-report-library/
├── dist/
│   ├── index.js          # UMD 번들
│   ├── index.esm.js      # ES Module
│   ├── index.d.ts        # TypeScript 타입
│   └── styles.css        # 스타일시트
├── src/
│   ├── components/       # React 컴포넌트
│   │   ├── ReportEditor.tsx
│   │   ├── ReportViewer.tsx
│   │   └── Elements/
│   ├── engine/           # 렌더링 엔진
│   ├── migration/        # Migration 도구
│   ├── utils/            # 유틸리티
│   └── types/            # TypeScript 타입
├── package.json
└── README.md
```

#### 2.1.1 장점

**1. 개발 효율성 극대화**:
- **단일 코드베이스**: 리포트 기능을 한 번만 개발
- **중복 제거**: SCP Cloud, Imaging Cloud, Analytics Cloud 등 모든 Cloud 서비스에서 동일한 코드 재사용
- **타입 안정성**: TypeScript 타입 정의 공유로 타입 안정성 보장

**2. 최소 운영 비용**:
- **추가 인프라 불필요**: 별도 서버, DB, 스토리지 없음
- **NPM Private Registry**: Azure Artifacts 또는 GitHub Packages 활용 (기존 인프라)
- **배포 자동화**: CI/CD 파이프라인 1개만 관리

**3. 독립적 배포**:
```
Shared Library 업데이트:
  v1.0.0 → v1.1.0 배포

각 Cloud 서비스의 선택적 업데이트:
  - SCP Cloud: v1.1.0으로 즉시 업데이트
  - Imaging Cloud: v1.0.0 유지 (안정성 우선)
  - Analytics Cloud: v1.1.0으로 업데이트

각 Cloud 서비스는 독립적으로 배포 가능
```

**4. 버전 관리 유연성**:
```json
// SCP Cloud package.json
{
  "dependencies": {
    "@ewoosoft/scp-report-library": "^1.1.0"  // 최신 버전 사용
  }
}

// Imaging Cloud package.json
{
  "dependencies": {
    "@ewoosoft/scp-report-library": "1.0.5"   // 특정 버전 고정
  }
}

// Analytics Cloud package.json
{
  "dependencies": {
    "@ewoosoft/scp-report-library": "^1.1.0"  // 최신 버전 사용
  }
}
```

**5. 빠른 기능 배포**:
- 신규 기능을 Shared Library에 추가
- 각 서비스가 필요할 때 업데이트
- 강제 업데이트 불필요

**6. 테스트 효율성**:
- Shared Library 단위 테스트 1회
- 각 서비스에서 통합 테스트만 수행
- 테스트 중복 최소화

#### 2.1.2 단점

**1. 버전 동기화 관리**:
```
문제 상황:
  - SCP Cloud: v1.2.0 사용
  - Imaging Cloud: v1.0.0 사용 (업데이트 안 함)
  - Analytics Cloud: v1.1.0 사용

결과:
  - 서비스별로 다른 기능/버그 존재
  - 버그 수정 시 여러 버전 지원 필요
```

**완화 방안**:
- Semantic Versioning 엄격 준수
- Breaking Change 최소화
- 버전별 지원 정책 명확화 (최신 2개 Major 버전만 지원)

**2. 의존성 충돌 가능성**:
```typescript
// SCP Cloud
{
  "dependencies": {
    "react": "18.2.0",
    "@ewoosoft/scp-report-library": "1.0.0"  // react ^18.0.0 요구
  }
}

// 충돌 없음: 동일한 react 버전 사용
```

**완화 방안**:
- peerDependencies로 React 버전 명시
- 넓은 버전 범위 허용 (^18.0.0)

**3. 빌드 시간 증가**:
- 각 서비스가 Shared Library를 번들링
- 빌드 시간 약간 증가

**완화 방안**:
- Tree-shaking으로 사용하지 않는 코드 제거
- 빌드 캐싱 활용

#### 2.1.3 적합성

**내부 Cloud 서비스 통합에 최적**:
- ✓ 중복 개발 제거 (SCP Cloud, Imaging Cloud, Analytics Cloud 등)
- ✓ 최소 운영 비용
- ✓ 독립적 배포 보장
- ✓ 빠른 기능 공유
- ✓ 타입 안정성
- ✓ Desktop 제품(E2, E3, EzOrtho, CleverOne) 리포트 Migration 지원

---

### 2.2 Microservice 방식

**개념**: 독립적인 리포트 서비스, 각 서비스가 API로 연동

**아키텍처**:
```
┌─────────────────────────────────────────────────────────┐
│           Report Microservice (별도 서버)                │
├─────────────────────────────────────────────────────────┤
│  - Report API Server                                     │
│  - Report Database                                       │
│  - Report Storage (S3/Blob)                              │
│  - Report Rendering Service                              │
└─────────────────────────────────────────────────────────┘
         │                │                │
         ↓                ↓                ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  SCP Cloud   │  │Imaging Cloud │  │Analytics Cloud│
│              │  │              │  │              │
│ REST API     │  │ REST API     │  │ REST API     │
│ 연동         │  │ 연동         │  │ 연동         │
└──────────────┘  └──────────────┘  └──────────────┘
```

**사용 예시**:

```typescript
// SCP Cloud에서 사용
async function loadReport(reportId: string) {
  const response = await fetch(
    `https://report-service.scp-cloud.com/api/reports/${reportId}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  )
  return await response.json()
}
```

#### 2.2.1 장점

**1. 완전한 독립성**:
- 리포트 서비스가 완전히 독립적으로 운영
- 각 서비스는 API만 호출
- 리포트 로직 변경 시 각 서비스 재배포 불필요

**2. 중앙화된 관리**:
- 단일 서비스로 모든 리포트 관리
- 통합 모니터링 및 로깅
- 일관된 업데이트

**3. 확장성**:
- 리포트 서비스만 독립적으로 스케일링
- 부하 분산 용이

#### 2.2.2 단점

**1. 높은 운영 비용**:
```
추가 인프라 필요:
  - Report API Server (최소 2대, HA)
  - Report Database (PostgreSQL/MongoDB)
  - Report Storage (S3/Azure Blob)
  - Load Balancer
  - Monitoring/Logging

예상 월 비용:
  - 서버: $200-500
  - DB: $100-300
  - Storage: $50-100
  - 기타: $50-100
  Total: $400-1,000/월
```

**2. 네트워크 의존성**:
```
문제 상황:
  - Report Service 장애 발생
  → SCP Cloud, Imaging Cloud, Analytics Cloud 모두 리포트 기능 중단
  → 의료 업무 마비
```

**3. 성능 오버헤드**:
```
Shared Library:
  - 로컬 함수 호출: < 1ms

Microservice:
  - Network Round-trip: 50-200ms
  - API 처리: 10-50ms
  - Total: 60-250ms
```

**4. 개발 복잡도 증가**:
- API 설계 및 문서화
- 인증/인가 시스템
- 에러 처리 및 재시도 로직
- API 버전 관리

#### 2.2.3 적합성

**내부 Cloud 서비스 통합에 부적합**:
- ✗ 높은 운영 비용 (불필요한 인프라)
- ✗ 네트워크 의존성 (장애 전파)
- ✗ 성능 오버헤드
- ✗ 개발 복잡도 증가

**적합한 경우** (현재 해당 없음):
- 리포트 기능이 매우 복잡하고 독립적인 팀이 관리
- 리포트 서비스를 외부에도 제공할 계획
- 각 Cloud 서비스의 기술 스택이 완전히 다름 (React, Vue, Angular 혼재)

---

### 2.3 Monolithic 통합 방식

**개념**: 각 서비스에 리포트 코드를 직접 복사하여 통합

**아키텍처**:
```
┌──────────────────────────────────────────────────────┐
│  SCP Cloud                                            │
│  - Report 코드 복사 (src/report/)                     │
│  - 독립적으로 관리                                    │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  Imaging Cloud                                        │
│  - Report 코드 복사 (src/report/)                     │
│  - 독립적으로 관리                                    │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  Analytics Cloud                                      │
│  - Report 코드 복사 (src/report/)                     │
│  - 독립적으로 관리                                    │
└──────────────────────────────────────────────────────┘
```

#### 2.3.1 장점

**1. 완전한 독립성**:
- 각 서비스가 완전히 독립적
- 다른 서비스에 영향 없음

**2. 커스터마이징 자유**:
- 각 서비스별로 자유롭게 수정 가능
- 제약 없음

#### 2.3.2 단점

**1. 심각한 중복 개발**:
```
리포트 기능 개발:
  - SCP Cloud: 개발자 A가 구현
  - Imaging Cloud: 개발자 B가 동일한 기능 재구현
  - Analytics Cloud: 개발자 C가 또 재구현

결과:
  - 3배의 개발 시간
  - 3배의 버그 가능성
  - 3배의 유지보수 비용
```

**2. 불일치 문제**:
```
신규 기능 추가:
  - SCP Cloud: 새로운 Annotation 타입 추가
  - Imaging Cloud: 아직 추가 안 함
  - Analytics Cloud: 다르게 구현

결과:
  - 서비스별로 다른 기능
  - 사용자 혼란
  - 데이터 호환성 문제
```

**3. 버그 수정 비효율**:
```
버그 발견:
  - SCP Cloud에서 버그 발견 및 수정
  - Imaging Cloud에 동일한 버그 존재 (수정 필요)
  - Analytics Cloud에도 동일한 버그 (수정 필요)

결과:
  - 3배의 수정 작업
  - 일부 서비스에서 수정 누락 가능성
```

**4. 막대한 유지보수 비용**:
- 각 서비스별로 독립적인 유지보수
- 코드 동기화 불가능
- 기술 부채 누적

#### 2.3.3 적합성

**내부 Cloud 서비스 통합에 매우 부적합**:
- ✗ 심각한 중복 개발 (SCP Cloud, Imaging Cloud, Analytics Cloud 각각 구현)
- ✗ 불일치 문제
- ✗ 버그 수정 비효율
- ✗ 막대한 유지보수 비용

**절대 피해야 할 방식**

---

## 3. 상세 비교 분석

### 3.1 개발 효율성 비교

| 항목                | Shared Library     | Microservice       | Monolithic         |
| ------------------- | ------------------ | ------------------ | ------------------ |
| **초기 개발**       |                    |                    |                    |
| 개발 시간           | 1배                | 1.5배              | 3배                |
| 개발 인력           | 2-3명              | 3-4명              | 6-9명              |
| **유지보수**        |                    |                    |                    |
| 버그 수정           | 1회 수정           | 1회 수정           | 3회 수정           |
| 기능 추가           | 1회 개발           | 1회 개발           | 3회 개발           |
| 코드 동기화         | 자동 (패키지)      | 불필요 (API)       | 불가능             |
| **테스트**          |                    |                    |                    |
| 단위 테스트         | 1회                | 1회                | 3회                |
| 통합 테스트         | 3회 (각 서비스)    | 3회 (각 서비스)    | 3회                |
| **문서화**          |                    |                    |                    |
| API 문서            | TypeScript 타입    | REST API 문서      | 각 서비스별        |
| 사용 가이드         | 1개                | 1개                | 3개                |

### 3.2 운영 효율성 비교

| 항목                | Shared Library     | Microservice       | Monolithic         |
| ------------------- | ------------------ | ------------------ | ------------------ |
| **인프라**          |                    |                    |                    |
| 추가 서버           | 없음               | 필요 (2-4대)       | 없음               |
| 추가 DB             | 없음               | 필요               | 없음               |
| 추가 Storage        | 없음               | 필요               | 없음               |
| Load Balancer       | 없음               | 필요               | 없음               |
| **월 운영 비용**    |                    |                    |                    |
| 인프라 비용         | $0                 | $400-1,000         | $0                 |
| 개발 인력 (유지보수)| 1명                | 1-2명              | 3명                |
| DevOps 인력         | 0명                | 1명                | 0명                |
| **배포**            |                    |                    |                    |
| 배포 복잡도         | 낮음               | 높음               | 낮음               |
| 배포 빈도           | 주 1-2회           | 주 1-2회           | 서비스별 다름      |
| 롤백 용이성         | 쉬움 (버전 다운)   | 중간               | 어려움             |
| **모니터링**        |                    |                    |                    |
| 모니터링 대상       | 없음 (각 서비스)   | Report Service     | 각 서비스          |
| 로깅                | 각 서비스          | 중앙 집중          | 각 서비스          |
| 알림                | 각 서비스          | Report Service     | 각 서비스          |

### 3.3 기술적 독립성 비교

| 항목                | Shared Library     | Microservice       | Monolithic         |
| ------------------- | ------------------ | ------------------ | ------------------ |
| **독립 배포**       |                    |                    |                    |
| 각 서비스 독립 배포 | ✓                  | ✓                  | ✓                  |
| 리포트 기능 독립 배포| ✓ (패키지 업데이트)| ✓                  | ✗                  |
| **장애 격리**       |                    |                    |                    |
| 리포트 장애 시      | 해당 서비스만 영향 | 전체 서비스 영향   | 해당 서비스만 영향 |
| 서비스 장애 시      | 다른 서비스 정상   | 다른 서비스 정상   | 다른 서비스 정상   |
| **기술 스택**       |                    |                    |                    |
| React 버전 통일     | 필요 (^18.0.0)     | 불필요             | 불필요             |
| TypeScript 버전     | 권장               | 불필요             | 불필요             |
| 빌드 도구           | 각 서비스 자유     | 불필요             | 각 서비스 자유     |

---

## 4. Shared Library 아키텍처 상세 설계

### 4.1 패키지 구조

**Monorepo 구조 (권장)**:
```
scp-report/
├── packages/
│   ├── core/                          # 핵심 엔진
│   │   ├── src/
│   │   │   ├── engine/                # 렌더링 엔진
│   │   │   ├── elements/              # Element 클래스
│   │   │   ├── utils/                 # 유틸리티
│   │   │   └── types/                 # TypeScript 타입
│   │   └── package.json
│   │
│   ├── components/                    # React 컴포넌트
│   │   ├── src/
│   │   │   ├── ReportEditor/
│   │   │   ├── ReportViewer/
│   │   │   ├── Elements/              # Element 컴포넌트
│   │   │   └── Toolbar/
│   │   └── package.json
│   │
│   ├── migration/                     # Migration 도구
│   │   ├── src/
│   │   │   ├── parsers/               # 제품별 파서
│   │   │   ├── converters/            # 변환 로직
│   │   │   └── validators/            # 검증
│   │   └── package.json
│   │
│   └── library/                       # 통합 패키지
│       ├── src/
│       │   └── index.ts               # Re-export
│       └── package.json
│
├── apps/                              # 테스트 앱
│   ├── scp-cloud-demo/                # SCP Cloud 통합 데모
│   ├── imaging-cloud-demo/            # Imaging Cloud 통합 데모 (가상)
│   └── analytics-cloud-demo/          # Analytics Cloud 통합 데모 (가상)
│
├── package.json                       # Root package.json
├── turbo.json                         # Turborepo 설정
└── tsconfig.json                      # 공통 TypeScript 설정
```

**패키지 분리 이유**:
- `@ewoosoft/scp-report-core`: 핵심 로직만 필요한 경우
- `@ewoosoft/scp-report-components`: React 컴포넌트만 필요한 경우
- `@ewoosoft/scp-report-migration`: Migration 도구만 필요한 경우
- `@ewoosoft/scp-report-library`: 전체 기능 (위 3개 패키지 통합)

### 4.2 핵심 API 설계

**ReportEditor 컴포넌트**:
```typescript
import { ReportEditor } from '@ewoosoft/scp-report-library'

interface ReportEditorProps {
  // 필수
  reportId: string
  onSave: (report: Report) => Promise<void>

  // 선택적
  theme?: 'e3' | 'ezortho' | 'cleverone' | CustomTheme
  locale?: string
  enabledElements?: ElementType[]
  readonly?: boolean
  
  // 이벤트
  onChange?: (report: Report) => void
  onError?: (error: Error) => void
  onReady?: () => void
}

// 사용 예시
<ReportEditor
  reportId="report-123"
  onSave={async (report) => {
    await api.saveReport(report)
  }}
  theme="e3"
  locale="ko-KR"
  enabledElements={['imageBox', 'textBox', 'annotation']}
/>
```

**ReportViewer 컴포넌트**:
```typescript
import { ReportViewer } from '@ewoosoft/scp-report-library'

interface ReportViewerProps {
  report: Report
  zoom?: number
  theme?: string
  onExport?: (format: 'pdf' | 'image') => Promise<Blob>
}

// 사용 예시
<ReportViewer
  report={report}
  zoom={1.0}
  theme="e3"
  onExport={async (format) => {
    return await exportReport(report, format)
  }}
/>
```

**Headless API** (고급 사용):
```typescript
import { ReportEngine } from '@ewoosoft/scp-report-library'

// 커스텀 UI 구현 시
const engine = new ReportEngine({
  container: document.getElementById('canvas'),
  report: reportData
})

// Element 추가
engine.addElement({
  type: 'textBox',
  position: { x: 10, y: 10 },
  size: { width: 100, height: 50 },
  content: 'Hello World'
})

// 렌더링
engine.render()

// Export
const pdf = await engine.exportToPDF()
```

### 4.3 버전 관리 전략

**Semantic Versioning**:
```
v1.2.3
│ │ │
│ │ └─ Patch: 버그 수정 (하위 호환)
│ └─── Minor: 신규 기능 추가 (하위 호환)
└───── Major: Breaking Change
```

**버전 지원 정책**:
```
현재 버전: v2.5.0

지원 버전:
  - v2.x.x: Full Support (버그 수정, 신규 기능)
  - v1.x.x: Security Fix Only (보안 패치만)
  - v0.x.x: End of Life (지원 종료)

권장 업데이트 주기:
  - Major: 6개월마다
  - Minor: 1개월마다
  - Patch: 즉시
```

**Breaking Change 최소화**:
```typescript
// Bad: Breaking Change
// v1.0.0
function createReport(data: ReportData): Report

// v2.0.0 (Breaking!)
function createReport(config: ReportConfig): Report

// Good: 하위 호환 유지
// v1.0.0
function createReport(data: ReportData): Report

// v2.0.0 (하위 호환)
function createReport(dataOrConfig: ReportData | ReportConfig): Report {
  // 타입 체크로 하위 호환 유지
  if (isReportData(dataOrConfig)) {
    return createReportFromData(dataOrConfig)
  }
  return createReportFromConfig(dataOrConfig)
}
```

**Deprecation 정책**:
```typescript
/**
 * @deprecated Use `createReport` instead. Will be removed in v3.0.0
 */
export function createReportLegacy(data: ReportData): Report {
  console.warn('createReportLegacy is deprecated. Use createReport instead.')
  return createReport(data)
}
```

### 4.4 배포 전략

**NPM Private Registry**:

**Option 1: Azure Artifacts** (권장):
```bash
# .npmrc 설정
registry=https://pkgs.dev.azure.com/ewoosoft/_packaging/scp-packages/npm/registry/
always-auth=true

# 배포
npm publish --registry https://pkgs.dev.azure.com/ewoosoft/_packaging/scp-packages/npm/registry/
```

**Option 2: GitHub Packages**:
```bash
# .npmrc 설정
@ewoosoft:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}

# 배포
npm publish
```

**CI/CD 파이프라인**:
```yaml
# .github/workflows/publish.yml
name: Publish Package

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://pkgs.dev.azure.com/ewoosoft/_packaging/scp-packages/npm/registry/'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Test
        run: npm test
      
      - name: Publish
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.AZURE_ARTIFACTS_TOKEN }}
```

**자동 버전 관리**:
```bash
# Changeset 사용 (권장)
npm install -g @changesets/cli

# 변경 사항 기록
npx changeset

# 버전 업데이트
npx changeset version

# 배포
npx changeset publish
```

### 4.5 통합 가이드

**E3 Cloud 통합 예시**:

**1. 패키지 설치**:
```bash
npm install @ewoosoft/scp-report-library
```

**2. 타입 정의**:
```typescript
// src/types/report.ts
import type { Report, ReportElement } from '@ewoosoft/scp-report-library'

export interface E3Report extends Report {
  patientId: string
  clinicId: string
  // E3 특화 필드
}
```

**3. 컴포넌트 통합**:
```typescript
// src/pages/ReportPage.tsx
import React from 'react'
import { ReportEditor } from '@ewoosoft/scp-report-library'
import '@ewoosoft/scp-report-library/dist/styles.css'
import { useE3Report } from '@/hooks/useE3Report'

export function ReportPage() {
  const { report, saveReport, loading } = useE3Report()

  if (loading) return <div>Loading...</div>

  return (
    <div className="report-page">
      <ReportEditor
        reportId={report.id}
        onSave={saveReport}
        theme="e3"
        locale="ko-KR"
        enabledElements={[
          'imageBox',
          'textBox',
          'label',
          'annotation'
        ]}
      />
    </div>
  )
}
```

**4. 커스텀 테마**:
```typescript
// src/theme/e3-report-theme.ts
import { createTheme } from '@ewoosoft/scp-report-library'

export const e3Theme = createTheme({
  colors: {
    primary: '#007bff',
    secondary: '#6c757d',
    background: '#ffffff',
    border: '#dee2e6'
  },
  fonts: {
    body: 'Arial, sans-serif',
    heading: 'Arial, sans-serif'
  },
  spacing: {
    unit: 8
  }
})

// 사용
<ReportEditor theme={e3Theme} />
```

**5. API 통합**:
```typescript
// src/api/report.ts
import type { Report } from '@ewoosoft/scp-report-library'

export async function saveReport(report: Report): Promise<void> {
  await fetch('/api/reports', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(report)
  })
}

export async function loadReport(reportId: string): Promise<Report> {
  const response = await fetch(`/api/reports/${reportId}`)
  return await response.json()
}
```

---

## 5. 비용 분석

### 5.1 개발 비용 비교

| 항목                | Shared Library     | Microservice       | Monolithic         |
| ------------------- | ------------------ | ------------------ | ------------------ |
| **초기 개발 (Year 0)** |                |                    |                    |
| Core Engine         | $150,000           | $150,000           | $450,000 (3배)     |
| Components          | $100,000           | $100,000           | $300,000 (3배)     |
| Migration           | $50,000            | $50,000            | $150,000 (3배)     |
| API/Infrastructure  | -                  | $100,000           | -                  |
| **Total**           | **$300,000**       | **$400,000**       | **$900,000**       |

### 5.2 운영 비용 비교 (연간)

| 항목                | Shared Library     | Microservice       | Monolithic         |
| ------------------- | ------------------ | ------------------ | ------------------ |
| **개발 인력**       |                    |                    |                    |
| 유지보수            | $100,000 (1명)     | $150,000 (1.5명)   | $300,000 (3명)     |
| **인프라**          |                    |                    |                    |
| 서버                | -                  | $6,000             | -                  |
| DB                  | -                  | $3,600             | -                  |
| Storage             | -                  | $1,200             | -                  |
| 기타                | -                  | $1,200             | -                  |
| **Total/Year**      | **$100,000**       | **$162,000**       | **$300,000**       |

### 5.3 3년 총 소유 비용 (TCO)

| 항목                | Shared Library     | Microservice       | Monolithic         |
| ------------------- | ------------------ | ------------------ | ------------------ |
| Year 0 (개발)       | $300,000           | $400,000           | $900,000           |
| Year 1 (운영)       | $100,000           | $162,000           | $300,000           |
| Year 2 (운영)       | $100,000           | $162,000           | $300,000           |
| Year 3 (운영)       | $100,000           | $162,000           | $300,000           |
| **3년 Total**       | **$600,000**       | **$886,000**       | **$1,800,000**     |

**비용 절감 효과**:
- Shared Library vs Microservice: **$286,000 절감** (32%)
- Shared Library vs Monolithic: **$1,200,000 절감** (67%)

### 5.4 개발 시간 비교

**신규 기능 추가 시나리오**: 새로운 Annotation 타입 추가

| 작업                | Shared Library     | Microservice       | Monolithic         |
| ------------------- | ------------------ | ------------------ | ------------------ |
| 기능 개발           | 3일                | 3일                | 9일 (3배)          |
| 테스트              | 2일                | 2일                | 6일 (3배)          |
| 배포                | 1일                | 1일                | 3일 (3배)          |
| **Total**           | **6일**            | **6일**            | **18일**           |

**버그 수정 시나리오**: 렌더링 버그 발견

| 작업                | Shared Library     | Microservice       | Monolithic         |
| ------------------- | ------------------ | ------------------ | ------------------ |
| 버그 수정           | 1일                | 1일                | 3일 (3배)          |
| 테스트              | 1일                | 1일                | 3일 (3배)          |
| 배포                | 0.5일              | 0.5일              | 1.5일 (3배)        |
| **Total**           | **2.5일**          | **2.5일**          | **7.5일**          |

---

## 6. 리스크 및 완화 방안

### 6.1 기술적 리스크

| 리스크                  | 확률 | 영향 | 완화 방안                              |
| ----------------------- | ---- | ---- | -------------------------------------- |
| 버전 충돌               | 중   | 중   | peerDependencies 명확화, 넓은 버전 범위|
| Breaking Change         | 중   | 높음 | Semantic Versioning, Deprecation 정책  |
| 빌드 시간 증가          | 낮   | 낮음 | Tree-shaking, 빌드 캐싱                |
| 타입 불일치             | 낮   | 중   | TypeScript strict mode, 자동 타입 체크 |

### 6.2 운영 리스크

| 리스크                  | 확률 | 영향 | 완화 방안                              |
| ----------------------- | ---- | ---- | -------------------------------------- |
| 버전 동기화 실패        | 중   | 중   | 자동 업데이트 알림, 버전 호환성 테스트 |
| 패키지 배포 실패        | 낮   | 중   | CI/CD 자동화, 롤백 절차                |
| 문서 부족               | 중   | 중   | 자동 문서 생성, 예제 코드 제공         |

### 6.3 조직 리스크

| 리스크                  | 확률 | 영향 | 완화 방안                              |
| ----------------------- | ---- | ---- | -------------------------------------- |
| 팀 간 협업 부족         | 중   | 중   | 정기 회의, Slack 채널, 문서화          |
| 책임 소재 불명확        | 중   | 중   | RACI 매트릭스, 명확한 소유권           |
| 지식 공유 부족          | 중   | 중   | 내부 교육, 코드 리뷰, 페어 프로그래밍  |

---

## 7. 실행 계획

### 7.1 Phase 1: Shared Library 개발 (3개월)

**Week 1-4: 기본 구조 및 Core Engine**
```
- Monorepo 구조 설정 (Turborepo)
- TypeScript 설정 및 빌드 파이프라인
- Core Engine 개발
  - Rendering Engine
  - Element Management
  - Coordinate System
- 단위 테스트 (Jest)
```

**Week 5-8: React 컴포넌트 개발**
```
- ReportEditor 컴포넌트
- ReportViewer 컴포넌트
- Element 컴포넌트 (ImageBox, TextBox, Label 등)
- Toolbar 컴포넌트
- Storybook 설정
```

**Week 9-12: Migration 및 통합**
```
- Migration 도구 개발
- 통합 패키지 구성
- API 문서 작성
- 통합 가이드 작성
```

**산출물**:
- `@ewoosoft/scp-report-library` v1.0.0
- API 문서
- 통합 가이드
- 데모 앱

### 7.2 Phase 2: SCP Cloud 통합 (1개월)

**Week 1-2: 통합 준비**
```
- SCP Cloud 프로젝트에 패키지 설치
- 타입 정의 및 API 통합
- 테마 커스터마이징
- Desktop 제품(E2, E3, EzOrtho, CleverOne) 리포트 import 기능
```

**Week 3-4: 통합 및 테스트**
```
- ReportEditor 통합
- ReportViewer 통합
- Migration 기능 테스트 (Desktop → Cloud)
- E2E 테스트
- 사용자 테스트
```

**산출물**:
- SCP Cloud 리포트 기능 완성
- Desktop 제품 리포트 import 기능 완성
- 통합 테스트 리포트
- 사용자 피드백

### 7.3 Phase 3: 신규 Cloud 서비스 통합 준비 (1개월)

**Week 1-2: Imaging Cloud 통합 예시 개발**
```
- Imaging Cloud 가상 시나리오 구현
- 의료 영상 분석 리포트 특화 기능
- 통합 가이드 작성
```

**Week 3-4: Analytics Cloud 통합 예시 개발**
```
- Analytics Cloud 가상 시나리오 구현
- 진료 데이터 분석 리포트 특화 기능
- 전체 통합 테스트
- 성능 최적화
```

**산출물**:
- 신규 Cloud 서비스 통합 가이드
- 통합 예시 코드
- 성능 벤치마크
- 최종 문서

### 7.4 마일스톤

```
Month 1-3: Phase 1 (Shared Library 개발)
  └─ Milestone 1: v1.0.0 출시 (Desktop 제품 Migration 지원 포함)

Month 4: Phase 2 (SCP Cloud 통합)
  └─ Milestone 2: SCP Cloud 리포트 기능 완성 (Desktop 제품 import 지원)

Month 5: Phase 3 (신규 Cloud 서비스 통합 준비)
  └─ Milestone 3: 통합 가이드 및 예시 완성
```

---

## 8. 결론

### 8.1 최종 권장: Shared Library (NPM Private Package)

**선정 근거**:

**1. 개발 효율성**:
- 중복 개발 완전 제거
- 단일 코드베이스 관리
- 3배 빠른 개발 속도

**2. 최소 운영 비용**:
- 추가 인프라 불필요 ($0)
- 최소 인력 (1명)
- 3년 TCO: $600,000 (Microservice 대비 32% 절감)

**3. 기술적 우수성**:
- 각 Cloud 서비스 독립 배포 보장
- 타입 안정성 (TypeScript)
- 빠른 기능 공유
- Desktop 제품(E2, E3, EzOrtho, CleverOne) 리포트 Migration 지원

**4. 내부 Cloud 서비스에 최적**:
- 외부 판매 불필요
- SCP Cloud 주 사용처
- 신규 Cloud 서비스 확장 용이
- 팀 간 협업 용이
- 일관된 코드 품질

### 8.2 기대 효과

**비용 절감**:
- 개발 비용: 67% 절감 (vs Monolithic)
- 운영 비용: 67% 절감 (vs Monolithic)
- 3년 TCO: $1,200,000 절감

**개발 효율성**:
- 신규 기능: 3배 빠른 개발
- 버그 수정: 3배 빠른 수정
- 코드 품질: 일관된 품질 유지

**사용자 경험**:
- 일관된 UI/UX (SCP Cloud, Imaging Cloud, Analytics Cloud 등)
- 빠른 기능 업데이트
- 안정적인 서비스
- Desktop 제품 리포트를 SCP Cloud에서 seamless하게 편집

### 8.3 다음 단계

**즉시 실행**:
1. Monorepo 구조 설정 (Turborepo)
2. Core Engine 개발 시작
3. CI/CD 파이프라인 구축

**단기 (1-3개월)**:
4. Shared Library v1.0.0 개발 (Desktop 제품 Migration 지원 포함)
5. SCP Cloud 통합 시작
6. 문서화 및 가이드 작성

**중기 (4-5개월)**:
7. SCP Cloud 통합 완료 (Desktop 제품 import 기능 포함)
8. 신규 Cloud 서비스 통합 가이드 작성
9. 전체 통합 테스트

### 8.4 성공 지표

**기술적 지표**:
- 코드 재사용률 > 90%
- 빌드 시간 < 5분
- 테스트 커버리지 > 80%
- TypeScript 타입 안정성 100%

**비즈니스 지표**:
- 개발 시간 단축 > 60%
- 버그 수정 시간 단축 > 60%
- 운영 비용 절감 > 60%

**품질 지표**:
- 코드 품질 일관성 > 90%
- 문서화 완성도 > 90%
- 사용자 만족도 > 4.5/5.0

