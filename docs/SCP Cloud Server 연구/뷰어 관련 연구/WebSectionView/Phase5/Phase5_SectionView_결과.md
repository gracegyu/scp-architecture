# Phase 5: Section View(9장 Cross-Section) 결과 보고

## 1. 개요

Phase 3 치열궁 곡선·Phase 4 파노라마에 이어, 사용자가 지정한 **Section 중심**을 기준으로 곡선에 **수직인 단면 9장**을 실시간 생성해 우측 3×3 그리드에 표시하는 PoC를 구현했다. CleverOne 등 상용 UI와의 배치·B/L 방향을 맞추기 위한 좌표 규약과, **표시 경로(WebGL2 / Canvas 2D)**·**연산 경로(JS / WASM 매번 복사 / WASM 상주)** 비교를 수행했다. **픽셀 생성 알고리즘(삼선형 보간·슬랩·윈도) 상세는 `Phase5_SectionView_OnePager.md` 알고리즘 절·아래 4.2절**을 본다.

---

## 2. 결과 화면

데모에서 CT 볼륨 로드 후 Scout·Panorama·Section이 동작하는 화면이다.

![Phase 5 Section View PoC 결과 화면](Screenshot.png)

스크린샷 예시 조건(화면 표시 기준):

- 샘플 볼륨: **496 × 496 × 399** (약 187 MB)
- 투영: **MIP(최댓값)**
- WC / WW: **3000 / 9100** (Scout·Section 공유, 파노라마는 별도 Pan WC/WW 가능)
- INT: **1.0 mm**
- Section 표시: **WebGL2**, 연산 모드 예시(WASM 경로): 툴바 **약 445 ms** (한 시점 값; **아래 3.1 절 표는 콘솔 다중 샘플 평균**과 다를 수 있음)

동일 조건에서 파노라마 1회 생성은 화면상 **약 132 ms** 수준으로, 9장 Section이 단일 파노라마 생성보다 무거운 작업임을 확인할 수 있다.

---

## 3. 성능 비교

### 3.1 연산 경로별 9장 생성 시간(콘솔 측정)

데모에서 **동일 볼륨·Scout/Panorama에서 Section 위치를 연속 변경**하며 `console.log`로 남긴 `{ "tag":"SectionGen", "mode", "ms" }` 샘플을 모아 산출했다. **`ms`는 JS·WASM 공통으로 `nU`/`nV` 확정 직후부터 9장 `ImageData`가 준비될 때까지**이다(JS: `buildCurveArcContext` 이전 단계 제외. WASM: 해당 구간에 **힙 레이아웃·`mem.grow`·(경로에 따라) 전체 볼륨 `Int16` 복사·곡선 버퍼·`sectionGenerate9`·RGBA→`ImageData` 복사** 포함. **`initSectionWasm`(최초 fetch/instantiate)은 제외**.)

| 연산 경로 | 표본 수 n | 평균 ms | 최소~최대 ms |
| --- | ---: | ---: | --- |
| **JS** (`generateSectionImagesData`) | 16 | **393.2** | 362.7 ~ 427.4 |
| **WASM (매번 복사)** (`generateSectionImagesDataWasm`) | 19 | **420.3** | 370.9 ~ 483.2 |
| **WASM (상주)** (`generateSectionImagesDataWasmResident`, 동일 `CTVolume` 참조) | 19 | **415.9** | 371.9 ~ 454.9 |

이번 세션에서는 **평균이 JS < WASM(상주) < WASM(매번 복사)** 순이었다. 구간을 맞춘 뒤 **매번 복사**에는 호출마다 **전체 볼륨 복사(~187MB)** 가 포함되어 평균·최댓값이 가장 크게 나오는 것이 타당하다. **상주**는 동일 참조에서 복사를 생략해 **복사 대비 평균 약 4ms 낮았**지만, 여전히 **JS 평균보다 약 23ms 높았**다(WASM 호출·메모리·JIT 대비 등). 표본마다 분산(`wasm-copy` 최대 483ms 등)이 커서 **더 긴 반복 측정**이 필요하다. 콘솔 **`setTimeout` handler long task** 경고는 **체감 지연**이 표의 ms보다 클 수 있음을 시사한다.

**정리:**

