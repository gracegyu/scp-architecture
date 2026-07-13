# Cloud Web Viewer v1.3.2 — Section 모듈 개발계획

| 항목 | 내용 |
|------|------|
| 문서 버전 | 0.9 |
| 작성일 | 2026-07-09 (최종 현행화 2026-07-13) |
| 작성 | Raymond |
| 상태 | **Spec(OnePager) v1.5 완성.** 현재: VKS 공유·리뷰 요청 + **환경 정렬(§10)→구현 착수** 병행. 모든 핵심 결정 확정(§16 Decision Log) |

> 본 문서는 **내부 개발 계획·의사결정 기록**이다. 리뷰 공유 정본은 [OnePager Spec](./Section-Module-Spec-v1.3.2-OnePager.md)이며, 세부 요구·접목 계약은 그쪽을 따른다. 본 문서는 "왜 이렇게 정했는가"의 배경을 남긴다.

---

## 0. 최신 결정 요약 (2026-07-13)

OnePager §12 Decision Log와 동기. 상세는 각 절 참조.

| # | 결정 | 내용 |
|---|------|------|
| D1 | **접목 범위** | Section 모듈은 **Cloud Web Viewer(CW)의 vtk 파이프라인 미접목**. Section 뷰(**WebGL, PoC 확장**)만 구현하고, CW가 우리 컴포넌트를 **embed**한다(§8·§9) |
| D2 | **B/L 자동 판정** | **확정** — 기획 단일 규칙: P1→P2 선분에서 **CT 단면 중심 C가 있는 쪽=L, 반대=B**. 최초 2점으로 **1회 고정**, 이후 편집 재판정 없음, 변경은 수동 L/B Switching (§6.2) |
| D4 | **접목 형태** | `@ewoosoft/scp-section-*` 패키지 + 공개 API `SectionViewer`(React)로 CW가 import. 순수 수학 코어는 프레임워크 독립 유지(OnePager §9.2·§9.8) |
| D5 | **Save prj** | CW prj XML 스키마 호환 직렬화. 개발 중엔 동일 payload를 **브라우저 localStorage/export**로 임시 저장(§8.4) |
| D6 | **구현 커버리지** | PoC를 확장해 **MMI 1.1~1.13 전 기능** |
| D9 | **일정** | 목표 **1주**, 예상 **2주**. Section 모듈 = Raymond 1명 / 접목 = CW 팀 |
| 기타 | D3(Overlay normal 5° 튜닝)·D7(Slice 스크롤 NFR 벤치마크)·D8(Scout 명칭·Th cap 기본값)·D10(B/L 1회 고정) — OnePager §12 |

---

## 1. 이 문서의 역할

MMI 검토·기획 답변(PLAN-1287)·PoC 결과를 바탕으로, **Section 모듈**을 무엇으로 부르고 어디까지 만들며 어떤 순서로 진행할지 정리한 **개발 계획·의사결정 기록**이다.

- 구현 코드베이스는 **`scp-section-poc`에서 이어서 개발**한다 (§3 **방안 1** 확정). `cloudwebviewer` 레포에 Section을 직접 넣지 않는다.
- Section 뷰는 **WebGL로 직접 구현**(PoC 확장). **CW의 vtk 파이프라인은 사용·구현하지 않는다**(D1). 접목은 CW가 우리 React 컴포넌트를 embed하는 방식이다.
- **개발 환경·UI 스택·툴바 look&feel** 은 `cloudwebviewer`와 **통일**하여 embed 비용을 최소화한다 (§10). 개발 중엔 CW `Toolbar`를 **pnpm link**로 가져와 데모에서 검증한다(§10.4).
- Spec(SRS) 본문은 **OnePager Spec** (`Section-Module-Spec-v1.3.2-OnePager.md`, v1.5).

---

## 2. 명칭 정의

### 2.1 Section 모듈

