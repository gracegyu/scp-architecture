# 세션 핸드오프 노트 (VT-GW-스펙)

> **목적**: 이 작업 세션의 전체 맥락·현황·미결을 한 장으로 캡처. resume 실패 시 새 세션이 여기서 이어받는다.
> **작성**: 2026-07-20 · Raymond (Claude 세션 "VT-GW-스펙")
> **정본 주의**: 이 파일은 스냅샷이다. 실제 정본은 각 산출물·git·아래 링크 문서. 상태가 바뀌면 갱신하거나 폐기.

---

## 0. 지금 어디까지 왔나 (한 줄)

③ GW SRS PR 리뷰 마무리·baseline 임박 + **③-I 인프라 계획서(→Jack)·③-P-EZ EzServer OnePager(→EzServer 팀) 초안 작성·인계** 단계.

---

## 1. ③ GW SRS PR (#11766) 현황

- **레포/브랜치**: `vt-api-gateway` · `docs/gw-srs-initial` (원격 push 완료)
- **최근 커밋**: `5efe4b9`(region_catalog endpoint 주석 정합) ← `3d9514a`(2-cluster·clinic_id 불변·리전 endpoint 미노출) ← `2bfa8cc` ← `e568995`
- **스레드**: 총 51개 = **17 resolved(fixed) / 34 active**. **34개 모두 우리 답변이 마지막** — 리뷰어 resolve 대기(우리 대응 필요분 없음).
- **승인**: 필수 **Scott·Thomas 승인** + 옵션 Jack 승인(이미지 기준). ⚠ **DBML push로 vote reset 가능** → 재승인 확인 필요.
- **다음 액션(월 7/20)**: 리뷰어 resolve 촉구(PR/Teams 코멘트 이미 작성함) → 재승인 → **Complete(병합)** → **문서 0.9→1.0 baseline**.

## 2. ③-I 인프라 IaC 구축 계획서 (→ Jack)

- **정본(SSOT)**: `vt-api-gateway-infra/docs/IaC-구축계획서.md` — **브랜치 `docs/iac-plan-draft`** 에 배치(**미커밋** — 사용자가 커밋). 커밋 메시지 초안 이미 제공함.
- **scp 원본**: `specs/03i-infra/IaC-구축계획서.md` = **리다이렉트 stub**(정본=infra 레포). `_status.md`도 이관 반영.
- **내용**: 전체 인프라 mermaid(LR·4-way·2-cluster·istio egress·OPA) + SRS 인프라 요구 §2.1~2.15 + §2.13 규모입력 + §3 미결 + §4 소유경계. 각 항목 `🔧 Jack 상세`.
- **이번 세션 보강(SRS 전수 대조)**: admin 토폴로지 수정 · §2.8 시크릿/키 **전수 목록**(Secrets Manager/KMS/ACM) · §2.13 규모 잠정치 · **§2.14 service mesh(istio)** · **§2.15 OPA** · WAF/Shield · ECR 스캔 · 경보 소스 · Helm · NTP · VPC endpoint · **③-C Console·④ AXS 후행 의존 TBD** · **§2.11 CI/CD 소유 경계**(Dockerfile·pipeline=GW / Jack=선행 제공).
- **인계**: 브랜치 push 후 링크를 Jack에게. PR은 Jack이 상세 완성 후 생성.

## 3. ③-P-EZ EzServer GW 적응 OnePager (→ EzServer 팀 Teddy·Thomas)

- **위치**: `specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md` (scp-architecture·**미커밋**). 아직 제품 레포로 이관 안 함.
- **포맷**: Engineering One Pager (OnePager v1.0 템플릿). **소유=EzServer 팀(Teddy·Thomas)**, 초안=Raymond.
- **구조**: 기존 EzServer suite 코드 분석(nginx/EAP/ELM/EPI(Rust)/WebConsole) 기반 **기능 블록 WS-1~9**:
  - WS-1 라우팅/Bypass(nginx·오류 패스스루·호환경고·타임아웃30s·자기헤더) · WS-2 인증/온보딩(private_key_jwt·jti/NTP·차단상태) · WS-3 MQTT 하행(+**엣지 last-hop 분배 TBD**·ClinicResolution) · WS-4 presigned 업로드(+멱등키) · WS-5 heartbeat · WS-6 로컬 콘솔 · WS-7 하위호환 · WS-8 IO Scanner(TBD·R1) · **WS-9 org-binding·AXS link 개시**
  - 각 블록 `🔧 EzServer 팀 상세` + 데이터흐름 다이어그램 + nginx config 예제.
