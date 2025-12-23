#!/usr/bin/env python3
"""
캐시 시뮬레이터

다양한 캐시 알고리즘의 성능을 측정합니다.
"""

import time
from typing import Dict, List, Optional
from cache_algorithms import LRUCache, SLRUCache, WindowTinyLFU


class CacheSimulator:
    """
    캐시 시뮬레이터
    """
    
    def __init__(self, algorithm_type: str, capacity: int, **kwargs):
        """
        Args:
            algorithm_type: 'LRU', 'SLRU', 'TinyLFU', 'Hybrid'
            capacity: 캐시 용량 (바이트)
            **kwargs: 알고리즘별 추가 파라미터
        """
        self.capacity = capacity
        self.algorithm_type = algorithm_type
        
        # 알고리즘 초기화
        if algorithm_type == 'LRU':
            self.algorithm = LRUCache(capacity)
        elif algorithm_type == 'SLRU':
            probation_ratio = kwargs.get('probation_ratio', 0.2)
            self.algorithm = SLRUCache(capacity, probation_ratio)
        elif algorithm_type == 'TinyLFU' or algorithm_type == 'Hybrid':
            window_ratio = kwargs.get('window_ratio', 0.01)
            threshold = kwargs.get('threshold', 5)
            self.algorithm = WindowTinyLFU(capacity, window_ratio, threshold)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_type}")
        
        # 통계
        self.stats = {
            'hit': 0,
            'miss': 0,
            'byte_hit': 0,
            'byte_miss': 0,
            'admitted': 0,
            'rejected': 0,
            'evicted': 0,
            'access_count': 0,
            'total_latency_ms': 0.0
        }
        
        # 메모리 오버헤드 추정
        self.memory_overhead = {
            'base': 0,  # 기본 캐시 구조 오버헤드
            'sketch': 0,  # Count-Min Sketch 오버헤드
            'metadata': 0  # 메타데이터 오버헤드
        }
        
        # 알고리즘별 오버헤드 계산
        if algorithm_type == 'TinyLFU' or algorithm_type == 'Hybrid':
            # Count-Min Sketch: width * depth * 4 bytes (int)
            sketch_width = 1000000
            sketch_depth = 5
            self.memory_overhead['sketch'] = sketch_width * sketch_depth * 4
    
    def access(self, key: str, size: int) -> Dict:
        """
        캐시 접근 시뮬레이션
        
        Returns:
            {'hit': bool, 'latency_ms': float}
        """
        start_time = time.perf_counter()
        self.stats['access_count'] += 1
        
        is_hit = self.algorithm.contains(key)
        
        if is_hit:
            self.stats['hit'] += 1
            self.stats['byte_hit'] += size
            self.algorithm.on_hit(key)
            result = {'hit': True, 'latency_ms': 0.0}
        else:
            self.stats['miss'] += 1
            self.stats['byte_miss'] += size
            
            # 입소 필터 적용
            should_admit = self.algorithm.should_admit(key)
            
            if should_admit:
                self.stats['admitted'] += 1
                evicted = self.algorithm.admit(key, size)
                if evicted:
                    self.stats['evicted'] += 1
            else:
                self.stats['rejected'] += 1
            
            result = {'hit': False, 'latency_ms': 0.0}
        
        # 지연 시간 측정
        latency_ms = (time.perf_counter() - start_time) * 1000
        result['latency_ms'] = latency_ms
        self.stats['total_latency_ms'] += latency_ms
        
        return result
    
    def get_hit_rate(self) -> float:
        """요청 히트율 계산"""
        total = self.stats['hit'] + self.stats['miss']
        if total == 0:
            return 0.0
        return self.stats['hit'] / total
    
    def get_byte_hit_rate(self) -> float:
        """바이트 히트율 계산"""
        total = self.stats['byte_hit'] + self.stats['byte_miss']
        if total == 0:
            return 0.0
        return self.stats['byte_hit'] / total
    
    def get_admission_rate(self) -> float:
        """입소율 계산"""
        total = self.stats['admitted'] + self.stats['rejected']
        if total == 0:
            return 1.0
        return self.stats['admitted'] / total
    
    def get_avg_latency_ms(self) -> float:
        """평균 지연 시간 계산"""
        if self.stats['access_count'] == 0:
            return 0.0
        return self.stats['total_latency_ms'] / self.stats['access_count']
    
    def get_memory_overhead_ratio(self) -> float:
        """메모리 오버헤드 비율 계산"""
        total_overhead = sum(self.memory_overhead.values())
        if self.capacity == 0:
            return 0.0
        return total_overhead / self.capacity
    
    def get_stats(self) -> Dict:
        """전체 통계 반환"""
        return {
            'algorithm': self.algorithm_type,
            'capacity_bytes': self.capacity,
            'hit_rate': self.get_hit_rate(),
            'byte_hit_rate': self.get_byte_hit_rate(),
            'admission_rate': self.get_admission_rate(),
            'avg_latency_ms': self.get_avg_latency_ms(),
            'memory_overhead_ratio': self.get_memory_overhead_ratio(),
            'total_access': self.stats['access_count'],
            'total_hit': self.stats['hit'],
            'total_miss': self.stats['miss'],
            'total_admitted': self.stats['admitted'],
            'total_rejected': self.stats['rejected'],
            'total_evicted': self.stats['evicted']
        }
    
    def reset_stats(self):
        """통계 초기화"""
        self.stats = {
            'hit': 0,
            'miss': 0,
            'byte_hit': 0,
            'byte_miss': 0,
            'admitted': 0,
            'rejected': 0,
            'evicted': 0,
            'access_count': 0,
            'total_latency_ms': 0.0
        }


def run_simulation(trace: List[Dict], algorithm_type: str, capacity: int, **kwargs) -> Dict:
    """
    트레이스를 사용하여 캐시 시뮬레이션 실행
    
    Args:
        trace: 접근 패턴 트레이스 [{'key': str, 'size': int, ...}, ...]
        algorithm_type: 알고리즘 타입
        capacity: 캐시 용량 (바이트)
        **kwargs: 알고리즘별 추가 파라미터
    
    Returns:
        시뮬레이션 결과 통계
    """
    simulator = CacheSimulator(algorithm_type, capacity, **kwargs)
    
    print(f"Running simulation: {algorithm_type} (capacity: {capacity / (1024**3):.2f} GB)")
    
    # 트레이스 재생
    for i, req in enumerate(trace):
        if (i + 1) % 100000 == 0:
            hit_rate = simulator.get_hit_rate()
            print(f"  Progress: {i+1}/{len(trace)} ({100*(i+1)/len(trace):.1f}%), Hit rate: {hit_rate*100:.2f}%")
        
        simulator.access(req['key'], req['size'])
    
    stats = simulator.get_stats()
    return stats


if __name__ == '__main__':
    # 테스트
    import json
    
    # 샘플 트레이스 생성
    trace = [
        {'key': 'key1', 'size': 1024},
        {'key': 'key2', 'size': 2048},
        {'key': 'key1', 'size': 1024},
        {'key': 'key3', 'size': 3072},
    ]
    
    # LRU 시뮬레이션
    result = run_simulation(trace, 'LRU', capacity=10 * 1024)
    print("\nLRU Results:")
    print(json.dumps(result, indent=2))














