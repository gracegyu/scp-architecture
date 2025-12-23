#!/usr/bin/env python3
"""
캐시 알고리즘 벤치마크 실행 스크립트

다양한 알고리즘과 캐시 크기로 시뮬레이션을 실행하고 결과를 수집합니다.
"""

import json
import argparse
import time
from pathlib import Path
from cache_simulator import run_simulation
from generate_trace import MedicalTraceGenerator


def benchmark_all_algorithms(trace_file: str, capacities_gb: list = [50, 100, 200]):
    """
    모든 알고리즘에 대해 벤치마크 실행
    
    Args:
        trace_file: 트레이스 파일 경로
        capacities_gb: 테스트할 캐시 크기 목록 (GB)
    """
    # 트레이스 로드
    print(f"Loading trace from {trace_file}...")
    with open(trace_file, 'r') as f:
        trace = json.load(f)
    print(f"Loaded {len(trace)} requests")
    
    # 알고리즘 목록
    algorithms = [
        {'name': 'LRU', 'params': {}},
        {'name': 'SLRU', 'params': {'probation_ratio': 0.2}},
        {'name': 'TinyLFU', 'params': {'window_ratio': 0.01, 'threshold': 5}},
        {'name': 'Hybrid', 'params': {'window_ratio': 0.01, 'threshold': 5}},
    ]
    
    results = []
    
    for capacity_gb in capacities_gb:
        capacity_bytes = capacity_gb * 1024 * 1024 * 1024
        
        print(f"\n{'='*60}")
        print(f"Capacity: {capacity_gb} GB")
        print(f"{'='*60}")
        
        for algo in algorithms:
            algo_name = algo['name']
            params = algo['params']
            
            print(f"\n--- {algo_name} ---")
            start_time = time.time()
            
            try:
                result = run_simulation(trace, algo_name, capacity_bytes, **params)
                result['capacity_gb'] = capacity_gb
                result['execution_time_sec'] = time.time() - start_time
                results.append(result)
                
                print(f"  Hit rate: {result['hit_rate']*100:.2f}%")
                print(f"  Byte hit rate: {result['byte_hit_rate']*100:.2f}%")
                print(f"  Admission rate: {result['admission_rate']*100:.2f}%")
                print(f"  Execution time: {result['execution_time_sec']:.2f}s")
                
            except Exception as e:
                print(f"  ERROR: {e}")
                continue
    
    return results


def benchmark_with_scenarios():
    """
    다양한 시나리오로 벤치마크 실행
    """
    generator = MedicalTraceGenerator(num_patients=100, num_studies=500, days=7)
    
    scenarios = [
        {'name': 'medical_pattern', 'pattern': 'medical', 'num_requests': 1000000},
        {'name': 'zipf_pattern', 'pattern': 'zipf', 'num_requests': 1000000, 'zipf_param': 1.2},
        {'name': 'onehit_pattern', 'pattern': 'onehit', 'num_requests': 1000000, 'one_hit_ratio': 0.5},
    ]
    
    all_results = {}
    
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"Scenario: {scenario['name']}")
        print(f"{'='*60}")
        
        # 트레이스 생성
        if scenario['pattern'] == 'zipf':
            trace = generator.generate_zipf_trace(
                num_requests=scenario['num_requests'],
                zipf_param=scenario.get('zipf_param', 1.2)
            )
        elif scenario['pattern'] == 'medical':
            trace = generator.generate_medical_pattern_trace(
                num_requests=scenario['num_requests']
            )
        elif scenario['pattern'] == 'onehit':
            trace = generator.generate_one_hit_wonder_trace(
                num_requests=scenario['num_requests'],
                one_hit_ratio=scenario.get('one_hit_ratio', 0.5)
            )
        
        # 트레이스 저장
        trace_file = f"trace_{scenario['name']}.json"
        generator.save_trace(trace, trace_file)
        
        # 벤치마크 실행
        results = benchmark_all_algorithms(trace_file, capacities_gb=[50, 100, 200])
        all_results[scenario['name']] = results
    
    return all_results


def save_results(results: dict, output_file: str):
    """결과를 JSON 파일로 저장"""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")


def print_summary_table(results: dict):
    """결과 요약 테이블 출력"""
    print("\n" + "="*80)
    print("BENCHMARK SUMMARY")
    print("="*80)
    
    for scenario_name, scenario_results in results.items():
        print(f"\nScenario: {scenario_name}")
        print("-" * 80)
        print(f"{'Algorithm':<12} {'Capacity':<10} {'Hit Rate':<10} {'Byte Hit':<12} {'Admit':<10} {'Time':<10}")
        print("-" * 80)
        
        for result in scenario_results:
            print(f"{result['algorithm']:<12} "
                  f"{result['capacity_gb']:>6} GB  "
                  f"{result['hit_rate']*100:>7.2f}%  "
                  f"{result['byte_hit_rate']*100:>9.2f}%  "
                  f"{result['admission_rate']*100:>7.2f}%  "
                  f"{result['execution_time_sec']:>7.2f}s")


def main():
    parser = argparse.ArgumentParser(description='캐시 알고리즘 벤치마크')
    parser.add_argument('--trace-file', type=str, help='트레이스 파일 경로 (기존 파일 사용)')
    parser.add_argument('--scenarios', action='store_true', help='다양한 시나리오로 벤치마크 실행')
    parser.add_argument('--capacities', nargs='+', type=int, default=[50, 100, 200],
                       help='테스트할 캐시 크기 목록 (GB)')
    parser.add_argument('--output', type=str, default='benchmark_results.json',
                       help='결과 출력 파일')
    
    args = parser.parse_args()
    
    if args.scenarios:
        # 여러 시나리오로 벤치마크
        results = benchmark_with_scenarios()
    elif args.trace_file:
        # 기존 트레이스 파일 사용
        results = {'single_scenario': benchmark_all_algorithms(args.trace_file, args.capacities)}
    else:
        # 기본: 의료 패턴으로 벤치마크
        generator = MedicalTraceGenerator(num_patients=100, num_studies=500, days=7)
        trace = generator.generate_medical_pattern_trace(num_requests=1000000)
        trace_file = 'trace_medical.json'
        generator.save_trace(trace, trace_file)
        results = {'medical_pattern': benchmark_all_algorithms(trace_file, args.capacities)}
    
    # 결과 저장
    save_results(results, args.output)
    
    # 요약 테이블 출력
    print_summary_table(results)


if __name__ == '__main__':
    main()














