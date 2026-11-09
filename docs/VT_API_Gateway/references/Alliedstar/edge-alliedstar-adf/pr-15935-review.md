# PR 15935 리뷰 — multer·systeminformation 보안 업데이트

| 항목 | 내용 |
| --- | --- |
| PR | [15935](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15935) · `tasks/fix-prod-transitive-audit` → main (분기 `6ccff84`) |
| 작성 | Scott |
| 변경 | `package.json` overrides 2줄 + 설명 · `pnpm-lock.yaml` (multer 2.4.0→2.5.0 · systeminformation 5.33.1→5.33.19) |
| 검토일 | 2026-11-09 (같은 날 갱신 — PR 15946 머지 반영) |
| **판단** | **abandon 권장** — 같은 수정이 PR 15946 으로 main 에 먼저 들어가 중복. Scott 이 직접 abandon 하도록 코멘트로 요청 |

## 경과

1. **처음 검토(오전)** — 변경 범위가 정확히 두 패키지와 그 사용처 두 곳뿐이고 기존 override 방식과 같아 **승인** 의견이었다.
2. **PR 15946 머지(2026-11-09 10:46)** — High 4건(zod 4.6.7 · body-parser · multer · systeminformation)을 한 번에 고친 PR 이 main 에 들어갔다. main 의 `package.json` 에 `multer ^2.5.0`·`systeminformation ^5.33.16`·`body-parser ^2.4.0` 이 모두 있는 것을 확인했다.
3. **이 PR 이 conflict** — 같은 줄(overrides·lockfile)을 양쪽이 다르게 고쳐서 충돌한다. 풀면 main 값을 그대로 가져가 **남는 변경이 없다.** conflict 상태라 CI 재실행도 잡히지 않는다(마지막 결과 = 2026-11-08 빌드 63440 실패, main 의 High 4건 때문).

## 왜 우리가 abandon·충돌 해결을 하지 않나

- PR 주인이 Scott 이고, Scott 이 Teams 에서 이 PR 을 리뷰 대상 5건 중 하나로 소개했다. 말없이 닫으면 혼선이 생긴다.
- conflict 상태라 머지될 수 없고 다른 PR 을 막지도 않아 급하지 않다.
- 충돌 해결은 Scott 의 PR 브랜치에 push 하는 일이고, 해결해도 빈 PR 이 된다.

## 참고 — 같은 원인으로 실패했던 나머지 PR

| PR | 새 main 기준 CI |
| --- | --- |
| 15931 | 통과 (빌드 63510) |
| 15932 | 통과 (빌드 63511) |
| 15933 | 통과 (빌드 63516) |
| 15934 | 문서만 바뀐 PR 이라 CI 대상 아님 |

## 리뷰 코멘트 초안 (PR 전체 코멘트·복사용)

```
같은 수정이 PR 15946 으로 오늘 main 에 먼저 들어갔습니다. multer 2.5.0, systeminformation 5.33.16 에 더해 zod 와 body-parser 까지 High 4건을 함께 올린 PR 입니다. 그래서 이 PR 은 지금 conflict 가 났고, 풀면 남는 변경이 없어 abandon 하셔도 될 것 같습니다. 나머지 네 PR 은 새 main 기준으로 CI 를 다시 돌려 두었고 15931·15932·15933 은 통과했습니다.
```
