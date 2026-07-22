URL : https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-infra/pullrequest/11973

브랜치: `docs/iac-plan-jack-detail` → `docs/iac-plan-draft` · 대상 파일: `docs/IaC-구축계획서.md`

---

# PR #11973 리뷰 (Jack: IaC 플랜 상세 구체화)

## 1. PR 개요 — Jack이 바꾼 것 (4 commits)

| commit | 내용 |
| --- | --- |
| `4846c17` | 실제 `es-infra`/`es-gitops` 구현 방식 반영 + **AppConfig 제거** |
| `9676c27` | es-gitops 실물 반영 — OPA/Rego→**Kyverno**로 교체(과함), 앱 차트 용어 정정, `rel-` 태그 표기 |
| `57f57bc` | 다이어그램/§2.15 **OPA 복원**(Kyverno 오버교체 되돌림) + **"역할 확인" 플래그** |
| `5170b3d` | **§2.7 매트릭스 안전 요건 반영**(우리 코멘트 2·3·4 대응) — CI 검증 게이트·write 봉쇄·앱 LKG·cold-start·§2.9 경보 |

## 2. 종합 판정 (진행 상태)

- **방향 수용**: es-infra/es-gitops/es-ci-templates 편입, GW 전용 레포 미생성 = 합리적.
- **(A) compat matrix 안전** — **합의 완료.** Jack이 `5170b3d`로 CI 스키마 검증 게이트·write IAM 봉쇄·앱 in-memory LKG·cold-start fail-closed·§2.9 경보까지 반영(우리 요청+보강). → 스레드 2·3·4 **resolve 가능**. 우리 후속(SRS §7.7.5·IP) unblock.
- **(B) OPA 역할** — **결정 완료**: v1.0 = 앱 내부 PDP + Istio egress, 별도 OPA 불필요 / OPA(Rego) = gw/1.1+. 스레드 5·6 **resolved(fixed)**. §2.15 문서 반영은 **Jack 별도 예정**.
- **SRS 반영**: §1.4 OPA 용어 **추가 완료**. §7.7.5(구현 중립+안전 보완)·OPA 관련 절은 우리 후속(§4).
- **투표**: 2·3·4 resolve → overview resolve → approve.

### 스레드 현황

| 코멘트 | thread | 위치 | 상태 | 내가 할 것 |
| --- | --- | --- | --- | --- |
| 1 Overview | 80609 | overview | active | 2·3·4 닫은 뒤 **마지막 resolve**(approve 시) |
| 2 매트릭스 서빙 | 80592 | §2.7:163 | active | 아래 추천 답글 달고 **resolve** |
| 3 전파·검증·롤백 | 80594 | §2.7:164 | active | 아래 추천 답글 달고 **resolve** |
| 4 경보 | 80595 | §2.9:194 | active | 아래 추천 답글 달고 **resolve** |
| 5 OPA | 80600 | §2.15:245 | **fixed** ✓ | 완료 |
| 6 Kyverno | 80605 | §2.15:246 | **fixed** ✓ | 완료 |

---

## 3. 코멘트 스레드 (우리 코멘트 → Jack 회신 → 내가 달 추천 답글)

### 코멘트 1 — Overview (thread 80609 · active)

**우리 코멘트**:
```
상세 채워주셔서 감사합니다. 인프라 산출물을 es-infra(Terraform)·es-gitops(GitOps/ArgoCD)·es-ci-templates(CI)로 편입하고 GW 전용 신규 레포를 만들지 않는 방향, 계획 문서는 vt-api-gateway-infra에 두고 실물은 표준 레포로 승계하는 방향 모두 동의합니다.

라인 코멘트는 크게 두 갈래로 남겼습니다. 하나는 호환성 매트릭스를 Parameter Store로 서빙할 때 충족돼야 할 안전 요건(§2.7·§2.9)이고, 다른 하나는 OPA(§2.15)입니다. OPA는 검토 결과 v1.0에는 별도 배포가 필요 없어(앱 내부 인가 + Istio egress로 충분, 세분화 정책은 gw/1.1+ 예약) v1.0 인프라 프로비저닝에서 빼시면 됩니다. SRS는 §1.4에 OPA 정의를 추가했고, 세부 정합(§7.7.5·OPA 관련 절)은 코멘트 합의 후 맞추겠습니다.
```
**↳ Jack 회신 (원문 · 05:08 빈 코멘트 1개 + 05:21)**:
```
매트릭스 안전 요건(§2.7·§2.9) 반영해 push했습니다(`5170b3d`): ① CI 발행 파이프라인 스키마 검증 게이트 필수 + Parameter Store write를 CI identity 전용 IAM으로 제한(검증 우회 차단), ② 앱 in-memory last-known-good 서빙 필수화 + cold-start는 fail-closed/번들 default, ③ 검증 실패·LKG fallback 경보 추가. OPA(§2.15)는 별도로 정리하겠습니다.
```
**↳ 내가 달 추천 답글**: (없음 — 2·3·4 다 resolve하고 전체 합의·approve 시 이 overview를 마지막으로 resolve. 필요하면 아래 한 줄)
```
매트릭스 안전 요건 반영 확인했습니다. OPA(§2.15)만 정리되면 approve하겠습니다.
```

