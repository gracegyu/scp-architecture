# Azure Pipelines self-hosted agent (Self-hosted1 pool) — GW 백엔드 + Console 빌드용
#
# 변경(2026-09-02): 지난번 실패(에이전트에 Docker 부재) 대응 + 양쪽 repo 요구 superset:
#   - Docker CLI + buildx  : GW devsecops-* 파이프라인의 이미지 buildx build/push (핵심 원인)
#   - AWS CLI v2           : GW 이미지 push(서비스커넥션)·Console `aws s3 sync`
#   - Playwright chromium 시스템 라이브러리 : Console e2e·a11y·시각 회귀(`--with-deps` 없이 통과)
#   ※ Docker 데몬은 이 컨테이너에 없다 — reinstall_agent.sh 가 호스트 /var/run/docker.sock 을 마운트해
#     "docker CLI(컨테이너) → 호스트 데몬" 으로 빌드한다(가장 간단·self-hosted 박스 전용).
#   ※ Node/pnpm 은 파이프라인이 준비: Console=UseNode@1(20.19.x)+corepack(pnpm 9.15.9),
#     GW=이미지 빌드가 docker 내부에서 node 사용(에이전트 host node 불요) → 이미지에 pre-bake 안 함.
FROM ubuntu:22.04

ENV TARGETARCH="linux-x64"
ENV DEBIAN_FRONTEND=noninteractive

# 기본 도구 + 빌드 필수 (+ docker/aws repo 준비용 ca-certificates·gnupg·unzip·lsb-release)
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --fix-missing \
       curl git jq libicu70 iputils-ping build-essential python3 bash \
       ca-certificates gnupg unzip lsb-release \
    && apt-get dist-upgrade -y

# Rust/Cargo (기존 유지 — 이 풀을 쓰는 다른 잡 대비)
RUN curl -sSf https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init -o rustup-init \
    && chmod +x rustup-init && ./rustup-init -y && rm rustup-init \
    && . /root/.cargo/env && rustup default stable

# Docker CLI + buildx (데몬 아님 — 호스트 소켓 마운트로 사용) : GW 이미지 buildx build/push
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable" \
       > /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y docker-ce-cli docker-buildx-plugin

# AWS CLI v2 : GW 이미지 push(서비스커넥션 es-ci-es-platforms)·Console aws s3 sync
RUN curl -sSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip \
    && unzip -q awscliv2.zip && ./aws/install && rm -rf awscliv2.zip aws

# 보안 스캐너(trivy·gitleaks)는 이미지에 넣지 않는다 — 공유 볼륨 /opt/trivy-cache/bin/ 에 두고
# 새벽 cron(ci-scanners-update.sh)이 매일 자동 최신화(smoke-test). 에이전트는 그 볼륨을 :ro 마운트하고
# CI 는 /opt/trivy-cache/bin/{trivy,gitleaks} 를 호출 → 버전업에 이미지 재빌드/에이전트 재설치 불요.

# Playwright chromium 시스템 라이브러리 (Console e2e·a11y·시각) — 사전설치로 `--with-deps`(apt/sudo) 함정 회피
RUN apt-get update && apt-get install -y \
       libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-0 \
       libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 \
       libxcb1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2 libwayland-client0 \
       fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /azp/

COPY ./start.sh ./
RUN chmod +x ./start.sh

# Create agent user and set up home directory
RUN useradd -m -d /home/agent agent
RUN chown -R agent:agent /azp /home/agent

# root 로 실행(AGENT_ALLOW_RUNASROOT) — 마운트한 docker.sock 접근 + apt(--with-deps 필요 시) 가능
# USER agent
ENV AGENT_ALLOW_RUNASROOT="true"

# Add Cargo to PATH for all users
ENV PATH="/root/.cargo/bin:${PATH}"

ENTRYPOINT [ "./start.sh" ]
