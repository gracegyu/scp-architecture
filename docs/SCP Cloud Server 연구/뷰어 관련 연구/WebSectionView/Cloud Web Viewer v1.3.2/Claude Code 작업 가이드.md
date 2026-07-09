# Cloud Web Viewer v1.3.2 Section 모듈 — Claude Code 작업 가이드

> 대상: Claude Code(개발 표준 AI 에이전트)가 Section 모듈 Spec 작성·구현을 이어서 수행할 때 읽는 핸드오프 문서.
>
> 실행 컨텍스트: **작업 유형별 cwd** 는 §2.1. 문서 루트 = `.../Cloud Web Viewer v1.3.2/`, 코드 루트 = `scp-section-poc`.
>
> 갱신: 2026-07-09 (v1.4) · §2.1 Claude Code 작업 폴더(cwd)·세션 유지 가이드.
>
> 요구사항 정본은 MMI. 본 가이드는 요약·핸드오프·구현 맥락. 상세 기능 정의는 MMI와 후속 Spec을 따른다.

---

## 1. 이 문서를 먼저 읽는 이유

Cloud Web Viewer v1.3.2 Section Layout은 문서·코드가 세 갈래로 나뉜다.

| 체계 | 역할 | 위치 |
| --- | --- | --- |
| 요구사항 (MMI) | 기획 기능 정의 v0.9.1 | `.../MMI_Kor/MMI.md` |
| MMI PPT comments | PPT 변경 이력·MMI.md 드리프트 보조 정본 | `.../MMI_Kor/comments/` (§4.2) |
| **UI 시각 정본** | Section Layout 3영역 기본 화면 | `.../MMI_Kor/media/image23.png` (§4.1) |
| 검토·합의 | 개발실 리뷰, PLAN-1287 기획 답변 | `MMI_개발실리뷰.md`, `../PLAN-1287.md` |
| 기술 검증 (PoC) | Web Section View 타당성·엔진·UI 프로토타입 | `scp-section-poc` 레포 + `../WebSectionView/` Phase 문서 |
| Section 모듈 (현재 단계) | MMI 정합 구현체 — 제품 접목 전 | `scp-section-poc` 확장 → 인계 |
| 최종 제품 | Clever Space CT Viewer 접목 | `cloudwebviewer` 레포 |

AI는 Section 모듈 Spec·구현을 담당한다. Clever Space `cloudwebviewer` 레포에 직접 넣지 않는다. 인계 후 CW Viewer 담당 개발자가 접목한다.

명칭: PoC 이후 단계는 PoC가 아니라 Section 모듈(Section Module v1.3.2)이라 부른다. 상세는 [Section-Module-개발계획.md](./Section-Module-개발계획.md).

---

## 2. Multi-root 워크스페이스 · 레포

VS Code / Claude Code는 `~/Documents/Azure/scp.code-workspace` 등으로 여러 레포를 동시에 연다.

| 레포 | 로컬 경로 | Section 모듈에서의 역할 |
| --- | --- | --- |
| scp-architecture | `~/Documents/Azure/scp-architecture` | MMI, 개발실 리뷰, Spec, 본 가이드 |
| scp-section-poc | `~/Documents/Azure/scp-section-poc` | Section 모듈 구현 코드베이스 (출발점) |
| cloudwebviewer | `~/Documents/Azure/cloudwebviewer` | 접목 대상 (읽기·Integration Spec 협의용) |
| stream-zip-unzip | `~/Documents/Azure/stream-zip-unzip` | CT ZIP Stream Unzip 참고 (PoC에서 패턴 차용) |
| abc-dev-assistant | `~/Documents/Git/abc-dev-assistant` | dev-chain·Spec 작성 스킬 |
| es-toolkit | `~/Documents/Azure/es-toolkit` | `/es-*` 개발 표준 명령 |

### 2.1 Claude Code 작업 폴더(cwd) — 세션 유지

Claude Code는 **시작할 때 연 cwd(작업 디렉터리)** 를 기준으로 상대 경로·터미널·컨텍스트가 잡힌다. Section 모듈은 문서와 코드가 **서로 다른 레포**에 있으므로, 세션 목적에 맞는 cwd를 고른다.

**절대 경로 (로컬 기준):**

| 별칭 | 경로 |
| --- | --- |
| **문서 루트 (v1.3.2)** | `~/Documents/Azure/scp-architecture/docs/SCP Cloud Server 연구/뷰어 관련 연구/WebSectionView/Cloud Web Viewer v1.3.2/` |
| WebSectionView 상위 | `~/Documents/Azure/scp-architecture/docs/.../WebSectionView/` |
| **코드 루트** | `~/Documents/Azure/scp-section-poc/` |
| CW 참조 | `~/Documents/Azure/cloudwebviewer/` |

#### 권장 cwd (결론)

| 작업 유형 | cwd로 열 폴더 | 이유 |
| --- | --- | --- |
| **Spec·MMI·개발계획 문서** | `Cloud Web Viewer v1.3.2/` | MMI, OnePager Spec, 본 가이드, 개발실 리뷰가 **한 폴더**에 모임. 상위 `PLAN-1287.md`는 `../` 한 단계 |
| **구현·빌드·환경 정렬** | `scp-section-poc/` | `package.json`, `pnpm`, `apps/section-demo`가 여기. 변경·커밋 대상 레포 |
| **cloudwebviewer 분석(읽기)** | `cloudwebviewer/` 또는 멀티루트 | Toolbar·`package.json` 정본 탐색 시 |

#### 쓰지 않는 것 (단독 cwd)

| 폴더 | 이유 |
| --- | --- |
| `WebSectionView/` (상위만) | Phase1~5·구 PoC OnePager 등 **v1.3.2와 무관한 문서가 섞여** 세션 컨텍스트가 흐려짐 |
| `scp-architecture/` 레포 루트 | Section 문서까지 상대 경로가 김. 문서 전용 세션에는 v1.3.2 하위가 낫다 |

#### 세션 유지 팁

1. **한 세션 = 한 주 cwd.** 문서 세션과 코드 세션을 섞으면 상대 경로·git 상태가 헷갈린다. 문서 끝나고 구현으로 넘어갈 때는 **새 세션**을 열고 cwd를 `scp-section-poc`로 바꾼다.
2. **멀티루트 워크스페이스** (`scp.code-workspace`)는 VS Code/Cursor에서 레포를 동시에 보기용. Claude Code **cwd는 위 표대로 하나만** 고른다.
3. **매 세션 첫 메시지**에 §16 프롬프트를 붙여 `문서 루트`·`코드 루트`를 **둘 다 명시**한다. cwd가 `scp-section-poc`여도 문서 경로는 절대경로 또는 `../scp-architecture/docs/.../Cloud Web Viewer v1.3.2/` 로 읽게 한다.
4. **장기 작업(문서+코드 반복)** 의 기본 cwd는 **`scp-section-poc`** 를 권장한다. Section 모듈의 실체가 코드이고, 문서는 가이드·Spec 경로만 프롬프트로 고정하면 된다.
5. **환경 정렬(§9)** 단계는 반드시 cwd = `scp-section-poc`. `cloudwebviewer`는 link·버전 **참조만**.

#### cwd 빠른 선택

```
문서만 수정?     → Cloud Web Viewer v1.3.2/
코드·pnpm·빌드?  → scp-section-poc/
둘 다?           → scp-section-poc/ + §16 프롬프트(문서 루트 명시)
```

---

## 3. 현재 진행 상태 (2026-07-09)

### 3.1 완료

| 단계 | 산출물 | 상태 |
| --- | --- | --- |
| MMI v0.9.1 | Epic 1 Section Layout 1.1~1.14 | 기획 반영 중 (Overlay §6, 회전 스펙아웃 등) |
| MMI 개발실 리뷰 | VKS + 로컬 MD | 완료 |
| 기획 답변 | PLAN-1287 Jessi #1~#11 | 완료 (Save, Overlay, 회전 스펙아웃, Thickness, Draw curve, 모바일 등) |
| B/L 알고리즘 초안 | PLAN-1287 Raymond comment | 제안 완료 → 기획 Jira confirm 대기 |
| Save Project Curve 초기화 | MMI EP01_F014 #3 + PPT comment 913 | proj Curve 있으면 세팅, 없으면 blank (§4.2) |
| MMI PPT comments 정리 | `comments/` XML 6개 (Jessi, 7/1~8) | §4.2 — ESC·1점 더블클릭·proj 예외·B/L 일정 |
| Web Section View PoC | Phase 1~5 구현 | 기술 검증 완료 |
| Section 모듈 개발계획 | `Section-Module-개발계획.md` | 초안 완료 |

### 3.2 지금 단계

```
[지금] Section 모듈 Spec v1.3.2 작성
    ↓
Spec 리뷰 (기획 + Cloud Web Viewer 담당자 권장)
    ↓
Section 모듈 구현 (scp-section-poc → MMI 정합)
    ↓
인계 → CW Viewer 접목 → 통합 테스트 → 출시
```

