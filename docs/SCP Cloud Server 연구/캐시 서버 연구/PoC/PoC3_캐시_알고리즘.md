# PoC #3: 캐시 알고리즘 검증

## Project Name

로컬 캐시 서버 캐시 알고리즘 및 히트율 향상 전략 검증

## Date

2025-10-21 (예정)

## Submitter Info

Raymond

## Project Description

로컬 캐시 서버의 캐시 알고리즘을 검증한다.

**기술 검증 목적**: LRU, SLRU, TinyLFU, 의료 특화 알고리즘 등 다양한 캐시 정책의 성능을 비교 측정하여 최적 알고리즘을 선정하고, 향후 프로덕션 개발 시 캐시 전략을 확정한다.

## Business and Marketing Justification

**PoC 검증 가치:**

- 캐시 알고리즘별 성능 비교 (히트율, 메모리 사용량, 처리 지연)
- 치과 진료 패턴에 맞는 최적 캐시 전략 도출
- 향후 프로덕션 개발 시 캐시 알고리즘 선택 근거 확보

**핵심 목표:**

- 요청 기준 히트율: 80% 이상
- 바이트 기준 히트율: 70% 이상
- 오리진 트래픽 감소: 60% 이상

**알고리즘 후보:**

- LRU (Least Recently Used): 기본 알고리즘
- SLRU (Segmented LRU): 핫/콜드 세그먼트 분리
- TinyLFU: 빈도 기반 입소 필터 (Window-TinyLFU)
- 하이브리드: W-TinyLFU + SLRU
- **의료 특화**: 진료 일정 기반 우선순위 캐싱
- **응급 우선**: 응급도별 캐시 우선순위
- **진료진 맞춤**: 의사별 환자 선호도 기반 캐싱

**Windows 설치 호환성:**

- 알고리즘 라이브러리 배포 (Go/Python/C++)
- 의존성 관리 (수학 라이브러리, 메모리 관리)
- 서비스 등록 및 설정 파일 관리

## Risk Assessment

**기술 리스크:**

- TinyLFU 구현 복잡도 (Count-Min Sketch, Bloom Filter)
- 메모리 오버헤드 (빈도 카운터 유지)
- 프로덕션 환경에서 실제 효과 검증 필요
- **Windows 설치 리스크**: 알고리즘 라이브러리 Windows 바이너리 안정성, 의존성 관리

**성능 리스크:**

- 입소 필터 계산이 지연 증가
- 빈도 카운터 갱신이 동시성 저하
- 세그먼트 관리 오버헤드

**완화 전략:**

- 시뮬레이션으로 사전 검증
- 단계적 적용 (LRU → SLRU → TinyLFU)
- 오버헤드 측정 및 튜닝

## Resource and Scheduling Details

