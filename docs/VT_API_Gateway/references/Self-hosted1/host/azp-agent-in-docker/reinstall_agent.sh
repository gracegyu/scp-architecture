#!/bin/bash
# Azure Pipelines 에이전트 컨테이너 재생성 스크립트.
#
#   관리 정본 : scp-architecture repo · docs/VT_API_Gateway/references/Self-hosted1/host/azp-agent-in-docker/reinstall_agent.sh   <- 이 파일
#   배치 위치 : 빌드 호스트 ~/azp-agent-in-docker/reinstall_agent.sh
#
# sbom/jenkins 저장소 docker/ 에도 사본이 있다. 그쪽은 참고용이다.
#
# ⚠ 이 스크립트는 Self-hosted1 풀 전체를 재생성한다. 그 풀을 쓰는 모든 ADO
#   파이프라인이 그동안 멈춘다. 도는 빌드가 없는 시간에 실행할 것.
set -euo pipefail

# ── 시크릿 ───────────────────────────────────────────────────────────
# PAT 는 이 파일에 두지 않는다. 한동안 평문으로 들어 있었는데, 파일 권한이
# 644 라 호스트의 다른 사용자도 읽을 수 있었고 .bak 사본에도 그대로 남았다.
# git 추적에서 빠져 있다는 것만으로는 가려지지 않는다.
#
#   ~/.azp-agent-secrets  (chmod 600)
#     AZP_TOKEN=<PAT>
#
# PAT 스코프: Agent Pools (Read & manage). 에이전트 **등록** 에만 쓰인다 —
# 이미 등록된 에이전트는 PAT 가 만료돼도 계속 돈다. 그래서 만료를 모르고
# 지내다가 재생성하려는 순간 막힌다.
SECRETS_FILE="${SECRETS_FILE:-$HOME/.azp-agent-secrets}"
if [ ! -f "$SECRETS_FILE" ]; then
  echo "시크릿 파일이 없다: $SECRETS_FILE" >&2
  echo "  AZP_TOKEN=<PAT> 한 줄을 적고 chmod 600 할 것." >&2
  exit 1
fi
# shellcheck source=/dev/null
. "$SECRETS_FILE"
if [ -z "${AZP_TOKEN:-}" ]; then
  echo "$SECRETS_FILE 에 AZP_TOKEN 이 없다." >&2
  exit 1
fi

# ── docker ───────────────────────────────────────────────────────────
# sudo 를 쓰지 않는다. 운영 계정이 docker 그룹에 있어 필요 없고, sudo 를 붙이면
# TTY 가 없는 실행(ssh 비대화식·자동화)에서 "a password is required" 로 전부
# 실패한다. stop 과 rm 이 따로라 중간에 걸리면 반쯤 지워진 상태가 될 수 있다.
DOCKER="${DOCKER:-docker}"
if ! $DOCKER ps >/dev/null 2>&1; then
  echo "docker 를 실행할 수 없다: $DOCKER" >&2
  echo "  운영 계정이 docker 그룹에 있는지 확인할 것." >&2
  exit 1
fi

# ── 설정 ─────────────────────────────────────────────────────────────
AZP_URL="https://dev.azure.com/ewoosoft"
AZP_POOL="Self-hosted1"
BASE_AGENT_NAME="Agent Linux"
BASE_CONTAINER_NAME="azp-agent-linux"
IMAGE="${IMAGE:-azp-agent:linux}"
NEW_N=${1:-4}

echo "이미지=$IMAGE  풀=$AZP_POOL  개수=$NEW_N"

# PAT 가 유효한지 먼저 확인한다. 등록 단계에서 실패하면 컨테이너는 지워진
# 뒤라 풀이 빈 채로 남는다.
code=$(curl -s -o /dev/null -w "%{http_code}" -u ":$AZP_TOKEN" \
  "$AZP_URL/_apis/projects?api-version=7.1" || echo 000)
if [ "$code" != "200" ]; then
  echo "PAT 가 유효하지 않다 (HTTP $code). 재생성을 중단한다." >&2
  echo "  새 PAT 를 발급해 $SECRETS_FILE 에 넣을 것 (스코프: Agent Pools · Read & manage)." >&2
  exit 1
fi
echo "PAT 확인 완료 (HTTP 200)"

# 1. 기존 에이전트 중지·삭제
echo "기존 컨테이너 정리: ${BASE_CONTAINER_NAME}*"
for CONTAINER_ID in $($DOCKER ps -a --filter "name=$BASE_CONTAINER_NAME" --format "{{.ID}}"); do
  echo "  중지·삭제: $CONTAINER_ID"
  $DOCKER stop "$CONTAINER_ID" >/dev/null || true
  $DOCKER rm "$CONTAINER_ID" >/dev/null || true
done

# 2. 새 에이전트 설치
echo "에이전트 $NEW_N 대 생성"
for i in $(seq 1 "$NEW_N"); do
  AGENT_NAME="${BASE_AGENT_NAME}${i}"
  CONTAINER_NAME="${BASE_CONTAINER_NAME}${i}"
  echo "  생성: $CONTAINER_NAME"
  $DOCKER run -d --restart unless-stopped \
    --network webnet \
    --dns 192.168.6.5 \
    --dns 192.168.6.140 \
    --dns 192.168.6.40 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /opt/trivy-cache:/opt/trivy-cache:ro \
    --memory=6g --memory-swap=6g \
    -e AZP_URL="$AZP_URL" \
    -e AZP_TOKEN="$AZP_TOKEN" \
    -e AZP_POOL="$AZP_POOL" \
    -e AZP_AGENT_NAME="$AGENT_NAME" \
    --name "$CONTAINER_NAME" "$IMAGE" >/dev/null
done

echo "완료. 등록 확인: $DOCKER logs ${BASE_CONTAINER_NAME}1 | tail -20"
