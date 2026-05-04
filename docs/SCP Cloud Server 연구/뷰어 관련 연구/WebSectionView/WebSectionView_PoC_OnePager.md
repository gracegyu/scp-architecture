# Web Section View PoC OnePager

## Project Name

Web Section View 기술 검증 PoC (Proof of Concept)

## Date

2026-04-27

## Submitter Info

Raymond

## Project Description

Web App(브라우저) 환경에서 치과 CT의 Section View를 표시하는 기능의 기술적 타당성을 검증하는 PoC 프로젝트이다.

기존 Desktop 애플리케이션(CleverOne 등)에서 제공하는 Section View 기능을 Web 환경에서 동일하게 구현할 수 있는지 단계별로 검증한다.

Section View 화면 구성:

- Scout View (좌상단): CT Axial Slice에서 치열이 잘 보이는 단면을 선택하고, 치열궁 곡선 및 Section 위치를 표시
- Panorama View (좌하단): 치열궁 곡선을 따라 생성한 파노라마 이미지
- Section View 3x3 (우측): 선택한 위치 기준으로 자동 생성된 9개의 단면 이미지

총 11개의 View (Scout 1 + Panorama 1 + Section 9)를 동시에 Web에서 표시해야 한다.

### 이전 연구 및 문제점

- [POPV-87](https://vts.vatech.com/browse/POPV-87): vtkImageMapper/vtkImageReslice를 활용한 CT 2D View 렌더링 방식 검토 완료
- [POPV-959](https://vts.vatech.com/browse/POPV-959): CONTEXT_LOST_WEBGL 에러 처리 - Chrome 기준 최대 15개의 WebGL Context 생성 가능하며, 초과 시 가장 오래된 Context가 Lost됨
- [EZDM-9](https://vts.vatech.com/browse/EZDM-9): RemoteViz(Server-side Rendering) 평가 완료

이전 시도에서는 11개의 View를 각각 별도의 WebGL Context로 생성하려다 Context 수 제한(Chrome 기준 최대 15개)에 걸려 실패한 것으로 추정된다. 하지만 이 접근법은 불필요하며, 아래와 같은 대안 전략이 가능하다:

- **전략 A**: **`<canvas>` 1개** + **WebGL Context 1개** — `gl.viewport`(및 필요 시 scissor)로 **11개 논리 영역**을 한 표면에 나눈다.
- **전략 B (Phase 1에서 구현·채택)**: **`<canvas>` 3개**(Scout · Panorama · Section 각각 1요소) + **WebGL Context 3개**(요소마다 Context 1개). Section 영역 canvas **1장 안**에서만 `viewport`를 **9번** 적용해 9칸을 그린다(합계 Viewport = 1+1+9).

### Canvas 요소와 WebGL Context (사실 정리)

브라우저에서는 일반적으로 **`<canvas>` HTML 요소 하나에 WebGL(WebGL2) Context 하나**를 연결하여 사용한다. 본 PoC에서의 대안은 다음과 같다.

| 구분 | 설명 |
| --- | --- |
| **`<canvas>` 개수** | 화면에 깔리는 **표면(요소) 수**. 전략 B는 Scout·Panorama·Section이 **서로 다른 canvas 요소**이다. Phase 2 이후 Scout는 Axial+오버레이용으로 **동일 그리드 셀 안에 2D `<canvas>` 2장**을 겹쳐 쓸 수 있다(요소 수는 이보다 많아질 수 있음). |
| **WebGL Context 개수** | GPU 렌더링 컨텍스트 수. **전략 B + Phase 1 데모**: Scout/Panorama/Section 각 WebGL 1개 → **최대 3개**. **CT 로드 후 Scout만 Canvas 2D**로 둔 경우 Scout canvas에는 WebGL Context가 없어, **전체 WebGL Context는 2개**(Panorama + Section)만 존재할 수 있다. |

**전략과의 대응**: 채택안(전략 B)은 **`<canvas>` 요소 3개 + WebGL Context 3개**이고, 대안(전략 A)은 **요소 1개 + Context 1개 + 뷰포트 11분할**이다. 문서에서 말하는 **「3 Canvas · 3 Context」**는 **서로 다른 `<canvas>` 요소 세 칸**을 의미한다.

> **렌더링 기술 선택 (Section 중심)**: **9개 Section View(3×3 Grid)에서의 CT 볼륨 리슬라이스 + 실시간 표시**에는 **WebGL2를 채택한다**. 이 경로는 단순 2D 이미지 나열이 아니라 **CT 볼륨에서 매 프레임 다수 단면을 재계산해 화면에 올리는** 워크로드라, ① 픽셀 단위 데이터-병렬 연산(3선형 보간), ② 표시까지의 GPU read-back 최소화, ③ 9뷰 동시 인터랙션 측면에서 GPU 경로가 구조적으로 유리하다. 자세한 근거는 [Phase1 결과 문서 — “왜 WebGL이 필요한가”](./Phase1/Phase1_WebGL_MultiView_결과.md#왜-webgl이-필요한가--왜-cpu만으로는-부적합한가) 참조. **CPU(JS, Worker) 대비 정량 수치**는 의사결정에는 영향이 없으므로 본 PoC의 결정 가지에서는 빼고, **Phase 6의 부속 PoC**에서 필요 시 측정한다(아래 Technical Description 참고).

### 뷰별 렌더링 경로 (PoC 기준 확정)

11뷰 레이아웃은 Phase 1에서 **서로 다른 `<canvas>` 요소 3개**(Scout / Panorama / Section Grid)에 WebGL Context를 각각 붙여 **총 3 Context**로 Context 수 제한을 피하는 것이 검증되었다(위 절 **「Canvas 요소와 WebGL Context」** 참조). **Phase 2 이후** Scout에서 실제 DICOM Axial을 **Canvas 2D**로 그리는 구성이 PoC 기본이므로, Scout 영역에는 **WebGL Context 없이 2D Canvas만** 둘 수 있다(정적 `scout.png` 데모만 쓸 때는 Phase 1과 같이 WebGL이 될 수 있음). Panorama·Section Grid는 **WebGL Canvas**를 유지하는 전제를 유지한다. **각 Canvas에 그리는 내용(GPU 리슬라이스 vs 2D 비트맵)** 은 아래 표와 같이 뷰마다 다르게 둔다.

| 뷰 | PoC에서의 표시(렌더) 경로 | 볼륨 리슬라이스 등 연산 | 비고 |
| --- | --- | --- | --- |
| **Scout** | **Canvas 2D**를 기본으로 한다. CT Axial 한 장 + Windowing + Phase 3 곡선·수직선 오버레이는 2D가 구현·디버깅에 유리하다. Phase 1에서는 정적 `scout.png`를 **WebGL 텍스처**로 표시한 데모가 있다. | Axial은 이미 메모리 볼륨에서 추출한 2D 슬라이스. Scout 표시를 WebGL로 **통일할 필요는 PoC 범위에서 두지 않는다.** | 제품화 시 볼륨을 **GPU 3D 텍스처 한 번만** 올리는 아키텍처를 택하면, Scout에서도 동일 텍스처를 샘플링하도록 **WebGL로 옮길 수 있는 선택지**는 남긴다. |
| **Panorama** | **2D 결과 이미지**(Phase 4에서 합성)를 **Canvas 2D 또는 WebGL 텍스처(단일 쿼드)** 중 하나로 표시한다. PoC는 구현 단순성 우선. | 곡선 따라 Reslice로 파노라마를 **만드는** 쪽은 **GPU(WebGL)** 경로를 우선 검토한다(Client / WASM / Server 비교는 Phase 6에서 병행). **표시**만으로 WebGL이 필수는 아니다. | 연산은 GPU, 표시는 2D라도 파이프라인 검증에는 충분한 경우가 많다. |
| **Section Grid (9뷰)** | **WebGL2**로 **9 Viewport**(+ Scissor)에 각각 리슬라이스 결과를 **셰이더 기반**으로 그리는 것을 **본 PoC의 채택안**으로 둔다. | **CT 볼륨 → GPU(3D/2D Array 텍스처) 업로드 후**, 곡선·위치에 따른 단면을 **프래그먼트 셰이더에서 샘플링**하는 경로를 Phase 5 목표로 한다. | PoC의 **성능·아키텍처 검증 핵심**은 이 뷰이다. **“Section만 WebGL로 충분한가?”**에 대한 답은 **이 워크로드까지 커버하면 PoC 목적에는 충분**하다고 본다. Scout·Panorama는 2D 위주로 남겨도 된다. |

**정리**: **WebGL2 필수·채택의 중심은 Section Grid(9뷰)의 볼륨 리슬라이스 + 실시간 표시**이다. Scout·Panorama는 PoC 단계에서 **Canvas 2D 중심**으로 두어도 본 OnePager의 기술 방향과 모순되지 않으며, Phase 4~5에서 Panorama **연산**을 GPU로 가져가더라도 **표시**까지 WebGL로 통일할 의무는 없다.

## Business and Marketing Justification

- SCP Cloud 제품에서 치과 CT Section View는 핵심 진단 기능이며, Web 환경에서의 구현은 Cloud-first 전략의 필수 요소이다.
- Desktop 전용이었던 Section View를 Web에서 제공하면, 브라우저만으로 치과 CT 진단이 가능해져 접근성이 크게 향상된다.
- 경쟁사(CleverOne 등) 대비 Web 기반 Section View 제공은 차별화 포인트가 된다.
- 본 PoC 결과에 따라 SCP Cloud 제품 로드맵의 Section View 구현 일정 및 아키텍처를 결정할 수 있다.

## Risk Assessment

| 리스크                                                 | 영향도 | 발생 가능성 | 대응 방안                                                        |
| ------------------------------------------------------ | ------ | ----------- | ---------------------------------------------------------------- |
| WebGL Context 수 제한으로 11개 View 동시 표시 불가     | 높음   | 낮음        | Viewport 분할 전략 (1~3 Context + 다수 Viewport) 적용            |
| CT ZIP 다운로드 시간이 과도하거나 메모리 부족          | 중간   | 낮음        | Stream Unzip으로 점진적 로딩, 대용량 CT 시 메모리 한도 사전 측정 |
| DICOM Volume 메모리 적재 시 브라우저 메모리 한도 초과  | 중간   | 낮음        | 치과 CT 기준 ~250MB 이내, 필요 시 Slice 범위 제한 또는 다운샘플링 |
| 9개 Section 이미지 실시간 생성 시 클라이언트 성능 부족 | 높음   | 중간        | WASM 또는 Server-side Compute로 대체 가능 여부 함께 검증         |
| 파노라마 생성 속도가 실시간 상호작용에 부적합          | 중간   | 중간        | WASM 또는 Server-side Compute 검토                               |
| 브라우저/GPU 호환성 문제                               | 낮음   | 낮음        | WebGL2 기준으로 구현, fallback 방안 검토                         |
| 치아 Segmentation 모델의 브라우저 추론 성능 부족       | 중간   | 중간        | Server-side 추론 후 결과만 전송하는 방식으로 대체 가능           |
| 전통적 알고리즘으로 치아 경계선 정확도 부족            | 중간   | 높음        | AI 기반 Segmentation으로 전환, 또는 두 방식 병행 검토            |

## Resource and Scheduling Details

### 인력

- 연구 담당자: 1~2명 (Web 렌더링 + 영상처리 역량)

### 일정 (순차 진행)

| 단계     | 검증 항목                               | 예상 기간 | 비고                                            |
| -------- | --------------------------------------- | --------- | ----------------------------------------------- |
| Phase 1  | WebGL 11개 View 동시 표시               | 1주       | Context/Viewport 전략 검증 (완료)               |
| Phase 2  | CT Data Download 및 Axial Slice 선택    | 1주       | S3 ZIP 다운로드 + Volume 구성 + Scout View Slider |
| Phase 3  | 치열궁 곡선(Arch Curve) 연결            | 1주       | 수동 Point 편집 UI (간소화)                     |
| Phase 4  | 파노라마 이미지 생성                    | 1주       | 곡선을 따라 Volume Reslice                      |
| Phase 5  | 9개 Section 이미지 실시간 생성 및 표시  | 2주       | 기능 구현 + 성능 측정                           |
| Phase 6  | 종합 성능 검증 및 아키텍처 결정         | 1주       | Client vs WASM vs Server-side 비교              |
| Phase 7  | 치아 Segmentation 오버레이              | 2~3주     | Scout/Section 치아 경계선 표시                  |
| **합계** |                                         | **8~10주** |                                                |

### 필요 장비 및 환경

- 테스트용 치과 CT DICOM 데이터 (다양한 해상도)
- 개발 환경: TypeScript, WebGL2
- (선택) WASM 빌드 환경, Server-side Rendering 테스트 서버

### 소스코드 저장소

모든 Phase(1~7)의 소스코드를 하나의 Monorepo에서 관리한다. scp-report-poc와 동일한 패턴(pnpm workspaces + Turborepo)을 적용한다.

- **Repository**: Azure DevOps `prototypes/scp-section-poc`
- **소스코드 위치**: [Azure DevOps](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc)

**Repository 구조**:

```
scp-section-poc/
├── packages/
│   ├── core/                           # @ewoosoft/scp-section-core
│   │   ├── src/
│   │   │   ├── webgl/                  # WebGL Context, Viewport(Phase 1)·Section Grid GPU 파이프라인(Phase 5)
│   │   │   ├── dicom/                  # DICOM 파싱, ZIP Stream Unzip, Volume 구성 (Phase 2)
│   │   │   ├── volume/                 # CT Volume Reslice·GPU 연동 (Phase 4~5)
│   │   │   ├── curve/                  # 치열궁 곡선 (Phase 3)
│   │   │   └── utils/                  # 좌표 변환, 수학 유틸리티
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── components/                     # @ewoosoft/scp-section-components
│       ├── src/
│       │   ├── SectionViewer.tsx        # 최상위 컴포넌트 (11 View 레이아웃)
│       │   ├── ScoutView.tsx            # Scout View (Phase 2~3, 기본 Canvas 2D)
│       │   ├── PanoramaView.tsx         # Panorama View (Phase 4, 2D 또는 단일 WebGL 쿼드)
│       │   ├── SectionGrid.tsx          # 3x3 Section Grid (Phase 5, WebGL2 + 9 Viewport)
│       │   └── hooks/                   # WebGL 관련 React hooks
│       ├── package.json
│       └── tsconfig.json
│
├── apps/
│   └── section-demo/                   # Demo 앱 (Vite + React)
│       ├── src/
│       │   └── App.tsx
│       ├── public/
│       │   └── sample-ct/              # 테스트용 CT 데이터 (또는 mock 이미지)
│       ├── index.html
│       ├── vite.config.ts
│       └── package.json
│
├── package.json                        # Monorepo root (pnpm workspaces)
├── pnpm-workspace.yaml
├── turbo.json                          # Turborepo
├── tsconfig.json
└── azure-pipelines.yml                 # CI: 빌드 + S3 배포
```

**개발 플로우**:

1. 초기 설정
   ```bash
   pnpm install
   pnpm --filter section-demo dev
   ```
2. 일상 개발: `packages/core`, `packages/components` 수정 -> `apps/section-demo`에서 즉시 HMR 반영 (workspace 링크)
3. Phase별 코드는 동일 Monorepo에 누적 (packages/core 하위 모듈로 분리)

### CT Data 저장소 (S3)

CT DICOM 데이터는 수십~수백 MB 규모이므로 앱 번들에 포함하지 않고, S3에 별도 저장하여 런타임에 다운로드한다. 이 방식은 다양한 CT 데이터셋으로 교체/추가 테스트가 용이하고, 추후 제품 아키텍처(서버에서 CT를 제공하는 구조)와도 일관된다.

- **S3 버킷 이름**: `scp-section-ct-data`
- **리전**: ap-northeast-2 (서울)
- **AWS 계정**: 767397951498 (SCPSharedDev) - 기존과 동일
- **퍼블릭 액세스 차단**: 비활성화 (PoC 전용, Demo Site 버킷과 동일)
- **저장 형식**: CT별 ZIP 파일 (예: `ct-data/sample-ct-01.zip`)
- **접근 URL**: `https://scp-section-ct-data.s3.ap-northeast-2.amazonaws.com/ct-data/{파일명}.zip`
- **접근 방식**: 퍼블릭 읽기 (PoC 전용)

**버킷 정책**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::scp-section-ct-data/*"
        }
    ]
}
```

**CORS 설정**:

브라우저에서 `fetch`로 다운로드할 수 있도록 Demo Site 및 로컬 개발 서버의 Origin을 허용한다.

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": [
            "http://scp-section-demo.test.scp.esclouddev.com",
            "http://localhost:5173",
            "http://localhost:4173"
        ],
        "ExposeHeaders": ["Content-Length", "Content-Type"],
        "MaxAgeSeconds": 3600
    }
]
```

**다운로드 및 Volume 구성 흐름**:

1. 브라우저에서 S3의 ZIP 파일을 `fetch` (ReadableStream)
2. `fflate` 라이브러리로 Stream Unzip (다운로드와 동시에 압축 해제)
3. 각 DICOM 파일을 `dicom-parser`로 파싱하여 픽셀 데이터 + 메타데이터 추출
4. 추출된 슬라이스들을 정렬(Instance Number 또는 Image Position 기준)하여 연속 `Int16Array`로 3D Volume 구성
5. 구성된 Volume을 메모리에 유지하고, 이후 Phase에서 Reslice/렌더링에 활용

> **메모리 안정성**: 치과 CT 기준 200~500 슬라이스 x 512x512 x 16bit = 약 100~250MB. 브라우저 메모리 한도(보통 1~2GB) 내에 충분히 수용 가능하다. 처음부터 연속 TypedArray(`Int16Array`)로 3D Volume 형태를 구성하면 Phase 6에서 WebGL 3D Texture로 GPU 업로드 시에도 효율적이다.

> **기존 PoC 참고**: Stream ZIP/Unzip 기술은 [stream-zip-unzip PoC](https://dev.azure.com/ewoosoft/prototypes/_git/stream-zip-unzip)에서 이미 검증 완료되었다. 해당 PoC의 `http2-client` 모듈이 S3에서 ZIP 다운로드 + `fflate`를 이용한 브라우저 Stream Unzip + DICOM 파싱을 구현하고 있으며, 이 코드를 참고하여 `packages/core/src/dicom/` 모듈로 통합한다.

### Demo Site 구축

scp-report-poc의 배포 패턴을 동일하게 적용한다. (참고: [SCP Cloud Report PoC 설계](../리포트 연구/SCP Cloud Report PoC 설계.md))

- **데모 사이트 URL**: `http://scp-section-demo.test.scp.esclouddev.com/`
- **AWS 계정**: 767397951498 (SCPSharedDev) - scp-report-poc와 동일 계정
- **호스팅**: AWS S3 정적 웹 사이트 호스팅
- **DNS**: Route 53 호스팅 영역 `test.scp.esclouddev.com`, 레코드 `scp-section-demo`

**S3 버킷**:

- 버킷 이름: `scp-section-demo.test.scp.esclouddev.com` (FQDN과 동일)
- 리전: ap-northeast-2 (서울)
- 정적 웹 사이트 호스팅 활성화, 인덱스 문서: `index.html`
- 퍼블릭 액세스 및 버킷 정책: scp-report-poc와 동일 설정 (데모 전용)

**CI/CD (Azure DevOps)**:

- 파이프라인: `scp-section-poc/azure-pipelines.yml`
- 트리거: main, develop 브랜치 push
- 빌드: pnpm install -> packages 빌드 -> section-demo 빌드
- 배포: `aws s3 sync apps/section-demo/dist s3://scp-section-demo.test.scp.esclouddev.com/ --delete`
- 변수: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (Secret), `AWS_REGION=ap-northeast-2`, `S3_BUCKET=scp-section-demo.test.scp.esclouddev.com`

**자격 증명**:

- scp-report-poc 파이프라인에서 사용 중인 IAM 자격 증명 재사용 가능 (동일 AWS 계정)
- 해당 IAM에 새 S3 버킷에 대한 `s3:ListBucket`, `s3:PutObject`, `s3:DeleteObject` 권한 추가 필요
- 자격 증명은 Azure DevOps Variable Group 또는 Pipeline variables에만 보관. Git에 커밋 금지

### Phase별 OnePager

각 Phase는 착수 시점에 범위가 확정되면 별도 OnePager를 작성한다.

| Phase | OnePager 파일 | 상태 |
| --- | --- | --- |
| Phase 1 | [Phase 1: WebGL 11개 View 동시 표시 기술 검증](https://vks.vatech.com/spaces/ESDEVELOPER/pages/302045959/Phase+1+WebGL+11%EA%B0%9C+View+%EB%8F%99%EC%8B%9C+%ED%91%9C%EC%8B%9C+%EA%B8%B0%EC%88%A0+%EA%B2%80%EC%A6%9D) | 완료 |
| Phase 2 | [Phase 2 결과](./Phase2/Phase2_CT_Download_결과.md) | 완료 |
| Phase 3 | [Phase 3 OnePager](./Phase3/Phase3_ArchCurve_OnePager.md) / [Phase 3 결과](./Phase3/Phase3_ArchCurve_결과.md) | 완료 |
| Phase 4 | (Phase 3 완료 후 작성 예정) | - |
| Phase 5 | (Phase 4 완료 후 작성 예정) | - |
| Phase 6 | (Phase 5 완료 후 작성 예정) | - |
| Phase 7 | (Phase 6 완료 후 작성 예정) | - |

## Technical Description

### Phase 1: WebGL 11개 View 동시 표시 (완료)

- **목표**: 브라우저에서 WebGL을 이용하여 11개의 View를 동시에 안정적으로 표시할 수 있는지 검증
- **배경**: 이전 시도에서 View마다 별도 WebGL Context를 생성하여 Context 수 제한에 걸림 (Chrome 최대 15개). 하지만 모든 View가 독립 Context일 필요는 없음
- **검증 방법**:
  - 전략 A: 단일 Canvas + 단일 WebGL Context + `gl.viewport()`로 11개 영역 분할
  - 전략 B: 3개 Canvas (Scout, Panorama, Section Grid) + 각각 WebGL Context, Section Grid는 9개 Viewport 분할
  - 각 전략의 렌더링 정상 동작, FPS, GPU 메모리 사용량 비교
- **성공 기준**: 11개 View가 CONTEXT_LOST_WEBGL 에러 없이 안정적으로 동시 렌더링됨
- **결과**: 전략 B(3 Canvas + 3 Context)로 검증 완료. [Phase 1 결과 문서](./Phase1/Phase1_WebGL_MultiView_결과.md) 참조

### Phase 2: CT Data Download 및 Axial Slice 선택

- **목표**: S3에 저장된 CT DICOM ZIP 파일을 브라우저에서 다운로드하여 3D Volume을 구성하고, Phase 1의 11-View 레이아웃의 Scout View에서 Axial Slice를 선택할 수 있도록 통합
- **배경**: Phase 3 이후 모든 단계는 CT Volume 데이터가 필요하다. CT DICOM 데이터는 수백 장의 파일로 구성되어 ZIP으로 압축 보관하며, 앱 번들에 포함하기에는 너무 크다(수십~수백 MB). Stream Unzip 기술은 [stream-zip-unzip PoC](https://dev.azure.com/ewoosoft/prototypes/_git/stream-zip-unzip)의 `http2-client` 모듈에서 이미 검증되었으며, 해당 코드를 참고하여 통합한다.
- **구현 범위**:
  - S3 버킷(`scp-section-ct-data`)에서 CT ZIP 파일을 `fetch` (ReadableStream)
  - `fflate` 라이브러리(`Unzip`/`UnzipInflate`)로 다운로드와 동시에 Stream Unzip
  - 각 DICOM 파일을 `dicom-parser`로 파싱: 픽셀 데이터(Pixel Data) + 메타데이터(Image Position, Pixel Spacing, Rows, Columns 등) 추출
  - 슬라이스를 정렬(Instance Number 또는 Image Position Patient 기준)하여 연속 `Int16Array`로 3D Volume 구성
  - Volume 메타데이터(dimensions, spacing, origin) 함께 관리
  - CT 선택 및 다운로드 진행률 표시 UI (CTLoader 컴포넌트)
  - CT Volume 로드 후 Phase 1의 11-View 레이아웃으로 전환
  - Scout View에 Axial Slice Viewer 통합: Slider로 Slice 인덱스 변경, Windowing(WC/WW) 조절
- **메모리 관리**: 치과 CT 기준 200~500 슬라이스 x 512x512 x 16bit = 약 100~250MB. 브라우저 메모리 한도(1~2GB) 내 수용 가능. 연속 TypedArray로 구성하여 이후 WebGL 3D Texture 업로드에도 효율적
- **성공 기준**:
  - CT ZIP 다운로드부터 3D Volume 구성 완료까지의 전체 파이프라인이 정상 동작
  - 로드 완료 후 11-View 레이아웃의 Scout View에서 Slider로 Axial Slice를 탐색하며 치열이 잘 보이는 Slice를 수동으로 찾을 수 있음
  - Windowing(Window Center/Width) 조절을 통해 적절한 화질로 표시 가능

### Phase 3: 치열궁 곡선(Dental Arch Curve) 연결 (간소화)

- **목표**: 선택한 Axial Slice 위에서 치열궁을 따르는 곡선을 정의
- **구현 방식**: 수동 Point 편집 UI만 구현 (AI 자동 검출은 본 PoC 범위에서 제외)
  - Scout View 위에서 마우스 클릭으로 Control Point를 여러 개 배치
  - Control Point들을 Spline(또는 Catmull-Rom) 곡선으로 연결
  - Point 추가/이동/삭제 가능한 간단한 편집 UI
- **성공 기준**: 사용자가 치열궁을 따라 곡선을 수동으로 정의할 수 있으며, 정의한 곡선이 화면에 시각적으로 표시됨

### Phase 4: 파노라마 이미지 생성

- **목표**: Phase 3에서 정의한 치열궁 곡선을 따라 CT Volume을 Reslice하여 파노라마 이미지를 생성
- **렌더·표시**: 파노라마 **결과는 2D 비트맵**이다. OnePager **「뷰별 렌더링 경로」**에 따라 **표시는 Canvas 2D 또는 단일 WebGL 텍스처** 중 PoC 구현 편의로 선택한다. **연산(Reslice 합성)** 은 GPU(WebGL) 우선 검토하며, Client / WASM / Server-side 비교는 Phase 6에서 병행한다.
- **검증 방법**:
  - 곡선을 일정 간격으로 샘플링하여 각 위치에서 곡선에 수직인 단면을 추출
  - 추출한 단면들을 이어 붙여 파노라마 이미지 합성
  - 구현 위치 비교: Client-side JavaScript vs WASM vs Server-side
- **성공 기준**: Desktop 파노라마와 동등한 화질, 생성 시간 1초 이내 (곡선 변경 시 실시간 갱신 가능 여부)

### Phase 5: 9개 Section 이미지 실시간 생성 및 표시

- **목표**: Scout View에서 위치를 선택하면 해당 위치 기준으로 9개의 Cross-section 이미지를 자동 생성하여 3x3 Grid에 실시간 표시
- **채택 렌더 경로**: **WebGL2**. CT 볼륨을 GPU 텍스처로 올린 뒤, 곡선에 수직인 단면을 **셰이더에서 리슬라이스**하고, Phase 1에서 검증한 **단일 Section Canvas 안의 9 Viewport(+ Scissor)** 에 출력하는 것을 본 Phase의 구현 목표로 한다(OnePager 상단 **「뷰별 렌더링 경로」** 참조).
- **검증 방법**:
  - 치열궁 곡선 위의 선택 지점 기준, 전후 일정 간격(Interval)으로 9개 단면 위치 계산
  - 각 위치에서 곡선에 수직인 방향으로 CT Volume을 Reslice하여 Section 이미지 생성
  - 9개 이미지를 **WebGL Section Grid**에 실시간으로 렌더링
  - 위치 변경(드래그) 시 실시간 갱신 FPS 측정
- **성공 기준**: 위치 변경 시 9개 Section 이미지가 30 FPS 이상으로 갱신됨 (또는 체감상 끊김 없는 수준)

### Phase 6: 종합 성능 검증 및 아키텍처 결정

- **목표**: 전체 파이프라인(Slice 선택 -> 곡선 정의 -> 파노라마 생성 -> Section 실시간 표시)의 성능을 종합 평가하고, 최종 아키텍처를 결정
- **검증 방법**:
  - Client-side Only (JavaScript/WebGL): 모든 연산을 브라우저에서 수행
  - Client-side + WASM: Volume Reslice 등 연산 집약적 부분을 WASM으로 가속
  - Server-side Compute: Volume Reslice를 서버에서 수행하고 결과 이미지를 클라이언트로 전송
  - Server-side Rendering: 모든 렌더링을 서버에서 수행하고 영상 스트리밍 (RemoteViz 방식 참고)
  - 각 방식별 응답 시간, FPS, CPU/GPU 사용률, 메모리 사용량 비교
- **성공 기준**: SCP Cloud 제품에 적용 가능한 성능 수준의 아키텍처 방안 도출

#### Phase 6 - 부속 PoC: GPU(WebGL) vs CPU(JS) 정량 비교 (선택)

본 PoC 전체에서 **WebGL은 이미 채택**된 결정이다(Project Description 참조). 다만 SCP Cloud 제품 보고/대외 공유 시 **수치로 보여달라는 요구가 있을 때** 짧게 수행할 수 있도록 절차만 정리한다. 의사결정에는 영향이 없으므로 **착수 여부는 Phase 6 진입 시 별도 판단**한다.

- **언제 한다**: 위 비교 항목(Client-only / Client+WASM / Server-side …) 평가 표를 만드는 단계에서 **참고 행** 한 줄을 더 채워야 할 때만.
- **무엇을 측정한다**: 동일 입력(같은 CT 볼륨, 같은 단면 9개, 같은 출력 해상도, 같은 windowing)에서 다음을 비교한다.

  | 경로                                | 설명                                                                    | 핵심 지표                                  |
  | ----------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------ |
  | A. **WebGL(채택안)**                | CT를 GPU 텍스처(3D/2D Array)로 1회 업로드 후, 셰이더에서 reslice + 표시 | 평균 FPS, 1프레임 ms(9뷰 합), 첫 업로드 ms |
  | B. **CPU 단일 스레드 JS**           | typed array에서 trilinear reslice → ImageData → `putImageData`          | 위와 동일                                  |
  | C. (옵션) **CPU + Web Worker N개**  | 9개 단면을 N Worker로 분할, 결과를 메인에서 표시                        | 위와 동일                                  |
  | D. (옵션) **CPU 계산 + WebGL 표시** | 계산은 CPU, 표시만 WebGL 텍스처 업로드                                  | “표시 비용” vs “계산 비용” 분리            |

- **고정 조건**: 같은 브라우저(Chrome 최신), 같은 GPU(내장/외장 둘 다 1회씩이면 충분), 같은 데이터·해상도(예: 256³ 볼륨, 출력 512² × 9뷰).
- **산출물**: 결과 표 + 한 단락 결론(“표시까지의 회수 비용까지 합치면 자릿수 차이가 측정되었음”과 같은 형태).
- **명시적 비목표**: 이 부속 PoC는 **WebGL 채택 자체의 재검토를 위한 것이 아니다.** 결과가 어떻든 본 PoC의 채택안(WebGL2)은 변경되지 않는다. 보고용 정량 보강이 목적이다.

### Phase 7: 치아 Segmentation 오버레이

- **목표**: Scout View(Axial Slice)와 Section View(Cross-section)에서 치아 경계선(윤곽)을 검출하여 오버레이로 표시하는 기능의 기술적 타당성을 검증
- **배경**: CleverOne 등 Desktop 제품에서는 Scout View에서 각 치아의 외곽선을 반투명으로 표시하고, Section View에서도 치관(crown) 부분의 윤곽선을 표시한다. 이 기능이 전통적 영상처리 알고리즘(OpenCV 류)인지 AI 기반인지는 확인 필요하며, Web 환경에서의 구현 가능성을 검증한다.
- **검증 방법**:
  - 전통적 알고리즘: Threshold + Edge Detection (Canny 등), Contour Extraction. Client-side JavaScript 또는 WASM(OpenCV.js) 활용
  - AI 기반: U-Net 등 의료 영상 Segmentation 모델. ONNX Runtime Web 또는 TensorFlow.js로 브라우저 추론, 또는 Server-side 추론 후 결과 전송
  - Scout View 대상: Axial Slice에서 치아 영역 segmentation -> 외곽선 추출 -> WebGL 오버레이
  - Section View 대상: Cross-section에서 치관 영역 segmentation -> 외곽선 추출 -> 각 Viewport에 오버레이
  - 성능: 실시간 상호작용(Slice 변경, 위치 이동) 시 segmentation 갱신 속도 측정
- **성공 기준**: 치아 경계선이 Desktop 제품과 유사한 정확도로 표시되고, Slice/위치 변경 시 체감상 끊김 없이 갱신됨

### 기술 스택 (예상)

- Frontend: TypeScript, **WebGL2(Section Grid·볼륨 리슬라이스 파이프라인 중심)**, React, Vite. Scout·Panorama 결과 표시는 PoC에서 **Canvas 2D 병행** 가능(본 문서 「뷰별 렌더링 경로」).
- DICOM 처리: `dicom-parser` (DICOM 파일 파싱), `fflate` (ZIP Stream Unzip)
- Volume 처리: vtk.js 또는 자체 Reslice 구현
- (선택) WASM: C++/Rust -> WebAssembly 빌드
- (선택) Server-side: Node.js/Python 서버 또는 기존 SCP Cloud 인프라 활용
- AI (Phase 7 검토): 치아 Segmentation 모델
- Segmentation (Phase 7 검토): OpenCV.js(WASM) 또는 ONNX Runtime Web / TensorFlow.js (브라우저 추론)