| 구분 | 명칭 | 설명 |
|------|------|------|
| 본 작업 | **Section 모듈** | MMI v1.3.2 Section Layout 기능을 **제품 접목 전**에 구현·인계하는 WebGL 구현체 |
| 선행 검증 | **Web Section View PoC** (`scp-section-poc`) | 기술 타당성 검증 완료. Section 모듈의 **출발점**이자 확장 대상 |
| 최종 제품 | **Cloud Web Viewer** (Clever Space CT Viewer) | Section 모듈을 **embed**하는 대상 |

PoC와 Section 모듈의 차이:

| | PoC | Section 모듈 |
|---|-----|--------------|
| 목적 | WebGL·곡선·9단면 등 **기술 검증** | MMI v1.3.2 **동작·UX·데이터 규칙** 전 기능 구현 |
| 범위 | 단계별 최소 기능 | MMI 1.1~1.13 + Overlay 규칙. UI: image23 3영역 + CW Top Toolbar (§8) |
| 품질 | 데모·실험 수준 | 인계 가능 수준 (패키지·공개 API·데모·Known gaps) |
| 제품 연동 | 없음 | 인계 후 CW Viewer 팀이 embed |

대외·영문 표기: **Section Module (v1.3.2)**.

### 2.2 하지 않는 명칭

- **PoC** — 타당성 검증은 끝났으므로 이후 단계에 PoC라고 부르지 않는다(코드베이스 이름은 유지).
- **Prototype** — 버릴 코드 느낌. 인계 목적과 맞지 않음.

---

## 3. 개발 레포 선택 — 방안 1 확정 (기록)

Section v1.3.2를 어느 레포·어떤 방식으로 개발할지에 대한 결정이다. **결론: 방안 1**(scp-section-poc에서 개발 + CW 환경 정렬 + 인계). 아래는 의사결정 기록.

### 3.1 방안 요약

| | 방안 1 (확정) | 방안 2 | 방안 3 |
|---|--------|--------|--------|
| **명칭** | **scp-section-poc + CW 환경 정렬** | cloudwebviewer 브랜치 직접 개발 | cloudwebviewer fork |
| **코드 위치** | `scp-section-poc` (`@ewoosoft/scp-section-*`) | `cloudwebviewer` | fork 레포 |
| **CW 연동** | 개발 중 `pnpm link:`로 Toolbar 등 재사용, 제품은 CW가 패키지 embed | 네이티브 import | fork 본문 + 데이터 개조 |
| **Section 엔진** | PoC 계승 (WebGL·curve·9단면) | PoC 이식/재작성 | PoC 이식 |
| **인계·접목** | **필요** — 패키지·API·데모 → CW 팀 | 불필요 (PR 머지) | fork→upstream 역이식 |

### 3.2 방안 1 채택 근거

1. **PoC가 이미 Section 엔진·UI 골격을 갖춤** — 레포를 옮기면 이식만으로 2~4주 손실 가능.
2. 우리가 새로 만드는 것은 **(3) Section 뷰(WebGL)** 뿐. (1) Toolbar·(2) MPR/Section 선택은 CW와 정합(§9)해 embed 용이.
3. 접목 불가피 영역(Scout=MPR Axial, Clever Space 셸, prj, Federation)은 어차피 CW 팀 작업 — 방안 1은 **Section 로직만 인계**.
4. 방안 3은 fork 동기화·역머지 비용이 방안 1+2 합보다 큼(비권장).

**방안 2 예외 조건**(CW 정식 개발자가 Section까지 동일 브랜치에서 담당, PoC WebGL을 CW vtk로 교체 합의)은 현재 해당 없음. **D1로 "vtk 미접목, WebGL embed" 확정**되어 방안 1이 최종.

### 3.3 확정 후 작업 흐름

