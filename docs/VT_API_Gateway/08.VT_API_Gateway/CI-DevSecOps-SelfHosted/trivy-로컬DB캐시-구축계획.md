# self-hosted CI 보안 스캐너 (trivy·gitleaks) — 로컬 볼륨 · 새벽 자동 업그레이드

> CI 스캔이 매 실행 gcr.io에서 취약점 DB(110MB)를 받다 실패(flaky)하던 문제 + 바이너리 버전이 이미지에 박혀 방치되던 문제를, **스캐너 바이너리·DB를 사내 공유 볼륨에 두고 새벽 cron이 자동 최신화**하여 해결한다. (스캔구조 개선 C단계·[self-hosted-CI-DevSecOps-스캔구조-제안.md](self-hosted-CI-DevSecOps-스캔구조-제안.md))

- **작성/개정**: 2026-09-03 (스펙 세션·SSH 구축)
- **상태**: ✅ **구축 완료** — 볼륨 배치·새벽 cron·오프라인 스캔·자동 업그레이드 검증 완료. 남은 것은 A(GW CI verify가 볼륨 경로로 스캔 호출).
- **현재 버전**: trivy **0.74.0** · gitleaks **8.30.1** (이후 cron이 자동 최신).

---

## 1. 대상 호스트

- **BuildMachine2**(`wbs.ewoosoft.com`) · Self-hosted1 풀 · 접속 `ssh -i ~/.ssh/id_rsa raymond@wbs.ewoosoft.com`(keyless).
- CI 에이전트 = docker 컨테이너 4대 `azp-agent-linux1..4`. **`/opt/trivy-cache` 를 `:ro` 마운트**(C에서 배선·재설치 완료).
- 호스트 관리 파일 = `/home/raymond/azp-agent-in-docker/`(에이전트 dockerfile·reinstall·ci-scanners-update.sh 동거).

---

## 2. 최종 구조

```
        GitHub releases (trivy·gitleaks 바이너리)   gcr.io (trivy-db 110MB)
                        │  새벽 1회만 접속 (CI 밖 · flaky해도 재시도 · CI 무영향)
                        ▼
   ┌──────────────────────────────────────────────────────────┐
   │  ci-scanners-update.sh  (host cron · KST 03:00)           │
   │   · trivy/gitleaks latest 확인 → smoke-test → 원자 교체    │
   │   · trivy DB 갱신(재시도 5회)                              │
   └───────────────────────────┬──────────────────────────────┘
                               │ write
                               ▼
   /opt/trivy-cache/   (raymond 소유 · 재부팅 생존)
     ├─ bin/trivy      ← 최신 바이너리(cron 교체)
     ├─ bin/gitleaks   ← 최신 바이너리(cron 교체)
     ├─ db/trivy.db    ← 취약점 DB(cron 갱신·바이너리와 스키마 매칭)
     └─ update.log
                               │  (:ro 마운트)
        ┌──────────┬───────────┴──────────┬──────────┐
     Agent1     Agent2                  Agent3     Agent4
   CI verify 스캔 = /opt/trivy-cache/bin/{trivy,gitleaks} (오프라인·gcr.io 미접속)
```

**핵심 원리**
- 스캐너를 **이미지에 안 박고 공유 볼륨**에 둔다 → **버전업에 이미지 재빌드/에이전트 재설치 불요**(cron이 볼륨 바이너리만 교체, 에이전트는 마운트로 즉시 반영).
- **새벽 자동 업그레이드**: latest 확인 → smoke-test 통과 시에만 교체(나쁜 릴리스 차단·실패 시 옛 버전 유지). CI 안 도는 시간이라 교체 안전.
- **trivy 바이너리↔DB 스키마 매칭**: 갱신을 같은 스크립트가 함께 처리.
- **gitleaks**: DB 없는 정적 바이너리 → 완전 오프라인.

---

## 3. CI 소비 계약 (A단계·GW)

에이전트 안(=CI verify 스텝)에서 **볼륨 경로**로 호출한다. trivy는 DB를 심링크로 참조(1.3GB 복사 회피).

```bash
# 소스 종속성 스캔 (trivy fs · 오프라인)
TRIVY_LOCAL="$(mktemp -d)"
ln -s /opt/trivy-cache/db "$TRIVY_LOCAL/db"        # DB는 공유 마운트 심링크(읽기전용)·fanal만 로컬
/opt/trivy-cache/bin/trivy fs --skip-db-update --cache-dir "$TRIVY_LOCAL" \
  --scanners vuln --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 .

# 시크릿 스캔 (gitleaks git · full history · audit) — checkout fetchDepth: 0 필요
/opt/trivy-cache/bin/gitleaks git --redact --exit-code 1 \
  --report-format sarif --report-path "$(Agent.TempDirectory)/gitleaks.sarif" . || RC=$?
# RC==1 → 경고 + SucceededWithIssues(audit·devsecops secret-scan.yml과 동일 기준)
```
- ⚠ **반드시 `/opt/trivy-cache/bin/` 경로**(이미지 PATH 아님) — 볼륨이 자동 최신이라. `--skip-db-update` 필수(gcr.io 미접속).
- ✅ 2026-09-03 실증: 에이전트에서 볼륨 경로 오프라인 스캔 TRIVY_VOL_OK·GITLEAKS_VOL_OK.

