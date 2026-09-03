#!/bin/bash
# trivy 취약점 DB를 self-hosted 공유 캐시에 하루 1회 갱신한다.
#   - gcr.io 접속은 오직 여기서만(=CI 밖). 실패해도 마지막 성공본이 남아 CI는 무영향.
#   - CI(에이전트)는 이 캐시를 `trivy fs --skip-db-update`로 오프라인 사용.
#
# 관리 정본: scp .../VT_API_Gateway/references/Self-hosted1/trivy-db-update.sh
#            (dockerfile·reinstall_agent.sh와 같은 미러 · 여기서 편집 → 호스트로 배포)
# 배치/실행: 호스트 /home/raymond/azp-agent-in-docker/trivy-db-update.sh (다른 에이전트 관리파일과 동거)
#            cron(raymond) `0 18 * * *`(KST 03:00)
# 로그:      /opt/trivy-cache/update.log

set -euo pipefail

# updater와 에이전트의 trivy 버전은 동일해야 한다(DB 스키마 호환). 구축 시 최신 안정본으로 확정(계획서 §7).
TRIVY_VERSION="${TRIVY_VERSION:-0.74.0}"
CACHE_DIR="${CACHE_DIR:-/opt/trivy-cache}"   # 4 에이전트가 읽기전용으로 공유하는 호스트 볼륨
LOG="${CACHE_DIR}/update.log"

echo "=== $(date -u +%FT%TZ) trivy DB update start (trivy ${TRIVY_VERSION}) ===" >> "$LOG"
if docker run --rm -v "${CACHE_DIR}:/cache" "aquasec/trivy:${TRIVY_VERSION}" \
     image --download-db-only --cache-dir /cache >> "$LOG" 2>&1; then
  echo "OK   $(date -u +%FT%TZ)" >> "$LOG"
else
  echo "FAIL $(date -u +%FT%TZ) (마지막 성공본 유지·CI 무영향)" >> "$LOG"
  exit 1
fi
