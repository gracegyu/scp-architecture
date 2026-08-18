## MQTT 관련 문의

안녕하세요 Raymond (

전규현(Jeon, Gyu Hyeon)),  (CC. 민진우(Thomas))

VAG–EzServer 간 MQTT 연동 규격 관련하여 확인 요청드립니다.

SRS의 MQTT 요구사항을 확인한 결과, VAG의 MQTT는 다음 조건으로 정의되어 있는 것으로 확인 했습니다.

- Broker: AWS IoT Core
- Protocol: MQTT 5.0 필수
- 전송: QoS 1 + Persistent Session
- 인증: Device별 X.509 인증서를 이용한 mTLS
- Client ID: GW가 발급한 deviceId
- Topic: gw/clinic/{clinicId}/webhook
- Payload: Webhook 원문을 변형하지 않고 그대로 전달
- Session Expiry Interval: EzServer가 최대 7일 범위에서 설정
- Payload 제한: 최대 128KB

특히 MQTT 5.0을 필수로 지정한 이유는 MQTT 3.1.1 사용 시 AWS IoT Core의 세션 만료가 계정 전체에 대해 1시간으로 고정되어, EzServer가 1시간 이상 오프라인일 경우 메시지 보존 요구사항을 충족하기 어렵기 때문으로 확인됩니다.

다만 현재 EzServer, Desktop 제품의 MQTT 클라이언트는 MQTT v3.1.1 기반입니다.

첨부 테스트 결과에서도 MQTT v5로 발행한 메시지의 Topic과 Payload는 수신되지만, 다음과 같은 MQTT v5 전용 속성은 확인되지 않았습니다.

- Content Type
- Response Topic
- User Properties
- 기타 MQTT v5 전용 Message Properties

SRS상 현재 하행 메시지는 별도 Envelope 없이 Payload를 그대로 전달하며, EzServer가 필요한 라우팅 정보는 Topic과 Payload 내부 필드에서 획득하도록 되어 있는 것으로 확인 했습니다.

이에 아래 사항 확인 부탁드립니다.

1. VAG에서 발행하는 MQTT 메시지 처리 시 MQTT v5 Message Properties를 실제로 사용할 예정인지

2. 해당 Properties가 EzServer의 필수 처리 정보 또는 향후 확장 정보에 해당하는지

3. EzServer가 MQTT v3를 유지할 경우 Properties 유실을 허용할 수 있는지

4. 허용할 수 없다면 EzServer, Desktop MQTT 클라이언트를 v5로 변경해야 하는지

5. MQTT v5 전환 시 Session Expiry Interval, QoS 1, Persistent Session 및 clientId=deviceId 적용 방식에 대한 VAG 측 권장 설정