Spec 리뷰는 PoC가 아니다. 성능 검증은 구현 초기 벤치마크로 병행한다.

### 3.3 미확정 (Spec·기획 confirm 필요)

| 항목 | 상태 | 담당 |
| --- | --- | --- |
| B/L 자동 판정 최종 알고리즘 | Raymond 초안 → Jessi confirm. 기획 신규 정의 7/10 목표 (comment 91A) | 기획 |
| MMI.md vs PPT 최신본 | ESC 종료·1점 더블클릭·proj Curve 예외 — MD 미반영 가능 | Spec은 §4.2 우선, 추후 MMI.md 재추출 |
| Overlay Normal 허용 오차 | MMI "별도 정의" | Spec에서 수치 확정 |
| Section Slice 스크롤 NFR | 개발실 리뷰 최대 리스크 | 구현 초기 벤치마크 |
| Save Project Section 모듈 범위 | 데이터 모델+데모 vs CW prj I/O | Spec 리뷰 시 CW 팀 합의 |
| Scout 명칭 | Scout 유지, 7/10 기획 검토 | 기획 |

---

## 4. 디렉터리 · 문서 맵

```
docs/SCP Cloud Server 연구/뷰어 관련 연구/WebSectionView/
├── WebSectionView.md                          # 초기 연구 메모
├── WebSectionView_PoC_OnePager.md             # PoC 전체 로드맵
├── PLAN-1287.md                               # Jira comment 스레드 (기획 답변·B/L)
├── Phase1/ … Phase5/                          # Phase별 OnePager·결과
└── Cloud Web Viewer v1.3.2/
    ├── Claude Code 작업 가이드.md              ← 본 문서
    ├── Section-Module-개발계획.md              # 절차·범위·체크리스트
    ├── Confidential_CloudWebViewer_v1.3.2_MMI_개발실리뷰.md
    ├── Confidential_CloudWebViewer_v1.3.2_MMI_Kor/
    │   ├── MMI.md                             # ★ 요구사항 정본 (텍스트)
    │   ├── media/                             # PPT 원본 삽입 이미지 (§4.1)
    │   │   └── image23.png                    # ★ v1.3.2 Section Layout UI 시각 정본
    │   ├── comments/                          # PPT modern comment XML (§4.2)
    │   └── Slide*.jpg                         # SharePoint 저해상도 export (참고만)
    └── Section-Module-Spec-v1.3.2-OnePager.md   # OnePager Spec (B/L, 환경 정렬 §3)
```

---

## 4.1 MMI UI 시각 참조 — `image23.png` (v1.3.2 기본 레이아웃)

### 정본 이미지

| 우선순위 | 파일 | 역할 |
| ---: | --- | --- |
| **1 (필수)** | `Confidential_CloudWebViewer_v1.3.2_MMI_Kor/media/image23.png` | **v1.3.2 Section Layout 기본 UI** — Scout + Panorama + Section 3×3 전체를 관통하는 시각 정본 |
| 2 | `MMI.md` | 동작·규칙 **텍스트** 정본 (image23과 함께 읽을 것) |
| 3 | `media/image19.png`, `image27.png`, `image28.png` | image23과 **동일 계열** 뷰어 목업(해상도·슬라이스 번호·TH/INT만 다름). image23과 충돌 시 **image23 우선** |
| 4 | `media/` 나머지 | 부분 확대·아이콘·다른 슬라이드 설명용 **참고** |
| 5 | `Slide7.jpg` 등 `Slide*.jpg` | SharePoint 이미지 export — **저해상도**. 레이아웃 확인용 보조만 |

경로 (레포 기준):

```
scp-architecture/docs/SCP Cloud Server 연구/뷰어 관련 연구/WebSectionView/
  Cloud Web Viewer v1.3.2/Confidential_CloudWebViewer_v1.3.2_MMI_Kor/media/image23.png
```

- 해상도: **1428 × 906** PNG (SharePoint `Slide*.jpg` 1280×720 JPEG보다 선명).
- 출처: MMI PPT `ppt/media/` 에서 추출한 **삽입 비트맵**. Section 모듈 레이아웃·오버레이·눈금 맞출 때 **이 파일을 기준**으로 한다.

### image23이 담는 UI (Section Layout 본문)

Clever Space **전체 셸**(상단 툴바·헤더·사이드바·MPR/Section 토글)은 **포함하지 않는다.**  
그 부분은 PPT **Shape/텍스트**(`Slide7.jpg` 등 슬라이드 합성본 + `MMI.md` 1.1)로만 설명된다.  
**Section 모듈·PoC가 구현하는 “뷰어 3영역”** 의 기준 화면이 image23이다.

```
┌─────────────────────┬──────────────────────────┐
│ Scout (좌상)         │                          │
│ Axial + Curve       │   Section (우, 세로 통합)   │
│ 오버레이            │   3×3 Grid (기본)         │
│                     │   드롭다운 "3x3"          │
├─────────────────────┤                          │
│ Panorama (좌하)      │                          │
│ 파노라마 + 선 오버레이 │                          │
└─────────────────────┴──────────────────────────┘
```

| 영역 | image23에서 확인할 요소 | MMI 대응 |
| --- | --- | --- |
| **Scout** | Axial CT, R/L, 50mm 세로 눈금, 곡선(녹색)·호장 번호, Section line(빨간 수직선), TH/INT/Total Slice, 환자·날짜, 상단 1~7 탭·Scout 라벨 | 1.2, 1.3, 1.7 |
| **Panorama** | Panorama 라벨, R/L, 20mm 눈금, 가로 경계(노란/흰 점선), 세로 9선+가운데 Active(빨강/녹색), TH/INT, 각도 보조선(파란) | 1.4, 1.8 |
| **Section** | Section 라벨, **3×3** 그리드 선택, 타일 번호(예: 135~143), 타일별 B/L, 가로·세로 mm 눈금(10·20·30), 우상단 최대화 아이콘 | 1.2, 1.9 |
| **공통** | 다크 배경, 뷰별 우상단 expand(최대화), W/L·Filter 텍스트 오버레이 스타일 | 1.2, 1.11 |

Section 모듈(`scp-section-poc` `SectionViewer`) CSS Grid와 동일 구조:

- `gridTemplateColumns: 1fr 2fr`
- `gridTemplateRows: 2fr 1fr`
- areas: `scout | section` / `panorama | section`

PoC는 이미 이 비율을 따른다. MMI 정합 시 **image23의 비율·오버레이·눈금·라벨 위치**를 image23 기준으로 맞춘다.

### image23 밖 — Clever Space 셸 (접목 시 CW Viewer)

| UI | 어디서 보나 | Section 모듈 범위 |
| --- | --- | --- |
| [MPR] / [Section] 토글 | `Slide7.jpg`, MMI 1.1 | 접목 — `cloudwebviewer` |
| 상단 공통 툴바 (Panning, Zoom, Length…) | Slide 합성본, MMI 1.12~1.13 | 접목 또는 MPR 재사용 |
| Clever Space 헤더·좌측 사이드바 | Slide 합성본 | 접목 |
| 빨간 원·숫자 주석 (기획 설명) | PPT Shape | 구현 요소 **아님** |

### `media/` 폴더 사용 규칙

1. **레이아웃·뷰어 UX** 질문 → 먼저 **image23.png** 를 연다.
2. 특정 슬라이드 확대·부분 동작 → `media/` 다른 파일 또는 `SlideNN.jpg` + `MMI.md` 해당 절.
3. **에셋으로 복사해 쓰지 않는다** — CT 영상·UI는 목업 참고용. 구현은 PoC/WebGL·Canvas로 재생성.
4. `media/*.svg` — Office 아이콘 등. CW Viewer 아이콘은 제품 디자인 시스템 따름.

### PoC · Section 모듈과 image23 갭 (구현 시 의식)

| 항목 | image23 (MMI) | PoC 현재 | Section 모듈 |
| --- | --- | --- | --- |
| Scout 상단 1~7 탭 | 있음 | 없음 | MMI 1.2 확인 후 |
| Section 3×3 드롭다운 | 있음 | 고정 3×3 | v1.3.2는 3×3만이면 UI 생략 가능 |
| Total Slice + 슬라이스 인덱스 | 있음 | 부분 | **1.9 스크롤** 구현 시 필수 |
| Panorama 20mm / Scout 50mm 눈금 | 있음 | ViewVerticalScaleBar20mm 등 | 정합 |
| Clever Space 툴바·토글 | image23 **없음** | 없음 | 접목 |

---

## 4.2 MMI PPT comments — 변경 이력 보조 정본

위치: `Confidential_CloudWebViewer_v1.3.2_MMI_Kor/comments/` (PowerPoint modern comment XML 6개, 기획 Jessi, 2026-07-01~08).

PLAN-1287 Jira와 동일 수신자(Scott·Raymond·Thomas)에게 보낸 PPT 측 변경 알림이다. 본문 상세는 `MMI.md`·PPT 슬라이드에 있고, comment는 결정 근거·시점·MMI.md 드리프트 보정용이다. **unzip 전체·XML 원본은 레포에 필수 아님** — 본 절 요약만으로 Spec 작성 가능.

