#!/usr/bin/env python3
"""
프리페칭 전략 구현

다양한 프리페칭 전략을 구현하고 효과를 측정합니다.
"""

import random
from typing import List, Dict, Set, Optional
from datetime import datetime, timedelta


class PrefetchStrategy:
    """
    프리페칭 전략 기본 클래스
    """
    
    def __init__(self, name: str):
        self.name = name
        self.stats = {
            'prefetch_count': 0,
            'prefetch_hit_count': 0,
            'prefetch_bytes': 0,
            'prefetch_overhead': 0
        }
    
    def should_prefetch(self, current_request: Dict, cache_simulator) -> List[str]:
        """
        현재 요청에 대해 프리페칭할 키 목록 반환
        
        Returns:
            프리페칭할 키 리스트
        """
        return []
    
    def prefetch(self, keys: List[str], cache_simulator, trace_data: Dict):
        """
        키 목록을 프리페칭하여 캐시에 추가
        
        Args:
            keys: 프리페칭할 키 리스트
            cache_simulator: 캐시 시뮬레이터 인스턴스
            trace_data: 트레이스 데이터 (키-크기 매핑 등)
        """
        for key in keys:
            if key in trace_data:
                size = trace_data[key]
                # 프리페칭 오버헤드 계산 (대역폭 사용)
                self.stats['prefetch_overhead'] += size
                self.stats['prefetch_bytes'] += size
                self.stats['prefetch_count'] += 1
                
                # 캐시에 추가 (힛으로 카운트하지 않음)
                cache_simulator.algorithm.admit(key, size)
                
                # 이후 실제 요청에서 힛되는지 확인을 위해 기록
                cache_simulator.prefetched_keys.add(key)
    
    def get_stats(self) -> Dict:
        """통계 반환"""
        return {
            'name': self.name,
            'prefetch_count': self.stats['prefetch_count'],
            'prefetch_bytes': self.stats['prefetch_bytes'],
            'prefetch_overhead_mb': self.stats['prefetch_overhead'] / (1024 * 1024),
            'prefetch_hit_rate': (self.stats['prefetch_hit_count'] / self.stats['prefetch_count'] 
                                 if self.stats['prefetch_count'] > 0 else 0.0)
        }
    
    def reset_stats(self):
        """통계 초기화"""
        self.stats = {
            'prefetch_count': 0,
            'prefetch_hit_count': 0,
            'prefetch_bytes': 0,
            'prefetch_overhead': 0
        }


class PatientBasedPrefetch(PrefetchStrategy):
    """
    전략 1: 환자 기반 프리페칭
    - 환자 진입 시 모든 썸네일 프리페치
    - 대표 프리뷰 N개 프리페치
    """
    
    def __init__(self, num_previews: int = 5):
        super().__init__('환자 기반 프리페칭')
        self.num_previews = num_previews
        self.processed_patients: Set[str] = set()
    
    def should_prefetch(self, current_request: Dict, cache_simulator) -> List[str]:
        """
        환자 ID를 추출하여 해당 환자의 썸네일과 프리뷰를 프리페칭
        """
        key = current_request['key']
        parts = key.split('/')
        
        if len(parts) < 3:
            return []
        
        # patient_id/study_id/resource_type 형식 가정
        patient_id = parts[0]
        
        # 이미 처리한 환자는 스킵
        if patient_id in self.processed_patients:
            return []
        
        prefetch_keys = []
        
        # 해당 환자의 모든 썸네일과 프리뷰 찾기
        # 실제로는 trace_data에서 찾아야 하지만, 여기서는 패턴 기반으로 생성
        for study_key in cache_simulator.trace_keys_by_patient.get(patient_id, []):
            study_parts = study_key.split('/')
            if len(study_parts) >= 2:
                study_id = '/'.join(study_parts[:-1])
                # 썸네일 프리페치
                prefetch_keys.append(f"{study_id}/thumb")
                # 프리뷰 N개만 프리페치
                if len([k for k in prefetch_keys if '/preview' in k]) < self.num_previews:
                    prefetch_keys.append(f"{study_id}/preview")
        
        if prefetch_keys:
            self.processed_patients.add(patient_id)
        
        return prefetch_keys


