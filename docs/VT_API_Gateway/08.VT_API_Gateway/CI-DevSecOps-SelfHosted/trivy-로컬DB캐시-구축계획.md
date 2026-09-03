# 구축 계획: trivy 로컬 DB 캐시 (self-hosted · 스캔구조 개선 C단계)

> 목적: CI의 trivy 스캔이 매 실행 gcr.io에서 취약점 DB(약 110MB)를 받다가 실패(flaky)하는 것을, **DB를 self-hosted 로컬에 미리 받아두고 CI는 오프라인으로 읽게** 하여 근본 제거한다. (제안서 §4.C·[self-hosted-CI-DevSecOps-스캔구조-제안.md](self-hosted-CI-DevSecOps-스캔구조-제안.md))

- **작성**: 2026-09-03 (스펙 세션)
- **상태**: ✅ **구축 완료(2026-09-03)** — DB 캐시·cron·에이전트(trivy 0.74.0+마운트) 배선·오프라인 스캔 검증 완료. 남은 것은 A(GW CI verify에 §3 스니펫 배선).
- **구축 주체**: 스펙 세션이 SSH로 직접 수행(에이전트 재구축 때와 동일 방식)
- **선행/병행**: 순서 B → **C** → A. B(es-ci-templates `sourceDepScan` 토글·PR #13568)는 Jack 리뷰 중이며 C와 병행 가능. C 완료 후 A(CI verify에 trivy fs 추가·GW)가 이 캐시를 소비.

---

## 1. 대상 호스트

- **BuildMachine2** (`wbs.ewoosoft.com`) · Self-hosted1 풀 · 접속 `ssh -i ~/.ssh/id_rsa raymond@wbs.ewoosoft.com`(keyless).
- CI 에이전트 = **docker 컨테이너 4대** `azp-agent-linux1..4`(`azp-agent:linux` 이미지·root 실행·`--memory=6g`·docker.sock 마운트).
- **호스트 작업 경로(실물) = `/home/raymond/azp-agent-in-docker/`** — 여기에 `azp-agent-linux.dockerfile`·`start.sh`·`reinstall_agent.sh`가 있고 빌드·재설치가 여기서 돈다. (scp의 `references/Self-hosted1/`는 이 내용의 문서 미러 — 변경 시 함께 동기화.)
- docker는 sudo 없이(그룹), `/opt` 생성 등 일부만 sudo(암호) 필요 → 해당 단계는 Raymond 실행(아래 명시).

---

## 2. 설계 (구성 요소)

```
        gcr.io (aquasec/trivy-db · ~110MB)
              │  ← 하루 1회만 접속 (CI 밖 · 실패해도 재시도·CI 무영향)
              ▼
   ┌──────────────────────────────────────────┐
   │  DB updater  (host cron · daily)          │  docker run aquasec/trivy image --download-db-only
   └───────────────────┬──────────────────────┘
                       │ write
                       ▼
   /opt/trivy-cache/db/  (호스트 공유 볼륨 · 재부팅 생존)   ← trivy.db + metadata.json
                       │  (읽기전용 마운트)
        ┌──────────┬───┴──────┬──────────┐
     Agent1     Agent2     Agent3     Agent4     ← CI 스캔(trivy fs · gcr.io 미접속)
   (trivy 바이너리 이미지에 포함 · /opt/trivy-cache:ro 마운트)
```

**3요소:**
1. **공유 캐시 볼륨** `/opt/trivy-cache` — 호스트 퍼시스턴트 디렉터리. DB 1벌을 4 에이전트가 공유(재시작·재부팅 생존).
2. **DB updater (cron·하루 1회)** — `aquasec/trivy` 컨테이너로 `--download-db-only` 실행해 `/opt/trivy-cache`에 DB 갱신. **gcr.io 접속은 여기서만**, 실패해도 CI를 안 막고 다음날 재시도(마지막 성공본 유지).
3. **에이전트 소비** — 에이전트 이미지에 **trivy 바이너리 포함** + `/opt/trivy-cache`를 **읽기전용 마운트**. CI(A단계)는 `trivy fs --skip-db-update`로 이 DB를 오프라인 사용.

**버전 핀 = `0.74.0`**(2026-09-03 확정·구축 시점 최신 안정본): updater 이미지(`aquasec/trivy:0.74.0`)와 에이전트 trivy 바이너리를 **동일 버전으로 핀**한다(DB 스키마 호환). 갱신 시 둘을 함께 올린다.

**DB 종류**: JS/TS(Node) 레포라 **메인 취약점 DB(trivy-db)만** 받는다. Java jar 스캔용 `trivy-java-db`는 불필요(추후 java 스캔 필요 시 `--download-java-db-only` 추가).

**신선도(staleness)**: DB가 24h 넘어도 `--skip-db-update`는 그대로 스캔(graceful). 최종 백스톱은 build 스테이지의 이미지 스캔(별개). cron이 며칠 실패하면 경보(아래 §5).

---

## 3. A(CI)와의 소비 계약 — GW가 CI verify에 붙일 형태

에이전트 컨테이너 안에서(=CI verify 스텝) 아래처럼 소비한다. **`--cache-dir`는 쓰기 가능한 로컬 경로**로 두고, 공유 볼륨의 DB만 복사해 넣는다(읽기전용 마운트 충돌·4에이전트 동시쓰기 회피).

```bash
TRIVY_LOCAL="$(mktemp -d)"                     # 에이전트 로컬(fanal 스캔 캐시 쓰기용)
ln -s /opt/trivy-cache/db "$TRIVY_LOCAL/db"    # DB는 공유 마운트를 심링크(읽기전용)로 참조 → 1.3GB 복사 회피
trivy fs --skip-db-update --cache-dir "$TRIVY_LOCAL" \
  --scanners vuln --severity HIGH,CRITICAL --ignore-unfixed \
  --exit-code 1 .
```
> ✅ 2026-09-03 실증: 에이전트 안에서 위 심링크 방식으로 `--skip-db-update` 오프라인 스캔 성공(gcr.io 미접속). DB(trivy.db ~1.3GB)는 마운트로 읽고 fanal 캐시만 로컬에 쓴다.

- `--skip-db-update` = **gcr.io 미접속**(로컬 DB 사용). 접속 실패 소멸.
- 스캔 옵션(severity·ignore-unfixed·scanners)은 기존 devsecops `dep-scan-trivy.yml`과 정렬 — **A단계에서 GW가 기존 게이트와 동일 기준으로** 맞춘다(별도 확인).
- 이 계약(경로 `/opt/trivy-cache/db/`·복사 후 skip-db-update)만 지키면 A의 스텝 세부는 GW 소관.

---

## 관리 파일 (정본 위치)

C로 생기거나 바뀌는 산출물과 정본 위치. **정본에서 편집 → 호스트/파이프라인으로 배포**한다.

| 파일 | 정본 위치 | 호스트/적용 위치 | 역할 |
| --- | --- | --- | --- |
| `trivy-db-update.sh` | `references/Self-hosted1/` 미러 | `/home/raymond/azp-agent-in-docker/trivy-db-update.sh`(cron) | DB 하루 1회 갱신 |
| cron 등록 | (본 계획서 §4-3 한 줄) | raymond crontab | updater 스케줄 |
| `azp-agent-linux.dockerfile`(trivy + gitleaks 추가분) | `references/Self-hosted1/` 미러 | `/home/raymond/azp-agent-in-docker/` | 에이전트에 trivy(0.74.0)·gitleaks(8.30.1) 바이너리 |
| `reinstall_agent.sh`(볼륨 마운트 추가분) | `references/Self-hosted1/` 미러 | `/home/raymond/azp-agent-in-docker/` | `/opt/trivy-cache:ro` 마운트 |
| CI 소비 스니펫(`trivy fs --skip-db-update`) | **A단계·GW repo**(CI verify 파이프라인) | vt-api-gateway | 스캔 실행(§3 계약) |

- **버전 핀**은 `trivy-db-update.sh`의 `TRIVY_VERSION` + dockerfile의 trivy 설치 버전 **두 곳을 동일하게**.
- `/opt/trivy-cache/db/`(DB 실물)·`/opt/trivy-cache/update.log`(로그)는 **호스트 런타임 산출물**(git 관리 아님·§5에서 조회).

## gitleaks (시크릿 스캔 · 이미지 내장 · 2026-09-03)

CI verify의 시크릿 스캔(gitleaks)도 **에이전트 이미지에 바이너리 내장**한다 — trivy와 동일 오프라인 원칙(컨테이너/설치 방식은 매 실행 network pull이라 우리가 없애려던 그 문제를 재도입).

- **trivy와 다른 점**: gitleaks는 **취약점 DB가 없다**(패턴이 바이너리에 내장된 정적 스캐너) → **cron·공유 캐시 볼륨 불요**. 이미지에 바이너리만 있으면 완전 오프라인.
- **버전 = 8.30.1**(2026-09-03 최신 안정본). dockerfile `ARG GITLEAKS_VERSION`.
- **소비(A단계 ②·GW)**: CI verify에 gitleaks 게이트 추가(기존 devsecops `secret-scan.yml`과 동일 기준). full history 스캔이면 checkout `fetchDepth: 0` 필요.
- **✅ 반영 완료(2026-09-03)**: 에이전트 이미지에 gitleaks 8.30.1 설치 + 4대 재설치 완료(실행 중 `gitleaks version`=8.30.1 확인). GW가 CI verify에 게이트만 붙이면 됨.

## 4. 구축 절차 (SSH)

> 범례: **[R]** = Raymond가 실행(sudo 필요) · **[S]** = 스펙 세션이 SSH로 실행

### 4-1. 공유 볼륨 생성 **[R]** (sudo·1회)
```bash
sudo mkdir -p /opt/trivy-cache
sudo chown raymond:raymond /opt/trivy-cache      # 이후 cron(raymond)이 write·agent가 read
```

### 4-2. updater 스크립트 배포 + DB 최초 채움 **[S]**
updater 정본은 **[`references/Self-hosted1/trivy-db-update.sh`](../../references/Self-hosted1/trivy-db-update.sh)**(dockerfile·reinstall_agent.sh와 같은 미러) — 호스트로 배포해서 쓴다(호스트에서 heredoc으로 만들지 않음).
```bash
# (1) 정본 스크립트를 호스트의 에이전트 관리 폴더에 배포(다른 관리파일과 동거)
scp references/Self-hosted1/trivy-db-update.sh raymond@wbs.ewoosoft.com:/home/raymond/azp-agent-in-docker/trivy-db-update.sh
ssh -i ~/.ssh/id_rsa raymond@wbs.ewoosoft.com 'chmod +x /home/raymond/azp-agent-in-docker/trivy-db-update.sh'
# (2) 최초 1회 실행(이후 cron이 갱신) — 스크립트가 DB를 /opt/trivy-cache/db 에 받는다
ssh -i ~/.ssh/id_rsa raymond@wbs.ewoosoft.com '/home/raymond/azp-agent-in-docker/trivy-db-update.sh && tail -2 /opt/trivy-cache/update.log'
```
(스크립트 상단 `TRIVY_VERSION`이 버전 핀 — updater·에이전트 동일. 변경은 이 폴더 정본에서 하고 재배포.)

### 4-3. cron 등록 (하루 1회·raymond 사용자) **[S]**
```bash
( crontab -l 2>/dev/null; echo "0 18 * * * /home/raymond/azp-agent-in-docker/trivy-db-update.sh" ) | crontab -
# 18:00 UTC = KST 03:00(야간·CI 한산). 로그 = /opt/trivy-cache/update.log
```

### 4-4. 에이전트 이미지에 trivy 추가 + 볼륨 마운트 **[S]** (호스트 `/home/raymond/azp-agent-in-docker/`)
- ✅ **미러 반영 완료(2026-09-03·0.74.0)**: `references/Self-hosted1/azp-agent-linux.dockerfile`에 trivy 설치(`ARG TRIVY_VERSION=0.74.0`) · `reinstall_agent.sh`에 `-v /opt/trivy-cache:/opt/trivy-cache:ro` 추가됨.
- 호스트 배포 + 재빌드 + 재설치:
  ```bash
  scp azp-agent-linux.dockerfile reinstall_agent.sh raymond@wbs.ewoosoft.com:/home/raymond/azp-agent-in-docker/
  ssh ... 'cd /home/raymond/azp-agent-in-docker && docker build --tag azp-agent:linux --file azp-agent-linux.dockerfile . && ./reinstall_agent.sh'
  # ⚠ 에이전트 4대 재생성(deregister/reregister) → CI 한산한 때
  ```

### 4-5. 검증 **[S]**
```bash
# 에이전트 안에서 오프라인 스캔이 되는지
docker exec azp-agent-linux1 sh -lc '
  T=$(mktemp -d); mkdir -p "$T/db"
  cp /opt/trivy-cache/db/trivy.db /opt/trivy-cache/db/metadata.json "$T/db/"
  trivy fs --skip-db-update --cache-dir "$T" --scanners vuln /usr/ >/dev/null && echo OFFLINE_SCAN_OK'
# DB 신선도
cat /opt/trivy-cache/update.log | tail -3
```

---

## 5. 운영·관리 (추후 참조)

| 무엇 | 방법 |
| --- | --- |
| **DB 신선도 확인** | `tail /opt/trivy-cache/update.log` (마지막 OK 시각) · `stat /opt/trivy-cache/db/trivy.db` |
| **수동 갱신** | `/home/raymond/azp-agent-in-docker/trivy-db-update.sh` 직접 실행 |
| **cron 동작 확인** | `crontab -l` · 로그 파일 최근 라인 |
| **trivy 버전 올리기** | ⚠ 바이너리↔DB 스키마 호환. ① `references/Self-hosted1/`의 dockerfile `ARG TRIVY_VERSION` + `trivy-db-update.sh` `TRIVY_VERSION` **동일 변경** → ② **updater 먼저 실행**(새 스키마 DB 다운로드) → ③ 이미지 재빌드 + 에이전트 4대 재설치. 안 맞추면 `db schema version` 오류 |
| **gitleaks 버전 올리기** | DB 없음(정적 바이너리)이라 간단: dockerfile `ARG GITLEAKS_VERSION` 변경 → 이미지 재빌드 + 에이전트 4대 재설치. updater·캐시 무관 |
| **버전 확인(현재)** | 에이전트 안 `trivy --version`(0.74.0)·`gitleaks version`(8.30.1). 정본 핀 = `references/Self-hosted1/` dockerfile ARG · `trivy-db-update.sh` |
| **디스크** | `/opt/trivy-cache` 용량(수백 MB) · `df -h /` |
| **경보(권장)** | update.log 마지막 성공이 48h 초과면 알림(후속·§6.3.2 관측과 연계 가능) |

**트러블슈팅:**
- CI에서 `trivy fs`가 gcr.io를 치면 → `--skip-db-update` 누락 or `--cache-dir`에 db 없음(복사 단계 확인).
- `db schema version` 오류 → updater trivy와 에이전트 trivy 버전 불일치(핀 재정렬).
- cron이 계속 FAIL → gcr.io 접근/네트워크(마지막 성공본으로 CI는 계속 동작·긴급 아님).

---

## 6. 롤백

- 되돌리기 간단: A(CI)에서 `--skip-db-update`를 빼면 즉시 온라인 DB(구 동작)로 복귀. cron·볼륨·에이전트 마운트는 그대로 둬도 무해.
- 에이전트 마운트/이미지 변경만 되돌리려면 reinstall_agent.sh 원복 후 재설치.

---

## 7. 결정·확인 필요

1. ~~trivy 버전 핀~~ — **✅ `0.74.0` 확정**(2026-09-03·최신 안정본). updater·에이전트 동일 반영 완료.
2. **스캔 기준(severity·ignore-unfixed·scanners)** — 기존 devsecops `dep-scan-trivy.yml`과 동일하게 A에서 맞춤(GW 확인).
3. **cron 시각** — KST 03:00(18:00 UTC) 제안. 변경 원하면 조정.
4. **4-1 sudo 단계** — Raymond 실행(또는 passwordless sudo 없으면 그 한 줄만 대신).
