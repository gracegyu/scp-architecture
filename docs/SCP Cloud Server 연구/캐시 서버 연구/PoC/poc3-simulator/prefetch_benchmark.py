#!/usr/bin/env python3
"""
프리페칭 전략 벤치마크

다양한 프리페칭 전략의 효과를 측정합니다.
"""

import json
import time
from typing import List, Dict
from cache_simulator import CacheSimulator
from prefetch_strategies import (
    NoPrefetch,
    PatientBasedPrefetch,
    SliceBasedPrefetch,
    TimeBasedPrefetch,
    PredictivePrefetch,
    MedicalSpecificPrefetch
)


class PrefetchCacheSimulator(CacheSimulator):
    """
    프리페칭 기능이 통합된 캐시 시뮬레이터
    """
    
    def __init__(self, algorithm_type: str, capacity: int, prefetch_strategy=None, **kwargs):
        super().__init__(algorithm_type, capacity, **kwargs)
        self.prefetch_strategy = prefetch_strategy or NoPrefetch()
        self.prefetched_keys = set()
        self.trace_keys_by_patient = {}
        self.trace_data = {}  # key -> size 매핑
        
        # 프리페칭 통계
        self.prefetch_stats = {
            'prefetch_hits': 0,  # 프리페칭된 항목이 실제로 힛된 횟수
            'prefetch_misses': 0  # 프리페칭된 항목이 실제로 미스된 횟수
        }
    
    def build_trace_index(self, trace: List[Dict]):
        """트레이스 인덱스 구축 (환자별 키 그룹화)"""
        for req in trace:
            key = req['key']
            size = req['size']
            self.trace_data[key] = size
            
            # 환자 ID 추출
            parts = key.split('/')
            if len(parts) >= 1:
                patient_id = parts[0]
                if patient_id not in self.trace_keys_by_patient:
                    self.trace_keys_by_patient[patient_id] = []
                if key not in self.trace_keys_by_patient[patient_id]:
                    self.trace_keys_by_patient[patient_id].append(key)
    
    def access_with_prefetch(self, current_request: Dict, trace: List[Dict] = None):
        """
        프리페칭을 포함한 캐시 접근
        
        Args:
            current_request: 현재 요청
            trace: 전체 트레이스 (프리페칭용)
        """
        key = current_request['key']
        size = current_request['size']
        
        # 프리페칭 결정
        prefetch_keys = self.prefetch_strategy.should_prefetch(current_request, self)
        
        # 프리페칭 실행
        if prefetch_keys:
            self.prefetch_strategy.prefetch(prefetch_keys, self, self.trace_data)
        
        # 실제 요청 처리
        is_hit = self.algorithm.contains(key)
        was_prefetched = key in self.prefetched_keys
        
        if is_hit:
            self.stats['hit'] += 1
            self.stats['byte_hit'] += size
            self.algorithm.on_hit(key)
            
            if was_prefetched:
                self.prefetch_stats['prefetch_hits'] += 1
        else:
            self.stats['miss'] += 1
            self.stats['byte_miss'] += size
            
            should_admit = self.algorithm.should_admit(key)
            if should_admit:
                self.stats['admitted'] += 1
                self.algorithm.admit(key, size)
                
                if was_prefetched:
                    self.prefetch_stats['prefetch_misses'] += 1
            else:
                self.stats['rejected'] += 1
        
        self.stats['access_count'] += 1
        
        # 프리페칭된 키에서 제거 (이미 처리됨)
        if key in self.prefetched_keys:
            self.prefetched_keys.remove(key)
    
    def get_prefetch_stats(self) -> Dict:
        """프리페칭 통계 반환"""
        prefetch_strategy_stats = self.prefetch_strategy.get_stats()
        
        prefetch_hit_rate = 0.0
        if self.prefetch_stats['prefetch_hits'] + self.prefetch_stats['prefetch_misses'] > 0:
            prefetch_hit_rate = (self.prefetch_stats['prefetch_hits'] / 
                               (self.prefetch_stats['prefetch_hits'] + self.prefetch_stats['prefetch_misses']))
        
        return {
            **prefetch_strategy_stats,
            'prefetch_hit_rate': prefetch_hit_rate,
            'prefetch_hits': self.prefetch_stats['prefetch_hits'],
            'prefetch_misses': self.prefetch_stats['prefetch_misses']
        }


def run_prefetch_benchmark(trace: List[Dict], algorithm_type: str, capacity: int, 
                          prefetch_strategy, strategy_name: str) -> Dict:
    """
    프리페칭 전략 벤치마크 실행
    
    Args:
        trace: 접근 패턴 트레이스
        algorithm_type: 캐시 알고리즘 타입
        capacity: 캐시 용량 (바이트)
        prefetch_strategy: 프리페칭 전략 인스턴스
        strategy_name: 전략 이름
    
    Returns:
        벤치마크 결과 통계
    """
    simulator = PrefetchCacheSimulator(algorithm_type, capacity, prefetch_strategy)
    
    # 트레이스 인덱스 구축
    simulator.build_trace_index(trace)
    
    print(f"Running prefetch benchmark: {strategy_name} ({algorithm_type}, {capacity / (1024**3):.2f} GB)")
    
    # 트레이스 재생
    start_time = time.time()
    for i, req in enumerate(trace):
        if (i + 1) % 100000 == 0:
            hit_rate = simulator.get_hit_rate()
            print(f"  Progress: {i+1}/{len(trace)} ({100*(i+1)/len(trace):.1f}%), Hit rate: {hit_rate*100:.2f}%")
        
        simulator.access_with_prefetch(req, trace)
    
    execution_time = time.time() - start_time
    
    # 통계 수집
    cache_stats = simulator.get_stats()
    prefetch_stats = simulator.get_prefetch_stats()
    
    # 히트율 향상 계산 (baseline 대비)
    baseline_hit_rate = cache_stats.get('baseline_hit_rate', 0.0)
    hit_rate_improvement = cache_stats['hit_rate'] - baseline_hit_rate if baseline_hit_rate > 0 else 0.0
    
    result = {
        'strategy': strategy_name,
        'algorithm': algorithm_type,
        'capacity_gb': capacity / (1024**3),
        'hit_rate': cache_stats['hit_rate'],
        'byte_hit_rate': cache_stats['byte_hit_rate'],
        'hit_rate_improvement': hit_rate_improvement,
        'hit_rate_improvement_pct': hit_rate_improvement * 100,
        'execution_time_sec': execution_time,
        **prefetch_stats
    }
    
    return result


