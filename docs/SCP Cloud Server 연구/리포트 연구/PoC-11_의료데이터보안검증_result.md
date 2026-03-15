# PoC-11 결과 보고서: 의료 데이터 보안 검증

## 요약

- **목표**: SCP Cloud Report가 HIPAA, GDPR, 개인정보보호법 등 의료 데이터 보안 규정을 준수할 수 있는 보안 아키텍처 검증
- **범위**: 내부 Cloud 서비스 전용 Shared Library. 인증·접근 제어는 호스트(SCP Cloud 등) 담당, Report 라이브러리는 데이터 처리·전송·저장 시 보안 요구 반영
- **전략**: Defense in Depth(계층별 보안), 전송 암호화(TLS), 최소 권한, 감사 로그 연동
- **산출물**: 보안 아키텍처, 규정 준수 체크리스트, OWASP 대응 가이드, 감사 추적 인터페이스

---

## 1. 개요

### 1.1 검증 목표

SCP Cloud Report 시스템이 **의료 데이터 보안 규정**(HIPAA, GDPR, 개인정보보호법)을 준수할 수 있는 보안 아키텍처를 설계하고 검증합니다. 브라우저 환경에서 민감한 의료 데이터를 안전하게 처리하며, 감사 추적과 접근 제어가 가능한 구조를 수립합니다.

**프로젝트 범위 반영**:

- SCP Cloud Report는 **내부 Cloud 서비스 전용** Shared Library
- SCP Cloud, Imaging Cloud 등 호스트 서비스에 통합됨
- **인증·세션·접근 제어**는 호스트 서비스 담당
- Report 라이브러리는 **데이터 처리·캐시·전송** 시 보안 요구 반영

### 1.2 규정별 핵심 요구사항

| 규정 | 핵심 요구 | Report 라이브러리 관점 |
|------|-----------|------------------------|
| **HIPAA** | PHI 암호화, 접근 제어, 감사 추적, 무결성 | 데이터 전송·저장 시 암호화, 감사 이벤트 노출 |
| **GDPR** | 최소 수집, 동의, 삭제권, 이동권 | 데이터 Export/삭제 API, 최소 필드 사용 |
| **개인정보보호법** | 동의, 목적 제한, 안전 조치 | 호스트와 연동, 로컬 캐시 정책 |

### 1.3 평가 기준

| 항목 | 가중치 | 평가 기준 |
|------|--------|-----------|
| **규정 준수** | 35% | HIPAA/GDPR/개인정보보호법 요구 충족 |
| **구현 가능성** | 30% | 웹 환경에서 실현 가능한 방안 |
| **성능 영향** | 20% | 암호화·검증 오버헤드 최소화 |
| **유지보수성** | 15% | 단순한 구조, 호스트와 역할 분리 |

### 1.4 리포트 데이터의 의료 보안·인증 특성

리포트는 원본 영상(DICOM 등)이 아니어도 동일한 규제가 적용된다.

| 구분 | 내용 |
|------|------|
| **PHI 적용** | 리포트에는 환자 식별정보·진단 내용 포함. HIPAA/GDPR 기준 PHI로 동일 보호 |
| **의료기기(SaMD)** | 진단·치료 결정에 직접 사용 시 FDA 510(k), CE-MDR 대상. 서식·편집만 담당 시 Class I 이하 또는 비의료기기 가능 |
| **무결성** | 변조 시 잘못된 진단으로 이어질 수 있어 수정 이력·검증 메커니즘 필요 |
| **법적 문서** | 소송 시 증거로 사용될 수 있어 보존 기간, non-repudiation 요구 |
| **임베디드 이미지** | 리포트 내 썸네일·삽화도 PHI로 동일 취급 |

본 문서의 보안·감사 요구는 리포트 데이터에도 그대로 적용된다. SaMD 분류는 의료기기 규제 전문가와 용도 확인 후 결정.

---

## 2. 보안 아키텍처

### 2.1 계층별 책임 분리

```
┌─────────────────────────────────────────────────────────┐
│ 호스트 서비스 (SCP Cloud, Imaging Cloud 등)              │
│ - 인증 (MFA, SSO)                                       │
│ - 세션 관리, 토큰 발급                                   │
│ - 역할 기반 접근 제어 (RBAC)                             │
│ - 감사 로그 수집·저장                                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Report Library (본 PoC 대상)                              │
│ - API 호출 시 토큰 전달 (호스트 제공)                     │
│ - 민감 데이터 메모리·캐시 처리 정책                       │
│ - XSS/Injection 방지 (입력 검증)                         │
│ - 감사 이벤트 콜백 노출                                  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 데이터 흐름 보안

| 구간 | 조치 | 담당 |
|------|------|------|
| **클라이언트 ↔ 서버** | TLS 1.2+ (HTTPS) | 호스트 인프라 |
| **메모리** | 민감 데이터 최소 보유, 사용 후 참조 해제 | Report Library |
| **로컬 캐시** | IndexedDB 등 사용 시 암호화 또는 민감 데이터 미저장 | Report Library |
| **서버 저장** | 암호화 저장 (호스트 DB 정책) | 호스트 서비스 |

### 2.3 Report Library 보안 요구사항

1. **입력 검증**: 사용자 입력(텍스트, URL 등) sanitization, XSS 방지
2. **API 호출**: 호스트 제공 토큰으로 인증, 민감 데이터 URL/로그 노출 금지
3. **캐시**: 리포트 미리보기 등 캐시 시 민감 정보 제외 또는 암호화
4. **감사 이벤트**: 리포트 열기/저장/삭제 등 액션 시 콜백으로 호스트에 전달

---

## 3. OWASP Top 10 대응

### 3.1 적용 항목

| 위험 | 대응 | Report Library 역할 |
|------|------|---------------------|
| **A03:2021 – Injection** | 입력 검증, 파라미터화 | 텍스트/HTML 입력 sanitization |
| **A07:2021 – XSS** | 출력 인코딩, CSP | React 기본 이스케이프, dangerouslySetInnerHTML 금지 |
| **A01:2021 – Broken Access Control** | 토큰·권한 검증 | 호스트 담당, Library는 토큰 전달만 |
| **A05:2021 – Security Misconfiguration** | CSP, HTTPS | 호스트 배포 시 설정 |
| **A02:2021 – Cryptographic Failures** | TLS, 저장 암호화 | 호스트 인프라·DB |

### 3.2 입력 검증 가이드

```typescript
// 텍스트 입력 sanitization (XSS 방지)
function sanitizeText(input: string): string {
  const div = document.createElement('div')
  div.textContent = input
  return div.innerHTML
}

