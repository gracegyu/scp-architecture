# Engineering One Pager

## Project Name

Cloud Web Viewer v1.3.2 — Section Module

## Date

2026-07-09

## Submitter Info

Raymond (전규현) — Section 모듈 Spec 초안

## Project Description

Clever Space Cloud Web Viewer에 Section Layout(MMI v1.3.2)을 접목하기 전, **Section 모듈**을 **`scp-section-poc` 레포에서 이어서** MMI 정합 구현한다.

- **구현 레포:** `scp-section-poc` (PoC와 동일 — 별도 레포 신설 없음)
- **참조 레포:** `~/Documents/Azure/cloudwebviewer` — 툴바·공통 UI·**개발 환경 정본**
- **환경 정책:** scp-section-poc의 Node/pnpm/React/Vite/TS/MUI 등을 **cloudwebviewer와 통일** (본 Spec §3, 개발계획 §9). 구현 착수 전 필수.
- UI 정본: `image23.png` + CW Top Toolbar look&feel (`@cloudwebviewer/core` 재사용)
- 완성 후 패키지·API·데모로 CW Viewer 팀에 인계 (`cloudwebviewer` 직접 접목은 Section 모듈 범위 아님)

참조: [Section-Module-개발계획.md](./Section-Module-개발계획.md), [MMI.md](./Confidential_CloudWebViewer_v1.3.2_MMI_Kor/MMI.md), [Claude Code 작업 가이드.md](./Claude Code%20작업%20가이드.md)

## Business and Marketing Justification

Clever Space CT 뷰어 v1.3.2에서 Section Layout(치열궁 단면 진단)을 제공한다. MMI·기획 답변(PLAN-1287) 범위 내 구현으로 출시 일정을 맞춘다.

## Risk Assessment

| 리스크 | 완화 |
|--------|------|
| Section Slice 스크롤 성능 | 구현 초기 벤치마크, 디바운스·캐시 |
| B/L 자동 판정 | 본 문서 §B/L 알고리즘(PLAN-1287 초안). 기획 confirm 전 draft |
| CW 툴바·MUI 의존 | **scp-section-poc 환경을 cloudwebviewer와 통일** (§3) 후 Toolbar link |
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

| 포함 | 제외 (Integration) |
|------|------------------|
| image23 3영역 + 뷰 타이틀 바 + CW Top Toolbar | MPR/Section 토글, Clever Space 셸 |
| MMI 1.2~1.13 (±45° 회전 제외) | 실제 prj 파일 I/O |
| Overlay 데이터 모델, Save 스키마 정의 | |

상세: Section-Module-개발계획.md §7

### 3. 개발 환경 정렬 (scp-section-poc ↔ cloudwebviewer)

**정책:** Section 모듈은 `scp-section-poc`에서 계속 개발한다. `cloudwebviewer`로 코드베이스를 옮기지 않는다. 대신 **개발 환경·UI 스택을 cloudwebviewer와 통일**한다.

| 구분 | 레포 | 역할 |
|------|------|------|
| 구현 | `scp-section-poc` | Section 엔진·UI·데모 (`section-demo`) |
| 정본(참조) | `cloudwebviewer` | Toolbar, MUI 테마, pnpm/node 버전, `.npmrc` |

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
| CW core | `@cloudwebviewer/core` | pnpm `link:` 로컬 path 의존 (Toolbar·common) |
| 패키지명 | `@cloudwebviewer/*` | `@ewoosoft/scp-section-*` 유지 (인계 시 API 문서화) |

#### 3.2 scp-section-poc 적용 항목

1. 루트 `package.json` — `packageManager`, `engines.node`
2. `apps/section-demo` — vite 5, react 18.2, typescript 5.2
3. `.npmrc` — cloudwebviewer와 동일 (private `@ewoosoft` registry)
4. MUI·Emotion·(필요 시 Lingui) 의존성
5. `@cloudwebviewer/core` link — `packages/core/src/toolbar/`, `ContentTitleBar` 등
6. `pnpm i && pnpm build && pnpm dev` 검증

상세 체크리스트: [Section-Module-개발계획.md §9](./Section-Module-개발계획.md)

#### 3.3 완료 기준 (DoD)

- §3.1 표 목표 충족
- `section-demo` dev 서버 기동
- (선택) CW `Toolbar`가 Section 데모 상단에 렌더 — link 의존 성공 확인

### 4. B/L 자동 판정 알고리즘 (v1.3.2 Spec)

정본 출처: [PLAN-1287.md §2](../PLAN-1287.md) (Raymond 제안, 2026-07-09)  
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
| Integration (접목) | 개발계획 §7.3 |

### 6. DoD (발췌)

- [ ] **환경:** §3.1 버전 목표 충족 (`scp-section-poc`)
- [ ] **환경:** `section-demo` pnpm dev 기동
- [ ] **환경:** `@cloudwebviewer/core` link + Toolbar 렌더 (또는 Known gap)
- [ ] B/L: §4.4~4.8 알고리즘 단위 테스트 (제어점 시나리오)
- [ ] B/L: Scout·Section 라벨 동기화, L/B Switching 연동
- [ ] B/L: 기획 confirm 3항 반영 또는 Known gaps 문서화
- [ ] MMI 1.3~1.7 curve·기준점·B/L Switching
- [ ] image23 레이아웃 + CW Toolbar look&feel

---

## 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1 | 2026-07-09 | OnePager 초안. B/L 자동 판정 알고리즘(PLAN-1287 §2) Spec 반영 |
| 0.2 | 2026-07-09 | §3 개발 환경 정렬 — scp-section-poc에서 계속 개발, cloudwebviewer와 통일 |