def benchmark_all_prefetch_strategies(trace_file: str, algorithm_type: str = 'LRU', 
                                     capacity_gb: int = 100):
    """
    모든 프리페칭 전략에 대해 벤치마크 실행
    """
    # 트레이스 로드
    print(f"Loading trace from {trace_file}...")
    with open(trace_file, 'r') as f:
        trace = json.load(f)
    print(f"Loaded {len(trace)} requests")
    
    capacity_bytes = capacity_gb * 1024 * 1024 * 1024
    
    # Baseline (프리페칭 없음) 실행
    print("\n" + "="*60)
    print("Baseline: No Prefetch")
    print("="*60)
    baseline_result = run_prefetch_benchmark(
        trace, algorithm_type, capacity_bytes, NoPrefetch(), '프리페칭 없음'
    )
    baseline_hit_rate = baseline_result['hit_rate']
    
    # 프리페칭 전략 목록
    strategies = [
        (PatientBasedPrefetch(num_previews=5), '환자 기반'),
        (SliceBasedPrefetch(window_size=5), '슬라이스 기반'),
        (TimeBasedPrefetch(num_recent_patients=15, recent_days=5), '시간 기반'),
        (PredictivePrefetch(), '예측 기반'),
    ]
    
    # 의료 특화 프리페칭 설정
    # (실제로는 진료 일정 데이터가 있어야 하지만, 샘플로 일부 환자를 선택)
    medical_strategy = MedicalSpecificPrefetch()
    # 샘플: 상위 10% 환자를 예약 환자로 설정
    patient_ids = list(set([req['key'].split('/')[0] for req in trace]))
    scheduled_patients = patient_ids[:len(patient_ids)//10]
    medical_strategy.set_scheduled_patients(scheduled_patients)
    
    strategies.append((medical_strategy, '의료 특화'))
    
    results = [baseline_result]
    
    # 각 전략 실행
    for strategy, name in strategies:
        print("\n" + "="*60)
        print(f"Strategy: {name}")
        print("="*60)
        
        try:
            result = run_prefetch_benchmark(trace, algorithm_type, capacity_bytes, strategy, name)
            result['baseline_hit_rate'] = baseline_hit_rate
            result['hit_rate_improvement'] = result['hit_rate'] - baseline_hit_rate
            result['hit_rate_improvement_pct'] = result['hit_rate_improvement'] * 100
            results.append(result)
            
            print(f"  Hit rate: {result['hit_rate']*100:.2f}%")
            print(f"  Improvement: {result['hit_rate_improvement_pct']:+.2f}%")
            print(f"  Prefetch overhead: {result.get('prefetch_overhead_mb', 0):.2f} MB")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
    
    return results


def print_prefetch_summary_table(results: List[Dict]):
    """프리페칭 결과 요약 테이블 출력"""
    print("\n" + "="*80)
    print("PREFETCH BENCHMARK SUMMARY")
    print("="*80)
    print(f"{'전략':<15} {'히트율':<10} {'향상':<10} {'오버헤드 (MB)':<15} {'프리페치 히트율':<15}")
    print("-" * 80)
    
    baseline = results[0]
    print(f"{baseline['strategy']:<15} "
          f"{baseline['hit_rate']*100:>7.2f}%  "
          f"{'0.00%':>9}  "
          f"{'0.00':>13}  "
          f"{'N/A':>13}")
    
    for result in results[1:]:
        print(f"{result['strategy']:<15} "
              f"{result['hit_rate']*100:>7.2f}%  "
              f"{result['hit_rate_improvement_pct']:>+7.2f}%  "
              f"{result.get('prefetch_overhead_mb', 0):>11.2f} MB  "
              f"{result.get('prefetch_hit_rate', 0)*100:>11.2f}%  ")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='프리페칭 전략 벤치마크')
    parser.add_argument('--trace-file', type=str, required=True,
                       help='트레이스 파일 경로')
    parser.add_argument('--algorithm', type=str, default='LRU',
                       choices=['LRU', 'SLRU', 'TinyLFU'],
                       help='캐시 알고리즘')
    parser.add_argument('--capacity', type=int, default=100,
                       help='캐시 크기 (GB)')
    parser.add_argument('--output', type=str, default='prefetch_results.json',
                       help='결과 출력 파일')
    
    args = parser.parse_args()
    
    # 벤치마크 실행
    results = benchmark_all_prefetch_strategies(
        args.trace_file, args.algorithm, args.capacity
    )
    
    # 결과 저장
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {args.output}")
    
    # 요약 테이블 출력
    print_prefetch_summary_table(results)


if __name__ == '__main__':
    main()












