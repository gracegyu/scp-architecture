# PoC #5: 클리닉 배포 및 설치 검증

## Project Name

로컬 캐시 서버 클리닉 배포 및 설치 프로세스 검증

## Date

2025-10-21 (예정)

## Submitter Info

Raymond

## Project Description

PoC1,2,3에서 선정된 기술 스택의 배포 및 설치 프로세스를 검증한다. **기술 검증 목적**: Windows 환경에서의 설치 호환성, 의료 데이터 규정 준수, 배포 자동화 등을 검증하여 향후 프로덕션 배포 시 기술적 의사결정 근거를 확보한다.

## Business and Marketing Justification

**PoC 검증 가치:**

- Windows 환경 배포 호환성 검증
- 의료 데이터 규정 준수 방안 검증
- 배포 자동화 기술 검증
- 향후 프로덕션 배포 시 기술적 의사결정 근거 확보

**핵심 요구사항:**

- 설치 시간: 10분 이내 (IT 담당자 기준)
- 호환성: Windows Server 2019+ (PoC1,2,3에서 선정된 기술 스택)
- 자동화: 원클릭 설치, 자동 업데이트, 모니터링
- 보안: 의료 데이터 규정 준수 (HIPAA, 개인정보보호법)
- 운영: 사용자 교육, 문제 해결, 원격 지원

※ 자동 업데이트 정책: 백그라운드 업데이트, 무중단 업데이트, 롤백 전략 — 필수

**성공 기준:**

- 설치 성공률: 95% 이상
- 설치 시간: 평균 5분 이내
- 운영 도구 완성도: 100% (모니터링, 진단, 업데이트)
- 의료 규정 준수: 100%
- 사용자 교육 완료: 100%

## Risk Assessment

**배포 리스크:**

- 클리닉 네트워크 환경의 다양성 (방화벽, 프록시, 보안 정책)
- 하드웨어 사양 부족 (CPU, 메모리, 디스크)
- 네트워크 대역폭 제약
- IT 담당자 역량 부족

**법적 리스크:**

- 의료 데이터 규정 미준수 (HIPAA, 개인정보보호법)
- 의료기기 인증 요구사항
- 클리닉별 보안 정책 미준수

**운영 리스크:**

- 클리닉 IT 역량 부족
- 원격 지원 어려움
- 업데이트 실패
- 장애 대응 지연
- 사용자 교육 부족

**완화 전략:**

- 사전 호환성 테스트 (다양한 클리닉 환경)
- 자동 진단 도구 및 사용자 매뉴얼 제공
- 원격 모니터링 및 지원 시스템
- IT 담당자 교육 프로그램 운영

## Resource and Scheduling Details

**기간:** 2주 (Week 1-2, 다른 PoC와 병렬)

**인력:**

- 개발자 1명 (Raymond) - 배포 자동화, 설치 스크립트 개발, 라이선스 검토 및 호환성 테스트

**체크리스트(작업 순서):**

- [ ] PoC1/2/3 결과 분석 및 배포 요구사항 정리(컴포넌트/포트/권한/의존성 목록화)
- [ ] Windows 설치 프로그램(NSIS) 개발(서비스 등록/방화벽/설정파일/포터블 대안 포함)
- [ ] 운영 도구 개발(모니터링/진단/자동 업데이트: 백그라운드·무중단·롤백)
- [ ] 규정 준수 검증 및 문서화(HIPAA/개인정보보호법 체크리스트, 근거 기록)
- [ ] 실제 클리닉 환경 테스트 및 사용자 교육(설치 가이드/운영 매뉴얼/피드백 수렴)

**리소스:**

- 테스트 서버 3대 (Windows Server 2019/2022, Windows 10/11)
- 실제 클리닉 환경 2곳 (베타 테스트)
- 의료 규정 전문가 자문

## Technical Description

### 1. PoC1,2,3 결과 기반 배포 아키텍처

**선정된 기술 스택 (PoC1,2,3 결과):**