### 코멘트 요약 (Section 모듈 관련)

| 일자 | 슬라이드(대략) | 내용 | Spec·구현 |
| --- | --- | --- | --- |
| 7/7 | 1.5 Draw Curve | Clever Space MPR에 ESC 없음 → Section도 **ESC 미적용** | ESC 핸들러 구현 금지 |
| 7/7 | 1.5 Draw Curve | **점 1개일 때 더블클릭** → curve 종료 안 됨, 점 1개만 유지 | 종료는 point ≥ 2일 때만 |
| 7/7 | 1.8 Panorama | Active section line **±45° 회전 v1.3.2 스펙아웃** | PLAN-1287 #3, MMI 반영됨 |
| 7/7 | 1.13 §6 | Overlay 표시 규칙 Clever One 기준으로 갱신 | MMI 775행~ §6 |
| 7/8 | 1.14 Save | proj에 Curve 저장 확인 → **proj 기반 초기 세팅** 추가 | Curve 있으면 복원 |
| 7/8 | 1.14 Save | Clever One에서 **Section view 1회 이상 열어야** proj에 Curve 기록 → **없을 수 있음** | 없으면 EP01_F005와 동일 blank |
| 7/1·7/7 | 1.3·1.5 B/L | Ez3D-i porting 검토 → 코드 확인 어려움 → **기획 신규 정의, 7/10 목표** | Raymond 초안 → Jessi confirm 대기 |
| 7/1 | 여러 | "Clever One 기준 보강" (본문 없음) | 해당 슬라이드·MMI 본문 참조 |

### MMI.md 드리프트 (Spec 작성 시 주의)

추출본 `MMI.md`가 PPT 최신보다 뒤처질 수 있다. 아래는 **§4.2·PLAN-1287이 MMI.md보다 우선**.

| 항목 | PPT comment (최신) | `MMI.md` 추출본 |
| --- | --- | --- |
| Draw Curve ESC | 미적용 | 273행 ESC 종료 문구 **잔존** |
| 1점 더블클릭 | 종료 안 됨 | **미기재** |
| proj Curve 없음 | blank 허용 | 840행 복원만, **예외 미명시** |
| ±45° 회전 | 스펙아웃 | 반영됨 |
| Overlay §6 | 갱신 | 반영됨 |

### Spec·구현 체크리스트 (comment 확정분)

1. Draw Curve: ESC 없음. 더블클릭 종료는 2점 이상. 1점 더블클릭 무시.
2. 초기 로드: prj에 Curve 없음 → Draw Curve 초기·Pano/Section blank (Clever One Section 미오픈 prj 포함).
3. B/L: 기획 신규 정의(7/10 목표) 수령 전 자동 판정 구현 확정 보류. 폴백 L/B Switching.
4. ±45° 회전: v1.3.2 구현·Spec 제외.
5. Overlay: MMI §6 + Normal 허용 오차 Spec 수치화.

---

## 5. 읽기 순서 (새 세션)

1. 본 문서 (§4.1 image23, **§4.2 PPT comments**)
2. **UI 시각 정본**: `Confidential_CloudWebViewer_v1.3.2_MMI_Kor/media/image23.png` (§4.1)
3. [Section-Module-개발계획.md](./Section-Module-개발계획.md)
4. [MMI.md](./Confidential_CloudWebViewer_v1.3.2_MMI_Kor/MMI.md) — 1.1~1.14 + Overlay §6 (775행~) + Save Project. **§4.2와 충돌 시 §4.2 우선**
5. [PLAN-1287.md](../PLAN-1287.md) — 기획 확정·B/L 알고리즘
6. [MMI_개발실리뷰.md](./Confidential_CloudWebViewer_v1.3.2_MMI_개발실리뷰.md) — 공수·리스크·아키텍처
7. [WebSectionView_PoC_OnePager.md](../WebSectionView_PoC_OnePager.md) — PoC 배경
8. Phase 결과: 본 문서 **§7.9** (인라인 정본). 원문 필요 시 [Phase5](../Phase5/Phase5_SectionView_결과.md) 등
9. 코드: `scp-section-poc/README.md` → `packages/core`, `packages/components`

구현 착수 시 추가:

- `scp-section-poc/packages/core/src/section/section.ts` — 9단면 수학
- `scp-section-poc/packages/components/src/hooks/useScoutAxialUi.ts` — 공유 상태
- `scp-section-poc/packages/components/src/SectionViewer.tsx` — 레이아웃·생성 스로틀

접목·Integration Spec 작성 시:

- `cloudwebviewer/README.md` — Clever Space 뷰어 구조
- CW Viewer 담당자와 MPR prj 저장/로드 존재 여부 확인

---

## 6. 기획 확정 사항 (반드시 Spec·구현에 반영)

PLAN-1287 Jessi 회신 + MMI 업데이트 + §4.2 PPT comments 기준. 상세 표는 `Section-Module-개발계획.md` §5.

| MMI | 항목 | 확정 |
| --- | --- | --- |
| 1.14 | Save Project | MPR과 동일. Desktop→Web 최초만. Clever One sync 없음. proj Curve 있으면 복원 |
| 1.14 | proj Curve 없음 | Clever One Section 미오픈 prj 등 — Curve 없으면 Pano/Section blank (§4.2 comment 913) |
| 1.11·1.12 | 계측·주석 | prj 저장. Overlay 규칙 MMI §6 |
| 1.8 | ±45° 회전 | v1.3.2 스펙아웃. Save 항목 ⑧ 회전 각도 삭제 |
| 1.6·1.7 | BL/LB 기준점 | 포함 |
| 1.5 | B/L 자동 | Raymond 초안 → 기획 confirm. 기획 신규 정의 7/10 목표 (§4.2). 폴백 L/B Switching |
| 1.5 | Draw Curve ESC | **미적용** — Clever Space MPR 동일 (§4.2 comment 901) |
| 1.5 | Draw Curve 1점 더블클릭 | curve **종료 안 됨**, 점 1개 유지. 종료는 point ≥ 2 (§4.2) |
| 1.10 | Thickness | 기본 0mm. combo 30mm. drag 상한 없음(Ez3D-i·Clever One). 개발실 30mm cap 가능 |
| 1.10 | Draw 중 Thickness/Interval | curve 취소 없음, 즉시 적용 |
| 1.5 | Draw curve 표시 | Active line 실시간. Section 이미지 완료 후 1회 |
| 1.9 | slice 더블클릭 최대화 | 포함 |
| — | 모바일 | v1.3.2 마우스 전용 |
| — | Scout 명칭 | Scout (7/10 검토) |

### 6.1 Overlay 표시 규칙 (MMI EP01_F013 §6)

- Overlay는 Curve + 생성 시점 평면(point, normal)에 귀속.
- Section 표시: (1) 거리 ≤ ±Interval/2, (2) Normal 허용 오차 — Spec에서 수치화.
- Curve point 변경: 일시 미표시 가능, 데이터 삭제 아님.
- Interval 변경: normal 유지, 원위치 복귀 시 재표시.
- Thickness: Overlay 표시 조건 무영향.
- MPR 레이아웃과 Overlay 공유하지 않음.

### 6.2 B/L 자동 판정 알고리즘 (PLAN-1287 Raymond 초안)

기획 confirm 전까지 draft. confirm 후 Spec §고정.

1. 입력: Scout(Axial) 화면 좌표 curve 제어점. 첫 점 = BL/LB 기준점.
2. 시작 반구: 화면 가로 중앙선 기준 좌/우.
3. 초기 방향: 1→2 벡터로 가로/세로 우세, 좌→우·우→좌·위→아래·아래→위.
4. 기본 B/L: 좌반구+좌→우 = Section 왼쪽 B (표는 PLAN-1287 §2.5).
5. 동적 반전(토글 누적): 접선 급반전(내적<0), 중앙선 교차, 기준점 관련 반전.
6. 예외: 점 1개 — 라벨 미표시 또는 임시 기본값(confirm 요청). 불확실 시 L/B Switching.

PoC 현재: `section.ts`에서 출력 열 `nU-1-iu` 좌우 반전만. Scout에 +법선 쪽 B 라벨 고정 표시. 자동 판정·blPolarity 없음.

---

## 7. PoC에서 검증된 기술 Knowhow

### 7.1 WebGL Context 전략 (Phase 1)

- 문제: Chrome WebGL Context 최대 ~15개. 11 View 각각 Context → CONTEXT_LOST_WEBGL.
- 해결: Canvas 3개 + WebGL Context 3개. Section 1 Canvas 안에서 viewport/scissor 9분할.
- Scout(CT 로드 후): Canvas 2D만 사용 → 실질 WebGL Context 2개(Panorama + Section).

### 7.2 뷰별 렌더링 경로 (PoC 확정)

