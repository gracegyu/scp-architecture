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

검증 체크리스트

- [x] 기본 프록시 라우팅/업스트림 연결 확인(CloudFront, API)
- [x] 디스크 캐시 동작(HIT/MISS/STALE 헤더) 확인
- [x] 이미지 타입별 TTL 적용 확인(X-ray/CT/스캔/썸네일)
- [ ] Lua 입소 필터(빈도 임계치) 적용 및 우회 정책 검증
- [ ] 성능 예열 및 벤치마크 스크립트(k6/wrk) 준비

메모

- 초기 단계는 Nginx 디스크 캐시와 경로별 TTL로 치과 워크로드 최적화에 집중
- Rust 외부 서비스는 무효화/통계/관리 API 제공(후속 단계에서 연결 및 측정)

상태: 설치/기본 동작/TTL 검증 완료, 입소 필터/성능 테스트 준비 중

---

다음 단계(이 문서 범위)

- Envoy PoC 구현 및 동일 시나리오 측정
- Pingora PoC(CacheBox/Linux) 기본 경로 검증
- 공통 부하 시나리오로 3자 비교(기능/성능/운영성/설치·배포/생태계)