### 코멘트 2 — §2.7 매트릭스 서빙 (thread 80592 · active) [핵심]

**우리 코멘트**:
```
호환성 매트릭스는 안전 크리티컬이라(잘못 발행되면 전 클라이언트가 잠기거나 부적합 버전이 통과) 서빙 경로에 두 가지 안전장치가 필요합니다. 하나는 발행 전 스키마 검증이고, 다른 하나는 나쁜 값이 올라가도 서비스가 죽지 않는 것(직전 정상본 유지)입니다. SRS §7.7.5가 이 특성 때문에 검증·롤백을 요건으로 두었습니다.

서빙을 Parameter Store로 가는 방향은 좋습니다(도구를 안 늘리는 이점 동의). 그 위에서 위 요건을 이렇게 충족하면 됩니다 — 발행 파이프라인(CI)에 매트릭스 JSON 스키마 검증 게이트를 두고, GW 앱이 적용 전에 검증해 실패하면 직전 정상본(last-known-good)을 유지하는 것입니다. 8KB 초과 시 S3 간접은 적어주신 대로 좋습니다. 이 요건 기준으로 SRS §7.7.5도 구현 중립적으로 맞추겠습니다.
```
**↳ Jack 회신 (원문 · 05:21)**:
```
반영했습니다(`5170b3d`). 발행 파이프라인에 **매트릭스 JSON 스키마 검증 게이트를 필수**로 두어 실패 시 발행이 중단되게 했고, Parameter Store **write 권한은 CI 발행 identity 전용 IAM으로 제한**(사람·앱 role 직접 write deny)해 콘솔/CLI 임의 수정으로 게이트를 우회할 수 없게 했습니다. 앱은 마운트 파일을 직접 서빙하지 않고 검증 통과분을 **in-memory last-known-good**으로 서빙합니다. 8KB 초과 S3 간접은 유지. SRS §7.7.5 구현 중립화 감사합니다.
```
**↳ 내가 달 추천 답글**:
```
반영 확인했습니다. CI 검증 게이트 + write 경로 IAM 봉쇄로 임의 수정 우회를 막은 것 좋습니다. 이 방향으로 SRS §7.7.5도 구현 중립으로 정리하겠습니다.
```
→ 답글 후 **resolve**.

### 코멘트 3 — §2.7 전파·검증·롤백 (thread 80594 · active)

**우리 코멘트**:
```
여기 "앱이 자체 검증"을 선택이 아니라 필수 요건으로 두는 게 좋겠습니다. 매트릭스가 안전 크리티컬이라, GW 앱이 서빙 전에 스키마를 검증하고 실패 시 직전 정상본을 유지하며 검증 실패를 경보로 올리는 것을 기본 동작으로 삼겠습니다. 이렇게 하면 AppConfig의 배포 전 검증·자동 롤백을 앱·CI 레이어에서 대체하게 됩니다.
```
**↳ Jack 회신 (원문 · 05:21)**:
```
선택이 아니라 **필수 요건**으로 고쳤습니다(`5170b3d`). "서빙 전 스키마 검증 → 실패 시 직전 LKG 유지 → 검증 실패 경보"를 기본 동작으로 §2.7에 명시했습니다. 다만 **cold-start**(신규 pod가 나쁜 값 상태로 떠 메모리 LKG가 없는 경우)는 LKG로 못 막으므로, 위 **CI 게이트 + write 봉쇄**가 1차 방어이고 그 상태의 새 pod는 **fail-closed**(매트릭스 의존 경로 서빙 거부 → 롤아웃 자동 중단) 또는 **이미지 번들 default**로 대응하도록 §2.7에 열어뒀습니다.
```
**↳ 내가 달 추천 답글**:
```
반영 확인했습니다. 앱 레이어 검증+LKG를 필수로 두고 cold-start를 fail-closed로 처리하신 것까지 좋습니다.
```
→ 답글 후 **resolve**.

### 코멘트 4 — §2.9 경보 소스 (thread 80595 · active)

**우리 코멘트**:
```
ESO 동기화 실패를 경보 소스로 추가하신 것 좋습니다. 여기에 매트릭스 스키마 검증 실패 또는 last-known-good 사용 중 상태도 경보로 더하면, AppConfig의 자동 롤백을 대체하는 감지 지점이 생깁니다.
```
**↳ Jack 회신 (원문 · 05:21)**:
```
추가했습니다(`5170b3d`). §2.9 필수 경보 소스에 **매트릭스 스키마 검증 실패**와 **last-known-good fallback 활성** 상태를 넣어 AppConfig 자동 롤백을 대체하는 감지점을 만들었습니다.
```
**↳ 내가 달 추천 답글**:
```
반영 확인했습니다. 매트릭스 검증 실패·LKG fallback 경보가 AppConfig 자동 롤백을 대체하는 감지점으로 충분합니다.
```
→ 답글 후 **resolve**.

### 코멘트 5 — §2.15 OPA 역할 (thread 80600 · **fixed** ✓) [핵심]

