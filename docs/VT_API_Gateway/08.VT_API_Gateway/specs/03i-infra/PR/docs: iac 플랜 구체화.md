URL : https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-infra/pullrequest/11973

브랜치: `docs/iac-plan-jack-detail` → `docs/iac-plan-draft` · 대상 파일: `docs/IaC-구축계획서.md`

---

# PR #11973 리뷰 준비 (Jack: IaC 플랜 상세 구체화)

## 1. PR 개요 — Jack이 바꾼 것 (3 commits)

| commit | 내용 |
| --- | --- |
| `4846c17` | 실제 `es-infra`/`es-gitops` 구현 방식 반영 + **AppConfig 제거** |
| `9676c27` | es-gitops 실물 반영 — OPA/Rego→**Kyverno**로 교체(과함), 앱 차트 용어 정정, `rel-` 태그 표기 |
| `57f57bc` | 다이어그램/§2.15 **OPA 복원**(Kyverno 오버교체 되돌림) + **"역할 확인" 플래그** |

**핵심 변경 3가지**
1. **인프라 SSOT 확정** — Terraform=`es-infra`(계층형 root module envs/<env>/{network,security,data,platform,apps}), K8s/GitOps=`es-gitops`(공용 `helm/app-chart` + `apps/gw-*/`), CI=`es-ci-templates`. GW 전용 신규 인프라 레포 미생성.
2. **AppConfig 제거** — compat matrix 포함 config/secret을 Secrets Manager + Parameter Store(ESO)로 통일(§2.7).
3. **OPA↔Kyverno** — 혼동으로 Kyverno 교체했다가 되돌려 OPA 복원, 우리에게 역할 확인 요청.

## 2. 종합 판정

- **방향 수용**: es-infra/es-gitops/es-ci-templates 편입, GW 전용 레포 미생성 = 합리적. 계획 문서는 vt-api-gateway-infra 유지.
- **논의 스레드 2건**:
  - **(A) compat matrix 안전장치** — AppConfig를 Parameter Store로 바꾸면 SRS §7.7.5가 근거로 든 *배포 전 스키마 검증 + 자동 롤백*이 사라짐. 수용하되 CI 검증 + 앱 last-known-good으로 보완 필요.
  - **(B) OPA 역할** — **검토 완료·결정**: v1.0 = 앱 내부 PDP(포트 뒤) + Istio egress 집행, **별도 OPA 불필요**. OPA(Rego) = gw/1.1+ 세분화 정책 활성화 시. 근거 = SRS §7.5.3(v1.0 인가 coarse·세분화는 gw/1.1 예약).
- **SRS 반영**: §1.4에 OPA 용어 정의 **추가 완료**(오늘). §7.7.5(AppConfig→구현 중립+안전 보완)는 (A) 합의 후 반영.
- **투표**: 위 2 스레드 resolve 후 approve. 그 전까지 "Wait for author".

---

## 3. 남길 코멘트 (위치별 · 복붙용)

> Azure DevOps PR **Files** 탭에서 `docs/IaC-구축계획서.md`를 열고, 아래 "앵커 문구"가 있는 줄에 마우스오버 → 말풍선 아이콘으로 inline 코멘트. Overview 코멘트는 **Overview** 탭 상단.
> (코멘트 본문은 그대로 붙여넣어도 되게 서술형으로 작성했습니다.)

### 코멘트 1 — Overview (PR 전체 코멘트)

**위치**: PR **Overview** 탭 상단 코멘트 입력란

