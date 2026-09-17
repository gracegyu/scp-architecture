# sec-tools — 취약점·코드품질 조회 도구

사내 **Dependency-Track**(의존성 취약점)과 **SonarQube**(코드 품질·보안)에 **REST API 로 직접** 붙는 명령줄 도구다.

- **SSH 불필요** · 빌드 서버 접속 권한 없어도 된다
- **추가 설치 불필요** · Python 3.8+ 표준 라이브러리만 쓴다
- **AI 코딩 도구에 그대로 넘길 수 있다** — `--json` 출력을 Claude Code 등에 물리면 취약점 파악부터 수정까지 이어진다

> ⚠ 사내망에서만 접속된다. 재택이면 VPN 이 필요하다.

---

## 어디에 둘 것인가

**프로젝트 안에 복사하지 말 것.** 여러 저장소에서 쓰게 되는데, 복사본이 늘어나면 서로 어긋난다.

**홈 디렉토리에 한 벌만 두고 모든 프로젝트에서 공유한다.**

### macOS · Linux

```bash
mkdir -p ~/.claude
cp -r <이 폴더> ~/.claude/sec-tools
cd ~/.claude/sec-tools
cp .env.example .env          # 키는 여기 한 번만 넣으면 된다

# 어디서나 sec 로 부를 수 있게 (PATH 에 ~/.local/bin 이 있어야 한다)
mkdir -p ~/.local/bin
ln -sf ~/.claude/sec-tools/sec.py ~/.local/bin/sec
chmod +x ~/.claude/sec-tools/sec.py
```

`~/.local/bin` 이 PATH 에 없으면 `~/.zshrc` 나 `~/.bashrc` 에 추가한다.

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Windows

```powershell
mkdir "$env:USERPROFILE\.claude" -Force
Copy-Item -Recurse <이 폴더> "$env:USERPROFILE\.claude\sec-tools"
cd "$env:USERPROFILE\.claude\sec-tools"
copy .env.example .env
```

어디서나 부르려면 **시스템 환경 변수 → Path** 에 `%USERPROFILE%\.claude\sec-tools` 를 추가한다. 그러면 `sec check` 로 쓸 수 있다(`sec.cmd` 래퍼가 들어 있다).

PATH 에 넣지 않으려면 전체 경로로 부른다.

```powershell
python "$env:USERPROFILE\.claude\sec-tools\sec.py" check
```

---

## Claude Code 가 이 도구를 알게 하기

여기까지 하면 사람이 쓸 수 있다. **Claude Code 가 모든 프로젝트에서 이 도구를 알아서 쓰게 하려면** 전역 메모리에 한 줄 등록한다.

`~/.claude/CLAUDE.md`(Windows 는 `%USERPROFILE%\.claude\CLAUDE.md`)에 아래를 추가한다. 파일이 없으면 새로 만든다.

```markdown
## 보안 도구 (sec-tools)

사내 Dependency-Track·SonarQube 조회 도구가 `~/.claude/sec-tools/sec.py` 에 있다.
취약점·코드 이슈를 물어보면 이것을 쓴다. `--json` 을 붙이면 구조화된 출력이 나온다.

    python3 ~/.claude/sec-tools/sec.py projects <검색어>     프로젝트 찾기
    python3 ~/.claude/sec-tools/sec.py --json vulns <프로젝트>    DT 취약점
    python3 ~/.claude/sec-tools/sec.py --json issues <프로젝트>   SonarQube 이슈

사내망에서만 동작한다. 설정은 `~/.claude/sec-tools/README.md` 참조.
```

이 파일은 **모든 프로젝트의 Claude Code 세션에 자동으로 로드**된다. 프로젝트마다 설명할 필요가 없다.

> 특정 저장소에서만 쓰는 도구라면 그 저장소의 `CLAUDE.md` 에 넣는 것이 맞다. 이건 전사 공통이라 전역에 둔다.

---

## 빠른 시작

설치를 마쳤으면 키 두 개를 채우고 점검한다.