class SliceBasedPrefetch(PrefetchStrategy):
    """
    전략 2: 슬라이스 기반 프리페칭
    - 슬라이스 i 조회 시 주변 i±k 프리페치
    """
    
    def __init__(self, window_size: int = 5):
        super().__init__('슬라이스 기반 프리페칭')
        self.window_size = window_size
        self.last_slice_index: Dict[str, int] = {}
    
    def should_prefetch(self, current_request: Dict, cache_simulator) -> List[str]:
        """
        슬라이스 요청 시 주변 슬라이스 프리페치
        """
        key = current_request['key']
        
        if '/slice' not in key:
            return []
        
        # 슬라이스 인덱스 추출 시도
        # key 형식: study_id/slice_123 또는 study_id/slice?index=123
        parts = key.split('/')
        study_base = '/'.join(parts[:-1])
        
        # 슬라이스 인덱스 파싱 (간단한 구현)
        slice_part = parts[-1]
        try:
            # slice_123 형식 가정
            if 'slice_' in slice_part:
                current_index = int(slice_part.split('_')[1])
            elif 'slice' in slice_part:
                # slice?index=123 형식
                current_index = int(slice_part.split('=')[1])
            else:
                return []
        except (ValueError, IndexError):
            return []
        
        prefetch_keys = []
        
        # 주변 슬라이스 프리페치
        for offset in range(-self.window_size, self.window_size + 1):
            if offset == 0:
                continue  # 현재 슬라이스는 이미 요청됨
            
            target_index = current_index + offset
            if target_index >= 0:
                prefetch_keys.append(f"{study_base}/slice_{target_index}")
        
        return prefetch_keys


class TimeBasedPrefetch(PrefetchStrategy):
    """
    전략 3: 시간 기반 프리페칭
    - 최근 N명 환자 썸네일
    - 최근 M일 스터디 프리뷰
    """
    
    def __init__(self, num_recent_patients: int = 15, recent_days: int = 5):
        super().__init__('시간 기반 프리페칭')
        self.num_recent_patients = num_recent_patients
        self.recent_days = recent_days
        self.recent_patients: List[str] = []
        self.recent_studies: List[str] = []
        self.last_access_time: Dict[str, int] = {}
        self.current_time = 0
    
    def should_prefetch(self, current_request: Dict, cache_simulator) -> List[str]:
        """
        최근 접근한 환자/스터디 기반 프리페치
        """
        key = current_request['key']
        timestamp = current_request.get('timestamp', self.current_time)
        self.current_time = timestamp
        
        parts = key.split('/')
        if len(parts) < 2:
            return []
        
        patient_id = parts[0]
        
        # 최근 환자 목록 업데이트
        if patient_id not in self.recent_patients:
            self.recent_patients.append(patient_id)
            if len(self.recent_patients) > self.num_recent_patients:
                self.recent_patients.pop(0)
        
        # 최근 접근 시간 업데이트
        self.last_access_time[key] = timestamp
        
        # 프리페칭: 최근 환자의 썸네일
        prefetch_keys = []
        cutoff_time = timestamp - (self.recent_days * 24 * 60 * 60 * 1000)  # 일->밀리초 변환 간소화
        
        for recent_patient in self.recent_patients[-self.num_recent_patients:]:
            # 해당 환자의 최근 스터디 썸네일 프리페치
            if recent_patient in cache_simulator.trace_keys_by_patient:
                for study_key in cache_simulator.trace_keys_by_patient[recent_patient]:
                    if '/thumb' in study_key and self.last_access_time.get(study_key, 0) >= cutoff_time:
                        prefetch_keys.append(study_key)
        
        return prefetch_keys[:50]  # 최대 50개로 제한


