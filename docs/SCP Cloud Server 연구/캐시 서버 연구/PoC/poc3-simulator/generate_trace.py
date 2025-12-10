#!/usr/bin/env python3
"""
합성 접근 패턴 데이터 생성기

의료 환경에 맞는 Zipf 분포 및 의료 특화 패턴을 생성합니다.
"""

import random
import numpy as np
from scipy.stats import zipf
from datetime import datetime, timedelta
import json
import argparse


class MedicalTraceGenerator:
    """
    의료 환경 접근 패턴 생성기
    """
    
    def __init__(self, num_patients=100, num_studies=500, days=7):
        self.num_patients = num_patients
        self.num_studies = num_studies
        self.days = days
        
        # 환자 ID 생성
        self.patients = [f"patient_{i:04d}" for i in range(num_patients)]
        self.studies = {}
        
        # 환자별 스터디 생성
        for patient in self.patients:
            num_patient_studies = random.randint(1, 10)
            patient_studies = [f"{patient}/study_{j:03d}" for j in range(num_patient_studies)]
            self.studies[patient] = patient_studies
        
        # 리소스 타입 및 크기
        self.resource_types = {
            'thumb': {'size_range': (10, 50), 'ttl_days': 30},  # KB
            'preview': {'size_range': (100, 500), 'ttl_days': 7},  # KB
            'slice': {'size_range': (50, 200), 'ttl_days': 1},  # KB
            'meta': {'size_range': (1, 5), 'ttl_days': 0.0035}  # KB, 5분
        }
        
    def generate_zipf_trace(self, num_requests=1000000, zipf_param=1.2):
        """
        Zipf 분포 기반 접근 패턴 생성
        """
        # 모든 가능한 키 생성
        all_keys = []
        for patient, studies in self.studies.items():
            for study in studies:
                for res_type in self.resource_types:
                    all_keys.append(f"{study}/{res_type}")
        
        # Zipf 분포로 순위 생성
        zipf_dist = zipf(zipf_param)
        num_items = len(all_keys)
        
        # 순위별 확률
        ranks = np.arange(1, num_items + 1)
        probabilities = ranks ** (-zipf_param)
        probabilities = probabilities / probabilities.sum()
        
        trace = []
        for i in range(num_requests):
            # Zipf 분포로 키 선택
            key_idx = np.random.choice(num_items, p=probabilities)
            key = all_keys[key_idx]
            
            # 리소스 타입 추출
            res_type = key.split('/')[-1]
            size_kb = random.randint(
                self.resource_types[res_type]['size_range'][0],
                self.resource_types[res_type]['size_range'][1]
            )
            size_bytes = size_kb * 1024
            
            trace.append({
                'key': key,
                'size': size_bytes,
                'timestamp': i  # 순서 번호
            })
        
        return trace
    
    def generate_medical_pattern_trace(self, num_requests=1000000):
        """
        의료 특화 패턴 생성
        - Temporal Locality: 최근 진료 환자 집중
        - Spatial Locality: 동일 환자의 여러 스터디 연속 조회
        - Hot/Warm/Cold 분포
        """
        trace = []
        
        # Hot/Warm/Cold 분류
        hot_patients = self.patients[:int(self.num_patients * 0.2)]  # 상위 20%
        warm_patients = self.patients[int(self.num_patients * 0.2):int(self.num_patients * 0.5)]  # 20-50%
        cold_patients = self.patients[int(self.num_patients * 0.5):]  # 하위 50%
        
        current_patient = None
        patient_study_index = {}
        
        for i in range(num_requests):
            # 80% 확률로 Temporal Locality (최근 접근 환자 재접근)
            if current_patient and random.random() < 0.8:
                patient = current_patient
            else:
                # Hot 60%, Warm 30%, Cold 10% 분포
                rand = random.random()
                if rand < 0.6:
                    patient = random.choice(hot_patients)
                elif rand < 0.9:
                    patient = random.choice(warm_patients)
                else:
                    patient = random.choice(cold_patients)
                current_patient = patient
            
            # Spatial Locality: 동일 환자의 여러 스터디 연속 조회
            if patient not in patient_study_index:
                patient_study_index[patient] = 0
            
            studies = self.studies[patient]
            
            # 70% 확률로 현재 스터디 또는 인접 스터디
            if random.random() < 0.7 and patient_study_index[patient] < len(studies):
                study_idx = patient_study_index[patient]
                # 인접 스터디 조회
                if random.random() < 0.5 and study_idx + 1 < len(studies):
                    study_idx += 1
                study = studies[study_idx]
                patient_study_index[patient] = study_idx
            else:
                study = random.choice(studies)
            
            # 리소스 타입 선택 (썸네일 50%, 프리뷰 30%, 슬라이스 15%, 메타 5%)
            res_type_rand = random.random()
            if res_type_rand < 0.5:
                res_type = 'thumb'
            elif res_type_rand < 0.8:
                res_type = 'preview'
            elif res_type_rand < 0.95:
                res_type = 'slice'
            else:
                res_type = 'meta'
            
            key = f"{study}/{res_type}"
            size_kb = random.randint(
                self.resource_types[res_type]['size_range'][0],
                self.resource_types[res_type]['size_range'][1]
            )
            size_bytes = size_kb * 1024
            
            trace.append({
                'key': key,
                'size': size_bytes,
                'timestamp': i
            })
        
        return trace
    
    def generate_one_hit_wonder_trace(self, num_requests=1000000, one_hit_ratio=0.5):
        """
        One-hit-wonder 테스트용 트레이스
        - 일정 비율의 항목이 1회만 접근됨
        """
        # 모든 가능한 키
        all_keys = []
        for patient, studies in self.studies.items():
            for study in studies:
                for res_type in self.resource_types:
                    all_keys.append(f"{study}/{res_type}")
        
        # One-hit 항목 선택
        num_one_hit = int(len(all_keys) * one_hit_ratio)
        one_hit_keys = set(random.sample(all_keys, num_one_hit))
        regular_keys = [k for k in all_keys if k not in one_hit_keys]
        
        trace = []
        one_hit_used = set()
        
        for i in range(num_requests):
            rand = random.random()
            
            if rand < one_hit_ratio and one_hit_keys:
                # One-hit 항목 선택 (1회만)
                key = random.choice(list(one_hit_keys - one_hit_used))
                one_hit_used.add(key)
                if len(one_hit_used) == len(one_hit_keys):
                    # 모두 사용했으면 다시 초기화
                    one_hit_used.clear()
            else:
                # 일반 항목 (반복 접근)
                key = random.choice(regular_keys)
            
            # 리소스 타입 추출
            res_type = key.split('/')[-1]
            size_kb = random.randint(
                self.resource_types[res_type]['size_range'][0],
                self.resource_types[res_type]['size_range'][1]
            )
            size_bytes = size_kb * 1024
            
            trace.append({
                'key': key,
                'size': size_bytes,
                'timestamp': i
            })
        
        return trace
    
    def save_trace(self, trace, filename):
        """트레이스를 JSON 파일로 저장"""
        with open(filename, 'w') as f:
            json.dump(trace, f, indent=2)
        print(f"Trace saved to {filename}: {len(trace)} requests")