```
상세 채워주셔서 감사합니다. 인프라 산출물을 es-infra(Terraform)·es-gitops(GitOps/ArgoCD)·es-ci-templates(CI)로 편입하고 GW 전용 신규 레포를 만들지 않는 방향, 계획 문서는 vt-api-gateway-infra에 두고 실물은 표준 레포로 승계하는 방향 모두 동의합니다.

라인 코멘트는 크게 두 갈래로 남겼습니다. 하나는 호환성 매트릭스를 Parameter Store로 서빙할 때 충족돼야 할 안전 요건(§2.7·§2.9)이고, 다른 하나는 OPA(§2.15)입니다. OPA는 검토 결과 v1.0에는 별도 배포가 필요 없어(앱 내부 인가 + Istio egress로 충분, 세분화 정책은 gw/1.1+ 예약) v1.0 인프라 프로비저닝에서 빼시면 됩니다. SRS는 §1.4에 OPA 정의를 추가했고, 세부 정합(§7.7.5·OPA 관련 절)은 코멘트 합의 후 맞추겠습니다.
```

### 코멘트 2 — §2.7 compat matrix 서빙 [핵심]

**위치**: line 163 부근, 앵커 문구 =
`- **호환성 매트릭스(compat matrix) 서빙** = Parameter Store **파일 파라미터**로 발행`

```
호환성 매트릭스는 안전 크리티컬이라(잘못 발행되면 전 클라이언트가 잠기거나 부적합 버전이 통과) 서빙 경로에 두 가지 안전장치가 필요합니다. 하나는 발행 전 스키마 검증이고, 다른 하나는 나쁜 값이 올라가도 서비스가 죽지 않는 것(직전 정상본 유지)입니다. SRS §7.7.5가 이 특성 때문에 검증·롤백을 요건으로 두었습니다.

서빙을 Parameter Store로 가는 방향은 좋습니다(도구를 안 늘리는 이점 동의). 그 위에서 위 요건을 이렇게 충족하면 됩니다 — 발행 파이프라인(CI)에 매트릭스 JSON 스키마 검증 게이트를 두고, GW 앱이 적용 전에 검증해 실패하면 직전 정상본(last-known-good)을 유지하는 것입니다. 8KB 초과 시 S3 간접은 적어주신 대로 좋습니다. 이 요건 기준으로 SRS §7.7.5도 구현 중립적으로 맞추겠습니다.
```

### 코멘트 3 — §2.7 전파·롤백

**위치**: line 164 부근, 앵커 문구 =
`- **전파·롤백** — ESO는 pull(폴링)이라`

```
여기 "앱이 자체 검증"을 선택이 아니라 필수 요건으로 두는 게 좋겠습니다. 매트릭스가 안전 크리티컬이라, GW 앱이 서빙 전에 스키마를 검증하고 실패 시 직전 정상본을 유지하며 검증 실패를 경보로 올리는 것을 기본 동작으로 삼겠습니다. 이렇게 하면 AppConfig의 배포 전 검증·자동 롤백을 앱·CI 레이어에서 대체하게 됩니다.
```

### 코멘트 4 — §2.9 관측 경보 소스

**위치**: line 194 부근, 앵커 문구 =
`- **필수 경보 소스**` (…`ESO 동기화 실패`… 줄)

```
ESO 동기화 실패를 경보 소스로 추가하신 것 좋습니다. 여기에 매트릭스 스키마 검증 실패 또는 last-known-good 사용 중 상태도 경보로 더하면, AppConfig의 자동 롤백을 대체하는 감지 지점이 생깁니다.
```

### 코멘트 5 — §2.15 OPA 역할 [핵심]

**위치**: line 245 부근, 앵커 문구 =
`- **⚠ 역할 확인 필요(Raymond·SRS §2.2 인가):**`