```bash
cd ~/.claude/sec-tools
cp .env.example .env
# .env 에 키 두 개를 채운다 (아래 1·2단계)
./sec.py check                 # Windows: python sec.py check
```

`check` 가 모두 `[OK]` 면 끝이다.

---

## 1단계 — Dependency-Track API 키

DT 는 **팀 단위로 API 키**를 발급한다. 개인 계정이 아니라 팀 키를 공유해 쓴다.

### 개발자

**관리자에게 읽기 전용 API 키를 요청**해서 `.env` 의 `DTRACK_API_KEY` 에 넣는다. 발급은 관리자 몫이다.

### 관리자 (최초 1회)

```
http://dtrack.ewoosoft.com → Administration → Access Management → Teams
  → Create Team:  Developers (Read Only)
  → Permissions:  VIEW_PORTFOLIO
                  VIEW_VULNERABILITY
                  VIEW_POLICY_VIOLATION
  → API Keys → + 로 키 생성
```

⚠ **`BOM_UPLOAD` 와 `PORTFOLIO_MANAGEMENT` 는 주지 않는다.** 조회 전용이어야 실수로 데이터를 바꾸지 않는다.

> 자동화용 `Automation` 팀 키를 그대로 돌려쓰지 말 것. 그 키는 BOM 업로드 권한이 있어 CI 가 쓰는 것이다.

---

## 2단계 — SonarQube 토큰

SonarQube 는 **개인 계정 토큰**을 쓴다. 각자 발급한다.

```
http://sqube.ewoosoft.com → 로그인
  → 우측 상단 계정 → My Account → Security
  → Generate Tokens
       Name:  sec-tools
       Type:  User Token
       Expires in: 조직 정책에 맞게
  → Generate → 화면에 한 번만 보인다. 그때 복사한다
```

`.env` 의 `SONAR_TOKEN` 에 넣는다.

⚠ **개인 토큰을 쓰는 이유가 있다.** CI 자동화 토큰은 `hotspots` 조회 권한이 없어 `./sec.py hotspots` 가 막힌다. 개인 계정이면 대개 열려 있다.

---

## 사용법

```
sec check                  설정·연결·권한 점검
sec projects [검색어]      DT·SonarQube 프로젝트 검색
sec vulns <프로젝트>       DT 취약점 상세
sec issues <프로젝트>      SonarQube 미해결 이슈
sec hotspots <프로젝트>    SonarQube security hotspot
sec analyze <프로젝트>     DT 재분석 요청
```

PATH 에 등록하지 않았다면 아래처럼 부른다.

| | 명령 |
|---|---|
| macOS · Linux | `./sec.py check` 또는 `python3 sec.py check` |
| Windows | `python sec.py check` 또는 `sec.cmd check` |

⚠ **Windows 에서 `python3` 은 쓰지 말 것.** Microsoft Store 가 열린다. `python` 이 맞다.

`<프로젝트>` 는 **이름 일부**면 된다. 여러 개가 걸리면 목록을 보여 주니 더 좁혀서 다시 부르면 된다. 이름이 정확히 일치하면 그것을 고른다. DT 는 UUID 를 그대로 줘도 된다.

### 예

내 프로젝트 찾기.

```
$ ./sec.py projects vt
Dependency-Track — 2개 (BOM 있는 것만)

  vt-api-gateway-console 1.0.0        취약점    6   dd56db3b-fef6-4939-a73b-6c6c8e8a1f6e
  vt-api-gateway 1.0.0                취약점    2   729320de-d848-4ba9-a29a-c17dece5f6f1

SonarQube — 2개

  es-platforms_vt-api-gateway
  es-platforms_vt-api-gateway-console
```

취약점 보기.

```
$ ./sec.py vulns vt-api-gateway
vt-api-gateway 1.0.0 — 취약점 2건

  심각도        취약점 ID                CVSS  컴포넌트                               출처
  ---------- -------------------- -----  ---------------------------------- --------
  MEDIUM     GHSA-4mjr-xmp4-gh2g      -  qs@6.15.3                          GITHUB
  LOW        GHSA-x5fp-wj9c-mxmx      -  qs@6.15.3                          GITHUB
```

