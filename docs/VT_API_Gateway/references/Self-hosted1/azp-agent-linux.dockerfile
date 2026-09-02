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