- HTTP 서버: Rust 내장 HTTP 서버 (Axum/Actix-web, PoC4에서 구현)
- 데이터 저장소: 파일시스템 + MongoDB (PoC2에서 선정, PoC4에서 MongoDB로 변경)
- 캐시 알고리즘: LRU (PoC3에서 선정)
- 개발 언어: Rust (PoC1,2,3,4 결정 반영)

**배포 아키텍처:**

```
┌─────────────────────────────────────────┐
│           Windows 클리닉 서버            │
├─────────────────────────────────────────┤
│  NSIS Installer / Portable Version     │
├─────────────────────────────────────────┤
│  Rust Cache Service (단일 바이너리) + MongoDB │
├─────────────────────────────────────────┤
│  모니터링 + 진단 + 업데이트 도구         │
└─────────────────────────────────────────┘
```

**개발 환경:**

- **개발 OS**: macOS (Windows 크로스 컴파일)
- **빌드**: Rust cargo (단일 .exe 바이너리)
- **배포 OS**: Windows 10/11, Windows Server 2019+

### 1.3 CacheBox(하드웨어) 옵션

**개요:** SW 단독 제공 외에 하드웨어 어플라이언스(CacheBox) 형태로 제공을 검토하며, Linux 기반 + Docker Compose로 구성한다.

**구성:**

```
┌──────────────────────────────┐
│ CacheBox (HW)                │
├──────────────────────────────┤
│ Docker Compose               │
│ - cache-service (Rust)       │
│ - mongodb (옵션/외부연결)     │
│ - monitoring (Prom/Graf)     │
└──────────────────────────────┘
```

**운영:** 원격 모니터링, OTA 업데이트(이미지 교체 + 롤백), 일괄 프로비저닝(초기 설정 스크립트)

### 2. Windows 설치 프로그램 설계

#### 2.1 설치 프로그램 구조 (NSIS 우선)

```
scp-cache-installer-1.0.0.exe
├── 설치 마법사 (GUI)
├── 자동 환경 검사
├── 서비스 등록
├── 방화벽 설정
└── 제거 프로그램
```

#### 2.2 포터블 버전 구조

```
scp-cache-portable-1.0.0.zip
├── scp-cache-server.exe       # Rust 단일 바이너리
├── cache-manager.exe          # 관리 도구 (선택)
├── config/
│   └── cache-config.toml      # 설정 파일
├── mongodb/                   # MongoDB (포함 또는 별도 설치)
└── run.bat                    # 포터블 실행 스크립트
```

### 3. 운영 도구 개발

#### 3.1 모니터링 시스템

**주요 기능:**

- 실시간 성능 모니터링 (CPU, 메모리, 디스크, 네트워크)
- 캐시 히트율 및 통계 수집
- 알림 시스템 (장애, 성능 임계값 초과)
- 원격 모니터링 데이터 전송
- 대시보드 웹 인터페이스

#### 3.2 자동 진단 도구

**주요 기능:**

- 시스템 상태 자동 진단 (서비스, 포트, 디스크, 네트워크)
- 문제 원인 자동 분석 및 해결 방안 제시
- 로그 분석 및 오류 패턴 감지
- 성능 최적화 권장사항 제공
- 원격 지원을 위한 진단 리포트 생성

**패키지 구조:**

```
scp-cache-server-1.0.0/
├── bin/
│   ├── scp-cache-server.exe  # Rust 단일 바이너리
│   ├── cache-manager.exe     # 관리 도구 (선택)
│   └── install.bat           # Windows 설치 스크립트
├── config/
│   ├── cache-config.toml     # 설정 파일
│   └── mongodb/              # MongoDB (포함 또는 별도 설치)
├── scripts/
│   ├── start.bat             # 서비스 시작
│   ├── stop.bat              # 서비스 중지
│   └── update.bat            # 업데이트 스크립트
└── docs/
    ├── README.md
    ├── LICENSE
    └── CHANGELOG.md
```

### 3. 설치 프로세스 설계

#### 3.1 설치 프로그램 (Installer) - 권장 방식