코드 이슈 보기.

```
$ ./sec.py issues es-platforms_vt-api-gateway
es-platforms_vt-api-gateway — 미해결 이슈 35건 (최대 200건 표시)

  CRITICAL  CODE_SMELL   apps/admin/src/targets/...:57   Refactor this function to reduce its ...
  CRITICAL  BUG          apps/core/src/config/...:112    Provide a compare function that ...
```

---

## AI 코딩 도구와 함께 쓰기

`--json` 을 붙이면 구조화된 출력이 나온다. 이것을 Claude Code 등에 그대로 넘기면 **취약점 파악 → 해당 의존성 찾기 → 버전 상향 → 검증**까지 이어갈 수 있다.

```bash
./sec.py --json vulns vt-api-gateway > vulns.json
```

```
Claude Code 에서:
  vulns.json 을 읽고, 각 취약점이 어느 lock 파일의 어느 의존성인지 찾아
  안전하게 올릴 수 있는 것부터 제안해 줘
```

출력에 `purl`(예: `pkg:npm/qs@6.15.3`)이 들어 있어 패키지 생태계와 정확한 버전을 바로 알 수 있다.

⚠ **자동으로 전부 올리게 두지 말 것.** 메이저 버전 상향은 breaking change 를 부르고, 수정 버전이 아직 없는 취약점도 있다. **제안을 받고 사람이 판단**하는 방식이 맞다.

---

## 고치고 나서

의존성을 올렸으면 **DT 에 반영되기까지 두 단계**가 있다.

1. **SBOM 이 다시 올라가야 한다** — Jenkins SBOM 잡이 매일 새벽에 돈다. 급하면 잡을 수동 실행한다.
2. **재분석** — 새 SBOM 이 올라가면 자동으로 분석된다.

취약점 소스(OSV·GHSA)만 갱신된 경우처럼 **컴포넌트는 그대로인데 다시 보고 싶을 때**는 SBOM 재업로드 없이 이것으로 충분하다.

```bash
./sec.py analyze vt-api-gateway
```

> DT 는 BOM 이 올라오는 시점에만 분석한다. 취약점 DB 가 갱신돼도 기존 프로젝트를 소급해서 다시 보지 않는다.

---

## 문제 해결

| 증상 | 원인·조치 |
|---|---|
| `연결할 수 없다` | 사내망 밖이다. VPN 확인. |
| (Windows) `python` 을 못 찾음 | [python.org](https://www.python.org/downloads/) 에서 설치. 설치 시 **Add python.exe to PATH** 를 체크할 것. |
| (Windows) 한글이 깨짐 | 스크립트가 UTF-8 출력을 강제하지만, 그래도 깨지면 `chcp 65001` 후 다시 실행. PowerShell 7 이상을 권장. |
| `Python 3.8 이상이 필요하다` | 구버전이다. macOS 는 `brew install python3`, Windows 는 위 링크. |
| `DT 인증 실패(401)` | `DTRACK_API_KEY` 가 틀렸다. 관리자에게 재발급 요청. |
| `DT 권한 부족(403)` | 키에 조회 권한이 없다. 1단계의 권한 3종 확인. |
| `SonarQube 인증 실패(401)` | 토큰이 틀렸거나 만료됐다. 2단계로 재발급. |
| `hotspot 조회 권한이 없다` | CI 자동화 토큰을 쓰고 있다. 개인 계정 토큰으로 바꿀 것. |
| `~에 해당하는 프로젝트를 못 찾았다` | `./sec.py projects` 로 실제 이름 확인. |

---

## 보안

- **`.env` 는 커밋하지 않는다.** 이 폴더의 `.gitignore` 가 막고 있다.
- SonarQube 토큰은 **개인 것이다.** 공유하지 않는다.
- DT 팀 키는 조회 전용이어야 한다. 쓰기 권한이 있는 키를 돌려쓰지 않는다.
