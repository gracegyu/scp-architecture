# PoC #1: Reverse Proxy 비교 및 선정

## Project Name

로컬 캐시 서버 Reverse Proxy 솔루션 비교 및 선정

## Date

2025-10-21 (예정)

## Submitter Info

Raymond

## Project Description

치과 클리닉용 로컬 캐시 서버의 핵심 컴포넌트인 Reverse Proxy 솔루션을 Nginx(OpenResty)와 Envoy 중에서 비교 검증한다. **기술 검증 목적**: 각 솔루션의 캐싱 성능, 확장성, 운영 복잡도를 측정하여 최적 솔루션을 선정하고 향후 프로덕션 개발 시 기술적 의사결정 근거를 확보한다.

**핵심 고려사항:**

- Reverse Proxy와 데이터 저장 구조 통합 방법 (외부 서비스 vs 내장 필터)
- 개발 언어 선택 (Go, C++, Lua)에 따른 성능/복잡성 트레이드오프
- 라이선스 호환성 및 상업적 사용 가능성

## Business and Marketing Justification

**PoC 검증 가치:**

- 기술적 의사결정 근거 확보 (Nginx vs Envoy)
- 성능/복잡성 트레이드오프 정량적 측정
- 향후 프로덕션 개발 시 기술 스택 확정

**선정 기준:**

- 캐시 기능 유연성 (TTL, 무효화, 조건부 캐싱)
- 동적 확장성 (Lua/필터를 통한 커스터마이징)
- 성능 (처리량, 지연시간, 리소스 사용)
- 운영 편의성 (설정, 모니터링, 디버깅)
- 커뮤니티 및 생태계 (문서, 라이브러리, 지원)
- **개발 언어 및 통합 아키텍처** (Go 외부 서비스 vs C++/Lua 내장)
- **라이선스 호환성** (상업적 사용, 수정/배포 권한)
- **Windows 설치 호환성** (바이너리 배포, 의존성, 서비스 등록)

**리스크:**

- 잘못된 선택 시 중간에 변경 비용이 매우 큼
- 각 솔루션의 학습 곡선과 팀 역량 고려 필요

## Risk Assessment

**기술 리스크:**

- Nginx: OpenResty Lua 학습 곡선, 동적 설정 제한
- Envoy: 복잡한 설정 구조, 상대적으로 적은 레퍼런스
- 공통: 캐시 정책 고도화 시 커스텀 개발 필요
- **개발 언어 선택**: Go vs C++/Lua 간 성능/복잡성 트레이드오프
- **통합 아키텍처**: 외부 서비스 vs 내장 필터 간 통신 오버헤드
- **Windows 설치 리스크**: Nginx/Envoy Windows 바이너리 안정성, 의존성 관리

**일정 리스크:**

- 각 솔루션 PoC 구현에 3-5일 소요 예상
- 성능 테스트 및 비교 분석 2-3일 추가

**완화 전략:**

- 명확한 평가 기준표 사전 작성
- 동일 시나리오로 공정 비교
- 필요 시 하이브리드(Nginx 캐시 + Envoy 라우팅) 검토

## Resource and Scheduling Details

**기간:** 2주 (Week 1-2)

**인력:**

- 개발자 1명 (Raymond) - Nginx/Envoy 검증 및 비교 분석

**일정:**

- Day 1-2: 요구사항 정리 및 평가 기준 수립
- Day 3-5: Nginx(OpenResty) PoC 구현 (Go 외부 서비스 + Lua 내장)
- Day 6-8: Envoy PoC 구현 (Go 외부 서비스 + C++ 필터)
- Day 9-10: 성능 비교 테스트 (통합 아키텍처별 성능 측정)
- Day 11-12: 분석 보고서 작성 및 의사결정 회의

**리소스:**

- 개발 서버 2대 (Nginx용, Envoy용)
- 부하 테스트 도구 (wrk, k6)
- S3/CloudFront 테스트 환경

## Technical Description

### 검증 범위

#### 1. 기본 Reverse Proxy 기능

- HTTP/HTTPS 프록시
- 업스트림 서버 연결 (CloudFront, API 서버)
- 커넥션 풀링 및 Keep-Alive
- 타임아웃 설정