| 뷰 | 연산 | 표시 |
| --- | --- | --- |
| Scout | Axial 슬라이스 추출 | Canvas 2D + 곡선 오버레이 Canvas 2D |
| Panorama | JS trilinear + 슬랩(MIP/mean/percentile) | Canvas 2D (또는 WebGL 텍스처) |
| Section 9장 | JS 또는 WASM trilinear + 슬랩 | WebGL2 9 viewport (또는 Canvas 2D 비교) |

Section Grid는 WebGL2 채택이 PoC 핵심 결론. CPU만으로는 9장 실시간 갱신에 구조적 한계(Phase 1 결과 §「왜 WebGL이 필요한가」).

### 7.3 Section 단면 기하 (Phase 5 — 구현 시 반드시 유지)

- 각 단면 평면: 치열궁에 직교 (`evaluateCurveAtArcMm`의 법선 n̂ × 환자 Z).
- 슬랩 적분 축: 호 접선 방향 (파노라마 열 평면과 다름 — `section.ts` 주석).
- 9장 위치: `sectionCenterMm + (k-4)*intervalMm`, k=0..8.
- B/L 정렬: 픽셀 출력 시 열 좌우 반전 (`nU - 1 - iu`).

### 7.4 곡선·호장 (Phase 3~4)

- Catmull-Rom spline (`packages/core/src/curve/catmullRom.ts`).
- `buildCurveArcContext`: 밀집 폴리라인 + 누적 호장 mm.
- `pixelToClosestArcMm`: Scout 클릭 → 가장 가까운 호장 위치.
- 파노라마: `generatePanoramaImageData`, 열 간격 `panoramaColumnSpacingFromVolumeSpacing`.

### 7.5 CT Volume 로드 (Phase 2)

- S3 `scp-section-ct-data` → fetch stream → fflate Unzip → dicom-parser → `Int16Array` 3D.
- `CTVolumeLoader.ts`. stream-zip-unzip PoC 패턴 참고.
- 메모리: 치과 CT ~100~250MB, 브라우저 내 수용.

### 7.6 성능 수치 (Phase 5 측정 — Section 모듈 NFR 기준선)

9장 생성 시간 (`SectionGen` 콘솔 로그, 동일 볼륨 496×496×399):

| 연산 | 평균 ms | 범위 ms |
| --- | ---: | --- |
| JS | 393.2 | 362.7 ~ 427.4 |
| WASM 상주 | 415.9 | 371.9 ~ 454.9 |
| WASM 매번 복사 | 420.3 | 370.9 ~ 483.2 |

- PoC 기본 연산: JS (`sectionComputeMode: 'js'`).
- WASM은 복사·글루 비용으로 JS 대비 이점 제한적. Section 모듈은 JS 우선, 필요 시 WASM·Worker 검토.
- SectionViewer 재생성 디바운스: **48ms** `setTimeout` + seq 취소.
- 개발실 리뷰: 단면 9장 ~390~420ms → 30 FPS(33ms) 미달. Section Slice 스크롤이 최대 리스크.
- 대응 방향: 디바운스 강화, 캐싱(이미 생성 slice 재사용), 표시 분리(이전 이미지 유지), Thickness 상한, Worker/WASM 단계적 검토.

### 7.7 PoC 기본값 vs MMI v1.3.2 (구현 시 변경 필요)

| 항목 | PoC 현재 | MMI/기획 |
| --- | --- | --- |
| Thickness (slabHalfWidthMm) | `DEFAULT_PANORAMA_OPTIONS.slabHalfWidthMm = 3` (≈6mm 슬랩) | 기본 **0mm** |
| Section 가로 폭 | `DEFAULT_SECTION_WIDTH_MM = 30` | MMI 폭 기본 30mm (일치) |
| Section Z 높이 | `DEFAULT_SECTION_HEIGHT_MM = 60` | Panorama 경계 100mm 등 MMI 확인 |
| Interval | `useCurveEditor` 기본 1mm | MMI Setting UI |
| Draw curve Section 이미지 | 점 2개 이상이면 실시간 생성 | **완료 후 1회** |
| B/L | 고정 반전·라벨만 | 자동 판정 + Switching + 기준점 |
| Section Slice 페이징 | 중심 9장만 | **전체 인덱싱 + 스크롤** (1.9) |

### 7.8 이전 연구 이슈 (참고)

- POPV-87: vtkImageMapper/vtkImageReslice 2D View — Web 전환 배경.
- POPV-959: CONTEXT_LOST_WEBGL — 15 Context 제한 → 3 Context 전략으로 해소.
- EZDM-9: RemoteViz — Server-side 대안 검토 완료(Closed). Section 모듈은 Client-first 유지.

### 7.9 PoC Phase별 상세 노하우 (인라인 정본)

아래는 Phase 1~5 결과 문서·코드에서 추출한 **구현·디버깅·설계 결정** 전체이다. Section 모듈 개발 시 Phase 문서를 다시 열지 않아도 되도록 인라인했다. 원문: `../Phase1/` ~ `../Phase5/`, `../WebSectionView_PoC_OnePager.md`.

#### 7.9.1 Phase 0 배경 — 왜 이 PoC를 했는가

| 이슈 | 내용 | PoC 대응 |
| --- | --- | --- |
| POPV-87 | vtkImageMapper/vtkImageReslice 기반 2D View | Web 자체 Reslice(trilinear)로 대체 |
| POPV-959 | Chrome WebGL Context ~15개 한도, 초과 시 CONTEXT_LOST_WEBGL | 3 Canvas + 3 Context + viewport 분할 |
| EZDM-9 | RemoteViz(Server-side Rendering) | Closed. Client-first 유지, Phase 6에서 WASM/Server 비교만 검토 |
| 레거시 실패 추정 | View마다 Context 11개 | 전략 B(3 Context)로 해소 |

OnePager 로드맵 Phase 6(종합 성능·아키텍처), Phase 7(치아 Segmentation 오버레이)은 **미착수**. Section 모듈 v1.3.2 범위 밖이나 향후 참고.

#### 7.9.2 Phase 1 — WebGL Multi-View

**목표**: 11 View(Scout 1 + Panorama 1 + Section 9) 동시 표시, Context Lost 없음.

**전략 비교 (OnePager)**:

| 전략 | Canvas | WebGL Context | Viewport |
| --- | ---: | ---: | --- |
| A (대안) | 1 | 1 | 11분할 |
| B (채택) | 3 | 3 | Scout 1 + Panorama 1 + Section 9 |

**Canvas / Context / Viewport 계층**:

- Canvas = DOM 픽셀 표면. Context = GPU 게이트웨이(탭당 ~16개 한도). Viewport = Context 내부 그리기 영역 상태(개수 무제한).
- Section Grid: 동일 Context에서 `gl.viewport` + `gl.scissor` 9회. 타일마다 별도 Texture.
- `useWebGLCanvas`: `devicePixelRatio`로 drawing buffer vs CSS pixel 정합.
- `QuadRenderer`: Context당 Program+VAO+VBO 1세트. `ViewportManager.calculateGrid(3,3)`.
- Context Lost 핸들러 등록. Phase 1 성공 기준 = Lost 0건.

**WebGL 채택 이론 근거** (Phase 1 결과):

- 9뷰 × 512² × 8 voxel trilinear = 프레임당 수백만~수천만 fetch. data-parallel → GPU 셰이더 1:1.
- CPU 경로는 계산 후 `putImageData` 또는 텍스처 업로드로 **read-back 비용** 매 프레임 발생. WebGL은 회수 0.
- 30 FPS(33ms/프레임) 목표에 CPU 단일 스레드는 구조적으로 부적합. Phase 5에서 JS 9장 ~393ms로 재확인.

**Phase 1 이후 Scout 변화**: CT 로드 후 Scout는 Canvas 2D만 사용 → 실질 WebGL Context **2개**(Panorama+Section). Phase 1 정적 데모만 Scout WebGL.

**데모**: http://scp-section-demo.test.scp.esclouddev.com/ 탭 「Phase 1: Multi-View」.

#### 7.9.3 Phase 2 — CT Download · Axial Slice

**파이프라인**:

```
S3 scp-section-ct-data (ap-northeast-2)
  → fetch ReadableStream
  → fflate Unzip/UnzipInflate (다운로드·압축해제 동시)
  → dicom-parser (파일별 onfile)
  → 슬라이스 정렬 (Instance Number 또는 Image Position Z)
  → Int16Array 연속 3D Volume + VolumeMetadata
  → SectionViewer(volume) → ScoutView Canvas 2D
```

**S3 / CORS**:

| 항목 | 값 |
| --- | --- |
| 버킷 | scp-section-ct-data |
| 리전 | ap-northeast-2 |
| 샘플 | ct-data/sample-ct-01.zip ~ sample-ct-04.zip |
| 접근 | PoC 퍼블릭 읽기, Demo+localhost CORS |

**DICOM 추출 태그** (`CTVolumeLoader.ts`): Rows/Columns, Pixel Spacing, Image Position Patient, Instance Number, WC/WW, Bits Allocated, Rescale Intercept/Slope, Pixel Data.

**Z spacing**: 인접 슬라이스 IPP z 차이 우선. 비정상이면 `(0018,0088) Spacing Between Slices` 폴백 (Phase 5 이슈에서도 동일).