**우리 코멘트**:
```
OPA 역할을 정리하면, OPA는 런타임에 매 프록시 요청의 인가를 판정하는 PDP입니다. target allowlist·리전·scope·egress·PHI 리전 경계를 deny-by-default로 평가하며, SRS §2.2의 3겹 방어 중 ②인가 레이어입니다. Kyverno(배포시점 admission)나 Istio egress(네트워크 경로 집행)와는 다른 계층입니다.

검토 결과 v1.0에서는 별도 OPA 배포 없이 가는 것으로 정리했습니다. SRS §7.5.3이 v1.0 인가를 "이 device/clinic이 target axs를 쓸 수 있다"는 굵은(coarse) 허용 + egress SSOT + 인증 + region/PHI 경계까지로 한정하고, 세분화된 endpoint·scope 정책(Rego의 패턴매칭·교집합이 값을 하는 부분)은 gw/1.1+로 예약해 두었기 때문입니다. 이 굵은 판정은 GW 앱이 이미 가진 레지스트리·resolver·policy 테이블(clinic→global)로 충분히 평가됩니다.

그래서 v1.0은 앱 내부 인가 모듈(PDP 포트 뒤)로 판정하고, egress는 Istio egress gateway가 target.egress_allowlist(SSOT)를 참조해 고정 EIP로 집행합니다. OPA(Rego)는 세분화 정책이 활성화되는 gw/1.1+에 같은 PDP 포트 뒤로 도입하면 되므로, v1.0 인프라에는 OPA 프로비저닝이 필요 없습니다. §2.15는 "v1.0=앱 내부 PDP+Istio egress / OPA(Rego)=gw/1.1+ 예약"으로 정리해 주시고, SRS(§2.2·§3.1.2·§7.2.2·§7.5.3)도 같은 방향으로 저희가 맞추겠습니다. 참고로 SRS §1.4에 OPA 정의를 추가했습니다.
```
**↳ Jack 회신**: (없음) — thread resolved(fixed). Overview 회신에서 "OPA(§2.15)는 별도 정리" 언급 → **§2.15 문서 반영은 Jack 후속 커밋 예정**.
**↳ 내가 달 추천 답글**: (이미 resolved — 추가 답글 불요. Jack §2.15 커밋 오면 반영 확인만.)
**상태**: resolved 완료.

### 코멘트 6 — §2.15 Kyverno 구분 (thread 80605 · **fixed** ✓)

**우리 코멘트**:
```
Kyverno와 OPA를 다른 레이어로 구분해 적어주신 것 정확합니다. Kyverno는 배포 시점의 K8s admission(클러스터 거버넌스)이고 OPA는 런타임 요청 인가라 대체 관계가 아닙니다. OPA를 되돌려 복원해주신 판단도 맞습니다.
```
**↳ Jack 회신**: (없음) — thread resolved(fixed).
**↳ 내가 달 추천 답글**: (불요 — 긍정 확인이라 그대로 resolved.)
**상태**: resolved 완료.

### (삭제) 코멘트 7 — §0.5 ② "재론 금지"

> **남기지 않음.** config 서빙 *메커니즘*(Parameter Store vs AppConfig)은 Jack(인프라) 도메인이고 우리가 이미 수용. "재론 금지" 라벨 다투기는 영역 침범·중복. 안전 요구는 코멘트 2·3로 충분.

---

## 4. 코멘트 후 우리(GW) 후속 작업

- **(A) compat matrix — 합의됨(Jack `5170b3d` 반영) → SRS 정합화 진행 가능.** SRS §7.7.5·Appendix B(매트릭스 항목)을 다음으로 구현 중립 개정 + IP `T-CFG-5-2` 갱신:
  - 동적 config 서비스(인프라 = Parameter Store + ESO), **매트릭스 = safety-critical**.
  - **CI 발행 스키마 검증 게이트 필수** + **Parameter Store write = CI identity 전용 IAM**(사람·앱 write deny = 1차 방어).
  - **앱 in-memory last-known-good 서빙 필수**(마운트 파일 직접 서빙 금지·검증 통과분만 원자 교체) + **검증 실패 경보**(2차 방어).
  - **cold-start = fail-closed 또는 이미지 번들 default**.
  - 8KB 초과 → S3 간접. → AppConfig 네이티브(배포 전 검증+자동 롤백)를 이 앱·CI 레이어로 대체.
  - baseline 이후 변경이라 CCB·새 SHA.
- **(B) OPA — 결정 완료**(v1.0 = 앱 내부 PDP + Istio egress / OPA = gw/1.1+). 후속 = SRS **§2.2 다이어그램 OPA 노드·§3.1.2·§7.2.2·§7.5.3·§1.4**를 "v1.0 = 앱 내부 PDP(포트) / OPA = gw/1.1+ 예약"으로 정합화(CCB·새 SHA). 인가 **규칙**(deny-by-default·scope·egress SSOT·region/PHI) 불변 — 엔진·시점만 조정. §2.15 문서는 Jack 후속 커밋.
- SRS §1.4 OPA 용어 추가 = **완료** — 정합화 시 "v1.0=앱 내부 PDP, OPA=gw/1.1+" 문구 보강.
