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

- **전략 A**: 1개의 WebGL Context + 11개의 Viewport로 분할
- **전략 B**: 3개의 WebGL Context (Scout 1개, Panorama 1개, Section 9개 통합 1개) + Section 영역은 9개 Viewport로 분할

> **렌더링 기술 선택**: 본 PoC는 **WebGL2를 채택한다**. 단순 표시뿐 아니라 **CT 볼륨에서 매 프레임 다수 단면을 재계산해 그대로 화면에 표시**하는 워크로드라, ① 픽셀 단위 데이터-병렬 연산(3선형 보간), ② 표시까지의 회수(read-back) 비용 0, ③ 9뷰 동시 인터랙션 측면에서 GPU 경로가 구조적으로 강제된다. 자세한 근거는 [Phase1 결과 문서 — “왜 WebGL이 필요한가”](./Phase1/Phase1_WebGL_MultiView_결과.md#왜-webgl이-필요한가--왜-cpu만으로는-부적합한가) 참조. **CPU(JS, Worker) 대비 정량 수치**는 의사결정에는 영향이 없으므로 본 PoC의 결정 가지에서는 빼고, **Phase 6의 부속 PoC**에서 필요 시 측정한다(아래 Technical Description 참고).

## Business and Marketing Justification

- SCP Cloud 제품에서 치과 CT Section View는 핵심 진단 기능이며, Web 환경에서의 구현은 Cloud-first 전략의 필수 요소이다.
- Desktop 전용이었던 Section View를 Web에서 제공하면, 브라우저만으로 치과 CT 진단이 가능해져 접근성이 크게 향상된다.
- 경쟁사(CleverOne 등) 대비 Web 기반 Section View 제공은 차별화 포인트가 된다.
- 본 PoC 결과에 따라 SCP Cloud 제품 로드맵의 Section View 구현 일정 및 아키텍처를 결정할 수 있다.

## Risk Assessment

| 리스크                                                 | 영향도 | 발생 가능성 | 대응 방안                                                        |
| ------------------------------------------------------ | ------ | ----------- | ---------------------------------------------------------------- |
| WebGL Context 수 제한으로 11개 View 동시 표시 불가     | 높음   | 낮음        | Viewport 분할 전략 (1~3 Context + 다수 Viewport) 적용            |
| 9개 Section 이미지 실시간 생성 시 클라이언트 성능 부족 | 높음   | 중간        | WASM 또는 Server-side Compute로 대체 가능 여부 함께 검증         |
| 치열궁 곡선 자동 검출(AI) 정확도 부족                  | 중간   | 중간        | 수동 UI를 기본으로 제공하고, AI는 보조 수단으로 활용             |
| Axial Slice 자동 선택(AI) 정확도 부족                  | 중간   | 중간        | 수동 Slider UI를 기본으로 제공하고, AI는 초기값 추천 용도로 활용 |
| 파노라마 생성 속도가 실시간 상호작용에 부적합          | 중간   | 중간        | WASM 또는 Server-side Compute 검토                               |
| 브라우저/GPU 호환성 문제                               | 낮음   | 낮음        | WebGL2 기준으로 구현, fallback 방안 검토                         |

## Resource and Scheduling Details

### 인력

- 연구 담당자: 1~2명 (Web 렌더링 + 영상처리 역량)

### 일정 (순차 진행)

| 단계     | 검증 항목                               | 예상 기간 | 비고                                   |
| -------- | --------------------------------------- | --------- | -------------------------------------- |
| Phase 1  | WebGL 11개 View 동시 표시               | 1주       | Context/Viewport 전략 검증             |
| Phase 2  | CT Axial Slice에서 치열 최적 Slice 선택 | 1주       | 수동 UI 우선, AI 자동 선택 검토        |
| Phase 3  | 치열궁 곡선(Arch Curve) 연결            | 1~2주     | 수동 Point 편집 UI + AI 자동 검출 검토 |
| Phase 4  | 파노라마 이미지 생성                    | 1주       | 곡선을 따라 Volume Reslice             |
| Phase 5  | 9개 Section 이미지 실시간 생성 및 표시  | 2주       | 기능 구현 + 성능 측정                  |
| Phase 6  | 종합 성능 검증 및 아키텍처 결정         | 1주       | Client vs WASM vs Server-side 비교     |
| **합계** |                                         | **7~8주** |                                        |

### 필요 장비 및 환경

- 테스트용 치과 CT DICOM 데이터 (다양한 해상도)
- 개발 환경: TypeScript, WebGL2
- (선택) WASM 빌드 환경, Server-side Rendering 테스트 서버

### 소스코드 저장소

모든 Phase(1~6)의 소스코드를 하나의 Monorepo에서 관리한다. scp-report-poc와 동일한 패턴(pnpm workspaces + Turborepo)을 적용한다.

- **Repository**: Azure DevOps `prototypes/scp-section-poc`
- **소스코드 위치**: [Azure DevOps](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc)

**Repository 구조**:

```
scp-section-poc/
├── packages/
│   ├── core/                           # @ewoosoft/scp-section-core
│   │   ├── src/
│   │   │   ├── webgl/                  # WebGL Context 관리, Viewport 분할, Texture 관리 (Phase 1)
│   │   │   ├── volume/                 # CT Volume 데이터 로딩 및 Reslice (Phase 4~5)
│   │   │   ├── curve/                  # 치열궁 곡선 처리 (Phase 3)
│   │   │   └── utils/                  # 좌표 변환, 수학 유틸리티
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── components/                     # @ewoosoft/scp-section-components
│       ├── src/
│       │   ├── SectionViewer.tsx        # 최상위 컴포넌트 (11 View 레이아웃)
│       │   ├── ScoutView.tsx            # Scout View 컴포넌트 (Phase 2~3)
│       │   ├── PanoramaView.tsx         # Panorama View 컴포넌트 (Phase 4)
│       │   ├── SectionGrid.tsx          # 3x3 Section Grid 컴포넌트 (Phase 5)
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
| Phase 1 | [Phase 1: WebGL 11개 View 동시 표시 기술 검증](https://vks.vatech.com/spaces/ESDEVELOPER/pages/302045959/Phase+1+WebGL+11%EA%B0%9C+View+%EB%8F%99%EC%8B%9C+%ED%91%9C%EC%8B%9C+%EA%B8%B0%EC%88%A0+%EA%B2%80%EC%A6%9D) | 작성 완료 |
| Phase 2 | (Phase 1 완료 후 작성 예정) | - |
| Phase 3 | (Phase 2 완료 후 작성 예정) | - |
| Phase 4 | (Phase 3 완료 후 작성 예정) | - |
| Phase 5 | (Phase 4 완료 후 작성 예정) | - |
| Phase 6 | (Phase 5 완료 후 작성 예정) | - |

## Technical Description

### Phase 1: WebGL 11개 View 동시 표시

- **목표**: 브라우저에서 WebGL을 이용하여 11개의 View를 동시에 안정적으로 표시할 수 있는지 검증
- **배경**: 이전 시도에서 View마다 별도 WebGL Context를 생성하여 Context 수 제한에 걸림 (Chrome 최대 15개). 하지만 모든 View가 독립 Context일 필요는 없음
- **검증 방법**:
  - 전략 A: 단일 Canvas + 단일 WebGL Context + `gl.viewport()`로 11개 영역 분할
  - 전략 B: 3개 Canvas (Scout, Panorama, Section Grid) + 각각 WebGL Context, Section Grid는 9개 Viewport 분할
  - 각 전략의 렌더링 정상 동작, FPS, GPU 메모리 사용량 비교
- **성공 기준**: 11개 View가 CONTEXT_LOST_WEBGL 에러 없이 안정적으로 동시 렌더링됨

### Phase 2: CT Axial Slice 최적 선택

- **목표**: CT Volume에서 치열이 가장 잘 보이는 Axial Slice를 선택하는 방법 검증
- **검증 방법**:
  - 수동 UI: Slider를 이용한 Axial Slice 탐색 (기본)
  - AI 보조: CT Volume에서 치열이 포함된 최적 Slice를 자동으로 추천하는 AI 모델 적용 가능성 검토
- **성공 기준**: 사용자가 직관적으로 치열 Slice를 선택할 수 있는 UI 구현, AI 자동 추천 시 정확도 평가

### Phase 3: 치열궁 곡선(Dental Arch Curve) 연결

- **목표**: 선택한 Axial Slice 위에서 치열궁을 따르는 곡선을 정의하는 방법 검증
- **검증 방법**:
  - 수동 UI: 사용자가 Control Point를 찍고 Spline 곡선으로 연결 (Point 편집/추가/삭제 가능)
  - AI 보조: CT 영상에서 치열궁 곡선을 자동으로 검출하는 AI 모델 적용 가능성 검토
- **성공 기준**: 곡선이 치열궁을 정확히 따라가며, 사용자가 쉽게 편집 가능

### Phase 4: 파노라마 이미지 생성

- **목표**: Phase 3에서 정의한 치열궁 곡선을 따라 CT Volume을 Reslice하여 파노라마 이미지를 생성
- **검증 방법**:
  - 곡선을 일정 간격으로 샘플링하여 각 위치에서 곡선에 수직인 단면을 추출
  - 추출한 단면들을 이어 붙여 파노라마 이미지 합성
  - 구현 위치 비교: Client-side JavaScript vs WASM vs Server-side
- **성공 기준**: Desktop 파노라마와 동등한 화질, 생성 시간 1초 이내 (곡선 변경 시 실시간 갱신 가능 여부)

### Phase 5: 9개 Section 이미지 실시간 생성 및 표시

- **목표**: Scout View에서 위치를 선택하면 해당 위치 기준으로 9개의 Cross-section 이미지를 자동 생성하여 3x3 Grid에 실시간 표시
- **검증 방법**:
  - 치열궁 곡선 위의 선택 지점 기준, 전후 일정 간격(Interval)으로 9개 단면 위치 계산
  - 각 위치에서 곡선에 수직인 방향으로 CT Volume을 Reslice하여 Section 이미지 생성
  - 9개 이미지를 Phase 1의 Section View에 실시간으로 렌더링
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

### 기술 스택 (예상)

- Frontend: TypeScript, WebGL2, HTML5 Canvas
- Volume 처리: vtk.js 또는 자체 Reslice 구현
- (선택) WASM: C++/Rust -> WebAssembly 빌드
- (선택) Server-side: Node.js/Python 서버 또는 기존 SCP Cloud 인프라 활용
- AI (검토): 치열 Slice 자동 선택, 치열궁 곡선 자동 검출 모델
