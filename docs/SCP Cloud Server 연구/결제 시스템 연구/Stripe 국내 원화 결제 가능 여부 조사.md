# 1. Stripe의 한국 내 지원 여부

현재 Stripe는 **한국에 공식적으로 진출하지 않은 상태**이다. 따라서 한국 내에서 Stripe 계정을 개설하거나 한국 은행 계좌를 연결하는 것은 불가능하다. 이는 Stripe의 글로벌 지원 국가 목록에서 한국이 제외되어 있는 것으로 확인된다.

- 참고: https://stripe.com/global

---

# 2. 해외 법인을 통한 한국 결제 처리 가능성

2024년 10월 28일부터 Stripe는 한국의 주요 결제 수단을 공식적으로 지원하기 시작했다. 이 정책 변화로 인해 Stripe가 직접 진출하지 않은 국가인 한국에서도, 해외 법인을 통해 국내 결제 수단을 사용하는 것이 가능해졌다. 이는 Stripe가 한국의 대표적인 결제대행사(PG사) 중 하나인 **NICE Payments(나이스페이먼츠)** 와의 **전략적 파트너십**을 체결한 결과이다.

Stripe는 이 파트너십을 통해 국내 카드사 21개 브랜드 및 간편결제 수단(카카오페이, 네이버페이 등)을 Stripe Checkout, Payment Links, Subscription Billing 등 기존 Stripe 결제 흐름 내에서 통합 지원할 수 있게 되었으며, 한국 고객에게 보다 현지화된 결제 경험을 제공할 수 있게 되었다.

- 참고: https://stripe.com/blog/biggest-updates-sessions-2024

Stripe가 한국에 직접 진출하지 않았더라도, 미국이나 영국 등 Stripe가 **지원하는 국가에 법인을 설립**하면 해당 법인을 통해 한국 고객의 결제를 처리할 수 있다.

Stripe Atlas(Stripe가 제공하는 글로벌 스타트업 법인 설립 및 Stripe 계정 개설 지원 프로그램)를 비롯하여, 현지 법인 설립 대행 서비스, 미국 가상 주소 제공 업체, 미국 은행 계좌 개설 지원 서비스 등을 활용하여 Stripe 계정을 개설한 후, 한국 고객이 국내 카드나 간편결제를 사용할 수 있도록 설정할 수 있다.

미국 법인을 이미 보유하고 있다면 Stripe Atlas와 같은 법인 설립 서비스를 이용할 필요는 없다. Stripe는 미국 법인을 통해 직접 계정을 개설하고 계약을 진행할 수 있으며, 이 경우에도 한국 고객을 대상으로 국내 카드 및 원화 결제를 처리할 수 있다.

Stripe 계정을 개설하려면 다음 조건을 충족해야 한다:

- 미국 법인의 유효한 EIN (Employer Identification Number)
- 미국 내 주소
- 미국 은행 계좌

이러한 조건을 충족하는 미국 법인을 보유한 경우, Stripe에 직접 가입하고 계정을 개설하면 Stripe의 결제 시스템을 정상적으로 활용할 수 있다.

Stripe가 지원하는 한국 결제 수단

- 국내 발급 카드 (신한카드, 현대카드, 삼성카드, 국민카드, 롯데카드, 하나카드, 우리카드 등)
- 간편결제 (카카오페이, 네이버페이, 삼성페이, PAYCO, Toss페이, L.Pay, SSG페이 등)

이러한 결제 수단은 Stripe의 Checkout, Payment Links, Billing 등 다양한 통합 경로에서 사용할 수 있다.

- 참고: https://docs.stripe.com/payments/countries/korea
- 참고: https://docs.stripe.com/changelog/acacia/2024-10-28/south-korean-payment-methods
- 참고: https://stripe.com/atlas

---

# 3. 원화(KRW) 결제 지원 여부

Stripe는 **원화(KRW)를 결제 통화로 지원**한다. 즉, 한국 고객은 원화로 결제할 수 있으며 Stripe는 이를 정상적으로 처리할 수 있다.

- 단, 최소 결제 금액은 100원 이상이어야 하며 일부 결제 수단은 금액 제한이 존재할 수 있다.
- 참고: https://docs.stripe.com/currencies
- 참고: https://docs.stripe.com/payments/naver-pay/accept-a-payment?locale=de-DE

Stripe는 또한 **반복 결제(구독 모델)**을 위한 Billing 기능과도 통합되며, 이를 통해 정기 결제도 원화로 지원 가능하다.

- 참고: https://docs.stripe.com/billing/subscriptions/kr-card

---

# 4. 세금 및 법적 고려사항

한국 고객에게 디지털 서비스를 제공할 경우, 부가가치세(VAT) 등록 및 징수가 필요할 수 있다. Stripe Tax를 통해 이러한 세금 계산 및 징수를 자동화할 수 있다.

- 참고: https://docs.stripe.com/tax/supported-countries/asia-pacific/south-korea

---

# 결론

Stripe는 한국에 직접 진출하지 않았지만, 해외 법인을 통한 우회 방식으로 한국 고객의 결제를 처리할 수 있다.

- 국내 카드 및 간편결제를 지원
- 원화 결제 가능
- 반복 결제 및 세금 자동 처리 지원

즉, **미국 등 Stripe가 지원하는 국가에 법인을 보유한 경우**, Stripe를 통해 **한국 내 고객을 대상으로 국내 카드 및 원화 결제를 처리하는 것이 실질적으로 가능**하다.

다만 다음 사항은 반드시 유의해야 한다:

- **Stripe 계정은 해외 법인을 기반으로 개설되어야 하며, 한국 법인 명의로 개설하거나 한국 은행 계좌를 직접 연동하는 것은 현재로선 불가능**하다.
- 결제 수익 정산은 해당 법인의 현지 통화 및 은행 계좌를 통해 이뤄지며, 이에 따른 **외화 송금 절차 및 세무 처리**도 고려해야 한다.

따라서 Stripe를 통해 한국 결제를 구현하려면, 기술적 통합 외에도 법적/세무적 검토 및 해외 법인 운영 전략이 동반되어야 한다.

---

# 참고 자료 링크 정리

- Stripe 글로벌 지원 국가: https://stripe.com/global
- Stripe의 한국 결제 수단: https://docs.stripe.com/payments/countries/korea
- Stripe 간편결제 업데이트: https://docs.stripe.com/changelog/acacia/2024-10-28/south-korean-payment-methods
- Stripe 통화 목록: https://docs.stripe.com/currencies
- 원화 결제 상세: https://docs.stripe.com/payments/naver-pay/accept-a-payment?locale=de-DE
- 반복 결제 안내: https://docs.stripe.com/billing/subscriptions/kr-card
- Stripe Tax 한국 안내: https://docs.stripe.com/tax/supported-countries/asia-pacific/south-korea