```
OPA 역할을 정리하면, OPA는 런타임에 매 프록시 요청의 인가를 판정하는 PDP입니다. target allowlist·리전·scope·egress·PHI 리전 경계를 deny-by-default로 평가하며, SRS §2.2의 3겹 방어 중 ②인가 레이어입니다. Kyverno(배포시점 admission)나 Istio egress(네트워크 경로 집행)와는 다른 계층입니다.

검토 결과 v1.0에서는 별도 OPA 배포 없이 가는 것으로 정리했습니다. SRS §7.5.3이 v1.0 인가를 "이 device/clinic이 target axs를 쓸 수 있다"는 굵은(coarse) 허용 + egress SSOT + 인증 + region/PHI 경계까지로 한정하고, 세분화된 endpoint·scope 정책(Rego의 패턴매칭·교집합이 값을 하는 부분)은 gw/1.1+로 예약해 두었기 때문입니다. 이 굵은 판정은 GW 앱이 이미 가진 레지스트리·resolver·policy 테이블(clinic→global)로 충분히 평가됩니다.

그래서 v1.0은 앱 내부 인가 모듈(PDP 포트 뒤)로 판정하고, egress는 Istio egress gateway가 target.egress_allowlist(SSOT)를 참조해 고정 EIP로 집행합니다. OPA(Rego)는 세분화 정책이 활성화되는 gw/1.1+에 같은 PDP 포트 뒤로 도입하면 되므로, v1.0 인프라에는 OPA 프로비저닝이 필요 없습니다. §2.15는 "v1.0=앱 내부 PDP+Istio egress / OPA(Rego)=gw/1.1+ 예약"으로 정리해 주시고, SRS(§2.2·§3.1.2·§7.2.2·§7.5.3)도 같은 방향으로 저희가 맞추겠습니다. 참고로 SRS §1.4에 OPA 정의를 추가했습니다.
```

### 코멘트 6 — §2.15 Kyverno 구분 (긍정 확인)

**위치**: line 246 부근, 앵커 문구 =
"`참고(실물):` es-gitops에는 OPA/Rego 배포가 없고" 줄

```
Kyverno와 OPA를 다른 레이어로 구분해 적어주신 것 정확합니다. Kyverno는 배포 시점의 K8s admission(클러스터 거버넌스)이고 OPA는 런타임 요청 인가라 대체 관계가 아닙니다. OPA를 되돌려 복원해주신 판단도 맞습니다.
```

### (삭제) 코멘트 7 — §0.5 ② "재론 금지"

> **남기지 않음.** config 서빙 *메커니즘*(Parameter Store vs AppConfig)은 Jack(인프라) 도메인이고 우리가 이미 수용했다. "재론 금지" 라벨을 다투는 건 영역 침범·중복이다. 우리가 지킬 것 = *안전 요구사항*이고, 그건 코멘트 2·3(요건 명시)로 충분하다. SRS §7.7.5 정합은 코멘트 2 말미에서 우리가 맞추겠다고 이미 밝혔다.

---

## 4. 코멘트 후 우리(GW) 후속 작업 (합의 뒤)

- **(A) 합의 시** → SRS §7.7.5·Appendix B(매트릭스 항목)을 "동적 config 서비스(인프라=Parameter Store+ESO), 앱/CI가 스키마 검증+last-known-good, 8KB↑ S3 간접"으로 구현 중립 개정 + IP `T-CFG-5-2`(AppConfig Agent → Parameter Store/ESO + 검증) 갱신. baseline 이후 변경이라 CCB·새 SHA.
- **(B) OPA** → **결정 완료**(v1.0 = 앱 내부 PDP + Istio egress / OPA(Rego) = gw/1.1+). 후속 = SRS **§2.2 다이어그램 OPA 노드·§3.1.2·§7.2.2·§7.5.3·§1.4**를 "v1.0 = 앱 내부 PDP(포트) / OPA = gw/1.1+ 예약"으로 정합화(baseline 이후 변경·CCB·새 SHA). 인가 **규칙**(deny-by-default·scope 해석·egress SSOT·region/PHI)은 불변 — **엔진(OPA vs 앱내부)·시점만** 조정. §2.15는 위 코멘트대로 Jack이 계획서에 반영.
- SRS §1.4 OPA 용어 추가 = **완료**(오늘) — 단, 위 정합화 시 "v1.0=앱 내부 PDP, OPA=gw/1.1+" 문구를 이 항목에도 반영.
