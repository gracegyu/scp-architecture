#!/bin/bash

# 에이전트 정보 설정
AZP_URL="https://dev.azure.com/ewoosoft"
AZP_TOKEN="oirakc********************************"  # 새로 발급받은 PAT
AZP_POOL="Self-hosted1"
BASE_AGENT_NAME="Agent Linux"  # 에이전트 이름의 기본 값
BASE_CONTAINER_NAME="azp-agent-linux"  # 도커 컨테이너 이름의 기본 값

# New 에이전트 수 설정 (초기값 N은 4, 필요에 따라 수정 가능)
NEW_N=${1:-4}

# 1. Old 에이전트 중지 및 삭제 (모든 Old 에이전트 탐색)
echo "Stopping and removing all existing agents with the name pattern: $BASE_CONTAINER_NAME*..."
for CONTAINER_ID in $(sudo docker ps -a --filter "name=$BASE_CONTAINER_NAME" --format "{{.ID}}"); do
  echo "Stopping and removing container ID: $CONTAINER_ID"
  sudo docker stop $CONTAINER_ID
  sudo docker rm $CONTAINER_ID
done

# 2. New 에이전트 설치
echo "Installing $NEW_N new Azure Pipelines agents..."

for i in $(seq 1 $NEW_N); do
  AGENT_NAME="${BASE_AGENT_NAME}${i}"
  CONTAINER_NAME="${BASE_CONTAINER_NAME}${i}"

  echo "Reinstalling Azure Pipelines agent: $CONTAINER_NAME..."
  sudo nohup docker run --restart unless-stopped \
    --network webnet \
    --dns 192.168.6.5 \
    --dns 192.168.6.140 \
    --dns 192.168.6.40 \
    -e AZP_URL="$AZP_URL" \
    -e AZP_TOKEN="$AZP_TOKEN" \
    -e AZP_POOL="$AZP_POOL" \
    -e AZP_AGENT_NAME="$AGENT_NAME" \
    --name "$CONTAINER_NAME" azp-agent:linux &
done

echo "Reinstallation of $NEW_N Azure Pipelines agents complete."