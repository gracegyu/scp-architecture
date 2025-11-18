# PoC #2 저장소 아키텍처 벤치마크

## 개요

파일시스템, RocksDB, MinIO의 실제 성능을 Docker 환경에서 측정하여 비교합니다.

## 테스트 환경

- **파일시스템**: 해시 기반 2단계 디렉터리 구조
- **RocksDB**: LSM-Tree 기반 키-값 저장소 (LZ4 압축)
- **MinIO**: S3 호환 오브젝트 스토리지

## 테스트 시나리오

1. **썸네일 쓰기/읽기**: 200KB × 1,000개
2. **CT 이미지 쓰기/읽기**: 20MB × 100개

## 실행 방법

### 1. Docker 환경 구동

```bash
cd poc2-benchmark
docker-compose up -d
```

### 2. 벤치마크 실행

```bash
docker-compose run --rm benchmark python benchmark.py
```

### 3. 결과 확인

```bash
cat results/benchmark_results.json
```

### 4. 환경 정리

```bash
docker-compose down -v
```

## 측정 지표

- **쓰기 성능**: 평균 지연시간, 95p, 99p
- **읽기 성능**: 평균 지연시간, 95p, 99p
- **디스크 사용량**: 실제 사용 공간 (압축 포함)
- **메모리 사용량**: 컨테이너 메모리 사용량

## 결과 분석

벤치마크 완료 후 `benchmark_results.json` 파일을 확인하여:

1. 각 저장소별 성능 비교
2. 썸네일 vs CT 이미지 크기별 성능 차이
3. 디스크 효율 비교 (압축률)

결과는 `PoC2_저장소_아키텍처_result.md` 문서에 반영됩니다.

## 트러블슈팅

### MinIO 연결 실패

```bash
# MinIO 상태 확인
docker-compose logs minio

# MinIO 재시작
docker-compose restart minio
```

### RocksDB 빌드 실패

RocksDB Python 바인딩 컴파일에 시간이 걸릴 수 있습니다.
빌드 로그를 확인하세요:

```bash
docker-compose build --no-cache benchmark
```

### 디스크 공간 부족

테스트 데이터는 약 2GB 이상 필요합니다.

```bash
# 데이터 정리
rm -rf data/*
```

## 주의사항

- 벤치마크는 약 10-15분 소요됩니다.
- 테스트 중 다른 작업을 하지 마세요 (정확한 측정을 위해).
- 결과는 시스템 성능에 따라 달라질 수 있습니다.

