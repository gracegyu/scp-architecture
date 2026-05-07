# Phase 5: Section View(9장 Cross-Section) 결과 보고

## 1. 개요

Phase 3 치열궁 곡선·Phase 4 파노라마에 이어, 사용자가 지정한 **Section 중심**을 기준으로 곡선에 **수직인 단면 9장**을 실시간 생성해 우측 3×3 그리드에 표시하는 PoC를 구현했다. CleverOne 등 상용 UI와의 배치·B/L 방향을 맞추기 위한 좌표 규약과, **표시 경로(WebGL2 / Canvas 2D)**·**연산 경로(JavaScript / WebAssembly)** 비교를 수행했다.

---

## 2. 결과 화면

데모에서 CT 볼륨 로드 후 Scout·Panorama·Section이 동작하는 화면이다.

![Phase 5 Section View PoC 결과 화면](Screenshot.png)

스크린샷 예시 조건(화면 표시 기준):

- 샘플 볼륨: **496 × 496 × 399** (약 187 MB)
- 투영: **MIP(최댓값)**
- WC / WW: **3000 / 9100** (Scout·Section 공유, 파노라마는 별도 Pan WC/WW 가능)
- INT: **1.0 mm**
- Section 표시: **WebGL2**, 연산: **WASM**, 9장 생성 표시: **약 445 ms** (측정치는 환경·슬라이스·곡선 상태에 따라 변동)

동일 조건에서 파노라마 1회 생성은 화면상 **약 132 ms** 수준으로, 9장 Section이 단일 파노라마 생성보다 무거운 작업임을 확인할 수 있다.

---

## 3. 성능 비교

### 3.1 JavaScript vs WebAssembly(9장 생성 시간)

| 연산 경로 | 관측 범위(대표) |
| --- | --- |
| **JS** (`generateSectionImagesData`) | 약 **350~420 ms** |
| **WASM** (`sectionGenerate9` + 글루: 볼륨 복사·메모리·ImageData 구성) | 약 **390~450 ms** |

평균적으로 **JS가 약 10% 정도 빠른 것으로 관측**되었다. 이는 이 PoC 구조에서 충분히 나올 수 있는 결과다.

**WASM이 더 느리게 보이는 주요 요인(정리):**

- 매 생성 시(또는 메모리 정책상) **전체 볼륨 `Int16`을 WASM 선형 메모리로 복사**하는 비용이 크다. JS 경로는 `volume.data`를 **제자리**에서 trilinear 샘플링한다.
- `WebAssembly.Memory` **페이지 확장(grow)** 비용.
- 단일 스레드·단순 이중/삼중 루프 위주 핫패스는 브라우저 **JIT**에 유리한 경우가 많고, AssemblyScript WASM은 **SIMD·볼륨 상주 메모리 최적화 없이**는 역전되기 쉽다.
- 툴바에 표시되는 ms는 WASM 쪽이 **순수 `sectionGenerate9`만**이 아니라 **복사·호출 전후**를 포함하는 쪽에 가깝다(공정 분리 측정은 별도 프로파일이 필요).

**시사점:** “WASM이면 항상 빠르다”가 아니라, **현재 설계(매번 복사 + 동일 알고리즘)** 에서는 JS가 유리할 수 있다. 이득을 보려면 **볼륨을 한 번만 올려 재사용**, **Worker 이동(메인 스레드 체감)** , **SIMD/알고리즘 정리** 등 추가 작업이 필요하다.

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

### 4.2 샘플링 좌표와 데이터 레이아웃

- `sampleTrilinear`는 복셀 인덱스 **`(x, y, z)`** 에 대해 **열**은 `0..cols-1`, **행**은 `0..rows-1`, **z**는 `0..slices-1`의 **연속 좌표**로 보간한다.
- `volume.data`는 **`[z * (cols*rows) + y * cols + x]`** 순서의 `Int16`이다.
- Scout Axial 상의 곡선 제어점은 **현재 슬라이스 인덱스**의 **픽셀 좌표**이며, 호장(mm) 계산 시 **in-plane spacing**으로 mm로 환산한다.

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

- **기능:** 9장 Cross-Section 실시간 생성·WebGL2/Canvas2D 표시·JS/WASM 연산 선택·CleverOne 방향에 가까운 B/L·파노라마·Scout와의 연동을 PoC 수준에서 달성했다.
- **성능:** 동일 알고리즘 비교에서 **JS가 다소 유리**했고, 이는 **복사 비용·JIT·측정 구간**을 감안하면 자연스럽다. WASM의 이점은 **후속 최적화(상주 메모리·Worker·SIMD 등)** 에서 다시 평가하는 것이 맞다.
- **표시:** WebGL2와 Canvas2D는 **거의 차이 없음**, WebGL2가 **미세하게 부드러울 수 있음** 정도로 정리한다.

---

## 6. 참고 문서

- 기획·범위: [Phase5_SectionView_OnePager.md](./Phase5_SectionView_OnePager.md)
- 상위: [WebSectionView_PoC_OnePager.md](../WebSectionView_PoC_OnePager.md)
