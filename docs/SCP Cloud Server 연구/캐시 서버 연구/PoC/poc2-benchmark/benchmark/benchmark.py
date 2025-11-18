#!/usr/bin/env python3
"""
PoC #2 저장소 아키텍처 벤치마크

파일시스템, RocksDB, MinIO의 성능을 실제 측정하여 비교
"""

import time
import os
import hashlib
import statistics
import json
from pathlib import Path
from io import BytesIO

# 의존성 체크
try:
    from minio import Minio
    from minio.error import S3Error
    MINIO_AVAILABLE = True
except ImportError:
    print("경고: MinIO SDK를 찾을 수 없습니다.")
    MINIO_AVAILABLE = False
    Minio = None

try:
    import rocksdb
    ROCKSDB_AVAILABLE = True
except ImportError:
    print("경고: RocksDB를 찾을 수 없습니다. (파일시스템, MinIO만 테스트)")
    ROCKSDB_AVAILABLE = False
    rocksdb = None


class StorageBenchmark:
    def __init__(self):
        self.test_data_sizes = [
            (200 * 1024, "thumb", 1000),      # 200KB 썸네일 × 1000개
            (20 * 1024 * 1024, "ct", 100)     # 20MB CT 이미지 × 100개
        ]
        
    def generate_test_data(self, size):
        """테스트 데이터 생성"""
        return os.urandom(size)
    
    def benchmark_filesystem(self, base_path="/benchmark/cache"):
        """파일시스템 벤치마크"""
        print("\n" + "=" * 60)
        print("파일시스템 벤치마크")
        print("=" * 60)
        
        results = {}
        
        for size, data_type, iterations in self.test_data_sizes:
            print(f"\n[FileSystem] Testing {data_type} ({size} bytes × {iterations}개)...")
            
            # 쓰기 테스트
            write_times = []
            for i in range(iterations):
                data = self.generate_test_data(size)
                hash_key = hashlib.sha256(f"clinic123:study{i}".encode()).hexdigest()
                
                # 경로 생성
                dir_path = Path(base_path) / data_type / hash_key[0:2] / hash_key[2:4]
                dir_path.mkdir(parents=True, exist_ok=True)
                file_path = dir_path / f"{hash_key}.bin"
                
                # 쓰기 시간 측정
                start = time.perf_counter()
                file_path.write_bytes(data)
                elapsed = (time.perf_counter() - start) * 1000  # ms
                write_times.append(elapsed)
                
                if (i + 1) % 100 == 0:
                    print(f"  쓰기 진행: {i+1}/{iterations}")
            
            # 디스크 사용량 측정
            total_size = sum(f.stat().st_size for f in Path(base_path).rglob('*') if f.is_file())
            
            # 읽기 테스트
            print(f"  읽기 테스트 시작...")
            read_times = []
            for i in range(iterations):
                hash_key = hashlib.sha256(f"clinic123:study{i}".encode()).hexdigest()
                file_path = Path(base_path) / data_type / hash_key[0:2] / hash_key[2:4] / f"{hash_key}.bin"
                
                start = time.perf_counter()
                data = file_path.read_bytes()
                elapsed = (time.perf_counter() - start) * 1000
                read_times.append(elapsed)
                
                if (i + 1) % 100 == 0:
                    print(f"  읽기 진행: {i+1}/{iterations}")
            
            results[data_type] = {
                "write": self.calculate_stats(write_times),
                "read": self.calculate_stats(read_times),
                "disk_usage_mb": round(total_size / (1024 * 1024), 2),
                "iterations": iterations
            }
            
            print(f"  쓰기 - 평균: {results[data_type]['write']['mean']:.2f}ms, 95p: {results[data_type]['write']['p95']:.2f}ms")
            print(f"  읽기 - 평균: {results[data_type]['read']['mean']:.2f}ms, 95p: {results[data_type]['read']['p95']:.2f}ms")
            print(f"  디스크 사용량: {results[data_type]['disk_usage_mb']} MB")
        
        return results
    
    def benchmark_minio(self, endpoint="minio:9000"):
        """MinIO 벤치마크"""
        if not MINIO_AVAILABLE:
            print("\nMinIO SDK가 설치되지 않아 건너뜁니다.")
            return {}
        
        print("\n" + "=" * 60)
        print("MinIO 벤치마크")
        print("=" * 60)
        
        try:
            client = Minio(
                endpoint,
                access_key="admin",
                secret_key="password123",
                secure=False
            )
            
            # 버킷 생성
            bucket_name = "poc2-benchmark"
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                print(f"버킷 '{bucket_name}' 생성됨")
            
        except Exception as e:
            print(f"\nMinIO 연결 실패: {e}")
            print("MinIO 서버가 실행 중인지 확인하세요.")
            return {}
        
        results = {}
        
        for size, data_type, iterations in self.test_data_sizes:
            print(f"\n[MinIO] Testing {data_type} ({size} bytes × {iterations}개)...")
            
            # 쓰기 테스트
            write_times = []
            for i in range(iterations):
                data = self.generate_test_data(size)
                object_name = f"{data_type}/study{i}.bin"
                
                start = time.perf_counter()
                client.put_object(
                    bucket_name,
                    object_name,
                    BytesIO(data),
                    length=size
                )
                elapsed = (time.perf_counter() - start) * 1000
                write_times.append(elapsed)
                
                if (i + 1) % 100 == 0:
                    print(f"  쓰기 진행: {i+1}/{iterations}")
            
            # 읽기 테스트
            print(f"  읽기 테스트 시작...")
            read_times = []
            for i in range(iterations):
                object_name = f"{data_type}/study{i}.bin"
                
                start = time.perf_counter()
                response = client.get_object(bucket_name, object_name)
                data = response.read()
                response.close()
                response.release_conn()
                elapsed = (time.perf_counter() - start) * 1000
                read_times.append(elapsed)
                
                if (i + 1) % 100 == 0:
                    print(f"  읽기 진행: {i+1}/{iterations}")
            
            results[data_type] = {
                "write": self.calculate_stats(write_times),
                "read": self.calculate_stats(read_times),
                "iterations": iterations
            }
            
            print(f"  쓰기 - 평균: {results[data_type]['write']['mean']:.2f}ms, 95p: {results[data_type]['write']['p95']:.2f}ms")
            print(f"  읽기 - 평균: {results[data_type]['read']['mean']:.2f}ms, 95p: {results[data_type]['read']['p95']:.2f}ms")
        
        return results
    
    def benchmark_rocksdb(self, db_path="/benchmark/rocksdb/db"):
        """RocksDB 벤치마크"""
        if not ROCKSDB_AVAILABLE:
            print("\nRocksDB가 설치되지 않아 건너뜁니다.")
            return {}
        
        print("\n" + "=" * 60)
        print("RocksDB 벤치마크")
        print("=" * 60)
        
        # 디렉터리 생성
        Path(db_path).mkdir(parents=True, exist_ok=True)
        
        try:
            opts = rocksdb.Options()
            opts.create_if_missing = True
            opts.compression = rocksdb.CompressionType.lz4_compression
            
            db = rocksdb.DB(db_path, opts)
        except Exception as e:
            print(f"\nRocksDB 초기화 실패: {e}")
            return {}
        
        results = {}
        
        for size, data_type, iterations in self.test_data_sizes:
            print(f"\n[RocksDB] Testing {data_type} ({size} bytes × {iterations}개)...")
            
            # 쓰기 테스트
            write_times = []
            for i in range(iterations):
                data = self.generate_test_data(size)
                key = f"clinic123:study{i}:{data_type}".encode()
                
                start = time.perf_counter()
                db.put(key, data)
                elapsed = (time.perf_counter() - start) * 1000
                write_times.append(elapsed)
                
                if (i + 1) % 100 == 0:
                    print(f"  쓰기 진행: {i+1}/{iterations}")
            
            # 읽기 테스트
            print(f"  읽기 테스트 시작...")
            read_times = []
            for i in range(iterations):
                key = f"clinic123:study{i}:{data_type}".encode()
                
                start = time.perf_counter()
                data = db.get(key)
                elapsed = (time.perf_counter() - start) * 1000
                read_times.append(elapsed)
                
                if (i + 1) % 100 == 0:
                    print(f"  읽기 진행: {i+1}/{iterations}")
            
            # 디스크 사용량 측정
            total_size = sum(f.stat().st_size for f in Path(db_path).rglob('*') if f.is_file())
            
            results[data_type] = {
                "write": self.calculate_stats(write_times),
                "read": self.calculate_stats(read_times),
                "disk_usage_mb": round(total_size / (1024 * 1024), 2),
                "iterations": iterations
            }
            
            print(f"  쓰기 - 평균: {results[data_type]['write']['mean']:.2f}ms, 95p: {results[data_type]['write']['p95']:.2f}ms")
            print(f"  읽기 - 평균: {results[data_type]['read']['mean']:.2f}ms, 95p: {results[data_type]['read']['p95']:.2f}ms")
            print(f"  디스크 사용량: {results[data_type]['disk_usage_mb']} MB")
        
        return results
    
    def calculate_stats(self, times):
        """통계 계산"""
        if not times:
            return {}
        
        times_sorted = sorted(times)
        return {
            "mean": round(statistics.mean(times), 2),
            "median": round(statistics.median(times), 2),
            "p50": round(times_sorted[int(len(times) * 0.50)], 2),
            "p95": round(times_sorted[int(len(times) * 0.95)], 2),
            "p99": round(times_sorted[int(len(times) * 0.99)], 2),
            "min": round(min(times), 2),
            "max": round(max(times), 2)
        }
    
    def run_all(self):
        """모든 벤치마크 실행"""
        print("=" * 60)
        print("PoC #2 저장소 벤치마크 시작")
        print("=" * 60)
        print(f"테스트 시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"사용 가능한 저장소: 파일시스템" + 
              (", MinIO" if MINIO_AVAILABLE else "") + 
              (", RocksDB" if ROCKSDB_AVAILABLE else ""))
        
        results = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "test_config": {
                "thumb_size_kb": 200,
                "thumb_count": 1000,
                "ct_size_mb": 20,
                "ct_count": 100
            },
            "available_storage": {
                "filesystem": True,
                "minio": MINIO_AVAILABLE,
                "rocksdb": ROCKSDB_AVAILABLE
            }
        }
        
        # 1. 파일시스템
        print("\n[1/3] 파일시스템 벤치마크...")
        results["filesystem"] = self.benchmark_filesystem()
        
        # 2. MinIO
        if MINIO_AVAILABLE:
            print("\n[2/3] MinIO 벤치마크...")
            results["minio"] = self.benchmark_minio()
        else:
            print("\n[2/3] MinIO 건너뜀 (SDK 없음)")
            results["minio"] = {}
        
        # 3. RocksDB
        if ROCKSDB_AVAILABLE:
            print("\n[3/3] RocksDB 벤치마크...")
            results["rocksdb"] = self.benchmark_rocksdb()
        else:
            print("\n[3/3] RocksDB 건너뜀 (라이브러리 없음)")
            results["rocksdb"] = {}
        
        # 결과 저장
        self.save_results(results)
        self.print_summary(results)
        
        return results
    
    def save_results(self, results):
        """결과를 JSON 파일로 저장"""
        output_path = "/results/benchmark_results.json"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n결과가 {output_path}에 저장되었습니다.")
    
    def print_summary(self, results):
        """결과 요약 출력"""
        print("\n" + "=" * 60)
        print("벤치마크 결과 요약")
        print("=" * 60)
        
        for storage in ["filesystem", "minio", "rocksdb"]:
            if storage not in results or not results[storage]:
                continue
            
            print(f"\n[{storage.upper()}]")
            for data_type in ["thumb", "ct"]:
                if data_type not in results[storage]:
                    continue
                
                data = results[storage][data_type]
                print(f"  {data_type}:")
                print(f"    쓰기 - 평균: {data['write']['mean']:.2f}ms, 95p: {data['write']['p95']:.2f}ms")
                print(f"    읽기 - 평균: {data['read']['mean']:.2f}ms, 95p: {data['read']['p95']:.2f}ms")
                if 'disk_usage_mb' in data:
                    print(f"    디스크: {data['disk_usage_mb']} MB")


if __name__ == "__main__":
    benchmark = StorageBenchmark()
    benchmark.run_all()