#### 2. 치과 이미지 캐시 기능

- 디스크 캐시 설정 (파일시스템 기반)
- 캐시 키 설계 (clinicId + URI + 쿼리 + 버전)
- TTL 설정 (치과 이미지별 차등 TTL)
  - X-ray: 30일 (자주 참조)
  - CT: 14일 (치료 계획용)
  - 구강 스캔: 7일 (임시 데이터)
  - 썸네일: 30일
- 캐시 무효화 (환자별, 치료 단계별)
- Stale-while-revalidate 구현
- 조건부 캐싱 (ETag, Last-Modified)

#### 3. 동적 확장 및 커스터마이징

- **Nginx:** Lua 스크립트를 통한 TinyLFU 입소 필터 구현
- **Envoy:** Lua 필터 또는 WASM 확장을 통한 동일 기능 구현
- 동적 라우팅 (헤더/경로 기반)
- 인증 헤더 패스스루 (Authorization 제외한 캐시 키)
- **통합 아키텍처 검증**: 외부 Go 서비스 vs 내장 필터 성능 비교

#### 4. 치과 진료 무효화 API

- REST API를 통한 수동 무효화
- Webhook 수신 처리 (치료 완료, 예약 변경)
- 패턴 매칭 무효화 (환자ID/치료ID 단위)
- 치료 단계별 무효화 (진단 → 치료 → 완료)

#### 5. 관측성

- 캐시 상태 헤더 (X-Cache-Status: HIT/MISS/STALE)
- 메트릭 수집 (Prometheus 포맷)
- 액세스 로그 (구조화된 JSON)
- 에러 로그 및 디버깅

### 성능 테스트 시나리오

**시나리오 1: 캐시 HIT 성능**

- 동일 리소스 반복 요청 (10,000 req/s)
- 측정: 처리량, 지연시간(50/95/99p), CPU/메모리

**시나리오 2: 캐시 MISS 성능**

- 서로 다른 리소스 요청 (1,000 req/s)
- 측정: 프록시 오버헤드, 업스트림 연결 효율

**시나리오 3: 혼합 워크로드**

- HIT 80% + MISS 20% 혼합 (5,000 req/s)
- 측정: 실제 사용 패턴에서의 성능

**시나리오 4: 치과 이미지 파일**

- X-ray (1-5MB), CT (10-50MB), 구강 스캔 (5-20MB) 캐싱 및 서빙
- 측정: 메모리 사용량, 디스크 I/O, 치과 이미지별 성능

### 평가 기준표

| 항목               | 가중치 | Nginx | Envoy | 비고                |
| ------------------ | ------ | ----- | ----- | ------------------- |
| **기능성**         | 25%    |       |       |                     |
| - 캐시 유연성      | 10%    | ?     | ?     | TTL, 무효화, 조건부 |
| - 확장성           | 10%    | ?     | ?     | Lua/필터 개발       |
| - 무효화 API       | 5%     | ?     | ?     | REST API 구현       |
| **성능**           | 30%    |       |       |                     |
| - 캐시 HIT 처리량  | 10%    | ?     | ?     | req/s               |
| - 지연시간 (99p)   | 10%    | ?     | ?     | ms                  |
| - 리소스 효율      | 10%    | ?     | ?     | CPU/메모리          |
| **운영성**         | 25%    |       |       |                     |
| - 설정 편의성      | 10%    | ?     | ?     | 복잡도              |
| - 디버깅           | 5%     | ?     | ?     | 로그/추적           |
| - 모니터링         | 10%    | ?     | ?     | 메트릭 노출         |
| **개발/통합**      | 15%    |       |       |                     |
| - 개발 언어 적합성 | 8%     | ?     | ?     | Go/C++/Lua 지원     |
| - 통합 아키텍처    | 7%     | ?     | ?     | 외부/내장 방식      |
| **설치/배포**      | 10%    |       |       |                     |
| - Windows 호환성   | 5%     | ?     | ?     | 바이너리/의존성     |
| - 라이선스 호환성  | 5%     | ?     | ?     | 상업적 사용 가능    |
| **생태계**         | 5%     |       |       |                     |
| - 문서/커뮤니티    | 3%     | ?     | ?     | 자료 풍부도         |
| - 레퍼런스         | 2%     | ?     | ?     | 유사 사례           |
| **총점**           | 100%   | ?     | ?     |                     |