// HTML 콘텐츠 허용 시 DOMPurify 등 사용 권장
// dangerouslySetInnerHTML 직접 사용 금지 (사용자 입력에 대해)
```

### 3.3 Content Security Policy (CSP)

호스트 서비스에서 설정. Report Library는 외부 스크립트/이미지 로드 최소화.

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: blob: https:;
  connect-src 'self' https://api.scp-cloud.com;
  font-src 'self';
```

---

## 4. 감사 추적 (Audit Trail)

### 4.1 이벤트 인터페이스

Report Library는 액션 발생 시 콜백으로 호스트에 전달. 실제 저장·보관은 호스트 담당.

```typescript
interface AuditEvent {
  timestamp: string      // ISO 8601
  action: 'OPEN' | 'SAVE' | 'DELETE' | 'EXPORT' | 'PRINT'
  resourceType: 'REPORT' | 'TEMPLATE'
  resourceId?: string
  userId?: string        // 호스트에서 주입
  result: 'SUCCESS' | 'FAILURE'
  metadata?: Record<string, unknown>
}

interface ReportLibraryConfig {
  onAuditEvent?: (event: AuditEvent) => void
}
```

### 4.2 HIPAA 감사 요구 반영

- **접근 로그**: 리포트 열기(OPEN), 저장(SAVE), 삭제(DELETE) 기록
- **내용**: 누가, 언제, 무엇을, 결과. PHI 자체는 로그에 포함하지 않음
- **보관**: 호스트 서비스에서 6년 이상 등 정책에 따라 보관

---

## 5. GDPR·개인정보보호법 대응

### 5.1 데이터 최소화

- 리포트 구조에서 **필수 필드만** 수집·전송
- 디버그용 로그에 개인정보 포함 금지

### 5.2 삭제권 (Right to be Forgotten)

- 호스트 서비스가 삭제 API 제공
- Report Library는 삭제 요청 시 해당 리포트 로컬 캐시 무효화

### 5.3 데이터 이동권

- Export(JSON/PDF) 기능으로 사용자 데이터 반환
- 호스트가 사용자 요청에 따라 Export 결과 전달

---

## 6. 규정 준수 체크리스트

### 6.1 HIPAA

| 항목 | 담당 | 상태 |
|------|------|------|
| 암호화 저장 및 전송 | 호스트 | TLS, DB 암호화 |
| 접근 로그 기록 | 호스트 + Library 콜백 | 감사 이벤트 연동 |
| 최소 권한 접근 제어 | 호스트 | RBAC |
| PHI 노출 최소화 | Library | 로그·캐시에 PHI 미포함 |

### 6.2 GDPR

| 항목 | 담당 | 상태 |
|------|------|------|
| 데이터 처리 동의 | 호스트 | - |
| 개인정보 삭제 | 호스트 + Library 캐시 무효화 | - |
| 데이터 이동권 | 호스트 + Export | - |
| Privacy by Design | Library | 최소 수집, 익명화 가능 구조 |

### 6.3 개인정보보호법 (한국)

| 항목 | 담당 | 상태 |
|------|------|------|
| 동의 획득 | 호스트 | - |
| 목적 제한 | 호스트 | - |
| 안전 조치 | 호스트 + Library | 암호화, 접근 제어 |

---

## 7. 성능 vs 보안

| 항목 | 목표 | 비고 |
|------|------|------|
| 암호화 오버헤드 | < 10% | TLS는 네트워크 구간, Library 부담 적음 |
| 입력 검증 | < 5ms/요청 | sanitization 경량 |
| 감사 콜백 | 비동기, 블로킹 없음 | 호스트 처리 부담 |

---

## 8. 결론 및 다음 단계

### 8.1 핵심 결론

1. **역할 분리**: 인증·접근 제어·감사 저장은 호스트, Report Library는 데이터 처리·이벤트 노출
2. **입력 검증**: XSS/Injection 방지를 위한 sanitization 필수
3. **감사 연동**: AuditEvent 콜백으로 HIPAA 감사 요구 충족
4. **규정 준수**: 호스트와 협업하여 HIPAA/GDPR/개인정보보호법 요구 충족 가능

### 8.2 제한사항

- 실제 인증·암호화 구현은 호스트 서비스 범위
- 의료기기 인증(FDA, CE) 시 추가 요구사항 검토 필요

### 8.3 다음 단계

1. **PoC-14**: Report Library 구현 시 입력 검증·감사 콜백 적용
2. **SCP Cloud**: 호스트 서비스에 RBAC, 감사 로그, TLS 정책 반영
3. **보안 테스트**: OWASP ZAP 등으로 취약점 스캔 (통합 후)

---

**검증 일자**: 2026-01-23  
**참조**: PoC-11_의료데이터보안검증_OnePager.md, SCP Cloud Report PoC 설계.md
