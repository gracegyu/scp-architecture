# PoC-09 결과 보고서: 멀티 플랫폼 지원 검증

## 요약

- **목표**: SCP Cloud Report가 Web, Desktop, Mobile에서 동일한 기능·경험을 제공할 수 있는지 검증
- **기준 플랫폼**: Web App (TypeScript React SPA) — 100% 기능, 모든 개발·검증의 기준
- **Desktop**: WebView/Electron 래핑 — Web 동일 기능 + 네이티브 파일/인쇄, 95% 수준 목표
- **Mobile**: WebView 임베딩 — 편집 중심, 터치 최적화, 80% 수준 목표 (Progressive Enhancement)
- **전략**: 단일 코드베이스(Web) + 플랫폼별 래퍼, 기능 차등 제공으로 제약 대응
- **산출물**: 플랫폼별 기능 매트릭스, WebView 통합 가이드, 성능 목표, UX 가이드라인

---

## 1. 개요

### 1.1 검증 목표

SCP Cloud Report 시스템이 **Web App**, **Desktop App**, **Mobile App**에서 동일한 핵심 기능과 사용자 경험을 제공할 수 있는지 검증합니다. 각 플랫폼의 기술적 제약을 분석하고, **Web 우선(Web-first)** 전략과 WebView 기반 래핑의 타당성·한계를 확인하여 멀티 플랫폼 전략을 수립합니다.

**핵심 질문**:

- Web을 기준으로 할 때 Desktop/Mobile에서 얼마나 동일한 경험을 보장할 수 있는가?
- WebView 기반 접근의 성능·파일 시스템·인쇄 등 한계는 무엇인가?
- 플랫폼별로 어떤 기능을 차등 제공(Progressive Enhancement)할 것인가?

### 1.2 전제 조건

**내부 Cloud 서비스 전용**:

- SCP Cloud가 주 사용처이며, 멀티 플랫폼은 **동일 SCP Cloud 서비스에 대한 접근 경로 확대**가 목적
- Web이 1차 플랫폼, Desktop/Mobile은 필요 시 WebView/Electron으로 확장

**단일 코드베이스**:

- PoC-08에서 선정한 Shared Library(@ewoosoft/scp-report-library)는 Web(React) 기준
- Desktop/Mobile은 동일 Web 앱을 래핑하여 재사용

### 1.3 선행 PoC 반영

| PoC    | 결정 사항                    | 멀티 플랫폼 영향                                |
| ------ | ---------------------------- | ----------------------------------------------- |
| PoC-04 | HTML DOM + SVG, React        | 모든 플랫폼에서 동일 렌더링 (WebView 동일 엔진) |
| PoC-05 | React-Spring, html2canvas 등 | Web 기준 번들, 플랫폼별 로딩 전략 필요          |
| PoC-08 | Shared Library (NPM)         | Web 빌드 결과를 Desktop/Mobile에서 재사용       |

### 1.4 평가 기준

**1. 기능 동등성**: 동일 리포트 편집·저장·Export 결과 일치 **2. 성능**: 플랫폼별 로딩 시간, 반응성, 메모리 **3. 사용성**: 플랫폼별 입력 방식(마우스/키보드/터치)에 맞는 UX **4. 유지보수성**: 단일 코드베이스 유지 가능 여부

---

## 2. 플랫폼별 구현 전략

### 2.1 Web App (기준 플랫폼)

**역할**: 모든 기능의 기준. Desktop/Mobile은 Web 빌드를 그대로 또는 최소 수정으로 사용.

**기술 스택**:

- TypeScript, React (PoC-14 Element 렌더링 엔진)
- SPA, 브라우저 표준 API만 사용 (File API, Drag & Drop, Print)
- PWA(Progressive Web App) 선택 적용: 오프라인 캐시, 설치 가능

**특징**:

- **파일 I/O**: File API, Drag & Drop, 사용자 선택 파일만 접근
- **인쇄**: window.print(), PDF는 브라우저 인쇄 또는 jsPDF 등 클라이언트 생성
- **저장**: 서버 API 호출 (SCP Cloud 백엔드), 로컬 파일 직접 저장 불가
- **단축키**: 브라우저 기본 + 커스텀 키 바인딩

**성능 목표**:

- 초기 로딩(첫 화면): 3초 이내
- 리포트 로딩(50개 Element): 2초 이내
- 편집 반응성(드래그/리사이즈): 100ms 이내 반영

**제약 및 대응**: | 제약 | 대응 | | ----------------- | ----------------------------------------- | | 로컬 파일 직접 접근 불가 | 업로드/다운로드, Cloud 저장만 사용 | | 인쇄 품질 플랫폼 의존 | PoC-10에서 고해상도 PDF/인쇄 전략 수립 | | 오프라인 제한 | PWA 캐시로 뷰어/간단 편집 가능 범위 검토 |