```
section.code-workspace (탐색) + Claude cwd = scp-section-poc (실행)
    ↓
§10 환경 정렬 (버전·MUI·zustand·CW Toolbar link)
    ↓
section-demo = CW Toolbar(link) + MPR/Section stub + SectionViewer(WebGL)
    ↓
MMI 1.1~1.13 전 기능 구현 (@ewoosoft/scp-section-*)
    ↓
인계물: 패키지·공개 API·데모·embed 매핑·Known gaps
    ↓
[ CW 팀 ] embed (ContentDialog/ContentHandler에 SectionViewer 연결) + 접목(§8.3)
```

### 3.4 Claude Code cwd

기본 cwd = **`scp-section-poc`**(구현·빌드·git). 문서만 대량 수정 시 문서 폴더. 여러 레포 열람은 Cursor `section.code-workspace`. 상세: [작업 가이드 §2.1](./Claude%20Code%20작업%20가이드.md).

---

## 4. 전체 진행 절차 (현행)

```
[완료] MMI v0.9.1
[완료] MMI 개발실 리뷰 (VKS)
[완료] 기획 답변 (PLAN-1287) + MMI 보강
[완료] B/L 자동 판정 — 기획 단일 규칙 확정 (2026-07-13, §6.2)
[완료] 개발 레포 — §3 방안 1 확정
[완료] OnePager Spec v1.5 — MMI 1.1~1.14 매핑·접목 정합·B/L·Save·NFR
    ↓
[지금] Spec 리뷰 공유 (VKS) — 기획 + CW Viewer 팀
[지금] scp-section-poc 환경 정렬 (§10)  ← 구현 착수 전 필수, 리뷰와 병행
    ↓
Section 모듈 구현 (MMI 전 기능) + Section Slice 스크롤 성능 벤치마크(구현 초기)
    ↓
인계 (패키지·공개 API·데모·Known gaps·embed 매핑)
    ↓
[Cloud Web Viewer 팀] embed + 접목 (Scout↔MPR Axial, Layout 전환, prj I/O)
    ↓
통합 테스트 → 출시
```

주의:
- **Spec 리뷰는 공유·정렬 목적**이며, 구현은 리뷰와 병행 착수한다(핵심 결정 확정됨).
- **Save Project(1.14)** 는 데이터 모델·CW prj 스키마 매핑까지 Section 모듈, 실제 파일 I/O는 접목(§8.4).

---

## 5. 참조 문서·산출물 맵