**Volume 메타데이터 규약**:

- `dimensions`: `[columns, rows, sliceCount]` = X(열)·Y(행)·Z(슬라이스 수).
- `spacing`: `[pixelSpacingX, pixelSpacingY, sliceSpacing]` mm. DICOM Pixel Spacing row/column 문자열을 **열·행 순**으로 재배치.
- `volume.data` 인덱스: `[z * (cols*rows) + y * cols + x]`, `Int16`.
- 메모리: 512×512×200~500 ≈ 100~250MB, 브라우저 1~2GB 한도 내.

**UI**: `CTLoader.tsx` — CT 선택, Load CT, 3단계 진행(downloading/parsing/building), 완료 ms, 에러 표시.

**stream-zip-unzip PoC와 차이**: stream-zip-unzip은 썸네일 미리보기. 본 PoC는 **전 슬라이스 연속 3D Volume** (Reslice 목적).

**레거시**: `AxialSliceViewer.tsx` — ScoutView에 통합됐으나 독립 검증용 유지.

**ScoutView volume 모드**: Slice 0~(nz-1), WC -1000~3000, WW 1~4000, Rescale→HU→Windowing.

#### 7.9.4 Phase 3 — 치열궁 곡선 (Arch Curve)

**Canvas 2겹 (Scout)**:

```
Scout 영역
├── Canvas 1: CT Axial (2D)
├── Canvas 2: Curve Overlay (투명, 2D, 마우스 이벤트)
└── Edit Curve 토글 버튼
```

**좌표계 4단**:

| 계층 | 설명 |
| --- | --- |
| Screen | clientX/Y |
| Canvas | element bounding rect |
| Slice | CT 픽셀 (0~cols, 0~rows) |
| Physical | mm (Pixel Spacing) |

`ScoutView.screenToSliceCoords()`: **objectFit: contain** 오프셋·스케일 보정 필수. 마우스→슬라이스 픽셀 변환.

**Catmull-Rom** (`catmullRom.ts`):

- `catmullRomPoint`, `catmullRomTangent`, `sampleSpline` — 양 끝 **반사 가상 제어점**으로 C1 연속.
- `sampleAtInterval` — mm 간격 재샘플 + 수직 단위벡터.
- `findClosestPointOnCurve` — 곡선 삽입점 인덱스.
- 세그먼트당 샘플: `useCurveEditor` 20, `buildCurveArcContext` 48 (Section용 밀집).

**useCurveEditor 상수**:

| 상수 | 값 | 의미 |
| --- | ---: | --- |
| POINT_HIT_RADIUS | 8px | 제어점 히트 |
| CURVE_HIT_DISTANCE | 10px | 곡선 히트 |
| 드래그 시작 | 3px 이동 | 클릭 vs 드래그 구분 |
| sectionInterval 기본 | 1mm | INT 슬라이더 0.5~5.0, 0.1 step |

**편집 UX**: 빈 곳 클릭=끝에 추가, 곡선 근처=삽입, 드래그=이동, 우클릭=삭제. Edit OFF 시 곡선 유지·편집 불가.

**Section Cut 수직선**: INT 간격 붉은 반투명 선 (Scout 오버레이). Phase 3 빨간선 길이와 Core `slabHalfWidthMm`은 **별개 개념**(Phase 4 주의).

**AI 자동 곡선 검출**: OpenCV/VTDentalArchDetection 레거시 있으나 **본 PoC 미사용**. 수동 제어점만.

#### 7.9.5 Phase 4 — 파노라마 (Curved MPR)

**렌더 경로**: volume+axialUi 있으면 **Canvas 2D**에 `generatePanoramaImageData` 결과. volume 없으면 WebGL 정적 `panorama.png`.

**DEFAULT_PANORAMA_OPTIONS** (`panorama.ts`):

| 필드 | 기본값 | 의미 |
| --- | ---: | --- |
| panoramaColumnSpacingMm | 0.4 | 호장 방향 열 간격(mm). 실제는 `panoramaColumnSpacingFromVolumeSpacing` = min(sx,sy) 우선 |
| slabHalfWidthMm | 3 | 법선 방향 슬랩 반폭 → **전체 ~6mm** (MMI 0mm와 불일치) |
| slabSampleStepMm | 0.5 | 슬랩 내부 스텝 |
| projection | mip | mip / mean / percentile |
| percentile | 0.9 | percentile 모드 시 |

**UI 투영 프리셋** (`PanoramaUiPreset`): mip, mean, p95, p90, p80, p70, p60, p50.

**생성 흐름**:

1. 제어점 2개 이상 (3개 이상 권장 — 스플라인 시각).
2. 툴바 투영 선택 → 「파노라마 생성」 클릭 (명시적).
3. 곡선·슬라이스·투영 변경 시 **자동 재생성 없음** — 다시 버튼 필요.
4. **최초 생성 성공 후** WC/WW만 변경 → **280ms 디바운스** 자동 재생성 (`PanoramaView`).
5. CT 재로드 시 파노라마 비트맵·플래그 초기화.

**생성 시간 (관측, 동일 PoC 환경)**:

| 투영 | 대략 |
| --- | --- |
| MIP / Mean | 0.1~0.2초 |
| 백분위 | 0.3~0.4초 (슬랩 sort 비용) |

OnePager 1초 목표 여유. **파노라마는 WASM 후순위** (속도만으로 WASM 불필요). Worker는 WC/WW 잦은 재생성 시 UI 스레드 분리용.

**알려진 제한**: Image Orientation Patient 전개 미지원(축 정렬 볼륨 가정). 단일 스레드 JS — 큰 볼륨·촘촘한 열 간격 시 UI 멈춤.

**Panorama ↔ Section 연동**: 동일 `axialUi` — `sectionCenterMm`, Z top/bottom, WC/WW, curve 공유. Panorama 위 9개 세로선 + 가운데 Active line 오버레이.

#### 7.9.6 Phase 5 — 9장 Section (핵심)

**픽셀 파이프라인** (`generateSectionImagesData`):

1. `buildCurveArcContext` → 호장 `sK`마다 `P_k`, `T̂_k`, `N̂_k`.
2. 단면 평면: u ∥ `T̂`(치열궁 따라), v ∥ 환자 Z. **법선 `N̂`은 Axial 내 곡선 수직.**
3. **슬랩 적분 축 = 접선 `T̂` 방향** (파노라마 열 평면과 다름). 초기 구현이 “파노라마 조각”처럼 보이던 문제의 **정정 사항**.
4. 각 (iu,j): uMm,vMm → 3D → 슬랩 스텝마다 `sampleTrilinear` → `reduceSlabHu`(MIP/mean/percentile) → `windowToByte`.
5. 출력 열 `iOut = nU-1-iu` (B/L 해부 정렬). JS·WASM 동일.

**해상도**:

- `nU = max(16, ceil(sectionWidthMm / min(sx,sy)))`
- `nV = max(16, ceil(zSpan / sz))`, zSpan = bottomMm - topMm

**연산 모드** (`SectionComputeMode`):

| 모드 | 설명 |
| --- | --- |
| js | `generateSectionImagesData` (PoC 기본) |
| wasm-copy | 매 호출 볼륨 WASM 힙 복사 |
| wasm-resident | 동일 CTVolume 참조 시 복사 생략 |

`SECTION_COMPUTE_INCLUDE_LEGACY_WASM_COPY` (useScoutAxialUi.ts): false면 툴바에서 wasm-copy 숨김.

**WASM 패키지** (`packages/section-wasm`):

- AssemblyScript (`assembly/index.ts`) — JS와 동일 trilinear+슬랩 수식.
- `initSectionWasm`, `generateSectionImagesDataWasm`, `generateSectionImagesDataWasmResident`.
- 빌드: `pnpm --filter @ewoosoft/scp-section-wasm build` → `dist/section.wasm`.
- Vite `sectionWasmDevPlugin` (`apps/section-demo/vite.config.ts`): `/section-wasm.wasm` 직접 서빙. 없으면 404 안내.

**측정 구간 정의**: `nU`/`nV` 확정 후 ~ 9장 ImageData 완료. `buildCurveArcContext`·WASM instantiate 제외. WASM 경로는 힙 grow·볼륨 복사·RGBA 패킹 포함.

**WebGL vs Canvas2D 표시**: 동일 ImageData 소비. 체감 차이 거의 없음. WebGL2 미세 선형 보간 가능.

**SectionGrid 표시**:

- `texturesLiveRef`: ImageData 갱신 시 cleanup/render 레이스 방지 — 업로드 직후 ref 동기화.
- `createTextureFromImageData` (TextureLoader).
- `SectionTileChrome`: contain·가로세로 동일 mm/pixel, 1mm/10mm 눈금, B/L 라벨.
- `sectionRulerConstants`: 우측·하단 ruler 여백 px.
- 툴바: WebGL/Canvas2D 토글, JS/WASM 토글, 마지막 생성 ms.

