1. 공용 캐시 계약 (ElastiCache Valkey)

앱들이 캐시 하나를 같이 쓸 때의 규칙. 프리픽스 체계와 강제 수단은 플랫폼(DevOps)이 정하고

지키는 건 앱팀 몫입니다 — 실패가 앱 경계를 넘기 때문(키 충돌·전체 삭제)에 개발 재량으로 두지 않습니다.

- *모든 앱은 캐시 키에 `

Unknown macro: {app}

:` 프리픽스를 붙이고, 이건 문서가 아니라 RBAC로 강제합니다.**

dev/prod 구분 없습니다. 컨벤션으로만 두면 안 지켜지고, 대가는 나중에 치릅니다 — 공용 클러스터를

앱별로 나눠야 할 때 프리픽스가 없으면 ***어느 키가 어느 앱 건지 구분이 안 돼*** 분리가 추측 작업이 됩니다.

dev를 포함하는 이유는 키 이름이 dev에서 정해지기 때문입니다.

공용 DB(`common-dev-db`)·공용 MQ와 같은 원칙 — ***기본은 공유***, 분리는 근거가 있을 때만.

—

1. 
    1. 테넌트 규칙

1. ***프리픽스를 등록하고 모든 키에 붙인다*** — `

Unknown macro: {앱/제품명}

:`. ***다른 앱 프리픽스는 읽지도 쓰지도 않는다.***

두 앱이 정말 같은 키를 봐야 하면 아래 `shared:` 건입니다.

2. ***`FLUSHALL`/`FLUSHDB` 금지.*** ACL이 막지만 그걸 기대하는 코드를 쓰지 마세요.

자기 데이터 정리는 자기 프리픽스 `SCAN` + 삭제.

3. ***모든 키에 TTL.*** 공용 메모리라 안 지워지는 키는 남의 여유분을 갉아먹습니다.

4. ***자기 유저로 인증한다.*** 익명 접속은 default 유저를 잠그는 시점에 끊깁니다(아래 롤아웃).

5. ***TLS 필수*** — `rediss://`.

1. 
    1. 
        1. 프리픽스 레지스트리
    2. 

| 프리픽스 | 소유 | 비고 |
| --- | --- | --- |
| — | — | — |
| `gw:` | vt-api-gateway (core/admin/receiver/dispatcher 4개 공유) | 처음부터 강제 적용. 키 카탈로그 = 앱 레포 `design/redis/redis-keyspace.md` |
| `ezcloud:` | ezcloud api-server + 워커 5개 | ***예약만, 미적용.*** POC 키에 프리픽스가 없어서 지금 이 유저로 AUTH하면 앱이 깨집니다. 키 정리 → 유저 전환 순 |

앱 추가 = 이 표에 한 줄 + `local.shared_valkey_tenants`(`envs/dev/data/elasticache_rbac.tf`) 항목.

등록이 코드보다 먼저입니다.

단위는 ***배포가 아니라 키스페이스***입니다. vt-api-gateway는 4개 배포가 캐시 상태를 의도적으로

공유하므로 `gw:` 하나를 씁니다.

—

1. 
    1. 앱 간 공유 (`shared:`)

기본 금지입니다. 예외는 하나 — 여러 앱이 ***같은 값을 봐야만 의미가 있는*** 상태.

SSO 세션이 대표적입니다. 앱마다 자기 프리픽스에 복제하면 한 앱에서 로그아웃해도

다른 앱 세션이 살아있습니다. 여기서 복제는 우회책이 아니라 버그입니다.

그래서 `shared:` 네임스페이스 하나를 두고 ***소유 앱만 쓰기 / 나머지는 읽기 전용***으로 가릅니다.

```

1. 소유 앱 (읽기+쓰기)on ~oneid:* &oneid:* ~shared:* &shared:* +@all -@dangerous …
2. 소비 앱 (읽기만)on ~app2:* &app2:* %R~shared:* &shared:* +@all -@dangerous …```

`%R~`가 Redis 7 / Valkey의 읽기 전용 키 패턴입니다. 소비 앱은 읽되 덮어쓰거나 지우지 못합니다.

- **주의: 채널 패턴 `&`에는 읽기 전용이 없어서, `&shared:**`를 받은 소비 앱은 발행도 됩니다.