---

### 2.2 Desktop App

**역할**: Web과 동일한 기능 + 네이티브 파일 접근·시스템 인쇄 등 보완.

**권장 방식: WebView 기반 래퍼**

- **Windows**: WebView2 (Edge Chromium)
- **macOS**: WKWebView 또는 Electron
- **Linux**: WebKitGTK 또는 Electron

Web 앱을 그대로 로드하고, 플랫폼별 네이티브 API만 브리지로 제공.

**구조**:

```
Desktop App
├── Native Shell (최소)
│   ├── WebView 컨테이너
│   ├── 메뉴/단축키
│   └── 파일 열기/저장/인쇄 대화상자
└── Web App (동일 URL 또는 로컬 번들)
```

**Electron 대안**:

- **기존 Web 소스와의 관계**: 기존 Web 리포트 소스(React/TypeScript)는 그대로 재사용한다. Electron은 Renderer 프로세스에서 해당 Web 앱을 로드하고, Main 프로세스에 메뉴·파일 대화상자·인쇄·단축키 등 데스크톱 셸만 추가하면 된다. 즉 새로 개발하는 부분은 최소한의 셸 코드뿐이며, 리포트 편집 로직은 Web과 완전 호환된다.
- 장점: 크로스 플랫폼 통일, Node 연동 쉬움, 파일/인쇄 제어 용이
- 단점: 번들 크기 큼(약 150MB 수준), 메모리 사용 많음
- 활용: 네이티브 파일 저장·로드·DICOM Print 등이 필수일 때 검토

**Desktop 전용 보완 기능**: | 기능 | Web | Desktop (WebView) | | -------------- | ---------- | ---------------------- | | 로컬 파일 열기 | 업로드만 | 네이티브 파일 선택/열기 | | 로컬 파일 저장 | 다운로드만 | 네이티브 저장 대화상자 | | 시스템 인쇄 | 브라우저 인쇄 | 네이티브 인쇄 대화상자 | | 단축키 | 브라우저 제약 | 앱 전역 단축키 |

**성능 목표**:

- 앱 시작(WebView 준비): 5초 이내
- Web과 동일: 로딩 2초, 반응성 100ms

**제약 및 대응**: | 제약 | 대응 | | ----------------- | ----------------------------------------- | | WebView 버전/정책 | WebView2 최소 버전 명시, 업데이트 유도 | | 코드 서명(보안) | 배포 시 서명 및 신뢰할 수 있는 게시자 권장 | | 자동 업데이트 | Squirrel(Windows), Sparkle(macOS) 등 검토 |

---

### 2.3 Mobile App

**역할**: 터치 중심의 편집·뷰어, 복잡한 고급 기능은 생략 또는 간소화(Progressive Enhancement).

**권장 방식: WebView 임베딩**

- **iOS**: WKWebView
- **Android**: WebView (Chromium) 또는 Chrome Custom Tabs(링크만 열 때)

동일 Web 앱을 로드하고, 터치·제스처·화면 크기에 맞춰 CSS/미디어쿼리 및 터치 이벤트로 조정.

**특징**:

- **입력**: 터치 드래그·핀치 줌·더블탭 등, 마우스 이벤트를 터치로 매핑
- **키보드**: 가상 키보드 노출 시 뷰포트·스크롤 처리 필요
- **파일**: 모바일에서는 업로드/다운로드 위주, 로컬 경로 직접 접근 제한
- **인쇄**: OS 인쇄 공유 또는 PDF 생성 후 공유

**기능 범위 (80% 목표)**:

- **지원**: 리포트 뷰어, 기본 편집(드래그·리사이즈·텍스트), 저장, PDF/이미지 내보내기
- **간소화 또는 제외**: 복잡한 다중 선택, 고급 Annotation 도구, 대용량 Multi ImageBox 동시 로딩

**성능 목표**:

- 앱 시작(WebView 준비): 5초 이내
- 리포트 로딩: 3초 이내 (요소 수에 따라 조정)
- 터치 반응: 100ms 이내

**제약 및 대응**: | 제약 | 대응 | | ----------------- | ----------------------------------------- | | 작은 화면 | 반응형 레이아웃, 모바일 툴바/패널 배치 | | 메모리 | 이미지 해상도/개수 제한, 지연 로딩 | | 배터리 | 불필요한 애니메이션·폴링 최소화 | | 브라우저 엔진 차이 | iOS WebKit, Android Chromium — 공통 CSS/JS로 호환성 유지 |

---

## 3. 플랫폼별 기능 지원 매트릭스

### 3.1 핵심 기능

본 매트릭스에서 **Desktop**은 WebView 방식(또는 동일 능력을 갖는 Electron 래핑)을 기준으로 한다.