- **JS**는 볼륨을 WASM으로 옮기지 않고 **`volume.data` 제자리 샘플링**이라 동일 정의의 `elapsedMs`에서 유리한 편으로 나왔다.
- **WASM(복사) vs (상주)** 는 같은 WASM 글루 안에서 **복사 포함 여부**만 달라, 평균 차이로 **상주 이득**이 드러난다(이번 데이터 기준 약 4ms).
- **SIMD·Worker·프로파일러 기준 분해**는 별도 과제.

**시사점:** 연산 경로 선택은 **수치·메모리·향후 오프로드**를 함께 본다. “항상 WASM이 빠르다”는 이번 조건에서 성립하지 않는다.

### 3.2 WebGL2 vs Canvas 2D(표시)

- 두 경로 모두 **동일한 9장 `ImageData`** 를 소비한다.
- **시각적으로는 거의 차이를 느끼기 어렵다.** WebGL2 쪽이 **텍스처 선형 보간** 등으로 **아주 미세하게 더 부드러운 느낌**은 있을 수 있으나, **큰 차이는 없다**고 보는 것이 타당하다.
- PoC 목적은 “표시 파이프라인 검증 + 연속 갱신 시 부담 비교”에 가깝고, Section **해상도·연산**이 지배적인 경우 표시 방식만으로 체감이 크게 바뀌지는 않는다.

---

## 4. 개발 과정에서 정리한 기술 사항

### 4.1 볼륨 축·메타데이터(`dimensions`, `spacing`)

- `dimensions`: **`[columns, rows, sliceCount]`** 즉 **X(열)·Y(행)·Z(슬라이스 개수)** 를 의미한다.
- `spacing`: **`[pixelSpacingX, pixelSpacingY, sliceSpacing]`** (단위 mm). DICOM `Pixel Spacing`(보통 row\column 문자열)을 파싱한 뒤, 볼륨 메타에서는 **열·행 순으로 재배치**해 넣는다.
- **Z 간격(`spacing[2]`):** 인접 슬라이스 `Image Position Patient`의 **z 차이**를 우선 사용하고, 비정상이면 DICOM **`(0018,0088) Spacing Between Slices`** 로 보조한다. Axial 스택 물리 두께와 Section의 **세로(v) 샘플링**·파노라마 **행(z) 샘플링**에 직결된다.

### 4.2 Section 픽셀 알고리즘(보간~윈도)

**목표:** 치열궁에 **수직인 단면** 9장(각 `nU×nV`)의 **그레이스케일(윈도 후 RGBA)**. 수학·구현 상세는 **`Phase5_SectionView_OnePager.md` — 알고리즘: Section 픽셀 생성** 절을 본다.

**파이프라인(요지):**

1. 호장 `s_k`마다 `P_k`, `T̂_k`, `N̂_k` 계산. 단면은 **u∥`T̂_k`**, **v∥환자 Z**; 슬랩은 **`N̂_k`** 방향(Phase 4 파노라마 **한 열**의 평면·슬랩 정의와 혼동하지 말 것).
2. 각 출력 `(iu, j)`에서 **u·v(mm)** → 볼륨 내 3D 샘플점. 슬랩 스텝마다 **연속 복셀 좌표** `(fx, fy, fz)`로 변환.
3. **`sampleTrilinear`:** **삼선형(trilinear) 보간** — 감싸는 격자 **8꼭짓점** `Int16`을 읽어 x·y·z로 각각 선형 보간(최근접 이웃만 사용 아님, IDW 아님). **z도 연속**이라 인접 슬라이스 간 혼합이 포함된다. 구현: `packages/core/src/panorama/panorama.ts`; WASM 동일 수식: `packages/section-wasm/assembly/index.ts`.
4. 슬랩 내 HU에 **MIP / Mean / Percentile** → **Rescale** → **`windowToByte(WC, WW)`**. 출력 열 **법선 방향 반전**(`nU-1-iu`, B/L).

**데이터 레이아웃:**

- `sampleTrilinear` 인자 `(x,y,z)`는 각각 **열·행·슬라이스 인덱스의 연속값**(복셀 경계 내).
- `volume.data`는 **`[z * (cols*rows) + y * cols + x]`** 순서의 `Int16`이다.
- Scout Axial 곡선 제어점은 **현재 슬라이스**의 **픽셀 좌표**; 호장(mm)은 **in-plane spacing**으로 환산한다.