방향이 중요하면 채널 이름을 방향별로 나누세요.

- **규칙은 하나 — 쓰는 앱은 1개.**소유자가 둘이 되는 순간 추적 불가능한 중복으로 되돌아갑니다.

`shared:` 아래를 `shared:<도메인>:`으로 또 나누지 않습니다. 분류할 게 아직 없고, 실제 키는

어차피 `shared:session:

Unknown macro: {id}

`처럼 생겨서 나중에 소유자가 둘이 되면 그때 그 세그먼트로 쪼개면 됩니다.

- **절차**: 양쪽 앱의 `shared_write`/`shared_read`와 아래 표를 추가하는 PR + 두 팀 합의.

접속 문자열은 안 바뀝니다 — 유저는 그대로고 서버 쪽 권한만 붙습니다.

1. 
    1. 
        1. 공유 네임스페이스 레지스트리
    2. 

| 키 | 소유(쓰기) | 소비(읽기) | 공유해야 하는 이유 |
| --- | --- | --- | --- |
| — | — | — | — |
| *(아직 없음)* |  |  |  |

—

1. 
    1. 어떻게 강제되나

테넌트마다 자기 프리픽스(+ 위 `shared:`)로 스코프된 ElastiCache 유저를 받습니다.

```

on ~gw:* &gw:* +@all -@dangerous +info +client|setinfo +client|setname

```

- `~gw:**` / `&gw:**` — 자기 프리픽스의 키·pub/sub 채널만.
- `-@dangerous` — ***전체 삭제를 막는 게 이 부분입니다.**`FLUSHALL`/`FLUSHDB`는 키 스코프 명령이아니라서 `~패턴`으로 안 막힙니다. `+@all`이면 패턴과 무관하게 그룹 전체를 날릴 수 있어요.`KEYS`·`CONFIG`·`SHUTDOWN` 등도 같이 빠집니다. `SCAN`은 @dangerous가 아니라 자기 키 정리는 됩니다.
- `+info +client|setinfo +client|setname` — @dangerous에 있지만 ***클라이언트 접속 핸드셰이크**라되돌려준 것들입니다(ioredis는 접속 시 `INFO`, 5.3+는 `CLIENT SETINFO` 전송). 빠지면 명령 하나실패가 아니라 ***연결 자체가 안 됩니다.**→ 새 테넌트는 ***실제 접속 테스트 먼저**.

인증은 유저명 + 비밀번호입니다. 비밀번호는 ***Terraform이 생성***하고(영숫자 32자 — URL에 들어가니

`@ : / #` 회피), `terraform output -json shared_dev_valkey_user_passwords`로 꺼내

앱 `dev/<app>` 시크릿의 `rediss://<user>:<password>@<endpoint>:6379`에 넣습니다.

tfvars로 받지 않는 이유: tfvars 값이든 생성값이든 ***어차피 state에 들어갑니다***(파일은 git에서만

가려줄 뿐). 그런데 tfvars로 받으면 CI PR 검증(tfvars 없음)에서 plan이 깨집니다. 생성이 사람 손도

줄이고 CI도 삽니다. 회전은

`terraform apply -replace='random_password.shared_valkey_user"<prefix>"'` 후 앱 시크릿 갱신

(유저는 in-place 갱신이라 시크릿 갱신 전까지 그 앱은 인증 실패).

대안은 IAM 인증(`authentication_mode

Unknown macro: { type = "iam" }

`) — 장수명 비밀번호가 없어지는 대신

앱마다 토큰 생성기 + 15분 갱신이 필요합니다. prod에서 재검토.

- **Redis DB 인덱스(`SELECT 0-15`)는 대체재가 아닙니다**— 아무나 다른 인덱스로 옮겨갈 수 있고

cluster mode에서는 못 씁니다.

1. 
    1. 
        1. 부착은 롤아웃이 아니라 컷오버입니다 (Valkey 제약)
    2. 

ElastiCache는 user group에 반드시 `default` 이름의 유저를 요구합니다 — 미인증 접속이

떨어지는 신원이 그겁니다. 원래는 이 `default`를 ***nopass***로 두면 미인증 클라이언트가 계속

동작해서, 앱별로 천천히 전환하는 무중단 롤아웃이 가능합니다.