**기간:** 2주 (Week 1-2, PoC #1, #2와 병렬)

**인력:**

- 개발자 1명 (Raymond) - 알고리즘 구현, 시뮬레이션 및 분석

**체크리스트(작업 순서):**

- [x] 실제 접근 패턴 데이터 수집/분석(익명화, Zipf 계수/크기 분포 산출)
- [x] 시뮬레이터 구현(LRU/SLRU/TinyLFU/W-TinyLFU 플러그 가능 구조)
- [x] 알고리즘별 시뮬레이션/측정(요청/바이트 히트율, 메모리 OH, 지연)
- [x] 프리페칭 전략 검증(환자/슬라이스/시간/예측 기반, 오버헤드 포함)
- [x] 파라미터 튜닝 및 보고서(임계치/세그먼트 비율, 효과/복잡도 트레이드오프)

**리소스:**

- 실제 로그 데이터 (익명화된 접근 패턴)
- 시뮬레이션 환경 (Python/Go)
- 분석 도구 (Jupyter Notebook)

## Technical Description

### 검증 대상

#### 1. 캐시 알고리즘 비교

**알고리즘 A: LRU (Baseline)**

```
- 입소: 무조건 허용
- 유지: 최근 사용 순서
- 제거: 가장 오래된 항목
```

**알고리즘 B: Segmented LRU**

```
- Probation (20%): 신규 진입, 빠른 제거
- Protected (80%): 재접근 항목, 오래 유지
- 승격: Probation에서 재접근 시 Protected로
```

**알고리즘 C: Window-TinyLFU**

```
- Window Cache (1%): 최근 항목 임시 보관
- Main Cache (99%): 빈도 기반 유지
- 입소 필터: 빈도 임계치 미만 거부
- Count-Min Sketch: 빈도 추정 (메모리 효율)
```

**알고리즘 D: 하이브리드 (W-TinyLFU + SLRU)**

```
- 입소: TinyLFU 필터 (임계치: 5회)
- Window Cache (1%): 최근 항목
- Main Cache (99%): SLRU (Probation 20% + Protected 80%)
- 승격: Probation → Protected (재접근 시)
```

**알고리즘 E: 의료 특화 우선순위 캐싱**

```
- 우선순위 1: 당일 예약 환자 (응급도 높음)
- 우선순위 2: 최근 3일 진료 환자 (빈도 높음)
- 우선순위 3: 진료진별 선호 환자 (개인화)
- 우선순위 4: 일반 환자 (LRU 기반)
- 동적 조정: 진료 일정 변경 시 우선순위 재계산
```

**알고리즘 F: 응급도 기반 캐싱**

```
- 응급도 1: 응급실 환자 (즉시 접근, 절대 제거 안됨)
- 응급도 2: 당일 수술 환자 (높은 우선순위)
- 응급도 3: 당일 예약 환자 (중간 우선순위)
- 응급도 4: 일반 예약 환자 (낮은 우선순위)
- 응급도 5: 과거 환자 (LRU 기반)
```

#### 2. 접근 패턴 분석

**실제 데이터 수집:**

- 클리닉 A: 환자 50명, 스터디 200개, 7일간 로그
- 클리닉 B: 환자 100명, 스터디 500개, 30일간 로그

**패턴 특성:**

- Zipf 분포: 상위 20% 항목이 80% 접근
- Temporal Locality: 최근 진료 환자 집중 조회
- Spatial Locality: 동일 환자의 여러 스터디 연속 조회
- One-hit-wonders: 1회만 조회되는 항목 비율

**의료 데이터 특수성:**

- **진료 일정 기반 접근**: 당일 예약 환자 데이터 우선 캐싱
- **응급 상황 우선순위**: 응급 환자 데이터 즉시 접근 가능
- **진료과별 패턴**: 내과/외과/영상의학과별 다른 접근 패턴
- **계절성**: 특정 질병의 계절적 발생 패턴
- **진료진별 선호도**: 의사별 자주 보는 환자/스터디 패턴

**패턴 카테고리:**

- 핫 데이터: 최근 3일 환자 (20%), 접근 빈도 높음
- 웜 데이터: 1주~1개월 환자 (30%), 가끔 조회
- 콜드 데이터: 1개월 이상 환자 (50%), 드물게 조회

#### 3. 프리페칭 전략

**전략 1: 환자 기반 프리페칭**

- 환자 진입 시 모든 썸네일 프리페치
- 대표 프리뷰 N개 프리페치 (N = 3~5)

**전략 2: 슬라이스 기반 프리페칭**

- 슬라이스 i 조회 시 주변 i±k 프리페치 (k = 5~10)
- 방향성 고려 (순방향/역방향)

**전략 3: 시간 기반 프리페칭**

- 최근 N명 환자 썸네일 (N = 10~20)
- 최근 M일 스터디 프리뷰 (M = 3~7)

**전략 4: 예측 기반 프리페칭**

- 진료 일정 연동 (당일 예약 환자)
- 이전 접근 패턴 기반 (환자 A 후 B 조회 확률)

**전략 5: 의료 특화 프리페칭**

- **진료 일정 기반**: 당일 예약 환자 전체 데이터 프리페치
- **진료진별 패턴**: 의사별 자주 보는 환자 유형 프리페치
- **응급 상황 대비**: 응급실 환자 데이터 항상 캐시 유지
- **진료과별 특성**: 내과(혈액검사), 외과(CT/MRI), 안과(안저촬영) 등
- **시간대별 패턴**: 오전(일반진료), 오후(수술), 야간(응급) 프리페치

### 시뮬레이션 설계

#### 시뮬레이터 구조

```python
class CacheSimulator:
    def __init__(self, algorithm, capacity):
        self.algorithm = algorithm  # 'LRU', 'SLRU', 'TinyLFU', 'Hybrid'
        self.capacity = capacity
        self.cache = {}
        self.stats = {'hit': 0, 'miss': 0, 'byte_hit': 0, 'byte_miss': 0}

    def access(self, key, size):
        if self.algorithm.contains(key):
            self.stats['hit'] += 1
            self.stats['byte_hit'] += size
            self.algorithm.on_hit(key)
        else:
            self.stats['miss'] += 1
            self.stats['byte_miss'] += size
            if self.algorithm.should_admit(key):
                self.algorithm.admit(key, size)

    def get_hit_rate(self):
        total = self.stats['hit'] + self.stats['miss']
        return self.stats['hit'] / total if total > 0 else 0

    def get_byte_hit_rate(self):
        total = self.stats['byte_hit'] + self.stats['byte_miss']
        return self.stats['byte_hit'] / total if total > 0 else 0
```

#### 테스트 시나리오

**시나리오 1: 실제 접근 패턴 리플레이**

- 수집한 로그를 순서대로 재생
- 캐시 크기별 히트율 측정 (50GB, 100GB, 200GB)

**시나리오 2: 합성 Zipf 패턴**

- Zipf(s=1.2) 분포로 접근 생성
- 10만 개 항목, 100만 번 접근

**시나리오 3: One-hit-wonder 테스트**

- 50% 항목이 1회만 접근
- TinyLFU 필터 효과 검증

**시나리오 4: 시간 지역성 테스트**

- 최근 접근 항목 재접근 확률 80%
- SLRU 세그먼트 효과 검증

**시나리오 5: 프리페칭 효과**

- 프리페칭 없음 vs 환자 기반 vs 슬라이스 기반
- 히트율 향상 및 오버헤드 측정

**시나리오 6: 의료 특화 알고리즘 검증**

- 진료 일정 기반 우선순위 캐싱 효과
- 응급도별 캐시 우선순위 성능
- 진료진별 개인화 캐싱 효과

**시나리오 7: 실제 클리닉 워크플로우 시뮬레이션**

- 오전 진료 시간대 (9-12시) 접근 패턴
- 오후 수술 시간대 (14-17시) 접근 패턴
- 야간 응급실 시간대 (18-09시) 접근 패턴
- 주말/공휴일 특수 상황 패턴

### TinyLFU 구현 상세

#### Count-Min Sketch

```python
import hashlib

class CountMinSketch:
    def __init__(self, width=1000000, depth=5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]

    def _hash(self, key, seed):
        h = hashlib.md5(f"{key}:{seed}".encode()).hexdigest()
        return int(h, 16) % self.width

    def increment(self, key):
        for i in range(self.depth):
            j = self._hash(key, i)
            self.table[i][j] += 1

    def estimate(self, key):
        estimates = []
        for i in range(self.depth):
            j = self._hash(key, i)
            estimates.append(self.table[i][j])
        return min(estimates)  # Conservative estimate
```

#### Window-TinyLFU 알고리즘

```python
class WindowTinyLFU:
    def __init__(self, capacity, window_size=0.01):
        self.capacity = capacity
        self.window_size = int(capacity * window_size)
        self.main_size = capacity - self.window_size

        self.window = LRUCache(self.window_size)
        self.main = SLRUCache(self.main_size)
        self.sketch = CountMinSketch()
        self.threshold = 5

    def access(self, key, size):
        self.sketch.increment(key)

        if self.window.contains(key):
            return True  # HIT in window

        if self.main.contains(key):
            return True  # HIT in main

        # MISS: Try to admit
        freq = self.sketch.estimate(key)
        if freq >= self.threshold:
            self.window.put(key, size)
            if self.window.is_full():
                evicted = self.window.evict()
                self.main.put(evicted)
        return False
```

### 평가 지표

**기본 지표:**

- 요청 히트율 = HIT / (HIT + MISS)
- 바이트 히트율 = HIT_BYTES / (HIT_BYTES + MISS_BYTES)
- 오리진 비율 = 1 - 바이트 히트율

**추가 지표:**

- 입소율 = 입소 항목 / 접근 항목 (TinyLFU 필터 효과)
- 오버헤드 = 메모리 사용 / 캐시 크기
- 지연 증가 = 필터 계산 시간

### 벤치마크 결과 템플릿

| 알고리즘 | 캐시 크기 | 요청 히트율 | 바이트 히트율 | 입소율 | 메모리 OH | 지연 | 의료 특화 |
| -------- | --------- | ----------- | ------------- | ------ | --------- | ---- | --------- |
| LRU      | 100GB     | ?           | ?             | 100%   | 1x        | 0ms  | ❌        |
| SLRU     | 100GB     | ?           | ?             | 100%   | 1.1x      | 0ms  | ❌        |
| TinyLFU  | 100GB     | ?           | ?             | ?%     | 1.2x      | ?ms  | ❌        |
| Hybrid   | 100GB     | ?           | ?             | ?%     | 1.3x      | ?ms  | ❌        |
| 의료특화 | 100GB     | ?           | ?             | ?%     | 1.4x      | ?ms  | ✅        |
| 응급우선 | 100GB     | ?           | ?             | ?%     | 1.5x      | ?ms  | ✅        |

**프리페칭 효과:**

| 전략          | 히트율 향상 | 대역폭 증가 | 지연 감소 | 의료 특화 | 권장     |
| ------------- | ----------- | ----------- | --------- | --------- | -------- |
| 없음          | -           | -           | -         | ❌        | Baseline |
| 환자 기반     | +?%         | +?%         | -?ms      | ❌        | ?        |
| 슬라이스 기반 | +?%         | +?%         | -?ms      | ❌        | ?        |
| 시간 기반     | +?%         | +?%         | -?ms      | ❌        | ?        |
| 진료일정 기반 | +?%         | +?%         | -?ms      | ✅        | ?        |
| 응급대비      | +?%         | +?%         | -?ms      | ✅        | ?        |

### 파라미터 튜닝

**TinyLFU 파라미터:**

- 임계치 (threshold): 3, 5, 10 비교
- Window 크기: 1%, 5%, 10% 비교
- CM Sketch 크기: 100만, 500만, 1000만 비교

**SLRU 파라미터:**

- Probation 비율: 10%, 20%, 30% 비교
- 승격 정책: 즉시 vs 2회 재접근

**TTL 파라미터:**

- 썸네일: 7일, 14일, 30일 비교
- 프리뷰: 1일, 3일, 7일 비교
- 메타: 5분, 10분, 15분 비교

**의료 특화 파라미터:**

- **응급도별 TTL**: 응급실(24시간), 당일수술(12시간), 일반예약(6시간)
- **진료진별 캐시**: 의사별 선호 환자 캐시 유지 기간 (1일, 3일, 7일)
- **진료과별 우선순위**: 내과(1.0), 외과(1.2), 영상의학과(1.5), 응급실(2.0)
- **시간대별 가중치**: 오전(1.0), 오후(1.1), 야간(1.3), 주말(0.8)

### 예상 결과 및 의사결정 기준

**검증 목표:**

- 각 캐시 알고리즘별 성능 측정 (히트율, 메모리 오버헤드, 처리 지연)
- 치과 진료 패턴 시뮬레이션을 통한 실제 효과 검증
- 알고리즘 복잡도 vs 성능 향상 트레이드오프 분석

**PoC 성공 기준:**

- 명확한 성능 차이 측정 (5% 이상 차이 시 의미 있음)
- 알고리즘별 장단점 정량화
- 치과 특화 알고리즘의 실제 효과 검증
- 기술적 의사결정 근거 문서화

**의사결정:**

- PoC 결과 기반 최적 알고리즘 선정
- 치과 진료 패턴에 맞는 캐시 전략 도출
- 향후 프로덕션 개발 시 알고리즘 선택 가이드라인 제시

## 5. 개발 언어 고려사항 (Rust 우선)

### 5.1 캐시 알고리즘 구현 언어

**Rust (권장):**

- **장점**: 메모리 안전성 + 고성능, lock-free/async 패턴 용이
- **적합성**: Count-Min Sketch, LRU/LFU, TinyLFU 입소 필터
- **라이브러리**: hashbrown, crossbeam, tokio, probabilistic DS 구현체

**Python (프로토타입):**

- **장점**: 빠른 개발, 풍부한 수학 라이브러리
- **적합성**: 알고리즘 시뮬레이션, 데이터 분석
- **라이브러리**: numpy, collections, heapq

**C++ (고성능):**

- **장점**: 최고 성능, 메모리 직접 제어
- **적합성**: 대용량 데이터 처리, 실시간 성능
- **단점**: 개발 복잡성, 디버깅 어려움

### 5.2 성능 측정 도구 언어

**Rust (권장):**

- **장점**: criterion.rs 기반 마이크로벤치마크, tokio-console/pprof
- **적합성**: 알고리즘/HTTP 경로 벤치마크, 프로파일링

**Python (분석):**

- **장점**: 데이터 시각화, 통계 분석
- **라이브러리**: matplotlib, pandas, scipy

### 5.3 라이선스 고려사항

**Rust 언어:**

- **라이선스**: Apache-2.0 / MIT (듀얼)
- **상업적 사용**: ✅ 허용
- **수정/배포**: ✅ 허용
- **고지 의무**: ✅ 라이선스 고지 유지

**Python:**

- **라이선스**: Python Software Foundation License
- **상업적 사용**: ✅ 허용
- **수정/배포**: ✅ 허용
- **고지 의무**: ✅ 라이선스 파일 포함

**NumPy/SciPy:**

- **라이선스**: BSD 3-clause License
- **상업적 사용**: ✅ 허용
- **수정/배포**: ✅ 허용
- **고지 의무**: ✅ 저작권 고지 유지

**C++ (STL):**

- **라이선스**: MIT License (일부), Public Domain
- **상업적 사용**: ✅ 허용
- **수정/배포**: ✅ 허용
- **고지 의무**: ❌ 없음 (Public Domain)

### 5.4 Windows/Linux 설치 호환성 고려사항

**Rust 알고리즘 서비스 Windows 배포:**

- **바이너리**: 단일 실행 파일로 컴파일 가능 (MSVC toolchain)
- **의존성**: 런타임 의존성 없음
- **서비스 등록**: windows-service/NSSM 사용

**Python 알고리즘 라이브러리 Windows 배포:**

- **바이너리**: PyInstaller로 단일 실행 파일 생성 가능
- **의존성**: Python 런타임 + NumPy/SciPy
- **수학 라이브러리**: NumPy, SciPy (BSD 라이선스)
- **서비스 등록**: python-windows-service 라이브러리 사용

**C++ 알고리즘 라이브러리 Windows 배포:** **Rust 알고리즘 서비스 Linux 배포:**

- **배포**: 단일 바이너리 + systemd 서비스
- **프로파일링**: perf/pprof, eBPF 기반 추적
- **컨테이너**: Docker/Podman 이미지 제공

- **바이너리**: 정적 링크 또는 DLL 형태
- **의존성**: Visual C++ Redistributable 필요
- **수학 라이브러리**: STL 내장 또는 Eigen (MPL2 라이선스)
- **서비스 등록**: Windows Service API 직접 사용

### 다음 단계

최적 알고리즘과 파라미터를 PoC #4 통합 프로토타입에 적용