**Windows 설치 프로그램 (NSIS/Inno Setup):**

```
scp-cache-installer-1.0.0.exe
├── 설치 마법사 (GUI)
├── 자동 환경 검사
├── 서비스 등록
├── 방화벽 설정
└── 제거 프로그램
```

**Windows 전용 배포:**

```
scp-cache-installer-1.0.0.exe    # Windows Installer (NSIS)
scp-cache-portable-1.0.0.zip     # 포터블 버전 (압축 해제 후 실행)
```

**설치 프로그램 장점:**

- 원클릭 설치 (GUI 기반)
- 자동 환경 설정
- 사용자 친화적 인터페이스
- 설치/제거 완전 자동화
- 시스템 통합 (시작 메뉴, 서비스 등록)
- 방화벽 자동 설정
- 서비스 자동 등록/시작

#### 3.2 원클릭 설치 스크립트 (대안)

```bash
#!/bin/bash
# install.sh - 원클릭 설치 스크립트

set -e

echo "SCP 로컬 캐시 서버 설치를 시작합니다..."

# 1. 시스템 요구사항 확인
check_requirements() {
    echo "시스템 요구사항을 확인합니다..."

    # OS 확인
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        echo "지원하지 않는 OS입니다: $OSTYPE"
        exit 1
    fi

    # CPU 코어 확인
    CPU_CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "unknown")
    if [[ "$CPU_CORES" -lt 4 ]]; then
        echo "경고: CPU 코어가 4개 미만입니다. 성능이 제한될 수 있습니다."
    fi

    # 메모리 확인
    MEMORY_GB=$(free -g 2>/dev/null | awk '/^Mem:/{print $2}' || echo "unknown")
    if [[ "$MEMORY_GB" -lt 8 ]]; then
        echo "경고: 메모리가 8GB 미만입니다. 성능이 제한될 수 있습니다."
    fi

    # 디스크 공간 확인
    DISK_GB=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [[ "$DISK_GB" -lt 1000 ]]; then
        echo "경고: 디스크 공간이 1TB 미만입니다. 캐시 용량이 제한됩니다."
    fi
}

# 2. 네트워크 연결 테스트
test_network() {
    echo "클라우드 연결을 테스트합니다..."

    CLOUD_ENDPOINT="https://api.scp-cloud.com"
    if ! curl -s --connect-timeout 10 "$CLOUD_ENDPOINT/health" > /dev/null; then
        echo "경고: 클라우드 연결에 실패했습니다. 방화벽 설정을 확인하세요."
        read -p "계속 진행하시겠습니까? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 3. 설치 디렉터리 생성
setup_directories() {
    echo "설치 디렉터리를 생성합니다..."

    INSTALL_DIR="/opt/scp-cache"
    CACHE_DIR="/var/cache/scp"
    LOG_DIR="/var/log/scp"

    sudo mkdir -p "$INSTALL_DIR" "$CACHE_DIR" "$LOG_DIR"
    sudo chown -R $USER:$USER "$INSTALL_DIR" "$CACHE_DIR" "$LOG_DIR"
}

# 4. 바이너리 설치
install_binaries() {
    echo "바이너리를 설치합니다..."

    # 바이너리 복사
    sudo cp bin/* "$INSTALL_DIR/"
    sudo chmod +x "$INSTALL_DIR"/*

    # 설정 파일 복사
    sudo cp -r config/* "$INSTALL_DIR/"
}

# 5. 서비스 등록
install_service() {
    echo "시스템 서비스를 등록합니다..."

    if [[ "$OS" == "linux" ]]; then
        # systemd 서비스 등록
        sudo cp config/systemd/scp-cache.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable scp-cache
    elif [[ "$OS" == "windows" ]]; then
        # Windows 서비스 등록 (NSSM 사용)
        nssm install scp-cache "$INSTALL_DIR/cache-daemon.exe"
        nssm set scp-cache Start SERVICE_AUTO_START
    fi
}

# 6. 초기 설정
initial_config() {
    echo "초기 설정을 진행합니다..."

    read -p "클리닉 ID를 입력하세요: " CLINIC_ID
    read -p "클라우드 API 엔드포인트를 입력하세요 (기본값: https://api.scp-cloud.com): " API_ENDPOINT
    API_ENDPOINT=${API_ENDPOINT:-https://api.scp-cloud.com}

    # 설정 파일 업데이트
    sed -i "s/CLINIC_ID_PLACEHOLDER/$CLINIC_ID/g" "$INSTALL_DIR/cache-config.yaml"
    sed -i "s|API_ENDPOINT_PLACEHOLDER|$API_ENDPOINT|g" "$INSTALL_DIR/cache-config.yaml"
}

# 7. 서비스 시작
start_service() {
    echo "서비스를 시작합니다..."

    if [[ "$OS" == "linux" ]]; then
        sudo systemctl start scp-cache
        sudo systemctl status scp-cache
    elif [[ "$OS" == "windows" ]]; then
        nssm start scp-cache
    fi

    # 헬스체크
    sleep 5
    if curl -s http://localhost:8080/health > /dev/null; then
        echo "✅ 설치가 완료되었습니다!"
        echo "관리 대시보드: http://localhost:8080"
    else
        echo "❌ 서비스 시작에 실패했습니다. 로그를 확인하세요: $LOG_DIR"
        exit 1
    fi
}

# 메인 실행
main() {
    check_requirements
    test_network
    setup_directories
    install_binaries
    install_service
    initial_config
    start_service
}

main "$@"
```