#### 7.9.7 UI · 상태 · 동기화 (Phase 5 §4.5 — Section 모듈에서 재사용)

| 상태/동작 | 규칙 |
| --- | --- |
| sectionCenterMm | 초기 -1(미배치). 곡선 유효 시 호장 중앙 자동. Scout 클릭·Panorama 중앙선 드래그로 변경 |
| Sec 폭 (sectionWidthMm) | Scout 하단 슬라이더. **드래그 중 draft만**, pointer up/blur에서 커밋 → 재생성 |
| Sec 높이 (top/bottom) | **Z 구간 중점 유지**하며 상·하 조정. `zExtent` 클램프. Panorama Top/Bottom 핸들과 **동일 state** |
| bitmapSectionLayout | 마지막 9장 apply 성공 시점의 widthMm/heightMm. `tileMmMetrics`에 사용 |
| 눈금·비트맵 짝 | axialUi 최신 mm가 아닌 **bitmapSectionLayout** mm — 새 ImageData 전 이미지 늘어보임 방지 |
| Edit Curve 모드 | Section 위치 픽 **차단** (곡선 편집과 충돌 방지) |
| Section 재생성 트리거 | curve, slice, center, interval, top/bottom, width, WC/WW, 투영 변경 → **48ms setTimeout** + seq 취소 |
| Panorama WC/WW | 생성 후 변경 시 **280ms** 디바운스 자동 재생성 |

**키보드 좌·우 INT 이동**: PoC **미구현**. CleverOne 비교표의 선택 항목. Section 모듈에서 접근성 필요 시 후속(포커스 영역 한정 시 구현 용이).

#### 7.9.8 개발 중 발견 이슈 · 해결 (재발 방지)

| 이슈 | 원인 | 해결 |
| --- | --- | --- |
| WASM 404 | `public/section-wasm.wasm` 없음 | Vite `serve-section-wasm` 플러그인 |
| WebGL bindTexture 삭제 객체 | texture cleanup과 renderGrid 동일 틱 레이스 | `texturesLiveRef` |
| sectionCenterMm=0 초기 | 곡선 전 0이면 9장 잘못 겹침 | -1 미배치 → 중앙 채움 |
| DICOM Z spacing 깨짐 | IPP z만 신뢰 불가 | Spacing Between Slices 폴백 |
| 폭·높이 커밋 vs 비트맵 지연 | layout 먼저 바뀌고 ImageData 늦음 | bitmapSectionLayout로 눈금 고정 |
| Section 슬랩 축 오류 | 초기 파노라마 열 평면 재사용 | 슬랩=접선 방향으로 정정 (§7.9.6) |

#### 7.9.9 레거시 VTK / 다중 viewport vs 웹 PoC (Phase 5 §4.7)

| 구분 | 레거시(VTK 등) | scp-section-poc |
| --- | --- | --- |
| 이벤트 | 단일 윈도우·다중 viewport 라우팅 까다로움 | DOM별 canvas, 요소별 리스너 |
| Section WebGL | VTK interactor·카메라 결합 | 표시 전용. 조작은 Scout/Panorama/슬라이더 |
| 치열궁 | OpenCV 자동 검출 | Catmull-Rom 수동 편집 |

웹 PoC 경로에서는 VTK 클래스 난제 **재현 안 됨**. 네이티브 VTK에 동일 UI 붙일 때는 포커스·라우팅 재설계 필요.

#### 7.9.10 Phase 6 · 7 로드맵 (미착수, 참고)

**Phase 6** — 전체 파이프라인 성능·아키텍처 결정:

- Client-only JS/WebGL vs Client+WASM vs Server-side Compute vs RemoteViz.
- 부속 PoC: GPU vs CPU 정량 비교 (WebGL 채택 **재검토 아님**, 보고용).

**Phase 7** — 치아 Segmentation 오버레이:

- Scout/Section 윤곽선. 전통 CV vs AI(ONNX/TF.js). v1.3.2 MMI 범위 밖.

#### 7.9.11 추가 코드·모듈 참고

| 파일/모듈 | 노하우 |
| --- | --- |
| `packages/core/src/webgl/createWebGLContext.ts` | webgl2 컨텍스트 생성·Lost 핸들러 |
| `packages/components/src/CTLoader.tsx` | S3 URL 목록, onVolumeLoaded 콜백 |
| `packages/components/src/ViewVerticalScaleBar20mm.tsx` | Scout·Panorama 우측 20mm 세로 눈금 |
| `packages/components/src/sectionRulerConstants.ts` | Section grid ruler px |
| `apps/section-demo/vite.config.ts` | monorepo alias, wasm dev plugin |
| `logSectionGenerationSample` | `{"tag":"SectionGen","mode","ms"}` JSON 한 줄 — 벤치마크 수집 |

**App.tsx 탭 의미**: 「Phase 1」= 정적 Multi-View. 「CT Volume」= Phase 2~5 통합(탭 이름≠Phase 번호 1:1).

**성능 프로파일 권장**: Section Slice 스크롤 구현 시 `SectionGen` 로그 + Chrome Performance long task 함께 기록.

---

## 8. scp-section-poc 코드베이스 맵

### 8.1 구조

```
scp-section-poc/
├── packages/
│   ├── core/                    @ewoosoft/scp-section-core
│   ├── components/              @ewoosoft/scp-section-components
│   └── section-wasm/            @ewoosoft/scp-section-wasm (AssemblyScript)
├── apps/
│   └── section-demo/            Vite + React 데모
├── package.json                 pnpm workspaces + turbo
└── README.md
```

기술 스택: TypeScript, React 18, Vite, pnpm, Turborepo, WebGL2, fflate, dicom-parser.

### 8.2 실행

```bash
cd ~/Documents/Azure/scp-section-poc
pnpm install
pnpm dev          # http://localhost:5173
pnpm build
```

데모 배포: http://scp-section-demo.test.scp.esclouddev.com/

`apps/section-demo`: 탭 「CT Volume」에서 CT 로드 후 Scout·Panorama·Section 통합 뷰.

### 8.3 패키지 책임

| 패키지 | 책임 |
| --- | --- |
| scp-section-core | Volume, DICOM, Catmull-Rom, Panorama/Section ImageData 생성, WebGL 유틸 |
| scp-section-components | SectionViewer, ScoutView, PanoramaView, SectionGrid, hooks, CTLoader |
| scp-section-wasm | Section 9장 WASM 경로 (비교·옵션) |
| section-demo | PoC/Section 모듈 데모 앱 |

### 8.4 핵심 소스 파일

| 파일 | 역할 |
| --- | --- |
| `packages/core/src/section/section.ts` | 9단면 생성, `buildCurveArcContext`, `evaluateCurveAtArcMm`, `generateSectionImagesData` |
| `packages/core/src/panorama/panorama.ts` | 파노라마, trilinear, 슬랩, `DEFAULT_PANORAMA_OPTIONS` |
| `packages/core/src/curve/catmullRom.ts` | 스플라인, interval 샘플, 수직선 |
| `packages/core/src/dicom/CTVolumeLoader.ts` | S3 ZIP → Volume |
| `packages/core/src/webgl/TextureLoader.ts` | ImageData → WebGL 텍스처 |
| `packages/core/src/webgl/ViewportManager.ts` | 9 viewport 분할 |
| `packages/components/src/SectionViewer.tsx` | 11뷰 그리드, Section 생성 트리거·48ms 디바운스 |
| `packages/components/src/hooks/useScoutAxialUi.ts` | Scout/Panorama/Section 공유 상태 (slice, WC/WW, sectionCenter, 폭·높이) |
| `packages/components/src/hooks/useCurveEditor.ts` | 곡선 편집, interval, draw/edit 모드 |
| `packages/components/src/ScoutView.tsx` | Axial 2D, 곡선 오버레이, Active section line, B/L 라벨 |
| `packages/components/src/PanoramaView.tsx` | 파노라마 생성·표시, Section line 오버레이 |
| `packages/components/src/SectionGrid.tsx` | 3×3 WebGL/Canvas2D, B/L·눈금 |
| `packages/components/src/SectionTileChrome.tsx` | 타일 B/L, mm 눈금 |
| `packages/components/src/CTLoader.tsx` | S3 CT 선택·로드 UI |
| `packages/components/src/ViewVerticalScaleBar20mm.tsx` | Scout·Panorama 20mm 눈금 |
| `packages/components/src/sectionRulerConstants.ts` | Section ruler 여백 |
| `packages/section-wasm/assembly/index.ts` | WASM trilinear (JS 동일 수식) |
| `apps/section-demo/vite.config.ts` | alias, section-wasm dev plugin |
| `apps/section-demo/src/App.tsx` | 데모 진입, CTLoader + SectionViewer |

### 8.5 상태 흐름 (구현 시 유지·확장)

```
CTVolume 로드
  → useScoutAxialUi(volume)  // slice, WC/WW, curveEditor, sectionCenterMm, ...
  → ScoutView / PanoramaView / SectionViewer 가 동일 axialUi 공유
  → controlPoints >= 2 && sectionCenterMm >= 0
  → SectionViewer 48ms 후 generateSectionImagesData → SectionGrid
```

