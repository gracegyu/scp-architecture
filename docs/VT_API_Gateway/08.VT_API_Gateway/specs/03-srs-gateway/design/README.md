# ③ GW 설계 산출물 초안 (design)

dev-chain-design 단계 산출물(OpenAPI·DBML)의 **작성 초안** 공간이다.

## 워크플로우

```
[초안 작성]  scp-architecture  .../03-srs-gateway/design/
     ↓ (baseline 시 PR 이관)
[공식 SSOT]  vt-api-gateway   docs/specs/design/
     ↓ (구현 착수 후)
[코드 생성]  NestJS code-first(@nestjs/swagger) → /api-docs · Prisma schema
```

- **OpenAPI**(`openapi/vt-api-gateway.openapi.yaml`): 설계 합의용 손작성 초안. 구현 시작 후엔 **code-first `/api-docs` 산출물이 정본**이 되고, 본 초안은 설계 근거로 남는다.
- **DBML**(`dbml/vt-api-gateway.dbml`): 신규 테이블 컬럼·타입·인덱스·relation SSOT. 이후 **Prisma schema**로 이어진다.

## 범위 메모

- OpenAPI에는 **GW 고유 API(A면 — `Vatech-Target` 없는 호출)** 만 정의한다(§4.1.1·ADR-11). Webhook 수신 엔드포인트도 여기 포함(§4.1.3). 외부 payload는 `$ref`/스냅샷 참조, MQTT 분배는 OpenAPI 밖.
- **파일 업로드: GW는 presigned를 발급하지 않는다**(경로①·Region Signer 철회, §4.1.4·§7.4). 발급=CleverSpace(②)·AXS(③), GW는 `Vatech-Target` proxy로 **중계(bypass)** 만 — 본 OpenAPI에 업로드 API를 정의하지 않는다.
- 프록시(B 내부·C 외부)는 **`Vatech-Target` 헤더로 라우팅되는 verbatim bypass**(§4.1.2)이며, 각 백엔드/외부 OpenAPI가 정본 — 본 파일에서 재정의하지 않는다. 신규 upstream은 레지스트리 1행으로 추가(경로/코드 변경 0).
