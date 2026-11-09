# PR 15932 리뷰 — 두 클라이언트의 독립 인증 공존 검증

| 항목 | 내용 |
| --- | --- |
| PR | [15932](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15932) · `tasks/ESIP-37-direct-client-coexistence` → main (분기 `6ccff84`) |
| 작성 | Scott |
| 변경 | `test/enroll/enroll-complete.e2e-spec.ts` (+124 −5) — e2e 1건 추가 · 헬퍼에 헤더 인자 |
| 검토일 | 2026-11-09 |
| **판단** | **승인** — 테스트만 추가, 런타임 변경 없음. 폐기 경로 보강은 제안(머지 차단 아님) |

## 확인한 것

- 같은 clinic 에 active EzServer 가 있을 때 Edge 를 등록하면 `deviceId`·`clientId`·`certificateId` 가 모두 다르고, 기존 EzServer 의 공개키·상태·토큰 발급이 그대로다.
- pending Edge 는 `403 authorization_pending`, 승인 뒤에는 자기 키로 토큰을 받고 `/v1/clinics/me` 가 같은 clinicId 를 돌려준다.
- **Edge 의 clientId 로 EzServer 개인키를 써 보면 401** — 제품 헤더가 키를 대신하지 못함을 고정한 좋은 케이스다.
- 기존 1:N 공존 테스트(`같은 clinic 으로 두 번 enroll`) 묶음 안에 들어가 있어 위치가 맞다.

## 짚을 것

1. **폐기를 실제 경로가 아니라 denylist 키 직접 설정으로 흉내 낸다.** 테스트는 `gw:revoked:{deviceId}` 를 Redis 에 직접 넣는다. 실제 폐기(운영자 상태 변경 `PATCH /v1/admin/devices/{id}` → revoked, 또는 kill)는 denylist 에 더해 **DB 상태 변경과 IoT 인증서 비활성화**(`deactivateCertForDevice`)를 함께 한다. PR 이 증명하려는 핵심은 "한 기기를 폐기해도 다른 기기는 그대로"인데, 지금 테스트는 그중 denylist 만 본다. 인증서 비활성화가 device 단위인지, 다른 기기 인증서를 건드리지 않는지는 검증되지 않는다. 폐기 서비스(`RevocationService` 또는 admin 폐기 경로)를 호출하고 Edge 인증서가 active 로 남는지까지 확인하면 PR 설명의 주장과 테스트가 맞는다.
2. **승인을 SQL 로 처리한다.** 운영자 승인 API 는 다른 앱(admin)이라 픽스처로 처리한 것은 이해한다. 주석에 이미 적혀 있어 수용.
3. **MQTT 공존은 범위 밖이다.** 이 테스트는 HTTP 인증만 본다. 두 기기의 IoT 인증서·정책·같은 clinic 토픽 동시 구독은 검증하지 않으니 PR 설명에 범위를 한 줄 적어 두면 좋겠다(문서 PR 15931 의 검증 조건 4 와 연결).

## 리뷰 코멘트 초안 (PR 전체 코멘트·복사용)

```
승인합니다. 같은 원내에 active EzServer 가 있을 때 Edge 를 추가해도 기존 신원과 토큰이 그대로이고, pending 과 승인 이후 동작, 제품 헤더가 키를 대신하지 못하는 경우까지 잘 고정했습니다.

한 가지 보강을 제안합니다. 지금 폐기는 denylist 키를 Redis 에 직접 넣어 흉내 내고 있는데, 실제 폐기 경로는 denylist 와 함께 DB 상태 변경과 IoT 인증서 비활성화를 같이 합니다. 이 PR 이 증명하려는 것이 "한 기기를 폐기해도 다른 기기는 그대로"인 만큼, 폐기 서비스를 직접 호출하고 Edge 의 인증서가 active 로 남는지까지 확인하면 설명과 테스트가 정확히 맞을 것 같습니다. 후속 PR 로 해도 괜찮습니다.

그리고 이 테스트는 HTTP 인증만 다루고 MQTT 쪽(인증서·정책·같은 clinic 토픽 동시 구독)은 범위 밖이라는 점을 PR 설명에 한 줄 적어 주시면 좋겠습니다.
```