---

## 4. 새벽 자동 갱신 (`ci-scanners-update.sh` · KST 03:00)

1. **trivy 바이너리**: GitHub latest 확인 → 새 버전이면 임시 다운로드 → **기존 로컬 DB로 smoke-test**(`trivy fs --skip-db-update`·**네트워크 0** — smoke 자체가 gcr.io flaky에 안 걸리게) → 통과 시 원자 교체(`mv`), 실패 시 옛 버전 유지.
2. **trivy DB**: 활성 바이너리로 `image --download-db-only` — **gcr.io flaky 대비 5회 재시도**(20s 간격). 새벽이라 재시도해도 CI 무영향·마지막 성공본 유지.
3. **gitleaks 바이너리**: latest 확인 → 다운로드 → `version` smoke → 교체(DB 없음).
- **긴급 고정**: `TRIVY_PIN`/`GITLEAKS_PIN` 환경변수 설정 시 그 버전에 잠금(latest 무시).

---

## 관리 파일 (정본 위치)

| 파일 | 정본 | 호스트/적용 | 역할 |
| --- | --- | --- | --- |
| `ci-scanners-update.sh` | `references/Self-hosted1/` | `/home/raymond/azp-agent-in-docker/`(cron 03:00) | 새벽 자동 갱신(바이너리+DB) |
| cron 등록 | (본 문서 §4·한 줄) | raymond crontab | `0 18 * * *` |
| `azp-agent-linux.dockerfile` | `references/Self-hosted1/` | `/home/raymond/azp-agent-in-docker/` | 에이전트 이미지(스캐너는 **미포함**·볼륨 사용) |
| `reinstall_agent.sh` | `references/Self-hosted1/` | `/home/raymond/azp-agent-in-docker/` | `-v /opt/trivy-cache:ro` 마운트 |
| CI 소비 스니펫(§3) | A단계·GW repo(CI verify) | vt-api-gateway | 스캔 실행 |

- `/opt/trivy-cache/{bin,db,update.log}` = 호스트 런타임 산출물(cron 관리·git 아님).

---

## 5. 운영·관리

| 무엇 | 방법 |
| --- | --- |
| **현재 버전** | `/opt/trivy-cache/bin/trivy --version` · `/opt/trivy-cache/bin/gitleaks version` |
| **갱신 로그·신선도** | `tail /opt/trivy-cache/update.log`(마지막 "update done" 라인에 버전) |
| **수동 즉시 갱신** | `/home/raymond/azp-agent-in-docker/ci-scanners-update.sh` |
| **버전 업그레이드** | **자동**(새벽 cron·latest+smoke). 사람이 할 일 없음 |
| **특정 버전 고정(긴급)** | cron/스크립트에 `TRIVY_PIN=x.y.z` / `GITLEAKS_PIN=x.y.z` 지정 |
| **경보(권장·후속)** | update.log 마지막 성공이 48h 초과 시 알림 |

**트러블슈팅**
- CI 스캔이 gcr.io 침 → 소비가 `--skip-db-update` 빠졌거나 `/opt/trivy-cache/bin/` 아닌 이미지 PATH 호출.
- DB 갱신 5회 실패(로그 `DB FAIL`) → gcr.io/네트워크 문제·마지막 성공본으로 CI는 계속 동작(긴급 아님).
- 새 trivy가 smoke 실패("db schema"·스캔 오류) → 옛 버전 유지·로그 확인(드묾). 필요 시 `TRIVY_PIN`으로 안정 버전 고정.

---

## 6. 재부팅·롤백

- **재부팅 후 유지**: 볼륨(`/opt/trivy-cache`)·cron·에이전트 마운트(restart=unless-stopped) 모두 생존. cron이 다음 새벽 갱신.
- **롤백**: 소비에서 볼륨 경로/`--skip-db-update`를 빼면 즉시 온라인 DB(구 동작). `TRIVY_PIN`/`GITLEAKS_PIN`으로 버전 고정. 자동 업그레이드 중단하려면 cron 라인 제거.

---

## 7. 구축 경위 (히스토리)

- C 최초: trivy DB를 docker로 받아 `/opt/trivy-cache/db`(root 소유)에 캐시 + 에이전트 이미지에 trivy·gitleaks 바이너리 내장(수동 업그레이드).
- 개선(2026-09-03·본 문서): 바이너리 방치 위험 지적 → **볼륨+새벽 cron 자동 업그레이드**로 전환. 이미지에서 스캐너 제거, `db/` 소유권 raymond 이전(`chown -R`), `trivy-db-update.sh` → `ci-scanners-update.sh`로 확장(바이너리 smoke+DB 재시도). 에이전트 재설치 불요.