def main():
    parser = argparse.ArgumentParser(description='의료 환경 접근 패턴 생성기')
    parser.add_argument('--pattern', choices=['zipf', 'medical', 'onehit'], 
                       default='medical', help='패턴 타입')
    parser.add_argument('--num-requests', type=int, default=1000000,
                       help='요청 개수')
    parser.add_argument('--num-patients', type=int, default=100,
                       help='환자 수')
    parser.add_argument('--num-studies', type=int, default=500,
                       help='전체 스터디 수')
    parser.add_argument('--days', type=int, default=7,
                       help='기간 (일)')
    parser.add_argument('--output', type=str, default='trace.json',
                       help='출력 파일')
    parser.add_argument('--zipf-param', type=float, default=1.2,
                       help='Zipf 분포 파라미터')
    parser.add_argument('--one-hit-ratio', type=float, default=0.5,
                       help='One-hit-wonder 비율')
    
    args = parser.parse_args()
    
    generator = MedicalTraceGenerator(
        num_patients=args.num_patients,
        num_studies=args.num_studies,
        days=args.days
    )
    
    if args.pattern == 'zipf':
        trace = generator.generate_zipf_trace(
            num_requests=args.num_requests,
            zipf_param=args.zipf_param
        )
    elif args.pattern == 'medical':
        trace = generator.generate_medical_pattern_trace(
            num_requests=args.num_requests
        )
    elif args.pattern == 'onehit':
        trace = generator.generate_one_hit_wonder_trace(
            num_requests=args.num_requests,
            one_hit_ratio=args.one_hit_ratio
        )
    
    generator.save_trace(trace, args.output)


if __name__ == '__main__':
    main()