#### 3.3 설치 프로그램 구현 예시

**Windows Installer (NSIS):**

```nsis
; SCP Cache Server Installer Script
!define APP_NAME "SCP Cache Server"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "Ewoosoft"

Name "${APP_NAME}"
OutFile "scp-cache-installer-${APP_VERSION}.exe"
InstallDir "C:\Program Files\SCP\CacheServer"

Section "Install"
    ; 1. MongoDB 설치 확인 (선택적)
    ; MongoDB가 설치되어 있지 않으면 경고 표시

    ; 2. 파일 복사
    SetOutPath "$INSTDIR"
    File "bin\scp-cache-server.exe"
    File "bin\cache-manager.exe"
    File "config\cache-config.toml"

    ; 3. 디렉터리 생성
    CreateDirectory "$INSTDIR\logs"
    CreateDirectory "$INSTDIR\cache"
    CreateDirectory "C:\ProgramData\SCP\Cache\media"
    CreateDirectory "C:\ProgramData\SCP\Cache\spool"

    ; 4. 서비스 등록 (windows-service 크레이트 사용 시)
    ; 또는 직접 sc 명령어 사용
    ExecWait 'sc create "SCPCacheServer" binPath= "$INSTDIR\scp-cache-server.exe" start= auto DisplayName= "SCP Cache Server"'

    ; 5. 방화벽 규칙 추가
    ExecWait 'netsh advfirewall firewall add rule name="SCP Cache" dir=in action=allow protocol=TCP localport=80'
    ExecWait 'netsh advfirewall firewall add rule name="SCP Cache Admin" dir=in action=allow protocol=TCP localport=8080'

    ; 6. 시작 메뉴 등록
    CreateShortCut "$SMPROGRAMS\SCP Cache Server.lnk" "$INSTDIR\cache-manager.exe"

    ; 7. 서비스 시작
    ExecWait 'net start "SCPCacheServer"'

    MessageBox MB_OK "설치가 완료되었습니다!"
SectionEnd

Section "Uninstall"
    ; 1. 서비스 중지 및 제거
    ExecWait 'net stop "SCPCacheServer"'
    ExecWait 'sc delete "SCPCacheServer"'

    ; 2. 방화벽 규칙 제거
    ExecWait 'netsh advfirewall firewall delete rule name="SCP Cache"'
    ExecWait 'netsh advfirewall firewall delete rule name="SCP Cache Admin"'

    ; 3. 파일 삭제 (캐시 데이터는 보존 옵션)
    RMDir /r "$INSTDIR"

    ; 4. 시작 메뉴 제거
    Delete "$SMPROGRAMS\SCP Cache Server.lnk"
SectionEnd
```

