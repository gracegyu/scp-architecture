# Engineering One Pager

## Project Name

Cloud Web Viewer v1.3.2 — Section Module

## Date

2026-07-13

## Submitter Info

Raymond (전규현) · raymond.jeon@ewoosoft.com 

## Project Description

Clever Space Cloud Web Viewer(CW, 웹 CT 뷰어)에 치열궁 단면 진단용 **Section Layout**(MMI v1.3.2)을 추가한다. 지금은 MPR만 제공해 Section 진단이 필요한 사용자가 데스크톱 제품(Clever One)에 묶여 있으며, 본 프로젝트는 이 단면 진단을 웹에서 제공해 Clever Space 사용자의 웹 전환을 지원한다.

Section 뷰는 **기존 PoC(`scp-section-poc`, WebGL)를 확장해 MMI 전 기능을 구현**하며, Cloud Web Viewer와 환경·인터페이스·툴바·공통 모듈·prj를 정합해 **CW가 그대로 embed**할 수 있게 인계한다. 구현 접근·산출물은 Technical Description §9·§10 참조.

참조: [MMI (요구사항 정본, SharePoint)](https://vatechcorp.sharepoint.com/:p:/s/es/IQCjrxXEJ0pTQYGI9-PSaawwARs_XFxM0DuVBzvOYQBGVu0?e=ztkM8R) · [PLAN-1287 (기획 답변, Jira)](https://vts.vatech.com/browse/PLAN-1287) · [개발실 리뷰 (VKS)](https://vks.vatech.com/x/2_bhEg)

## Business and Marketing Justification

치과 CT의 협설(B/L) 방향 단면은 임플란트·신경관·치근 판독의 핵심이다. 현재 Cloud Web Viewer는 MPR만 제공해, Section 진단이 필요한 사용자는 데스크톱(Ez3D-i·Clever One)에 묶여 있다. v1.3.2에서 Section Layout을 제공하면 웹 전환 장벽을 낮추고 Clever Space CT 뷰어의 진단 완결성을 높인다. MMI·PLAN-1287 확정 범위 내 구현으로 출시 일정에 맞춘다.

성공 지표: (a) 워크플로 = Section 진단 시 데스크톱 병행 없이 웹에서 완결, (b) 기술 수용 기준 = §8 NFR(9단면·Slice 스크롤 프레임 예산)·DoD 충족. 비즈니스 정량 KPI는 제품팀 별도 요구 없음(N/A, §12-D9).

## Risk Assessment

| 리스크 | 심각도 | 대응 |
|--------|:---:|------|
| **Section Slice 스크롤 성능** — 9단면 생성 JS 평균 393ms(§8), 30 FPS(33ms) 미달 | 높음 | 구현 초기 벤치마크 → 디바운스·캐시·표시 분리 정책을 NFR로 확정(§8·§12-D7) |
| **접목 정합 이탈** — poc가 CW 환경·인터페이스·툴바와 어긋나면 embed 비용 증가 | 중 | 구현 착수 전 환경 정렬 게이트(§9.3), 인터페이스·store·prj 정합(§9.4~9.6) |
| **B/L 규칙 구현 오차** | 낮음 | 기획 확정 단일 규칙(§5, P1·P2·C). 폴백 = 수동 L/B Switching |
| **Arrow 툴이 CW `InteractionType`에 없음**(MMI 1.12) | 중 | §9.6 — CW 패턴으로 신규 타입 추가, 접목 시 core 반영 |
| **Save prj 호환** — CW prj XML과 구조 불일치 시 복원 실패 | 중 | §7 — CW prj의 Curve/Section/Pano 필드(§9.5)에 매핑, 개발 중엔 동일 payload를 브라우저 임시 저장으로 검증 |
| Overlay Normal 허용 오차 미정의 | 낮음 | §4 — 초기값 5° 상수 분리, 실사용 튜닝 후 고정 |

## Resource and Scheduling Details

**담당(역할):** Section 모듈(poc 확장·명세) = Raymond(1명). 접목(CW embed·prj I/O·라우팅) = CW Viewer 팀. B/L·기획 항목 = 기획.

**일정:** 목표 **1주**, 예상 **2주**(§12-D9). 아래는 작업 분해·마일스톤.

| # | 작업 항목 | 산출 | 마일스톤 |
|---|-----------|------|:--------:|
| 1 | Spec 리뷰 (기획+CW팀) | §9 접목 정합·§12 결정 합의 | M1 Spec 승인 |
| 2 | 환경 정렬(§9.3) | 버전·MUI·zustand 정합, CW `Toolbar` 렌더 | M2 환경 게이트 |
| 3 | poc 확장 구현(§3~§7) | MMI 1.2~1.13·Draw curve(§6)·B/L(§5)·Overlay(§4) | M3 기능 완성 |
| 4 | 성능 벤치마크(§8) | Section Slice 스크롤 worst-case → NFR 수치 | M4 NFR 확정 |
| 5 | 인계(§10) | 패키지·공개 API·데모·embed 매핑(§9.7)·Known gaps | M5 인계 |

---

# Technical Description

> 본 절은 MMI 정합 요구(§3)와 CloudWebViewer 접목 정합(§9)을 다룬다. 구현 가능 수준으로 기술하되, 내부 클래스·모듈 세부(LLD)는 dev-chain-design / 구현 단계로 남긴다.
>
> **API(Swagger) / ERD(PostgreSQL): N/A** — 본 모듈은 REST API·관계형 DB가 없는 클라이언트 뷰어다. 인터페이스 계약은 타입·패키지 API(§9.4·§10), 영속 데이터는 CW prj XML 스키마(§7·§9.5)로 대체한다.

## 1. 범위 (Section 모듈)

Section 레이아웃 화면은 **(1) Toolbar · (2) MPR/Section 선택 · (3) Section 뷰** 3층이다(§2). Section 모듈은 **(3) Section 뷰를 `scp-section-poc`(WebGL)를 확장해 MMI 전 기능으로 직접 구현**하고, (1)(2)는 CW와 동일 look&feel·동일 이벤트로 정합한다. **CW의 vtk 파이프라인은 사용·수정하지 않는다(§9.1, §12-D1).**

| 포함 (Section 모듈) | 제외 (CW Viewer 팀 — 접목/제품) |
|------|------|
| **(3) Section 뷰(WebGL)** — image23 3영역, MMI 1.1~1.13 전 기능(±45° 회전 제외), Overlay 규칙(1.13 §6), B/L(§5)·Draw curve(§6) | CW 셸(LNB·Back·환자 목록), MPR↔Section 라우팅·권한 |
| (1) Toolbar 재사용·이벤트 연동(§9.6), (2) MPR/Section 선택(데모 stub) | 실제 prj 파일 I/O·자동저장·Desktop→Web 최초 업로드 |
| Save 저장 항목·CW prj 스키마 호환 직렬화(§7) + 개발용 브라우저 임시 저장 | Scout = MPR Axial 컴포넌트 결합(모듈은 2D Scout 유지) |
| 공개 API·데모·성능 NFR·벤치마크(§8), CW embed 매핑(§9.7) | CW `Layout3DPAN` 등 vtk Section 뷰(본 모듈 미사용) |

## 2. 화면 3분할 — Toolbar · MPR/Section 선택 · Section 뷰

MMI `Slide7.jpg`·EzCloud CT 화면(`CloudWebViewerData/2.png`) 기준. Clever Space 좌측 LNB·우측 썸네일은 범위 밖(접목).

```
+----------------------------------------------------------+
| (1) Toolbar                                              |
|  Pan Zoom Pointer | Length Angle FreeDraw Arrow | Grid Overlay | Reset… | Setting |
+----------------------------------------------------------+
| (2) 환자·스터디 정보 …                    [MPR] [Section] |
+----------------------------------------------------------+
| (3) Section 뷰 (Section 선택 시)                          |
|   +--------------+-----------------------------+          |
|   | Scout        |                             |          |
|   | (Axial+Curve)|   Section 3×3 grid (9 slice)|          |
|   +--------------+                             |          |
|   | Panorama     |                             |          |
|   +--------------+-----------------------------+          |
+----------------------------------------------------------+
```

3영역 배치(CSS Grid): `columns 1fr 2fr` / `rows 2fr 1fr`, areas `"scout section" / "panorama section"`. 기본 폭 30mm·경계 100mm 등 치수는 §3.

Section 뷰(3)의 데모·제품 렌더는 모두 **Section 모듈의 WebGL 구현**이다. MPR 선택 시 (3)은 CW MPR 2×2(접목), Section 선택 시 image23 Section Layout.

## 3. MMI 기능 요구사항 매핑 (1.1~1.14)

MMI 정본(SharePoint PPT) Epic 1 Section Layout 전 항목. "MPR과 동일"로 규정된 동작은 CW MPR 구현과 정합(§9). 상태: 확정 / 스펙아웃 / 미확정.

### 3.1 마스터 매핑

| MMI | 기능 | 요구 상세 (MMI 정본) | 현재(poc) | Section 모듈 작업 | 상태 |
|-----|------|----------------------|-----------|-------------------|------|
| **1.1** | Layout 전환 | 기본 MPR. `[MPR]`·`[Section]` 토글, 활성 layout 표시 | 데모 탭만 | (2) 선택 UI + layout state. 라우팅은 접목 | 확정 |
| **1.2** | 구성·정보 표시 | 3영역. 오버레이: Patient(좌상), W/L·Filter(우상), 상단 방향표기 = **R/L(Scout 고정) / Pano는 Curve 시작·끝점 각도로 R/L·L/R·P/A·A/P 동적(§5.1) / B/L(Section, Scout Section line 방향과 동일)**, thickness·interval·total slice(우하), ruler(우중앙). Slider(Scout H/F·**Pano B/L**(구 P/A, §12-D15)·Section R/L). Scout Axial은 **MPR Axial과 뷰 비연동**(단 Th/INT는 MPR 서브모듈과 동기, 1.10). Image Adjust/Setting/**최대화(3뷰 공통, 최대화 시 그 뷰만 전체·타이틀 유지)** = MPR 동일 | 대부분 보유 | 오버레이·라벨·slider image23 정합. **Section ruler = 가로·세로 전체 축**(PoC는 영상 폭). **최대화 버튼은 최대화 시 복원(최소화) 아이콘으로 토글**(CW `ContentTitleBar` `maximized`·`TitleMaximizeIcon`/`TitleNormalizeIcon` 정합, §9.5) | 확정(ruler 갭) |
| **1.3** | Scout Curve 요소 | Curve, Section line(전체 slice·빨강 수직), Active section line(9개, 폭=Section 가로폭 기본 **30mm**), Center section line(5번째·노랑·control point), Panorama navigator line(초록), Panorama thickness line(초록 한 쌍·control point), L/B 표시(흰 text), **BL/LB 기준점**(첫 point·연두 삼각형) | 곡선·line·라벨 보유 | line 요소 명확화, **BL/LB 기준점 신규**, B/L 자동(§5) | 확정 |
| **1.4** | Panorama Line 요소 | 경계선(노랑, 기본 거리 **100mm**), 중심선(초록), Scout 위치선(흰 점선, 기본=중심선), Active section line(중 Center 다른 색) | 부분 | 경계선 100mm, 각 line 오버레이 | 확정 |
| **1.5** | Draw Curve | 좌클릭=추가, 우클릭=직전 취소(1점이면 불가), 더블클릭=종료. 미리보기 실시간. **Section·Panorama는 curve 완료 후 표시(완료 전 blank)**. §6 상세 | 부분(점마다 생성) | ESC 미적용·1점 더블클릭 무시·완료 후 1회·Active line 실시간(§6) | 확정 |
| **1.6** | Edit Curve | curve 이동, point 이동(drop 시 갱신)·삭제·추가(context menu, 최소 2점), Curve 삭제(확인 box), **L/B Switching**(text만 반전, 영상 flip 없음), **BL/LB 기준점 이동**(section line 따라 한 칸) | 편집 보유, 기준점 없음 | context menu, 기준점 drag, 확인 다이얼로그 | 확정 |
| **1.7** | Scout 조작 | Active line 이동·**길이 조절**(Center line control point 대칭 드래그 — PoC는 slider), Panorama thickness 조절(대칭, **combo와 동일 30mm cap** — §12-D8), Scout slice 변경(휠·slider → Pano 위치선), 삭제·L/B Switching·기준점(편집 모드 동일) | slider 기반 | 드래그 핸들, thickness line 드래그(30mm clamp) | 확정 |
| **1.8** | Panorama 조작 | 경계선 이동(세로폭, 대칭), 중심선 이동(drop 시 3뷰 갱신·Scout 위치선 동기), Active line 이동, **B/L slice 변경(구 P/A, §12-D15) = 재슬라이스를 곡선 법선방향으로 offset 스윕**(휠·slider → Scout **navigator line** 이동, §3.3). **±45° 회전 스펙아웃** | 위치 이동 보유 | 경계선·중심선·active line 드래그, **B/L offset 스윕 신규**(§3.3, IP T-P3-5). 회전 제외 | 확정 / ±45° 스펙아웃 |
| **1.9** | Section 조작 | **Slice 변경**(휠·slider → 9장·slice number·Scout/Pano Active line 동기), Center slice(5번째 강조), 최대화(3×3 유지·타이틀 유지, ⛶↔복원 토글), **개별 slice 더블클릭 최대화(더블클릭으로 복원)** | 중심 9장만 | **전체 slice 인덱싱·스크롤·페이징 신규**(§8 성능 핵심), slice number, 더블클릭 최대화/복원 | 확정(핵심 신규) |
| **1.10** | Thickness/Interval | 각 뷰 Title Bar **Setting** 다이얼로그에서 조절, MPR 동일. **Thickness combo 옵션 = {0, 0.1, 0.5, 1, 2, 3, 5, 10, 20, 30}mm**(drag로 off-list 값 시 combo 미선택·필드에 원값 표시, MMI 1.7-3b). 기본 Th **0mm** = **전 뷰(Scout·Pano·Section 모두 slab 두께 보유** — Active line 가로폭·경계선 세로폭 extent와 **별개**). INT: Scout=**Voxel Based Interval**(MPR 동기)·Pano/Section=1mm. 변경 시 오버레이·total slice·slider·line 간격 갱신, **Section INT 변경 시 Active line 재중심**. Draw 중 Scout Th/INT 조정 시 curve 취소 없음(즉시 적용) | INT 보유, Th UI 없음·기본 full 6mm(=half 3mm) | **Th 기본 0mm**, Setting combo(옵션값), **Section slab 두께 명시·뷰별 독립**(Scout·Pano·Section 각자), combo·drag 공통 상한 30mm(§12-D8·§9.5). **Setting 다이얼로그 상세 §3.5**, 생성 모델 §3.3. **Scout Th/INT의 MPR 레이아웃 동기는 standalone 미구현(§12-D18, D1)** | 확정(MPR 동기 통합 시) |
| **1.11** | Windowing/Filter | Image Adjust: W/L + Smooth/Sharpen/Max Sharpen/Inverse/MIP + Revert. 전 단면 일괄, 좌상단 text. **CW `ImageAdjustDialog` 이식(필터 알고리즘 포함) — 상세 §3.6** | Windowing만 | CW 다이얼로그·필터 커널 이식(§3.6), 뷰 간 동기. **MPR 레이아웃 연동(1.11-b)은 standalone 미구현(§12-D18)** | 확정(MPR 연동 통합 시) |
| **1.12** | 공통 툴 신규 | Angle을 Length 우측 이동. Free Draw 2D 단면 확대(3D 제외). **Arrow 신규**(1클릭 시작·2클릭 화살표 끝, View/slice 단위) | 없음 | 배치, **Arrow 신규**(CW `InteractionType` 미포함 §9.6) | 확정(Arrow 신규) |
| **1.13** | Section 공통 툴 | Pan/Zoom/Reset/Pointer, Length/Angle/Free Draw/Arrow(**각 section별·경계 넘나들 불가**), Grid·Overlay, Reset Cloud Work·Initialize All, Single/Dual·View Original, Image Adjust·Setting·최대화. 모두 MPR 동일. **Overlay 규칙 §4** | 최소 | Toolbar 재사용(§9.6), section 스코프, Overlay(§4) | 확정 |
| **1.14** | Save Project | MPR 동일 prj 저장. §7 항목. 재오픈 시 레이아웃·Curve 복원. proj Curve 없으면 blank | 없음 | 저장 항목·CW prj 스키마 호환 직렬화(§7·§9.5) + 개발용 임시 저장 | 데이터 모델 확정 / prj I/O 접목 |

### 3.2 모드별 동작 지원 (MMI Appendix — 구현 정본)

Draw/Edit 모드에서 Panorama·Section 입력 영역(title 제외)은 disabled 커서.

| 툴/기능 | 일반 | Draw Curve | Edit Curve |
|---|:--:|:--:|:--:|
| Pan/Zoom/Reset/Pointer, Length/Angle, Free Draw/Arrow | ● | ✕ | ✕ |
| Show/Hide Grid·Overlay | ● | ● | ● |
| Show/Hide Patient Information | ✕(MPR 동일) | ✕ | ✕ |
| Reset Cloud Work / Initialize All | ● | ✕ | ✕ |
| View Original | ● | ✕(disabled) | ✕(disabled) |
| Single/Dual Layout | ● | ● | ● |
| Scout Image Adjust·Setting·Slice 이동 | ● | ● | ● |
| Scout Active line·thickness line·기준점 이동 | ● | ✕(클릭=point) | ● |
| Scout Curve point 생성/이동/삭제 | ✕ | △(생성만) | ● |
| Scout Curve 조정(전체 이동/삭제) | △(삭제만) | ✕(클릭=point) | ● |
| Scout L/B Switching | ● | ✕(우클릭=직전 취소) | ● |
| Panorama/Section Image Adjust·Setting | ● | ✕(disabled) | ● |
| Panorama 경계선·중심선·Active line 이동 | ● | ✕(blank) | ● |
| Panorama/Section Slice 이동(휠·slider) | ● | ✕(disabled) | ● |

> Edit 모드는 입력 영역 커서가 disabled여도 Panorama·Section의 **휠·slider slice 이동은 가능**(MMI 1.6-10). Draw 모드에서는 slice 이동도 disabled.

### 3.3 파노라마·단면 생성 모델 (2026-07-13 재분석 정정 — 기획 확인)

**정정 배경:** MMI 전면 재검토 + 기획 확인 결과, PoC의 "치열궁 곡선에 두꺼운 slab을 MIP(최댓값)로 투영해 **고정** 파노라마 생성" 모델은 MMI와 다르다. Ez3D-i·CleverOne·MMI 모두 아래 모델이며, 이전 MMI 분석에서 이 생성/네비 모델을 놓쳤다.

- **파노라마 = 곡선을 따라가는 가느다란(기본 Thickness 0mm = 1 voxel) 재슬라이스.** 두꺼운 MIP가 기본이 아니다.
- **B/L 슬라이더(구 P/A, §12-D15)로 재슬라이스 위치를 곡선의 법선방향으로 offset 스윕**(L 설측↔B 협측). 이 위치를 Scout에 **Panorama navigator line**(곡선을 offset한 초록선, 기본 = 곡선 위)로 표시한다(MMI 1.3-5·1.8-5). 파노라마는 곡선 고정이 아니라 **이동식 offset 재슬라이스**다. (법선=B/L 축이라 arch가 아닌 curve에서도 성립 — 그래서 P/A→B/L로 명칭 확정.)
- **Thickness > 0일 때만 slab**이 되며, 투영 방식 **기본 = 평균(mean)** — 기획 확정(§12-D12, 2026-07-14). **최댓값(MIP)은 Image Adjust 필터 토글**로만(§3.6). 엔진은 둘 다 파라미터로 지원(기본 preset `mean`).
- **슬랩 두께 샘플링 알고리즘(§12-D16, 개발실 정의 — CW 소스 분석 근거).** 슬랩은 XY 평면 내 방향(파노라마=곡선 법선, 단면=곡선 접선)으로 두께를 갖는다. **공식(구현 가능 수준):**
  1. **샘플 스텝** `stepMm = slabSampleStepMm > 0 ? slabSampleStepMm : max(1e-3, min(spacing[0], spacing[1]))` — 명시값 없으면 **in-plane 최소 voxel spacing**에 자동 연동(스텝을 지정하지 않은 게 기본; 슬랩이 XY 평면이라 Z spacing 불필요).
  2. **반쪽 샘플 수** `nHalf = max(0, round((thickness/2) / stepMm))`.
  3. **샘플 offset(mm)** `tmm = k · stepMm`, `k = −nHalf … +nHalf` → 총 `2·nHalf+1`개, **중앙 대칭·최소 1개**.
  4. 각 offset 위치(`pos + tmm·n̂`)에서 **trilinear 보간**으로 HU 추출 → 리스트를 `mean`(기본)/`mip`(토글, §3.6)로 축약.
  - **sub-voxel 처리:** voxel(보통 0.2~0.4mm)보다 얇은 두께(0mm·0.1mm 등)는 `round((thickness/2)/step)=0` → `nHalf=0` → **단일 중앙 샘플 1장**(0mm와 동일, 평균/MIP 무의미). **평균/MIP는 `nHalf≥1`(≈두께 ≥ 1 voxel)일 때만 실효.**
  - CW MPR 의도 공식 `max(1, round(thickness/voxelSpacing))`과 동치. ⚠ **CW 현행 MPR은 reslice Z=1 하드코딩으로 두께 미반영(stripped/미완성)** — 우리 엔진은 위 공식으로 정상 구현.
- **Section 단면도 동일**하게 slab 두께(0~30mm, §1.10)를 가지며 투영 방식은 파노라마와 같은 규칙(D12)을 따른다.
- **엔진 영향(재작성 불필요):** `scp-section-core`의 slab 코드는 이미 두께·투영을 파라미터화한다. 필요한 변경은 (1) 기본 Thickness 0(thin), (2) 파노라마 재슬라이스를 **navigator offset 위치**에서 생성(B/L 법선 스윕 신규, 구 P/A), (3) **기본 투영 = 평균(mean)**(D12 확정), MIP는 Image Adjust 토글. → IP T-P3-4·T-P3-5·T-P4-1.

### 3.4 MMI 미명시 — 개발실 정의 값 (파라미터)

MMI가 **값·범위·동작 방식·표기 의미를 명확히 규정하지 않은** UI 항목을 개발실이 확정한 값. (기본값만 주고 범위 미정, 또는 요소 명칭만 주고 의미/간격/렌더 방식 미정 등 모두 포함.) MMI 갱신 또는 기획 회신 시 갱신한다. (기준: 2026-07-14 개발실)

| 항목 | 개발실 확정 값 | MMI 명시 | 비고 |
|------|--------------|----------|------|
| **Section 가로폭**(Active section line 길이 = Buccolingual 폭) | 기본 **30mm**, 범위 **20~80mm** (control point 대칭 드래그·slider) | 기본 30mm만(1.3-3a), **범위 미명시** | 드래그/슬라이더 공통 clamp. `sectionWidthFromHandleMm(_, 20, 80)` |
| **Section 세로폭**(Z 구간, 경계선 간격) | 기본 **60mm**(`DEFAULT_SECTION_HEIGHT_MM`) | Pano 경계선 기본 100mm(1.4-1)와 별개, Section Z 기본 미명시 | 경계선 대칭 드래그로 조절(T-P3-2) |
| **Panorama navigator line 가시성·기본 위치**(MMI 1.3-5) | **커브가 존재하는 모든 모드에서 상시 표시**(단선·초록). 기본 위치 = **커브와 겹침(offset 0)**, B/L 슬라이더(구 P/A)로만 이동(Scout에선 조작 불가·읽기전용, MMI 1.7-4①·1.8-5①) | 1.3-5① "Default=curve와 동일"·1.8-5(slider 이동)만. **가시 토글·offset 범위(스윕 폭) 미명시** | offset 0 기본이라 커브와 겹쳐 별도로 안 보이며, 슬라이더 이동 시에만 분리 표시. **B/L 스윕 mm 범위 미확정** → T-P3-5에서 개발실 잠정값 지정 후 여기 기록 |
| **Panorama thickness line 가시성**(MMI 1.3-6) | **커브가 존재하는 모든 모드에서 상시 표시**(초록 한 쌍+control point). thickness=0이면 한 쌍이 커브에 겹쳐 사실상 안 보임. **조절(드래그)은 일반·Edit 모드만**(Draw 모드는 클릭=point 입력, Appendix 모드표) | 1.3-6(정의)·1.7-3(대칭 드래그)만. **별도 가시 토글 없음**(= 상시) | control point는 커브 시작점(s=0)·끝점(s=totalMm) 각 ±thickness/2에 표시(총 4개) |
| **Scout 커브 눈금·숫자의 의미·간격**(MMI 1.3 Section line) | **slice 번호 기준**: 짧은 tick=매 slice(호장 s=m·interval), **major(밝은 빨강+흰 숫자)=매 `20`번째 slice(`m % 20 === 0`), 숫자=slice 번호 `m`**. 총 호장 길이(mm)는 커브 끝 별도 라벨(별개) | MMI 1.3은 요소 **명칭만** 규정, 커브 위 **숫자/눈금의 의미(mm? slice?)·라벨 간격(몇 배수?)** 미명시(image26은 도식·간격만 암시) | **근거:** MMI image19 실데이터의 Section 타일이 slice 번호(109·110…)·"Total Slice 635"로 인덱싱 → 커브 숫자도 동일 slice 번호여야 correlation. **major 간격 20 slice**는 image26이 20 배수로 보여 개발실이 채택(미명시). interval 변경 시 총 slice 수 따라 갱신 |
| **Section 타일 이미지 fit 방식**(MMI 1.9) | **contain**(단면 W×H 전체가 보이게 종횡비 유지·letterbox) | MMI는 "꽉차게/여백" 명시 없음(image19는 거의 정사각 타일) | cover(꽉참)는 H>W 시 세로 crop되어 파노라마 H 조절이 안 보이는 문제 → contain 채택. 종횡비가 타일과 다르면 좌우 여백 불가피(§변경이력 1.13) |
| **Panorama 이미지 fit 방식**(MMI 1.4) | **contain**(물리 W×H 비율 유지·letterbox; arch 길면 상하 여백, 짧으면 좌우 여백) | MMI 미명시 | Section 타일과 동일 규칙. **비트맵을 물리 정사각 픽셀로 생성**(행 Z도 columnSpacing mm 간격)해 픽셀 비율=물리 비율 → 왜곡 없음(§변경이력 1.17) |
| **Scout R/L 방향 유도**(2026-07-15 확정) | **표준 axial 방향 가정**(화면 좌=R·우=L, 방사선 관례). DICOM `(0020,0037)`·`(0018,5100)` 방향 태그 **미독해** — 표준 방향으로 처리. **CloudWebViewer도 방향 태그를 읽지 않고 표준 처리**(§12-D19). | DICOM `(0020,0037)`·`(0020,0032)`·`(0018,5100)`에 실제 방향(LPS) 인코딩 — 이론상 유도 가능하나 미사용 | **확정: 표준 방향 처리(§12-D19).** Vatech dental CBCT는 표준 방향 저장이라 정상. 비표준 방향 데이터는 **범위 밖**. 향후 필요 시 방향 태그 유도로 견고화 가능(개선 여지로만 기록). |

> Thickness 범위(0~30mm)·combo 옵션은 MMI(Slide20)·CW `SLICE_THICKNESSES` 근거가 있어 여기 포함하지 않음(§1.10·§12-D8).

> **참고(2026-07-14):** 초기에 ScoutView가 그리던 **고정 offset 초록 한 쌍**(`COLOR_GUIDE` placeholder)은 MMI 1.3에 없는 요소라 **제거**했다. 이제 Scout의 초록 offset 한 쌍은 **thickness line(6번)으로 일원화** — 두께>0일 때만 ±(th/2)로 벌어져 보이고, 시작·끝점 각 ±half에 control point 4개가 **빨간 tick/Active line 위(맨 위 레이어)** 에 표시된다(image26). 두께=0이면 곡선 위로 collapse(네모는 시작·끝점에 위치, 드래그로 확장). (5) navigator(단선)는 아직 미구현 — **T-P3-5**.

#### 3.4.1 오버레이 색상 (RGB) — 임시, GUI styleguide 확정 전

**기획팀 회신(2026-07-14):** *"UI는 추후 VT UI/UX팀이 GUI styleguide를 제작해 전달 예정. MMI의 색상이 최종 반영 색이 아니므로 임의 색상 지정 무관. styleguide 일정은 미확정."* → 아래 색은 **개발실 임시 지정**이며 styleguide 전달 시 교체한다. Scout 오버레이 색은 `ScoutView.tsx` 상단 `COLOR_*` 상수로 일원화.

| 요소 | RGB | 상수 |
|------|-----|------|
| Curve 선(악궁 커브) | `#FFD21E` (**노랑** — MMI 1.3 정본; 타 슬라이드는 연두이나 1.3 우선) | `COLOR_CURVE` |
| Curve 제어점 네모(내가 찍은 점) | `#30B138` | `COLOR_CTRL_POINT` |
| BL/LB 시작점 삼각형 · "BL/LB" 글자 | `#30B138` | `COLOR_CTRL_POINT` |
| B/L 폭 핸들(Center line control point) 테두리 | `#20EE31` | `COLOR_HANDLE_BORDER` |
| ~~커브 바깥 가이드선~~ | — (제거됨, 2026-07-14 — MMI 1.3 미존재 placeholder) | ~~`COLOR_GUIDE`~~ |
| Panorama thickness line(초록 한 쌍+control point 4개) | `rgba(45,205,130,·)` (초록) | (리터럴) |
| Center section line(중앙, 노랑) | `#FFE046` | `COLOR_SEC_CENTER` |
| Section line 일반(minor tick·Active line) | `#683838` | `COLOR_SEC_MINOR` |
| Section line **20 배수 slice**(major tick·Active line) | `#DB696B` | `COLOR_SEC_MAJOR` |
| B/L 텍스트(**curve 양 끝점** 좌우, MMI 1.3-7c) · **slice 번호(20 배수 slice)** | `#FFFFFF` | — |
| 호장 길이 라벨(끝점 `<총길이> mm`, 접선 바깥; 시작점 `0.00 mm`는 제거) | `#20EE31` (초록) | `COLOR_ARC_LABEL` |
| Panorama 두께값 라벨(시작 thickness 선 L쪽 `<두께> mm`) | `rgb(45,205,130)` (초록) | (리터럴) |

> **Scout 커브 눈금·숫자 = slice 번호 기준(호장 mm 아님, 2026-07-14 정정).** 짧은 tick = 매 slice(호장 s=m·interval), **major(밝은 빨강+흰 숫자) = 매 20번째 slice(`m % 20 === 0`), 숫자 = slice 번호 `m`**. MMI Section 타일 slice 번호(109·110…·Total Slice 635)와 동일 인덱싱 → 커브 위치↔타일 번호 correlation. **interval 변경 시 총 slice 수가 달라져 major 위치·개수가 갱신**된다. 총 호장 길이(mm)는 커브 끝의 별도 라벨. Section line 색 규칙(중앙=노랑 / 20배수 slice=`#DB696B` / 그 외=`#683838`)은 짧은 tick·9 Active line에 동일 적용, 9 window slice 위치엔 짧은 tick 생략(겹침 방지). 숫자는 L(안쪽)·흰색·접선 평행.

#### 3.4.1a CW UI 크롬 색·치수 통일 (2026-07-15, CW 소스 대조 확정)

Section 모듈 셸(툴바·뷰 헤더·뷰 배경·아이콘)을 **CloudWebViewer와 시각 통일**. 사용자가 구동 화면에서 측정한 값을 **CW 소스코드(`cloudwebviewer`)에서 직접 대조** → 일부 항목이 측정값과 불일치(스포이드 오차 추정)하여 **소스 정본값을 채택**(Jessi 확정 2026-07-15). 오버레이 색(§3.4.1)과 별개의 **크롬(frame) 팔레트**이며, 이 역시 GUI styleguide 전달 시 교체 대상.

| 요소 | 정본값(적용) | 측정값(참고) | 위치(CW 소스) |
|------|-----|-----|------|
| Top Toolbar 배경 · 높이 | `#141414` · ~**60px** | 동일 | `toolbar/component/Toolbar.tsx`(btn36+pad12×2 파생) |
| 각 뷰 상단 헤더 배경 · 높이 | `#333333` · **32px** | `#2D2D2D`·34 | `lib/react-vtkjs …/color.ts` `getViewFrameNormalColor`, `const.ts` THICKNESS 32 |
| 각 뷰 배경 | `#000000` | 동일 | `ViewFrame.tsx`(`black`) |
| 아이콘 기본색 | `#FFFFFF` | 동일 | `ToolBtn.tsx`(`white`) |
| 아이콘 hover(비활성) · active | `#00BEA5` (teal) | `#16B69C` | `ToolBtn.tsx`, theme `primary.dark` |
| 아이콘 active + hover | `#61F2DF` (밝은 teal) | `#5BF0DB` | `ToolBtn.tsx`(`:hover`) |
| 아이콘 비활성(disabled) | **white @ opacity 0.3** | `#5B5B5B` | theme `MuiIconButton.disabled` |
| active 토글(데모 MPR/Section) 배경 | `#00BEA5` | `#16B69C` | `App.tsx` `activeToggleStyle` |

> **MPR/Section 전환 바**: CW엔 별도 전환 바가 없고 툴바 내 single/dual 버튼으로 처리. 데모에는 전환 UX용으로만 존재(BG `#3B3B3B`·h34, `App.tsx` `selectBarStyle`) — **접목 시 제거/대체**(Jessi 확정 2026-07-15).
> **아이콘 hover는 배경이 아닌 fill(글자색) 변경**으로 표현(CW 아이콘 SVG가 `fill` prop 사용). 기존 `rgba(0,190,165,0.4)` 배경 hover는 제거. **CustomMPRSlider류 슬라이더**의 teal(`#00B1A2`/`rgb(0,177,162)`)은 크롬 아이콘 팔레트와 구분해 **그대로 유지**.

#### 3.4.2 MMI 미명확 동작·상호작용 — 개발실 해석/처리 (§4.3)

MMI가 **동작·상호작용을 명확히 규정하지 않거나 문구가 모호한** 경우의 처리 원칙과 확정 사례. (값·범위는 §3.4, 색은 §3.4.1.)

**처리 원칙(우선순위):**
1. **MMI 본문 vs PPT comment 상충 → comment(최신) 우선**(§6). MMI 이미지(실데이터)로 교차검증.
2. MMI 미명확 시 **CW 소스·관례·타 조항으로 유추** → 근거와 함께 개발실 확정, 여기/§12에 기록.
3. 임상/UX 판단이 필요하면 **기획(Jessi) 문의 → §12 Decision Log** 등재 후 확정.

**확정 사례:**
| 항목 | MMI 모호점 | 개발실 해석/처리 |
|------|-----------|-----------------|
| **Add Point(컨텍스트 메뉴)** | 1.6-①"전후 order 사이 순번"이 애매 | **두 점 사이 삽입(insert)** 확정 — 클릭 위치를 최근접 세그먼트에 끼워넣음. **끝에 추가는 좌클릭**(별개). Add Point는 **커브 위/근처 우클릭에서만** 제공(먼 빈 공간의 중간 삽입 혼란 방지) (§6) |
| **컨텍스트 메뉴 발견성** | "커브 위" 한정이라 얇은 선 우클릭이 어려움 | 우클릭이 커브서 벗어나도 **메뉴는 표시**(L/B·Delete Curve), 단 Add Point만 커브 근처 제한. 항목은 MMI 유지(§6) |
| **Edit 점 추가 버튼** | 좌/우클릭 역할 불명확 | **좌클릭만** 추가/이동/선택, **우클릭=컨텍스트 메뉴 전용**(Draw 모드와 동일, §6) |
| **Edit 제어점 hover 커서** | 미규정 | **모든 제어점** 위 hover 시 이동(`move`) 커서(시작/끝뿐 아니라 전체) |
| **Edit 모드 시각 어포던스** | 미규정 | Edit 모드 상호작용은 **제어점·BL/LB 삼각형뿐**(width/thickness 핸들은 Edit에서 비활성)이므로, **제어점·삼각형만 밝게** 두고 **나머지(커브·section tick·9 active line·navigator·thickness·라벨)는 dim(opacity ≈0.28)** 처리해 "점 편집 중" 상태를 명확히. **임시 dev 스타일**(GUI styleguide 확정 시 교체, §3.4.1). 개발실 제안(2026-07-15) |
| **Scout 커브 숫자 의미** | mm vs slice 불명확 | **slice 번호**(§3.4·§3.4.1 주석) |
| **R/L 방향 유도** | 방향 태그 사용 여부 불명확 | **표준 axial 가정, 방향 태그 미독해**(CW 동일, §3.4·§12-D19) |
| **fit 방식(Section/Panorama)** | "꽉차게/여백" 미명시 | **contain**(§3.4) |
| **W/L·Filter 적용 범위** | "모든 단면"에 Scout 포함 여부 | **전 뷰 공유(Scout 포함)**(§12-D17) |

### 3.5 Setting 다이얼로그 (Thickness / Interval) — CW `CTSliceSettingDialog` 이식

각 뷰 Title Bar의 **Setting(기어) 아이콘** 클릭 → **Popover**(기어에 anchor, 폭 **184px**, 반투명 blur 배경, chromeless, **OK/Cancel 없이 선택 즉시 반영**, 바깥 클릭 시 닫힘). CW 원본: `packages/core/.../ctContent/CTSliceSettingDialog.tsx`.

**컨트롤 2개(둘 다 combo `Select`):**
| 항목 | 옵션 | 기본 | 매핑 |
|------|------|------|------|
| **Thickness (mm)** | `[0, 0.1, 0.5, 1, 2, 3, 5, 10, 20, 30]` (CW `SLICE_THICKNESSES`) | **0** | slab 두께(full mm) → `slabHalfWidthMm = thickness/2`. 0=thin(1 voxel). **뷰별 독립**(Scout·Pano·Section 각자 상태) |
| **Interval (mm)** | `['Voxel Based Interval', 0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 3, 5, 10]` (CW `getSliceIntervals`) | **'Voxel Based Interval'** | slice 간격(mm). **'Voxel Based Interval' → 0 → 볼륨 최소 voxel spacing 사용**(`useVoxelInterval=true`), 그 외 = 해당 mm |

- 스키마: CW `IMPRViewSetting { defaultThickness, defaultInterval, defaultZoom }`(types/core `MPRViewThicknessType`·`MPRViewIntervalType`). Section 모듈은 이 값 형태를 재사용.
- **combo이며 슬라이더/연속범위 아님**(원본 확정). "0.1~10"은 discrete 옵션 범위를 의미.
- Scout Setting 버튼은 **기존 PoC 슬라이더 박스를 이 다이얼로그로 교체**(T-P3-4).

> **구현 현황(2026-07-14, T-P3-4 부분 완료)**: `components/src/SettingDialog.tsx` 신설, Scout/Panorama/Section 3뷰 기어에 배선. Thickness는 뷰별 독립(`panoramaThicknessMm`/`sectionThicknessMm`/`scoutThicknessMm`). **잔여/편차**: (a) **Interval은 현재 3뷰가 단일 `curveEditor.sectionInterval`을 공유(버그)** — MMI 1.10-3①은 뷰별 독립(Scout=Z축 스크롤·Section=호 방향·Panorama=P/A 스텝, 각 의미 상이). **정정 대상 = §12-D15(기획 확인 완료 2026-07-14: 3뷰 독립·Panorama=법선 offset 스텝·슬라이더 B/L), IP T-P3-6.** (b) **Scout thickness는 구현됨**(Z-slab: 현재 slice ±th/2를 Z축 mean/MIP 투영, MIP는 Image Adjust MIP 토글 연동). **Scout interval은 placeholder**(Z 스크롤 스텝 미적용). MMI 1.10-2③의 "Scout Th/INT ↔ **MPR 레이아웃** Axial **값 상호 동기**"는 **크로스-모듈**이라 D1(MPR 미접목)로 **standalone 미구현**(§12-D18) — CW 임베드 시 MPR store와 배선. (렌더 동작은 되고, MPR과의 값 동기만 미구현.) (c) 기존 dev 컨트롤(투영/렌더/연산 모드, WC/WW 슬라이더)은 다이얼로그 하단 '개발용' 블록으로 임시 이동(WC/WW는 T-P4-1 Image Adjust로 이전 예정).

### 3.6 Image Adjust 다이얼로그 (Windowing · Image Filter) — CW `ImageAdjustDialog` 이식

Title Bar의 **Image Adjust(대비) 아이콘** 클릭 → **Dialog**(폭 **380px**, 제목 "Image Adjust" + 닫기). CW 원본(CT variant): `packages/core/.../common/ImageAdjustDialog.tsx` + `CTSliceWindowingDialog.tsx`. MMI에 설명이 없어 **CW를 그대로 이식**(필터 알고리즘 포함).

**구성:**
- **Width / Level 슬라이더** — 범위(볼륨 min/max에서): `valueRange = max-min`, `center=(max+min)/2` → `level ∈ [center-valueRange, center+valueRange]`, `width ∈ [0, 2·valueRange]`. **Windowing 매핑**: `mappingMin = level - ceil(width/2)`, `mappingMax = level + ceil(width/2)` (그 밖은 clamp, 사이 선형).
- **필터 토글 버튼(하단 좌측)** — **Smooth · Sharpen · Max Sharpen · Inverse · MIP** (CT 세트). on 색 `#00BEA5`(hover `#61F2DF`), off 흰색. **배타 규칙**: Smooth/Sharpen/MaxSharpen **상호 배타**(하나 켜면 나머지 off), Inverse는 공존 가능.
- **Revert 버튼(우측, BackupIcon)** — tooltip "Revert to the original image." → W/L 기본 복원 + 모든 필터 off.
- 적용: **전 단면 일괄(전역 공유, Scout 포함)** — §12-D17 확정. **근거(기획):** W/L·Filter는 판독자 개인 시각 기준·선호를 **View 전환에도 유지**해야 하므로 전역 동일(≠ Thickness/Interval은 진단 목적별 뷰별 독립). 상태 text 좌상단(T-P7-4).
- **MPR 연동 미구현(§12-D18):** MMI 1.11-b①②의 "Image Adjust default·조정값이 **MPR 레이아웃과 연동**"은 **별도 MPR 서브모듈과의 크로스-모듈 동기**로, D1(MPR 미접목)에 따라 **standalone v1.3.2에서는 미구현**. Section 모듈 내 W/L·필터는 독립 동작하며, CW 임베드 시 MPR store와 배선한다.

**필터 알고리즘 (CW `ESImageMapper` 3×3 커널 포팅 — Section은 canvas ImageData/셰이더 post-process):**
| 필터 | 알고리즘 |
|------|----------|
| **Smooth** | 3×3 box blur, 전 계수 `1/9` |
| **Sharpen** | 3×3, 가장자리 `-0.5`, 중심 `5.0` |
| **Max Sharpen** | 3×3, 가장자리 `-1.0`, 중심 `9.0` |
| **Inverse** | `rgb → 1.0 - rgb` |
| **MIP** | slab 투영을 **기본 평균(mean) → 최댓값(MIP)로 전환**하는 토글(§12-D12 확정: 기본 mean, MIP는 이 토글로만). Thickness>0 필요, 단일 slice면 no-op |

- CW ref: `ImageAdjustDialog.tsx`·`imageAdjust.ts`(toggle/exclusivity/default)·`lib/vtkjs-wrapper/.../ESImageMapper`(3×3 conv+inverse GLSL)·`VolumeObject2D`(windowing·MIP blend). (2D 경로는 5×5 sharpen 커널이나, Section은 CT형이라 3×3 채택.)

## 4. Overlay 표시 규칙 (MMI 1.13 §6)

계측·주석(Length·Angle·Arrow·Free Draw) 귀속·표시. Clever One 기반. **MPR 레이아웃과 공유하지 않음.**

- **귀속:** Overlay는 Curve + 생성 시점 평면(point, normal)에 귀속. v1.3.2 단일 Curve(차기 다중 Curve 대비 설계).
- **Section 표시 조건(둘 다 충족):** (1) 현재 슬라이스 평면과 저장 평면 **거리 ≤ ±Interval/2**, (2) **Normal 허용 오차** — MMI "별도 정의" → **Spec 수치화 필요**. 초기값(제안) 두 normal 각 **≤ 5°**(`dot ≥ cos5° ≈ 0.9962`), 상수 분리·실사용 튜닝. **미확정(§12-D3).**
- **Curve point 변경:** 일시 미표시 가능, **데이터 삭제 아님** — 평면 조건 복귀 시 재표시.
- **Interval 변경:** normal 유지 → 원위치 복귀 시 재표시. **Thickness 변경:** 표시 조건 무영향.
- **좌표계:** 계측·주석·Curve 제어점은 **환자 볼륨 3D 좌표** 저장(개발실 §3.3). 2D 픽셀만 저장 시 Curve/Interval 변경으로 무효.

## 5. B/L 자동 판정 알고리즘 (기획 확정 규칙 — 2026-07-13)

정본: 기획(Jessi) 회신 2026-07-13. PLAN-1287 초안(반구·진행 방향·드로잉 중 극성 반전)은 **폐기**하고, Clever One 검증을 거친 아래 **단일 규칙**으로 대체한다.

**규칙:** Scout(Axial)에서 첫 두 제어점 **P1(시작점)·P2(두 번째 점)**를 잇는 선분을 긋고, **CT 단면 중심점 C가 있는 쪽 = L(설측), 반대쪽 = B(협측)**.

- **입력은 첫 두 점 P1·P2와 C뿐.** 반구 시작 판정·진행 방향 분류·드로잉 중 극성 반전(구 초안 로직)은 **전부 불필요**. curve가 이후 어떻게 꺾이든 라벨은 뒤집히지 않는다.
- **C** = CT Axial 단면(화면)의 중심점(십자선 중심).
- **판정식:** 방향 선분 P1→P2에 대한 C의 부호 `s = sign( (P2 − P1) × (C − P1) )` (2D 외적 z성분). `s`가 가리키는 쪽(= C가 있는 쪽) = **L**, 반대 = **B**.
- **출력:** curve 전역 `blPolarity`. Section 타일 좌·우 라벨 및 픽셀 열 반전(`nU-1-iu`)과 일관 연동.
- **결정 시점(1회 고정):** B/L은 **P1·P2가 처음 정해지는 순간 1회 결정**되고 그 값으로 **고정**된다. 이후 P3 이상 추가, 그리기 완료 후 P1/P2 이동 등 **어떤 곡선 편집에도 재판정하지 않는다.** 이후 방향 변경은 **수동 L/B Switching만**으로 한다.
- **BL/LB 기준점:** 첫 점 P1 위치의 시각 표식(MMI 1.3 #8). **기준점 이동은 B/L에 영향 없음** — MMI 1.3 #8①의 "기준점 중심 반전"은 폐기(§12-D10). 방향 반전은 L/B Switching으로만. **이동 기능의 용도 자체는 미확정(§12-D14, 기획 확인 대기)** — 현재 드래그는 되나 무효과라 정적 표식으로 정리 검토.
- **수동 override:** MMI 1.6 **L/B Switching**으로 `blPolarity` 토글(고정된 자동 판정을 사용자가 반전). 텍스트만 반전, 영상 flip 없음.
- **BL/LB 기준점(삼각형)의 시각 반전 (NEW, 2026-07-14):** MMI 1.3-8은 "이 삼각형 아이콘의 **위치/방향을 기준으로** Section의 B/L 표기 방향이 결정된다"고 규정한다. 즉 삼각형은 현재 B/L 방향을 나타내는 표식이므로, **L/B Switching으로 `blPolarity`가 토글되면 Section·Scout 텍스트 라벨과 함께 삼각형(아이콘 방향 및 "BL/LB"↔"LB/BL" 텍스트)도 반전되어야 한다.** ← **구현됨(2026-07-14):** `blPolarity` inverted 시 삼각형 방향(B 반대쪽)·라벨 "BL/LB"↔"LB/BL" 반전(ScoutView). *반전 방향의 정확성은 시각 확인 대기.* 이는 폐기된 1.3-8①(기준점 *위치*가 active line 중앙을 지나면 자동 반전)과는 **다른 항목**이다 — 1.3-8①은 D2·D10으로 폐기 유지, 본 항목은 "삼각형이 현 blPolarity를 시각적으로 반영"하는 것.
- **예외:** 점이 1개뿐이면 P2 미정 → 라벨 미표시(2점 입력 시 확정·고정).

**구현:** `packages/core/src/bl/blPolarity.ts` — (P1, P2, C) → `blPolarity`. **P1·P2 최초 확정 시 1회 계산 후 고정**(이후 편집 시 재계산 안 함), `SectionGrid` 타일 B/L text·`ScoutView` 라벨에 매핑. prj 저장은 `blPolarity`(B/L Switching 상태) + 기준점 좌표(§7).

### 5.1 Panorama 상단 방향 라벨 (R/L · P/A) — 기획 확정 규칙 (2026-07-14)

정본: 기획(Jessi) 회신 2026-07-14(MMI EP01_F004_PanoLineComponents p.13 5번 업데이트). MMI 1.2-2②는 "R, L 표시"로만 적었으나, 실제로는 **Curve 시작/끝점 각도에 따라 R,L / L,R / P,A / A,P로 바뀐다**. (B/L 판정과 유사하나 **B/L은 첫 2점, 방향 라벨은 시작점·끝점**을 쓰는 점이 다름.)

- **입력:** Curve **시작점 Start(P1)·끝점 End(마지막 점)** — 3점 이상이어도 시작/끝만 비교(중간 점 무시).
- **축 판정:** Start→End 벡터가 **수평축과 이루는 각**.
  - **< 45°(좌우 우세)** → **R/L 체계**.
  - **≥ 45°(전후 우세)** → **P/A 체계** (정확히 45°는 P/A, 기획 확인 2026-07-14). (`|dx| > |dy|` ⇔ R/L, 아니면(=이거나 같으면) P/A. dx=End.x−Start.x, dy=End.y−Start.y, Scout 픽셀좌표.)
- **라벨 배치:** 두 점의 좌표를 상대 비교. **Panorama 좌측 = Start의 라벨, 우측 = End의 라벨.**
  - **R/L:** Scout에서 **더 좌측(x 작음) = R, 더 우측 = L**.
  - **P/A:** Scout에서 **더 상단(y 작음) = A, 더 하단 = P**.
- **검증(MMI 이미지):** 정상 arch=R·L / 시작 우측 수평=L·R / 대각(시작 상단)=A·P / 수직(시작 하단)=P·A. 4케이스 모두 규칙과 일치.
- **구현(예정):** 순수함수 `panoramaDirectionLabels(start, end) → {left, right}`, Panorama 상단 오버레이(T-P7-4)·좌/우 배치. Curve 편집 시 실시간 갱신(시작/끝 이동 반영).

## 6. Draw Curve / Edit Curve 상세

MMI 본문과 PPT comment(기획 Jessi, 7/7~8) 상충 시 **comment(최신) 우선**.

| 항목 | 규정 | 근거 |
|------|------|------|
| **커브 종료** | **더블클릭**(마지막 점에서). point ≥ 2에서만 종료. 우클릭 아님 | MMI 1.5-d |
| ESC 종료 | **미적용**(CW MPR에 ESC 없음). 핸들러 구현 금지 | PPT comment 7/7 |
| 1점 더블클릭 | 종료 안 됨, 1점 유지. 종료는 **point ≥ 2** | comment 7/7 |
| 우클릭 | 직전 point **취소**(종료 아님), 1점이면 불가 | MMI 1.5 |
| 미리보기 | 마지막 point→커서 실시간. Active line은 항상 section line 중간 | MMI 1.5 |
| **Section 이미지 시점** | **curve 완료 후 1회 생성**(완료 전 blank), Active line만 점마다 갱신 | MMI 1.5(289행)+개발실 §5 |
| Draw 중 Th/INT 변경 | curve 취소 없음, 즉시 적용 | PLAN-1287·개발실 §4.3 |
| Edit point 최소 | 2점 미만이면 삭제·context menu 불가 | MMI 1.6 |
| **Edit 점 추가 버튼** | **좌클릭만** point 추가/이동/선택. **우클릭은 컨텍스트 메뉴 전용**(직접 추가 아님). Draw 모드와 동일하게 좌클릭 전용 | MMI 1.6(추가=context menu)·2026-07-15 버그수정(우클릭이 점 추가하던 것 차단) |
| **Edit/일반 컨텍스트 메뉴** | **우클릭**: Edit **point 위=[Delete Point]**, **커브 선 위/근처=[Add Point]·[L/B Switching]·[Delete Curve]**, **커브서 먼 빈 공간=[L/B Switching]·[Delete Curve]**(Add Point 없음). 일반 모드=[L/B Switching]·[Delete Curve]. **[Add Point]=두 점 사이 삽입**(MMI 1.6-①: 전후 order 사이 순번, 클릭 위치를 최근접 세그먼트에 insert). **끝에 추가는 좌클릭**(별개). 곡선 없으면 메뉴 미표시. 발견성 위해 빈 공간에서도 L/B/Delete는 뜨나 **Add Point는 커브 근처(hit='curve')로 제한**(먼 빈 공간의 중간 삽입 혼란 방지) | MMI 1.6-2·3·4·1.7 |

## 7. Save Project 데이터 모델 (MMI 1.14)

기획 확정: MPR 동일, Desktop→Web 최초 업로드만, 이후 Clever One sync 없음. proj Curve 있으면 복원, 없으면 blank(Clever One에서 Section 미오픈 prj 포함).

- **저장 항목(회전 각도 삭제):** 레이아웃(MPR/Section), 각 뷰 slice·Active line 위치, 카메라, ShowGrid, **Curve(point 좌표)**, Panorama 경계선·중심선, 각 단면 Thickness/Interval, Overlay, Windowing/Filter, **B/L Switching**, **BL/LB 기준점**.
- **호환(§12-D5 확정):** 최종 직렬화는 **CW prj(XML)와 호환**되게 한다. CW prj는 `vtkjs-wrapper/projectFile.ts`가 소유하며 **`CurveList`·`CurveInfo`·`SectionInfo`·`PanoInfo`·`SectionalPos`·`SectionInterval`·`SectionalNum`·`AutoCurveInfo` 필드가 이미 존재**하므로, Section 저장 항목은 **자유 설계가 아니라 이 필드에 매핑**한다. 좌표계는 환자 볼륨 3D(§4). 호환 방향은 Desktop→Web 단방향 우선(개발실 §4.1).
- **개발 중 임시 저장(확정):** 실제 prj 파일 I/O는 CW 팀 몫이므로, 개발·데모 단계에서는 **동일 직렬화 payload를 브라우저 `localStorage`(또는 파일 export/import)로 임시 저장/로드**해 복원을 검증한다. **저장 위치만 다르고 payload 구조는 CW prj 스키마와 동일**하게 유지해, 접목 시 저장 계층만 CW I/O로 교체하면 되도록 한다.
- **범위:** Section 모듈 = 저장 항목·스키마 매핑 + serialize/deserialize API + 개발용 임시 저장. 실제 prj 파일 I/O·자동저장·Desktop→Web 업로드 = CW 팀.

## 8. NFR (성능·환경)

| 항목 | 기준 |
|------|------|
| 9단면 생성 | 측정 JS 평균 **393ms**(362~427). 기본 JS(WASM 이점 제한적) |
| Section Slice 스크롤 | 30 FPS(**33ms**) 미달 = 최대 리스크. **디바운스(≥48ms)·캐싱(생성 slice 재사용)·표시 분리(이전 이미지 유지)·Thickness 상한**. 구현 초기 worst-case 벤치마크 → NFR 목표 확정(§12-D7) |
| Thickness 0mm | `slabHalfWidthMm=0` 경로 검증(현 기본 half 3mm=full 6mm). 상한 **30mm — combo·드래그 공통**(단일 `MAX_THICKNESS_MM`, §12-D8) |
| 입력 | v1.3.2 **마우스 전용**(모바일/터치 스펙아웃) |
| 브라우저·메모리 | Chrome 기준. CT 볼륨 100~250MB 수용. WebGL Context 3개 전략(CONTEXT_LOST 방지) |
| 계측 로그 | `SectionGen` JSON 한 줄(`{tag,mode,ms}`) 벤치마크 수집 |

## 9. CloudWebViewer 접목 정합 (핵심)

> "접목 용이성"의 핵심 절. 인용 경로는 `~/Documents/Azure/cloudwebviewer` 기준(2026-07-13 조사).

### 9.1 접목 원칙 — Section(WebGL)만 구현, VTK 미접목

**Section 모듈은 CW의 vtk 파이프라인(`Layout3DPAN`, `VolumeSectionView` 등)을 사용·구현하지 않는다(§12-D1).** Section 뷰는 poc의 WebGL 구현을 확장하며, 접목은 CW가 이 **WebGL Section 컴포넌트를 CW content로 embed**하는 방식이다. 따라서 정합 대상은 CW의 **셸 계약**(환경·툴바 store·content·타이틀 바·prj)이지 vtk 뷰가 아니다.

> 참고: CW엔 Section용 레이아웃 슬롯(`CTViewerLayout.Layout3DPAN`)과 vtk 뷰 **스텁**(각 ~25줄, 빈 상속)이 있으나 본 모듈 범위 밖이다. embed 시 CW는 이 슬롯 대신 우리 컴포넌트를 새 content로 연결한다(§9.7).

### 9.2 접목 형태 — CW가 embed할 수 있는 패키지 (§12-D4)

가장 접목 용이한 형태로 인계한다.

- Section 뷰를 **`@ewoosoft/scp-section-*` 패키지 + 공개 API를 가진 React 컴포넌트(`SectionViewer`)**로 제공한다. CW는 이를 npm/워크스페이스 패키지(또는 Module Federation remote)로 import한다.
- 공개 API는 CW store·toolbar·prj와 배선할 수 있도록 설계한다(§10): `volume`, `curve`, `blPolarity`, active `interaction`, 이벤트 콜백(slice 변경·overlay·save) 등을 주입/수신.
- **순수 수학 코어**(`scp-section-core`의 곡선·9단면·파노라마 — Catmull-Rom·trilinear·slab)는 **프레임워크 독립**으로 유지해, CW가 어떤 렌더 경로를 쓰든 재사용·검증 가능하게 한다.

### 9.3 환경 일치 (버전)

poc가 CW와 look&feel·의존성이 맞도록 major/정확 버전 정합. 구현 착수 전 게이트.

| 항목 | cloudwebviewer | scp-section-poc(현재) | 목표 |
|------|------|------|------|
| Node / pnpm | 20.x / **9.15.9** | ≥18 / 9.1.1 | 20.x / **9.15.9** |
| React / TS / Vite | 18.2 / 5.2.2 / 5.0.8 | ^18 / ^5 / **6.0** | 18.2 / 5.2 / **5.0** |
| MUI / Emotion / zustand | 5.15 / 11.11 / 4.4.7(+immer) | 없음 | 동일 major |
| registry | `.npmrc` Azure DevOps `@ewoosoft` private | 없음 | CW `.npmrc` 설정 공유(`@ewoosoft/*` 인증) |
| Federation | `@originjs/vite-plugin-federation` ^1.3, `shared: react·react-dom·zustand·@lingui/react` | 없음 | 접목 검증 시 shared 버전 정합 |
| 패키지 스코프 | `@cloudwebviewer/*` | `@ewoosoft/scp-section-*` | 유지(인계 시 API 문서화) |

### 9.4 Interface 일치 (타입 계약)

Section 뷰·데모·embed가 CW 계약 위에 얹히도록 정합.

| 계약 | CW 위치 | 정합 |
|------|---------|------|
| 컨테이너 API | `core-types` `IContainerApis { contentIOApis, eventListenerApis, settingApis, lockServiceApis }` | 데모는 stub, 제품은 CW 컨테이너에서 Section content가 소비 |
| Layout/Content | `ContentType='2D'|'CT'|'3DModel'`, `ContentDialog` contentType 분기 | Section을 새 content(또는 CT 하위)로 등록해 우리 `SectionViewer` 렌더(§9.7) |
| Setting 값 | `IMPRViewSetting { defaultThickness: MPRViewThicknessType, defaultInterval, defaultZoom }` | Section Th/INT 이 스키마 재사용(§9.5) |
| prj 스키마 | `projectFile.ts`(§7) | Section 저장 항목 매핑 |

### 9.5 common / core 모듈 일치

CW 소스(컴포넌트·store 로직) 복사·포크 금지. 아래 패턴에 맞춰 구현하면 embed 시 그대로 결합. **단, 아이콘 SVG 에셋은 픽셀 일치를 위해 복사 허용**(자기완결 에셋만, 툴바 로직 제외 — 데모 `cw/icons/`, CW 변경 시 수동 동기화).

| 요소 | CW 위치 | 정합 |
|------|---------|------|
| 패키지 역할 | `@cloudwebviewer/core`(UI·toolbar·다이얼로그) / `core-types`(계약) | Section 로직·WebGL은 `@ewoosoft/scp-section-*`(§9.2), CW core와 분리 |
| Content 등록 | `content/handler/ContentHandler`(추상)+`ContentHandlerFactory.addHandler`+`ContentDialog` 분기 | 접목 시 `SectionContentHandler`(ContentHandler 상속)가 우리 `SectionViewer`를 감싸 `changeInteraction`·`showOverlay`·`showGrid`를 컴포넌트 API로 전달 |
| Store slice | `store/index.ts` `RootStoreState = IWorkSpaceSlice & IToolSlice & …`, `ImmerStateCreator<T>`, `createSelectors` | Section 상태 추가 시 `ISectionSlice` 동일 시그니처 병합. federation shared zustand singleton |
| 뷰 타이틀 바 | `layout/components/ContentTitleBar.tsx` props `{id,activated,maximized,imageAdjustRef,open2DImageAdjustDialog}` | Scout·Pano·Section 헤더(W/L·Setting·최대화) 동일 컴포넌트/패턴 |
| 공통 다이얼로그 | `content/components/common/`(`ImageAdjustDialog`·`OverlayPropertyDialog`·`LoadingOverlay`), `ctContent/CTSliceSettingDialog`(Th/INT) | Image Adjust(1.11)·Setting(1.10)·계측 스타일 재사용 |
| 공용 UI | `components/`(`CustomMessageDialog`·`CustomSlider`·…) | Curve 삭제 확인(1.6)은 `CustomMessageDialog`(`messageDialog` slice) |
| 스타일 토큰 | Toolbar `#141414`·36px·hover `rgba(0,190,165,0.4)` | 데모·컴포넌트 동일 토큰 |

### 9.6 Toolbar 통신 일치

CW는 Toolbar·뷰가 단일 zustand `useBoundStore`로 통신. Section도 MPR 동일 패턴.

| 계약 | CW 정의 | 정합 |
|------|---------|------|
| Interaction | `toolbar/type.ts` `InteractionType='pointer'|'pan'|'zoom'|'length'|'freeDraw'|'angle'` | 동일 사용. **`arrow` 미포함 → 신규**(type+`TOOL_POLICY`(`toolbar/const.ts`)+`convertInteractionTypeToCTActionInfo`) |
| Feature | `WorkspaceViewFeatureType='showGrid'|'showOverlays'` | Section grid·Scout overlay 동기 |
| Command | `CommandType='resetView'|'resetCloudWork'|'initializeAll'|'viewOrigin'` | Section 뷰 동일 handler |
| 액션 | `activateInteraction`·`deactivateInteraction`·`setWorkspaceViewFeature`(`useBoundStore.use.*`) | 재구현 금지, 구독만 |
| 구독→뷰 | Toolbar→store→`useSyncToolWithWorkspaceContext(id)`→`ContentHandler.changeInteraction/showOverlay/showGrid`→뷰 | Section 뷰(WebGL)가 동일 훅 패턴으로 구독, active interaction에 따라 pointer·pan·zoom·계측·overlay 처리 |
| section 스코프 | — | 계측·Arrow는 각 section slice 내부만(MMI 1.13) |

계측(length/freeDraw/angle) 활성 시 `showOverlays` 자동 true(`shouldEnableOverlaysForInteraction`) 정책 동일.

### 9.7 CW embed 매핑 (인계 핵심)

우리 WebGL Section 모듈이 CW의 어느 지점에 어떻게 연결되는지.

| CW 지점 | 연결 방식 |
|---------|-----------|
| `ContentDialog` contentType 분기 | Section content 추가 → 우리 `SectionViewer`(Scout·Pano·Section grid) 렌더 |
| `ContentHandler`/`ContentHandlerFactory` | `SectionContentHandler`가 toolbar·store 명령을 `SectionViewer` API로 중계(§9.5) |
| `useBoundStore`(tool/workspace slice) | interaction·grid·overlay 구독(§9.6) |
| `ContentTitleBar` | Scout/Pano/Section 헤더 |
| `projectFile.ts` Section/Curve 필드 | Save 매핑(§7) |
| `InteractionType`(+Arrow)·Setting Th·INT | 툴바·Setting 정합(§9.6·§9.5) |

### 9.8 EzCloud Test — 런타임 참고

[https://container.test.ezcloud.ezcld.net/](https://container.test.ezcloud.ezcld.net/) — Clever Space 내 Cloud Web Viewer. MPR·Toolbar·ContentTitleBar·Pan/Zoom/계측 UX 정본(조직 계정). Section Layout 미탑재 → MPR만 참고. Section 데모는 `scp-section-poc` `section-demo`.

## 10. 공개 API · 인계물

- 현재 표면: `@ewoosoft/scp-section-components` `SectionViewer({volume})`·`ScoutView`·`PanoramaView`·`SectionGrid`·`CTLoader`. `@ewoosoft/scp-section-core` `curve`·`panorama`·`section`·`webgl`·`dicom`.
- 확장(구현 시): `SectionViewer` props에 `curve`·`blPolarity`·active `interaction`·이벤트 콜백(slice·overlay·save) 주입/수신 추가 — CW store·toolbar·prj 배선 지점(§9.2). B/L·Save 직렬화 API를 core에 export.
- 인계물: ① MMI 정합 **동작 명세**(§3~§7), ② **패키지 + 공개 API**(§9.2), ③ **데모**(URL), ④ **CW embed 매핑**(§9.7), ⑤ **Known gaps**(Scout=MPR Axial 결합, Arrow 신규, Overlay normal 수치, §12 미결).

## 11. 스펙아웃 / Will Not Do (v1.3.2)

- Active section line **±45° 회전**(MMI 1.8) — 임플란트 시뮬 탑재 시 재검토(PLAN-1287 #3). Save 회전 항목 삭제.
- **모바일/터치** — 마우스 전용(작은 드래그 핸들이 터치 부적합, 공수 대비 효과 낮음).
- **Draw Curve ESC 종료** — CW MPR에 없어 미적용(§6).
- **다중 Curve** — v1.3.2 단일 Curve(데이터 모델만 확장 대비).
- **Web→Desktop / 양방향 prj** — Desktop→Web 단방향 우선(개발실 §4.1).
- **CW vtk `Layout3DPAN` 파이프라인 사용·구현** — 본 모듈은 WebGL Section만 제공(§9.1, §12-D1).
- **B/L 드로잉 중 극성 반전 로직** — 새 단일 규칙(§5)으로 불필요(폐기).

## 12. Decision Log / 미확정 (TBD)

| # | 항목 | 결정/상태 | 담당·게이트 |
|---|------|-----------|-------------|
| D1 | 접목 범위 (VTK 여부) | **확정** — Section 모듈은 CW vtk **미접목**, Section 뷰(WebGL, poc 확장)만 구현. 접목은 CW가 우리 컴포넌트를 embed(§9.1) | — |
| D2 | B/L 자동 판정 | **확정** — 기획 단일 규칙(§5): P1→P2 선분, C가 있는 쪽=L. 동적 반전·반구·기준점 중심 반전(MMI 1.3#8①) 폐기 | 기획 회신 반영 완료 |
| D3 | Overlay Normal 허용 오차(§4) | 초기값 5° 제안 → 구현 초기 튜닝 후 고정. **사용자 결정 불필요** | 구현 초기 |
| D4 | 접목 형태(§9.2) | **확정** — `@ewoosoft/scp-section-*` 패키지 + 공개 API `SectionViewer`로 CW embed, 순수 core 프레임워크 독립 | — |
| D5 | Save prj(§7) | **확정** — CW prj XML 스키마 호환 직렬화. 개발 중엔 동일 payload를 브라우저 `localStorage`/export로 임시 저장. 호환 방향 Desktop→Web 우선 | CW 팀(스키마 필드 확인) |
| D6 | 구현 커버리지 | **확정** — poc를 확장해 MMI 1.1~1.13 **전 기능** | — |
| D7 | Section Slice 스크롤 NFR(§8) | 벤치마크 결과로 목표 수치 확정. **사용자 결정 불필요** | 구현 초기 |
| D8 | Scout 명칭 / Thickness drag cap | Scout 유지(기획 검토). **Thickness 드래그도 combo와 동일 30mm cap 확정**(2026-07-13, 개발실) — 정합성 + Section scroll 성능 예산(§8, Thickness 상한이 완화책) + 단일 `MAX_THICKNESS_MM` 재사용. clamp 한 줄이라 가역적 | 기획 / 개발실 |
| D9 | 일정·인원·KPI | 목표 1주·예상 2주, Raymond 1명. 비즈니스 정량 KPI 제품팀 미요구(N/A) | — |
| D10 | B/L 결정 시점·기준점 역할 | **확정** — B/L은 최초 P1·P2로 **1회 고정**, 이후 편집(P3+·P1/P2 이동)에 재판정 없음. 변경은 수동 L/B Switching만. BL/LB 기준점 이동은 B/L 무영향(§5) | 기획 회신 반영 완료 |
| D11 | 파노라마·단면 생성 모델 | **확정**(기획 2026-07-13) — 파노라마 = 곡선 따라 **가느다란(기본 Th0) 재슬라이스를 P/A로 offset 스윕**(navigator line). PoC의 thick-MIP 고정 모델은 **정정**. Section도 동일 slab 두께 보유. MMI·Ez3D-i·CleverOne 동일(§3.3). *이전 MMI 분석 누락분* | 기획 확인 반영 완료 |
| D12 | 슬랩 투영 방식 (max vs mean) | **확정(기획 2026-07-14)** — Thickness>0 slab 투영 **기본 = 평균(mean)**. **MIP(최댓값)는 Image Adjust 다이얼로그의 필터 토글**로만 선택(§3.6). (임상적으론 다소 이상하나 요구사항.) 엔진은 둘 다 지원, 기본 preset=`mean` | 기획 확인 반영 완료 |
| D13 | MMI 미명시 파라미터 범위 | **확정(개발실, 2026-07-14)** — MMI가 기본값만 준 값의 범위를 개발실이 정함: Section 가로폭 기본 30mm·**범위 20~80mm**, Section 세로폭 기본 60mm(§3.4). MMI/기획 갱신 시 갱신 | 개발실 정의 |
| D14 | BL/LB 기준점(삼각형) 이동 기능 용도 | **미확정 — 기획 확인 대기.** D10으로 "기준점 위치 기반 B/L 반전"이 폐기되어 삼각형을 드래그해도 **기능적 효과가 없다**(순수 표식만 이동). MMI 1.6-8/1.7-7의 "기준점 이동"도 원래 *개발실 리뷰 후 적용 여부 확정(TBD)*. **선택지**: (a) 드래그 제거·시작점 **정적 표식**(D10과 가장 일관, 개발실 권장), (b) 이동에 별도 용도 부여, (c) 현행 유지(이동하나 무효과). 기획 회신 필요 | **기획 확인 대기** |
| D19 | **DICOM 방향 태그 처리 (R/L 방향 유도)** | **확정(2026-07-15) — 표준 axial 방향 가정, 방향 태그 미독해.** 화면 좌=R·우=L(방사선 관례). `CTVolumeLoader`는 `(0020,0037)`ImageOrientationPatient·`(0018,5100)`PatientPosition **미독해**. **CloudWebViewer도 동일**(코드 조사: IOP는 파싱하나 "do not consider image orientation" 주석으로 **무시**, direction 행렬 항등 하드코딩[`io/Dicoms/common/utils.ts:395`], PatientPosition 미독해, R/L 라벨 월드축 고정매핑[`common/utility/volumeUtility.ts`]). **근거:** Vatech dental CBCT는 표준 HFS·axial LPS 저장. **비표준 방향(뒤집힌 FFS·IOP 부호 반전) 데이터는 범위 밖** — CW/우리 모두 좌우 반대로 표시될 수 있으나 실제 유입 없음. CW팀 부재로 현행 유지. 향후 필요 시 direction cosine·PatientPosition 유도로 견고화(개선 여지, §3.4). | 확정(현행 유지) |
| D18 | **MPR 서브모듈 연동 항목 (Scout Th/INT 동기 · Image Adjust 연동)** | **확정 — standalone 미구현, CW MPR 통합 시 배선(근거 §12-D1).** MMI 1.10-2③(Scout Th/INT ↔ **MPR 레이아웃** Axial 상호 동기)·1.11-b①②(Image Adjust default·조정값 ↔ MPR 레이아웃 연동)은 **Section 레이아웃 내부가 아니라 별도 MPR 서브모듈과의 크로스-모듈 동기**다. D1로 **MPR 미접목**이 확정돼 현재 연동 대상이 없음 → **v1.3.2 standalone에서는 미구현**. Scout `scoutThicknessMm`/`scoutIntervalMm`·Image Adjust W/L·필터는 **모듈 내에서 독립 동작**(기능 결함 아님). **CW 임베드(§9.2) 시 MPR store와 양방향 배선**하면 충족. → 미구현 표시: §1.10·§1.11·§3.5·§3.6. | 통합 시 구현 |
| D17 | **Image Adjust 적용 범위 (전 뷰 공유 vs 뷰별)** | **확정(기획 회신 2026-07-14).** (Q1) **W/L·Filter = 전 뷰 공유(전역)**, **Thickness/Interval = 뷰별 독립** — 맞음. (Q2) **W/L은 Scout 포함 전역**(회신 "전역 동일·View 전환 시에도 동일 기준" → 모든 단면 view 포함). (Q3) **근거(기획):** *W/L은 판독자 개인의 시각적 기준·선호를 View 전환에도 유지해야 하므로 전역 동일; Thickness/Interval은 뷰의 진단 목적에 따라(예: Pano 두껍게·Cross-section 얇게 병행) 의도적으로 다르게 두고 비교 판독하므로 뷰별 독립.* **현재 구현(W/L·Filter 3뷰 공유·Th/INT 뷰별)과 일치.** | 기획 회신 반영 완료 |
| D16 | **슬랩 두께 샘플링 알고리즘 + sub-voxel(0.1mm) 처리** | **확정(개발실, 2026-07-14 — CW 소스 분석 근거).** MMI·기획 모두 알고리즘 미규정 → CW MPR 소스 분석으로 결정. **공식은 §3.3에 구현 수준으로 기재**: `stepMm=slabSampleStepMm>0?그값:max(1e-3,min(spacing[0],spacing[1]))`(기본 0=voxel 자동연동), `nHalf=max(0,round((thickness/2)/step))`, 샘플 `tmm=k·step (k=−nHalf..+nHalf)` → trilinear → mean(기본)/mip(토글). **sub-voxel(0·0.1mm)=단일 중앙 샘플 1장**, 평균/MIP는 `nHalf≥1`일 때만. CW 의도식 `max(1,round(thickness/voxelSpacing))` 동치. **CW 현행 MPR은 두께 미반영(reslice Z=1, stripped)** — 우리 엔진이 정상. 구현: `panorama.ts`·`section.ts`. | 개발실 정의(CW 분석) |
| D15 | **Interval 뷰별 독립 + Panorama Interval 용도** | **확정(기획 회신 2026-07-14).** MMI 1.10-3① "각기 다르게 적용" = **3 뷰 Interval 독립**(CleverOne도 독립 동작 — A3). 의미: **Scout=축(Z) 슬라이스 스크롤(MPR 동기·Voxel Based)** (A1 확정), **Section=호 방향 단면 간격(Scout·Pano의 Section line 간격도 구동, 1.10-3b)** (A1 확정), **Panorama=곡선 법선방향 offset 스텝**(Interval만큼 offset 주며 파노라마 위치 이동, A2 확정). **★ 명칭 변경(A2 후속):** 파노라마 슬라이더 **`P/A` → `B/L`** — 법선 방향이 곧 Buccal/Lingual 축이며, arch가 아닌 curve(세로 등)에서는 P(Posterior)/A(Anterior)가 성립 안 함. 기획이 MMI를 B/L로 업데이트 예정. **구현:** 3뷰 독립 interval(T-P3-6) + 파노라마 슬라이더/ navigator B/L 표기(T-P3-5). | 기획 회신 반영 완료 |

---

## DoD

**Spec 리뷰 게이트**
- [ ] MMI 1.1~1.14 전 항목 매핑(§3)·모드 표(§3.2), 확정/스펙아웃/미확정 명시
- [ ] 접목 정합 §9 — 원칙(9.1, VTK 미접목)·형태(9.2)·환경·Interface·common/core·Toolbar 통신·embed 매핑(9.7)
- [ ] B/L 규칙(§5) 확정 반영 — 최초 P1·P2 1회 고정, 이후 수동 switch만. Overlay normal 수치 TBD 명시

**환경 정렬 게이트(구현 전, §9.3)**
- [ ] pnpm 9.15.9·Node 20·React 18.2·TS 5.2·Vite 5.0.8·MUI 5.15·zustand 4.4, `.npmrc` `@ewoosoft` 인증
- [ ] `section-demo` pnpm dev 기동, CW `Toolbar` 렌더(실패 시 Known gap), CW toolbar/common 복사 없음

**구현·인계**
- [ ] §3 각 항목(1.2~1.13) 구현. Section Slice 스크롤(1.9) — §8 벤치마크로 확정한 NFR 목표(§12-D7) 충족
- [ ] Draw/Edit curve(§6), B/L(§5, P1·P2·C 규칙)+L/B Switching, Overlay(§4) 3D 좌표, Arrow(1.12) section 스코프
- [ ] Save 직렬화 CW prj 스키마 호환(§7·§9.5) + 브라우저 임시 저장 검증
- [ ] 공개 API·embed 매핑(§9.2·§9.7) 문서화, 인계물 5종(§10), image23+§2 한 화면 정합

---

## 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1~0.6 | 2026-07-09~10 | 초안 — B/L·환경 정렬·pnpm link·EzCloud·화면 3분할 |
| 1.0 | 2026-07-13 | MMI 1.1~1.14 전 매핑·모드 표. Overlay·Draw curve·Save·NFR 신설. cloudwebviewer 실조사 반영 §9 |
| 1.1~1.2 | 2026-07-13 | 접목 방식 검토, spec-reviewer 리뷰 반영(8필드·중복 최소화·N/A·측정가능 NFR·MMI 정합 보정) |
| **1.3** | **2026-07-13** | **접목 범위 확정(D1): CW vtk 미접목, Section(WebGL, poc 확장)만 구현 — §9 전면 재정리(스텁 채움 → embed 정합), §1·§2·Risk 재작성. B/L 새 규칙(D2): P1→P2 선분·C쪽=L 단일 규칙, 동적 반전 폐기 — §5 재작성. 접목 형태 패키지+공개 API(D4, §9.2). Save CW prj 호환+개발용 브라우저 임시 저장(D5, §7). 커버리지 poc 확장 전 기능(D6). 일정 목표1주/예상2주(D9)** |
| **1.4** | **2026-07-13** | B/L **결정 시점 명확화(D10 확정)**: 최초 P1·P2로 1회 고정, 이후 P3+·P1/P2 이동 등 편집에 재판정 없음, 변경은 수동 L/B Switching만. 기준점 이동 B/L 무영향. §6에 **커브 종료=더블클릭**(우클릭=직전 취소) 행 명시 |
| **1.5** | **2026-07-13** | **공유(VKS 리뷰)용 참조 정리**: "참조"를 org URL로 교체(MMI=SharePoint PPT, PLAN-1287=Jira, 개발실 리뷰=VKS), 내부 문서(개발계획·작업 가이드) 링크 제거. 본문 내부 인용(MMI.md 추출본·작업 가이드 §4.2) → 정본·출처 표기로 정리 |
| **1.22** | **2026-07-15** | **CW UI 크롬 색·치수 통일(§3.4.1a 신설)**: 사용자 측정값을 **CW 소스코드에서 직접 대조** → teal·헤더 색/높이가 불일치하여 **소스 정본값 채택(Jessi 확정)**. Top Toolbar `#141414`·h60(`CwToolbar` 44→60), 뷰 헤더 **`#333333`·h32**(`ViewTitleBar` 26→32), 뷰 배경 `#000`. **아이콘 색 모델**: 기본 `#FFFFFF`·hover/active **`#00BEA5`**·active+hover **`#61F2DF`**·disabled **white@opacity0.3**, **hover는 배경 대신 fill 변경**(`rgba(0,190,165,0.4)` 배경 hover 제거). 기존 `rgb(0,190,165)`(=`#00BEA5`)는 CW 정본과 일치해 유지. **MPR/Section 전환 바는 CW에 없음** → 데모 전용(`#3B3B3B`·h34)으로 명시, 접목 시 제거. (측정값 `#16B69C`/`#5BF0DB`/`#2D2D2D`/`#5B5B5B`은 스포이드 오차로 판단·미채택.) |
| **1.21** | **2026-07-14** | **자동 배치(사용자 부재 중)**: ① 방향 라벨 `panoramaDirectionLabels`(§5.1) core 구현 + Panorama 상단 렌더 + UT-UI-034. ② **prj 저장 모델·직렬화**(core `project/`: `SectionProjectState`·serialize/deserialize round-trip, T-P5-1/2) + 데모 localStorage/export·import. ③ **Info Overlay**(우상 W/L+Filter·우하 TH/INT/Slice) 3뷰(T-P7-4 부분). ④ **B/L 삼각형 blPolarity 반전**(방향·"BL/LB"↔"LB/BL", 시각확인 대기). ⑤ T-P7-3(Pano 슬라이더 B/L 실배선) 완료 체크. |
| **1.20** | **2026-07-14** | **§5.1 신설 — Panorama 상단 방향 라벨 규칙(기획 확정)**: MMI 1.2-2② "R,L"은 실제로 Curve 시작/끝점 각도에 따라 **R,L/L,R/P,A/A,P 동적**. 수평 기준 <45°=R/L·≥45°=P/A, 좌측=Start 라벨·우측=End 라벨(R/L: 좌측점=R·우측점=L / P/A: 상단점=A·하단점=P). MMI 이미지 4케이스 검증. §3.1(1.2) 갱신. 구현은 T-P7-4(방향 오버레이). |
| **1.19** | **2026-07-14** | **Scout thickness 실동작(Z-slab)**: Scout를 단일 slice→ **현재 slice ±(th/2)를 Z축 mean/MIP 투영**(MIP는 Image Adjust MIP 토글 연동). thickness=0이면 단일 slice. Scout에서도 두께·MIP가 의미를 가짐. (Scout interval의 Z 스크롤·MPR 값 동기는 여전히 미구현 §12-D18.) |
| **1.18** | **2026-07-14** | **T-P4-1 Image Adjust 완성**: `ImageAdjustDialog`(W/L·필터·Revert) 3뷰 배선. W/L 범위=볼륨 기본값 적응형(`wlSliderRanges`, 9000 등 큰 WW도 수용). MIP 재생성 버그 수정(Panorama). **필터 알고리즘** core `applyImageFilter`(3×3: Smooth 1/9·Sharpen 중심5/이웃−0.5·MaxSharpen 중심9/이웃−1 모두 합1, Inverse 255−v) Scout/Panorama/Section 후처리. Section 캐시키에 필터 포함. 전 뷰 공유(§12-D17 확인 대기). UT-FLT-001. |
| **1.17** | **2026-07-14** | **Panorama 비율 정합(왜곡 수정)**: 파노라마 비트맵의 픽셀 비율(nCols:nRows)이 물리 비율(archMm:Zmm)과 달라(열 간격≠Z 간격) 왜곡·이상 여백 발생 → **행(Z)을 columnSpacing mm 간격으로 생성**해 **물리 정사각 픽셀**로 만들고, 표시는 **contain**(비율 유지 letterbox) 유지. arch 길면 상하 여백·짧으면 좌우 여백(Section 타일과 동일). (fit-width 시도는 폐기.) |
| **1.16** | **2026-07-14** | **T-P3-5·T-P3-6 구현**: ① **Panorama navigator line**(Scout 단선·초록, 커브 법선 offset, 기본 0=커브 위) + **B/L 슬라이더**(±20mm 잠정·step=panoramaInterval, L−/B+)로 조작. ② `generatePanoramaImageData` **`navigatorOffsetMm`** 추가 → 재슬라이스를 법선 바깥(B)/안(L) 이동, offset 변경 시 자동 재생성. ③ **3뷰 독립 interval**: `scoutIntervalMm`(축 Z·placeholder)·`panoramaIntervalMm`(B/L step, 기본1)·`sectionIntervalMm`(호 방향, section line 구동). 각 Setting 다이얼로그 자기 interval 바인딩(단일 공유 버그 해소, §12-D15). |
| **1.15** | **2026-07-14** | **Scout 커브 숫자 = slice 번호로 정정(중요)**: MMI 재검토 결과 커브 위 숫자는 **호장 mm가 아니라 slice 번호**(Section 타일 109·110…·Total Slice 635와 동일 인덱싱)임을 확인. 구현: 짧은 tick=매 slice, **major·숫자=매 20번째 slice(`m%20===0`), 라벨=slice 번호 `m`**, 9 Active line major도 slice 번호 %20. **interval 변경 시 총 slice 수가 달라져 major가 갱신**됨(이전 arc-mm 방식은 interval 무관하게 20mm 고정이라 "반영 안 됨"으로 보였음). v1.14(arc-length 접근)는 폐기. §3.4.1 정정 |
| **1.14** | **2026-07-14** | **(폐기·discard됨) Scout 20mm major tick arc-length 접근**: 기존 index 기반(`m % round(20/intv)`)→**호장 20mm 배수에 가장 가까운 tick 1개**(`|s−round(s/20)·20| < interval/2`). interval을 바꿔도 항상 20mm마다 major 1개. minor 촘촘해도 묻히지 않게 **major tick을 더 길게(반장 5.5mm vs minor 2.2)·굵게(2px vs 1)**. 숫자 라벨=`nearest20`. 9개 Active line major도 동일 기준. |
| **1.13** | **2026-07-14** | **Section 타일 ruler·레이아웃 정합(MMI image19)**: ① ruler·slice번호·B/L을 **오버레이**로(reserved strip 제거) — WebGL·Canvas2D 두 경로 모두. ② **가로 ruler = 타일 전체 폭 바**(눈금은 이미지 원점 기준 mm로 배치). ③ **눈금 5mm(보조)·10mm(주)**. ④ 스케일 = **contain(단면 W×H 전체가 보이게 종횡비 유지·letterbox)**. **(설계 결정)** 초기 cover(꽉참) 시도는 **H>W일 때 세로가 crop되어 파노라마 경계선으로 H를 키워도 반영 안 되는 버그**를 유발 → contain으로 확정. contain은 H 변경이 항상 반영되고 이미지가 안 잘림(임상 정확). **대가:** 종횡비(예 30w×60h)가 타일과 다르면 좌우 여백 발생(불가피). **주의:** Scout B/L 핸들(W)·파노라마 경계선(H)은 **독립 데이터**지만, contain은 두 축으로 스케일을 맞추므로 W 변경 시 표시 배율이 바뀌어 W·H 표시가 함께 변함(왜곡 없는 fit의 특성, 데이터 결합 아님). `SectionTileChrome` 재작성. |
| **1.12** | **2026-07-14** | **세로 스케일 바(ruler) 뷰별 길이·DICOM 척도 정합**: Scout **50mm**/Panorama **20mm**(공용 20mm→분리, MMI image19). 척도(mm→px)는 **DICOM 값 기반 확인**: Scout=`spacing[1]`(PixelSpacing Y, 0028,0030), Panorama=`spacing[2]`(SpacingBetweenSlices Z, 0018,0088). ⚠ DICOM에 PixelSpacing 없으면 로더가 `1\1`로 fallback → 척도 오차 가능(데이터 의존). `ViewVerticalScaleBar`에 `lengthMm` prop 도입. **눈금 간격: 작은 눈금 5mm·큰 눈금 10mm**(기존 1mm→5mm, MMI). |
| **1.11** | **2026-07-14** | **MMI 1.3/1.4 렌더 정합(구현)**: ① 악궁 Curve **노랑**(`#FFD21E`, MMI 1.3 정본; 길이 라벨은 초록 분리). ② Scout thickness line·control point 4개(시작·끝점)를 **빨간 선 위(맨 위 레이어)** 로 이동, placeholder 가이드선 제거. ③ 시작 `0.00mm` 제거·끝 총길이 라벨 근접·시작선 L쪽 두께값 라벨. ④ **Panorama 상하 경계선 = 노란 실선**(점선→실선, MMI 1.4-1). ⑤ **Panorama Active section line은 상하 경계선 사이에만**(전체높이→밴드내, MMI 1.4-4·Slide13). ⑥ **Panorama 세로 Center section line = 노랑**(cyan→노랑, MMI 1.4-4① "다른 색상"; 가로 중심선은 초록 유지 1.4-2). ⑦ **Center section line이 상·하 경계선과 만나는 지점에 녹색 원 2개**(control point, image19/Slide13). ⑧ Scout 오버레이 interval 의존성 명시(Section interval 변경→Scout section/active line 간격 갱신, MMI 1.10-3b) |
| **1.10** | **2026-07-14** | **D12 확정(기획)** — slab 투영 **기본 = 평균(mean)**, **MIP는 Image Adjust 필터 토글**로만(임상적으론 이상하나 요구사항). §3.3·§3.6·D12·코드 기본 preset `mip→mean` 반영. IP T-P3-5 갱신 |
| **1.9** | **2026-07-14** | **§3.5(Setting 다이얼로그)·§3.6(Image Adjust 다이얼로그) 신설 — CW 이식 구현 스펙**. Setting: 기어→Popover, Thickness combo(0~30)·Interval combo(Voxel Based~10), **thickness 뷰별 독립**(파노라마↔Section 분리·기본 0). Image Adjust: W/L(mappingMin/Max)·필터(Smooth/Sharpen/MaxSharpen box1÷9·edge/center 커널·Inverse 1−rgb·MIP=slab투영/D12)·배타규칙·Revert. §1.10·1.11 행 갱신 |
| **1.8** | **2026-07-14** | **§3.4.1 신설 — 오버레이 색상(RGB) 임시 지정 정리**(기획 회신: GUI styleguide 전달 전 임의색 무관). Curve `#20EE31`·제어점/삼각형 `#30B138`·Section line 노랑`#FFE046`/major`#DB696B`/minor`#683838` 등. Section line 색 규칙(중앙/20배수/그외)을 짧은 tick·9 Active line에 동일 적용, window 위치 tick 생략(겹침 방지) |
| **1.7** | **2026-07-14** | **§3.4 신설 — MMI 미명시·개발실 정의 값**: Section 가로폭 기본 30mm·**범위 20~80mm**, 세로폭 기본 60mm(D13). MMI는 기본값만 명시(1.3-3a)해 범위를 개발실이 확정, 별도 항목으로 추적 |
| **1.6** | **2026-07-13** | **MMI 전면 재검토(38 슬라이드) — 파노라마 생성 모델 정정 + 누락 보강.** ① **파노라마 = thin 재슬라이스(기본 Th0)를 P/A로 offset 스윕**(navigator line), thick-MIP 고정 모델 정정 — 신규 **§3.3**·D11. ② **슬랩 투영 max vs mean = 기획 결정 대기(D12)**, CleverOne=평균. ③ **Section도 slab Thickness(0~30) 보유** 명시(§1.10). ④ **Thickness combo 옵션 {0,0.1,0.5,1,2,3,5,10,20,30}mm** + drag off-list 값 + **Voxel Based Interval**(§1.10). ⑤ 1.8 P/A slice=offset 스윕 명시. (MMI 1.3#8① 기준점 반전은 이미 D10에서 폐기 — 정합) |
