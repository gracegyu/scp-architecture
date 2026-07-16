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

### 저장소 · 데모 사이트

본 모듈은 **PoC 모노레포 `scp-section-poc`를 그대로 확장**해 구현한다(별도 신규 repo 생성 없음). 저장소·배포 인프라는 [WebSectionView PoC OnePager](../PoC/WebSectionView_PoC_OnePager.md) 「소스코드 저장소 / Demo Site 구축」과 동일하다.

| 항목 | 값 |
|------|-----|
| **Repository** | Azure DevOps `prototypes/scp-section-poc` — [https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc) |
| **모노레포 구조** | pnpm workspaces + Turborepo. `packages/core`(`@ewoosoft/scp-section-core`)·`packages/components`(`@ewoosoft/scp-section-components`)·`packages/section-wasm`·`apps/section-demo` |
| **데모 사이트** | [http://scp-section-demo.test.scp.esclouddev.com/](http://scp-section-demo.test.scp.esclouddev.com/) (AWS S3 정적 호스팅, 계정 767397951498 SCPSharedDev, 리전 ap-northeast-2) |
| **CT 데이터(S3)** | 버킷 `scp-section-ct-data` — `https://scp-section-ct-data.s3.ap-northeast-2.amazonaws.com/ct-data/{파일}.zip` (퍼블릭 읽기, PoC 전용) |
| **CI/CD** | `azure-pipelines.yml` — main/develop push 트리거 → pnpm build → `aws s3 sync apps/section-demo/dist s3://scp-section-demo.test.scp.esclouddev.com/ --delete` |

> **범위 경계**: 위 저장소·데모·S3는 **Section 모듈(WebGL) 개발·검증용**이다. CW 접목 시에는 이 데모 셸(`apps/section-demo`) 대신 CW가 `@ewoosoft/scp-section-*` 패키지를 소비하며(§9.2), CT도 데모 S3 provider가 아니라 CW/Clever Space가 공급한다(§9.4·§1). 데모 사이트는 **접목 전 기능·UX 확인용 레퍼런스**로 유지한다.

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

**기획팀 회신(2026-07-14):** *"UI는 추후 VT UI/UX팀이 GUI styleguide를 제작해 전달 예정. MMI의 색상이 최종 반영 색이 아니므로 임의 색상 지정 무관. styleguide 일정은 미확정."* → 아래 색은 **개발실 임시 지정**이며 styleguide 전달 시 교체한다. Scout·Panorama 오버레이 색·굵기는 **`components/src/overlayStyle.ts` 토큰**(`SCOUT_OVERLAY_COLORS`·`PANORAMA_OVERLAY_COLORS`)으로 일원화(T-P7-5/6, 2026-07-15) — styleguide 전달 시 이 파일만 교체.

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
| **Show/Hide Grid 격자**(MMI 1.13-2a) | `#A9A9A9`·opacity **0.7**·1px·점선 `setLineDash([1,1])` (**CW `@ewoosoft/es-view-info` GridView 정본**) | `GridOverlay.tsx` |

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
| **Top Toolbar 아이콘 크기** | **36×36** (버튼 36 content-box 꽉 채움) | — | `Toolbar.tsx`(btn 36·pad 0), 아이콘 SVG `viewBox 0 0 36 36` |
| **뷰 헤더 아이콘 크기** | **24×24** (버튼 ~28, 헤더 32) | — | `lib/react-vtkjs …/const.ts` `TITLE_BAR_STYLE.ICON_SIZE=24` |
| active 토글(데모 MPR/Section) 배경 | `#00BEA5` | `#16B69C` | `App.tsx` `activeToggleStyle` |

> **MPR/Section 전환 바**: CW엔 별도 전환 바가 없고 툴바 내 single/dual 버튼으로 처리. 데모에는 전환 UX용으로만 존재(BG `#3B3B3B`·h34, `App.tsx` `selectBarStyle`) — **접목 시 제거/대체**(Jessi 확정 2026-07-15).
> **아이콘 hover는 배경이 아닌 fill(글자색) 변경**으로 표현(CW 아이콘 SVG가 `fill` prop 사용). 기존 `rgba(0,190,165,0.4)` 배경 hover는 제거. **CustomMPRSlider류 슬라이더**의 teal(`#00B1A2`/`rgb(0,177,162)`)은 크롬 아이콘 팔레트와 구분해 **그대로 유지**.
> **아이콘 크기(2026-07-15 정합)**: 초기 구현이 CW보다 작아(툴바 22·헤더 15) CW 소스 기준으로 확대. 우리 아이콘 에셋은 CW와 **동일 viewBox(툴바 36)** 복사본이므로, 툴바는 축소 없이 **36으로 꽉 채우고**(버튼 36·content-box·padding 0), 헤더는 CW `ICON_SIZE=24`에 맞춰 **24**(버튼 28). 툴바 아이콘 확대에 맞춰 버튼 간격도 소폭 확대.
> **폰트(2026-07-15 최종)**: **실제 호스트(CleverSpace) 폰트에 맞춘다** = `'Noto Sans', 'Noto Sans KR', 'Segoe UI', sans-serif`(ezcloud `container-app`·`common-ui`·`policy-app` 정본). CleverSpace는 **Noto Sans를 Google Fonts로 로드**하므로 데모도 동일 로드(`index.html` `<link>`)해 실제 배포 룩을 미리보기. 컴포넌트 인라인도 동일 스택(monospace 숫자 유지). **폰트 소유·embed는 CW/CleverSpace 전역 styleguide 몫**(모듈은 스택만 맞추고 강제하지 않음, §9.10).
> ⚠️ **CW는 다른 폰트를 강제(`'Segoe UI','Roboto' !important`)해 호스트와 불일치**(§9.11-CW-1 버그). 그래서 앞서 CW의 Roboto에 맞추려던 시도(@fontsource/roboto embed 등)는 폐기하고, **올바른 정본인 CleverSpace 호스트 폰트(Noto Sans)** 로 정렬했다. CW-1이 수정돼야 접목 시 우리 텍스트도 호스트 Noto Sans로 일관 렌더된다.
> **참고(Roboto/Chrome 오해)**: Chrome이 Roboto를 웹에 기본 제공한다는 건 오해다. **Android·ChromeOS에서만 Roboto가 시스템 폰트**라 웹 `font-family:'Roboto'`가 잡히고, **macOS·Windows Chrome은 내장 Roboto를 웹페이지에 노출하지 않는다**. 그래서 맥에서 CW의 미embed `'Roboto'`는 폴백(Helvetica)으로 보였다.

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
| **Edit 모드 시각 어포던스** | 미규정 | Edit 모드 상호작용은 **제어점·BL/LB 삼각형뿐**(width/thickness 핸들은 Edit에서 비활성)이므로, **제어점·삼각형만 밝게** 두고 **나머지(커브·section tick·9 active line·navigator·thickness·라벨)는 dim** 처리해 "점 편집 중" 상태를 명확히. **dim opacity는 상수 `EDIT_MODE_DIM_OPACITY`(현재 0.45)** 한 곳에서 조정(2026-07-16 상향, 이전 0.28은 너무 흐림). **겹침 예외(2026-07-16):** 정본 겹침 순서(MMI #49)는 제어점이 맨 아래이나, **Edit 모드에서는 편집 대상인 제어점을 최상단으로 올려**(흐려진 빨간 Section line 위) 밝게 표시 → 클릭·식별 용이. **비-Edit는 MMI #49 순서 불변.** **임시 dev 스타일**(GUI styleguide 확정 시 교체, §3.4.1). 개발실 제안(2026-07-15) |
| **Scout 커브 숫자 의미** | mm vs slice 불명확 | **slice 번호**(§3.4·§3.4.1 주석) |
| **계측/주석 적용 뷰 범위(Length·Angle)** | 1.13-1에 공통툴로 나열되나 **적용 뷰 미명시**(Arrow·FreeDraw는 1.12에 3뷰 명시) | **Jessi 확정(2026-07-15, §12-D21): Length·Angle도 Arrow·Free Draw와 동일하게 Scout·Panorama·Section 3뷰 모두 동작.** 각 뷰는 **자기 영역/슬라이스 스코프**(Scout=Scout 영역·Panorama=Panorama 영역·Section=해당 slice, 경계 넘나들 불가) |
| **Initialize All 초기화 범위** | MMI 1.13-1a는 버튼만 나열·의미 미정의 | **"데이터·값"은 초기화, "모드·토글"은 유지**(CW 정합, 2026-07-16 확인). **초기화**: Curve 제거(→파노라마·섹션 blank)·계측 제거·**Pan/Zoom 값→identity**·WL=볼륨 기본·섹션/파노라마 파라미터 기본. **유지**: 활성 도구·Show/Hide Overlay·Grid 토글. **결과**: CT 최초 로드처럼 Scout만(파생 영상 없음 — 커브 있어야 파노라마/섹션 생성). **재오픈 복원(저장본)과 별개**(저장본 불변). 상세=§3.10, 개발실 결정 §12-D30 |
| **Section slice 휠 스크롤 임계값** | MMI 1.9-1은 휠 스크롤만 명시(민감도 미정) | **누적 임계값 방식**(`SectionGrid onWheel`): deltaY를 누적해 **24 이상일 때 1칸** 스텝. 트랙패드 미세 스크롤·우클릭 제스처가 유발하는 작은 wheel로 slice가 튀는 것을 방지. 개발실 결정(2026-07-16) |
| **모드 상호 배타 (Curve Draw/Edit ↔ toolbar 도구)** | MMI 미명시 | **한 번에 한 모드만.** ① **Draw Curve/Edit Curve 버튼 클릭 시 활성 toolbar interaction(Pan/Zoom/계측/Pointer)을 해제**(`onClearInteraction`→`deactivateInteraction`)하고 커브 모드 시작. ② 반대로 **toolbar 도구가 활성화되면 진행 중 Curve Draw/Edit를 취소**(ScoutView 효과). ③ 커브 Draw/Edit 중엔 계측 오버레이 입력 차단(`SectionMeasureOverlay disabled`)·Pan/Zoom 비활성. 근거: 여러 모드 동시 활성 시 클릭이 엉킴(사용자 피드백 2026-07-16). 개발실 결정 |
| **계측/주석 도구 커서**(§3.7·§3.8) | MMI에 도구별 커서 미명시 | **CW `CURSORS` 정본 그대로**(도구→커서 매핑도 CW `ContentDialog.getSupportedCursorIcon` 정합): length→LENGTH(자), angle→ANGLE(각도), freeDraw→FREEDRAW(펜), pan→PAN(손), zoom→ZOOM(돋보기), Pointer Pen→POINTER·Eraser→ERASE, **편집 hover/선택→MOVE**(CW `overlaySelectedCursor`=화살표+십자, §3.9). **Arrow(v1.3.2 신규)는 CW에 전용 커서가 없어 임시로 FREEDRAW(펜) 사용** → **기획이 Arrow 전용 커서 제작 후 교체 필요(§11 숙제)**. `components/src/cursors.ts`(CW 복사)·`SectionMeasureOverlay` 배선. 2026-07-16 |
| **Section Pan/Zoom 적용 단위**(§3.7·§12-D27) | 1.13-1a "MPR 동일"만 있고 **3×3 내부 9뷰에 어떻게 적용하는지 미명시** | **9개 뷰가 하나의 transform으로 함께** Pan/Zoom(각 뷰 자기 중앙 기준 제자리 확대·타일 클립, 뭉쳐 스프레드 아님). **근거:** slice 스크롤(타일↔슬라이스 재매핑)·Save Project 단순화 — 뷰당 1개 상태. 타일별 독립(9개)은 스크롤 시 배율 혼선·저장 9벌로 복잡해 배제. "뷰 모드" 단일 상태. 개발실 결정(2026-07-15) |
| **Show/Hide Grid 간격·스타일** | 1.13-2a에 기능만 있고 **간격·색·선 스타일 미명시** | **CW 소스(`@ewoosoft/es-view-info` GridView) 정본 채택**: 간격 = **물리 10mm**(등방 isotropic `pxPerMm`, 설정 1~50mm), 색 `#A9A9A9`·opacity 0.7·1px·점선 `[1,1]`. **뷰(셀) 전체를 채움**(이미지 letterbox 여백 포함, zoom out 시에도), **원점 = 뷰 좌·상단(0mm)** = ruler 눈금과 정렬(MMI: view 시작=0). **Pan/Zoom에 반응하지 않는 고정 오버레이**(이미지만 확대/이동, 격자는 base 10mm 그대로 뷰 전체 유지 — §3.7·§12-D27, 2026-07-15). 3뷰 공통. Canvas 2D `GridOverlay`. (측정치 `#636363`은 검은 배경 0.7 불투명 렌더의 스포이드값으로 판단, §3.4.1a 선례.) **주: 초기 구현에서 누락(스토어·툴바만·뷰 미배선)이었고 2026-07-15 보완.** |
| **Scout 커브 편집/삭제 버튼(연필·휴지통) 스타일** | MMI는 **흰 바탕·검은 아이콘**이나 이는 PPT 임시 버튼(styleguide 아님)·식별성 낮음 | MMI placeholder 미채택. **CW 아이콘 버튼 컨벤션 재사용**(§3.4.1a·CW `ToolBtn`): 흰 아이콘·투명 배경·**hover/active teal `#00BEA5`**, 헤더 `IconBtn` 공용(28px·아이콘 18px), 연필/휴지통 글리프를 또렷한 Material edit/delete로 확대. **임시 dev 스타일**(styleguide 확정 시 교체, §3.4.1). CW엔 Section 커브 버튼 원본 없음(신규)이라 개별 매칭 대신 규칙 일치 |
| **Ruler 원점·범위(Section)** | image19에 눈금은 있으나 원점·범위 미명시 | **원점 0 = 뷰(셀) 좌·상단**(이미지 시작 아님, MMI "view 시작=0" 확인 2026-07-15), 눈금·라벨 **뷰 전체**에 걸침(letterbox 여백 포함). 등방 `pxPerMm`. **위치는 타일 하단/우측 고정**이나 **눈금 단위·간격·표시 mm는 Zoom 반영**(유효 pxPerMm=fit×zoom, 소·대눈금은 `chooseRulerSteps` 공통 규칙 1·5·10·50·100mm, 확대 시 1mm까지 촘촘 — §3.7·§12-D27b, 2026-07-15). `SectionTileChrome` |
| **Pan/Zoom/Reset View/Pointer 동작** | 1.13-1a "MPR 레이아웃과 동일"로만 규정·상세 미명시 | **MPR 동일 정의(§3.7)**: Pointer=기본(도구 해제), Pan=좌드래그 뷰 평행이동, Zoom=드래그/휠 배율(이미지 확대·축소), Reset View=Pan/Zoom 초기화. 정확한 제스처·중심은 **CW MPR interactor(`ES3DRenderWindowInteractor` 등) 정합**(구현 시 확인). 우리 초기 구현에서 **미배선**(interaction이 뷰 변환에 미연결)이라 보완 대상(IP T-P4-6) |
| **R/L 방향 유도** | 방향 태그 사용 여부 불명확 | **표준 axial 가정, 방향 태그 미독해**(CW 동일, §3.4·§12-D19). Scout 오버레이 **좌 가장자리=R·우 가장자리=L**(세로 중앙, 곡선과 무관하게 고정) |
| **환자정보 오버레이(MMI 1.2)** | 표시 필드·포맷·태그 미명시 | Scout **좌상단**에 line1=`[<성별>] <나이>`·line2=`<촬영일 YYYYMMDD>`. DICOM 태그 = Sex(0010,0040)·Age(0010,1010)·**StudyDate(0008,0020) 우선, 없으면 AcquisitionDate(0008,0022)**. 값 없는 필드는 생략(태그 전무 시 미표시). 오버레이 Age는 DICOM 원문(`034Y`) 그대로 |
| **환자 배너 타이틀(MMI 1.2)** | 필드·포맷 미명시 | 셸 상단 배너 = `<ID> <이름> <나이>`(예 `123456789-123 Jane Doe 34Y`). DICOM ID(0010,0020)·Name(0010,0010)·Age(0010,1010). **이름 = PN `Family^Given^Middle` → `Given Middle Family`**(빈 컴포넌트 제외, `^` 없으면 원문). **타이틀 Age = 앞 0 제거**(`034Y`→`34Y`). 값 없으면 안내 문구. 헬퍼 `patientTitle`/`formatPatientName`/`formatPatientAge`(components) |
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

### 3.7 공통 뷰 조작 도구 (Pan / Zoom / Reset View / Pointer) — MPR 동일

MMI 1.13-1a는 이 4개를 "동작 방식 MPR과 동일"로만 규정(상세 미명시). MPR 정합 기준 동작을 아래로 정의한다(§3.4.2). 3뷰(Scout·Panorama·Section) 공통, **일반 모드 전용**(Draw/Edit 모드에선 비활성, Appendix 매트릭스), toolbar `interaction`(`useToolStore`)로 구동(§9.6).

| 도구 | 동작(MPR 동일 목표) | 비고 |
|------|------|------|
| **Pointer** | **일시 주석(그리기) 도구** — 클릭 시 Pointer 모드 진입, 다이얼로그 열림, 다른 조작 정지(§3.8). ※ "도구 해제(neutral)"는 별개로 `interaction=null`(활성 도구 재클릭으로 토글 해제) | CW `PointerDialog`/`PointerCanvas` 정본(§3.8) |
| **Pan** | **마우스 이동(드래그)** 으로 뷰 이미지 **평행이동**(translate). 배율 유지 | 뷰 로컬 transform(pan offset), **뷰마다 독립** |
| **Zoom** | **마우스 우클릭 드래그**: **위·우로=확대·좌·하로=축소**. X·Y 이동량을 **합산**(`delta = dx − dy`)해 배율에 반영(위=−dy>0·우=dx>0 → 확대) | 뷰 로컬 transform(scale), **뷰마다 독립**. Section slice 휠 스크롤과 별개(휠은 slice 유지) |
| **Reset View** | Pan/Zoom transform **초기화**(기본 fit 상태 복귀). Windowing/Curve는 무관 | command형 |

**Pan·Zoom은 뷰(패널)별 독립 적용**(Scout·Panorama·Section 3패널 각자 pan offset·zoom scale — MPR 각 단면이 독립이듯). **입력은 마우스 이동(드래그)**: Pan=드래그 평행이동, Zoom=**우클릭 드래그(위·우=확대, 좌·하=축소; X+Y 이동량 합산)**. **드래그 중 오버레이 라벨 텍스트가 선택되지 않도록 뷰 컨테이너에 `user-select:none`.**

**Section 3×3 내부(중요, MMI 미명시·개발실 결정 — §3.4.2·§12-D27):** Section 패널의 **9개 뷰는 하나의 transform으로 함께** Pan/Zoom된다(모두 같은 pan/zoom 값). 각 뷰는 **자기 중앙 기준**으로 제자리 확대·이동하며 **타일 안에서만** 클립된다(9칸이 한 덩어리로 뭉쳐 스프레드되지 않음; 각 칸은 제자리에서 동일하게 커짐). **근거:** 9개가 함께 움직여야 slice 스크롤 시 타일↔슬라이스 재매핑이 단순하고(칸마다 다른 배율이면 스크롤 때 배율이 뒤섞임), Save Project도 뷰당 1개 상태만 저장하면 된다(9벌 불필요). 즉 Section Pan/Zoom은 **"뷰 모드" 단일 상태**로 다룬다. WebGL은 타일별 `gl.viewport`에 같은 transform을 각 타일 중앙 기준으로 적용 + `gl.scissor`로 타일 클립, 오버레이(grid·계측)는 셀별 중앙 기준 동일 transform.

**커서 = CW 정본 그대로**(2026-07-15, `components/src/cursors.ts`에 복사): 도구 활성 시 뷰 커서를 CW `CURSORS`(`cloudwebviewer/.../workSpace/setting/index.ts`)의 커스텀 SVG 커서로 바꾼다. **Pan = 손(panning) 아이콘(핫스팟 16,16)**, **Zoom = 돋보기(핫스팟 13,13)**, Pointer = 화살표(7,6), 입력 불가 영역 = DISABLE(금지, 3,3). 자기완결 base64 SVG data-URI라 §9.5 에셋 복사 허용(로직 아님, CW 변경 시 수동 동기화).

**Grid·Ruler는 Pan/Zoom에 반응하지 않는 고정 오버레이다(중요, 2026-07-15 확정 — §3.4.2·§12-D27):** Pan/Zoom은 **이미지(및 이미지에 앵커된 계측)에만** 적용되고, **격자(Grid)와 눈금(Ruler)은 움직이지 않는다.**
- **Grid**: 뷰 전체를 채우는 **고정 물리 10mm 격자**(pan해도 이동 안 함, zoom해도 간격 그대로). zoom out으로 이미지가 작아져 여백이 생겨도 격자는 뷰 전체를 그대로 덮는다(고정이라 자연히 항상 뷰 전체).
- **Ruler**: 각 뷰의 **하단/우측에 고정**(Section 타일 눈금도 타일 하단/우측 고정) — **위치는 Pan/Zoom에 불변**. 단, **눈금 단위·간격과 표시 길이(mm)는 배율을 반영**한다(Scout/Panorama 스케일 바는 픽셀 길이 고정·표시 mm = base/zoom → 2배 확대 시 50mm→25mm; Section 타일 눈금은 유효 pxPerMm=fit×zoom로 간격이 벌어지고 표시 mm 축소). **소·대눈금 단위는 3뷰 공통 규칙**(`chooseRulerSteps`): 화면 간격이 확보되는 최소 nice 단위(1·5·10·50·100mm)를 소눈금으로, 그 이상에서 라벨 간격이 확보되는 단위를 대눈금으로 선택(확대 시 1mm 소눈금까지 촘촘).
- **이미지 + 계측**: 같은 transform을 공유해 함께 이동·확대되고, 계측은 이미지 위 앵커를 유지한다. (Grid/Ruler는 뷰 고정 기준자 역할이고, 확대는 이미지 확인용.)
- 근거: 사용자 피드백(2026-07-15) — Grid가 pan 따라 흔들리고 Ruler가 이미지와 함께 커지면 기준자로서 혼란. 고정이 MPR 뷰어 관례에도 맞고 slice 스크롤·저장과도 단순.

**구현(T-P4-6, 완료)**: 공용 `useViewTransform` 훅(뷰별 `panX/panY/zoom`), 이미지+계측만 transform, Grid 고정·Ruler 위치 고정·단위 배율 반영. Section 9뷰는 단일 transform 함께(각 타일 중앙 기준·§D27). 감도·제스처는 접목 시 CW MPR interactor 정합 확인.

### 3.8 Pointer 주석 도구 (MMI 1.13-1a Pointer — CW PointerDialog/PointerCanvas 정본)

MMI 1.13-1a Pointer는 **일시 주석(임시 그리기)** 도구다. **동작·UI는 CW `PointerDialog`/`PointerCanvas`가 정본**이며, 본 모듈은 이를 **소스 그대로 포트**한다(접목 시 CW 것으로 대체 — §9.10). CW 조사(2026-07-15): 순수 React + Canvas 2D(`Path2D`), **vtk 의존 없음**.

**동작(CW 1:1):**
- Pointer 버튼 클릭 → **Pointer 모드** 진입(`interaction='pointer'`). 다른 상호작용(pan/zoom/계측/커브)은 정지하고 **컨트롤 다이얼로그**가 열린다. 진입 시 기본 **Pen** 모드.
- **드로잉:** Free Draw처럼 마우스 드래그로 자유곡선. **3뷰 전체를 덮는 단일 오버레이 캔버스**에 그린다(뷰 구분 없이 어디나). **여러 개 요소**를 만들 수 있다(획 1개 = 요소 1개, `Path2D`).
- **Eraser:** 다이얼로그에서 Eraser 선택 → 지우개 커서. 그려진 요소를 **클릭하면 그 요소 하나 삭제**(`ctx.isPointInStroke`, 관용 두께 15px hit-test).
- **선 두께:** 1~5, **기본 2**(드롭다운). **색상:** 단일 컬러버튼(현재 색) → 팝오버 스와치+커스텀. **기본 노랑 `#FFD64A`**(CW settings `annotation.pointer.color` 실제 기본값). **Reset:** 모든 그림 삭제.
- **모달 차단(중요):** Pointer 모드 동안 **Toolbar·다른 버튼·뷰 조작이 일절 동작하지 않는다.** 전체 화면 backdrop이 뒤의 모든 UI 클릭을 막는다(모달). **종료는 다이얼로그 Close(X)로만** — Toolbar Pointer 버튼 재클릭으로 끄는 경로는 없다(가려짐).
- **그리기 범위 = 뷰(본문)만:** 드로잉 캔버스는 **본문(3뷰) 영역에만** 겹친다 → **Toolbar·패널 위에는 그려지지 않는다**(CW 정합; backdrop이 그 영역을 덮어 클릭만 차단). 본문 rect를 추적해 캔버스를 그 위에만 배치.
- **Close:** 다이얼로그 닫기 = **interaction 해제** → 오버레이 캔버스 언마운트로 **그동안의 모든 그림 소거**(즉 Reset 후 close). 재진입 시 빈 캔버스·Pen 시작.
- **커서(CW 정본):** Pen = `CURSORS.POINTER`(핫스팟 7,6, 기보유), Eraser = `CURSORS.ERASE`(핫스팟 6,24, 신규 복사 — §9.5). 자기완결 base64 SVG.
- **저장 안 됨:** Pointer 그림은 **임시**(prj 저장 대상 아님, CW 툴팁 "The lines are not saved"). MMI 1.14 저장 항목(§7)에도 미포함.

**소유(중요):** Pointer는 **CW 워크스페이스(셸) 레벨** 기능이다 — CW `WorkSpace`가 `interaction==='pointer'`에서 전역 `PointerDialog`/`PointerCanvas`를 직접 렌더한다(Section content가 기여하지 않음, Save Project와 유사한 셸 소유). 따라서 **접목 시 우리 포트는 삭제**하고 CW WorkSpace가 그대로 제공한다. 우리 포트는 **standalone 데모 파리티용**일 뿐이다.

**구현(T-P4-8, 완료):** `packages/components`에 `PointerCanvas`(드로잉·Eraser·Reset ref)·`PointerDialog`(Pen/Eraser/두께/단일 컬러버튼+팝오버/Reset/Close) 포트. App이 `interaction==='pointer'`에서 **전체 화면 모달 레이어(zIndex 1000)** = backdrop(뒤 UI 차단) + **본문 rect에만 겹치는** 드로잉 캔버스 + 다이얼로그. 기본색 `#FFDD40`. **CW는 react-rnd·react-color(SketchPicker)·MUI 사용**하나 본 포트는 의존성 최소화를 위해 **경량 드래그 + 컬러버튼 스와치 팝오버**로 대체(닫힌 다이얼로그 레이아웃·색·동작은 근접; 그라디언트 picker만 미복제). **1안 채택(2026-07-16):** verbatim 복제(2안)는 react-rnd·react-color를 들여왔다가 접목 시 다시 버리는 낭비라, **경량 포트 유지 + 접목 시 CW 컴포넌트로 대체**(§9.10). 픽셀 동일 picker가 데모에 필요하면 그때 react-color 추가.

### 3.9 계측/주석 편집 (Edit · Property) — CW 정합

length·angle·freeDraw·arrow 계측/주석은 **생성 후 편집**할 수 있다(CW `es-pixi-wrapper` 정합; CW는 PIXI, 우리는 Canvas 2D에 동일 UX 이식). **도구 미선택(neutral) 상태에서 동작**한다(그리기 도구 활성 시 편집 비활성).

**선택 규칙(단일 선택 · CW 정합):** 한 번에 **하나만** 선택된다. 선택 해제는 ① **다른 주석 선택**, 또는 ② **빈 배경 클릭(좌/우 버튼 모두)** — 주석이 아닌 뷰 배경을 클릭하면 해제된다.

**좌클릭:**
- 주석 선 위 hover → **이동 커서**(CW `overlaySelectedCursor` = 화살표+십자, §3.4.2). 선을 드래그하면 **통째 이동**(모든 점 같은 delta, 타일 밖으로 안 나가게 clamp).
- 선택되면 각 점이 **속 빈 네모 핸들**(색=선색)로 표시되고, 핸들을 드래그하면 그 점만 이동 → **길이·각도 실시간 갱신**. **length·angle·arrow**에 적용.
- **FreeDraw는 점별 핸들 없음(CW `FreedrawOverlay` 정합)** — 점이 많아 per-point 편집이 번잡하므로 CW처럼 **선택 시 선을 굵게** 표시하고 **통째 이동·Property·Delete만** 지원(점 편집 없음).

**우클릭:** 주석 위에서 → **편집 진입 + 컨텍스트 메뉴**(흰 바탕·검정 글씨, CW `CustomMenu` 정합):
- **Property** → Property 다이얼로그(**Line Color · Font Color · Font Size**[6·8·10·12·14·16·18·20] · Save/Cancel). **선색을 바꾸면 핸들 색도 함께** 바뀐다.
- **Delete** → 해당 주석 삭제.
- (구현 주의) 우클릭은 `mousedown button===2`가 아니라 **`contextmenu` 이벤트**로 처리한다 — Mac control-click은 mousedown button이 0이라 button 검사로는 놓친다.

**저장:** 편집된 점 + 스타일(선색·글자색·글자크기)은 **계측 모델 `style`**(`measurement.ts`)에 담겨 **Save Project ⑨(Overlay, §7·§12-D26·T-P5-4)** 로 저장된다.

**모드 충돌 회피(중요 · hover 기반 캡처):** 편집 오버레이는 뷰 전체를 덮지만, **실제로 주석 위(hover)이거나·주석을 드래그 중이거나·컨텍스트 메뉴가 열렸을 때만** 입력을 캡처(`pointerEvents:auto`)한다. **빈 영역이나 뷰 고유 요소(커브·section line·Panorama 상하 경계선/중앙선) 위에서는 캡처하지 않아**(`pointerEvents:none`) 뷰 고유 조작이 그대로 동작한다. hover 판정은 **window `mousemove`**로 하여 `pointerEvents:none`인 동안에도 주석 진입 순간을 잡는다. (초기에는 "계측이 하나라도 있으면 뷰 전체 캡처" 방식이었으나, 이 방식은 **주석이 있으면 Panorama 상하 경계선(섹션 높이)·중앙선 드래그, Scout 조작 등 뷰 고유 neutral 조작을 막는 회귀**를 유발 → 2026-07-16 hover 기반으로 교체.) **Pan/Zoom·Pointer·Curve Draw/Edit 활성 시에는 오버레이를 `disabled`**(각 뷰가 `navTool`/curve 상태로 판정)로 그 모드가 우선이다.

**구현(T-P4-9, 완료):** `SectionMeasureOverlay`에 편집 상태(selectedId·핸들 드래그·이동·컨텍스트 메뉴)·hit-test(선분 거리·핸들)·스타일 렌더(선색/글자색/글자크기·속빈 네모 핸들) 추가. 우클릭 메뉴는 `onContextMenu`, 좌클릭 선택·드래그는 `onMouseDown/Move/Up`. hover 캡처는 window `mousemove`가 `editCapture`를, 드래그 지속은 `annDragging`이 담당(`captured = active || menu || annDragging || (canEdit && editCapture)`). `AnnotationPropertyDialog`(CW `OverlayPropertyDialog` 포트, 경량). 커서 `MOVE`(CW `overlaySelectedCursor`) `cursors.ts`에 복사. **접목 시** 편집·Property·메뉴는 CW `es-pixi-wrapper`/`OverlayPropertyDialog`/`CustomMenu` 정본으로 교체(§9.10).

### 3.10 초기화 명령 (Reset Cloud Work · Initialize All) — CW 소유

MMI 1.13-1a 툴바의 두 command형 초기화 버튼. **둘 다 CW 정본**(`packages/core/src/workSpace/content/handler/*.ContentHandler`)이며, 클라우드 영속(metadata)·`reloadState`·`refApis` 등 **CW 워크스페이스(셸) 인프라에 의존**한다. 따라서 Save Project·Pointer와 마찬가지로 **CW 셸 소유 기능**이다(§3.8 소유 논리 동일). 아래는 CW 소스에서 확인한 정확한 의미(2026-07-16):

| 명령 | CW 동작(정본) | 성격 |
|------|------|------|
| **Initialize All** (`initializeAll`) | ① pending 메타 업로드 취소 → ② `refApis.initializeAll()` → ③ 초기화된 메타 재업로드(lazy). **②의 실제 내용(MPR/CT 정본 = `CTViewerControllerCore.initializeAll`, Section이 MPR 계열이라 이게 기준):** ⓐ MPR axis widget `reset()`, ⓑ **overlay(주석) 전부 `clear()`**, ⓒ **VR/windowing 속성을 CT 뷰 setting 기본값으로 `initialize()`**(WL 등 리셋), ⓓ **`viewHandler.resetView()`**(pan/zoom·카메라 리셋), ⓔ **`reloadDefaultProjectFile()`** — **default project file로 되돌림**, ⓕ 전 뷰 렌더. (2D 콘텐츠는 PixiWrapper `ActionType.InitializeAll`로 오버레이 초기화 후 Select 복귀.) **= 현재 세션 작업을 버리고 default 상태로(클라이언트).** | 편집 권한 필요(`requiresEditControl:true`) |
| **Reset Cloud Work** (`resetCloudWork`) | ① `setLoading` → ② **Initialize All 수행** → ③ `await resetMetaData()`(**클라우드에 저장된 작업(메타) 리셋**) → ④ `reloadState.requestReload({toolId:'resetCloudWork'})`(**콘텐츠 전체 리로드**). 2D는 `refApis.clear()`도 호출. **= 저장분까지 폐기하고 원본에서 리로드(더 강한 초기화).** | 편집 권한 필요(`requiresEditControl:true`) |

**차이 요약:** *Initialize All* = 현재 세션 작업을 버리고 **default project file 상태로**(클라이언트, 저장분 미삭제). *Reset Cloud Work* = 그 위에 **클라우드 저장분 리셋 + 리로드**까지(서버 영속 폐기). 둘 다 **편집 권한(edit control)** 이 있어야 활성.

**기준(어디로 돌아가는가) — 중요, MMI 미명시:** MMI 1.13-1a는 버튼만 나열할 뿐 **초기화 기준을 정의하지 않는다.** CW 소스 기준으로 답은 **"default project file 상태"**(위 ⓔ)다. 즉 **"파노라마 생성 전/후"가 기준이 아니다** — 파노라마·3×3 섹션은 저장/체크포인트가 아니라 **Curve에서 파생(재구성)** 되는 결과물이기 때문이다. Initialize All은 **Curve(및 레이아웃·WL·뷰)를 default로 되돌리고**, 파생물(파노라마·섹션)은 그 default Curve로부터 **다시 계산**된다. 따라서 결과 화면은:
- **default project file에 Curve가 정의돼 있으면** → 그 default Curve 기준으로 파노라마·섹션이 재생성된 상태(사용자가 편집한 Curve가 아니라 **default Curve**).
- **default에 Curve가 없으면** → **blank**(Curve 없음 → 파노라마·섹션 없음). MMI 1.14가 "proj Curve 없으면 blank"라 한 것과 동일 개념.

**소유·구현 가능 여부(중요, 명확 구분):**
- **Initialize All = 우리도 구현한다(클라이언트, 완료 T-P5-5). MMI 미정의 → 아래로 정의(§3.4.2·§12-D30).**
  **"데이터·값"은 default로 초기화하되 "모드·토글"은 유지**한다(CW 정합, 2026-07-16 사용자 확인):
  - **초기화(default/제거)**:
    - **Curve** 제거 → 파노라마·섹션 **blank**(Curve 파생물이라 재계산할 원본이 없음)
    - **계측(주석) 전부 제거**(뷰별 measurements 비움) — overlay "데이터"
    - **Pan/Zoom 값(view transform)** → identity(모든 뷰) — "값"은 리셋
    - **WL** → 볼륨 기본값(DICOM), **Image Filter/Inverse** → 기본, 투영 → mean
    - **섹션·파노라마·Scout 파라미터**(두께/간격/폭/높이·B/L 극성·기준점·center) → 기본, scout slice → 중앙
  - **유지(바뀌지 않음)**:
    - **활성 도구/interaction**(예: Zoom 도구 선택 상태) — "모드"는 유지
    - **Show/Hide Overlay 토글**(overlay "모드") · **Show/Hide Grid 토글** — 셸(toolStore) 소유라 손대지 않음
  - **결과(중요):** Curve가 사라지므로 **CT 최초 로드 직후와 동일하게 Scout 뷰만(그것도 커브 없는 축 영상만) 보이고 파노라마·섹션은 비어 있다.** MPR은 3D라 초기화 후에도 축/관상/시상 단면을 보여줄 게 있지만, **본 Section 모듈은 Curve가 있어야 파노라마·섹션이 생기므로 초기화 시 보여줄 파생 영상이 없다**(정상 동작).
  - **재오픈 복원(저장본)과 별개**: Initialize All은 **저장본(localStorage/클라우드)을 지우지 않고 세션 데이터만 clean**한다 → 재오픈하면 저장본이 다시 복원된다(reopen=메타 로드 vs Initialize All=default 로드, CW 정합). 저장본까지 지우는 건 Reset Cloud Work(셸 소유·우리 미구현).
  - **(정정 이력)** "default=오픈 시 로드본"·"모드까지 OFF"라던 초기 서술은 각각 재오픈 복원/CW 동작과 혼동한 것이라 2026-07-16 위와 같이 정정.
- **Reset Cloud Work = 우리가 구현할 수 없다(CW/호스트 인프라 의존).** `resetMetaData()`는 `ioApis.resetMetaData('CT', id)`(=CW 호스트가 `ExternalAPIFactory`로 주입하는 **클라우드 서버 IO** — 저장 메타를 서버에서 리셋)를 호출하고, 이어 `reloadState.requestReload()`(=**CW 워크스페이스 콘텐츠 리로드 파이프라인**)를 탄다. 둘 다 standalone 모듈에 존재하지 않는 CW/호스트 계층이라 **대체 구현 불가.** 따라서 **본 모듈은 구현하지 않고 접목 시 CW가 제공**하며, **POC에서 이 버튼을 누르면 "추후 CW 접목 시 지원됩니다" 안내**(toast/알림)만 표시한다(로컬 Initialize All로 대체하지 **않음** — 의미가 다름: 서버 저장분 폐기·리로드).

**현재 상태(POC)·구현 완료(2026-07-16, T-P5-5):** **Initialize All 배선 완료** — 클릭 시 `SectionViewer.initializeAll()`가 **데이터만 default로**(Curve/계측/WL/섹션·파노라마 파라미터) 리셋, **뷰 모드(Zoom/pan·Overlay·Grid·도구)는 유지**(CW 정합). `toolStore` tick(`initializeAll`/`resetCloudWork`) + `CwToolbar` commandHandler + App effect로 구동. **Reset Cloud Work는 미구현 확정 → 클릭 시 "접목 시 지원" 안내 다이얼로그만**(상태 불변), 실제 클라우드 리셋·리로드는 **접목 시 CW 소유**(§9.10). (Reset View는 §3.7.)

### 3.11 국제화(i18n) 지원 — 한/영(en·ko) 통일 (2026-07-16 회의 확정)

**스펙 요구사항(확정 · §12-D23):** 본 모듈을 포함한 **3개 제품(CleverSpace·CW·Section)의 지원 언어를 한/영 `en_US`·`ko_KR` 2종으로 통일**하고, **CleverSpace(호스트) 연동으로 국제화를 적용**한다. (현황·불일치 배경·근거는 §9.11-CW-2 참조 — 여기서는 우리 모듈이 만족해야 할 요구를 규정한다.)

**요구 상세:**
1. **i18n 프레임워크 = Lingui(CW 정합).** 본 모듈은 현재 i18n 미적용·한/영 문자열 하드코딩 혼재 상태 → **모든 UI 문자열을 `t\`\`` 매크로로 외부화**하고 **`en_US`·`ko_KR` 카탈로그**를 제공한다. `@lingui/react`는 접목 시 CW/호스트와 **federation shared**로 공유(§9.3).
2. **선행: UI 문자열 한국어 통일.** 현재 "Draw Curve"·"Curve 1" 등 영어와 "취소"·"Section 생성 중…" 등 한국어가 혼재 → **한국어 기준으로 통일**한 뒤 카탈로그화(혼재 제거가 1차 목표).
3. **Locale 선택은 CleverSpace(호스트) 소유.** 언어 변경 UI는 호스트가 제공하며, 본 모듈·CW는 **호스트의 활성 locale(`en_US`/`ko_KR`)을 구독**해 따른다(자체 언어 선택 UI 없음). 접목 시 CW `useBoundStore i18nStore` locale 구독에 배선.
4. **지원 언어는 정확히 en/ko 2종.** 그 외(CW의 `es`/`fr`/`pt`)는 **비지원**(CleverSpace에서 선택 불가) — 우리 카탈로그에 추가하지 않는다. CW 측 `ko_KR` 채우기·`es`/`fr`/`pt` 정리는 **CW 팀 권고**(우리 범위 밖, §9.11-CW-2).

**범위·소유:** 문자열 외부화·카탈로그는 **본 모듈 소유**(우리 컴포넌트/코어 문자열). locale 선택·전역 i18n provider 배선은 **호스트(CleverSpace)/CW 셸 소유** — 접목 시 그쪽 provider 아래에서 우리 카탈로그가 활성화된다.

**구현:** IP **T-P4-7**(회의 결정 완료·착수 가능). DoD: 문자열 한국어 통일(혼재 제거)·Lingui 구조로 locale 전환 시 en/ko 반영.

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

**소유·기여 구조(중요):** Save Project는 **우리 모듈 기능이 아니라 상위(CleverSpace 컨테이너 + api-server) 소유**다 — Save 버튼("Your changes have been saved" 다이얼로그)·저장 flow·**`.e3prj` XML 직렬화**·**S3 저장/로드**(api-server `*.e3prj`)는 호스트가 처리한다. **각 Content는 `ContentHandler`를 통해 자기 데이터를 prj에 기여**한다(CW `CTContentHandler`가 `projectData`(CurveList/SectionInfo/PanoInfo)를 read/write). → **우리 Section 모듈의 역할 = Section 상태를 prj 필드로 직렬화/역직렬화해 상위 save에 기여**(Save 자체를 구현하지 않음). 접목 시 `SectionContentHandler`(§9.5·9.7)가 상위 save/load 훅에서 core `serializeProject`/`deserializeProject` 결과를 CW `projectFile.ts` 필드에 매핑한다(D5).

**저장 항목 대조표 (MMI 1.14-c ①~⑫ ↔ 소유·모델 필드·상태, 2026-07-15):** 회전 각도는 삭제(§11 이월). 소유 = **모듈**(우리 payload에 직렬화) / **셸**(CleverSpace 컨테이너·CW 워크스페이스가 저장, 모듈 payload 아님).

| # | MMI 1.14 저장 항목 | 소유 | 저장 모델 필드(`SectionProjectState`) | 상태 |
|---|---|------|------|------|
| ① | 마지막 레이아웃 (MPR / Section) | **셸** | — (CW 컨테이너 소유) | 셸 저장 |
| ② | 각 단면 View 위치 (slice·Active section line) | 모듈 | `scout.sliceIndex`·`section.centerMm`(Active line)·`panorama.navigatorOffsetMm` | ✅ 보유 |
| ③ | 각 단면 카메라 상태 (Position·Panning) — **우리에겐 뷰별 Pan/Zoom**(3D 카메라 없음, §D25) | 모듈 | **미보유 → 추가 필요**(뷰별 pan offset·zoom) | ⚠ 갭 — T-P4-6 **완료**, T-P5-4에서 추가 |
| ④ | ShowGrid 표시 여부 (+Overlay 가시성) | **셸** | — (CW `workspaceViewFeatures` 소유; 모듈은 표시 반영) | 셸 저장(§12-D24). **데모는 별도 키로 저장·복원**(파리티) |
| ⑤ | Section Curve (Point 좌표) | 모듈 | `curve.controlPoints` | ✅ 보유 |
| ⑥ | Panorama 가로선 위치 (이미지 경계선) | 모듈 | `section.topMm`·`section.bottomMm`(상하 Z 경계, 파노라마 경계선과 공유) | ✅ 보유 |
| ⑦ | Panorama 중심선 위치 | 모듈 | `panorama.navigatorOffsetMm`(B/L navigator) | ✅ 보유 |
| ⑧ | 각 단면 Thickness / Interval | 모듈 | `scout`·`panorama`·`section`의 `thicknessMm`·`intervalMm` | ✅ 보유 |
| ⑨ | 각 단면 Overlay 입력값 (Length·Angle·Arrow·FreeDraw) | 모듈 | **미보유 → 추가 필요**(`measurements[]`, `core/measure/measurement.ts` 모델 재사용, 뷰·slice/arc 앵커 포함) | ⚠ 갭 |
| ⑩ | 각 단면 Windowing / Image Filter | 모듈 | `imaging.{windowCenter,windowWidth,filterMode,inverse,projection}` | ✅ 보유 |
| ⑪ | B/L Switching 상태 | 모듈 | `curve.blPolarity` | ✅ 보유 |
| ⑫ | BL/LB 기준점 위치 | 모듈 | `curve.blRefArcMm` | ✅ 보유 |

> **갭 정리:** 모듈 저장 모델(`SectionProjectState`)은 ⑤·⑪·⑫(curve), ②·⑥·⑦(위치), ⑧(thickness/interval), ⑩(windowing/filter)을 보유. **미보유 2건**: **③ 카메라(pan/zoom)** — Pan/Zoom 자체가 미구현이라 **T-P4-6 완료 후** 뷰별 카메라 필드 추가(§12-D25); **⑨ Overlay 계측** — 계측 로직·모델(`measurement.ts`)은 구현됐으나 저장 모델에 미포함 → `measurements[]` 필드 추가(§12-D26). **셸 소유 2건**: ① 레이아웃·④ ShowGrid는 CW 컨테이너/워크스페이스가 저장(우리 payload 아님, §12-D24).
- **호환(§12-D5 확정):** 최종 직렬화는 **CW prj(XML)와 호환**되게 한다. CW prj는 `vtkjs-wrapper/projectFile.ts`가 소유하며 **`CurveList`·`CurveInfo`·`SectionInfo`·`PanoInfo`·`SectionalPos`·`SectionInterval`·`SectionalNum`·`AutoCurveInfo` 필드가 이미 존재**하므로, Section 저장 항목은 **자유 설계가 아니라 이 필드에 매핑**한다. 좌표계는 환자 볼륨 3D(§4). 호환 방향은 Desktop→Web 단방향 우선(개발실 §4.1).
- **개발 중 임시 저장(시뮬레이션 방침, 2026-07-15):** 실제 prj 파일 I/O·S3는 상위 몫이므로, 데모는 **`localStorage`(또는 export/import)로 저장/로드**를 시뮬레이션한다. **단, 저장 내용은 `.e3prj` 전체가 아니라 우리가 기여하는 "Section 조각"** 이다 — `.e3prj`엔 호스트 소유 필드(레이아웃·카메라·환자·타 content)가 대부분이라 전체를 지어내면 실제와 어긋난다. 따라서:
  - **core `SectionProjectState`(순수 모델) 유지** + **어댑터로 CW prj 필드 형태(`CurveList`·`SectionInfo{Width,Height,Interval,Thickness}`·`PanoInfo`, `projectFile.ts` 정본)로 변환** — 이 어댑터가 접목 시 기여 지점이자 매핑(D5) 검증 대상.
  - 데모는 그 **CW 필드 형태의 Section 조각**을 localStorage에 round-trip. **포맷은 객체(JSON)로 충분**(CW `projectFile.ts`도 객체(XML-attr 키 `@_…`), 객체↔XML 직렬화는 호스트 몫 — 우리 책임은 "필드 객체 산출"). 필요 시 **`.e3prj` XML 미리보기(export)** 로 실제 파일 모양 확인.
  - 접목 시 **저장 계층만 호스트 I/O로 교체**하고, 우리 조각은 `SectionContentHandler`가 상위 prj에 병합.
- **데모 완전 Save 흐름 — 구현 완료(2026-07-16, T-P5-2·3·4):** Save 버튼 → `SectionViewer` ref `getProjectState()`로 상태 수집 → **CT별 키(`ctStorageKey`=PatientID+StudyDate)로 localStorage 저장** → **CW `MessageDialog` 파리티**(로딩 스피너 → "Your changes have been saved." + teal OK, `cw/MessageDialog.tsx`; CW `ContentTitleBar` `openMessageDialog` 흐름 정합, 접목 시 CW 셸 소유로 교체) → **동일 CT 재오픈 시 자동 로드·`applyProjectState` 적용**. 저장 대상 = §7 ①~⑫ 중 모듈 소유 항목(curve·section·pano·windowing·계측⑨·뷰별 Pan/Zoom③).
- **구현 노트(2026-07-16 구현 반영):**
  - **저장 상태 소재·수집:** 라이브 상태는 `SectionViewer`의 `useScoutAxialUi`(slice·thickness·interval·window·filter·section·pano)·`useCurveEditor`(controlPoints·blPolarity·blRefArcMm·sectionInterval)에 있고, **계측·뷰별 Pan/Zoom은 `useScoutAxialUi`로 공유 승격**(`measurements`/`viewTransforms` + 안정 dispatcher, `SectionMeasureOverlay`·`useViewTransform`이 이를 사용). `SectionViewer`가 **`forwardRef`+`useImperativeHandle`로 `getProjectState()`/`applyProjectState()` 노출**(수집·복원). ShowGrid·interaction은 `toolStore`(셸 소유, ④ 근거).
  - **CT 식별 키:** `VolumeMetadata`에 Series/Study UID가 없어(현 `CTVolumeLoader` 미파싱) **PatientID+StudyDate 폴백**(`ctStorageKey`)을 사용. UID 도입 시 그쪽 우선으로 승격 가능(향후).
  - **재오픈 자동 복원:** App effect가 volume 로드 시 CT 키로 저장본 조회 → `applyProjectState` 적용(없으면 blank). App(부모) effect가 `SectionViewer`/`useCurveEditor`의 볼륨-리셋(자식) 뒤 실행돼 복원이 우선한다.
- **범위:** Section 모듈 = **Section 상태 serialize/deserialize + prj 필드 매핑 어댑터 + `SectionContentHandler`의 save/load 기여** + 개발용 임시 저장. **Save 버튼·flow·`.e3prj` XML I/O·S3 저장·자동저장·Desktop→Web 업로드 = 상위(CleverSpace 컨테이너 + api-server) 몫.** (근거: ezcloud `api-server`(`*.e3prj` S3), CW `CTContentHandler`(`projectData` read/write)·`projectFile.ts`.)

## 8. NFR (성능·환경)

| 항목 | 기준 |
|------|------|
| 9단면 생성 | 얇은 단면 측정 JS 평균 **393ms**(362~427). **두꺼운 슬랩(Th 30mm) worst-case: JS mean 1484ms·max 1787ms / WASM-resident mean 1225ms·max 1336ms**(T-P6-1, 2026-07-15). WASM이 두꺼운 슬랩에선 JS 대비 mean −17%·max −25%·저분산(얇은 단면에선 이점 제한적) |
| Section Slice 스크롤 | 30 FPS(**33ms**) 미달 = 최대 리스크. **측정(T-P6-1): CPU 경로 두꺼운 슬랩 재생성 1.2~1.8s로 예산의 ~40~54× 초과** → CPU만으로 두꺼운 슬랩 실시간 스크롤 불가. **완충책(디바운스 ≥48ms·캐싱[재방문 slice ~72ms]·표시 분리[이전 이미지 유지]·Thickness 상한 30mm)으로 체감 보전**, 실시간 리슬라이스는 **WebGL2 GPU 경로**(§8 채택안)·필요 시 프리페치. 얇은 단면(≤2mm) 스크롤 수치는 보강 측정 예정. 상세 `docs/benchmark-section-scroll.md`(poc) (§12-D7) |
| Thickness 0mm | `slabHalfWidthMm=0` 경로 검증(현 기본 half 3mm=full 6mm). 상한 **30mm — combo·드래그 공통**(단일 `MAX_THICKNESS_MM`, §12-D8) |
| 입력 | v1.3.2 **마우스 전용**(모바일/터치 스펙아웃) |
| 브라우저·메모리 | Chrome 기준. CT 볼륨 100~250MB 수용. WebGL Context 3개 전략(CONTEXT_LOST 방지) |
| 계측 로그 | `SectionGen` JSON 한 줄(`{tag,mode,ms}`) 벤치마크 수집 |

## 9. CloudWebViewer 접목 정합 (핵심)

> "접목 용이성"의 핵심 절. 인용 경로는 `~/Documents/Azure/cloudwebviewer` 기준(2026-07-13 조사).

### 9.1 접목 원칙 — Section(WebGL)만 구현, VTK 미접목

**Section 모듈은 CW의 vtk 파이프라인(`Layout3DPAN`, `VolumeSectionView` 등)을 사용·구현하지 않는다(§12-D1).** Section 뷰는 poc의 WebGL 구현을 확장하며, 접목은 CW가 이 **WebGL Section 컴포넌트를 CW content로 embed**하는 방식이다. 따라서 정합 대상은 CW의 **셸 계약**(환경·툴바 store·content·타이틀 바·prj)이지 vtk 뷰가 아니다.

> 참고: CW엔 Section용 레이아웃 슬롯(`CTViewerLayout.Layout3DPAN`)과 vtk 뷰 **스텁**(각 ~25줄, 빈 상속)이 있으나 본 모듈 범위 밖이다. embed 시 CW는 이 슬롯 대신 우리 컴포넌트를 새 content로 연결한다(§9.7).

### 9.2 접목 형태 — 소스 병합(권장) vs 패키지 (§12-D4)

**권장 = CW 모노레포로 소스 이동 병합.** 별도 npm publish/Federation remote가 아니라, `scp-section-poc`의 소스를 CW 모노레포(`cloudwebviewer`)로 옮겨 **단일 빌드·단일 버전**으로 관리한다. 근거(2026-07-15 D4 개정):

- **이미 결합도가 높다.** Section 모듈은 CW 내부(`ContentHandler`·`useBoundStore` zustand singleton·`ContentTitleBar`·`ImageAdjustDialog`·`CTSliceSettingDialog`)를 깊게 재사용하고, `InteractionType`에 `arrow`를 **CW 측에 추가**해야 한다(§9.5~9.7). 패키지 경계가 사실상 의미가 없다.
- **소비자가 CW 하나뿐.** 여러 host가 소비하지 않으므로 private registry·`.npmrc`·변경마다 republish 마찰의 이점이 없고, Federation `shared`(react·zustand) singleton 버전 불일치 런타임 버그 위험만 남는다.
- **소유권·진화.** 접목 후 CW 팀이 한 코드베이스로 소유하고, API를 cross-repo 버전 범프 없이 함께 리팩터한다.

**단, 순수 코어는 CW 내부 워크스페이스 패키지로 유지한다.** `scp-section-core`(Catmull-Rom·trilinear·slab·prj 직렬화 등 프레임워크 독립 로직)는 CW `packages/`에 **publish하지 않는 내부 패키지**로 넣어 단일 버전·마찰 제로를 유지하면서 **WebGL/React 없이 단위 테스트 가능**하게 남긴다. React 뷰(`components`)는 CW 컴포넌트 트리에 병합한다. 구체 절차는 **§9.9**.

**대안(패키지/Federation):** 접목을 미루고 독립 평가만 할 때(또는 여러 host 소비가 생길 때)는 `@ewoosoft/scp-section-*` 패키지 + Federation remote로 제공할 수 있다. 이때 공개 API는 CW store·toolbar·prj와 배선 가능하도록 설계한다(§10: `volume`·`curve`·`blPolarity`·active `interaction`·이벤트 콜백). **현 결정은 소스 병합 우선**이며 패키지는 fallback이다.

### 9.3 환경 일치 (버전)

poc가 CW와 look&feel·의존성이 맞도록 major/정확 버전 정합. 구현 착수 전 게이트.

| 항목 | cloudwebviewer | scp-section-poc(현재) | 목표 |
|------|------|------|------|
| Node / pnpm | 20.x / **9.15.9** | ≥18 / 9.1.1 | 20.x / **9.15.9** |
| React / TS / Vite | 18.2 / 5.2.2 / 5.0.8 | ^18 / ^5 / **6.0** | 18.2 / 5.2 / **5.0** |
| MUI / Emotion / zustand | 5.15 / 11.11 / 4.4.7(+immer) | 없음 | 동일 major |
| registry | `.npmrc` Azure DevOps `@ewoosoft` private | 없음 | **소스 병합 시 불필요**(publish 안 함, §9.2). 패키지 fallback 시에만 `.npmrc` 스코프 인증 |
| Federation | `@originjs/vite-plugin-federation` ^1.3, `shared: react·react-dom·zustand·@lingui/react` | 없음 | **소스 병합 시 불필요**(remote 아님). 패키지 fallback 시에만 shared 버전 정합 |
| 패키지 스코프 | `@cloudwebviewer/*` | `@ewoosoft/scp-section-*` | **병합 시 `@cloudwebviewer/section-core`·`@cloudwebviewer/section`으로 개명**(§9.9 1b). 패키지 fallback 시 `@ewoosoft/*` 유지 |

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

### 9.9 접목 실행 절차 (Step-by-step, CW 개발자용)

§9.1~9.8이 "무엇을 무엇에 맞추는가"(정합 대상)라면, 이 절은 **CW 팀이 실제로 어떤 순서로 무엇을 하면 embed되는가**를 구체 단계로 기술한다. 각 단계는 위 절의 근거를 참조한다.

**0단계 — 전제.** Section 모듈은 CW의 vtk 파이프라인을 쓰지 않고, **`SectionViewer` React 컴포넌트를 CW content로 embed**하는 방식이다(§9.1). CW가 손대는 것은 셸 계약(store·toolbar·content·title bar·prj)뿐이며 Section 내부 렌더(WebGL)는 블랙박스다.

**1단계 — 소스 병합(§9.2 권장안).** `scp-section-poc` 소스를 CW 모노레포(`cloudwebviewer`, pnpm@9.15.9·`packages/*`·`types/*`·`lib/*`·스코프 `@cloudwebviewer/*`)로 이동한다. **core는 내부 패키지 유지, components는 CW 트리에 병합**한다.

1a. **디렉터리 이동.** PoC의 `packages/core`·`packages/components`·`packages/section-wasm`를 CW `packages/` 아래로 옮긴다. 권장 배치:
   - `packages/section-core/`  ← `scp-section-core`(순수 로직·dicom·webgl·curve·panorama·section·직렬화). **내부 패키지**(publish 안 함).
   - `packages/section/`       ← `scp-section-components`(React 뷰 `SectionViewer`·`ScoutView`…·`SectionContentHandler`). `@cloudwebviewer/core`·`section-core`에 의존.
   - `packages/section-wasm/`  ← WASM 빌드(그대로 이동, 또는 `section-core`에 흡수).

1b. **패키지 스코프·이름 변경.** `@ewoosoft/scp-section-core`→`@cloudwebviewer/section-core`, `@ewoosoft/scp-section-components`→`@cloudwebviewer/section`. 각 `package.json` `name`과 **모든 import 경로**를 일괄 치환. CW `pnpm-workspace.yaml`은 이미 `packages/*`를 포함하므로 자동 인식(수정 불필요).

1c. **의존성 정리.** PoC의 React·zustand·MUI·Emotion·lingui 버전을 CW 버전(React 18.2·zustand 4.4.7·MUI 5.15 등, §9.3)에 맞춰 `package.json`에서 제거·정렬 → CW 루트가 단일 버전으로 hoist. **중복 명시 금지**(singleton 보장).

1d. **빌드·테스트 편입.** CW `turbo`/빌드 파이프라인에 `section-core`·`section` 빌드 태스크 추가. `section-core`의 단위 테스트(vitest)는 CW 테스트 스위트에 편입해 **프레임워크 독립 검증 유지**(WebGL/React 불필요).

1e. **데모 셸 분리.** PoC `apps/section-demo`(및 데모 전용 `cw/` stub 툴바·`App.tsx` 3층 셸)는 **이동하지 않는다.** CW가 자체 Toolbar·Content·TitleBar를 제공하므로(3~7단계), 데모 셸은 `scp-section-poc` repo에 남겨 접목 전 레퍼런스로만 유지(§Resource 「저장소·데모 사이트」).

**2단계 — 환경 게이트(§9.3).** 소스 병합이므로 버전은 CW 루트로 hoist되지만, 착수 전 정합을 확인한다: Node 20.x/pnpm 9.15.9, React 18.2/TS 5.2/Vite 5.0, MUI 5.15/Emotion 11/zustand 4.4.7. **zustand·react는 CW 루트 단일 버전으로 hoist**되어 singleton 보장(1c에서 하위 패키지 중복 명시 제거). 불일치 시 이 단계에서 차단.

**3단계 — Content 등록(§9.4·§9.5·§9.7).** CW의 content 시스템에 Section을 붙인다:
1. `SectionContentHandler`를 `ContentHandler`(추상) 상속으로 작성 — 내부에 `SectionViewer` ref를 들고, `changeInteraction`·`showOverlay`·`showGrid`를 컴포넌트 API로 중계.
2. `ContentHandlerFactory.addHandler(...)`로 Section 핸들러 등록.
3. `ContentDialog`의 `contentType` 분기에 Section 케이스 추가 → 해당 슬롯에서 `SectionContentHandler`가 `SectionViewer`를 렌더. (CW의 `Layout3DPAN` vtk 스텁 슬롯은 쓰지 않고 새 content로 연결, §9.1 참고.)

**4단계 — Store 배선(§9.5·§9.6).** Section 상태가 필요하면 `ISectionSlice`를 CW `RootStoreState`에 `ImmerStateCreator<T>` 동일 시그니처로 병합(`store/index.ts`). toolbar/workspace slice는 **재구현 금지, 구독만** 한다.

**5단계 — Toolbar 구독(§9.6).** Section 뷰가 `useSyncToolWithWorkspaceContext(id)` 패턴으로 store를 구독해 active interaction(pointer·pan·zoom·length·angle·freeDraw)·feature(showGrid·showOverlays)·command(resetView 등)를 받아 처리한다. **`arrow`는 CW `InteractionType`에 없는 신규 타입**이므로 CW 측에 type + `TOOL_POLICY`(`toolbar/const.ts`) + `convertInteractionTypeToCTActionInfo` 추가가 선행돼야 한다. 계측/Arrow는 각 section slice 내부 스코프(MMI 1.13).

**6단계 — CT 공급 배선(§9.4·§1).** 데모의 `SectionCtProvider`(S3 ZIP→`CTVolume`) 자리에 **CW/Clever Space provider**를 주입한다. CW는 이미 로드한 CT 볼륨을 `CTVolume`(`{data: Int16Array, metadata}`) 형태로 어댑트해 `SectionViewer`의 `volume` prop으로 전달. 환자정보(§3.4.2)는 `metadata.patient`로 함께 넘긴다. Section 모듈은 취득 방식(S3/CW/DICOM)을 모른다.

**7단계 — Title bar · 다이얼로그 재사용(§9.5).** Scout/Pano/Section 헤더는 CW `ContentTitleBar` props(`{id,activated,maximized,imageAdjustRef,open2DImageAdjustDialog}`) 패턴으로 맞추고, Image Adjust(1.11)·Setting Th/INT(1.10)는 CW `ImageAdjustDialog`·`CTSliceSettingDialog`와 동일 스키마(`IMPRViewSetting`)로 배선한다.

**8단계 — Save/Load 매핑(§7·§9.7).** core `serializeProject(state)` 결과(CurveList·SectionInfo·PanoInfo)를 CW `projectFile.ts`의 prj XML 필드에 어댑터로 매핑. **정확한 CW prj 필드 구조는 §12-D5(CW팀 확인 대기)** — 확정 후 어댑터 완성. 역방향(`deserializeProject`)으로 prj 로드 시 곡선·B/L·Section 위치 복원.

**8b단계 — Pointer 주석 도구 제거·CW 위임(§3.8·§9.10).** Pointer는 **CW 워크스페이스(셸) 레벨** 기능이다 — CW `WorkSpace.tsx`가 `interaction==='pointer'`일 때 전역 `PointerDialog`/`PointerCanvas`를 **이미 자체 렌더**한다(Section content는 Pointer에 기여하지 않음). 따라서 접목 시:
> - **삭제:** 우리 standalone 포트 `packages/components/src/{PointerDialog,PointerCanvas}.tsx` 와 그 export(`index.ts`), 데모 App의 Pointer 배선(전체화면 모달 레이어·backdrop·`bodyRect` 캔버스·`drawingMode/color/strokeWidth` 상태). 이들은 데모 파리티용일 뿐 CW와 100% 중복이다.
> - **위임:** Pointer 동작(다이얼로그 UI·드로잉·Eraser·두께/색·Reset·Close=소거·모달 backdrop)은 **CW WorkSpace가 그대로 제공**한다. 우리 경량 대체본(경량 드래그·스와치 팝오버)은 폐기하고 **CW의 react-rnd·react-color(SketchPicker)·MUI 정본**을 사용한다.
> - **커서:** 우리 `cursors.ts`의 `ERASE`(및 Pan/Zoom/Pointer/Disable) 복사본도 §9.10대로 CW `CURSORS` import로 대체.
> - **주의(단일 오버레이 특성):** CW `PointerCanvas`는 워크스페이스 전체를 덮는 단일 오버레이라, Section 뷰가 CW content로 embed되면 **별도 배선 없이** 그 위에도 자동으로 그려진다. Section 모듈은 Pointer용 코드를 남길 필요가 없다.
> - **검증:** CW에서 Pointer 버튼 → CW 기본 다이얼로그(노랑 `#FFDD40`·SketchPicker)·워크스페이스 드로잉·Section 뷰 위 드로잉·Eraser 1요소 삭제·Close 시 전체 소거·모달 차단(Toolbar 비활성) 동작 확인.

**9단계 — MPR 연동(§12-D18, 접목 시).** MMI 1.10-2③ "Scout Th/INT ↔ MPR Axial 값 상호 동기", Image Adjust ↔ MPR 연동은 **크로스-모듈**이라 standalone에서는 미구현. CW embed 시 CW MPR store와 양방향 배선한다(standalone 렌더 동작은 정상, 값 동기만 추가).

**10단계 — 검증.** EzCloud Test 컨테이너([§9.8](https://container.test.ezcloud.ezcld.net/))에서 Toolbar·ContentTitleBar·Pan/Zoom/계측 UX 정합을 확인. (현재 Section Layout 미탑재 → 접목 후 최초 통합 지점.)

> **접목 시 최소 변경 요약**: CW가 **소스 병합**하는 것 = `section-core`(내부 패키지)·`section`(뷰, CW 트리 병합)(1단계). CW가 새로 **작성**하는 것 = `SectionContentHandler`(3단계)·`arrow` 툴 정의(5단계)·CT provider 어댑터(6단계)·prj 어댑터(8단계). CW가 **재사용**하는 것 = store/toolbar/title bar/다이얼로그/prj 파일(구독·매핑만). **이동 안 함** = 데모 셸 `apps/section-demo`(1e). **CW 정본으로 대체·중복 제거** = 커서·Grid·색 토큰·다이얼로그 등(**§9.10**). **삭제(CW가 셸 레벨 제공)** = Pointer 포트(`PointerDialog`·`PointerCanvas`·App 배선)(8b단계). **미결 선행조건** = §12-D5(prj 필드)·D18(MPR 연동 범위).

### 9.10 접목 시 중복 제거 — CW 정본으로 대체 (필수)

standalone에서는 CW를 import할 수 없어(Module Federation·CW 의존성 없음) **CW 자산을 복사·미러**했다. **소스 병합(§9.2·D4) 시 CW 원본과 중복**되므로, 아래 원칙으로 정리한다.

**원칙:** ① **데모 셸(`apps/section-demo/`)에 있는 미러/stub은 이동하지 않으므로 중복 아님**(§9.9-1e, PoC repo에 잔류·소멸). ② **모듈(`packages/`)로 병합되는 복사본은 접목 시 CW 정본 import로 교체하고 우리 복사본 삭제**(단일 정본 유지). 복사는 "standalone 실행을 위한 임시 미러"이지 유지 대상이 아니다.

| 아티팩트 | 위치 | 성격 | CW 정본 | 접목 시 조치 |
|---|---|---|---|---|
| Toolbar 아이콘 SVG | `apps/section-demo/src/cw/icons/` | 데모 stub 복사 | CW 아이콘 에셋 | **이동 안 함**(데모 잔류). 중복 아님 |
| Tool store/contract 미러 | `apps/section-demo/src/cw/{toolStore,toolContract,cwTypes}.ts` | 데모 미러 | CW `useBoundStore`·`toolbar/type.ts` | **이동 안 함**. 접목 뷰는 CW store 직접 구독(§9.6) |
| `CwToolbar` stub | `apps/section-demo/src/cw/CwToolbar.tsx` | 데모 stub | CW `Toolbar` | **이동 안 함**. CW Toolbar가 제공 |
| **커서 `CW_CURSORS`**(Pan·Zoom·Pointer·Disable·Erase·Length·Angle·FreeDraw·**Move**) | `packages/components/src/cursors.ts` | 모듈 복사(§3.7·§3.8·§3.4.2·§3.9) | CW `workSpace/setting` `CURSORS` + `vtkjs-wrapper` `overlaySelectedCursor`(Move) | **CW import로 교체·복사본 삭제**. Arrow 임시(FreeDraw)는 기획 전용 커서로 교체(§11) |
| **계측/주석 편집 + Property**(`SectionMeasureOverlay` 편집 로직·`AnnotationPropertyDialog`) | `packages/components/src/SectionMeasureOverlay.tsx`·`AnnotationPropertyDialog.tsx` | 모듈 구현/포트(§3.9) | CW `es-pixi-wrapper`(편집 엔진)·`OverlayPropertyDialog`·`CustomMenu` | **CW 정본으로 교체**(편집·Property·컨텍스트 메뉴). 우리는 Canvas2D UX 이식본이라 접목 시 CW PIXI 엔진/다이얼로그 사용 |
| **Pointer 주석**(`PointerDialog`·`PointerCanvas` + App 배선) | `packages/components/src/PointerDialog.tsx`·`PointerCanvas.tsx`, `apps/section-demo/src/App.tsx`(모달 레이어·backdrop·bodyRect) | 모듈 포트(§3.8) | CW `workSpace/layout/components/PointerDialog`·`PointerCanvas` (WorkSpace가 자체 렌더) | **삭제**(CW 셸이 제공 — Section content 기여 없음). 상세 절차 **§9.9-8b단계**. CW는 react-rnd·react-color·MUI 정본; 우리 경량 대체본 폐기 |
| **Grid 렌더** | `packages/components/src/GridOverlay.tsx` | 모듈 복제(알고리즘·값) | CW `@ewoosoft/es-view-info` `GridView` | **CW `GridView` 사용 검토·교체**(값 동일). 불가 시 정본 참조 주석 유지 |
| **색 토큰**(teal·크롬) | `ViewTitleBar.tsx`·`App.tsx` 등 하드코딩 | 모듈 복사(§3.4.1a) | CW `theme.ts`(`primary.dark` 등) | **CW theme 토큰 import로 교체** |
| **Title bar** | `ViewTitleBar.tsx` | 모듈 이식(패턴) | CW `ContentTitleBar` | CW 컴포넌트/토큰에 정합·중복 로직 제거(§9.5) |
| **Image Adjust·Setting 다이얼로그** | `ImageAdjustDialog.tsx`·`SettingDialog.tsx` | 모듈 이식 | CW `ImageAdjustDialog`·`CTSliceSettingDialog` | CW 공통 다이얼로그 재사용으로 교체(§9.5) |
| 곡선·9단면·slab·필터·직렬화 등 | `section-core` | **우리 고유 로직**(복사 아님) | — | **유지**(내부 패키지, §9.2) |

> **요지**: 복사/미러는 전부 "standalone 임시"다. **데모 셸 것은 버려지고, 모듈 것은 CW 정본 import로 대체**한다. 각 복사 파일 상단 주석에 CW 정본 경로를 명시해 교체 지점을 표시한다(예: `cursors.ts`·`GridOverlay.tsx`). 아이콘·커서 같은 자기완결 에셋은 §9.5 예외로 복사 허용이나, 병합 후 CW 원본이 있으면 그쪽을 단일 정본으로 삼는다.

### 9.11 개발 중 발견한 CW 이슈 (접목 전 개선 권고)

Section 모듈 개발 중 CloudWebViewer/CleverSpace 소스 대조에서 발견한 CW 측 이슈. 우리 모듈 범위 밖이나 **접목 품질에 영향**을 주므로 CW 팀에 전달·개선 권고한다.

**CW-1: 폰트 설정 불일치 (CleverSpace ≠ CW).** CleverSpace(호스트)와 CW가 **서로 다른 폰트 스택**을 쓰고, CW는 그것을 **`!important`로 강제**해 호스트 폰트를 덮어쓴다. 게다가 CW는 자기 폰트를 로드(embed)하지 않아 환경마다 렌더가 제각각이다. **우리 모듈은 이 둘의 합집합이 아니라 "호스트(CleverSpace) 스택에 정렬"** 했다.

**현재 폰트 현황 비교:**
| 대상 | 폰트 스택 | 웹폰트 로드 | `!important` | 맥 렌더 | Windows | ChromeOS |
|------|-----------|:---:|:---:|------|------|------|
| **CleverSpace**(ezcloud 호스트) | `'Noto Sans','Noto Sans KR','Segoe UI', sans-serif` | ✅ Noto Sans/KR **Google Fonts 로드** | ✗ | **Noto Sans** | Noto Sans | Noto Sans |
| **CW**(cloudwebviewer) | `'Segoe UI','Roboto'` | ❌ 없음 | ✅ `* !important` | **Helvetica**(폴백) | Segoe UI | Roboto |
| **우리 Section/데모** | `'Noto Sans','Noto Sans KR','Segoe UI', sans-serif`(=CleverSpace) | ✅ 데모가 Noto Sans **Google Fonts 로드** | ✗ | **Noto Sans** | Noto Sans | Noto Sans |

**문제 요약:** ① CleverSpace·CW 스택이 다름(Noto Sans vs Segoe UI/Roboto). ② CW의 `* !important`가 **호스트의 로드된 Noto Sans를 덮어씀** → CW 영역만 CleverSpace 나머지 UI와 폰트가 다름. ③ CW는 `'Segoe UI'`(Win 전용)·`'Roboto'`(미embed·CleverSpace 미로드)를 **로드하지 않아** 없는 환경(맥/리눅스)에선 폴백(Helvetica)으로 **환경별 제각각**. (근거: CW `index.css:24`, ezcloud `container-app/index.html`·`common-ui/customTheme.ts`. 관측: 동일 맥에서 CleverSpace=Noto Sans, CW=Helvetica.)

**추후 수정 방향(누가 무엇을):**
| 주체 | 조치 | 우선 |
|------|------|:---:|
| **CW** | `index.css`의 `* { font-family:'Segoe UI','Roboto' !important }` **override 제거** → 호스트(CleverSpace) 폰트 상속. (특정 폰트 필요 시 미제공 폰트를 강제하지 말고 호스트처럼 **웹폰트 로드**) | **높음(주 원인)** |
| **CleverSpace** | 현재 정상(Noto Sans 로드). embed content(CW·Section)에도 호스트 폰트가 상속되는지 확인 | 중 |
| **styleguide(VT UI/UX)** | org 전역 **단일 폰트 스택 확정**(호스트 Noto Sans 유력) → CW·Section 모두 그 하나를 따름 | 중(확정 시 정본) |

> **우리 모듈 대응(최종):** 폰트 소유는 호스트 몫(§9.10)이라 Section·데모는 **CleverSpace 호스트 스택에 정렬**(데모는 Noto Sans를 Google Fonts로 로드해 실제 배포 룩 미리보기). 접목 시 우리는 폰트를 강제하지 않고 호스트를 상속한다. **단 CW-1(CW의 Roboto 강제)이 남으면 CW가 우리 텍스트까지 덮어쓰므로, CW-1 수정이 폰트 일관성의 전제**다. → §3.4.1a. 주간회의 공유(Agenda).

**CW-2: 국제화(i18n) 현황 불일치.** CW·CleverSpace 모두 **Lingui** i18n을 쓰나 **CW의 한국어 카탈로그가 비어** 한국어 사용자에게 영어로 표시된다. 우리 Section 모듈은 i18n 프레임워크가 없고 한/영 문자열이 혼재한다. 셋의 국제화 구조·언어를 일치시켜야 접목 시 언어가 일관된다.

**현재 국제화 현황 비교:**
| 대상 | i18n 프레임워크 | 지원 locale | 한국어 상태 |
|------|----------------|-------------|-------------|
| **CleverSpace**(ezcloud 호스트) | Lingui(`@lingui/*` 4.7) | `en_US, ko_KR` | ✅ 번역됨(한국어 정상) |
| **CW**(cloudwebviewer) | Lingui(`i18n.load/activate`·`t\`\`` 238곳) | `en_US, es_MX, fr_FR, ko_KR, pt_BR` | ❌ **`ko_KR_core.po` 163개 전부 빈 translation** → 한국어에서 영어 폴백(es/fr/pt는 번역됨) |
| **우리 Section 모듈** | **없음** | — | ❌ i18n 미적용, 한/영 하드코딩 혼재 |

**문제점:** ① 우리 모듈은 i18n 미적용·한영 혼재(가장 불일치). ② CW는 인프라는 있으나 **한국어 번역 누락**(CleverSpace는 한국어 되는데 CW 영역만 영어로 튐 — 폰트 CW-1과 같은 종류의 불일치). ③ **지원 언어 목록 불일치**: **언어 선택(변경) UI는 CleverSpace(호스트)가 소유**하고 CleverSpace는 `en_US·ko_KR`만 제공하는데, **CW는 en/es/fr/ko/pt로 더 많다** → CW가 번역한 **es/fr/pt는 CleverSpace에서 선택조차 불가한 "죽은 번역"**이고, 정작 선택 가능한 **한국어는 CW가 비어 있다.** (근거: CW `packages/core/i18n/*.po`(5개 locale, ko 비어있음)·`src/App.tsx`(`i18n.load/activate`, locale=`useBoundStore i18nStore`) · ezcloud `i18n/ko_KR_EzCloud.po`·`lingui.config.ts` `locales:['en_US','ko_KR']`.)

**방침(결정 · §12-D23, 2026-07-16 회의):** **지원 언어를 셋(CleverSpace·CW·Section) 모두 한/영(`en_US`·`ko_KR`)으로 통일**하고, **CleverSpace 연동으로 CW·Section 모두 국제화 적용**. 근거: 언어 선택이 **CleverSpace(en/ko)에 종속**되므로 지원 언어는 CleverSpace 기준으로 맞춘다(그 이상은 선택 불가·무의미). 구체:
> ① **Section 모듈** = CW와 동일 **Lingui 구조 채택**(문자열 `t\`\`` 매크로화, `@lingui/react` federation shared §9.3), **en/ko 카탈로그** 제공. 선행으로 UI 문자열 한국어 통일(한영 혼재 제거).
> ② **CW**(권고) = **비어 있는 ko_KR 채우고**, 선택 불가한 **es/fr/pt는 정리**(유지 부담만·CleverSpace 미선택). → CleverSpace와 언어 목록 일치.
>
> **결정됨(2026-07-16 회의):** 지원 언어 = **한/영(en/ko) 통일**로 3개 제품 모두 확정. CW의 언어 목록 정리·ko 채우기는 **CW 팀**에 권고. 프레임워크 정합(Lingui)은 기술적 당연. → IP **T-P4-7 착수 가능**(더 이상 결정 대기 아님).

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
- **Single/Dual Layout 전환 · View Original — standalone 미구현(CW 컨테이너 몫, §12-D22).** MMI 1.13-4는 Section 레이아웃 공통툴로 나열("MPR 동일")하나 실동작은 **CW 셸/워크스페이스 레벨**이다. **View Original** = 압축본→원본 CT 재로드(CW CT 파이프라인, §9.4·§12-D20). **Single/Dual** = 워크스페이스 1/2 슬롯 분할 + 2번째 슬롯을 **외부 CT 썸네일 패널**에서 선택(다중 CT). 둘 다 외부 패널·CT 파이프라인 전제라 standalone 불가. **Section 모듈 역할은 최소**(View Original=재공급된 `CTVolume`로 재렌더 / Layout=배정된 슬롯만 채움·리사이즈 대응). 데모 툴바는 시각 정합 stub. **접목 시 CW 컨테이너가 완성.**
- **Arrow 전용 커서 제작(기획)** — **후속.** 계측/주석 커서는 CW `CURSORS` 정본을 그대로 쓰나(length→LENGTH·angle→ANGLE·freeDraw→FREEDRAW·Pointer Pen→POINTER·Eraser→ERASE), **Arrow는 v1.3.2 신규라 CW에 전용 커서가 없다.** 현재 **임시로 FreeDraw(펜) 커서** 사용(§3.4.2). **기획이 Arrow 전용 커서(화살표 그리기 표현)를 SVG로 제작하면 `cursors.ts`에 추가·교체**한다(§3.8·§3.4.2).
- **계측 크로스뷰 트래킹** — **후속.** 계측/주석은 뷰별 독립 캔버스라, 드래그·미리보기 중 커서가 다른 뷰(S↔P↔S)나 창 밖으로 빠르게 나가면 원래 뷰의 입력이 경계에서 멈춘다(버그 아님·뷰별 스코프 D21의 자연스러운 경계 행동). 창 내 연속 추적은 `setPointerCapture`(Free Draw 드래그)+window `mousemove`/`mouseup` 리스너(클릭 미리보기·유실 방지)로 가능하나 빠른 출시 우선으로 이연.
- **실제 WebGL2 GPU 리슬라이스(볼륨 3D 텍스처 → 프래그먼트 셰이더 단면 샘플링)** — **이번 범위 밖, 숙제로 남김(빠른 출시 우선, D20)**. 현재 9단면은 **CPU(WASM-resident 기본/JS 폴백)로 생성 후 WebGL은 텍스처 표시만** 한다(§8이 서술한 "채택안"과의 간극). 두꺼운 슬랩 실시간 스크롤(≤33ms)의 근본 해결책이나 큰 공수 → **Phase 5/6 후속**(GPU reslice 셰이더 구현). 현행은 완충책(캐시·디바운스·표시분리)+WASM으로 체감 유지.

## 12. Decision Log / 미확정 (TBD)

| # | 항목 | 결정/상태 | 담당·게이트 |
|---|------|-----------|-------------|
| D1 | 접목 범위 (VTK 여부) | **확정** — Section 모듈은 CW vtk **미접목**, Section 뷰(WebGL, poc 확장)만 구현. 접목은 CW가 우리 컴포넌트를 embed(§9.1) | — |
| D2 | B/L 자동 판정 | **확정** — 기획 단일 규칙(§5): P1→P2 선분, C가 있는 쪽=L. 동적 반전·반구·기준점 중심 반전(MMI 1.3#8①) 폐기 | 기획 회신 반영 완료 |
| D3 | Overlay Normal 허용 오차(§4) | 초기값 5° 제안 → 구현 초기 튜닝 후 고정. **사용자 결정 불필요** | 구현 초기 |
| D4 | 접목 형태(§9.2) | **개정(2026-07-15)** — **소스 병합 우선**: `scp-section-poc` 소스를 CW 모노레포로 이동, `section-core`는 CW 내부 패키지(publish 안 함·단위 테스트 유지)·`section`(뷰)은 CW 트리 병합(§9.9 1단계). 근거 = 이미 CW 내부(store·toolbar·title bar·다이얼로그) 결합도 높음·소비자 CW 하나뿐·publish/Federation 마찰. 패키지(`@ewoosoft/scp-section-*`)+공개 API는 **fallback**(독립 평가·다중 host 시). 기존 "패키지 확정"(v1.3)에서 전환 | — |
| D5 | Save prj(§7) | **확정·구조 파악(2026-07-15 보강)** — Save는 **상위(CleverSpace 컨테이너+api-server) 소유**: prj=**`.e3prj` XML**·**S3 저장**(api-server), 각 content는 **`ContentHandler`로 기여**(CW `CTContentHandler`가 `projectData` read/write). Section 모듈=상태 serialize/deserialize + `SectionContentHandler` 기여 + prj 필드 매핑. **CW `projectFile.ts` 필드 확인됨**: `CurveList`·**`SectionInfo{Width,Height,Interval,Thickness}`**·`PanoInfo`·`SectionalPos`·`SectionInterval`·`SectionalNum`·`AutoCurveInfo`. 개발 중엔 동일 payload를 `localStorage`/export 임시. **잔여(CW 팀):** 매핑 세부(우리 상태↔필드 정확 대응)·역호환 확인 | CW 팀(매핑 세부) |
| D6 | 구현 커버리지 | **확정** — poc를 확장해 MMI 1.1~1.13 **전 기능** | — |
| D7 | Section Slice 스크롤 NFR(§8) | 벤치마크 결과로 목표 수치 확정. **사용자 결정 불필요** | 구현 초기 |
| D8 | Scout 명칭 / Thickness drag cap | Scout 유지(기획 검토). **Thickness 드래그도 combo와 동일 30mm cap 확정**(2026-07-13, 개발실) — 정합성 + Section scroll 성능 예산(§8, Thickness 상한이 완화책) + 단일 `MAX_THICKNESS_MM` 재사용. clamp 한 줄이라 가역적 | 기획 / 개발실 |
| D9 | 일정·인원·KPI | 목표 1주·예상 2주, Raymond 1명. 비즈니스 정량 KPI 제품팀 미요구(N/A) | — |
| D10 | B/L 결정 시점·기준점 역할 | **확정** — B/L은 최초 P1·P2로 **1회 고정**, 이후 편집(P3+·P1/P2 이동)에 재판정 없음. 변경은 수동 L/B Switching만. BL/LB 기준점 이동은 B/L 무영향(§5) | 기획 회신 반영 완료 |
| D11 | 파노라마·단면 생성 모델 | **확정**(기획 2026-07-13) — 파노라마 = 곡선 따라 **가느다란(기본 Th0) 재슬라이스를 P/A로 offset 스윕**(navigator line). PoC의 thick-MIP 고정 모델은 **정정**. Section도 동일 slab 두께 보유. MMI·Ez3D-i·CleverOne 동일(§3.3). *이전 MMI 분석 누락분* | 기획 확인 반영 완료 |
| D12 | 슬랩 투영 방식 (max vs mean) | **확정(기획 2026-07-14)** — Thickness>0 slab 투영 **기본 = 평균(mean)**. **MIP(최댓값)는 Image Adjust 다이얼로그의 필터 토글**로만 선택(§3.6). (임상적으론 다소 이상하나 요구사항.) 엔진은 둘 다 지원, 기본 preset=`mean` | 기획 확인 반영 완료 |
| D13 | MMI 미명시 파라미터 범위 | **확정(개발실, 2026-07-14)** — MMI가 기본값만 준 값의 범위를 개발실이 정함: Section 가로폭 기본 30mm·**범위 20~80mm**, Section 세로폭 기본 60mm(§3.4). MMI/기획 갱신 시 갱신 | 개발실 정의 |
| D14 | BL/LB 기준점(삼각형) 이동 기능 용도 | **미확정 — 기획 확인 대기.** D10으로 "기준점 위치 기반 B/L 반전"이 폐기되어 삼각형을 드래그해도 **기능적 효과가 없다**(순수 표식만 이동). MMI 1.6-8/1.7-7의 "기준점 이동"도 원래 *개발실 리뷰 후 적용 여부 확정(TBD)*. **선택지**: (a) 드래그 제거·시작점 **정적 표식**(D10과 가장 일관, 개발실 권장), (b) 이동에 별도 용도 부여, (c) 현행 유지(이동하나 무효과). 기획 회신 필요 | **기획 확인 대기** |
| D30 | **초기화 명령(Reset Cloud Work · Initialize All) = CW 셸 소유; 기준 = default project file** | **확정(2026-07-16) — §3.10.** 두 command형 버튼 모두 CW `ContentHandler` 정본. **Initialize All**(MPR/CT 정본 `CTViewerControllerCore.initializeAll`) = MPR axis reset·overlay clear·windowing setting 기본값·`resetView`·**`reloadDefaultProjectFile`**(default 상태 복귀)·렌더. **Reset Cloud Work** = Initialize All + `resetMetaData()`(클라우드 저장분 리셋) + `requestReload()`(리로드) = 저장분 폐기 후 리로드(더 강함). 둘 다 `requiresEditControl:true`. **기준(어디로): MMI 미명시 → CW 소스상 "default project file 상태".** "파노라마 생성 전/후"가 아니라 — 파노라마·섹션은 Curve에서 **파생**되므로, Curve를 default로 되돌리면 파생물이 재계산됨(default Curve 없으면 blank, MMI 1.14 "proj Curve 없으면 blank"와 동일). **Initialize All 본체는 클라이언트라 우리도 구현(완료 T-P5-5).** **의미(MMI 미정의→정의, 2026-07-16): "데이터·값" 초기화 + "모드·토글" 유지** — 초기화=Curve 제거(→파노라마·섹션 blank)·계측 제거·**Pan/Zoom 값→identity**·WL=볼륨 기본·섹션/파노라마 파라미터 기본; 유지=활성 도구·Show/Hide Overlay·Grid 토글. 결과=CT 최초 로드처럼 Scout만(파생 영상 없음). 재오픈 복원(저장본)과 별개(저장본 불변). 상세 §3.10. **Reset Cloud Work는 구현 불가 확정** — `resetMetaData`=`ioApis.resetMetaData`(CW 호스트 주입 **클라우드 서버 IO**)·`reloadState.requestReload`(**CW 워크스페이스 리로드**)에 의존, standalone 모듈에 없음 → **미구현, 클릭 시 "접목 시 지원" 안내만**, 실제 동작은 접목 시 CW 제공(§9.10). POC 현재 두 버튼 미배선(no-op). | 확정 |
| D29 | **계측/주석 편집(Edit·Property) = CW 정합 이식, 속성 저장** | **확정(2026-07-16) — §3.9.** length·angle·freeDraw·arrow는 생성 후 편집: 도구 미선택 시 hover→이동커서(CW `overlaySelectedCursor`)·선 드래그 통째 이동·속빈 네모 핸들 드래그로 점 편집(길이·각도 실시간)·단일 선택. 우클릭→편집+컨텍스트 메뉴(흰 바탕 검정, Property/Delete). Property=선색·글자색·글자크기(6~20), **선색 바꾸면 핸들색도**. 속성·편집점은 계측 `style`로 **Save ⑨ 저장**(D26·T-P5-4). CW는 PIXI(`es-pixi-wrapper`)·`OverlayPropertyDialog`·`CustomMenu` 정본 → 우리는 Canvas2D에 동일 UX 이식, **접목 시 CW 정본으로 교체**(§9.10). 편집 오버레이는 hover 시에만 입력 캡처해 커브/Pan-Zoom 방해 안 함. 구현=T-P4-9. | 확정 |
| D28 | **Pointer 주석 = CW 컴포넌트 포트, 임시(저장 안 함)** | **확정(2026-07-15) — CW `PointerDialog`/`PointerCanvas`가 정본.** MMI 1.13-1a Pointer는 일시 주석(그리기) 도구다. CW 조사: 순수 React+Canvas2D(`Path2D`)·vtk 무관, 전역 오버레이 캔버스에 FreeDraw식 다중 요소·Eraser(클릭 1요소 삭제, `isPointInStroke` 15px)·두께(1~5, 기본 2)·색(기본 노랑 `#FFD64A`, CW settings 실제값)·Reset, **모달(뒤 UI 전부 차단)**, **Close=비활성→언마운트→그림 전부 소거**(임시, prj 저장 안 함). 본 모듈은 **소스 포트**(components), 커서 Pen=`POINTER`·Eraser=`ERASE`(신규 복사). **접목 시 CW 컴포넌트로 교체·포트 삭제**(§9.10). CW 의존(react-rnd·react-color·MUI)은 포트에서 경량 대체(드래그·color input)나 기능 동일. 구현=T-P4-8. | 확정 |
| D27b | **Pan/Zoom 대상 = 이미지·계측만; Grid 완전 고정; Ruler 위치 고정·단위는 배율 반영** | **확정(2026-07-15) — 모든 뷰.** Pan/Zoom은 **이미지(및 이미지 앵커 계측)에만** 위치·배율 적용. **Grid는 완전 고정**(pan 이동·zoom 스케일 안 함, 뷰 전체 덮는 고정 10mm). **Ruler는 위치 고정**(뷰/타일 하단·우측)이나 **눈금 단위·간격·표시 mm는 Zoom 반영**(스케일 바 픽셀길이 고정·표시 mm=base/zoom, 예 2×→25mm; 소·대눈금은 `chooseRulerSteps` 공통 규칙 1·5·10·50·100mm). 근거: Grid가 pan 따라 흔들리면 기준자로 혼란(고정), Ruler는 확대 시 실제 척도를 보여야 유용(단위 갱신)(사용자 피드백). 구현: GridOverlay transform 미적용, `ViewVerticalScaleBar`·`SectionTileChrome`에 `zoom` 전달(단위 갱신·위치 고정), 이미지(WebGL viewport/CSS)·`SectionMeasureOverlay`만 transform. | 확정 |
| D27 | **Section Pan/Zoom 적용 단위(3×3)** | **확정(2026-07-15) — 9개 뷰가 하나의 transform으로 함께 Pan/Zoom.** MMI 1.13-1a는 "MPR 동일"만 규정, 3×3 내부 처리 미명시. 각 뷰는 **자기 중앙 기준 제자리 확대·타일 클립**(뭉쳐 스프레드 아님)이되 **9개 모두 같은 값**으로 움직인다. **근거:** ① slice 스크롤 시 타일↔슬라이스가 재매핑되는데 칸마다 배율이 다르면 스크롤 때 배율이 뒤섞여 매우 복잡, ② Save Project가 뷰당 1개 상태로 단순(9벌 저장 불필요). "뷰 모드" 단일 상태로 처리. 타일별 독립(초안)은 위 이유로 배제. 구현: `useViewTransform`(단일) → WebGL `gl.viewport`+`scissor` 타일별 적용·오버레이 셀별 중앙 기준(§3.7·T-P4-6). | 확정 |
| D26 | **Save ⑨ Overlay 계측(Ann) 저장 항목** | **확정(2026-07-15, 명확화 2026-07-16) — 모듈 소유(CW도 저장하므로 우리도 저장).** MMI 1.14-⑨(Length·Angle·Arrow·FreeDraw)는 우리 계측이라 모듈 payload에 포함. `SectionProjectState`에 **`measurements[]` 필드 추가** — **뷰별(Scout·Panorama·Section)로 각각** 저장하고, **Section 주석은 어느 섹션(타일/번호)에 속하는지**(`tileIndex` + slice/arc 앵커)와 **스타일(선색·글자색·크기)** 포함. 좌표는 tile-normalized(u,v). 재오픈 시 재표시 로직과 정합. 구현=IP T-P5-4. | 확정(구현 T-P5-4) |
| D25 | **Save ③ = 뷰별 Pan/Zoom(우리에겐 3D 카메라 아님)** | **확정(2026-07-15, 명확화 2026-07-16) — 모듈 소유.** MMI 1.14-③(각 단면 Position·Panning)은 MPR이 **3D라 카메라(보는 방향+Zoom)** 를 저장하는 항목이나, **본 Section 모듈은 3D 카메라가 없다** → **각 View(Scout·Panorama·Section)의 Pan offset·Zoom 배율만** `SectionProjectState`에 저장한다(뷰당 1세트, Section 3×3은 9뷰 공통 단일 transform=§D27). Pan/Zoom 구현(**T-P4-6 완료**)됐으므로 추가 착수 가능. 구현=IP T-P5-4. | 확정 |
| D24 | **Save ①레이아웃·④ShowGrid(+Overlay 가시성) 소유** | **확정(2026-07-15, 보강 2026-07-16) — 셸(호스트) 소유, 모듈 payload 아님.** MMI 1.14-①(MPR/Section 레이아웃)·**④(ShowGrid, MMI 저장 항목)**는 **CW 컨테이너/워크스페이스 공통 상태**(레이아웃=컨테이너 슬롯 D22, ShowGrid=CW `workspaceViewFeatures.showGrid`). Overlay 표시 토글(Show/Hide Overlay)도 같은 워크스페이스 뷰기능(MMI ①~⑫엔 별도 항목 아님·⑨는 주석 "입력값"). **상위 Save가 저장·복원하고 모듈은 표시 반영만** → 모듈 `SectionProjectState` 조각엔 미포함. **단 데모 파리티**: `apps/section-demo`가 이 셸 토글(`showGrid`·`showOverlays`)을 **모듈 조각과 분리된 별도 localStorage 키**(`scp-section-viewfeatures:<CT키>`)로 저장·복원해 재오픈 시 Grid·주석 가시성까지 재현(2026-07-16). 접목 시 CW 워크스페이스가 정본. | 확정 |
| D23 | **국제화(i18n) 정책·구조·지원 언어** | **결정됨(2026-07-16 회의)** — **지원 언어를 3개 제품(CleverSpace·CW·Section) 모두 한/영(en_US·ko_KR)으로 통일 + CleverSpace 연동 국제화**. 배경: 언어 선택은 CleverSpace(en/ko)가 소유하는데 CW는 en/es/fr/ko/pt로 목록이 달라 es/fr/pt는 선택 불가·죽은 번역, 한국어는 CW 비어있음(§9.11-CW-2). Section=CW와 동일 Lingui 구조(문자열 `t\`\`` 매크로·en/ko 카탈로그, 선행 한국어 통일, **스펙 §3.11**, IP T-P4-7 **착수 가능**). CW=ko 채우고 es/fr/pt 정리는 CW 팀 권고. | 2026-07-16 회의 |
| D22 | **Single/Dual Layout · View Original 지원 범위** | **확정(2026-07-15) — CW 컨테이너/셸 레벨, Section 모듈 standalone 미구현·접목 시 CW 담당.** MMI 1.13-4가 Section 공통툴로 나열("MPR 동일")하나: **View Original**=압축본→원본 CT 재로드(CW CT 파이프라인, §9.4·D20 연장), **Single/Dual Layout**=CW 워크스페이스 1/2 슬롯+외부 CT 썸네일 패널 연동(다중 CT). 둘 다 **외부 패널·CT 파이프라인 전제**라 standalone 불가·실익 없음. Section 모듈 역할 최소(View Original=재공급 volume 재렌더 / Layout=슬롯 채움·리사이즈 대응, 이미 ResizeObserver 보유). 데모 툴바는 시각 정합 stub. → §11. | 통합 시 구현(CW) |
| D21 | **계측/주석 적용 뷰 범위** | **확정(Jessi, 2026-07-15) — Length·Angle·Free Draw·Arrow 4개 공통툴 모두 Scout·Panorama·Section 3뷰에서 동작.** 각 뷰는 자기 영역/슬라이스 스코프로 제한(Scout=Scout 영역 내·Panorama=Panorama 영역 내·Section=해당 slice 내, 경계 넘나들 불가). Arrow·FreeDraw는 MMI 1.12에 3뷰 명시돼 있었고, Length·Angle은 미명시라 확인 → 동일 적용 확정(§3.4.2). 구현: `SectionMeasureOverlay`를 Scout/Panorama 단일 영역 오버레이로 재사용. | 확정 |
| D20 | **Section 생성 기본 연산 경로 + GPU 리슬라이스 범위** | **확정(2026-07-15) — 기본 `wasm-resident`(JS 자동 폴백), 실제 GPU 리슬라이스는 숙제로 이연.** T-P6-1 측정: 두꺼운 슬랩(Th30mm) worst-case JS mean 1484·max 1787ms vs WASM-resident mean 1225·max 1336ms → **WASM이 mean −17%·max −25%·저분산**, 출력은 JS와 동일. 제품엔 연산 선택 UI가 없으므로 **기본값을 `wasm-resident`로 고정**(`useScoutAxialUi`), **WASM init/실행 실패 시 JS로 자동 폴백**(`SectionViewer`, 빈 화면 방지). 둘 다 30FPS(33ms) 미달이나 **근본해결(WebGL2 GPU 리슬라이스)은 공수 큼 → 빠른 출시 우선으로 이번 범위 밖(§11)**, 완충책(캐시·디바운스·표시분리)으로 체감 유지. **메모리:** resident는 볼륨을 WASM 힙에 상주(100~250MB, 예산 내). | 확정 |
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
| 1.64 | 2026-07-16 | **Initialize All 구현·의미 정의(§3.10·§3.4.2·T-P5-5)**: MMI 미정의 항목이라 의미를 정의 — **"데이터·값" 초기화(Curve 제거→파노라마/섹션 blank·계측 제거·Pan/Zoom 값→identity·WL 볼륨 기본·파라미터 기본) + "모드·토글" 유지(활성 도구·Show/Hide Overlay·Grid)**. 결과=CT 최초 로드처럼 Scout만(파생 영상 없음). 재오픈 복원(저장본)과 별개. `SectionViewer.initializeAll()`(Save 스냅샷 인프라 재사용, view는 identity로 리셋)·`toolStore` tick·`CwToolbar`·App effect(toolStore 미변경으로 모드 유지) 배선. **Reset Cloud Work=미구현→"접목 시 지원" 안내만**. IP T-P5-5 완료. |
| 1.63 | 2026-07-16 | **Save 복원 StrictMode 버그 수정 + 셸 뷰 토글(ShowGrid·Overlay) 데모 저장(§7-④·§12-D24)**: ① 재오픈 복원이 안 되던 원인 = **React StrictMode effect 이중 실행**으로 `useCurveEditor` 볼륨 리셋이 2회 도는데 복원은 가드로 1회만 적용 → 리셋이 이김. 복원 effect 가드 제거·deps=`[volume, initialProjectState]`로 각 pass가 "리셋→복원" 순서 보장(멱등). ② **ShowGrid는 MMI ④ 저장 항목**(셸 소유)·Overlay 가시성 토글이 데모에서 저장 안 돼 재오픈 시 주석이 안 보이던 것 → 데모가 셸 토글을 **별도 키**(`scp-section-viewfeatures:<CT키>`)로 저장·복원(D24 보강). |
| 1.62 | 2026-07-16 | **Save Project 전체 흐름 구현(§7·T-P5-2·3·4)**: 저장 모델에 **계측(⑨, 뷰별 `measurements`)·뷰별 Pan/Zoom(③, `views`)** 추가(D25/D26; ③=3D 카메라 아닌 pan/zoom 확정). 계측·view transform을 **`useScoutAxialUi` 공유 상태로 승격**(overlay·useViewTransform이 사용). `cwPrjAdapter`에 계측→`OverlayList{Scout,Panorama,Section}` 문자열·views→`_pendingD5` 반영. 데모 **Save 버튼 배선**: `SectionViewer` ref(`getProjectState`/`applyProjectState`) → CT별 키(PatientID+StudyDate) localStorage 저장 → **CW `MessageDialog` 파리티**(로딩→"Your changes have been saved."+OK) → 동일 CT 재오픈 자동 복원. UT-SAV-014/015/017/018 포함 core 102·components 32·demo 8 통과. |
| 1.61 | 2026-07-16 | **Reset Cloud Work 구현 불가 확정 + 국제화 정식 스펙 항목화(§3.10·§3.11)**: ① Reset Cloud Work는 `ioApis.resetMetaData`(CW 호스트 클라우드 서버 IO)·`reloadState.requestReload`(CW 워크스페이스 리로드)에 의존해 **standalone 구현 불가** 확정 → 미구현, **클릭 시 "접목 시 지원" 안내만**(로컬 초기화로 대체 안 함), 실제 동작은 접목 시 CW 소유. §3.10·D30·IP T-P5-5 반영. ② 국제화(en/ko 통일, D23 확정)를 **§3.11 정식 스펙 항목으로 신설**(요구사항: Lingui·문자열 외부화·한국어 통일·CleverSpace locale 구독·en/ko 2종). 기존 §9.11은 현황/문제 분석으로 유지, §3.11은 만족할 요구 규정. |
| 1.60 | 2026-07-16 | **초기화 명령 문서화 + 기준 규명(§3.10·§3.4.2·§12-D30)**: Reset Cloud Work / Initialize All을 CW 소스에서 확인해 §3.10 신설. **기준(어디로 돌아가는가)=MMI 미명시 → CW `CTViewerControllerCore.initializeAll`의 `reloadDefaultProjectFile` = "default project file 상태"**(파노라마·섹션은 Curve 파생물이라 "생성 전/후"가 기준 아님, Curve default 복귀 후 재계산·없으면 blank). Initialize All 본체(default 복귀)는 클라이언트라 **우리도 구현 가능**(본 모듈 default=오픈 시 로드 상태). Reset Cloud Work의 클라우드 리셋·리로드는 CW 셸 소유. 초기화 대상=Save §7 ①~⑫ 역연산. §3.4.2 행·D30 추가, **IP T-P5-5 신설**(Initialize All 구현 — Save Project 이후 착수, 저장 항목의 역연산). |
| 1.59 | 2026-07-16 | **주석 편집 캡처 = hover 기반으로 교체(회귀 수정, §3.9) + Setting 개발용 컨트롤 정리**: 주석이 있으면 오버레이가 뷰 전체를 캡처해 **Panorama 상하 경계선(섹션 높이)·중앙선 드래그가 막히던 회귀**를 hover 기반 캡처(window mousemove로 주석 위일 때만 `pointerEvents:auto`)로 해결. Scout도 동일. **Setting "개발용(임시)" 컨트롤 제거**: Scout Slice/WC/WW/INT·Sec 폭(대체 UI 존재), Panorama 투영 백분위·생성 버튼·타이밍(자동 생성·ImageAdjust로 대체), Section 렌더/연산 모드·타이밍. Scout **Sec 높이 슬라이더만 유지**(§3.4.2 Edit 제어점 최상단 예외와 별개). |
| 1.58 | 2026-07-16 | **국제화(i18n) 정책 결정(§12-D23·§9.11-CW-2)**: 2026-07-16 회의에서 **지원 언어를 3개 제품(CleverSpace·CW·Section) 모두 한/영(en/ko)으로 통일** + CleverSpace 연동 국제화로 확정. D23 상태를 "결정 대기"→"결정됨"으로, §9.11 방침을 결정문으로 갱신. IP **T-P4-7 결정 대기 해제·착수 가능**. CW ko 채우기·es/fr/pt 정리는 CW 팀 권고. |
| 1.57 | 2026-07-16 | **우클릭 메뉴 = contextmenu 이벤트 + Section 휠 임계값(§3.9·§3.4.2)**: 우클릭 컨텍스트 메뉴를 `mousedown button===2`→**`contextmenu` 이벤트**로 처리(Mac control-click 대응, 메뉴 안 뜨던 문제 해결). Section slice 휠은 **누적 임계값 24**로 미세 스크롤 무시(우클릭 제스처가 slice 튀게 하던 문제 해결). §3.9의 옛 window-리스너 서술 정정(오버레이 뷰 캡처 방식으로). |
| 1.56 | 2026-07-16 | **주석 편집 캡처 방식 재정비(§3.9)**: window 전역 리스너 방식(부작용: 메뉴 안 뜸·Section 미끄러짐)을 제거하고, **편집 모드에서 계측이 있으면 오버레이가 뷰를 직접 캡처**하도록 단순화 — 우클릭 메뉴·선택·드래그가 확실히 동작. **Pan/Zoom·Curve Draw/Edit 시에는 오버레이 `disabled`**(그때는 measureTool null이라 오작동하던 것 차단). 계측 없으면 캡처 안 함. |
| 1.55 | 2026-07-16 | **주석 편집 입력을 window 캡처 처리로 견고화(§3.9)**: (v1.56에서 재정비) |
| 1.54 | 2026-07-16 | **주석 선택 해제 = 빈 배경 클릭(좌/우) (§3.9)**: 선택 후 다른 주석 선택 전엔 해제 안 되던 것 수정 — CW처럼 **주석 아닌 뷰 배경 클릭(좌/우)** 시 해제. 오버레이가 주석 위에서만 캡처하므로 `window` mousedown으로 배경 클릭 감지. §3.9 단일 선택·해제 규칙 명문화. |
| 1.53 | 2026-07-16 | **FreeDraw 편집 = CW 정합(점 핸들 없음, §3.9)**: CW `FreedrawOverlay` 조사 — FreeDraw는 `select()`가 선을 굵게만 하고 per-point 핸들 없이 **통째 이동·Property·Delete**만. 우리도 FreeDraw는 점 핸들 제거·선택 시 굵은 선(length/angle/arrow는 핸들 유지). |
| 1.52 | 2026-07-16 | **모드 상호 배타(§3.4.2)**: Draw Curve/Edit Curve 클릭 시 활성 toolbar interaction(Pan/Zoom/계측/Pointer) 해제 후 시작(충돌 방지, 사용자 피드백). 반대로 toolbar 도구 활성 시 커브 Draw/Edit 취소. 커브 모드 중 계측 오버레이 입력 차단(`disabled` prop). `onClearInteraction` 콜백 App→SectionViewer→ScoutView 배선. |
| 1.51 | 2026-07-16 | **계측/주석 편집(Edit·Property) 신설(§3.9·§12-D29·§9.10·T-P4-9)**: length·angle·freeDraw·arrow 생성 후 편집 — hover 이동커서(CW `overlaySelectedCursor` `MOVE` 복사)·선 드래그 이동·속빈 네모 핸들 편집(길이·각도 실시간)·단일 선택·우클릭 컨텍스트 메뉴(Property/Delete)·Property 다이얼로그(선색·글자색·글자크기 6~20, `AnnotationPropertyDialog`=CW `OverlayPropertyDialog` 포트). 계측 모델에 `style` 추가→Save ⑨ 저장(D26). 계측 라벨 검정 박스 제거(흰 글씨). 접목 시 CW PIXI 엔진/다이얼로그로 교체(§9.10). |
| 1.50 | 2026-07-16 | **계측/주석 도구별 커서(§3.4.2·§11)**: 그리는 도구에 따라 전용 커서 — CW `CURSORS` 정본 복사(LENGTH·ANGLE·FREEDRAW 추가) + CW `ContentDialog` 매핑 정합(length→LENGTH·angle→ANGLE·freeDraw→FREEDRAW). **Arrow는 CW에 전용 커서 부재(v1.3.2 신규)라 임시 FreeDraw 펜 커서** 사용, 기획이 전용 커서 제작 후 교체(§11 숙제). `SectionMeasureOverlay`에 배선. |
| 1.49 | 2026-07-16 | **Pointer 접목 절차 상세화(§9.9-8b단계)**: 접목 시 Pointer 처리를 단계별로 명시 — Pointer는 CW WorkSpace 셸 레벨이라 우리 포트(`PointerDialog`·`PointerCanvas`·App 모달 배선) **삭제**, CW가 자체 제공(단일 오버레이라 Section 뷰 위 자동 드로잉), 커서 CW import 대체, 검증 항목까지. §9.10 표·최소 변경 요약에 링크. |
| 1.48 | 2026-07-16 | **Pointer 그리기 뷰 스코프·CW 근접 정합·소유 명확화(§3.8·§9.10)**: 드로잉 캔버스를 **본문(뷰) rect에만** 겹쳐 Toolbar 위엔 안 그려지게(backdrop이 나머지 클릭만 차단, CW 정합). 다이얼로그를 CW 닫힘 레이아웃(다크 패널·헤더 divider·teal 펜·"2" 드롭다운·노란 스와치·Reset)에 근접화, 기본색 `#FFDD40`(소스 확인). **1안 확정**: 경량 포트 유지 + 접목 시 CW 컴포넌트로 대체(verbatim 2안은 throwaway 의존이라 배제). Pointer는 **CW 셸(WorkSpace) 소유** 명시. |
| 1.47 | 2026-07-16 | **Pointer 모달 차단·기본색·다이얼로그 정합(§3.8·D28)**: Pointer 모드를 **전체화면 모달 레이어**로 → Toolbar·버튼 등 뒤 UI 클릭 완전 차단(종료는 Close만; 기존엔 toolbar가 눌려 dialog 사라짐). 기본색 빨강 → **CW 실제 기본 노랑 `#FFD64A`**. 색 UI를 단일 컬러버튼+팝오버(CW ColorButton 구조)로. 다이얼로그 픽셀 동일화는 접목 시 CW 컴포넌트로(§9.10). |
| 1.46 | 2026-07-16 | **Zoom 방향 X+Y 합산 + 드래그 텍스트 선택 방지(§3.7)**: Zoom을 Y축만 → **X·Y 합산**(`delta=dx−dy`, 위·우=확대/좌·하=축소)로. Pan/Zoom 드래그 시 오버레이 라벨(환자정보·W/L·R/L 등)이 선택되던 문제 → 뷰 컨테이너 `user-select:none`. (사용자 피드백) |
| 1.45 | 2026-07-15 | **Pointer 주석 도구 신설(§3.8·§12-D28·§9.10)**: CW `PointerDialog`/`PointerCanvas`(순수 React+Canvas2D) 포트 — 3뷰 전체 오버레이 FreeDraw 다중 요소·Eraser(1요소 삭제)·두께 1~5(기본2)·색·Reset·Close(=소거). Erase 커서 CW 정본 복사(§9.5). 접목 시 CW 컴포넌트로 교체(§9.10 표 추가). §3.7 "Pointer=deselect" 오기 정정(Pointer=주석 도구). IP T-P4-8. |
| 1.44 | 2026-07-15 | **Ruler 적응형 눈금(§3.7·§12-D27b)**: Ruler 위치는 고정이되 **Zoom에 따라 눈금 단위·간격·표시 mm 변경**(2×→50mm→25mm). 소·대눈금 3뷰 공통 규칙 `chooseRulerSteps`(core `view/rulerTicks.ts`, 1·5·10·50·100mm, 확대 시 1mm까지). `ViewVerticalScaleBar`·`SectionTileChrome`에 `zoom` 배선. Grid는 여전히 완전 고정. |
| 1.43 | 2026-07-15 | **Pan/Zoom 대상 = 이미지·계측만, Grid·Ruler 고정(§3.7·§3.4.2·§12-D27b)**: 사용자 피드백 — Grid는 Pan/Zoom에 움직이면 안 되고(고정 10mm 뷰 전체), Ruler는 뷰(Section 타일) 하단/우측에 고정. 이미지·계측만 transform. 이전 "grid/ruler가 뷰 transform 공유"(v1.33) 서술을 정정. 구현 반영(GridOverlay·SectionTileChrome·스케일바 transform 제거). |
| 1.42 | 2026-07-15 | **Section Pan/Zoom 적용 단위 확정(§3.7·§3.4.2·§12-D27)**: 3×3 **9개 뷰가 하나의 transform으로 함께** Pan/Zoom(각 뷰 자기 중앙 기준 제자리·타일 클립, 뭉쳐 스프레드 아님). MMI 미명시·개발실 결정 — 근거는 slice 스크롤·Save Project 단순화(뷰당 1상태). 구현 T-P4-6: 타일별 독립(초안)→단일 transform으로 정정, WebGL `gl.viewport`+`scissor` 타일별 적용. |
| 1.41 | 2026-07-15 | **Save 저장 항목 MMI 1.14-c ①~⑫ 전수 대조표(§7)**: 소유(모듈/셸)·모델 필드·상태 표로 정리. **갭 2건** — ③ 카메라(Pan/Zoom, D25·T-P4-6 후)·⑨ Overlay 계측(D26·`measurements[]`). **셸 소유 2건** — ①레이아웃·④ShowGrid(D24). 데모 완전 Save 흐름(CT별 키·재오픈 자동복원)·구현 노트(상태 소재·CT키=SeriesUID/폴백·캡처·적용 경로) 추가. D24·D25·D26 신설. |
| 1.40 | 2026-07-15 | **Save 시뮬레이션 방침(§7·IP T-P5-2)**: 데모는 `localStorage`에 **`.e3prj` 전체가 아닌 "CW 필드 형태의 Section 조각"**(CurveList/SectionInfo/PanoInfo 객체)을 round-trip. core `SectionProjectState` 유지 + **CW prj 필드 어댑터** 신설(접목 기여 지점·D5 매핑 검증). 포맷은 객체(JSON), 객체↔XML은 호스트 몫(선택 XML 미리보기). |
| 1.39 | 2026-07-15 | **Save Project 소유·기여 구조 명확화(§7·D5)**: Save는 **우리 모듈이 아니라 상위(CleverSpace 컨테이너+api-server) 소유** — Save 버튼·flow·**`.e3prj` XML**·**S3 저장**은 호스트, 각 content는 **`ContentHandler`로 prj에 기여**(CW `CTContentHandler` `projectData`). Section 모듈=상태 serialize/deserialize + `SectionContentHandler` 기여 + 필드 매핑. CW `projectFile.ts` 필드 확인(`CurveList`·`SectionInfo{Width,Height,Interval,Thickness}`·`PanoInfo` 등). §7 소유·기여 구조·범위 명시, D5 보강. |
| 1.38 | 2026-07-15 | **국제화(i18n) 현황 정리 + 방침(§9.11-CW-2·§12-D23)**: CleverSpace·CW 모두 Lingui이나 **CW 한국어 카탈로그 비어 영어 폴백**·**지원 언어 목록 불일치**(CleverSpace en/ko vs CW en/es/fr/ko/pt, 언어 선택은 CleverSpace 소유→CW es/fr/pt는 죽은 번역)·우리 모듈 미적용(한영 혼재). 현황 비교 표 §9.11. **추천안: 지원 언어 한/영(en/ko) 통일 + CleverSpace 연동 국제화**(Section=CW 동일 Lingui·한국어 통일, CW=ko 채우고 es/fr/pt 정리, IP T-P4-7). 지원 언어·정리는 **기획(Scott) 결정**. Agenda 공유. |
| 1.37 | 2026-07-15 | **폰트 정본 = CleverSpace 호스트(Noto Sans)로 정정 + CW 폰트 버그(§9.11-CW-1) 발견·정리**: ezcloud(=CleverSpace) 확인 결과 호스트는 `'Noto Sans','Noto Sans KR','Segoe UI',sans-serif`(Noto Sans Google Fonts 로드). CW는 `'Segoe UI','Roboto' !important`로 **호스트 폰트를 덮어쓰고 자기 폰트는 미로드** → 환경별 제각각(맥=Helvetica)·호스트 UI와 불일치 = **CW 버그**. 우리 모듈·데모를 **호스트 Noto Sans 스택에 정렬**(합집합 아님), 데모는 Noto Sans 로드. §9.11 신설(현황 비교 표·수정 주체 표), §3.4.1a 정정, 주간회의 Agenda S6/R4 공유. |
| 1.36 | 2026-07-15 | **폰트 = CW 동일 스택·embed 안 함(접목 시 렌더 검증)**: 전역 폰트를 CW 스택 `'Segoe UI','Roboto',sans-serif`로 선언(`body` 상속 + 컴포넌트 인라인, monospace 숫자 유지). **웹폰트 embed는 안 함**(폰트 소유는 CW/CleverSpace 전역 styleguide 몫). 실제 렌더는 환경 의존(Windows=Segoe UI, Roboto 설치 환경=Roboto, 그 외 폴백)이라 **접목 시 배포 환경에서 의도 폰트로 일관 렌더되는지 검증** 필요. `@fontsource/roboto` 시도했다 제거. Chrome Roboto는 Android/ChromeOS만 웹 노출(맥/윈도우 미노출) 분석 포함. §3.4.1a. |
| 1.35 | 2026-07-15 | **접목 시 중복 제거 가이드 신설(§9.10)**: standalone용 CW 복사/미러(커서·Grid·색 토큰·Title bar·다이얼로그·데모 툴바/store 미러/아이콘)를 접목 시 어떻게 정리할지 표로 명시 — 데모 셸(`apps/section-demo/cw/`)은 이동 안 해 중복 아님, 모듈(`packages/`) 복사본은 **CW 정본 import로 교체·복사본 삭제**(단일 정본). 각 복사 파일 상단에 CW 정본 경로 주석 유지. §9.9 요약에 링크. |
| 1.34 | 2026-07-15 | **Pan/Zoom 커서 = CW 정본 복사**: CW `CURSORS`(`workSpace/setting/index.ts`)의 커스텀 SVG 커서(Pan=손 핫스팟 16,16·Zoom=돋보기 13,13·Pointer 7,6·Disable 3,3)를 `components/src/cursors.ts`에 base64 그대로 복사(§9.5 에셋 허용). §3.7·IP T-P4-6에 커서 사양 반영(구현 시 뷰 cursor에 배선). |
| 1.33 | 2026-07-15 | **Grid·Ruler 뷰 전체 정합 + Pan/Zoom 상세(§3.7·T-P4-6)**: ① Grid·Section ruler **원점=뷰 좌상단(0mm)**·**뷰 전체**(letterbox 여백 포함)로 그림(등방 10mm, ruler 라벨도 뷰 전체). MMI "view 시작=0" 반영, §3.4.2 2행. ② **Pan/Zoom = 뷰별 독립·마우스 드래그**(Zoom=우클릭 상하: 위 확대·아래 축소), **zoom out으로 여백 커져도 grid/ruler는 뷰 transform 기준으로 전체 유지** — §3.7 상세·IP T-P4-6 보강(useViewTransform, 이미지+grid+ruler+계측 동일 transform, 5h). |
| 1.32 | 2026-07-15 | **Single/Dual Layout·View Original 범위 확정(D22)**: CW 셸/워크스페이스 레벨(다중 CT·CT 파이프라인·외부 썸네일 패널 전제)이라 Section 모듈 standalone 미구현·접목 시 CW 담당. Section 역할 최소(재공급 volume 재렌더/슬롯 채움). §11·D22 등재, 데모 툴바는 시각 stub 유지. |
| 1.31 | 2026-07-15 | **Show/Hide Grid 구현 + Pan/Zoom/Reset/Pointer 문서화(누락 보완)**: ① **Grid**(MMI 1.13-2a, 초기 미배선 누락 보완) — CW `es-view-info` GridView 정본(물리 10mm·`#A9A9A9`·0.7·점선 `[1,1]`·셀 중앙 원점) `GridOverlay.tsx`로 3뷰 구현, `showGrid` 배선. §3.4.1·§3.4.2 등재(IP T-P4-5 완료). ② **Pan/Zoom/Reset View/Pointer** — MMI "MPR 동일"만 있고 상세·구현 미비 → **§3.7 신설**(동작 정의)·§3.4.2 등재·IP T-P4-6(미구현, 4h) 추가. |
| 1.30 | 2026-07-15 | **계측/주석 3뷰 확장(D21, Jessi 확정)**: Length·Angle·Free Draw·Arrow 4개 툴이 **Scout·Panorama·Section 모두**에서 동작(각 뷰 영역/슬라이스 스코프). `SectionMeasureOverlay`에 `contentRect`(letterbox 보정) 추가·helper를 base rect 기반으로 일반화, Scout/Panorama에 단일 영역(rows=cols=1)으로 마운트. §3.4.2 모호점 해소 등재. |
| 1.29 | 2026-07-15 | **Section 생성 기본 = WASM-resident + JS 폴백(D20)**: 기본 연산 경로를 `js`→`wasm-resident`로 변경(`useScoutAxialUi`), WASM init/실행 실패 시 JS 자동 폴백(`SectionViewer`, 빈 화면 방지). 근거=T-P6-1(WASM mean −17%·max −25%·저분산). **실제 WebGL2 GPU 리슬라이스는 이번 범위 밖·숙제**로 §11 명시(현행 WebGL=CPU 결과 텍스처 표시-only, §8 간극). 빠른 출시 우선. |
| 1.28 | 2026-07-15 | **T-P4-4·T-P6-1**: ① **Overlay 3D 평면 귀속**(core `overlayPlane.ts`: 거리≤±Int/2 & normal≤5° `OVERLAY_NORMAL_TOLERANCE_DEG` D3 분리, UT-OVL-001/002/003 12케이스) + UI 호장 앵커 재표시(계측이 생성 slice에서만 보임·스크롤 앵커 해소). ② **Slice 스크롤 벤치마크**(core `sectionGenBench.ts`·dev 훅, UT-NFR-001): Th30mm worst-case **JS 1484/1787ms·WASM-resident 1225/1336ms**(30FPS 40~54× 초과)→§8 반영. 계측 도구(Length/Angle/FreeDraw/Arrow) 계속 Section 한정 상태(Scout/Pano 확장은 Jessi 답변 대기). |
| 1.27 | 2026-07-15 | **T-P4-2/3 계측·주석**: Section 타일 Length(mm)·Angle(화면좌표°)·Free Draw(선)·Arrow(2클릭+화살촉). core `measure/measurement.ts`(정규화좌표·타일 clamp) + `SectionMeasureOverlay`(그리드 오버레이·타일 hit-test 스코프) + Toolbar 배선. UT-MEA-001/002·UT-ARR-001/002. |
| 1.26 | 2026-07-15 | **T-P7-5/6 마감(오버레이 스타일 토큰화)**: Scout·Panorama 오버레이 색·굵기를 `components/src/overlayStyle.ts`(`SCOUT_OVERLAY_COLORS`·`PANORAMA_OVERLAY_COLORS`·`rgbaDim`)로 분리, 두 뷰가 참조(인라인 rgba 제거·출력 동일). 9 Active section line 호장 좌표를 공용 `nineSectionArcOffsetsMm`로 추출. UT-UI-041/051(`overlayStyle.test.ts` 6케이스) 통과. §3.4.1 색 소스 위치 갱신. |
| 1.25 | 2026-07-15 | **접목 형태 = 소스 병합으로 D4 개정**: 패키지/Federation → **CW 모노레포 소스 병합 우선**(`section-core`=CW 내부 패키지·`section`=CW 트리 병합). §9.2 재작성, §9.9 1단계를 1a~1e 상세 절차(디렉터리 이동·스코프 개명·의존성 hoist·빌드/테스트 편입·데모 셸 분리)로 확장, §9.3 registry/Federation/스코프 행 갱신, 2단계·최소변경요약 정정, D4 개정. 패키지는 fallback으로 유지. |
| 1.24 | 2026-07-15 | **저장소·데모 사이트 명시 + 접목 실행 절차(§9.9) 신설**: Resource에 「저장소·데모 사이트」 표 추가(repo `dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc`·데모 `scp-section-demo.test.scp.esclouddev.com`·CT S3·CI/CD, WebSectionView PoC OnePager 참조). §9에 **10단계 접목 how-to**(패키지 설치→환경 게이트→Content 등록→Store→Toolbar→CT 공급→Title bar/다이얼로그→Save/Load→MPR 연동→검증) + 최소 변경 요약 추가. |
| 0.1~0.6 | 2026-07-09~10 | 초안 — B/L·환경 정렬·pnpm link·EzCloud·화면 3분할 |
| 1.0 | 2026-07-13 | MMI 1.1~1.14 전 매핑·모드 표. Overlay·Draw curve·Save·NFR 신설. cloudwebviewer 실조사 반영 §9 |
| 1.1~1.2 | 2026-07-13 | 접목 방식 검토, spec-reviewer 리뷰 반영(8필드·중복 최소화·N/A·측정가능 NFR·MMI 정합 보정) |
| **1.3** | **2026-07-13** | **접목 범위 확정(D1): CW vtk 미접목, Section(WebGL, poc 확장)만 구현 — §9 전면 재정리(스텁 채움 → embed 정합), §1·§2·Risk 재작성. B/L 새 규칙(D2): P1→P2 선분·C쪽=L 단일 규칙, 동적 반전 폐기 — §5 재작성. 접목 형태 패키지+공개 API(D4, §9.2). Save CW prj 호환+개발용 브라우저 임시 저장(D5, §7). 커버리지 poc 확장 전 기능(D6). 일정 목표1주/예상2주(D9)** |
| **1.4** | **2026-07-13** | B/L **결정 시점 명확화(D10 확정)**: 최초 P1·P2로 1회 고정, 이후 P3+·P1/P2 이동 등 편집에 재판정 없음, 변경은 수동 L/B Switching만. 기준점 이동 B/L 무영향. §6에 **커브 종료=더블클릭**(우클릭=직전 취소) 행 명시 |
| **1.5** | **2026-07-13** | **공유(VKS 리뷰)용 참조 정리**: "참조"를 org URL로 교체(MMI=SharePoint PPT, PLAN-1287=Jira, 개발실 리뷰=VKS), 내부 문서(개발계획·작업 가이드) 링크 제거. 본문 내부 인용(MMI.md 추출본·작업 가이드 §4.2) → 정본·출처 표기로 정리 |
| **1.23** | **2026-07-15** | **Scout 환자정보·R/L 오버레이(MMI 1.2)**: Scout 좌상단에 환자 **성별·나이·촬영일**(line1 `[F] 034Y`·line2 `20240919`) 표시, 좌우 가장자리에 방향 **R/L**(좌=R·우=L, 표준 axial 고정 §D19). core `VolumeMetadata.patient`(DICOM Sex 0010,0040·Age 0010,1010·StudyDate 0008,0020↣AcquisitionDate 0008,0022) 신설·파싱, `ViewInfoOverlay`에 `topLeft`·`leftCenter`/`rightCenter`·`patientInfoLines()` 추가. 값 없으면 미표시. §3.4.2 처리 2행 등재. **셸 상단 배너**도 하드코딩 stub→실데이터 `<ID> <이름> <나이>`(이름 PN 파싱·나이 앞0 제거, 헬퍼 `patientTitle` 등 components export). |
| **1.22** | **2026-07-15** | **CW UI 크롬 색·치수 통일(§3.4.1a 신설)**: 사용자 측정값을 **CW 소스코드에서 직접 대조** → teal·헤더 색/높이가 불일치하여 **소스 정본값 채택(Jessi 확정)**. Top Toolbar `#141414`·h60(`CwToolbar` 44→60), 뷰 헤더 **`#333333`·h32**(`ViewTitleBar` 26→32), 뷰 배경 `#000`. **아이콘 색 모델**: 기본 `#FFFFFF`·hover/active **`#00BEA5`**·active+hover **`#61F2DF`**·disabled **white@opacity0.3**, **hover는 배경 대신 fill 변경**(`rgba(0,190,165,0.4)` 배경 hover 제거). 기존 `rgb(0,190,165)`(=`#00BEA5`)는 CW 정본과 일치해 유지. **MPR/Section 전환 바는 CW에 없음** → 데모 전용(`#3B3B3B`·h34)으로 명시, 접목 시 제거. (측정값 `#16B69C`/`#5BF0DB`/`#2D2D2D`/`#5B5B5B`은 스포이드 오차로 판단·미채택.) **아이콘 크기도 CW 정합**: 툴바 22→**36**(버튼 꽉 채움), 뷰 헤더 15→**24**(CW `ICON_SIZE`, 버튼 22→28), 툴바 버튼 간격 소폭 확대. |
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
