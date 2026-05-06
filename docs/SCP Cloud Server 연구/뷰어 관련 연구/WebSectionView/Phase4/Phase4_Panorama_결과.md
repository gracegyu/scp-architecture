# Phase 4: 치열궁 곡선 기반 파노라마(Curved MPR) 연결 결과

## 개요

| 항목 | 내용 |
| --- | --- |
| 목표 | Phase 3 곡선·법선 정보로 메모리 CT Volume에서 파노라마용 2D `ImageData` 생성 후 Panorama 영역에 표시 |
| 기간 | 2026-05-05 ~ 2026-05-06 (PoC 구현 반영) |
| 상태 | 구현 완료(알고리즘·UI 연동, 후속 튜닝·성능 최적화는 별도) |
| 데모 사이트 | http://scp-section-demo.test.scp.esclouddev.com/ — 헤더 **CT Volume (Scout / Panorama)** 탭 → CT 로드 후 Panorama 상단 툴바 |
| 소스코드 | [Azure DevOps](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc) |
| 설계 상세 | [Phase 4: 치열궁 곡선 기반 파노라마(Curved MPR) 이미지 생성 기술 검증](https://vks.vatech.com/spaces/ESDEVELOPER/pages/303490289/Phase+4+%EC%B9%98%EC%97%B4%EA%B6%81+%EA%B3%A1%EC%84%A0+%EA%B8%B0%EB%B0%98+%ED%8C%8C%EB%85%B8%EB%9D%BC%EB%A7%88+Curved+MPR+%EC%9D%B4%EB%AF%B8%EC%A7%80+%EC%83%9D%EC%84%B1+%EA%B8%B0%EC%88%A0+%EA%B2%80%EC%A6%9D) |

![Phase 4 데모 화면 예](./Screenshot.png)

## 구현 결과

### 레이아웃·경로 변화 (Phase 3 대비)

Phase 3 결과 문서의 레이아웃은 유지되나, **Volume이 로드된 경우 Panorama 슬롯**은 다음처럼 동작한다.

| 조건 | Panorama 렌더링 |
| --- | --- |
| `volume == null` | Phase 1과 동일 — WebGL 쿼드 + 정적 `panorama.png` |
| `volume` + `axialUi` 있음 | **Canvas 2D** — `generatePanoramaImageData`의 `ImageData`를 소스 캔버스에 올린 뒤 표시 캔버스에 비율 유지 스케일 |

헤더 두 번째 탭은 **Phase 2~4 통합 뷰**로 CT를 올리면 Scout(Axial·곡선)·Panorama·Section 3×3이 한 그리드에 함께 나온다. 탭 이름만으로 Phase 번호가 나뉘지 않는다(`App.tsx` 주석 참고).

### UI 흐름

1. **CT Volume (Scout / Panorama)** 탭에서 CT 로드.
2. Scout에서 곡선 제어점 **2개 이상** 배치(Phase 3). 단, 스플라인 시각은 Phase 3과 같이 **3점 이상**일 때 풀 곡선 표시일 수 있으므로, 화질 비교 시에는 3점 이상 사용을 권장.

3. Panorama 툴바에서 **투영**(MIP / Mean / 백분위 50·60·70·80·90·95%) 선택 → **파노라마 생성** 클릭.

4. 툴바에 **마지막 생성 ms** 표시. 생성 중에는 버튼·투영 `<select>`·**Pan WC / Pan WW** 슬라이더 비활성.

5. **곡선·현재 Axial 슬라이스 인덱스·투영 프리셋**이 바뀌면 이미지는 그대로이므로, 반영하려면 다시 **파노라마 생성**을 누른다.

6. **WC/WW**: Scout 하단과 동일 상태(`useScoutAxialUi`). **최초 생성 성공 후** WC/WW만 바꾸면 **약 280ms 디바운스** 뒤 자동 재생성. CT(Volume)를 다시 로드하면 파노라마 비트맵·자동 재생성 플래그가 초기화된다.

### 기본 생성 옵션(Core)

`DEFAULT_PANORAMA_OPTIONS`(`packages/core/src/panorama/panorama.ts`):

| 필드 | 기본값 | 의미 |
| --- | --- | --- |
| `panoramaColumnSpacingMm` | 0.4 | 곡선 호장 방향 열 간격(mm) |
| `slabHalfWidthMm` | 3 | 법선 방향 슬랩 반폭(mm) |
| `slabSampleStepMm` | 0.5 | 슬랩 내부 샘플 스텝(mm) |
| `projection` | `mip` | MIP / mean / percentile |
| `percentile` | 0.9 | percentile 모드 시 비율(0~1); UI 프리셋이 덮어씀 |

### 주요 구현 모듈

#### 1. `packages/core/src/panorama/panorama.ts`

- **`buildPanoramaCurveSamples`**: 제어점 2개면 직선 구간 호장 샘플, 3개 이상이면 `sampleAtInterval`(Catmull-Rom 기반)으로 열 샘플 + 법선 생성.
- **`generatePanoramaImageData`**: 열×전체 슬라이스(`z`) 이중 루프, 슬랩마다 trilinear HU → `reduceSlabHu`(MIP·mean·백분위) → WC/WW로 0–255 그레이 RGBA `ImageData`. `performance.now()`로 경과 ms 반환.
- **`percentileFromSorted`**: 정렬 HU에 선형 보간 백분위.

#### 2. `packages/components/src/PanoramaView.tsx`

- Volume 없음: 기존 WebGL 정적 텍스처 경로.
- Volume+`axialUi`: 툴바(MIP/Mean/백분위, 생성 버튼, ms, Pan WC/WW) + `startGenerateAsync`로 Core 호출, WC/WW 디바운스 자동 재생성(`hadPanoramaRef` 등).

#### 3. `packages/components/src/hooks/useScoutAxialUi.ts`

- `sliceIndex`, `windowCenter`/`windowWidth`, `curveEditor`를 Scout·Panorama에 공유. Volume 바꿀 때 슬라이스·WC/WW를 메타데이터 기준으로 맞춤.

#### 4. `packages/components/src/SectionViewer.tsx`

- `useScoutAxialUi(volume)` 한 번만 호출해 `ScoutView`·`PanoramaView`에 동일 `axialUi` 전달.

## 성공 기준 달성 여부

| 기준 (OnePager 요약) | 달성 | 비고 |
| --- | --- | --- |
| 곡선·슬라이스·투영 변경 후 버튼으로 재생성 | O | 명시적 **파노라마 생성** |
| 치열궁을 따라 펼친 2D로 시각 판독 가능 수준 | O | 볼륨·곡선·윈도에 따라 상이; PoC 정성 평가 |
| Chrome 기준 생성 ~1초 목표 | 환경 의존 | **UI ms**로 케이스별 기록 가능; 미달 시 OnePager의 완화책(WASM 등) 검토 |
| MIP·Mean·백분위(50~95%) UI 선택 | O | 생성 시 반영; 프리셋만 변경 시에는 재클릭 필요 |
| WC/WW 반영 + (생성 후) 변경 시 디바운스 재생성 | O | Scout·Panorama 슬라이더 공유 |

## 알려진 제한·주의

- Phase 3 오버레이의 Section Cut **빨간 수직선** 길이와 Core **`slabHalfWidthMm`** 은 별도 개념일 수 있음(OnePager 참고).
- 좌표·방향은 PoC에서 **축 정렬 볼륨** 등 단순화를 가정; Image Orientation Patient 전개는 후속 과제.
- 클라이언트 단일 스레드 JS 루프이므로 큰 볼륨·촘촘한 Δs에서는 UI 멈춤이 길어질 수 있음.

## 다음 단계

- Phase 5: Section 9뷰와의 곡선·슬라이스 연동, 필요 시 GPU/Worker로 샘플링 이전 검토.
- 성능: 목표 ms 미달 시 `DEFAULT_PANORAMA_OPTIONS` 스윕·WASM(Phase 4 OnePager·메인 로드맵) 측정 비교.