**Windows 포터블 버전:**

```batch
@echo off
REM 포터블 버전 실행 스크립트

echo SCP Cache Server 포터블 버전을 시작합니다...

REM 현재 디렉터리 설정
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM MongoDB 확인 (선택적)
where mongod >nul 2>&1
if %errorlevel% neq 0 (
    echo 경고: MongoDB가 설치되어 있지 않습니다.
    echo MongoDB를 설치하거나 MongoDB 서버가 실행 중인지 확인하세요.
)

REM 서비스 모드 확인
if "%1"=="--install" (
    echo 시스템 서비스로 설치합니다...
    sc create "SCPCacheServer" binPath= "%SCRIPT_DIR%scp-cache-server.exe" start= auto DisplayName= "SCP Cache Server"
    netsh advfirewall firewall add rule name="SCP Cache" dir=in action=allow protocol=TCP localport=80
    netsh advfirewall firewall add rule name="SCP Cache Admin" dir=in action=allow protocol=TCP localport=8080
    net start "SCPCacheServer"
    echo 설치 완료!
) else (
    echo 포터블 모드로 실행합니다...
    start "" "%SCRIPT_DIR%scp-cache-server.exe"
)
```

#### 3.3 자동 업데이트 시스템

**주요 기능:**

- 백그라운드 업데이트 확인 (매일)
- 안전한 업데이트 다운로드 및 검증
- 무중단 업데이트 (롤링 업데이트)
- 업데이트 실패 시 자동 롤백
- 업데이트 로그 및 알림

**Rust 구현 예시:**

```rust
// update.rs - 자동 업데이트 로직
use serde::{Deserialize, Serialize};
use tokio::time::{interval, Duration};
use std::path::PathBuf;

#[derive(Debug, Deserialize)]
struct UpdateInfo {
    version: String,
    download_url: String,
    checksum: String,
    required: bool,
}

async fn check_for_updates() -> Result<UpdateInfo, Box<dyn std::error::Error>> {
    let client = reqwest::Client::new();
    let resp = client
        .get("https://api.scp-cloud.com/updates/latest")
        .send()
        .await?;

    let update: UpdateInfo = resp.json().await?;
    Ok(update)
}

async fn download_update(url: &str) -> Result<PathBuf, Box<dyn std::error::Error>> {
    let client = reqwest::Client::new();
    let resp = client.get(url).send().await?;
    let mut file = tokio::fs::File::create("cache-server-new.exe").await?;
    let mut content = resp.bytes().await?;
    tokio::io::copy(&mut content.as_ref(), &mut file).await?;
    Ok(PathBuf::from("cache-server-new.exe"))
}

async fn apply_update() -> Result<(), Box<dyn std::error::Error>> {
    // 1. 새 바이너리 다운로드
    // 2. 체크섬 검증
    // 3. 기존 바이너리 백업
    // 4. 새 바이너리로 교체
    // 5. Windows Service 재시작

    tokio::process::Command::new("net")
        .args(&["stop", "SCPCacheServer"])
        .status()
        .await?;

    // 바이너리 교체 로직...

    tokio::process::Command::new("net")
        .args(&["start", "SCPCacheServer"])
        .status()
        .await?;

    Ok(())
}

async fn update_worker() {
    let mut interval = interval(Duration::from_secs(24 * 60 * 60)); // 매일 체크

    loop {
        interval.tick().await;

        match check_for_updates().await {
            Ok(update) if update.required => {
                log::info!("필수 업데이트 발견: {}", update.version);
                if let Err(e) = download_update(&update.download_url).await {
                    log::error!("업데이트 다운로드 실패: {}", e);
                    continue;
                }

                if let Err(e) = apply_update().await {
                    log::error!("업데이트 적용 실패: {}", e);
                } else {
                    log::info!("업데이트 완료: {}", update.version);
                }
            }
            Ok(_) => {
                // 선택적 업데이트 처리
            }
            Err(e) => {
                log::error!("업데이트 확인 실패: {}", e);
            }
        }
    }
}
```

