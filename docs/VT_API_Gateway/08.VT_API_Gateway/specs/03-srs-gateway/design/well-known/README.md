# well-known 서버 구성 — 작성 가이드

API 버전 호환성 게이트(SRS §7.7, FR-COMPAT-02)가 런타임에 공시하는 **서버 구성 파일**의 샘플과 작성 규칙이다. 담당 개발자는 [`server-configuration.sample.json`](./server-configuration.sample.json)을 복사해 실제 값을 채운다.

## 1. 무엇인가

클라이언트(CleverOne·EzServer 등)가 **자신이 호환되는지 스스로 판단**하도록, GW가 "API/기능별 최소 클라이언트 버전·오류코드·fallback"을 공개하는 JSON이다. 구버전 클라이언트의 원인불명 실패를 제거하기 위한 단일 공시점이다(ADR-07).

## 2. 위치·서빙 (경로)

```
/.well-known/<env>/server-configuration.json
```

- `<env>`: 환경 구분(예 `production`·`staging`·`unstable`). 환경마다 별도 공시.
- 버전 프리픽스(`/v1`) 없이 표준 관례대로 노출한다(SRS §4.1.2-5 예외).
- 클라이언트는 캐시하며, GW는 변경 시 갱신한다(FR-COMPAT-02).

## 3. 스키마 필드

| 필드 | 타입 | 의미 |
| --- | --- | --- |
| `schemaVersion` | string | 본 구성 파일 스키마 버전(파서 호환용) |
| `env` | string | 환경 식별자(`production` 등) |
| `serverVersion` | string | GW 제품 버전(`gw/1.0.0.0`, ES 4-seg) |
| `generatedAt` | number | 생성 시각(Unix Timestamp ms, SRS §1.3) |
| `compatibility.apis[]` | array | **API 단위** 최소 호환 규칙 |
| `compatibility.features[]` | array | **기능 단위** 최소 호환 규칙 |

### `apis[]` / `features[]` 항목

| 필드 | 타입 | 의미 |
| --- | --- | --- |
| `id` | string | 안정적 식별자(API는 `리소스.동작`, 기능은 기능명). 변경 금지 |
| `path` | string | (apis만) 해당 엔드포인트 경로. `features`에는 없음 |
| `minClientVersion` | object | **제품(`Vatech-Product`)별** 최소 버전. 키=제품명, 값=semver 문자열 |
| `errorCode` | string | 미충족 시 반환할 표준 오류코드(SRS §7.7.4) |
| `fallback` | string | 사용자 안내 문구(예 "업데이트 필요") |

## 4. 작성 규칙

1. **단일 소스 원칙(FR-COMPAT-05)**: 본 파일이 아니라 **호환성 매트릭스가 SSOT**다. 매트릭스에서 본 JSON을 **생성**(빌드/CI)하고, 손으로 직접 편집하지 않는다. 매트릭스 위치는 ① API 호환성 One Pager(VKS)와 동기화.
2. **제품명 키**는 `Vatech-Product` 헤더 값과 정확히 일치시킨다(예 `CleverOne`·`EzServer`·`CleverSpace`).
3. **버전 표기**는 semver(`major.minor.patch`). 클라이언트 버전 비교는 semver 규칙을 따른다.
4. **`id`는 불변**으로 둔다. 경로(`path`)나 버전은 바뀌어도 `id`는 유지해 클라이언트 캐시·로깅 추적성을 보장한다.
5. **`errorCode`**는 §7.7.4 표준 오류코드 집합에서만 선택한다(임의 신설 금지).
6. **env별 분리**: `production`과 `staging`/`unstable`의 값이 다를 수 있으므로 환경마다 별도 파일을 생성한다.
7. **시간은 Unix ms**(SRS §1.3). 사람이 직접 넣지 말고 생성 시점에 자동 기입.

## 5. 채우는 순서 (담당 개발자)

1. `server-configuration.sample.json`을 복사한다.
2. `env`·`serverVersion`을 대상 환경/릴리스에 맞게 설정한다.
3. 호환성 매트릭스에서 API/기능별 `minClientVersion`을 가져와 채운다.
4. `errorCode`·`fallback`을 §7.7.4 표준에 맞춰 지정한다.
5. CI에서 매트릭스↔본 파일 일치를 검증(FR-COMPAT-05)하도록 파이프라인에 연결한다.

## 6. 참조

- SRS §7.7 API 버전 호환성 게이트 · §4.1.2-5 경로 컨벤션 · §7.7.4 오류코드
- 요구사항: FR-COMPAT-01~05
- 데이터 모델: `CompatMatrix`(api/feature, min_client_version, error_code, fallback) — API 명세·데이터 모델 문서
- ① API 호환성 One Pager(VKS) — 클라이언트측 적용·매트릭스 정본
