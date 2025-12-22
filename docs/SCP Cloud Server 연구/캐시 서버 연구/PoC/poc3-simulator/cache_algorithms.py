#!/usr/bin/env python3
"""
캐시 알고리즘 구현

LRU, SLRU, TinyLFU, Window-TinyLFU 등 다양한 캐시 알고리즘을 구현합니다.
"""

import hashlib
from collections import OrderedDict
from typing import Optional, Dict, Tuple


class LRUCache:
    """
    LRU (Least Recently Used) 캐시
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.size_used = 0
    
    def contains(self, key: str) -> bool:
        return key in self.cache
    
    def get(self, key: str) -> Optional[int]:
        if key in self.cache:
            # 최근 사용으로 이동
            size = self.cache.pop(key)
            self.cache[key] = size
            return size
        return None
    
    def put(self, key: str, size: int) -> Optional[Tuple[str, int]]:
        evicted = None
        
        if key in self.cache:
            # 이미 존재하면 크기 업데이트 및 최근 사용으로 이동
            old_size = self.cache.pop(key)
            self.size_used -= old_size
            self.cache[key] = size
            self.size_used += size
            return None
        
        # 용량 초과 시 제거
        while self.size_used + size > self.capacity and self.cache:
            evicted_key, evicted_size = self.cache.popitem(last=False)  # 가장 오래된 항목
            self.size_used -= evicted_size
            evicted = (evicted_key, evicted_size)
        
        # 새 항목 추가
        if self.size_used + size <= self.capacity:
            self.cache[key] = size
            self.size_used += size
        
        return evicted
    
    def on_hit(self, key: str):
        """히트 시 호출 (LRU에서는 최근 사용으로 이동)"""
        if key in self.cache:
            size = self.cache.pop(key)
            self.cache[key] = size
    
    def should_admit(self, key: str) -> bool:
        """입소 허용 여부 (LRU는 항상 허용)"""
        return True
    
    def admit(self, key: str, size: int):
        """항목 입소"""
        self.put(key, size)
    
    def evict(self) -> Optional[Tuple[str, int]]:
        """항목 제거 (가장 오래된 항목)"""
        if self.cache:
            key, size = self.cache.popitem(last=False)
            self.size_used -= size
            return (key, size)
        return None
    
    def is_full(self) -> bool:
        """캐시가 가득 찬지 확인"""
        return self.size_used >= self.capacity * 0.95  # 95% 이상 시 가득 참으로 간주


class SLRUCache:
    """
    Segmented LRU 캐시
    - Probation 세그먼트: 신규 진입, 빠른 제거
    - Protected 세그먼트: 재접근 항목, 오래 유지
    """
    
    def __init__(self, capacity: int, probation_ratio: float = 0.2):
        self.capacity = capacity
        self.probation_size = int(capacity * probation_ratio)
        self.protected_size = capacity - self.probation_size
        
        self.probation = LRUCache(self.probation_size)
        self.protected = LRUCache(self.protected_size)
        
        self.size_used = 0
    
    def contains(self, key: str) -> bool:
        return self.probation.contains(key) or self.protected.contains(key)
    
    def get(self, key: str) -> Optional[int]:
        size = self.protected.get(key)
        if size is not None:
            return size
        
        size = self.probation.get(key)
        if size is not None:
            # Probation에서 재접근 시 Protected로 승격
            self.probation.cache.pop(key)
            self.probation.size_used -= size
            
            # Protected가 가득 차면 가장 오래된 항목을 Probation으로 이동
            if self.protected.is_full():
                evicted = self.protected.evict()
                if evicted:
                    evicted_key, evicted_size = evicted
                    self.probation.put(evicted_key, evicted_size)
            
            self.protected.put(key, size)
            return size
        
        return None
    
    def put(self, key: str, size: int) -> Optional[Tuple[str, int]]:
        evicted = None
        
        if self.protected.contains(key):
            self.protected.put(key, size)
            return None
        
        if self.probation.contains(key):
            # Probation에서 재접근 시 Protected로 승격
            old_size = self.probation.cache.pop(key)
            self.probation.size_used -= old_size
            
            # Protected가 가득 차면 가장 오래된 항목을 Probation으로 이동
            if self.protected.is_full():
                evicted = self.protected.evict()
                if evicted:
                    evicted_key, evicted_size = evicted
                    self.probation.put(evicted_key, evicted_size)
            
            self.protected.put(key, size)
            return None
        
        # 새 항목은 Probation에 추가
        evicted = self.probation.put(key, size)
        return evicted
    
    def on_hit(self, key: str):
        """히트 시 호출"""
        if not self.contains(key):
            return
        
        size = self.get(key)
        if size is None:
            return
        
        # 이미 get()에서 승격 처리됨
    
    def should_admit(self, key: str) -> bool:
        """입소 허용 여부 (SLRU는 항상 허용)"""
        return True
    
    def admit(self, key: str, size: int):
        """항목 입소"""
        self.put(key, size)
    
    def evict(self) -> Optional[Tuple[str, int]]:
        """항목 제거 (Probation에서 먼저)"""
        if self.probation.cache:
            return self.probation.evict()
        if self.protected.cache:
            return self.protected.evict()
        return None
    
    def is_full(self) -> bool:
        """캐시가 가득 찬지 확인"""
        return (self.probation.size_used + self.protected.size_used) >= self.capacity * 0.95


class CountMinSketch:
    """
    Count-Min Sketch: 빈도 추정을 위한 확률적 자료구조
    """
    
    def __init__(self, width: int = 1000000, depth: int = 5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
    
    def _hash(self, key: str, seed: int) -> int:
        """해시 함수"""
        h = hashlib.md5(f"{key}:{seed}".encode()).hexdigest()
        return int(h, 16) % self.width
    
    def increment(self, key: str):
        """키의 빈도 증가"""
        for i in range(self.depth):
            j = self._hash(key, i)
            self.table[i][j] += 1
    
    def estimate(self, key: str) -> int:
        """키의 빈도 추정 (최소값, 보수적 추정)"""
        estimates = []
        for i in range(self.depth):
            j = self._hash(key, i)
            estimates.append(self.table[i][j])
        return min(estimates)


class WindowTinyLFU:
    """
    Window-TinyLFU 캐시
    - Window Cache: 최근 항목 임시 보관
    - Main Cache: 빈도 기반 유지 (SLRU)
    - Count-Min Sketch: 빈도 추정
    """
    
    def __init__(self, capacity: int, window_ratio: float = 0.01, threshold: int = 5):
        self.capacity = capacity
        self.window_size = int(capacity * window_ratio)
        self.main_size = capacity - self.window_size
        
        self.window = LRUCache(self.window_size)
        self.main = SLRUCache(self.main_size)
        self.sketch = CountMinSketch()
        self.threshold = threshold
    
    def contains(self, key: str) -> bool:
        return self.window.contains(key) or self.main.contains(key)
    
    def get(self, key: str) -> Optional[int]:
        # Window에서 먼저 확인
        size = self.window.get(key)
        if size is not None:
            return size
        
        # Main에서 확인
        size = self.main.get(key)
        if size is not None:
            return size
        
        return None
    
    def put(self, key: str, size: int) -> Optional[Tuple[str, int]]:
        # 빈도 증가
        self.sketch.increment(key)
        
        if self.window.contains(key):
            self.window.put(key, size)
            return None
        
        if self.main.contains(key):
            self.main.put(key, size)
            return None
        
        # MISS: 입소 필터 적용
        freq = self.sketch.estimate(key)
        if freq >= self.threshold:
            # Window에 추가
            evicted = self.window.put(key, size)
            
            # Window가 가득 차면 가장 오래된 항목을 Main으로 이동
            if evicted and self.window.is_full():
                evicted_key, evicted_size = evicted
                # Main에 추가 시도
                main_evicted = self.main.put(evicted_key, evicted_size)
                # Main도 가득 차면 제거
                return main_evicted
        
        return None
    
    def on_hit(self, key: str):
        """히트 시 호출"""
        if not self.contains(key):
            return
        
        # 빈도 증가
        self.sketch.increment(key)
        
        # Window에서 히트
        if self.window.contains(key):
            self.window.on_hit(key)
            return
        
        # Main에서 히트
        if self.main.contains(key):
            self.main.on_hit(key)
            return
    
    def should_admit(self, key: str) -> bool:
        """입소 허용 여부 (빈도 기반)"""
        freq = self.sketch.estimate(key)
        return freq >= self.threshold
    
    def admit(self, key: str, size: int):
        """항목 입소"""
        self.put(key, size)
    
    def evict(self) -> Optional[Tuple[str, int]]:
        """항목 제거"""
        if self.window.cache:
            return self.window.evict()
        if self.main.probation.cache:
            return self.main.evict()
        return None
    
    def is_full(self) -> bool:
        """캐시가 가득 찬지 확인"""
        return (self.window.size_used + self.main.size_used) >= self.capacity * 0.95












