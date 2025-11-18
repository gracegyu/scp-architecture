FROM python:3.11-slim

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 작업 디렉터리 설정
WORKDIR /benchmark

# 벤치마크 스크립트 실행 권한 부여
COPY benchmark.py /benchmark/
RUN chmod +x /benchmark/benchmark.py

# 결과 디렉터리 생성
RUN mkdir -p /results /benchmark/cache

CMD ["python", "/benchmark/benchmark.py"]