class PredictivePrefetch(PrefetchStrategy):
    """
    전략 4: 예측 기반 프리페칭
    - 이전 접근 패턴 기반 (환자 A 후 B 조회 확률)
    """
    
    def __init__(self):
        super().__init__('예측 기반 프리페칭')
        self.transition_prob: Dict[str, Dict[str, int]] = {}  # {current_key: {next_key: count}}
        self.last_key: Optional[str] = None
    
    def should_prefetch(self, current_request: Dict, cache_simulator) -> List[str]:
        """
        이전 접근 패턴을 기반으로 다음 요청 예측
        """
        key = current_request['key']
        prefetch_keys = []
        
        # 이전 키에서 현재 키로의 전환 기록
        if self.last_key:
            if self.last_key not in self.transition_prob:
                self.transition_prob[self.last_key] = {}
            if key not in self.transition_prob[self.last_key]:
                self.transition_prob[self.last_key][key] = 0
            self.transition_prob[self.last_key][key] += 1
        
        # 현재 키 다음에 자주 오는 키들을 프리페치
        if key in self.transition_prob:
            transitions = self.transition_prob[key]
            # 빈도 순으로 정렬하여 상위 3개만 프리페치
            sorted_transitions = sorted(transitions.items(), key=lambda x: x[1], reverse=True)
            for next_key, count in sorted_transitions[:3]:
                if count >= 2:  # 최소 2회 이상 등장한 경우만
                    prefetch_keys.append(next_key)
        
        self.last_key = key
        return prefetch_keys


class MedicalSpecificPrefetch(PrefetchStrategy):
    """
    전략 5: 의료 특화 프리페칭
    - 진료 일정 기반: 당일 예약 환자 전체 데이터 프리페치
    - 진료진별 패턴: 의사별 자주 보는 환자 유형 프리페치
    - 응급 상황 대비: 응급실 환자 데이터 항상 캐시 유지
    """
    
    def __init__(self):
        super().__init__('의료 특화 프리페칭')
        self.scheduled_patients: Set[str] = set()  # 당일 예약 환자
        self.emergency_patients: Set[str] = set()  # 응급 환자
        self.doctor_patient_pref: Dict[str, Set[str]] = {}  # 의사별 선호 환자
    
    def set_scheduled_patients(self, patient_ids: List[str]):
        """당일 예약 환자 설정"""
        self.scheduled_patients = set(patient_ids)
    
    def set_emergency_patients(self, patient_ids: List[str]):
        """응급 환자 설정"""
        self.emergency_patients = set(patient_ids)
    
    def should_prefetch(self, current_request: Dict, cache_simulator) -> List[str]:
        """
        의료 특화 프리페칭 로직
        """
        key = current_request['key']
        parts = key.split('/')
        
        if len(parts) < 1:
            return []
        
        patient_id = parts[0]
        prefetch_keys = []
        
        # 응급 환자: 모든 데이터 프리페치
        if patient_id in self.emergency_patients:
            if patient_id in cache_simulator.trace_keys_by_patient:
                prefetch_keys.extend(cache_simulator.trace_keys_by_patient[patient_id])
        
        # 당일 예약 환자: 썸네일과 프리뷰 프리페치
        elif patient_id in self.scheduled_patients:
            if patient_id in cache_simulator.trace_keys_by_patient:
                for study_key in cache_simulator.trace_keys_by_patient[patient_id]:
                    if '/thumb' in study_key or '/preview' in study_key:
                        prefetch_keys.append(study_key)
        
        return prefetch_keys


class NoPrefetch(PrefetchStrategy):
    """
    프리페칭 없음 (Baseline)
    """
    
    def __init__(self):
        super().__init__('프리페칭 없음')
    
    def should_prefetch(self, current_request: Dict, cache_simulator) -> List[str]:
        return []