`sectionCenterMm === -1`이면 아직 미배치. 곡선 확정 후 호장 중앙으로 자동 설정.

`bitmapSectionLayout`: 9장 apply 성공 시 widthMm/heightMm 스냅샷 → SectionGrid `tileMmMetrics`에 전달. 새 ImageData 전 눈금·비트맵 불일치 방지 (§7.9.7).

---

## 9. MMI 1.1~1.14 — PoC 대비 구현 현황

개발실 리뷰 §2 표 + PoC 코드 기준. Section 모듈에서 채워야 할 갭.

| MMI | 기능 | PoC | Section 모듈 작업 |
| --- | --- | --- | --- |
| 1.1 | Layout 전환 | 데모만 | Section↔MPR 토글 UI (접목 시 CW 셸) |
| 1.2 | Layout 정보·ruler | 부분 | image23 눈금·라벨 정합. Section ruler 전체 축 (CleverOne 방식) |
| 1.3 | Scout Curve 요소 | 대부분 | B/L 자동, 기준점, thickness line |
| 1.4 | Panorama Line | 부분 | 경계 100mm, Ruler(선택) |
| 1.5 | Draw Curve | 부분 | ESC 미적용, 1점 더블클릭 무시, 완료 후 1회 Section, Active line 실시간 (§4.2) |
| 1.6 | Edit Curve | 부분 | BL/LB 기준점 drag, context menu |
| 1.7 | Scout 조작 | 부분 | thickness line drag, 폭 드래그(MMI), 기준점 |
| 1.8 | Panorama 조작 | 부분 | 위치 이동 PoC有. **±45° 회전 제외** |
| 1.9 | Section 조작 | 핵심 갭 | **Slice 스크롤·전체 인덱싱**, 더블클릭 최대화 |
| 1.10 | Thickness/Interval | 부분 | Thickness UI·0mm 기본·상한 정책, Setting 패널 |
| 1.11 | Windowing/Filter | Windowing만 | Image Filter MPR→Section |
| 1.12 | 계측·Arrow 등 | 없음 | Measure, Arrow, Free Draw, Angle |
| 1.13 | Section 공통 툴 | 최소 | Pan/Rotate/Zoom 등 MPR 수준 |
| 1.14 | Save Project | 없음 | prj 데이터 모델·직렬화. Curve 없음 시 blank (§4.2). 접목 시 CW prj I/O |

우선순위 (개발실 리뷰):

1. Section Slice 변경 (1.9) — 신규·성능 핵심
2. B/L + BL/LB 기준점 (1.3~1.7)
3. Thickness/Interval MMI 정합 (1.10)
4. Draw curve UX (1.5)
5. Overlay + 계측 (1.11·1.12) + §6 규칙
6. Save Project 데이터 모델 (1.14) — CW 팀과 경계 합의

---

## 10. 아키텍처 — Section 모듈 vs Cloud Web Viewer

### 10.1 Scout = MPR Axial 재사용 (제품 접목 시)

MMI·개발실 리뷰 §3.1: Scout는 Clever Space 기존 MPR Axial 컴포넌트 재사용 + Curve 오버레이.

- Section 모듈(PoC)에서는 Scout를 Canvas 2D로 독립 구현해도 됨.
- Integration Spec: 접목 시 Scout 슬롯을 CW MPR Axial로 교체. Thickness/Interval·Image Adjust는 MPR 쪽 동기화.

### 10.2 Section line vs Active section line (§3.2)

- Section line: Interval로 잘린 전체 slice 위치 시퀀스.
- Active section line: 현재 3×3에 보이는 9개 window.
- PoC: 중심 9장만. Section 모듈: **전체 개수·시작 인덱스·스크롤** 상태 머신 신규.

### 10.3 좌표계 (§3.3 — Save·Overlay 공통)

- 계측·Overlay를 prj에 저장하려면 **환자 볼륨 3D 좌표** 권장. 2D 픽셀만 저장 시 Curve/Interval 변경 시 무효.
- Overlay plane: point + normal (MMI §6).
- Curve 제어점: 볼륨 좌표 저장 권장 (개발실 리뷰 §4.1 D).

### 10.4 Save Project 범위 분리

| 책임 | Section 모듈 | CW Viewer 팀 |
| --- | --- | --- |
| 저장 항목·JSON 스키마 정의 | O | 협의 |
| 데모 localStorage/import/export | O (검증용) | — |
| 실제 prj 파일 I/O | API만 | O (MPR 기존 구현 통합) |
| Desktop→Web 최초 업로드 | — | O |

기획: Desktop→Web 단방향. Web→Desktop·양방향은 v1.3.2 범위 아님.

저장 항목 (MMI 1.14, 회전 ⑧ 제외): 레이아웃, slice/Active line 위치, 카메라, ShowGrid, Curve, Panorama 선, Thickness/Interval, Overlay, Windowing/Filter, B/L Switching, BL/LB 기준점.

초기 로드 (§4.2): prj에 Section Curve가 없으면 Draw Curve 초기 상태·Pano/Section blank. Clever One에서 Section view를 한 번도 열지 않은 Desktop prj는 Curve 필드가 비어 있을 수 있음.

---

## 11. AI 방법론

### 11.1 abc-dev-assistant (Spec·dev-chain)

레포: `~/Documents/Git/abc-dev-assistant`

| 작업 | 스킬 |
| --- | --- |
| Spec 작성 | `abc-spec-writer` |
| Spec 리뷰 | `abc-spec-review` |
| 설계 DBML/Swagger/TCL | `dev-chain-design` (필요 시) |
| 구현 (프론트) | `dev-chain-frontend` — Section 모듈은 React+TS |
| 검증 | `dev-chain-verify` |

진행 순서 (dev-process-guide):

```
PHASE 0   Spec (지금)
PHASE 1   설계 (필요 시 API·데이터 모델 TCL)
PHASE 2   Section 모듈 구현 (scp-section-poc)
PHASE 3   검증 (MMI·TCL·벤치마크)
```

### 11.2 es-toolkit (구현·PR)

| 명령 | 용도 |
| --- | --- |
| `/es-git` | 커밋·브랜치 |
| `/es-pr` | Azure DevOps PR |
| `/es-style` | 코드 스타일 |
| `/es-tdd` | 테스트 사이클 |
| `/es-review` | 변경 리뷰 |

scp-section-poc에 `CLAUDE.md` 없으면 Section 모듈 작업용으로 추가 검토 가능.

### 11.3 Section 모듈 Spec 목차 (작성 시)

파일명 예: `Section-Module-Spec-v1.3.2.md` (본 폴더)

1. 개요·범위·용어·참조
2. 시스템 맥락 (PoC 계승, CW Viewer 경계)
3. 기능 요구 (MMI 1.1~1.14 매핑)
4. Overlay §6 + normal 허용 오차
5. B/L 자동 판정 (confirm 후 고정)
6. 데이터 모델·prj 직렬화 (Curve 없음 시 blank — §4.2)
7. UI/UX·상호작용 (Draw curve §4.2: ESC 없음·1점 더블클릭, Thickness, Interval, slice 더블클릭 최대화)
8. NFR (성능·브라우저·마우스 전용)
9. 스펙아웃 (±45°, 모바일)
10. 공개 API·인계 인터페이스
11. Integration Spec 요약
12. 검증·DoD

Integration Spec은 별도 또는 §11로 CW Viewer 담당자와 공동.

---

## 12. 다음 작업 (우선순위 — 사용자 지시 없이 자동 착수 금지)

| 우선 | 작업 | 입력·산출 |
| ---: | --- | --- |
| 1 | Section 모듈 Spec v1.3.2 작성 | MMI, §4.2, PLAN-1287, 개발실 리뷰, 본 가이드 |
| 2 | B/L 알고리즘 기획 confirm 반영 | PLAN-1287 Jira. 7/10 기획 신규 정의 (§4.2) |
| 3 | Spec 리뷰 | 기획 + CW Viewer |
| 4 | Draw curve UX (§4.2) | ESC 제거, 1점 더블클릭 무시, point≥2 종료. `ScoutView` |
| 5 | Thickness 0mm·Draw curve 게이트 | `panorama.ts`, `SectionViewer.tsx` |
| 6 | Section Slice 스크롤·인덱싱 (1.9) | `section.ts`, 상태 모델, 벤치마크 |
| 7 | B/L 자동 + L/B Switch + BL/LB 기준점 | `ScoutView`, `SectionGrid`, 신규 `blPolarity` |
| 8 | Thickness/Interval Setting UI (1.10) | MMI 상한 정책 |
| 9 | Panorama/Scout 드래그 조작 MMI 정합 | slider → drag 등 |
| 10 | Overlay·계측 (1.11·1.12) + 3D 좌표 | §6 규칙 |
| 11 | Save Project 데이터 모델 | prj 스키마, Curve 없음 blank, 데모 export/import |
| 12 | Image Filter MPR→Section | CW MPR 구현 참조 또는 스텁 |
| 13 | slice 더블클릭 최대화 (1.9) | |
| 14 | 인계 패키지 | API 문서, 데모, Known gaps, Integration Spec |
| 15 | Slice 스크롤 성능 NFR 수치 | `SectionGen` 벤치마크, 디바운스·캐시 |

