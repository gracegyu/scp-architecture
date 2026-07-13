# Engineering One Pager

## Project Name

Cloud Web Viewer v1.3.2 — Section Module

## Date

2026-07-13

## Submitter Info

Raymond (전규현) · Ewoosoft Cloud Web Viewer 팀 · raymond.jeon@ewoosoft.com — Section 모듈 Spec v1.5

## Project Description

Clever Space Cloud Web Viewer(웹 CT 뷰어)에 치열궁 단면 진단용 **Section Layout**(MMI v1.3.2)을 추가한다. 지금은 MPR만 제공해 Section 진단이 필요한 사용자가 데스크톱 제품(Clever One)에 묶여 있으며, 본 프로젝트는 이 단면 진단을 웹에서 제공해 Clever Space 사용자의 웹 전환을 지원한다.

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
| **1.2** | 구성·정보 표시 | 3영역. 오버레이: Patient(좌상), W/L·Filter(우상), 상단 방향표기 = **R/L(Scout·Pano) / B/L(Section, Scout Section line 방향과 동일)**, thickness·interval·total slice(우하), ruler(우중앙). Slider(Scout H/F·Pano P/A·Section R/L). Scout Axial은 **MPR Axial과 뷰 비연동**(단 Th/INT는 MPR 서브모듈과 동기, 1.10). Image Adjust/Setting/최대화 = MPR 동일 | 대부분 보유 | 오버레이·라벨·slider image23 정합. **Section ruler = 가로·세로 전체 축**(PoC는 영상 폭) | 확정(ruler 갭) |
| **1.3** | Scout Curve 요소 | Curve, Section line(전체 slice·빨강 수직), Active section line(9개, 폭=Section 가로폭 기본 **30mm**), Center section line(5번째·노랑·control point), Panorama navigator line(초록), Panorama thickness line(초록 한 쌍·control point), L/B 표시(흰 text), **BL/LB 기준점**(첫 point·연두 삼각형) | 곡선·line·라벨 보유 | line 요소 명확화, **BL/LB 기준점 신규**, B/L 자동(§5) | 확정 |
| **1.4** | Panorama Line 요소 | 경계선(노랑, 기본 거리 **100mm**), 중심선(초록), Scout 위치선(흰 점선, 기본=중심선), Active section line(중 Center 다른 색) | 부분 | 경계선 100mm, 각 line 오버레이 | 확정 |
| **1.5** | Draw Curve | 좌클릭=추가, 우클릭=직전 취소(1점이면 불가), 더블클릭=종료. 미리보기 실시간. **Section·Panorama는 curve 완료 후 표시(완료 전 blank)**. §6 상세 | 부분(점마다 생성) | ESC 미적용·1점 더블클릭 무시·완료 후 1회·Active line 실시간(§6) | 확정 |
| **1.6** | Edit Curve | curve 이동, point 이동(drop 시 갱신)·삭제·추가(context menu, 최소 2점), Curve 삭제(확인 box), **L/B Switching**(text만 반전, 영상 flip 없음), **BL/LB 기준점 이동**(section line 따라 한 칸) | 편집 보유, 기준점 없음 | context menu, 기준점 drag, 확인 다이얼로그 | 확정 |
| **1.7** | Scout 조작 | Active line 이동·**길이 조절**(Center line control point 대칭 드래그 — PoC는 slider), Panorama thickness 조절(대칭), Scout slice 변경(휠·slider → Pano 위치선), 삭제·L/B Switching·기준점(편집 모드 동일) | slider 기반 | 드래그 핸들, thickness line 드래그 | 확정 |
| **1.8** | Panorama 조작 | 경계선 이동(세로폭, 대칭), 중심선 이동(drop 시 3뷰 갱신·Scout 위치선 동기), Active line 이동, slice 변경(휠·slider → Scout navigator line). **±45° 회전 스펙아웃** | 위치 이동 보유 | 경계선·중심선·active line 드래그. 회전 제외 | 확정 / ±45° 스펙아웃 |
| **1.9** | Section 조작 | **Slice 변경**(휠·slider → 9장·slice number·Scout/Pano Active line 동기), Center slice(5번째 강조), 최대화(3×3 유지), **개별 slice 더블클릭 최대화** | 중심 9장만 | **전체 slice 인덱싱·스크롤·페이징 신규**(§8 성능 핵심), slice number, 더블클릭 최대화 | 확정(핵심 신규) |
| **1.10** | Thickness/Interval | Setting에서 조절, MPR 동일. 기본 Th **0mm**(전 뷰), INT: Scout=Voxel Based(MPR 동기)·Pano/Section=1mm. 변경 시 오버레이·total slice·slider·line 간격 갱신. Draw 중 조정 시 curve 취소 없음(즉시 적용) | INT 보유, Th UI 없음·기본 full 6mm(=half 3mm) | **Th 기본 0mm**, Setting UI, combo 상한 **30mm**(CW `SLICE_THICKNESSES` 정합 §9.5) | 확정 |
| **1.11** | Windowing/Filter | Image Adjust: W/L + Smooth/Sharpen/Max Sharpen/Inverse/MIP. 전 단면 일괄, 좌상단 text. MPR과 연동 | Windowing만 | Image Filter MPR→Section, 뷰 간 동기 | 확정 |
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
- **BL/LB 기준점:** 첫 점 P1 위치의 시각 표식(MMI 1.3 #8). **기준점 이동은 B/L에 영향 없음** — MMI 1.3 #8①의 "기준점 중심 반전"은 폐기(§12-D10). 방향 반전은 L/B Switching으로만.
- **수동 override:** MMI 1.6 **L/B Switching**으로 `blPolarity` 토글(고정된 자동 판정을 사용자가 반전). 텍스트만 반전, 영상 flip 없음.
- **예외:** 점이 1개뿐이면 P2 미정 → 라벨 미표시(2점 입력 시 확정·고정).

**구현:** `packages/core/src/bl/blPolarity.ts` — (P1, P2, C) → `blPolarity`. **P1·P2 최초 확정 시 1회 계산 후 고정**(이후 편집 시 재계산 안 함), `SectionGrid` 타일 B/L text·`ScoutView` 라벨에 매핑. prj 저장은 `blPolarity`(B/L Switching 상태) + 기준점 좌표(§7).

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
| Thickness 0mm | `slabHalfWidthMm=0` 경로 검증(현 기본 half 3mm=full 6mm). 상한 30mm(CW combo) |
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

CW 소스 복사·포크 금지. 아래 패턴에 맞춰 구현하면 embed 시 그대로 결합.

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
| D8 | Scout 명칭 / Thickness drag cap | Scout 유지(기획 검토) / drag 상한 없음 기본(개발실). **사용자 결정 불필요**(기본값 유지) | 기획 / 개발실 |
| D9 | 일정·인원·KPI | 목표 1주·예상 2주, Raymond 1명. 비즈니스 정량 KPI 제품팀 미요구(N/A) | — |
| D10 | B/L 결정 시점·기준점 역할 | **확정** — B/L은 최초 P1·P2로 **1회 고정**, 이후 편집(P3+·P1/P2 이동)에 재판정 없음. 변경은 수동 L/B Switching만. BL/LB 기준점 이동은 B/L 무영향(§5) | 기획 회신 반영 완료 |

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