- **Valkey 엔진에서는 안 됩니다.**실제 apply에서 확인됨(2026-07-27):

```

InvalidParameterCombination: No-password-required is not allowed for a user with engine Valkey

```

즉 그룹 멤버 전원이 비밀번호를 가져야 하고, 그래서 **user group을 붙이는 순간 AUTH 안 하는

클라이언트는 전부 거부**됩니다. 중간의 관대한 상태가 존재하지 않습니다.

그래서 부착은 `var.valkey_attach_user_group`(기본 ***false***) 뒤에 두었습니다. 유저와 그룹은

미리 만들어 두되 캐시에는 안 붙입니다. 실제 순서는:

1. ***유저·그룹 생성***(현재 상태). 캐시는 그대로라 운영 중인 앱에 영향 없음.

2. ***모든 테넌트가 키 프리픽스 적용 + 자기 자격증명을 시크릿에 배포.***

아직 인증은 안 되지만(그룹 미부착) 준비는 끝난 상태.

3. ***`valkey_attach_user_group = true`로 컷오버.*** 이 시점에 전 앱이 동시에 인증 모드로 전환됩니다.

준비 안 된 앱은 즉시 장애이므로 ***창을 잡고 한 번에*** 해야 합니다.

미리 붙여놓고 앱을 하나씩 옮기는 건 불가능합니다 — 그룹 부착 전엔 AUTH할 유저가 없고,

부착 후엔 미인증으로 못 붙습니다. Valkey에서는 그 사이가 없습니다.

(`aws elasticache describe-users`로 AWS가 미리 만든 nopass `default` 유저를 Valkey 그룹에

넣을 수 있는지 확인 중입니다. 가능하면 위 3단계가 무중단 롤아웃으로 되돌아갑니다.)

—

1. 
    1. 언제 전용 그룹을 주나
- **dev: 안 줍니다.**전부 공용 하나, 대신 프리픽스 강제는 prod와 동일.
- **prod: 앱별로 갈립니다.**판단 기준은 플랫폼팀이 별도 관리. 어느 쪽이든 프리픽스와 RBAC는

유지됩니다 — 그게 나중에 분리를 가능하게 하는 전제입니다. 출발점:

1. ***키 이름을 못 바꾸는 앱*** — 키 스킴 고정된 서드파티/OSS 이미지(`eslockserver`).

2. ***그룹 단위 설정이 달라야 하는 앱*** — TLS on/off, keyspace notification, `maxmemory-policy`는

키가 아니라 그룹 속성입니다. (prod의 vt-api-gateway: `gw:jti:**`·`gw:revoked:**`가 evict되면

보안 창이 열려 `noeviction`이 필요한데, 그러면 메모리 full일 때 같은 그룹 다른 앱의 쓰기가 전부 실패.)

3. ***데이터 등급이 다른 앱*** — 자격증명 캐시(vt-api-gateway는 webhook HMAC 시크릿·타겟 OAuth 토큰)와

단순 콘텐츠 캐시를 같이 두는 건 사이징이 아니라 데이터 분류 문제입니다.

셋 다 아니면 공용입니다.

—

1. 
    1. 공용 그룹 온보딩 절차

1. 레지스트리에 프리픽스 등록 + `local.shared_valkey_tenants` 항목 추가.

`shared_write`/`shared_read`는 정말 공유 건이 있을 때만.

2. apply. 비밀번호는 Terraform이 생성합니다(`random_password`, 영숫자 32자) —

tfvars에 넣을 것도, CI 변수도 없습니다.

값 확인: `terraform output -json shared_dev_valkey_user_passwords`

3. 공용 그룹 SG에 앱 pod SG 참조 6379 ingress 추가(`envs/dev/apps/security_group_rules.tf`).

4. 앱 `dev/<app>` 시크릿에 `rediss://<prefix>:<password>@<엔드포인트>:6379` 주입(TF 밖).

5. 앱팀 확인: 키 프리픽스·TTL, 그리고 ***ACL 상태에서 클라이언트가 실제 접속되는지***.

용량은 계속 보세요 — `cache.t3.micro`(0.5 GiB) 하나를 전부가 나눠 씁니다.

메모리 많이 쓰는 테넌트를 붙이기 ***전에*** `node_type`을 올립니다.