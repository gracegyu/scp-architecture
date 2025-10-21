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

**일정:**

- Day 1-2: PoC1,2,3 결과 분석 및 배포 요구사항 정리
- Day 3-5: Windows 설치 프로그램 개발 (NSIS, 포터블)
- Day 6-8: 운영 도구 개발 (모니터링, 진단, 업데이트)
- Day 9-10: 의료 규정 준수 검증 및 문서화
- Day 11-12: 실제 클리닉 환경 테스트 및 사용자 교육

**리소스:**

- 테스트 서버 3대 (Windows Server 2019/2022, Windows 10/11)
- 실제 클리닉 환경 2곳 (베타 테스트)
- 의료 규정 전문가 자문

## Technical Description

### 1. PoC1,2,3 결과 기반 배포 아키텍처

**선정된 기술 스택 (PoC1,2,3 결과):**

- Reverse Proxy: Nginx/Envoy (PoC1에서 선정)
- 데이터 저장소: 파일시스템 + PostgreSQL/Redis (PoC2에서 선정)
- 캐시 알고리즘: W-TinyLFU + SLRU (PoC3에서 선정)
- 개발 언어: Go (PoC1,2,3에서 선정)

**배포 아키텍처:**

```
┌─────────────────────────────────────────┐
│           Windows 클리닉 서버            │
├─────────────────────────────────────────┤
│  NSIS Installer / Portable Version     │
├─────────────────────────────────────────┤
│  Go Cache Service + Nginx + PostgreSQL │
├─────────────────────────────────────────┤
│  모니터링 + 진단 + 업데이트 도구         │
└─────────────────────────────────────────┘
```

### 2. Windows 설치 프로그램 설계

#### 2.1 설치 프로그램 구조

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
├── cache-daemon.exe
├── cache-manager.exe
├── config/
│   ├── cache-config.yaml
│   └── nginx.conf
└── run.bat (포터블 실행 스크립트)
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
│   ├── cache-daemon          # Go 바이너리
│   ├── nginx                 # Nginx 바이너리
│   └── install.sh            # 설치 스크립트
├── config/
│   ├── nginx.conf
│   ├── cache-config.yaml
│   └── systemd/
│       └── scp-cache.service
├── scripts/
│   ├── start.sh
│   ├── stop.sh
│   └── update.sh
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
    ; 1. 파일 복사
    SetOutPath "$INSTDIR"
    File "bin\cache-daemon.exe"
    File "bin\cache-manager.exe"
    File "config\cache-config.yaml"

    ; 2. 서비스 등록
    ExecWait 'sc create "SCPCache" binPath= "$INSTDIR\cache-daemon.exe" start= auto'

    ; 3. 방화벽 규칙 추가
    ExecWait 'netsh advfirewall firewall add rule name="SCP Cache" dir=in action=allow protocol=TCP localport=80'
    ExecWait 'netsh advfirewall firewall add rule name="SCP Cache Admin" dir=in action=allow protocol=TCP localport=8080'

    ; 4. 시작 메뉴 등록
    CreateShortCut "$SMPROGRAMS\SCP Cache Server.lnk" "$INSTDIR\cache-manager.exe"

    ; 5. 서비스 시작
    ExecWait 'net start "SCPCache"'

    MessageBox MB_OK "설치가 완료되었습니다!"
SectionEnd

Section "Uninstall"
    ; 1. 서비스 중지 및 제거
    ExecWait 'net stop "SCPCache"'
    ExecWait 'sc delete "SCPCache"'

    ; 2. 방화벽 규칙 제거
    ExecWait 'netsh advfirewall firewall delete rule name="SCP Cache"'
    ExecWait 'netsh advfirewall firewall delete rule name="SCP Cache Admin"'

    ; 3. 파일 삭제
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

REM 서비스 모드 확인
if "%1"=="--install" (
    echo 시스템 서비스로 설치합니다...
    sc create "SCPCache" binPath= "%SCRIPT_DIR%cache-daemon.exe" start= auto
    netsh advfirewall firewall add rule name="SCP Cache" dir=in action=allow protocol=TCP localport=80
    netsh advfirewall firewall add rule name="SCP Cache Admin" dir=in action=allow protocol=TCP localport=8080
    net start "SCPCache"
    echo 설치 완료!
) else (
    echo 포터블 모드로 실행합니다...
    start "" "%SCRIPT_DIR%cache-manager.exe"
)
```

#### 3.3 자동 업데이트 시스템

**주요 기능:**

- 백그라운드 업데이트 확인 (매일)
- 안전한 업데이트 다운로드 및 검증
- 무중단 업데이트 (롤링 업데이트)
- 업데이트 실패 시 자동 롤백
- 업데이트 로그 및 알림

```go
// update.go - 자동 업데이트 로직
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "os"
    "os/exec"
    "time"
)

type UpdateInfo struct {
    Version     string `json:"version"`
    DownloadURL string `json:"download_url"`
    Checksum    string `json:"checksum"`
    Required    bool   `json:"required"`
}

func checkForUpdates() (*UpdateInfo, error) {
    resp, err := http.Get("https://api.scp-cloud.com/updates/latest")
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    var update UpdateInfo
    if err := json.NewDecoder(resp.Body).Decode(&update); err != nil {
        return nil, err
    }

    return &update, nil
}