- **Teddy 문의 답신**: 초안 **7/21(내일) 중 전달** 약속. 범위=Rust 전면 재개발 제외, IO Scanner 의존부=TBD.
- **다음**: EzServer 팀 레포로 이관 시 IaC와 동일하게 stub 처리(아직 안 함).

## 4. 주간회의 Agenda (7/23)

- `08.VT_API_Gateway/주간회의-Agenda.md` — 7/23 섹션 "이번 주 진행"에 3건(SRS PR baseline·③-I 인계·③-P-EZ 초안) 반영. S1 Gantt(③-I 초안+Jack 하나 bar로 병합)·S2 스펙테이블 갱신. 7/16 스냅샷 보존.

## 5. CI/CD 소유 (확정·참고)

- `Dockerfile`·`azure-pipelines.yml`·`azure-pipelines-config.yml` = **GW(Raymond) 소유·작성**. Jack=service connection·ECR·S3+IAM·ArgoCD·agent pool·manifest 위치 관례 **선행 제공**.
- 작성 전략: Dockerfile=인프라 무관 조기 / pipeline=build·test 조기 + 배포 트리거만 Jack 전제 확정 후. 정본=`specs/00-execution-allocation.md` §CI/CD. **Agenda 아님**(2026-07-07 실행 트래커로 이관).

## 6. 미커밋 상태 (사용자가 커밋 예정)

- **scp-architecture**: Agenda·EzServer OnePager(신규)·03p-ez _status·03i-infra stub+_status·00-execution-allocation·(이 핸드오프 노트).
- **vt-api-gateway-infra**: `docs/iac-plan-draft` 브랜치에 `docs/IaC-구축계획서.md`(신규).
- **vt-api-gateway**: 이미 push 완료(5efe4b9까지).

## 7. 핵심 결정·제약 (놓치면 안 됨)

- **PHI 리전 로컬·2-cluster 불변식**(전역일관 Aurora Global DB / 리전로컬 webhook_event·audit·fleet). payload=관계형 DB·KMS envelope.
- **clinic_id 불변**(EVNL-238)·자동 이관 없음·수동 이관 API=추후(Appendix B #49).
- **OneID는 GW에 없음**(확정). EPI의 OneID 결합은 GW 경로에서 분리.
- **IO Scanner↔EzServer 연동 방식 미정(R1)** — v1.0 우선인데 선결. 의존부 전부 TBD.
- **PR 답변 스타일**: 서술문·내부 라벨(C-NN) 금지·`#숫자` 오링크 회피(B-N).

## 8. 열린 항목 (요약)

- 월 7/20: DBML 재승인 → baseline v1.0.
- IaC 계획서 → Jack 커밋·PR / EzServer OnePager → EzServer 팀 이관.
- TBD: MQTT 브로커 제품(#4)·RTO/RPO(#9)·라우팅 방식(R1)·엣지 분배 메커니즘·클라 타임아웃30s(#25)·③-C Console/④ AXS 인프라 영향.

---

## 참고 — 세션 이력 메모 (비작업)

- 이 세션 = `5cf10750`("VT-GW-스펙"으로 rename). 부모였던 `587af9a6`(온보딩 원본·82MB) **삭제됨**(복구 불가). 그 결과 `claude -r`로 이 세션 resume 시 크래시 가능(요약이 없는 부모 hydrate 시도). **산출물·현재 세션 내용은 무사** — resume 안 되면 이 노트로 새 세션에서 이어받을 것.