**참고:**

- Rust의 `tokio`, `reqwest`, `serde` 크레이트 사용
- Windows Service는 `windows-service` 크레이트 또는 `net` 명령어 사용
- 체크섬 검증은 `sha2` 크레이트 활용

### 4. 의료 규정 준수 검증

#### 4.1 HIPAA 준수 체크리스트

**기술적 보호조치:**

- [ ] 전송 암호화 (TLS 1.3)
- [ ] 저장 암호화 (AES-256)
- [ ] 접근 제어 (인증/인가)
- [ ] 감사 로그 (모든 접근 기록)
- [ ] 데이터 무결성 (체크섬 검증)

**관리적 보호조치:**

- [ ] 개인정보보호정책 수립
- [ ] 직원 교육 및 훈련
- [ ] 접근 권한 관리
- [ ] 보안 사고 대응 절차

#### 4.2 개인정보보호법 준수

**개인정보 처리 현황:**

- 수집: 환자 ID, 클리닉 ID (최소한)
- 저장: 로컬 캐시 (암호화)
- 이용: 캐시 키 생성, 무효화
- 제공: 없음
- 파기: TTL 만료 시 자동 삭제

**개인정보보호 영향평가:**

- 영향도: 중간 (의료 데이터 캐싱)
- 위험도: 낮음 (로컬 저장, 암호화)
- 대응방안: 기술적/관리적 보호조치

### 5. 사용자 교육 및 지원

#### 5.1 IT 담당자 교육 프로그램

**교육 내용:**

- 설치 및 설정 방법
- 일상 운영 및 모니터링
- 문제 해결 및 진단 도구 사용
- 보안 정책 및 의료 규정 준수
- 업데이트 및 유지보수

**교육 방식:**

- 온라인 교육 영상 (30분)
- 실습 가이드 문서
- Q&A 세션 (1시간)
- 원격 지원 연락처

#### 5.2 사용자 매뉴얼 및 가이드

**제공 자료:**

- 설치 가이드 (단계별 스크린샷 포함)
- 운영 매뉴얼 (일상 관리, 모니터링)
- 문제 해결 가이드 (FAQ, 트러블슈팅)
- 보안 정책 가이드 (의료 규정 준수)
- 업데이트 가이드 (자동/수동 업데이트)

### 6. 실제 클리닉 환경 테스트

#### 6.1 베타 테스트 클리닉 선정

**테스트 환경:**

- 대형 클리닉 (환자 1000명/일, 서버 2대)
- 중형 클리닉 (환자 500명/일, 서버 1대)
- 소형 클리닉 (환자 200명/일, 서버 1대)

**테스트 시나리오:**

- 정상 운영 환경에서 1주일 연속 테스트
- 피크 시간대 부하 테스트
- 네트워크 장애 상황 테스트
- 업데이트 프로세스 테스트

#### 6.2 사용자 피드백 수집

**피드백 항목:**

- 설치 과정의 어려움
- 운영 중 발견된 문제점
- 성능 및 안정성 평가
- 사용자 인터페이스 개선사항
- 교육 자료의 완성도

### 7. 호환성 테스트

#### 7.1 지원 OS 및 버전

| OS             | 버전   | 아키텍처 | 상태 | 비고          |
| -------------- | ------ | -------- | ---- | ------------- |
| Windows Server | 2019   | x64      | ✅   | 권장          |
| Windows Server | 2022   | x64      | ✅   | 지원          |
| Windows 10     | 1909+  | x64      | ✅   | 지원          |
| Windows 11     | 21H2+  | x64      | ✅   | 지원          |
| Ubuntu Server  | 20.04+ | x64      | ✅   | CacheBox 권장 |
| Ubuntu Server  | 22.04+ | x64      | ✅   | 지원          |
| Debian         | 12+    | x64      | ✅   | 지원          |
| RHEL           | 9+     | x64      | ✅   | 지원          |