func downloadUpdate(url string) error {
    resp, err := http.Get(url)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    file, err := os.Create("/tmp/cache-daemon-new")
    if err != nil {
        return err
    }
    defer file.Close()

    _, err = io.Copy(file, resp.Body)
    return err
}

func applyUpdate() error {
    // 1. 새 바이너리 다운로드
    // 2. 체크섬 검증
    // 3. 기존 바이너리 백업
    // 4. 새 바이너리로 교체
    // 5. 서비스 재시작

    cmd := exec.Command("systemctl", "restart", "scp-cache")
    return cmd.Run()
}

func updateWorker(ctx context.Context) {
    ticker := time.NewTicker(24 * time.Hour) // 매일 체크
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            update, err := checkForUpdates()
            if err != nil {
                log.Printf("업데이트 확인 실패: %v", err)
                continue
            }

            if update.Required {
                log.Printf("필수 업데이트 발견: %s", update.Version)
                if err := downloadUpdate(update.DownloadURL); err != nil {
                    log.Printf("업데이트 다운로드 실패: %v", err)
                    continue
                }

                if err := applyUpdate(); err != nil {
                    log.Printf("업데이트 적용 실패: %v", err)
                } else {
                    log.Printf("업데이트 완료: %s", update.Version)
                }
            }
        }
    }
}
```

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

| OS             | 버전  | 아키텍처 | 상태 | 비고 |
| -------------- | ----- | -------- | ---- | ---- |
| Windows Server | 2019  | x64      | ✅   | 권장 |
| Windows Server | 2022  | x64      | ✅   | 지원 |
| Windows 10     | 1909+ | x64      | ✅   | 지원 |
| Windows 11     | 21H2+ | x64      | ✅   | 지원 |

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

```go
// monitoring.go - 원격 모니터링 설정
type MonitoringConfig struct {
    Enabled     bool   `yaml:"enabled"`
    Endpoint    string `yaml:"endpoint"`
    APIKey      string `yaml:"api_key"`
    Interval    int    `yaml:"interval"` // seconds
    Metrics     []string `yaml:"metrics"`
}

func sendMetrics(config MonitoringConfig) {
    metrics := collectMetrics()

    payload := map[string]interface{}{
        "clinic_id": config.ClinicID,
        "timestamp": time.Now().Unix(),
        "metrics":   metrics,
    }

    jsonData, _ := json.Marshal(payload)

    req, _ := http.NewRequest("POST", config.Endpoint, bytes.NewBuffer(jsonData))
    req.Header.Set("Authorization", "Bearer "+config.APIKey)
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{Timeout: 10 * time.Second}
    resp, err := client.Do(req)
    if err != nil {
        log.Printf("메트릭 전송 실패: %v", err)
    }
    defer resp.Body.Close()
}
```

#### 8.2 자동 진단 도구

```bash
#!/bin/bash
# diagnose.sh - 자동 진단 도구

echo "SCP 로컬 캐시 서버 진단을 시작합니다..."

# 1. 서비스 상태 확인
check_service() {
    if systemctl is-active --quiet scp-cache; then
        echo "✅ 서비스 실행 중"
    else
        echo "❌ 서비스 중지됨"
        systemctl status scp-cache
    fi
}

# 2. 포트 확인
check_ports() {
    if netstat -tlnp | grep -q ":80 "; then
        echo "✅ HTTP 포트 (80) 열림"
    else
        echo "❌ HTTP 포트 (80) 닫힘"
    fi

    if netstat -tlnp | grep -q ":8080 "; then
        echo "✅ 관리 포트 (8080) 열림"
    else
        echo "❌ 관리 포트 (8080) 닫힘"
    fi
}

# 3. 디스크 공간 확인
check_disk() {
    USAGE=$(df -h /var/cache/scp | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$USAGE" -gt 90 ]; then
        echo "⚠️ 디스크 사용률 높음: ${USAGE}%"
    else
        echo "✅ 디스크 사용률 정상: ${USAGE}%"
    fi
}

# 4. 네트워크 연결 확인
check_network() {
    if curl -s --connect-timeout 5 https://api.scp-cloud.com/health > /dev/null; then
        echo "✅ 클라우드 연결 정상"
    else
        echo "❌ 클라우드 연결 실패"
    fi
}

# 5. 로그 확인
check_logs() {
    if [ -f /var/log/scp/error.log ]; then
        ERROR_COUNT=$(grep -c "ERROR" /var/log/scp/error.log | tail -100)
        if [ "$ERROR_COUNT" -gt 10 ]; then
            echo "⚠️ 에러 로그 많음: $ERROR_COUNT개"
        else
            echo "✅ 에러 로그 정상"
        fi
    fi
}

# 진단 실행
check_service
check_ports
check_disk
check_network
check_logs

echo "진단 완료. 문제가 발견되면 지원팀에 문의하세요."
```

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

- 배포 방식: Windows Installer + 포터블 (하이브리드)
- 운영 도구: 모니터링 + 진단 + 업데이트 시스템
- 교육 프로그램: IT 담당자 대상 체계적 교육
- 지원 체계: 원격 모니터링 + 자동 진단 + 사용자 매뉴얼

### 11. 다음 단계

선정된 기술 스택과 배포 방식을 PoC #4 통합 프로토타입에 적용
