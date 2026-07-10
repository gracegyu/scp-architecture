Engineering One Pager

## Project Name
Phase 1: WebGL 11개 View 동시 표시 기술 검증

## Date
- **기획/제출(초안)**: 2026-04-27
- **상태**: 검증 완료

## Submitter Info
Raymond

## Project Description
브라우저(WebGL) 환경에서 치과 CT Section View에 필요한 11개의 View(Scout 1 + Panorama 1 + Section 9)를 동시에 안정적으로 표시할 수 있는지 검증한다.

이전 시도([POPV-959](https://vts.vatech.com/browse/POPV-959))에서는 각 View마다 별도 WebGL Context를 생성하여 Chrome의 Context 수 제한(최대 15개)에 걸려 CONTEXT_LOST_WEBGL 에러가 발생했다. 본 PoC에서는 **WebGL Context를 3개로 제한**하고(Scout·Panorama·Section 각 1), 특히 Section은 **같은 Context 안에서 9개 Viewport(+ Scissor)로** 타일을 나누어 이 문제를 우회한다. (Context를 여러 뷰가 “하나로 공유”하는 것이 아니라, **개수를 줄이고** 한 Context 내에서 **화면만 분할**하는 방식이다.)

### Canvas 요소와 WebGL Context

브라우저에서는 일반적으로 **`<canvas>` 요소 하나에 WebGL(WebGL2) Context 하나**를 연결하여 사용한다.

- **채택 구현(전략 B)**: **서로 다른 `<canvas>` 요소 3개** — Scout용 1개, Panorama용 1개, Section Grid용 1개 — 에 각각 WebGL Context 1개씩 연결하여 **WebGL Context 합계 3개**. Section용 canvas **한 장**에서만 `viewport`를 9번 바꿔 9칸을 그린다.
- **대안(전략 A)**: `<canvas>` **1개** + WebGL Context **1개** + viewport로 11영역 분할. 본 Phase 1에서는 구현하지 않았다.

전체 PoC 문서와 동일 정의는 메인 [`WebSectionView_PoC_OnePager.md`](../WebSectionView_PoC_OnePager.md) **「Canvas 요소와 WebGL Context」** 절을 참조한다.

### 화면 레이아웃 (CleverOne 참고)

```
+-------------------+---------------------------+
|                   |  Section 3x3 Grid         |
|   Scout View      |  [1] [2] [3]              |
|   (Axial Slice)   |  [4] [5] [6]              |
|                   |  [7] [8] [9]              |
+-------------------|                           |
|   Panorama View   |                           |
|                   |                           |
+-------------------+---------------------------+
```

- 총 11개 View: Scout(1) + Panorama(1) + Section(9)
- 각 View에 서로 다른 2D 이미지를 WebGL Texture로 표시

## Business and Marketing Justification
- Phase 1은 이후 모든 Phase(2~6)의 기술적 전제 조건이다. WebGL로 11개 View를 동시에 표시할 수 없으면 나머지 PoC 진행이 불가하다.
- 이전에 실패했던 WebGL Context 문제를 해결하는 것이 본 연구의 첫 번째 관문이다.
- SCP Cloud에서 Section View 기능 제공 가능 여부를 결정하는 핵심 Gate이다.

## Risk Assessment

| 리스크 | 영향도 | 발생 가능성 | 대응 방안 |
|--------|--------|-------------|-----------|
| Context 3개 사용 시에도 CONTEXT_LOST_WEBGL 발생 | 높음 | 매우 낮음 | 전략 A(단일 Context + 11 Viewport)로 fallback |
| Section Grid의 9 Viewport 분할 시 렌더링 깨짐 | 중간 | 낮음 | scissor test 적용, Viewport 좌표 계산 검증 |
| Context 간 텍스처/셰이더 공유 불가로 GPU 메모리 증가 | 낮음 | 중간 | 셰이더는 소규모이므로 중복 생성 허용, 텍스처는 Context별 독립 관리 |
| 브라우저별 Viewport 개수/크기 제한 차이 | 낮음 | 낮음 | Chrome, Edge, Safari 크로스 브라우저 테스트 |

## Resource and Scheduling Details

- **기간**: 1주 (5일)
- **인력**: 1명 (Web 렌더링 역량)
- **선행 요구사항**: 없음 (최초 Phase)

| Day | 작업 | 산출물 |
|-----|------|--------|
| 1 | 프로젝트 셋업 (Monorepo, Demo App, CI/CD) | 프로젝트 초기 구조, Demo site 배포 |
| 2 | 3 Canvas + 3 Context + CSS 레이아웃 구현 | 11개 View 영역 표시 |
| 3 | Section Grid 9 Viewport 분할 + 더미 텍스처 렌더링 | 11개 View 독립 렌더링 동작 |
| 4 | 마우스 이벤트 처리 + 벤치마크 (FPS, GPU 메모리, 안정성) | 성능 측정 결과 |
| 5 | 크로스 브라우저 테스트 + 결과 정리 + 문서화 | 검증 보고서 |

### 소스코드 저장소

- **Repository**: Azure DevOps `prototypes/scp-section-poc` (Monorepo)
- **구조**: scp-report-poc와 동일한 Monorepo 패턴 (pnpm workspaces + Turborepo)

```
scp-section-poc/
├── packages/
│   ├── core/                           # @ewoosoft/scp-section-core
│   │   ├── src/
│   │   │   ├── webgl/                  # WebGL Context 관리, Viewport 분할, Texture 관리
│   │   │   ├── volume/                 # CT Volume 데이터 로딩 및 Reslice (Phase 4~5)
│   │   │   ├── curve/                  # 치열궁 곡선 처리 (Phase 3)
│   │   │   └── utils/                  # 좌표 변환, 수학 유틸리티
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── components/                     # @ewoosoft/scp-section-components
│       ├── src/
│       │   ├── SectionViewer.tsx        # 최상위 컴포넌트 (11 View 레이아웃)
│       │   ├── ScoutView.tsx            # Scout View 컴포넌트
│       │   ├── PanoramaView.tsx         # Panorama View 컴포넌트
│       │   ├── SectionGrid.tsx          # 3x3 Section Grid 컴포넌트
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
├── package.json                        # Monorepo root
├── pnpm-workspace.yaml
├── turbo.json
├── tsconfig.json
└── azure-pipelines.yml                 # CI: 빌드 + S3 배포
```

### Demo Site 구축

scp-report-poc의 배포 패턴을 동일하게 적용한다.

**S3 버킷**:
- 버킷 이름: `scp-section-demo.test.scp.esclouddev.com` (FQDN과 동일)
- 리전: ap-northeast-2 (서울)
- 정적 웹 사이트 호스팅 활성화, 인덱스 문서: `index.html`
- 퍼블릭 액세스: scp-report-poc와 동일한 버킷 정책 적용 (데모 전용)

- **데모 사이트 URL**: `http://scp-section-demo.test.scp.esclouddev.com/`
- **AWS 계정**: 767397951498 (SCPSharedDev) - scp-report-poc와 동일 계정
- **호스팅**: AWS S3 정적 웹 사이트 호스팅
- **DNS**: Route 53 호스팅 영역 `test.scp.esclouddev.com`, 레코드 `scp-section-demo`

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

## Technical Description

### 전략 비교: 단일 Context(1개) vs 다중 Context(3개)

이전 시도에서는 View 11개에 각각 Context를 생성하여(11개) Chrome 제한(최대 15개)에 걸렸다. 이를 해결하기 위해 Context 수를 줄이는 두 가지 방향이 있다.

**방향 1: 단일 Canvas + 단일 Context + 11 Viewport**

| 항목 | 평가 |
|------|------|
| Context 수 제한 회피 | 1개이므로 완전 회피 |
| 텍스처/셰이더 공유 | 가능하나, 셰이더는 2D quad 렌더링용 단순 셰이더라 중복 생성해도 무시할 수준. 텍스처는 각 View마다 서로 다른 이미지이므로 어차피 11개 별도 생성 필요. **공유할 리소스가 사실상 없음** |
| CSS 레이아웃 | Canvas 하나가 전체 화면을 차지하므로 HTML/CSS 레이아웃과의 통합 불가. View 영역 배치를 JavaScript로 직접 계산해야 함 |
| 마우스 이벤트 | Canvas 좌표 -> Viewport 영역 매핑 hit-test를 직접 구현해야 함 |
| 리사이즈 | 특정 View만 리사이즈하기 어려움 |
| 이후 Phase 확장 | Scout에 곡선 편집 UI, Panorama에 드래그/줌 등 독립 상호작용 추가 시, 단일 Canvas 위에서 영역별 분기 로직이 복잡해짐 |

**방향 2: 3 Canvas + 3 Context + Section 9 Viewport** (채택)

| 항목 | 평가 |
|------|------|
| Context 수 제한 회피 | 3개이므로 Chrome 제한(15개) 대비 충분한 여유 |
| CSS 레이아웃 | 각 Canvas가 독립 HTML 요소이므로 CSS Grid/Flexbox로 자연스러운 레이아웃 가능 |
| 마우스 이벤트 | 각 Canvas에서 독립적으로 이벤트 수신. 별도 hit-test 불필요 |
| 리사이즈 | 각 Canvas 독립 리사이즈 가능 |
| 이후 Phase 확장 | Scout/Panorama/Section이 각각 독립 컴포넌트이므로 Phase 2~5 기능 추가가 용이 |

**결론**: 단일 Context의 유일한 이론적 장점인 GPU 리소스 공유는 이 PoC에서 실질적 이점이 없다 (공유할 리소스가 없음). 반면 3 Context는 레이아웃, 이벤트, 확장성 모든 면에서 우위이므로, **3 Canvas + 3 Context 전략만 구현한다.**

### 구현 전략: 3 Canvas + 3 Context + Viewport 분할 혼합

기능적으로 독립적인 3개 영역(Scout, Panorama, Section Grid)에 각각 Canvas와 WebGL Context를 생성한다. Section Grid Canvas는 내부적으로 9개 Viewport로 분할한다.

**Canvas/Context 구성**:
```
Canvas 1 (Scout):      1 Context, 1 Viewport   → ScoutView.tsx
Canvas 2 (Panorama):   1 Context, 1 Viewport   → PanoramaView.tsx
Canvas 3 (Section):    1 Context, 9 Viewport    → SectionGrid.tsx
───────────────────────────────────────────────
합계:                   3 Context, 11 Viewport
```

**Section Grid 렌더링 루프 (의사코드)**:
```typescript
function renderSectionGrid(gl: WebGL2RenderingContext, sections: SectionConfig[]) {
  gl.clear(gl.COLOR_BUFFER_BIT);

  for (const section of sections) {
    gl.viewport(section.x, section.y, section.width, section.height);
    gl.scissor(section.x, section.y, section.width, section.height);
    gl.enable(gl.SCISSOR_TEST);

    gl.bindTexture(gl.TEXTURE_2D, section.texture);
    drawQuad(gl);
  }
}
```

**CSS 레이아웃**:
```
SectionViewer (CSS Grid)
├── ScoutView      (grid-area: scout)      → <canvas> + WebGL Context
├── PanoramaView   (grid-area: panorama)   → <canvas> + WebGL Context
└── SectionGrid    (grid-area: section)    → <canvas> + WebGL Context + 9 Viewport
```

### 성능 측정 항목

| 항목 | 측정 방법 | 목표 |
|------|-----------|------|
| FPS | `requestAnimationFrame` 기반 | >= 30 FPS (11개 View 동시 렌더링) |
| Context 안정성 | 장시간(10분+) 렌더링 후 CONTEXT_LOST_WEBGL 발생 여부 | 에러 없음 |
| GPU 메모리 | Chrome DevTools → Performance → GPU | 합리적 수준 (기준: 512MB 이내) |
| CPU 사용률 | Chrome DevTools → Performance → CPU | Idle 시 10% 이내 |
| 이벤트 응답 | 마우스 클릭/드래그 시 반응 시간 | 16ms 이내 (60fps 기준) |

### 테스트 환경

- **브라우저**: Chrome (최신), Edge (최신), Safari (최신)
- **GPU**: 내장 GPU (Intel/Apple Silicon) + 외장 GPU (가능 시)
- **해상도**: 1920x1080, 2560x1440
- **데이터**: 초기 단계는 더미(256x256~512x512) 텍스처로도 검증 가능. **실 CT/섹션 이미지·오버레이**를 쓰는 것도 가능하나, Phase 1의 제안 목표는 “11 View 동시 렌더 + Context 수”이므로 **볼륨/리슬라이스 품질은 이후 Phase**에서 다룬다.

### Phase 1 성공 기준

1. 3 Canvas + 3 Context + 9 Viewport로 11개 View가 CONTEXT_LOST_WEBGL 에러 없이 동시 렌더링됨
2. 30 FPS 이상 유지
3. 각 View(Scout, Panorama, Section 개별)에서 마우스 이벤트가 정상적으로 동작함
4. 10분 이상 안정적으로 동작함 (Context Lost 없음)
5. 크로스 브라우저(Chrome, Edge, Safari) 정상 동작 확인

### Phase 1 산출물

1. 3 Canvas 전략 동작 데모 (section-demo 앱) — **완료(결과·캡처: `Phase1_WebGL_MultiView_결과.md`, `screenshot.png`)**
2. 성능 벤치마크 결과 (FPS, GPU 메모리, CPU 사용률) — 측정치는 데모/로그에 기록되면 본 One Pager에 표로 보강 가능
3. 크로스 브라우저 테스트 결과 — 동일
4. Demo site 배포 완료 (`http://scp-section-demo.test.scp.esclouddev.com/`) — 인프라는 계획서 기준; URL·배포 상태는 운영 시점에 맞게 확인
