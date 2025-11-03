# PoC #1 결과(진행중): Reverse Proxy 비교 및 선정

## 1) 요구사항 및 평가 기준 확정

- 범위: 치과 클리닉용 로컬 캐시 서버의 Reverse Proxy 후보(Nginx/OpenResty, Envoy, Pingora)의 기술 검증 및 비교
- 기능 요구: HTTP/HTTPS 프록시, 디스크 캐시, TTL/무효화, 조건부 재검증(ETag/Last-Modified), SWR, 관측성(메트릭/로그)
- 통합 요구: Rust 외부 서비스(캐시 정책/무효화/관리 API) 연동, Windows(NSIS)와 Linux(CacheBox) 배포 경로 지원
- 성능 지표: 처리량(req/s), 지연(50/95/99p), 리소스(CPU/메모리), 디스크 I/O, 캐시 HIT/MISS/STALE 비율
- 운영성 지표: 설정/디버깅/모니터링 편의, 장애대응 시나리오(폴백/오프라인), 업데이트/롤백 용이성
- 설치/배포: Windows 호환성(NSIS), Linux(systemd/Docker, CacheBox), 의존성/서비스 등록
- 라이선스: 상업적 사용 가능 여부, 고지 의무 준수 용이성
- 평가표 가중치: 기능성 25% / 성능 30% / 운영성 25% / 개발·통합 15% / 설치·배포 10% / 생태계 5% (세부 항목은 본 PoC1 문서 표와 동일)

테스트 시나리오(공통)

- HIT 성능: 동일 리소스 반복 요청 → 처리량/지연
- MISS 성능: 서로 다른 리소스 요청 → 프록시/업스트림 오버헤드
- 혼합: HIT 80% + MISS 20%
- 치과 파일형태: X-ray(1–5MB), CT(10–50MB), 구강스캔(5–20MB), 썸네일(50–200KB)

상태: 요구사항/평가 기준 확정 완료

---

## 2) Nginx(OpenResty) PoC 구현

환경

- OS: Windows Server 2022(NSIS 배포 경로 검증), Linux(Ubuntu 22.04, CacheBox 시범)
- 프록시: Nginx(OpenResty) 기본 프록시 + 디스크 캐시
- 연동: Rust 외부 서비스(무효화/관리 API) 연동 계획, 초기 단계는 Nginx 캐시 중심

핵심 설정(요약)

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=media:10g max_size=200g;

map $http_x_clinic_id $clinic_id { default "anon"; }
set $policy_version "v1";
proxy_cache_key "$clinic_id:$uri:$policy_version";

