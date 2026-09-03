#!/bin/bash
# 새벽(KST 03:00·cron) 통합 자동 갱신: trivy·gitleaks 바이너리 + trivy 취약점 DB.
#
#  - 바이너리·DB를 공유 볼륨 /opt/trivy-cache 에 둔다. 에이전트는 이 볼륨을 :ro 마운트하고
#    CI 스캔은 /opt/trivy-cache/bin/{trivy,gitleaks} 를 호출 → 이미지 재빌드/에이전트 재설치 없이
#    매일 새벽 최신 버전을 자동으로 쓴다.
#  - 바이너리는 GitHub latest 확인 후 smoke-test 통과 시에만 원자적 교체(나쁜 릴리스 차단·실패 시 옛 버전 유지).
#  - trivy 바이너리 smoke 는 **기존 로컬 DB로(네트워크 0)** 검증한다 — smoke 자체가 gcr.io flaky 에 걸리지 않게.
#  - DB 다운로드는 **재시도(5회)** — self-hosted→gcr.io 가 flaky(connection reset)해서. 새벽이라 재시도해도 CI 무영향.
#  - gitleaks 는 DB 없음(정적 바이너리)·완전 오프라인.
#  - 긴급 고정: 환경변수 TRIVY_PIN / GITLEAKS_PIN 설정 시 그 버전으로 고정(latest 무시).
#
# 관리 정본: scp .../VT_API_Gateway/references/Self-hosted1/ci-scanners-update.sh
# 배치/cron: 호스트 /home/raymond/azp-agent-in-docker/ci-scanners-update.sh · `0 18 * * *`(KST 03:00)
# 로그:      /opt/trivy-cache/update.log

set -uo pipefail
CACHE_DIR="${CACHE_DIR:-/opt/trivy-cache}"
BIN_DIR="${CACHE_DIR}/bin"
LOG="${CACHE_DIR}/update.log"
mkdir -p "$BIN_DIR"
log(){ echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }
latest(){ curl -fsSL "https://api.github.com/repos/$1/releases/latest" 2>/dev/null | grep -m1 '"tag_name"' | sed -E 's/.*"v?([0-9.]+)".*/\1/'; }

log "=== ci-scanners update start ==="

# ---------- trivy 바이너리: 기존 DB로 smoke(네트워크 0) 후 교체 ----------
CUR_T="$("$BIN_DIR/trivy" --version 2>/dev/null | awk '/^Version:/{print $2}')"
WANT_T="${TRIVY_PIN:-$(latest aquasecurity/trivy)}"
if [ -z "$WANT_T" ]; then log "trivy 최신버전 조회 실패 — 바이너리 유지"
elif [ "$WANT_T" = "$CUR_T" ]; then log "trivy 최신($CUR_T)"
else
  log "trivy $CUR_T -> $WANT_T 시도"
  TMP="$(mktemp -d -p "$CACHE_DIR")"
  OK=""
  if curl -sfL "https://github.com/aquasecurity/trivy/releases/download/v${WANT_T}/trivy_${WANT_T}_Linux-64bit.tar.gz" | tar -xz -C "$TMP" trivy 2>>"$LOG" \
     && "$TMP/trivy" --version >/dev/null 2>&1; then
    if [ -f "${CACHE_DIR}/db/trivy.db" ]; then
      "$TMP/trivy" fs --skip-db-update --cache-dir "$CACHE_DIR" --scanners vuln --quiet /etc >/dev/null 2>>"$LOG" && OK=1
    else
      OK=1   # 아직 DB 없음 — 버전만 확인·통과(DB는 아래서 받음)
    fi
  fi
  if [ -n "$OK" ]; then mv -f "$TMP/trivy" "$BIN_DIR/trivy"; log "trivy 교체 OK -> $WANT_T"; else log "trivy 업그레이드 smoke 실패 — 옛 버전 유지($CUR_T)"; fi
  rm -rf "$TMP"
fi

# ---------- trivy DB 일일 갱신(활성 바이너리·gcr.io 재시도 5회) ----------
if [ -x "$BIN_DIR/trivy" ]; then
  DBOK=""
  for i in 1 2 3 4 5; do
    if "$BIN_DIR/trivy" image --download-db-only --cache-dir "$CACHE_DIR" >>"$LOG" 2>&1; then DBOK=1; break; fi
    log "DB 다운로드 실패(시도 $i/5·gcr.io flaky) — 20s 후 재시도"; sleep 20
  done
  [ -n "$DBOK" ] && log "DB OK" || log "DB FAIL(5회 실패)·마지막 성공본 유지"
else
  log "trivy 바이너리 없음 — DB 갱신 생략"
fi

# ---------- gitleaks: 바이너리만(DB 없음·오프라인) ----------
CUR_G="$("$BIN_DIR/gitleaks" version 2>/dev/null)"
WANT_G="${GITLEAKS_PIN:-$(latest gitleaks/gitleaks)}"
if [ -z "$WANT_G" ]; then log "gitleaks 최신버전 조회 실패 — 유지"
elif [ "$WANT_G" = "$CUR_G" ]; then log "gitleaks 최신($CUR_G)"
else
  log "gitleaks $CUR_G -> $WANT_G 시도"
  TMP="$(mktemp -d -p "$CACHE_DIR")"
  if curl -sfL "https://github.com/gitleaks/gitleaks/releases/download/v${WANT_G}/gitleaks_${WANT_G}_linux_x64.tar.gz" | tar -xz -C "$TMP" gitleaks 2>>"$LOG" \
     && "$TMP/gitleaks" version >/dev/null 2>&1; then
    mv -f "$TMP/gitleaks" "$BIN_DIR/gitleaks"; log "gitleaks 교체 OK -> $WANT_G"
  else log "gitleaks 업그레이드 실패 — 옛 버전 유지($CUR_G)"; fi
  rm -rf "$TMP"
fi

log "=== ci-scanners update done (trivy=$("$BIN_DIR/trivy" --version 2>/dev/null | awk '/^Version:/{print $2}') gitleaks=$("$BIN_DIR/gitleaks" version 2>/dev/null)) ==="
