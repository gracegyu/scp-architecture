# ③-I — GW Infra 구축 계획 (3·4단계)

- 상태: 미작성 (인프라 담당 별도 — GW SRS 요구를 입력으로 IaC 계획 작성)
- 문서 유형: IaC 구축 계획서 (기능 스펙/One Pager 아님)
- 범위: 단일 Region GW(3단계), Route 53 GeoDNS·K8s HA·비-AWS MinIO·고정 egress IP·DNS 호스트(4단계)
- 입력(spec_refs): ③ GW SRS(§3.1·§4.5.1 DNS·§7.3.5 GeoDNS), Roadmap §4, 실행 할당표
- 작성 모델: 인프라 담당 주도. GW SRS는 계획·요구만 명시(본 SRS §3·§4.5.1·§7.3.5)
- TBD: DNS 호스트명 확정(§4.5.1), 노드 타입·수, RTO/RPO, MQTT 브로커 운영 주체
- 공식 등록처: TBD (vt-api-gateway-infra repo 권장 — 별도 담당)
