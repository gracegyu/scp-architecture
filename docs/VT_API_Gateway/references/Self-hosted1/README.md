# **Dockerfile & docker run 이용**

- 사전 준비
  - $ sudo docker network create webnet
- 참조 : https://learn.microsoft.com/ko-kr/azure/devops/pipelines/agents/docker?view=azure-devops
- Docker image 생성
  - $ mkdir azp-agent-in-docker
  - $ cd azp-agent-in-docker
  - Dockerfile 생성 (root로 실행, Rust, Cargo 설치, 필요한 여러 모듈 미리 설치)
  - azp-agent-linux.dockerfile

```
FROM ubuntu:22.04

ENV TARGETARCH="linux-x64"

# Update package lists, upgrade existing packages, and fix any missing packages
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --fix-missing curl git jq libicu70 iputils-ping build-essential python3 \
    && apt-get dist-upgrade -y \
    && apt-get install -y bash  # Install bash explicitly

# Download and install Rust and Cargo directly using rustup-init binary
RUN curl -sSf https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init -o rustup-init \
    && chmod +x rustup-init \
    && ./rustup-init -y \
    && rm rustup-init \
    && . /root/.cargo/env \
    && rustup default stable

# Set the working directory
WORKDIR /azp/

COPY ./start.sh ./
RUN chmod +x ./start.sh

# Create agent user and set up home directory
RUN useradd -m -d /home/agent agent
RUN chown -R agent:agent /azp /home/agent

# USER agent
ENV AGENT_ALLOW_RUNASROOT="true"

# Add Cargo to PATH for all users
ENV PATH="/root/.cargo/bin:${PATH}"

ENTRYPOINT [ "./start.sh" ]
```

- start.sh 만들기
  - start.sh

```
#!/bin/bash
set -e

if [ -z "${AZP_URL}" ]; then
  echo 1>&2 "error: missing AZP_URL environment variable"
  exit 1
fi

if [ -z "${AZP_TOKEN_FILE}" ]; then
  if [ -z "${AZP_TOKEN}" ]; then
    echo 1>&2 "error: missing AZP_TOKEN environment variable"
    exit 1
  fi

  AZP_TOKEN_FILE="/azp/.token"
  echo -n "${AZP_TOKEN}" > "${AZP_TOKEN_FILE}"
fi

unset AZP_TOKEN

if [ -n "${AZP_WORK}" ]; then
  mkdir -p "${AZP_WORK}"
fi

cleanup() {
  trap "" EXIT

  if [ -e ./config.sh ]; then
    print_header "Cleanup. Removing Azure Pipelines agent..."

    while true; do
      ./config.sh remove --unattended --auth "PAT" --token $(cat "${AZP_TOKEN_FILE}") && break

      echo "Retrying in 30 seconds..."
      sleep 30
    done
  fi
}

print_header() {
  lightcyan="\033[1;36m"
  nocolor="\033[0m"
  echo -e "\n${lightcyan}$1${nocolor}\n"
}

export VSO_AGENT_IGNORE="AZP_TOKEN,AZP_TOKEN_FILE"

print_header "1. Determining matching Azure Pipelines agent..."

AZP_AGENT_PACKAGES=$(curl -LsS \
    -u user:$(cat "${AZP_TOKEN_FILE}") \
    -H "Accept:application/json;" \
    "${AZP_URL}/_apis/distributedtask/packages/agent?platform=${TARGETARCH}&top=1")

AZP_AGENT_PACKAGE_LATEST_URL=$(echo "${AZP_AGENT_PACKAGES}" | jq -r ".value[0].downloadUrl")

if [ -z "${AZP_AGENT_PACKAGE_LATEST_URL}" -o "${AZP_AGENT_PACKAGE_LATEST_URL}" == "null" ]; then
  echo 1>&2 "error: could not determine a matching Azure Pipelines agent"
  echo 1>&2 "check that account "${AZP_URL}" is correct and the token is valid for that account"
  exit 1
fi

print_header "2. Downloading and extracting Azure Pipelines agent..."  

curl -LsS "${AZP_AGENT_PACKAGE_LATEST_URL}" | tar -xz & wait $!

source ./env.sh

trap "cleanup; exit 0" EXIT
trap "cleanup; exit 130" INT
trap "cleanup; exit 143" TERM

print_header "3. Configuring Azure Pipelines agent..."


./config.sh --unattended \
  --agent "${AZP_AGENT_NAME}" \
  --url "${AZP_URL}" \
  --auth "PAT" \
  --token $(cat "${AZP_TOKEN_FILE}") \
  --pool "${AZP_POOL:-Default}" \
  --work "${AZP_WORK:-_work}" \
  --replace \
  --acceptTeeEula & wait $!

print_header "4. Running Azure Pipelines agent..."

chmod +x ./run.sh

./run.sh "$@" & wait $!
```

- docker build
  - $ sudo docker build --tag "azp-agent:linux" --file "./azp-agent-linux.dockerfile" .
- Azure Devops 사이트에서 PAT를 발급 받는다.
  - https://dev.azure.com/ewoosoft/_usersSettings/tokens
- docker run으로 실행하기
  - 필요한 agent 갯수만큼 실행해야 한다.
    - ./reinstall_agent.sh을 실행하면 초기 실행도 된다.
- PAT가 만료되기 전에 agent를 재설치해줘야 함 
- ~/azp-agent-in-docker/reinstall_agent.sh

```
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
```

    - PAT가 만료되기 전에 Azure Devops에서 PAT를 새로 발급 받아서 reinstall_agent.sh의 AZP_TOKEN 값을 업데이트 하고 실행한다.
    - Agent 갯수 default 값은 4
        - ./reinstall_agent.sh 처럼 실행하면 4개가 실행됨
        - 6개를 실행하려면?
            - ./reinstall_agent.sh 6


- Pipeline에서 Self-hosted Agent 적용하기
  - Pipeline에서 Agent pool만 선택해서 빌드할 수도 있고, OS를 지정하여 빌드할 수도 있다.

```
pool:
  name: 'Self-hosted1'
  demands:
    - agent.os -equals Linux


pool:
  name: 'Self-hosted1'
  demands:
    - agent.os -equals Windows_NT

# MacOS
pool:
  name: 'Self-hosted1'
  demands:
    - agent.os -equals Darwin
```

    - OS 버전을 지정할 수 있다.

```
pool:
  name: 'Self-hosted1'
  demands:
    - agent.os -equals Linux
    - agent.os -equals Windows_NT

pool:
  name: 'Self-hosted1'
  demands:
    - agent.os -equals Windows_NT
    - Agent.OSVersion -equals 10.0.17763
```

    - Agent pool 내의 특정 Agent를 지정하여 빌드할 수 없다.
        - 그러려면 독립된 Agent pool을 만들어야 한다.