| 기능                          | Web     | Desktop | Mobile  | 비고                                  |
| ----------------------------- | ------- | ------- | ------- | ------------------------------------- |
| 리포트 열기(Cloud)            | full    | full    | full    | API 동일                              |
| 리포트 저장(Cloud)            | full    | full    | full    | API 동일                              |
| 로컬 파일 열기                | partial | full    | partial | Web/모바일: 업로드만                  |
| 로컬 파일 저장                | partial | full    | partial | Web/모바일: 다운로드만                |
| Element 편집(드래그/리사이즈) | full    | full    | full    | 터치 = 드래그 매핑                    |
| TextBox 편집                  | full    | full    | partial | 모바일: 가상 키보드 UX 고려           |
| ImageBox (Single)             | full    | full    | full    |                                       |
| ImageBox (Multi/Ref)          | full    | full    | partial | 모바일: 성능에 따라 제한              |
| Annotation 6종                | full    | full    | full    | 터치로 그리기                         |
| ToothBox / TreatmentCategory  | full    | full    | partial | 모바일: 터치 선택 최적화              |
| PDF Export                    | full    | full    | full    |                                       |
| 인쇄                          | partial | full    | partial | Web: 브라우저 인쇄, Desktop: 네이티브 |
| 키보드 단축키                 | full    | full    | none    | 모바일: 해당 없음                     |
| 오프라인 뷰어                 | partial | partial | partial | PWA/캐시 범위 내                      |

### 3.2 플랫폼별 지원 수준 정의

- **full**: 기준(Web)과 동등하거나 네이티브로 보완
- **partial**: 제한적 지원(업로드만, 브라우저 인쇄만 등) 또는 UX 조정
- **none**: 해당 플랫폼에서 미제공

### 3.3 TypeScript 인터페이스 (참고)

```typescript
interface PlatformSupport {
  feature: string
  web: 'full' | 'partial' | 'none'
  desktop: 'full' | 'partial' | 'none'
  mobile: 'full' | 'partial' | 'none'
  alternative?: string // 대안 (예: '업로드로 대체')
}
```

---

## 4. WebView 통합 가이드

### 4.1 공통 원칙

- **단일 URL 또는 단일 Web 빌드**: Desktop/Mobile은 동일 Web 앱을 로드
- **User-Agent / Capability 감지**: 플랫폼별로 다른 레이아웃·기능 노출 시 사용
- **PostMessage 또는 URL Scheme**: 네이티브(파일 열기/저장, 인쇄) 연동

### 4.2 Windows (WebView2)