#### 7.2 하드웨어 요구사항

**최소 사양:**

- CPU: 2코어 (Intel/AMD x64)
- 메모리: 4GB RAM
- 디스크: 500GB SSD
- 네트워크: 100Mbps

**권장 사양:**

- CPU: 4코어 이상
- 메모리: 8GB RAM 이상
- 디스크: 1TB SSD
- 네트워크: 1Gbps

#### 7.3 네트워크 환경 테스트

**방화벽 설정:**

- 아웃바운드: HTTPS (443), HTTP (80)
- 인바운드: HTTP (80), 관리 포트 (8080)

**프록시 환경:**

- HTTP 프록시 지원
- 인증 프록시 지원
- SSL 인증서 검증

### 8. 모니터링 및 지원

#### 8.1 원격 모니터링

**Rust 구현 예시:**

```rust
// monitoring.rs - 원격 모니터링 설정
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Deserialize, Serialize)]
struct MonitoringConfig {
    enabled: bool,
    endpoint: String,
    api_key: String,
    interval: u64, // seconds
    metrics: Vec<String>,
    clinic_id: String,
}

async fn send_metrics(config: &MonitoringConfig) -> Result<(), Box<dyn std::error::Error>> {
    let metrics = collect_metrics().await?;

    let payload = json!({
        "clinic_id": config.clinic_id,
        "timestamp": SystemTime::now()
            .duration_since(UNIX_EPOCH)?
            .as_secs(),
        "metrics": metrics,
    });

    let client = reqwest::Client::new();
    let resp = client
        .post(&config.endpoint)
        .header("Authorization", format!("Bearer {}", config.api_key))
        .header("Content-Type", "application/json")
        .json(&payload)
        .timeout(Duration::from_secs(10))
        .send()
        .await?;

    if !resp.status().is_success() {
        log::error!("메트릭 전송 실패: {}", resp.status());
    }

    Ok(())
}
```

**참고:**

- Rust의 `tokio`, `reqwest`, `serde_json` 크레이트 사용
- 비동기 처리는 `tokio` 런타임 활용

#### 8.2 자동 진단 도구

**Windows PowerShell 버전:**

