# host/ — 빌드 호스트 배치 미러

빌드 호스트 `wbs.ewoosoft.com`(BuildMachine2)에 **실제로 배치된** 설정 파일들의 미러다.
디렉토리 구조는 호스트의 `/home/raymond/` 아래 실제 경로를 그대로 따른다.

```
host/
  azp-agent-in-docker/     <- ~/azp-agent-in-docker/
  Docker/                  <- ~/Docker/
  Documents/dtrack/        <- ~/Documents/dtrack/
```

## 왜 만들었나

2026-09-10 호스트-저장소 동기화 점검에서 두 가지가 드러났다.

첫째, 같은 파일의 사본이 세 곳(이 저장소 · `sbom/jenkins` 저장소 · 호스트)에 흩어져 있고
어디가 정본인지 정해져 있지 않아 전부 갈라져 있었다. 6개 중 정본과 호스트가 일치한 것은
`ci-scanners-update.sh` 하나였고, 그것만 헤더에 정본이 적혀 있었다.

둘째, SonarQube·Dependency-Track compose 파일은 **어디에도 버전관리가 안 되고** 호스트에만
있었다. 호스트를 잃으면 복구할 근거가 없다.

## 정본이 어디인가

**각 파일 헤더의 "관리 정본" 표기를 따를 것.** 여기 있는 파일이 전부 정본은 아니다.

| 파일 | 정본 |
|---|---|
| `azp-agent-in-docker/azp-agent-linux.dockerfile` | 이 저장소 |
| `azp-agent-in-docker/ci-scanners-update.sh` | 이 저장소 |
| `azp-agent-in-docker/start.sh` | 이 저장소 |
| `azp-agent-in-docker/reinstall_agent.sh` | 이 저장소 (**git 추적 제외** — ADO PAT 평문) |
| `Docker/docker-compose.sonarqube.yml` | 이 저장소 |
| `Docker/docker-compose.sonarqube-dtrack.yml` | 이 저장소 (무력화된 안내 파일) |
| `Documents/dtrack/Dockerfile` | 이 저장소 |
| `Documents/dtrack/docker-compose-dependency-track.yml` | 이 저장소 |

호스트에 배치되지만 정본이 **`sbom/jenkins` 저장소**인 것들은 여기 사본을 두지 않는다.
중복이 곧 드리프트라서다.

| 호스트 경로 | 정본 |
|---|---|
| `~/azp-agent-in-docker/jenkins-node.dockerfile` | `sbom/jenkins` · `docker/jenkins-node.dockerfile` |
| `~/azp-agent-in-docker/reinstall_jenkins_nodes.sh` | `sbom/jenkins` · `docker/reinstall_jenkins_nodes.sh` |
| (직접 빌드) `jenkins-node:java21` | `sbom/jenkins` · `docker/jenkins-node-java21.dockerfile` |

## 2026-09-10 변경분

- `azp-agent-in-docker/` — 기존에 `Self-hosted1/` 루트에 평면으로 있던 4개를 옮겼다
- `Docker/docker-compose.sonarqube.yml` — 신규. SonarQube 전용으로 분리
- `Docker/docker-compose.sonarqube-dtrack.yml` — DT 정의를 걷어내고 안내문만 남긴 상태
- `Documents/dtrack/` — 신규 추가. 그때까지 버전관리 밖에 있었다

## 시크릿

이 저장소는 GitHub(`github.com/gracegyu/scp-architecture`)에 올라간다. 사내망 격리와
무관하게 외부다. 그래서 값을 그대로 두지 않는다.

- `reinstall_agent.sh` — Azure DevOps PAT 평문. `.gitignore`로 추적 제외
- `docker-compose-dependency-track.yml` — NVD API 키를 `${NVD_API_KEY}`로 가렸다
- PostgreSQL 비밀번호(`postgres`)는 내부 전용 값이라 그대로 둔다. 기존 설치 문서에도 그 값이 적혀 있다