location /xray/   { proxy_cache media; proxy_cache_valid 200 30d; proxy_pass http://cloudfront; }
location /ct/     { proxy_cache media; proxy_cache_valid 200 14d; proxy_pass http://cloudfront; }
location /scan/   { proxy_cache media; proxy_cache_valid 200 7d;  proxy_pass http://cloudfront; }
location /thumb/  { proxy_cache media; proxy_cache_valid 200 30d; proxy_pass http://cloudfront; }

add_header X-Cache-Status $upstream_cache_status always;
```

Lua 정책(입소 필터 스케치)

```nginx
access_by_lua_block {
  local key = ngx.var.proxy_cache_key
  local freq = cms and cms:inc(key, 1) or 10  -- PoC 단계: 임계치 우회 가능
  if freq < 5 then ngx.var.no_cache = "1" end
}
```

### 실행/검증 기록 (macOS, 2025-11-03)

- 개발 환경: macOS (Docker Desktop)
- 실행 위치: `scp-cache-poc/poc1/nginx-openresty`
- 구성: OpenResty(프록시/디스크 캐시), Origin(정적 샘플), Rust 외부 서비스 스텁(`/health`, `/metrics`, `/cache/invalidate`)
- 참고: 상세 실행/트러블슈팅은 `poc1/nginx-openresty/README.md`

실행

```
cd /Users/gracegyu/Documents/Azure/scp-cache-poc/poc1/nginx-openresty
docker compose up -d --build
```

스모크(예상 헤더 확인: MISS→HIT, STALE)

```
bash scripts/smoke.sh
```

수동 확인 예시

```
curl -s -D - http://localhost:8080/ -o /dev/null | grep -i '^X-Cache-Status'
curl -s -D - http://localhost:8080/assets/sample.jpg -o /dev/null | grep -i '^X-Cache-Status'
```

관측 결과

```
X-Cache-Status: MISS
X-Cache-Status: HIT
```

테스트 결과

- 첫 요청: `X-Cache-Status: MISS`, 두 번째: `X-Cache-Status: HIT` 확인
- 이미지(`sample.jpg`) 동일 동작 확인
- Rust 외부 서비스(`http://localhost:3100/health`, `/metrics`) 정상 동작 확인
- 원본 중단 시 캐시된 응답 서빙 확인(`X-Cache-Status: HIT` 유지)
- 스모크 스크립트 자동 실행 정상 동작

성능 벤치마크 결과(초기 리허설, 2025-11-03)

k6 벤치마크 스크립트: `scp-cache-poc/bench/k6/nginx-openresty/`

시나리오 1: 캐시 HIT 성능

- 테스트: 30초, 50 VUs
- 처리량: 461 req/s
- 지연(95p): 12.5ms
- 지연(99p): 12.5ms
- 에러율: 0%

시나리오 2: 캐시 MISS 성능

- 테스트: 30초, 20 VUs
- 처리량: 91 req/s
- 지연(95p): 24.8ms
- 지연(99p): 24.8ms
- 에러율: 0%

메모

- HIT 처리량이 MISS에 비해 약 5배 높음
- 더미 워크로드 기준이며, 실제 치과 이미지(1-50MB) 워크로드에서는 처리량이 낮아질 가능성
- 향후 Envoy/Pingora와 동일 시나리오로 비교 예정

트러블슈팅

- OpenResty alpine 이미지 권한 이슈: `user nginx` 제거, 로그는 `stderr`로 처리
- docker-compose `version` 필드 제거(경고 없앰)
- 포트 충돌: Rust 서비스 3000 → 호스트 3100 매핑

진행 현황

- 기본 프록시/디스크 캐시 동작 및 TTL 적용 확인 완료(macOS 환경)
- Lua 접근 필터 스텁 배선 완료, 정책/임계치 로직 확장 가능
- Rust 외부 서비스 스텁(`/health`, `/metrics`, `/cache/invalidate`) 구현 및 동작 확인
- 스모크 스크립트 준비 및 검증 완료
- k6 벤치마크 스크립트 준비 및 초기 실행 완료

검증 체크리스트

- [x] 기본 프록시 라우팅/업스트림 연결 확인(origin 컨테이너)
- [x] 디스크 캐시 동작(HIT/MISS 헤더) 확인
- [x] 이미지 타입별 TTL 적용 확인(sample.jpg: 30분)
- [x] Lua 입소 필터 스텁 배선 확인(정책 확장 가능)
- [x] Rust 외부 서비스 스텁 구현 및 동작 확인
- [x] 스모크 스크립트 준비 및 실행 검증
- [x] k6 벤치마크 스크립트 준비 및 리허설 완료

메모

- 초기 단계는 Nginx 디스크 캐시와 경로별 TTL로 치과 워크로드 최적화에 집중
- Rust 외부 서비스는 무효화/통계/관리 API 제공(후속 단계에서 연결 및 측정)
- macOS 환경에서 Docker 컨테이너 기반 PoC 검증 완료
- 커스텀 캐시 정책/임계치 로직은 Lua 필터 확장으로 구현 예정

상태: macOS PoC 기본 검증 완료, 벤치마크 테스트 대기 중

---

다음 단계(이 문서 범위)

- Envoy PoC 구현 및 동일 시나리오 측정
- Pingora PoC(CacheBox/Linux) 기본 경로 검증
- 공통 부하 시나리오로 3자 비교(기능/성능/운영성/설치·배포/생태계)