구현 초기 1주 내: Section Slice 스크롤 worst-case 측정 → Spec NFR 반영.

---

## 13. 작성·커밋·코딩 규칙

| 항목 | 규칙 |
| --- | --- |
| 사용자 대화·문서 | 한국어 |
| scp-architecture 커밋 메시지 | 한국어 |
| scp-section-poc 코드 주석 | 파일 헤더 Ewoosoft 저작권. export 함수 JSDoc (@param, @returns) |
| 커밋 | 사용자가 요청할 때만. AI 임의 commit/push 금지 |
| 이모지 | 문서·코드 주석 금지 |
| 범위 | 요청·Spec 범위만 수정. CW Viewer 레포 무단 수정 금지 |
| Confluence 붙여넣기 | VKS용 문서는 `**` 마크다운 최소화 (개발실 리뷰 교훈) |
| PoC 명칭 | 타당성 검증 완료 후 구현 단계는 Section 모듈이라 부름 |

### 13.1 파일 헤더 예 (신규 ts/tsx)

```
/*
 * [파일 한 줄 설명]
 *
 * Copyright (c) Ewoosoft Co., Ltd.
 *
 * All rights reserved.
 */
```

---

## 14. 성능·구현 시 주의 (개발실 리뷰 + PoC 교훈)

1. 9장 생성 ~400ms — 스크롤·드래그마다 전량 재생성하면 체감 지연. 디바운스·캐시·이전 프레임 유지 필수.
2. Draw curve 중 Section 이미지는 MMI상 blank 유지, Active line만 실시간 (오버레이 선 재그리기만 — 부하 낮음). **ESC로 모드 종료 없음**. 1점 더블클릭은 curve 종료하지 않음 (§4.2).
3. Thickness 0mm: `slabHalfWidthMm = 0` 경로 검증 필요 (PoC는 3mm half = 6mm 슬랩). 슬랩 루프 `tmm = -half ~ +half` 경계 케이스 확인.
4. WASM: JS가 PoC에서 더 빠름. Section 모듈 기본은 JS. WASM/Worker는 병목·long task 확인 후.
5. Scout 접목: Section 모듈 내부는 2D Scout 유지. CW 통합 시 MPR Axial 교체 — API 경계 Spec에 명시.
6. Overlay normal 허용 오차: Spec 확정 전 임시값은 상수 분리.
7. **bitmapSectionLayout**: 폭·높이 변경 시 반드시 apply 성공 mm와 눈금 동기화 (§7.9.7).
8. **texturesLiveRef**: SectionGrid WebGL 텍스처 갱신 시 레이스 재발 주의 (§7.9.8).
9. **objectFit contain**: Scout 마우스 좌표는 `screenToSliceCoords` 경유만 (§7.9.4).
10. **파노라마 vs Section 슬랩 축**: 혼동 금지. Section=접선 슬랩, Panorama=법선 슬랩 (§7.9.6).
11. **파노라마 재생성**: 곡선/슬라이스/투영 변경 후 버튼 필요. WC/WW만 280ms 디바운스 (§7.9.5).
12. **DICOM Z spacing**: IPP만 믿지 말고 Spacing Between Slices 폴백 유지 (§7.9.3).
13. Section Slice 스크롤 구현 시: 전체 slice 인덱스 캐시·window 이동만으로 9장 부분 재생성 검토.
14. `SectionGen` 콘솔 로그로 mode별 ms 수집 — Spec NFR 근거.

---

## 15. 관련 링크

| 자료 | 링크·경로 |
| --- | --- |
| 본 가이드 | `Cloud Web Viewer v1.3.2/Claude Code 작업 가이드.md` |
| 개발 계획 | `Cloud Web Viewer v1.3.2/Section-Module-개발계획.md` |
| MMI | `Cloud Web Viewer v1.3.2/Confidential_CloudWebViewer_v1.3.2_MMI_Kor/MMI.md` |
| MMI PPT comments (요약) | 본 가이드 §4.2. 원본 `.../MMI_Kor/comments/` (선택) |
| **MMI UI 시각 정본** | `.../MMI_Kor/media/image23.png` (1428×906) — §4.1 |
| MMI media (참고) | `.../MMI_Kor/media/` — image19/27/28 동계열, 나머지 부분 설명용 |
| 개발실 리뷰 (VKS) | https://vks.vatech.com/spaces/ESDEVELOPER/pages/316794587/ |
| PLAN-1287 | `WebSectionView/PLAN-1287.md` |
| PoC OnePager | `WebSectionView/WebSectionView_PoC_OnePager.md` |
| Phase 1 결과 | `WebSectionView/Phase1/Phase1_WebGL_MultiView_결과.md` |
| Phase 2 결과 | `WebSectionView/Phase2/Phase2_CT_Download_결과.md` |
| Phase 3 결과 | `WebSectionView/Phase3/Phase3_ArchCurve_결과.md` |
| Phase 4 결과 | `WebSectionView/Phase4/Phase4_Panorama_결과.md` |
| Phase 5 결과 | `WebSectionView/Phase5/Phase5_SectionView_결과.md` |
| Phase 5 OnePager (VKS) | https://vks.vatech.com/spaces/ESDEVELOPER/pages/305058086/ |
| Phase 4 OnePager (VKS) | https://vks.vatech.com/spaces/ESDEVELOPER/pages/303490289/ |
| PoC 데모 | http://scp-section-demo.test.scp.esclouddev.com/ |
| PoC 레포 | https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc |
| CW Viewer | https://dev.azure.com/ewoosoft/cloudwebviewer/_git/cloudwebviewer |
| abc-dev-assistant | `~/Documents/Git/abc-dev-assistant/AGENTS.md` |
| spec-standard | `abc-dev-assistant/document/spec-standard.md` |
| dev-process-guide | `abc-dev-assistant/document/dev-process-guide.md` |

---

## 16. Claude Code 시작 프롬프트 예시

아래를 Claude Code **첫 메시지**로 붙여넣는다. cwd는 §2.1 참고.

### 16.1 문서·Spec 세션 (cwd = `Cloud Web Viewer v1.3.2/`)

```
Cloud Web Viewer v1.3.2 Section 모듈 — 문서 작업.

cwd: .../WebSectionView/Cloud Web Viewer v1.3.2  (본 폴더)
코드 루트(참조만): ~/Documents/Azure/scp-section-poc

먼저 읽을 파일:
- Claude Code 작업 가이드.md (§2.1 cwd, §4.1 image23, §4.2 comments)
- Section-Module-Spec-v1.3.2-OnePager.md
- Section-Module-개발계획.md
- Confidential_CloudWebViewer_v1.3.2_MMI_Kor/MMI.md
- ../PLAN-1287.md

다음 작업: [여기에 구체 지시]
```

### 16.2 구현·환경 정렬 세션 (cwd = `scp-section-poc/`) — **기본 권장**

```
Cloud Web Viewer v1.3.2 Section 모듈 — 구현 작업.

cwd: ~/Documents/Azure/scp-section-poc
문서 루트: ~/Documents/Azure/scp-architecture/docs/SCP Cloud Server 연구/뷰어 관련 연구/WebSectionView/Cloud Web Viewer v1.3.2
CW 참조: ~/Documents/Azure/cloudwebviewer

먼저 읽을 파일:
- [문서 루트]/Claude Code 작업 가이드.md (§2.1, §7.9 PoC 노하우, §9 환경 정렬)
- [문서 루트]/Section-Module-Spec-v1.3.2-OnePager.md
- [문서 루트]/Section-Module-개발계획.md §9
- [문서 루트]/Confidential_CloudWebViewer_v1.3.2_MMI_Kor/media/image23.png

방법론: es-toolkit /es-* + abc-dev-assistant dev-chain-frontend

현재 단계: scp-section-poc에서 개발. cloudwebviewer 접목·커밋은 scp-section-poc만.
다음 작업: [여기에 구체 지시 — 예: §9 환경 정렬 적용]
```

---

## 17. 변경 이력

| 버전 | 일자 | 변경 |
| --- | --- | --- |
| 1.0 | 2026-07-09 | 초판. Cursor→Claude Code 핸드오프 |
| 1.1 | 2026-07-09 | §7.9 PoC Phase 1~5 상세 노하우 인라인 추가. §14·§15 보강 |
| 1.2 | 2026-07-09 | §4.1 MMI UI 시각 정본 `media/image23.png` 및 media/ 사용 규칙 |
| 1.3 | 2026-07-09 | §4.2 MMI PPT comments. ESC·1점 더블클릭·proj Curve 예외 — §3·§6·§9·§12 반영 |
| 1.4 | 2026-07-09 | §2.1 Claude Code cwd·세션 유지. §16 프롬프트 문서/구현 분리 |