### 구현 샘플

#### Nginx(OpenResty) 샘플

```nginx
# 캐시 영역 정의
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=media:10g max_size=200g;

# TinyLFU 입소 필터 (Lua)
access_by_lua_block {
  local key = ngx.var.proxy_cache_key
  local freq = cms:inc(key, 1)
  if freq < 5 then
    ngx.var.no_cache = "1"
  end
}

# 치과 이미지 캐시 설정
location /xray/ {
  proxy_cache media;
  proxy_cache_key "$clinic_id:$uri:v1";
  proxy_cache_valid 200 30d;  # X-ray는 자주 참조
  proxy_cache_use_stale error timeout;
  add_header X-Cache-Status $upstream_cache_status;
  proxy_pass http://cloudfront;
}

location /ct/ {
  proxy_cache media;
  proxy_cache_key "$clinic_id:$uri:v1";
  proxy_cache_valid 200 14d;  # CT는 치료 계획용
  proxy_cache_use_stale error timeout;
  add_header X-Cache-Status $upstream_cache_status;
  proxy_pass http://cloudfront;
}

location /scan/ {
  proxy_cache media;
  proxy_cache_key "$clinic_id:$uri:v1";
  proxy_cache_valid 200 7d;   # 구강 스캔은 임시 데이터
  proxy_cache_use_stale error timeout;
  add_header X-Cache-Status $upstream_cache_status;
  proxy_pass http://cloudfront;
}
```

#### Envoy 샘플

```yaml
http_filters:
  - name: envoy.filters.http.lua
    typed_config:
      inline_code: |
        function envoy_on_request(handle)
          local freq = increment_frequency(handle:headers():get(":path"))
          if freq < 5 then
            handle:headers():add("cache-control", "no-store")
          end
        end
  - name: envoy.filters.http.cache
    typed_config:
      typed_config:
        cache_path: /var/cache/envoy
        max_size: 214748364800
```

### 예상 결과 및 의사결정 기준

**PoC 검증 목표:**

- Nginx vs Envoy 성능 비교 (처리량, 지연시간, 리소스 사용량)
- 개발 복잡도 측정 (설정, 커스터마이징, 디버깅)
- 운영 복잡도 평가 (모니터링, 장애 대응, 유지보수)

**PoC 성공 기준:**

- 명확한 성능 차이 측정 (10% 이상 차이 시 의미 있음)
- 개발/운영 복잡도 정량화 (시간/비용 측정)
- 기술적 의사결정 근거 문서화
- 향후 프로덕션 개발 가이드라인 제시

**의사결정:**

- PoC 결과 기반 솔루션 선정
- **개발 언어 및 통합 아키텍처** 검증 결과 반영
- **라이선스 호환성** 확인 (상업적 사용 가능)
- 프로덕션 개발 시 고려사항 정리

## 5. 개발 언어 및 통합 아키텍처 고려사항

### 5.1 Reverse Proxy와 데이터 저장 구조 통합 방법

**Nginx + 데이터 저장 구조:**

**방법 1: Nginx + 외부 Go 서비스 (권장)**

- **구조**: Nginx (프록시) + Go 서비스 (캐시 로직)
- **통신**: HTTP API 또는 Unix Socket
- **개발 언어**: Go (캐시 서비스)
- **장점**: 언어 독립성, 유지보수 용이, 확장성
- **단점**: 프로세스 간 통신 오버헤드

**방법 2: OpenResty (Nginx + Lua)**

- **구조**: Nginx 내장 Lua 스크립트로 캐시 로직 구현
- **개발 언어**: Lua (Nginx 내부)
- **장점**: 단일 프로세스, 고성능
- **단점**: Lua 학습 곡선, 복잡한 로직 구현 어려움

**방법 3: Nginx C 모듈**

- **구조**: C로 Nginx 모듈 직접 개발
- **개발 언어**: C
- **장점**: 최고 성능, Nginx와 완전 통합
- **단점**: C 개발 복잡성, 디버깅 어려움

**Envoy + 데이터 저장 구조:**