- **최소 런타임**: WebView2 Runtime 지정 버전 이상
- **로드**: SCP Cloud URL 또는 로컬 빌드(파일:// 또는 embedded)
- **파일 연동**: 사용자 선택 시 네이티브 대화상자 → 파일 경로 또는 내용을 Web에 전달
- **참고**: [Microsoft WebView2 문서](https://docs.microsoft.com/en-us/microsoft-edge/webview2/)

### 4.3 macOS (WKWebView)

- **WKWebView** 로드, 쿠키/스토리지 공유 설정
- **파일 연동**: NSOpenPanel / NSSavePanel → 데이터 또는 경로를 Web에 전달
- **인쇄**: NSPrintOperation 연동

### 4.4 iOS (WKWebView)

- **WKWebView** 사용, 터치 딜레이 제거 옵션
- **뷰포트**: viewport meta, safe area 반영
- **키보드**: input 포커스 시 스크롤·뷰 이동 처리
- **파일**: 문서 선택 UI → 파일 데이터 전달

### 4.5 Android (WebView)

- **WebView** 또는 Chrome Custom Tabs(전체 화면이 필요할 때)
- **터치**: 스크롤·핀치 동작과 편집 제스처 구분
- **파일**: Activity Result API로 파일 선택 후 Web에 전달
- **인쇄**: PrintManager 또는 PDF 공유

---

## 5. 성능 최적화 전략

### 5.1 Web (기준)

- **코드 스플리팅**: 라우트·헤비 컴포넌트(리포트 에디터) 지연 로딩
- **번들**: Tree-shaking, PoC-05 선정 라이브러리 사용량 점검
- **캐싱**: 서비스 워커로 정적 자원·API 응답 정책에 따라 캐시
- **렌더링**: 가상화 없이 50개 Element 기준 목표 유지, 초과 시 PoC-14에서 가상화 검토

### 5.2 Desktop

- **WebView 사전 초기화**: 앱 시작 시 WebView 프로세스만 미리 띄우기
- **캐시**: WebView 디스크 캐시 활용
- **네이티브 리소스**: 파일 읽기/쓰기는 네이티브에서 수행 후 Web에 결과만 전달

### 5.3 Mobile

- **이미지**: 썸네일·저해상도 먼저, 필요 시 고해상도 로드
- **메모리**: 동시 로드 Element 수 제한, 이전 페이지 언로드
- **터치**: passive 이벤트, 스크롤 중 불필요한 연산 지연
- **배터리**: requestAnimationFrame·타이머 사용 최소화

---

## 6. UX 가이드라인

### 6.1 공통

- **mm 단위 일관**: PoC-02·PoC-06에 따라 모든 플랫폼 동일 좌표·크기
- **접근성**: 키보드 탐색(Web/Desktop), 스크린 리더(플랫폼 a11y) 고려
- **에러**: 네트워크 오류·저장 실패 시 동일한 메시지·복구 안내

### 6.2 Web / Desktop

- **마우스**: 호버 상태, 컨텍스트 메뉴, 드래그 핸들
- **키보드**: Tab, Enter, Esc, 방향키, 단축키(저장, 실행 취소 등)
- **고해상도**: 고 DPI 스케일링 시 선명도 유지(PoC-03 DPI 전략)

### 6.3 Mobile

- **터치**: 드래그 = 이동/리사이즈, 더블탭 = 편집 모드 등 제스처 통일
- **툴바**: 하단 또는 상단 고정, 엄지 영역 고려
- **모달**: 전체 화면 또는 하단 시트로 키보드와 겹침 최소화
- **텍스트 입력**: 포커스 시 자동 스크롤, 줌 비활성화 또는 제한

---

## 7. 테스트 시나리오

### 7.1 기능 동등성

- **동일 리포트**: 하나의 리포트 JSON을 Web / Desktop / Mobile에서 열기
- **편집**: 동일한 변경(위치, 크기, 텍스트, Annotation) 수행
- **저장 후 비교**: 저장된 JSON이 플랫폼 간 일치하는지 검증
- **Export**: PDF/이미지 출력이 플랫폼 간 동일한 품질인지 비교(PoC-10 연계)

### 7.2 성능 벤치마크

| 항목                    | Web        | Desktop    | Mobile     |
| ----------------------- | ---------- | ---------- | ---------- |
| 앱(또는 첫 화면) 로딩   | &lt; 3초   | &lt; 5초   | &lt; 5초   |
| 리포트 로딩(50 Element) | &lt; 2초   | &lt; 2초   | &lt; 3초   |
| 편집 반응성             | &lt; 100ms | &lt; 100ms | &lt; 100ms |
| 메모리(편집 중)         | 기준       | 기준+상한  | 기준+상한  |

### 7.3 사용성

- **플랫폼별 인터랙션**: 마우스/키보드(Web·Desktop), 터치만(Mobile)으로 핵심 작업 완료 가능 여부
- **화면 크기**: 320px~1920px 구간에서 레이아웃·가독성
- **접근성**: 키보드만으로 편집 플로우 수행, 필요 시 스크린 리더 확인

---

## 8. 제약사항 및 리스크

### 8.1 WebView 의존성

- **리스크**: OS·WebView 버전에 따라 동작 차이
- **완화**: 최소 WebView 버전 명시, 공통 CSS/JS만 사용, 회귀 테스트

### 8.2 모바일 성능

- **리스크**: 복잡한 리포트에서 지연 또는 메모리 부족
- **완화**: Element 수·이미지 해상도 제한, 모바일은 80% 기능 목표 유지

### 8.3 파일·인쇄

- **리스크**: Web에서는 로컬 파일 직접 접근·시스템 인쇄 불가
- **완화**: 업로드/다운로드·브라우저 인쇄로 대체, 고급 요구는 Desktop 앱으로 유도

---

## 9. 결론 및 권장 사항

### 9.1 권장 전략

- **1차 플랫폼**: **Web App** — 모든 기능 구현·검증의 기준
- **Desktop**: **WebView 기반 래퍼** — 동일 Web 앱 + 네이티브 파일/인쇄/단축키
- **Mobile**: **WebView 임베딩** — 동일 Web 앱 + 터치·레이아웃 최적화, 기능 80% 목표

단일 코드베이스를 유지하고, 플랫폼별로 Progressive Enhancement를 적용하는 것이 유지보수와 품질 측면에서 유리합니다.

### 9.2 예상 지원 수준

- **Web**: 100% (기준)
- **Desktop**: 95% (로컬 파일·시스템 인쇄 보완)
- **Mobile**: 80% (편집 중심, 복잡한 기능·대용량 제한)

### 9.3 다음 단계

- PoC-14(Element 렌더링 엔진)에서 Web 기준 구현 후, 동일 빌드로 WebView 로딩 테스트
- PoC-10(인쇄·Export 품질)과 연계해 플랫폼별 PDF·인쇄 품질 검증
- 필요 시 Desktop/Mobile용 최소 래퍼 프로토타입으로 실제 WebView 연동·성능 측정