```powershell
# diagnose.ps1 - 자동 진단 도구 (Windows)

Write-Host "SCP 로컬 캐시 서버 진단을 시작합니다..." -ForegroundColor Cyan

# 1. 서비스 상태 확인
function Check-Service {
    $service = Get-Service -Name "SCPCacheServer" -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq "Running") {
        Write-Host "✅ 서비스 실행 중" -ForegroundColor Green
    } else {
        Write-Host "❌ 서비스 중지됨" -ForegroundColor Red
        Get-Service -Name "SCPCacheServer" -ErrorAction SilentlyContinue
    }
}

# 2. 포트 확인
function Check-Ports {
    $port80 = Get-NetTCPConnection -LocalPort 80 -ErrorAction SilentlyContinue
    if ($port80) {
        Write-Host "✅ HTTP 포트 (80) 열림" -ForegroundColor Green
    } else {
        Write-Host "❌ HTTP 포트 (80) 닫힘" -ForegroundColor Red
    }

    $port8080 = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
    if ($port8080) {
        Write-Host "✅ 관리 포트 (8080) 열림" -ForegroundColor Green
    } else {
        Write-Host "❌ 관리 포트 (8080) 닫힘" -ForegroundColor Red
    }
}

# 3. 디스크 공간 확인
function Check-Disk {
    $drive = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -eq "C:\" }
    $usage = [math]::Round(($drive.Used / $drive.Free) * 100, 2)
    if ($usage -gt 90) {
        Write-Host "⚠️ 디스크 사용률 높음: ${usage}%" -ForegroundColor Yellow
    } else {
        Write-Host "✅ 디스크 사용률 정상: ${usage}%" -ForegroundColor Green
    }
}

# 4. 네트워크 연결 확인
function Check-Network {
    try {
        $response = Invoke-WebRequest -Uri "https://api.scp-cloud.com/health" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✅ 클라우드 연결 정상" -ForegroundColor Green
    } catch {
        Write-Host "❌ 클라우드 연결 실패" -ForegroundColor Red
    }
}

# 5. MongoDB 연결 확인
function Check-MongoDB {
    try {
        $mongoProcess = Get-Process -Name "mongod" -ErrorAction SilentlyContinue
        if ($mongoProcess) {
            Write-Host "✅ MongoDB 실행 중" -ForegroundColor Green
        } else {
            Write-Host "⚠️ MongoDB 프로세스 없음 (원격 서버 연결 가능)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ MongoDB 확인 실패" -ForegroundColor Red
    }
}

# 6. 로그 확인
function Check-Logs {
    $logPath = "C:\ProgramData\SCP\Cache\logs\error.log"
    if (Test-Path $logPath) {
        $errorCount = (Select-String -Path $logPath -Pattern "ERROR" | Select-Object -Last 100).Count
        if ($errorCount -gt 10) {
            Write-Host "⚠️ 에러 로그 많음: ${errorCount}개" -ForegroundColor Yellow
        } else {
            Write-Host "✅ 에러 로그 정상" -ForegroundColor Green
        }
    }
}

# 진단 실행
Check-Service
Check-Ports
Check-Disk
Check-Network
Check-MongoDB
Check-Logs

Write-Host "`n진단 완료. 문제가 발견되면 지원팀에 문의하세요." -ForegroundColor Cyan
```

**Rust 구현 버전 (권장):**

자동 진단 도구도 Rust로 구현하여 단일 바이너리로 배포 가능합니다.

### 9. 검증 기준

#### 9.1 설치 테스트

**기능 테스트:**

- [ ] 원클릭 설치 성공 (5분 이내)
- [ ] 서비스 자동 시작
- [ ] 헬스체크 통과
- [ ] 관리 대시보드 접근 가능

**호환성 테스트:**

- [ ] Windows Server 2019 설치 성공
- [ ] Windows Server 2022 설치 성공
- [ ] Windows 10/11 설치 성공
- [ ] 최소 사양에서 동작
- [ ] 프록시 환경에서 동작

#### 9.2 라이선스 테스트

**준수 확인:**

- [ ] 모든 라이선스 파일 포함
- [ ] 저작권 고지 정확
- [ ] 소스코드 제공 방법 명시
- [ ] 법무팀 검토 완료

#### 9.3 보안 테스트

**암호화 확인:**

- [ ] TLS 1.3 연결
- [ ] 디스크 암호화 활성화
- [ ] 민감 정보 마스킹

**접근 제어:**

- [ ] 인증 없이 접근 불가
- [ ] 권한별 접근 제한
- [ ] 감사 로그 기록

### 10. 예상 결과 및 의사결정 기준

**예상 결과:**

- PoC1,2,3에서 선정된 기술 스택 기반 배포 아키텍처 완성
- Windows 설치 프로그램 및 운영 도구 개발 완료
- 의료 규정 준수 검증 완료 (HIPAA, 개인정보보호법)
- 실제 클리닉 환경에서 검증 완료

**의사결정:**

- 배포 방식: Windows Installer(NSIS 우선) + 포터블 + CacheBox(Docker)
- 운영 도구: 모니터링 + 진단 + 업데이트 시스템 (Rust 기반)
- 교육 프로그램: IT 담당자 대상 체계적 교육
- 지원 체계: 원격 모니터링 + 자동 진단 + 사용자 매뉴얼

### 11. 다음 단계

PoC #4 통합 프로토타입 완료 후 클리닉 배포 검증 진행

**참고:**

- PoC4에서 Rust 단일 바이너리로 구현된 통합 프로토타입 기반
- MongoDB 설치/설정 자동화 포함
- Windows Service 등록 및 관리 도구 포함