**방법 1: Envoy + 외부 Go 서비스 (권장)**

- **구조**: Envoy (프록시) + Go 서비스 (캐시 로직)
- **통신**: HTTP API 또는 gRPC
- **개발 언어**: Go (캐시 서비스)
- **장점**: 마이크로서비스 아키텍처, 확장성
- **단점**: 프로세스 간 통신 오버헤드

**방법 2: Envoy C++ 필터**

- **구조**: C++로 Envoy 필터 직접 개발
- **개발 언어**: C++
- **장점**: Envoy와 완전 통합, 고성능
- **단점**: C++ 개발 복잡성, Envoy 의존성

**방법 3: Envoy WASM 필터**

- **구조**: WebAssembly로 필터 개발
- **개발 언어**: Go → WASM 컴파일
- **장점**: 언어 독립성, 안전성
- **단점**: WASM 런타임 오버헤드, 제한된 API

### 5.2 권장 아키텍처 및 개발 언어

**권장 아키텍처: Reverse Proxy + 외부 Go 서비스**

```
┌─────────────────┐    HTTP/gRPC    ┌─────────────────┐
│   Nginx/Envoy   │ ←─────────────→ │   Go Cache      │
│   (프록시)      │                 │   Service       │
│                 │                 │                 │
│ - 요청 라우팅   │                 │ - 캐시 로직     │
│ - SSL 종료      │                 │ - 데이터 저장   │
│ - 로드밸런싱    │                 │ - 알고리즘      │
└─────────────────┘                 └─────────────────┘
```

**개발 언어 선택:**

**Go (권장) - 캐시 서비스:**

- **장점**: 고성능 I/O, 고루틴, 단일 바이너리
- **적합성**: 캐시 관리, HTTP 서버, 모니터링
- **통합**: Nginx/Envoy와 HTTP API로 통신

**C++ (고성능) - 필터 개발:**

- **장점**: 최고 성능, 프록시와 완전 통합
- **단점**: 개발 복잡성, 디버깅 어려움
- **적합성**: 단순한 캐시 로직만 구현 시

**Lua (OpenResty) - 내장 스크립트:**

- **장점**: Nginx 내부에서 직접 실행
- **단점**: 복잡한 로직 구현 어려움
- **적합성**: 기본적인 캐시 정책만 구현 시

### 5.3 라이선스 및 상업적 사용 고려사항

**Nginx 선택 시:**

- **라이선스**: 2-clause BSD License
- **상업적 사용**: 허용
- **수정/배포**: 허용
- **고지 의무**: 소스코드 제공 (요청 시)

**Envoy 선택 시:**

- **라이선스**: Apache License 2.0
- **상업적 사용**: 허용
- **수정/배포**: 허용
- **고지 의무**: 라이선스 파일 포함

**Go 언어:**

- **라이선스**: BSD 3-clause License
- **상업적 사용**: 허용
- **수정/배포**: 허용
- **고지 의무**: 저작권 고지 유지

### 5.4 Windows 설치 호환성 고려사항

**Nginx Windows 배포:**

- **바이너리**: 공식 Windows 바이너리 제공
- **의존성**: Visual C++ Redistributable 필요
- **서비스 등록**: nginx.exe를 Windows 서비스로 등록 가능
- **설정 파일**: nginx.conf Windows 경로 지원
- **포트 바인딩**: 관리자 권한 필요 (80/443 포트)

**Envoy Windows 배포:**

- **바이너리**: 공식 Windows 바이너리 제공
- **의존성**: Visual C++ Redistributable 필요
- **서비스 등록**: envoy.exe를 Windows 서비스로 등록 가능
- **설정 파일**: YAML 설정 파일 지원
- **포트 바인딩**: 관리자 권한 필요

**Go 서비스 Windows 배포:**

- **바이너리**: 단일 실행 파일로 컴파일 가능
- **의존성**: 런타임 의존성 없음
- **서비스 등록**: go-svc 라이브러리로 Windows 서비스 구현
- **설정 파일**: JSON/YAML 설정 파일 지원

### 다음 단계

선정된 솔루션과 개발 언어/통합 아키텍처로 PoC #4 통합 프로토타입 진행
