# Engineering One Pager

## Project Name

Cloud Web Viewer v1.3.2 — Section Module

## Date

2026-07-09

## Submitter Info

Raymond (전규현) — Section 모듈 Spec v0.6 **정제 중** (Claude Code §3.7)

## Project Description

Clever Space Cloud Web Viewer에 Section Layout(MMI v1.3.2)을 접목하기 전, **Section 모듈**을 **`scp-section-poc` 레포에서 이어서** MMI 정합 구현한다.

- **구현 레포:** `scp-section-poc` (PoC와 동일 — 별도 레포 신설 없음)
- **참조 레포:** `~/Documents/Azure/cloudwebviewer` — 툴바·공통 UI·**개발 환경 정본**
- **런타임 참고:** EzCloud Test [https://container.test.ezcloud.ezcld.net/](https://container.test.ezcloud.ezcld.net/) — Clever Space 안의 **Cloud Web Viewer**(MPR·툴바 UX 확인, §3.5)
- **CW UI 소비:** `@cloudwebviewer/core`를 **pnpm `link:`** 로 참조 (§3.4). toolbar·common **소스 복사 금지**
- **Section 엔진:** `@ewoosoft/scp-section-*` 유지 — CW core와 패키지·역할 분리
- **환경 정책:** scp-section-poc의 Node/pnpm/React/Vite/TS/MUI 등을 **cloudwebviewer와 통일** (본 Spec §3, 개발계획 §10). 구현 착수 전 필수.
- UI 정본: §2 화면 3분할 — (3) `image23.png`, (1)(2) EzCloud `2.png`·Slide7
- 완성 후 패키지·API·데모로 CW Viewer 팀에 인계 (`cloudwebviewer` 직접 접목은 Section 모듈 범위 아님)

참조: [Section-Module-개발계획.md](./Section-Module-개발계획.md), [MMI.md](./기획·요구사항/MMI/MMI.md), [Claude Code 작업 가이드.md](./Claude Code%20작업%20가이드.md)

## Business and Marketing Justification

Clever Space CT 뷰어 v1.3.2에서 Section Layout(치열궁 단면 진단)을 제공한다. MMI·기획 답변(PLAN-1287) 범위 내 구현으로 출시 일정을 맞춘다.

## Risk Assessment

| 리스크 | 완화 |
|--------|------|
| Section Slice 스크롤 성능 | 구현 초기 벤치마크, 디바운스·캐시 |
| B/L 자동 판정 | 본 문서 §B/L 알고리즘(PLAN-1287 초안). 기획 confirm 전 draft |
| CW 툴바·이벤트 연동 | §2.3 — link + `useBoundStore` 동일 패턴. Section 타일 handler 미구현 시 Known gap |
| link·registry 실패 | Known gap + MUI 토큰 임시 UI → link 해결 후 CW 컴포넌트로 교체 |
| CW 로컬 빌드 부담 | link·`pnpm i` 1회만. MPR·툴바 참고는 **EzCloud Test** (§3.5)로 충분 |
| Arrow 툴(MMI 1.12) | CW `InteractionType` 미포함 — CW 패턴으로 신규 |
| Scout 접목 | 모듈 내 2D Scout 유지, Integration 시 MPR Axial 교체 |

## Resource and Scheduling Details

1. **scp-section-poc ↔ cloudwebviewer 개발 환경 정렬** (§3) — 구현 착수 전 필수
2. 본 OnePager Spec 리뷰 (기획 + CW Viewer)
3. Section 모듈 기능 구현 (`scp-section-poc`)
4. 인계 → CW Viewer 접목

B/L: PLAN-1287 Raymond 초안 → Jessi confirm (세로 우세·반전 조건·1점 정책)

## Technical Description

### 1. 범위 (Section 모듈)

화면은 **Toolbar · MPR/Section 선택 · Section 뷰** 3층으로 나뉜다 (§2). Section 모듈이 **신규 구현·인계하는 핵심**은 **(3) Section 뷰** 이다. (1)(2)는 EzCloud·Slide7과 **동일 look&feel·동일 이벤트**로 맞추되, 소스는 **복사가 아니라 `@cloudwebviewer/core` link** 로 동일 컴포넌트를 쓴다.

| 포함 | 제외 (Integration) |
|------|------------------|
| **(3) Section 뷰** — image23 3영역 + 뷰 타이틀 바 (Scout·Panorama·Section grid) | Clever Space LNB·우측 갤러리·Back 라우팅 |
| **(1) Toolbar** — CW `Toolbar` link + **동일 zustand 이벤트** (§2.3) | 실제 prj 파일 I/O |
| **(2) MPR/Section 선택** — Slide7·EzCloud와 동일 L&F + layout 전환 (§2) | EzCloud 컨테이너 앱 배포·권한 |
| MMI 1.2~1.13 (±45° 회전 제외), Overlay·Save 스키마 | |

상세: Section-Module-개발계획.md §8, 본 Spec §2

### 2. 화면 3분할 — Toolbar · MPR/Section 선택 · Section 뷰

MMI Slide7·EzCloud CT 화면(`CloudWebViewerData/2.png`)을 기준으로, Cloud Web Viewer **본문**은 아래 3영역으로 구성된다. Clever Space 좌측 LNB·우측 썸네일 패널은 본 Spec 범위 밖(접목)이다.

#### 2.1 레이아웃 구조 (텍스트 다이어그램)

```
+------------------------------------------------------------------------+
| Clever Space LNB (접목)  |  Cloud Web Viewer 본문                       |
|                          |  +----------------------------------------+ |
|                          |  | (1) Toolbar                            | |
|                          |  | Back Pan Zoom ... Length Angle ... HQ  | |
|                          |  +----------------------------------------+ |
|                          |  | (2) MPR / Section 선택                  | |
|                          |  | 환자·스터디 정보 ...    [MPR] [Section]  | |
|                          |  +----------------------------------------+ |
|                          |  | (3) Section 뷰  (Section 선택 시)       | |
|                          |  | +-------------+----------------------+ | |
|                          |  | | Scout       | Section 3×3 grid     | | |
|                          |  | | Panorama    |                      | | |
|                          |  | +-------------+----------------------+ | |
|                          |  +----------------------------------------+ |
+------------------------------------------------------------------------+
```

MPR 선택 시 (3)은 MPR 2×2(3D·Axial·Sag·Cor) — EzCloud `2.png` 정본. Section 선택 시 (3)은 `image23`·Slide7 Section Layout.

#### 2.2 영역별 정리 (표)

| # | 영역 | MMI·시각 정본 | EzCloud Test 현황 | 구현 주체 | 소스·방식 | Section 모듈 책임 |
|---|------|---------------|-------------------|-----------|-----------|-------------------|
| **1** | **Toolbar** | MMI 1.12·1.13, Slide7 상단 | `2.png` 상단 — **있음** | CW core (link) | `@cloudwebviewer/core` `toolbar/Toolbar` **pnpm link** | link·렌더. **툴바 store와 Section 뷰 이벤트 연동** (§2.3). 소스 복사 금지 |
| **2** | **MPR/Section 선택** | MMI 1.1, Slide7 ① `[MPR][Section]` | `2.png` — **토글 미탑재** (MPR만) | CW core 또는 CW 패턴 | CW에 컴포넌트 있으면 **link**. 없으면 Slide7·EzCloud와 **동일 L&F** stub + layout state (접목 시 CW 정본 교체) | 데모에서 Section 선택 시 (3) 표시. MPR 선택 시 MPR placeholder 또는 EzCloud 동작 참고 |
| **3** | **Section 뷰** | MMI 1.2~1.9, `image23.png`, Slide7 본문 | **미탑재** | **Section 모듈** | `@ewoosoft/scp-section-core` · `@ewoosoft/scp-section-components` | **핵심 인계물.** Scout·Panorama·Section grid·curve·B/L·Draw curve·뷰 타이틀 바 |

참고 이미지:

| 영역 | 파일 |
|------|------|
| (1) Toolbar + (2) 바 + MPR 본문 | `CloudWebViewerData/2.png` |
| (1)(2)(3) Section 목표 | `기획·요구사항/MMI/Slide7.jpg`, `기획·요구사항/MMI/media/image23.png` |
| (1) 단일 뷰 예 (Section 비교용 아님) | `CloudWebViewerData/1.png` |

#### 2.3 Toolbar ↔ Section 뷰 이벤트 연동 (필수)

**가능하다.** CW는 Toolbar와 뷰가 **동일 zustand store** 로 통신한다. Section 모듈도 MPR과 **같은 패턴**을 따른다.

| 항목 | CW (MPR) 정본 | Section 모듈 요구 |
|------|---------------|-------------------|
| 상태 저장소 | `useBoundStore` — `toolStore.interaction`, `workspaceViewFeatures`, Command slice | **동일 store import** (link된 `@cloudwebviewer/core`) |
| Interaction | `pointer`, `pan`, `zoom`, `length`, `freeDraw`, `angle` (+ v1.3.2 `arrow`) | Scout·Panorama·Section **타일별** active view에 MMI 1.13 정책 적용 (slice 경계 밖 불가) |
| Workspace | `showGrid`, `showOverlays` | Section grid·Scout overlay 동기 |
| Command | `resetView`, `resetCloudWork`, `initializeAll`, `viewOrigin` | Section 뷰에 동일 handler 연결 |
| 뷰 타이틀 바 | `ContentTitleBar` — W/L, Setting, 최대화 | Section 3영역 각각 CW 패턴 (link) |

연동 원칙:

1. Toolbar 버튼 클릭 → CW `activateInteraction` / `setWorkspaceViewFeature` / command hook — **재구현하지 않음**.
2. Section 뷰(Scout·Pano·Section tile)는 store를 **구독**하고, 활성 interaction에 따라 pointer 이동·pan·zoom·계측·overlay를 처리 (MPR 2D view handler와 동일 계열).
3. `section-demo`는 `App.tsx`와 같이 **Toolbar + (2) layout bar + (3) WorkSpace/SectionViewer** 세로 배치로 조립해, EzCloud에서 보이는 것과 **한 화면으로 이어지게** 한다.

#### 2.4 “복사” vs link (용어 정리)

| 사용자 표현 | Spec 정의 |
|-------------|-----------|
| Toolbar·MPR/Section을 “똑같이” | **소스 파일 복사·포크 금지.** `@cloudwebviewer/core` **link** 로 **동일 컴포넌트** 사용 → look&feel·이벤트 자동 일치 |
| Section 뷰만 “우리가 제공” | `@ewoosoft/scp-section-*` 에만 Section 엔진·UI 구현 |

#### 2.5 데모·접목 시 기대 화면

| 모드 | (1) Toolbar | (2) 선택 | (3) 본문 |
|------|-------------|----------|----------|
| Section 데모 (`section-demo`) | CW link | Slide7 동일 `[MPR][Section]` | **Section 모듈** (인계 대상) |
| EzCloud Test (현재) | CW 제품 | MPR만 (토글 없음) | MPR 2×2 |
| 접목 후 제품 | CW | CW MMI 1.1 | Section 모듈 패키지 embed |

### 3. 개발 환경 정렬 (scp-section-poc ↔ cloudwebviewer)

**정책:** Section 모듈은 `scp-section-poc`에서 계속 개발한다. `cloudwebviewer`로 코드베이스를 옮기지 않는다. CW UI는 **복사 없이 link**, 개발 환경·UI 스택은 **cloudwebviewer와 통일**한다.

| 구분 | 레포 | 역할 |
|------|------|------|
| 구현 | `scp-section-poc` | Section 엔진·UI·데모 (`@ewoosoft/scp-section-*`) |
| 정본(참조) | `cloudwebviewer` | Toolbar, MUI 테마, pnpm/node 버전, `.npmrc` — **link 소스** |
| 런타임 참고 | EzCloud Test | [container.test.ezcloud.ezcld.net](https://container.test.ezcloud.ezcld.net/) — Clever Space 내 **Cloud Web Viewer** |
| 문서 | `scp-architecture` … `Cloud Web Viewer v1.3.2/` | Spec·MMI·개발계획 정본 (poc로 이전하지 않음) |

#### 3.1 버전 목표 (scp-section-poc)

| 항목 | cloudwebviewer | scp-section-poc 목표 |
|------|----------------|----------------------|
| Node.js | 20.x | 20.x |
| pnpm | 9.15.9 (`packageManager`) | 9.15.9 |
| React | 18.2.0 | 18.2.x |
| TypeScript | 5.2.2 | 5.2.x |
| Vite | 5.0.8 | 5.0.x (`section-demo`; 현재 6.x → 다운그레이드) |
| UI | MUI 5.15 + Emotion (+ Lingui) | 동일 도입 |
| 상태 | zustand 4.4 | zustand 또는 CW store 패턴 |
| CW core | `@cloudwebviewer/core` | pnpm `link:` — Toolbar·ContentTitleBar·common **import만** |
| Section core | `@ewoosoft/scp-section-core` | WebGL·수학·curve — **CW core와 별도 유지** |
| 패키지명 | `@cloudwebviewer/*` | scp 쪽은 `@ewoosoft/scp-section-*` 유지 (인계 시 API 문서화) |

#### 3.2 scp-section-poc 적용 항목

1. 루트 `package.json` — `packageManager`, `engines.node`
2. `apps/section-demo` — vite 5, react 18.2, typescript 5.2
3. `.npmrc` — cloudwebviewer와 동일 (private `@ewoosoft` registry; **설정 파일만** 복사)
4. MUI·Emotion·(필요 시 Lingui) — CW와 동일 major
5. **§3.4** — `@cloudwebviewer/core`·`core-types` pnpm link
6. `section-demo`에서 CW `Toolbar` import·렌더 검증
7. `pnpm i && pnpm build && pnpm dev` 검증

상세 체크리스트: [Section-Module-개발계획.md §10](./Section-Module-개발계획.md)

#### 3.3 완료 기준 (DoD)

- §3.1 표 목표 충족
- `section-demo` dev 서버 기동
- `@cloudwebviewer/core` link 후 CW `Toolbar` 상단 렌더 (실패 시 Known gap)

#### 3.4 CW UI 의존 — pnpm link (확정)

| 항목 | 내용 |
|------|------|
| 방식 | `pnpm link:` 로 `cloudwebviewer/packages/core`, `types/core` 참조 |
| 금지 | toolbar·`workSpace/.../common/` 소스를 scp-section-poc로 **복사·포크** |
| import 예 | `Toolbar`, `ContentTitleBar`, `toolbar/type`, (필요 시) `ImageAdjustDialog` |
| Section 로직 | Draw curve, B/L, 9단면 — **`@ewoosoft/scp-section-*`만** |
| CW clone | link 전제로 **나란히 clone** (`~/Documents/Azure/cloudwebviewer`) |
| CW 빌드 | link 설정 시 `pnpm i` 1회. **일상 개발은 section-demo `pnpm dev`만** |
| UX 참고 | MPR·툴바는 **EzCloud Test** §3.5 (CW `host-app` 필수 아님) |

```json
// apps/section-demo/package.json 예시
"@cloudwebviewer/core": "link:../../../cloudwebviewer/packages/core",
"@cloudwebviewer/core-types": "link:../../../cloudwebviewer/types/core"
```

link 불가 시: Known gap 기록 → MUI + `#141414`·36px·hover 토큰으로 임시 상단 바 → link 후 CW 컴포넌트로 교체.

상세: [개발계획 §10.4](./Section-Module-개발계획.md)

#### 3.5 EzCloud Test — Cloud Web Viewer 런타임 참고

| 항목 | 내용 |
|------|------|
| URL | [https://container.test.ezcloud.ezcld.net/](https://container.test.ezcloud.ezcld.net/) |
| 제품 구조 | **EzCloud**(Clever Space) 컨테이너 앱 안에 **Cloud Web Viewer** 탑재 |
| 확인 항목 | MPR 레이아웃, Top Toolbar(MMI 1.12·1.13), 뷰 타이틀 바, Pan/Zoom/계측·Overlay UX |
| 전제 | 조직 계정 로그인. 테스트 CT·환자 데이터는 Test 환경 정책 따름 |
| Section 미탑재 | v1.3.2 Section Layout은 아직 없음 — **MPR만** look&feel·동작 정본. Section 데모는 `scp-section-poc` |
| PoC 데모와 구분 | `scp-section-demo` = Section 엔진 검증 / EzCloud Test = CW 제품 UI·MPR 워크플로 참고 |

상세: [개발계획 §10.3.1](./Section-Module-개발계획.md)

### 4. B/L 자동 판정 알고리즘 (v1.3.2 Spec)

정본 출처: [PLAN-1287.md §2](./기획·요구사항/PLAN-1287.md) (Raymond 제안, 2026-07-09)  
상태: **기획 confirm 대기** — confirm 전까지 구현은 본 초안을 따르되, §4.8 예외·§4.9 confirm 항목은 feature flag 또는 설정으로 분리 가능.

#### 4.1 합의·역할 분담 (PLAN-1287 §1)

- Ez3D-i 코드 porting 경로는 사용하지 않는다.
- B/L 자동 판정: **개발실 알고리즘 초안(본 절) → 기획 confirm**.
- 자동 판정으로 커버되지 않으면 MMI **L/B Switching**(수동 반전).
- BL/LB 기준점 이동(MMI 1.6·1.7)은 유지.

#### 4.2 용어·출력

- B(Buccal): 협측(바깥), L(Lingual): 설측(안). Scout·Section view 라벨과 단면 이미지 좌우 표기에 동일 적용.
- 판정 결과는 curve 전역 `blPolarity` (normal / inverted) 로 관리. Section 타일 좌·우에 B/L 매핑.
- 수동 L/B Switching 시 `blPolarity` 토글 (MMI 1.6·1.7).
- 구현 시 `blPolarity`와 Section 픽셀 열 반전(`section.ts`의 `nU-1-iu`)을 일관되게 연동한다.

#### 4.3 전제

- 입력: **Scout(Axial) 화면 좌표** curve 제어점 시퀀스 (`objectFit: contain` 좌표 변환 후).
- **전악 curve가 아니어도** 동일 규칙 (부분 curve 포함).
- 첫 번째 입력 점 = **BL/LB 기준점** (MMI 1.3 #8).

#### 4.4 1단계 — 시작 반구

Scout view 가로 폭 **중앙 수직선** 기준:

| 조건 | 명칭 |
|------|------|
| 시작점 X < 화면 너비 / 2 | 좌반구 시작 |
| 시작점 X ≥ 화면 너비 / 2 | 우반구 시작 |

#### 4.5 2단계 — 초기 진행 방향 (1→2번째 점)

1→2 벡터 `(dx, dy)`:

| 분류 | 조건 |
|------|------|
| 가로 우세 | \|dx\| ≥ \|dy\| |
| 세로 우세 | \|dx\| < \|dy\| |

가로 우세: 좌→우 `dx > 0`, 우→좌 `dx < 0`  
세로 우세: 위→아래 `dy > 0`, 아래→위 `dy < 0` (화면 좌표, +Y = 아래)

#### 4.6 3단계 — 기본 B/L 극성 (`blPolarity = normal`)

Section view 기준 **화면 왼쪽 / 오른쪽 라벨**.

좌반구에서 시작:

| 주 진행 방향 | 왼쪽 | 오른쪽 |
|-------------|------|--------|
| 좌→우 (가로) | B | L |
| 우→좌 (가로) | L | B |
| 위→아래 (세로) | B | L |
| 아래→위 (세로) | L | B |

우반구에서 시작:

| 주 진행 방향 | 왼쪽 | 오른쪽 |
|-------------|------|--------|
| 좌→우 (가로) | L | B |
| 우→좌 (가로) | B | L |
| 위→아래 (세로) | L | B |
| 아래→위 (세로) | B | L |

요약: **좌반구 + 좌→우 = 왼쪽 B**가 기본. 우반구이거나 진행 방향이 반대이면 좌우 뒤바뀜.

#### 4.7 4단계 — 드로잉 중 극성 반전 (동적)

curve 이어 그리는 동안 **아래 중 하나** 발생 시 `blPolarity` **토글** (B↔L swap):

1. **진행 방향 급반전**: 직전 구간 접선과 현재 구간 접선 내적 < 0 (대략 90° 이상 꺾임)
2. **화면 중앙선 교차**: curve가 가로 중앙을 지나 반대 반구로 이동 (이전 반구 ≠ 현재 반구)
3. **Active Section Line 중앙 기준점** 통과 시 BL/LB 기준점 기준 반전 (MMI 1.3 #8, 기준점 이동과 동일 규칙)

토글은 **누적** (홀수 번 반전 = inverted 상태).

#### 4.8 5단계 — 예외·폴백

| 상황 | 처리 |
|------|------|
| 점 1개만 (방향 미정) | B/L 라벨 미표시 또는 임시 기본값(좌반구·좌→우 가정) — **기획 confirm** |
| 자동 판정 불확실 | 사용자 **L/B Switching** (context menu) |
| BL/LB 기준점 이동 | 기준점 변경 시 B/L 재판정 (MMI 1.6·1.7) |

#### 4.9 기획 confirm 요청 (구현 고정 전)

1. **§4.6 세로 우세** B/L 배치 — Clever One 체감과 일치 여부 (부분 curve 샘플 2~3종)
2. **§4.7 반전 조건** — 중앙선 교차·급반전 토글 전부 적용 vs 일부만
3. **점 1개일 때** 표시 정책

confirm 후 본 절 버전을 올리고 DoD에 반영한다.

#### 4.10 구현 체크 (Section 모듈)

- 신규 모듈 예: `packages/core/src/bl/blPolarity.ts` — 입력(제어점, 화면 크기) → `blPolarity` + 좌/우 B/L 라벨
- `useScoutAxialUi` / Draw Curve hook에서 점 추가·편집 시 재계산
- `SectionGrid` 타일 B/L 텍스트에 매핑
- prj 저장 시 `blPolarity` + BL/LB 기준점 좌표 포함 (MMI 1.14)

### 5. 기타 Technical Description (요약·TBD)

| 항목 | Spec 상태 |
|------|-----------|
| Overlay §6 + Normal 허용 오차 | 수치 TBD |
| Draw Curve (ESC 없음, 1점 더블클릭) | Claude Code 가이드 §4.2 |
| Save Project / proj Curve 없음 | PLAN-1287 Jessi comment |
| NFR (9단면 ~400ms, 마우스 전용) | 구현 초기 벤치마크 |
| CW UI · 화면 3분할 | §2 — Toolbar·MPR/Section(link/동일 L&F)·Section 뷰. §3.4 link |
| Toolbar 이벤트 | §2.3 — `useBoundStore` / `toolStore` MPR 동일 패턴 |
| MPR/Section 토글 | §2.2 — CW link 또는 Slide7 동일 L&F (EzCloud 미탑재) |
| CW 런타임 참고 | §3.5 EzCloud Test — `container.test.ezcloud.ezcld.net` |
| Integration (접목) | 개발계획 §8.3 |

### 6. DoD (발췌)

- [ ] **UI 3분할:** §2.2 — (1) Toolbar CW link, (2) MPR/Section 선택, (3) Section 뷰 조립
- [ ] **이벤트:** §2.3 — Toolbar interaction이 Section Scout·Pano·tile에 전달 (pan/zoom/length 등)
- [ ] **환경:** §3.1 버전 목표 충족 (`scp-section-poc`)
- [ ] **환경:** `section-demo` pnpm dev 기동
- [ ] **환경:** `@cloudwebviewer/core` link + CW Toolbar 렌더 (실패 시 Known gap, §3.4)
- [ ] **환경:** CW toolbar/common **복사 없음** — link만 사용
- [ ] B/L: §4.4~4.8 알고리즘 단위 테스트 (제어점 시나리오)
- [ ] B/L: Scout·Section 라벨 동기화, L/B Switching 연동
- [ ] B/L: 기획 confirm 3항 반영 또는 Known gaps 문서화
- [ ] MMI 1.3~1.7 curve·기준점·B/L Switching
- [ ] image23 레이아웃 + §2 전체가 EzCloud·Slide7과 한 화면으로 자연스럽게 연결

---

## 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1 | 2026-07-09 | OnePager 초안. B/L 자동 판정 알고리즘(PLAN-1287 §2) Spec 반영 |
| 0.2 | 2026-07-09 | §3 개발 환경 정렬 — scp-section-poc에서 계속 개발, cloudwebviewer와 통일 |
| 0.3 | 2026-07-09 | §3.4 **pnpm link 확정** — CW UI 복사 금지, 패키지 분리, Dev 서비스 참고, DoD 강화 |
| 0.4 | 2026-07-09 | §3.5 **EzCloud Test URL** — Clever Space 내 Cloud Web Viewer 런타임 참고 |
| 0.5 | 2026-07-09 | §2 **화면 3분할** — Toolbar·MPR/Section 선택(link/동일 L&F)·Section 뷰(인계). §2.3 Toolbar 이벤트 연동 |
| 0.6 | 2026-07-10 | 개발계획 §10 교차참조 정합. Spec 상태 **초안→정제 중** (Claude Code §3.7) |
