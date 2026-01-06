Engineering One Pager

**Project Name**: PoC-08: 멀티 플랫폼 지원 검증

**Date**: 2026년 1월 6일

**Submitter Info**: Raymond

**Project Description**: SCP Cloud Report 시스템이 Web App, Desktop App, Mobile App 등 다양한 플랫폼에서 동일한 기능과 사용자 경험을 제공할 수 있는지 검증합니다. 각 플랫폼별 기술적 제약사항을 분석하고, WebView 기반 접근법의 성능과 한계를 확인하여 최적의 멀티 플랫폼 전략을 수립합니다.

**Business and Marketing Justification**:

- **시장 접근성 확대**: 다양한 디바이스에서 접근 가능한 서비스로 사용자 저변 확대
- **사용자 편의성**: 언제 어디서나 동일한 리포트 편집 경험 제공
- **디바이스 트렌드 대응**: 태블릿, 모바일 기반 의료진 업무 환경 변화 대응
- **투자 효율성**: 하나의 코드베이스로 다중 플랫폼 지원
- **경쟁 우위**: Desktop 전용 경쟁 제품 대비 차별화 요소
- **미래 대응**: IoT, AR/VR 등 신기술 플랫폼 확장 기반 마련

**Risk Assessment**:

- **높은 리스크**:
  - WebView 성능 한계로 인한 Desktop 수준 기능 구현 어려움
  - 플랫폼별 파일 시스템 접근 방식 차이로 인한 기능 제약
- **중간 리스크**:
  - 모바일에서 복잡한 리포트 편집 시 UX 저하
  - 플랫폼별 브라우저 엔진 차이 (Chromium vs WebKit vs Gecko)
  - 메모리 제약이 있는 모바일 디바이스 성능 이슈
- **저위험**:
  - WebView 기술 자체는 검증된 안정적 기술
- **완화 방안**:
  - 플랫폼별 기능 차등 제공 (Progressive Enhancement)
  - 핵심 기능 우선 구현 후 점진적 확장
  - 플랫폼별 성능 최적화 적용

**Resource and Scheduling Details**:

- **기간**: 3주 (Week 9-11)
- **인력**:
  - Raymond (멀티플랫폼 개발자, UX/UI 디자이너, 성능 엔지니어 역할 겸임)
    - Web App 기준 기능 구현
    - Desktop App (Electron/WebView) 래핑
    - Mobile App WebView 통합
    - 플랫폼별 성능 최적화
- **환경**:
  - Windows, macOS, Linux 데스크톱 환경
  - iOS, Android 모바일 테스트 디바이스
  - 다양한 화면 크기 및 해상도 테스트

**Technical Description**:

**플랫폼별 구현 전략**:

**1. Web App (기준 플랫폼)**:

- React 기반 SPA (Single Page Application)
- PWA (Progressive Web App) 지원으로 오프라인 기능
- 모든 기능 완전 구현
- 브라우저 네이티브 기능 최대 활용

**2. Desktop App**: **Electron 방식**:

- Web App을 Electron으로 패키징
- 파일 시스템 직접 접근 가능
- 네이티브 메뉴, 단축키 지원
- 단점: 번들 크기 큰 편, 메모리 사용량 높음

**WebView 방식** (권장):

- 시스템 브라우저 엔진 활용 (Edge WebView2, Safari WebKit)
- 가벼운 네이티브 래퍼
- 자동 업데이트 가능
- 플랫폼별 네이티브 연동

**3. Mobile App**: **WebView 임베딩**:

- iOS: WKWebView 활용
- Android: Chrome Custom Tabs 또는 WebView
- 터치 제스처 최적화
- 모바일 UI 패턴 적용

**기존 Desktop 제품 기능 분석**:

**E3 RC Report 기능 중 플랫폼별 지원 가능성**:

- **파일 I/O**: Desktop 완전지원, Web 제한적, Mobile 제한적
- **인쇄 기능**: Desktop DICOM Print, Web 일반 인쇄, Mobile 제한적
- **드래그 앤 드롭**: 모든 플랫폼 지원 (터치는 대체 인터랙션)
- **키보드 단축키**: Desktop/Web 완전, Mobile 가상키보드 제약
- **클립보드**: Desktop 완전, Web/Mobile 제한적

**플랫폼별 기능 매트릭스**:

```typescript
interface PlatformSupport {
  feature: string
  web: 'full' | 'partial' | 'none'
  desktop: 'full' | 'partial' | 'none'
  mobile: 'full' | 'partial' | 'none'
  alternative?: string
}
```

**성능 최적화 전략**:

**Web App**:

- 코드 스플리팅으로 초기 로딩 최적화
- 서비스 워커로 캐싱 및 오프라인 지원
- Virtual Scrolling으로 대용량 리포트 처리

**Desktop App**:

- 네이티브 파일 시스템 직접 접근
- 시스템 리소스 효율적 활용
- 백그라운드 프로세스 활용

**Mobile App**:

- 터치 친화적 UI 패턴
- 메모리 사용량 최적화
- 배터리 효율성 고려

**테스트 시나리오**:

**1. 기능 동등성 테스트**:

- 동일한 리포트를 각 플랫폼에서 편집
- 저장/로드 결과 비교
- 출력 품질 (PDF, 인쇄) 비교

**2. 성능 벤치마크**:

- 앱 시작 시간: Web < 3초, Desktop < 5초, Mobile < 5초
- 리포트 로딩: 100개 Element 리포트 < 2초
- 편집 반응성: 터치/마우스 입력 후 100ms 이내 반영

**3. 사용성 테스트**:

- 플랫폼별 인터랙션 패턴 적용 확인
- 화면 크기별 UI 적응성
- 키보드/터치 접근성

**플랫폼별 제약사항 및 대응**:

**Web App**:

- 파일 시스템 제약 → File API, Drag & Drop API 활용
- 인쇄 제약 → 브라우저 인쇄 API + PDF 다운로드

**Desktop App**:

- 보안 정책 → 코드 서명, 신뢰할 수 있는 게시자 등록
- 자동 업데이트 → Squirrel (Windows), Sparkle (macOS)

**Mobile App**:

- 화면 크기 → 반응형 디자인, 모바일 전용 UI
- 성능 제약 → 기능 간소화, 지연 로딩

**예상 결과**:

- Web: 100% 기능 지원 (기준 플랫폼)
- Desktop: 95% 기능 지원 (파일 I/O, 고급 인쇄 추가)
- Mobile: 80% 기능 지원 (편집 중심, 복잡한 기능 제외)

**산출물**:

1. **플랫폼별 기능 지원 매트릭스**: 상세 호환성 표
2. **WebView 통합 가이드**: 각 플랫폼별 구현 방법
3. **성능 최적화 가이드**: 플랫폼별 최적화 방안
4. **UX 가이드라인**: 플랫폼별 사용자 인터페이스 설계
5. **배포 전략서**: 각 플랫폼별 배포 및 업데이트 방안
6. **프로토타입 앱**: 각 플랫폼별 기본 기능 구현 예제

**다음 단계**: 플랫폼별 최적화된 아키텍처를 기반으로 PoC-09(성능 최적화) 진행

