## Project Name : Stripe 결제 기능 Technical Prototyping

## Date : 2025-04-24

## Submitter Info : Raymond

## Project Description :

Stripe를 이용하여 다양한 결제 유형을 서버 및 클라이언트 환경에서 구현 및 검증하는 Technical Prototyping 프로젝트. Nest.js 기반의 백엔드 서버와 Next.js 기반의 프론트엔드 클라이언트를 활용하여 Stripe 결제 기능의 기술적 적합성을 검토함.

## Business and Marketing Justification :

향후 상용화될 SaaS 서비스에서 결제 기능은 핵심적인 모듈이며, 안정적이고 확장성 있는 결제 인프라의 선택은 매우 중요함. Stripe는 글로벌 표준 솔루션이며, 다양한 결제 방식 및 수단을 지원하므로 그 적합성 여부를 기술적으로 사전 검증함으로써, 추후 개발 일정의 리스크를 낮추고 고객 경험을 향상시킬 수 있음.

## Risk Assessment :

- Stripe API의 기능적 제약 혹은 예상치 못한 제한사항 발생 가능성
- 국내 결제 환경(예: 은행 계좌 결제)과의 호환성 문제
- 테스트 환경에서의 한계로 인해 실환경과의 Gap 발생 가능성

## Resource and Scheduling Details :

- 리소스: Backend, Frontend 개발자 1명
- 예상 소요 기간: 4/24 ~ (8일)
- 기술 스택: Node.js(Nest.js), React, Stripe API
- 소스코드: https://ewoosoft@dev.azure.com/ewoosoft/prototypes/\_git/stripe_payment_prototype
- 디렉토리 구조:

  ```
  stripe_payment_prototype/
  ├── docs/          # 스펙 문서
  ├── backend/       # Nest.js 기반 백엔드 소스코드
  ├── frontend/      # React 프론트엔드 소스코드
  └── .env           # 환경 변수 파일 (Stripe API Key, Webhook Secret 등 관리)

  ```

## Technical Description :

### 검증 항목

1. 서버 기반 결제 검증 항목

   - (P1) 비정기 단건 결제: Stripe PaymentIntent API 활용
   - (P1) 정기 결제 (정액제): Stripe의 Subscription 기능 활용
   - (P1) 정기 결제 (Usage-based): Stripe의 metered billing 기능 적용, 매 cycle마다 usage record 전송
   - (P1) Stripe Customer Portal 연동: 고객이 자신의 구독, 결제 수단, 인보이스를 직접 관리할 수 있는 포털 세션 생성 및 리디렉션 흐름 검증
   - (P1) 결제 취소 및 환불 처리: 전체 및 부분 환불 시나리오 검토
   - (P2) 미리 생성된 invoice 기반 수동 결제: Invoice를 서버에서 생성하고 고객이 이를 보고 결제
   - (P2) Subscription 변경/업그레이드/다운그레이드: 기존 구독에서 새로운 요금제로 전환 시나리오, proration 처리 등
   - (P2) 서버에서 결제수단 변경 처리: 카드 만료 등의 상황에서 결제수단 갱신 처리
   - 검증 목적을 고려하여 간단한 REST API를 Nest.js 기반으로 구성함. 주요 엔드포인트는 다음과 같음:
     - POST /payments/intent # 단건 결제 생성 (PaymentIntent)
     - POST /payments/subscribe # 정기 결제 생성 (Subscription)
     - POST /payments/setup # 결제 수단 등록 (SetupIntent)
     - POST /payments/portal # Stripe Customer Portal 세션 생성
     - POST /webhook # Stripe Webhook 이벤트 수신 처리
   - 각 API는 실제 서비스 적용 시 예상되는 데이터 흐름과 일치하도록 구성하여, Stripe 도입 시 필요한 구현 복잡도와 흐름을 검토하는 데 목적이 있음.

2. 클라이언트 카드 인증 및 결제 수단 관리 검증 항목

   - (P1) 카드 저장 후 단건 결제: SetupIntent로 저장된 payment method를 사용한 서버 기반 결제
   - (P1) 카드 직접 입력 후 결제: PaymentElement UI를 통한 카드 정보 수집 및 PaymentIntent 인증 처리
   - (P2) Stripe Checkout 세션 기반 결제: 서버에서 세션 생성 후 Stripe 호스팅 페이지로 리디렉션하여 결제
   - (P2) 결제 수단 등록만 수행: 결제는 하지 않고 payment method만 저장하는 흐름 (SetupIntent 단독 활용)

3. 결제 수단 지원

   - (P1) 신용/체크카드: 기본 Stripe 결제 수단
   - (P1) 결제 수단 등록하기

4. 결과 보고 및 회고

   - 본 프로토타이핑의 성공 기준은 Stripe의 다양한 결제 시나리오에 대해 기술적 구현 가능성뿐 아니라, 서비스 적용 시 가장 적합한 Stripe 기능(예: SetupIntent, PaymentIntent, Checkout 등)을 비교 분석하여 선택할 수 있는 기준을 마련하는 것임.
   - (P1) 테스트 결과 문서 작성
   - (P1) 프로토타이핑 결과를 바탕으로 실제 서비스 개발에 필요한 설계 가이드 작성

5. 추가 검증 항목

   - (P1) Webhook 이벤트 처리 검증: invoice.created, invoice.paid, subscription.deleted 등 Stripe Webhook 처리. Stripe CLI의 웹훅 리스너 기능을 이용해 로컬 개발 환경에서도 테스트 가능함. (`stripe listen --forward-to http://localhost:3000/api/webhook` 명령어로 Stripe 웹훅 이벤트를 로컬 서버로 포워딩하여 검증)
   - (P1) 보안 및 인증 관련 검토: 3D Secure(3DS) 인증 적용 여부 및 처리 방식
   - (P2) Free Trial 및 프로모션 적용: 일정 기간 무료 체험 후 유료 전환, 쿠폰 코드 또는 할인 적용
   - (P2) 결제 실패 및 재시도 로직: payment_failed 이벤트 수신 후 재시도 처리 시나리오 확인
   - (P2) 다국적 통화 및 결제 시나리오: USD, KRW, JPY 등 다양한 통화 환경에서의 결제
   - (P2) 은행 계좌: Stripe ACH debit 또는 Bank Redirect 기반 결제 수단 시나리오 검토
   - (P2) Stripe Checkout과 Payment Elements 비교: Checkout 기반 간편 결제 vs. Element 기반 커스터마이징 구현 비교
   - (P2) 자체 UI 구현 vs Stripe Customer Portal 비교: 구독 관리, 결제 수단 관리, 인보이스 조회 등의 기능을 자체 구현하는 방식과 Stripe Portal을 활용하는 방식의 장단점 분석

6. 고객 관리 아키텍처 연구
   - 기존 구현된 고객 API를 기반으로 SaaS를 위한 최적의 고객 데이터 아키텍처를 연구했습니다.
   - (P1) Stripe Customer 생성 및 관리: 이메일 중복 확인 및 고유성 보장
   - (P1) 사용자-고객 매핑 모델: 개인 사용자 중심 서비스 구현
   - (P1) 조직-고객 매핑 모델: B2B 서비스를 위한 조직 단위 결제 구현
   - (P2) 고객 정보 조회 및 업데이트: API 활용 고객 정보 관리
   - (P2) 메타데이터 활용: 비즈니스 데이터와 Stripe 고객 정보 연동