| 단계 | 문서 | 링크 |
|------|------|------|
| **Spec 정본** | Section OnePager Spec v1.5 | [로컬](./Section-Module-Spec-v1.3.2-OnePager.md) |
| 요구사항 | MMI (요구사항 정본) | [SharePoint PPT](https://vatechcorp.sharepoint.com/:p:/s/es/IQCjrxXEJ0pTQYGI9-PSaawwARs_XFxM0DuVBzvOYQBGVu0?e=ztkM8R) · [로컬 추출본](./기획·요구사항/MMI/MMI.md) |
| 기획 답변 | PLAN-1287 | [Jira](https://vts.vatech.com/browse/PLAN-1287) |
| 개발실 리뷰 | MMI 개발실 리뷰 | [VKS](https://vks.vatech.com/x/2_bhEg) · [로컬](./검토/MMI_개발실리뷰.md) |
| PoC 배경 | Web Section View PoC OnePager | [로컬](../PoC/WebSectionView_PoC_OnePager.md) |
| 구현 코드 | scp-section-poc | `~/Documents/Azure/scp-section-poc` |
| 접목 대상 | cloudwebviewer | `~/Documents/Azure/cloudwebviewer` · [Azure DevOps](https://dev.azure.com/ewoosoft/cloudwebviewer/_git/cloudwebviewer) |
| 인계물 | (구현 후 작성) | README·API·데모 URL·Known gaps |

---

## 6. 기획 확정 사항

PLAN-1287 Jessi 회신 + MMI + 2026-07-13 B/L 회신 기준. OnePager §3~§7에 반영됨.

| MMI | 항목 | 확정 내용 |
|-----|------|-----------|
| 1.14 | Save Project | MPR과 동일. Desktop→Web 최초 업로드만. Clever One sync 없음. proj Curve 있으면 세팅, 없으면 blank |
| 1.11·1.12 | 계측·주석 | prj 저장. Clever One 규칙 + MMI Overlay §6 |
| 1.8 | Active section line 회전 ±45° | **v1.3.2 스펙아웃** (임플란트 시뮬 재검토) |
| 1.6·1.7 | BL/LB 기준점 이동 | 포함. **단, 이동은 B/L 판정에 영향 없음**(§6.2, D10) |
| 1.5·1.3 | **B/L 자동 판정** | **확정 — §6.2 새 단일 규칙**. 폴백: 수동 L/B Switching |
| 1.10 | Thickness | 기본 0mm. combo 상한 30mm(Clever One 동일). **drag(Panorama thickness line)도 동일 30mm cap 확정**(2026-07-13, 개발실 — 정합성·Section scroll 성능 예산, 단일 `MAX_THICKNESS_MM`) |
| 1.10 | Draw curve 중 Thickness/Interval | curve 취소 없음, 즉시 적용 |
| 1.5 | Draw curve 표시 | Active line: 점 추가마다 갱신. Section 이미지: curve 완료 후 1회. 종료=더블클릭(우클릭=직전 취소), ESC 미적용 |
| 1.9 | slice 더블클릭 최대화 | 포함 |
| — | 모바일/터치 | v1.3.2 마우스 전용 |
| — | Scout 명칭 | Scout 유지 (D8) |

### 6.1 Overlay 표시 규칙 (MMI EP01_F013 §6)

- Overlay는 Curve + 생성 시점 평면(point, normal)에 귀속.
- Section 표시 조건: (1) 현재 슬라이스 평면과 거리 ≤ ±Interval/2, (2) Normal 허용 오차 — **초기값 5° 제안, 구현 튜닝 후 고정**(D3).
- Curve point 변경: 일시 미표시 가능, 데이터 삭제 아님. Interval 변경: normal 유지·복귀 시 재표시. Thickness 변경: 무영향.
- Overlay는 MPR 레이아웃과 공유하지 않음. 좌표계는 **환자 볼륨 3D**.

### 6.2 B/L 자동 판정 — 확정 규칙 (2026-07-13 기획)

> PLAN-1287의 초안(반구·진행 방향·드로잉 중 극성 반전)은 **폐기**. Clever One 검증을 거친 아래 단일 규칙으로 확정.

- **규칙:** 첫 두 점 **P1(시작)·P2(두 번째)** 선분을 긋고, **CT 단면 중심점 C가 있는 쪽 = L(설측), 반대쪽 = B(협측).**
- 판정식: `s = sign((P2−P1) × (C−P1))` (2D 외적). C가 있는 쪽 = L.
- **최초 2점으로 1회 결정·고정.** 이후 P3+ 추가·P1/P2 이동 등 어떤 편집에도 **재판정 없음**. 방향 변경은 **수동 L/B Switching**만.
- BL/LB 기준점(첫 점 P1)은 시각 표식으로 유지하나 **이동은 B/L에 영향 없음**(구 "기준점 중심 반전" MMI 1.3#8① 폐기).
- 상세·구현: [OnePager §5](./Section-Module-Spec-v1.3.2-OnePager.md).

---

## 7. Spec 확정 항목 현황

| 항목 | 상태 |
|------|------|
| B/L 자동 판정 | **확정**(§6.2, OnePager §5) |
| 접목 방식(vtk 여부) | **확정** — vtk 미접목, WebGL embed(D1, §8·§9) |
| Save Project 저장 필드·prj 매핑 | **확정** — 회전 각도 삭제, CW prj 스키마 매핑(OnePager §7) |
| Overlay Normal 허용 오차 | 초기값 5° → 구현 튜닝(D3) |
| Section Slice 스크롤 성능 | 구현 초기 벤치마크로 NFR 수치(D7) |
| Image Filter / 계측 툴 / Arrow | MPR→Section. **Arrow는 CW `InteractionType` 미포함 → 신규**(§9) |
| UI 스택·툴바 정합 | §10 환경 정렬 (구현 전 게이트) |

---

## 8. Section 모듈 범위

### 8.1 범위 — image23 3영역 + Top Toolbar (WebGL 구현)

| UI 계층 | MMI | Section 모듈 | 근거 |
|---------|-----|--------------|------|
| **3영역 뷰어 본문(WebGL)** | 1.2~1.9 | **포함(직접 구현)** | image23 정본. PoC SectionViewer 확장 |
| **뷰별 타이틀 바** | 1.7~1.9 | 포함 | CW `ContentTitleBar` 패턴 |
| **Top Toolbar** | 1.12·1.13 | 포함 | 개발 중 CW `Toolbar` link, 이벤트 연동(OnePager §9.6) |
| **MPR/Section 선택** | 1.1 | 포함(데모 stub) | Clever Space 라우팅은 접목(§8.3) |
| **Clever Space 셸** | LNB·Back·환자 목록 | 제외(접목) | host·ezcloud 연동 |
| **CT 로드·prj I/O** | 1.14 | 데이터 모델·직렬화 / 데모 임시저장 | 실제 prj I/O는 CW 팀(§8.4) |

구현 원칙:
- Section 엔진·WebGL·수학·Draw curve·B/L·9단면은 **`@ewoosoft/scp-section-*`** 에 둔다.
- 툴바·다이얼로그는 CW 소스 **복사 금지** — 개발 중 `@cloudwebviewer/core` **pnpm link**로 재사용(§10.4). look&feel·이벤트 자동 일치.
- **CW의 vtk Section 뷰(Layout3DPAN 등)는 사용하지 않는다**(D1, §9).
- MMI 1.12 **Arrow**는 CW `InteractionType` 미포함 → CW 패턴으로 신규 추가.

### 8.2 Integration Spec — Cloud Web Viewer 담당 (접목)

- **embed**: CW `ContentDialog` contentType 분기에 Section content 추가 → `SectionContentHandler`(ContentHandler 상속)가 우리 `SectionViewer`(WebGL) 렌더·중계(OnePager §9.7).
- MPR ↔ Section 토글·라우팅 (MMI 1.1).
- Scout view = MPR Axial 컴포넌트 재사용 (Section 모듈 2D Scout 교체).
- Save Project prj 읽기/쓰기 (MPR 기존 구현 통합, CW prj 스키마).
- Desktop→Web 최초 업로드, Curve 유무 초기 세팅.
- Clever Space `host-app`·Back·권한·환자 컨텍스트. Module Federation 배포.

### 8.3 Save Project 범위 (D5)

- Section 모듈: 저장 항목·**CW prj XML 스키마 매핑** 정의 + serialize/deserialize API + **개발용 브라우저 임시 저장**(localStorage/export — payload 구조는 CW prj와 동일 유지).
- CW 팀: 실제 prj 파일 I/O·자동저장·Desktop→Web 업로드.

---

## 9. cloudwebviewer 레포 분석 (2026-07-13 실조사)

로컬: `~/Documents/Azure/cloudwebviewer` · 원격: [Azure DevOps](https://dev.azure.com/ewoosoft/cloudwebviewer/_git/cloudwebviewer)

### 9.1 아키텍처·환경 (실측)

- **Module Federation**(`@originjs/vite-plugin-federation` ^1.3.3). `packages/core/vite.config.ts`: `exposes { './viewer','./handler' }`, `shared: react·react-dom·zustand·@lingui/react`.
- 패키지: `@cloudwebviewer/core`(UI·toolbar·다이얼로그) / `core-types`(계약) / `lib/react-vtkjs`·`vtkjs-wrapper`(vtk 엔진) / `packages/comment` / `examples/host-app`.
- 버전: pnpm **9.15.9**, React **18.2**, TS **5.2.2**, Vite **5.0.8**, MUI **5.15.5**, Emotion 11.11, zustand **4.4.7**(+immer), Lingui 4.7, react-query 5.39. `.npmrc` = Azure DevOps `@ewoosoft` private registry.

### 9.2 CW의 Section 관련 자산 (참고 — 본 모듈 미사용, D1)

CW vtk 엔진에 Section 파이프라인 **뼈대(계약)는 있으나 뷰 로직은 스텁**이다. **우리는 이것을 사용·구현하지 않는다.** 접목은 CW가 우리 WebGL 컴포넌트를 embed하는 방식이다.

| 요소 | 위치 | 상태 |
|------|------|------|
| Layout/ViewType | `vtkjs-wrapper` `CTViewerLayout.Layout3DPAN`, `ViewType.Volume2DSection` | 존재 |
| 뷰 클래스 | `view/VolumeSectionView·ScoutView·PanView.ts` | **스텁(각 ~25줄)** |
| 오브젝트·코어 | `3DObject/VolumeObjectSection`·`core/PanViewerCore` | 빈 상속 |
| prj 스키마 | `common/defines/projectFile.ts` `CurveList·CurveInfo·SectionInfo·PanoInfo·SectionalPos/Interval/Num·AutoCurveInfo` | 존재 → **Save 매핑 대상**(§8.3) |
| Setting | `types/core/setting.ts` `MPRViewThicknessType=0..30`, `SLICE_THICKNESSES` | MMI Th 0mm·30mm cap과 일치 |

### 9.3 Section 모듈이 정합할 CW 셸 계약

개발 중 재사용(link)하거나 접목 시 결합할 대상. 상세는 OnePager §9.4~9.7.

| 영역 | 경로 | 용도 |
|------|------|------|
| Top Toolbar | `packages/core/src/toolbar/` (`Toolbar`·`ToolBtn`·컨테이너들) | look&feel·이벤트 (개발 중 link) |
| 툴 타입 | `toolbar/type.ts` `InteractionType`(pointer/pan/zoom/length/freeDraw/angle — **arrow 없음**)·`CommandType`·`WorkspaceViewFeatureType` | 구독·Arrow 신규 |
| store | `store/index.ts` `useBoundStore`(`IToolSlice` 등, `ImmerStateCreator`) | 툴바↔뷰 통신(OnePager §9.6) |
| 뷰 타이틀 바 | `workSpace/layout/components/ContentTitleBar.tsx` | Scout/Pano/Section 헤더 |
| Content 등록 | `content/handler/ContentHandler`·`ContentHandlerFactory`·`ContentDialog` | embed 지점(§8.2) |
| 공통 다이얼로그 | `workSpace/content/components/common/`·`ctContent/CTSliceSettingDialog` | Image Adjust·Setting 재사용 |

### 9.4 EzCloud Test — 런타임 참고

[https://container.test.ezcloud.ezcld.net/](https://container.test.ezcloud.ezcld.net/) — Clever Space 내 Cloud Web Viewer. MPR·Toolbar·ContentTitleBar UX 정본(조직 계정). Section Layout 미탑재 → MPR만 참고. Section 데모는 `scp-section-poc` `section-demo`. 로컬 `host-app`은 link 디버깅 시에만.

---

## 10. 개발 환경 정렬 — scp-section-poc ↔ cloudwebviewer

### 10.0 정책 (확정)

| 항목 | 결정 |
|------|------|
| 구현 레포 | `scp-section-poc` (방안 1). 동일 레포에서 계속 개발 |
| 정본(참조) | `cloudwebviewer` — 버전·MUI·`.npmrc`·Toolbar 정본 |
| CW UI 소비(개발 중) | `@cloudwebviewer/core` **pnpm `link:`**. 소스 복사·포크 금지 |
| Section 엔진 | `@ewoosoft/scp-section-*` 유지 — CW core와 분리 |
| 하지 않는 것 | Section 구현을 cloudwebviewer로 이전하지 않음. **CW vtk 파이프라인 미사용** |
| CW 로컬 빌드 | link·최초 `pnpm i` 1회. 일상 개발은 `scp-section-poc pnpm dev`만 |
| 문서 정본 | Spec·MMI·개발계획은 scp-architecture 유지 |
| 목적 | 툴바·공통 UI 재사용, embed 시 의존성·빌드 갭 최소화 |

환경 정렬은 **구현 착수 전 게이트**(OnePager §9.3와 동일).

### 10.1 버전 목표

| 항목 | cloudwebviewer | scp-section-poc(현재) | 목표 |
|------|------|------|------|
| Node / pnpm | 20.x / 9.15.9 | ≥18 / 9.1.1 | 20.x / **9.15.9** |
| React / TS / Vite | 18.2 / 5.2.2 / 5.0.8 | ^18 / ^5 / **6.0** | 18.2 / 5.2 / **5.0** |
| MUI / Emotion / zustand | 5.15 / 11.11 / 4.4.7 | 없음 | 동일 major |
| registry | `.npmrc` `@ewoosoft` private | 없음 | CW `.npmrc` 공유 |
| 패키지 스코프 | `@cloudwebviewer/*` | `@ewoosoft/scp-section-*` | 유지 |

### 10.2 scp-section-poc 적용 체크리스트

1. 루트 `package.json` — `packageManager: pnpm@9.15.9`, `engines.node: 20.x`.
2. `apps/section-demo` — vite **5.0.8**, react/react-dom **18.2**, typescript **5.2**.
3. MUI·Emotion·(필요 시 Lingui) — CW major 정합.
4. `.npmrc` — CW와 동일 registry 설정(설정 파일만).
5. `@cloudwebviewer/core`·`core-types` pnpm `link:` (§10.3).
6. `section-demo`에서 `Toolbar`·`ContentTitleBar` import·렌더 검증.
7. `pnpm i` / `pnpm build` / `pnpm dev` 검증.
8. README — Node 20·pnpm 9.15.9·CW clone·link 전제 명시.

완료 기준: 버전 목표 충족 + `section-demo` dev 기동 + CW Toolbar link 렌더(실패 시 Known gap).

### 10.3 CW UI link (개발 중, 복사 금지)

```json
// apps/section-demo/package.json (또는 packages/components)
"@cloudwebviewer/core": "link:../../../cloudwebviewer/packages/core",
"@cloudwebviewer/core-types": "link:../../../cloudwebviewer/types/core"
```

- import 허용: `toolbar/Toolbar`·`ToolBtn`·store, `ContentTitleBar`, `common/*` 다이얼로그, `toolbar/type`.
- Section 전용 로직(Draw curve·B/L·9단면)은 `@ewoosoft/scp-section-*`에만.
- 금지: CW toolbar/common 소스(컴포넌트·store 로직) 복사, `@cloudwebviewer/core` 포크, Section 엔진을 CW core에 선행 머지.
- 예외(허용): **아이콘 SVG 에셋 복사** — 픽셀 일치용, 자기완결 에셋만(툴바 로직 제외). 데모 `apps/section-demo/src/cw/icons/`(cloudwebviewer `assets/icon`에서 복사, 수동 동기화). 접목 시 CW 네이티브 아이콘 사용.
- link 불가 시: Known gap 기록 → MUI + `#141414`·36px·hover `rgba(0,190,165,0.4)` 토큰으로 임시 상단 바 → link 해결 후 교체.

> 용도 구분: **link = 개발 중 우리 데모가 CW UI를 소비**. **embed = 제품이 우리 패키지를 소비**(§8.2). 방향이 반대인 두 정합이며 둘 다 유효.

---

## 11. PoC 없이 바로 구현 가능 (확정)

별도 PoC 없이 Section 모듈 구현을 시작한다.

- PoC에서 WebGL 3 Context·곡선·파노라마·9단면·기본 UI 검증됨.
- 기획 미확정 항목 전부 확정(B/L·접목·Save 포함).
- 남은 것(Overlay normal 5° 튜닝, Slice 스크롤 NFR)은 구현 초기 벤치마크로 처리.

유의:
1. **환경 정렬(§10) 선행** — 툴바·MUI 없이 기능만 먼저 넣지 않음.
2. **Section Slice 스크롤** — 최대 리스크. 착수 첫 주 수치 측정.
3. **Scout** — PoC 방식 유지, 접목 시 MPR Axial 교체(Spec 명시).
4. **B/L** — 확정 규칙(§6.2) 구현. feature flag 불필요.

---

## 12. 구현·인계 계획 (요약)

| 항목 | 내용 |
|------|------|
| 코드베이스 | `scp-section-poc` + 개발 중 CW Toolbar `pnpm link` |
| UI 정본 | `image23.png` + CW Toolbar/ContentTitleBar |
| 목표 | MMI v1.3.2 Section Layout을 CW look&feel 데모에서 재현 |
| 인계물 | `@ewoosoft/scp-section-*` 패키지·공개 API `SectionViewer`·데모 URL·embed 매핑·Known gaps |
| 인계 대상 | Cloud Web Viewer 담당 개발자 |
| 접목 | CW 팀이 CW 레포에서 embed(§8.2) |

---

## 13. 다음 작업 체크리스트 (현행)

| 순서 | 작업 | 담당 | 상태 |
|------|------|------|------|
| 0 | cloudwebviewer 레포 실조사(§9) | Raymond | **완료** |
| 1 | OnePager Spec v1.5 (MMI 매핑·접목 정합·B/L·Save·NFR) | Raymond | **완료** |
| 2 | B/L 자동 판정 기획 confirm | Jessi | **완료**(§6.2) |
| 3 | Spec 리뷰 공유 (VKS) | 기획 + CW Viewer | **진행** |
| 4 | scp-section-poc 환경 정렬(§10) | Raymond | **다음 (구현 전 필수)** |
| 5 | Section 모듈 구현 (MMI 전 기능, CW 툴바 연동) | Raymond | 대기 (목표 1주/예상 2주) |
| 6 | Slice 스크롤 성능 벤치마크 | Raymond | 구현 초기 |
| 7 | 인계 패키지 정리 | Raymond | 구현 완료 후 |
| 8 | embed·접목 | CW Viewer 팀 | 인계 후 |

---

## 14. Spec 산출물 — OnePager (완료)

Section 모듈 Spec은 **OnePager** 로 작성했다(장문 SRS 아님). 파일: `Section-Module-Spec-v1.3.2-OnePager.md` (v1.5, 8필드 + Technical Description §1~§12 + DoD). 팀 OnePager 템플릿 준수. MMI 1.1~1.14 매핑·접목 정합·B/L·Save·NFR 모두 반영 완료. 장문 SRS는 필요 시 OnePager 승인 후 확장.

---

## 15. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1~0.6 | 2026-07-09 | 초안 — 명칭·절차·범위, OnePager 형식, cloudwebviewer 분석, 환경 정렬, pnpm link, EzCloud |
| 0.7 | 2026-07-10 | §3 개발 레포 3방안 — 방안 1 확정. §3.7 Spec 정제 계획 |
| 0.8 | 2026-07-10 | 문서 폴더 재정리 — 경로 동기화 |
| **0.9** | **2026-07-13** | **전체 현행화**: §0 Decision Log 요약 신설(D1~D10). B/L **확정 규칙**(§6.2, P1→P2·C쪽=L·1회 고정). 접목 **D1**(vtk 미접목·WebGL embed) 반영 — §1·§8·§9 재작성. §9 cloudwebviewer **실조사**(Federation·vtk 스텁·prj 스키마·버전). Save **D5**(§8.3). 상태·§4 절차·§7·§13 체크리스트 현행화(Spec 완성·B/L 확정·다음=환경정렬·구현). §5 참조 org URL. §3.7(구 Spec 정제 계획)·과거 상태 표기 정리 |
