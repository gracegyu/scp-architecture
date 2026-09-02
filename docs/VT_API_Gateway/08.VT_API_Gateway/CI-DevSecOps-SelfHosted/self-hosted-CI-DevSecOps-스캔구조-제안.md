# 제안: self-hosted CI/DevSecOps 스캔 구조 개선

> 스캔을 CI verify로 일원화하고, trivy DB를 self-hosted 로컬 공유캐시로 — trivy 4중복·DB 다운로드 실패·OOM 해소

- **작성**: 2026-09-02 (GW)
- **공유/논의**: 2026-09-03 GW 주간회의
- **관련 PR**: [#13480](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13480)(root CI self-hosted·머지)·[#13498](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13498)(devsecops pool·보류)·[#13512](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13512)(트리거 main 제거·머지, Jack)

---

## 1. 배경 — 왜 이 논의가 나왔나

self-hosted 전환(Microsoft-hosted agent pool 적체로 대기 과다 → 자체 Self-hosted1로 이전) 진행 중, **devsecops를 self-hosted로 옮기는 [#13498](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13498)이 반복 실패**했고 세 가지 구조 문제가 드러났다.

1. **trivy 4중복 스캔** — devsecops 게이트 4개(core/admin/receiver/dispatcher)가 **공유 코드(libs·package.json·Dockerfile 등) 변경 시 전부 발동**해, 앱과 무관한 **레포-공통 스캔을 4번** 돌린다.
2. **trivy DB 다운로드 실패(flaky)** — 매 스캔이 gcr.io에서 취약점 DB(약 110MB)를 새로 받는데, **self-hosted 호스트→gcr.io 네트워크가 불안정**(`connection reset by peer`). [#13498](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13498)의 dispatcher 실패, 그리고 2026-09-02 재실패가 모두 이 다운로드다.
3. **OOM** — 동시 스캔이 **6GB 에이전트 컨테이너 한도를 초과** → "stopped hearing from agent"(에이전트 소실). receiver 실패가 이것.

## 2. 현재 상태 (팩트)

**main 브랜치 Build-validation 정책(라이브 조회):**

| 정책 | 게이트 | 경로 필터 |
|---|---|---|
| 151 | DevSecOps — core | `/apps/core/*` + 공유(libs·prisma·package.json·pnpm-lock·Dockerfile·nest-cli·tsconfig·devsecops-core.yml) |
| 152 | DevSecOps — admin | `/apps/admin/*` + 공유 |
| 153 | DevSecOps — receiver | `/apps/receiver/*` + 공유 |
| 154 | DevSecOps — dispatcher | `/apps/dispatcher/*` + 공유 |
| 156 | CI verify (lint·build·unit·e2e·scan) | `/*` (단 `!docs` `!.env.example`) = **레포 전체** |

- **핵심**: 4개 게이트가 **각자 앱+공유 필터**라, 공유 변경 시 4개가 다 발동 → **같은 스캔 4번**.
- **Jack PR [#13512](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13512) 불일치**: PR 설명은 "admin·receiver·dispatcher 게이트(152·153·154) **삭제**"라 하나, **라이브 정책엔 4개가 그대로 살아 있다**. 머지된 것은 코드 부분(root 트리거에서 main 제거)뿐이고, 게이트 삭제(브랜치 정책·az CLI)는 **미반영**. → **Jack 확인 필요.**

## 3. 목표(설계 원칙)

1. **레포 공통 스캔(trivy/DT)은 어떤 앱이 바뀌든 정확히 1회.**
2. **각 앱 이미지 빌드는 자기(또는 공유)가 바뀔 때만.**
3. **trivy DB의 gcr.io 다운로드를 CI 임계경로에서 제거**(flaky 근본 해소).
4. self-hosted 부하 최소.

## 4. 제안 (핵심 3조각)

### A. 종속성 스캔을 **우리 CI verify(레포 코드 검증 파이프라인)에 흡수**

> **CI verify 란?** 이 레포의 **코드 검증 파이프라인**이다. 모든 PR에서 자동으로 돌며 **lint → 빌드(4개 앱) → 단위테스트 → e2e 테스트 → 의존성 감사**를 수행하고, **하나라도 실패하면 그 PR은 main에 머지할 수 없다**(필수 게이트). 문서(`docs/`)만 빼고 **레포 어디가 바뀌든 PR당 한 번** 돈다. **GW가 직접 소유**하는 파이프라인이라 우리가 단계를 넣고 뺄 수 있다.

- 이 CI verify에 **소스 보안 스캔을 추가**한다 = **gitleaks(시크릿) + `trivy fs`(종속성·IaC)** — 원래 devsecops가 PR에서 돌리던 그 스캔을 그대로 여기로 가져온다.
- CI verify는 원래 **어느 앱이 바뀌든 PR당 1회** 돌기 때문에, 여기에 넣으면 스캔도 **자동으로 PR당 정확히 1회** 수행된다 → **레포 공통 스캔의 자연스러운 자리가 이미 CI verify**이고, 스캔 전용 파이프라인을 따로 만들 필요가 없다.

### B. **우리가 브랜치 정책에서 devsecops PR 게이트 정리 → 4중복 스캔 제거** (중앙 템플릿 손 안 댐)
devsecops의 소스 스캔(ci 스테이지)은 **PR 게이트로만** 돈다(중앙 템플릿이 main push에선 ci 스킵). 그래서 **우리 repo 브랜치 정책에서 devsecops PR 게이트를 정리**하면 그 4중복 스캔이 사라진다 — **우리 소관(Raymond/PL)이라 Jack 대기 불요**. 그 스캔(gitleaks + trivy fs)은 **A의 CI verify가 이어받는다**.
- devsecops 4개는 **빌드 + 이미지 스캔(trivy image·main) + push/서명/배포**만 남는다(빌드는 앱별이라 유지).
- (참고: PR **소스 스캔(trivy fs)** 과 main **이미지 스캔(trivy image)** 은 범위가 다르다 — 소스 의존성 vs 이미지 레이어. 이미지 스캔은 그대로.)
- **Jack = 거버넌스 리뷰만**: vt-api-gateway가 중앙 devsecops 스캔 대신 **자체 CI verify에서 스캔**해도 되는지(중앙 SBOM/리포팅 강제 여부) 승인. 중앙 템플릿을 정말 손대야 하면 **우리가 PR·Jack 리뷰**(#13482처럼).
- → **4중복 소스 스캔 소멸.**

### C. **trivy를 유지하고, DB를 self-hosted 로컬 캐시로 — gcr.io 다운로드 제거**
CI 게이트에는 **trivy가 더 적합**하다(동기 exit code 한 방·**IaC까지 커버**·SBOM 생성·별도 서버/프로젝트/정책/비동기 폴링 불요). 문제는 오직 **매 실행 gcr.io서 취약점 DB(110MB)를 받다가 실패**하는 것 → **DB를 CI 임계경로 밖으로** 빼면 된다(trivy 공식 air-gapped 패턴):
- **① self-hosted에 trivy 설치**(컨테이너 또는 바이너리).
- **② cron 하루 1회 `trivy --download-db-only`** → **공유 캐시에 DB 갱신**. (gcr.io 접속은 여기서만·**CI 밖**이라 흔들려도 느긋하게 재시도.)
- **③ CI: `trivy fs --skip-db-update --cache-dir <공유캐시>`** → **gcr.io 미접속·오프라인 스캔.**
- **핵심 전제 — 공유 퍼시스턴트 볼륨**: 에이전트가 컨테이너 4개라, DB 캐시를 **4개가 공유하는 호스트 볼륨 1개**(예 `/opt/trivy-cache`)에 두고 각 에이전트에 마운트해야 **cron 1회 갱신을 4개가 모두 읽는다**(안 그러면 4벌·재시작 시 휘발).
- **staleness**: DB가 <24h 지나도 `--skip-db-update`가 그대로 스캔(graceful) — main 이미지 스캔이 최종 백스톱.

**구조 다이어그램** (외부 볼륨을 DB-갱신 컨테이너와 Agent 컨테이너들이 공유):

```
                gcr.io (aquasec/trivy-db · 110MB)
                          │   ← 하루 1회만 접속 (CI 밖 · 흔들려도 CI 무영향)
                          ▼
        ┌─────────────────────────────────────────┐
        │  trivy DB-updater 컨테이너 (cron · daily) │  trivy --download-db-only
        └────────────────────┬────────────────────┘
                             │ write (DB 1벌)
                             ▼
   ╔═════════════════════════════════════════════════════════╗
   ║   Host 퍼시스턴트 볼륨   /opt/trivy-cache                 ║  ← 재시작에도 생존
   ╚═══▲═════════════▲═════════════▲═════════════▲════════════╝
 mount │             │             │             │   (모든 Agent가 같은 볼륨 마운트)
   ┌───┴────┐   ┌────┴───┐    ┌────┴───┐    ┌────┴───┐
   │ Agent1 │   │ Agent2 │    │ Agent3 │    │ Agent4 │   ← CI 스캔 (컨테이너)
   │ trivy  │   │ trivy  │    │ trivy  │    │ trivy  │   trivy fs --skip-db-update
   └────────┘   └────────┘    └────────┘    └────────┘   (gcr.io 미접속 · 오프라인)

   * CI 스캔(Agent)은 gcr.io를 절대 건드리지 않는다 → flaky 다운로드 실패 소멸.
   * gcr.io 접속은 오직 좌상단 cron 1회뿐이고, 실패해도 재시도(CI 안 막힘).
```

## 5. 이 제안이 세 문제를 어떻게 푸나

| 문제 | 해소 방식 |
|---|---|
| trivy 4중복 스캔 | **B**(devsecops 스캔 OFF) + **A**(CI verify 1회) → **스캔 1회** |
| trivy DB 다운로드 flaky | **C**(trivy DB 로컬 공유캐시·cron 갱신) → CI는 gcr.io 미접속 |
| OOM | 스캔 1개로 축소 + DB 미다운로드로 부하 감소 |

## 6. Trivy vs DependencyTrack — 비교와 "커버리지 누락 여부"

### 6.1 비교표

| 항목 | Trivy | DependencyTrack(DT) |
|---|---|---|
| 유형 | CLI 스캐너(실행 시점 1회) | 상주 SCA 서버(지속 모니터링) |
| 취약점 DB | **매 실행 gcr.io서 다운로드(~110MB)** | **서버 보유·중앙 갱신 → CI 다운로드 0** |
| 종속성 취약점(SCA) | O | O (본업) |
| OS 패키지 취약점 | O (`trivy image`) | O (이미지 SBOM 업로드 시) |
| 라이선스 컴플라이언스 | O | O |
| IaC/misconfig(Dockerfile·k8s·tf) | O (`trivy config`) | **X** |
| 시크릿 | O (부가) | X (우리는 gitleaks 별개) |
| SBOM | 생성 | 소비(외부 생성 SBOM 업로드) |
| 게이팅 방식 | exit code(동기·즉시) | 정책 위반 폴링(비동기) |
| 배포 後 신규 CVE 지속 모니터링 | X (실행 시점만) | **O (강점)** |
| self-hosted 네트워크 | gcr.io 의존(**flaky**) | **로컬 도달(안정)** |
| 이력/대시보드 | X | O |

### 6.2 결론 — CI 게이트는 **trivy**, DT는 **지속 모니터링 보완(선택)**

- **CI 게이트 = trivy**: 동기(exit code) 한 방 · **IaC까지 커버** · 별도 서버/프로젝트/정책/비동기 폴링 불요 → self-hosted CI에 붙이기 단순. (DB 다운로드 문제는 4.C 로컬 캐시로 해결.)
- **DT = 보완(선택·향후·별건)**: DT의 고유 강점은 **배포 後 신규 CVE 지속 모니터링**이다. 게이트로 쓰면 `SBOM+업로드+폴링+정책` 배선이 무거우므로, **게이트는 trivy로 두고 DT엔 SBOM을 보내 대시보드/모니터링**으로 병행하는 편이 낫다.
- **커버리지 누락 없음**: PR = **`trivy fs`**(소스 deps + IaC) + main = **`trivy image`**(이미지 레이어·OS 패키지). 종속성 취약점은 **두 지점에서** 걸린다 → 오히려 안전. **trivy를 유지하므로 현행 대비 커버리지 변화 없음.**

## 7. 열린 항목 (회의에서 결정)

1. **trivy 로컬 DB 캐시 배선**(주 조치) — self-hosted에 **trivy 설치** + **cron 하루 1회 DB 갱신** + **4개 Agent 공유 퍼시스턴트 볼륨**(4.C 다이어그램) + CI `--skip-db-update --cache-dir`. (스펙/호스트 + GW)
2. **스캔 4→1** — CI verify에 소스 스캔(gitleaks+trivy fs) 흡수(A) + **우리가 브랜치 정책에서 devsecops PR 게이트 정리**(B·우리 소관). **Jack = 거버넌스 승인만**(자체 CI verify 스캔 허용 여부). Jack의 [#13512](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13512) 게이트 정리가 **왜 라이브 정책에 미반영**인지도 확인.
3. **IaC 범위** — `trivy fs`를 유지하므로 현행 그대로(별도 결정 불요). image 스캔이 백스톱(6.2).
4. **DT 병행 여부**(선택·별건) — 게이트는 trivy로 두고, DT엔 SBOM을 보내 **배포 後 지속 모니터링**만 병행할지. 하려면: 현재 DT 공급 경로 확인 → SBOM 업로드 → 프로젝트/정책(급하지 않음).

## 8. 대안 (백업)

- **DB 소스 대안 — ECR 미러** — 로컬 캐시(cron+볼륨) 대신, trivy DB를 **우리 ECR에 미러**하고 CI가 `--db-repository <ecr>/trivy-db`로 ECR서 pull. cron/볼륨 juggling 대신 ECR pull-through가 갱신. 로컬 캐시와 **택일**(둘 다 gcr.io 제거).
- **DT를 게이트로(무거운 대안)** — trivy 대신 DT 정책을 게이트로. deps는 되나 **IaC 안 됨** + `SBOM+업로드+폴링+정책` 배선 필요 → **권장 안 함**(DT는 6.2처럼 모니터링 보완으로만).
- **최악 폴백** — devsecops 스캔을 **Microsoft-hosted 유지**(안정적). self-hosted 이득 일부 포기.

## 9. 역할 분담 (액션)

| 주체 | 작업 |
|---|---|
| **GW(구현 주체)** | ① **브랜치 정책에서 devsecops PR 게이트 정리** ② CI verify에 **gitleaks + `trivy fs`**(`--skip-db-update --cache-dir`) 추가 |
| **Jack(리뷰)** | **거버넌스 승인**: 자체 CI verify 스캔 허용 여부(중앙 SBOM/리포팅 영향). 중앙 템플릿 변경 필요 시 **우리 PR 리뷰** |
| **스펙/호스트** | self-hosted에 **trivy 설치 + DB 갱신 cron + 4-Agent 공유 캐시 볼륨** + 에이전트 메모리 여유 |
| **회의 결정** | 로컬 캐시 **vs** ECR 미러 / DT 모니터링 병행 여부 |

## 10. 현황 스냅샷

- **[#13480](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13480)** root CI self-hosted: 머지·작동.
- **[#13498](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13498)** devsecops pool self-hosted: **보류**(trivy DB 다운로드 반복 실패·2026-09-02 재확인).
- **[#13512](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/13512)** 트리거 main 제거: 머지(단, devsecops 게이트 4→1은 라이브 정책 미반영).