**Phase 4와의 관계:** `Phase4_Panorama_OnePager.md` §3 복셀 샘플링과 같이 **삼선형 보간 + 슬랩 + 투영**이라는 **값 읽기 방식**은 공유한다. Section은 **어떤 3D 점을 찍을지(단면+슬랩 축)** 가 다르다.

### 4.3 파노라마 “좌우(호장)” 확장·열 간격

- 파노라마는 곡선을 따라 **호장(mm) 간격**으로 열을 늘려 **가로 방향(치열궁 따라)** “확장”된다.
- 열 간격(mm)은 `panoramaColumnSpacingFromVolumeSpacing`에서 **`min(spacing[0], spacing[1])`** 로 둔다. **X·Y 픽셀 간격 중 더 촘촘한 쪽**에 맞추면, 한 열이 대략 **한 격자 스텝**과 비슷한 물리 스케일이 되도록 하기 위함이다. (둘 다 비정상이면 기본값 0.4 mm 등으로 폴백.)
- Section 생성 옵션에도 동일한 `panoramaColumnSpacingMm`이 넘어가나, **9장 자체의 u·v 격자**는 `sectionWidthMm`, `topMm/bottomMm`, `spacing`으로 별도 결정된다.

### 4.4 Section 단면 기하(파노라마와의 차이)

- 한 장의 단면 평면: **접선 `T̂`(u축, 치열궁 따라)** × **볼륨 스택 Z(v축)**. **법선 `N̂`** 는 Axial 평면 내에서 곡선에 수직이다.
- **슬랩 적분 축은 접선 방향**이다. 파노라마 열이 쓰는 평면과 동일해지지 않도록 한 것이 Phase 5 핵심 정정 사항이다(이전에는 단면이 “파노라마 조각”처럼 보이는 문제가 있었음).
- **CleverOne B/L 정렬:** 법선 방향 출력 열을 **좌우 반전**(`nU-1-iu`)하여 CleverOne 등 관례와 맞췄다(JS·WASM 동일).

### 4.5 UI·상태·동기화

- `sectionCenterMm`, INT, Top/Bottom(mm), WC/WW, 곡선, 슬라이스 인덱스, 투영·슬랩 옵션이 바뀌면 **짧은 지연(스로틀)** 후 9장을 재생성한다.
- 파노라마·Scout에서 **동일 `axialUi`** 로 Section 중심과 핸들을 공유한다.
- **Edit Curve** 모드에서는 Section 위치 픽이 막히도록 해 곡선 편집과 충돌을 줄였다.

### 4.6 개발 중 발견한 이슈·대응(요약)

| 이슈 | 내용 |
| --- | --- |
| WASM 404 | `public/section-wasm.wasm`이 없으면 `fetch` 실패 후 조용히 Section이 비어 보였음. **Vite 개발 서버에서 `packages/section-wasm/dist/section.wasm`을 직접 서빙**하는 플러그인으로 보완. |
| WebGL `bindTexture` 삭제 객체 | `sectionImages` 갱신 시 텍스처 cleanup과 `renderGrid`가 **같은 틱에서** 어긋나 **삭제된 텍스처**를 bind하는 레이스. **`texturesLiveRef`**로 업로드 직후 참조를 동기화해 해결. |
| `sectionCenterMm` 초기값 | 곡선이 유효해지기 전 `0`이면 9장이 잘못 겹칠 수 있어 **배치 전 `-1`** 등으로 “미배치”를 두고, 유효 곡선 시 **호장 중앙**으로 채움. |
| DICOM Z 간격 | IPP z 차이만으로는 spacing이 깨지는 데이터가 있어 **`Spacing Between Slices`** 태그를 보조로 사용. |

---

## 5. 결론

- **기능:** 9장 Cross-Section 실시간 생성·WebGL2/Canvas2D 표시·**JS / WASM(복사) / WASM(상주)** 연산 선택·CleverOne 방향에 가까운 B/L·파노라마·Scout와의 연동을 PoC 수준에서 달성했다.
- **성능:** 위 콘솔 샘플 기준 **평균 ms는 JS(약 393ms) < WASM 상주(약 416ms) < WASM 매번 복사(약 420ms)** 에 가까웠다. 상주는 복사 경로 대비 소폭 유리했으나 JS보다는 느렸다. `wasm-copy` 최댓값 등 분산이 커 추가 측정이 필요하다.
- **표시:** WebGL2와 Canvas2D는 **거의 차이 없음**, WebGL2가 **미세하게 부드러울 수 있음** 정도로 정리한다.
