# VT API Gateway — SSOT 스펙 작업 폴더

> 본 폴더는 **SSOT(SRS·One Pager) 작성·AI dev-chain 초안 공간**이다.
> `scp-architecture`는 **개인 GitHub** repo이므로 *공식 리뷰·승인 장소가 아니다*.
> 작성은 여기서, **공식 리뷰·baseline 등록**은 아래 §등록 위치를 따른다.
>
> 스펙 단위 정본: [PRD §12.1](<../VT API Gateway — PRD (v2).md>) · 작성 전략: [프로젝트 진행·문서 전략](<../VT API Gateway — 프로젝트 진행·문서 전략.md>)

## 폴더 구조 (스펙 단위 = PRD §12.1)

> 제품 적응(③-P*)·인프라(③-I) 할당·소유는 [실행 할당표(조정 인덱스)](00-execution-allocation.md) 참조.

| 폴더 | 스펙 | 문서 유형 | 단계 |
|------|------|-----------|------|
| `01-onepager-api-compatibility/` | ① API 호환성 | Engineering One Pager | 1단계 |
| `02-onepager-presigned-url/` | ② Presigned URL | Engineering One Pager | 2단계 |
| `03-srs-gateway/` | ③ GW 일원화 + 멀티 Region (계약 SSOT) | SRS (메인) | 3+4단계 |
| `03c-subsrs-gw-console/` | ③-C GW Console | Sub-SRS (③ 하위) | 4단계 |
| `03p-cs-cleverspace/` | ③-P-CS CleverSpace 적응 | Sub-SRS 또는 One Pager | 3+4단계 |
| `03p-co-cleverone/` | ③-P-CO CleverOne 적응 | One Pager | 3+4단계 |
| `03p-ez-ezserver/` | ③-P-EZ EzServer 적응 | One Pager | 3+4단계 |
| `03i-infra/` | ③-I GW Infra 구축 | IaC 구축 계획서 | 3+4단계 |
| `04-subsrs-straumann-axs/` | ④ Straumann(AXS) | Sub-SRS (③ 하위) | 5단계 |

## 작성 순서

1. **③ SRS 골격** (부모·기준점) — §1.2 Scope/Why, §2.1·§2.2 아키텍처·시퀀스
2. **① One Pager** (가장 긴급, CleverSpace v1.3.0 연동) · **② One Pager** 병행
3. ③ SRS baseline 후 → **④ Sub-SRS** · **③-C Sub-SRS**
4. PHASE 1: DBML → Swagger → Unit TCL → IP

> 구현 순서(Straumann → CleverSpace)와 **스펙 순서는 다르다.** 부모 ③ SRS가 먼저 닫혀야 ④가 그 위에 올라간다.

## 작성 → 리뷰 → 등록 워크플로우

```
[작성·초안]                [공식 리뷰·승인]            [감사·공유]
scp-architecture     →     공식 저장소(아래)      →     VKS(Confluence)
(개인 GitHub, MD)          (PR diff / 페이지 리뷰)       추출·게시·baseline 증적
```

## 등록 위치 (공식 리뷰처) — 확정 (2안)

> 2안: SRS류는 Azure(git PR), One Pager는 VKS(Confluence)에서 저장·리뷰.

| 스펙 | 작성(개인) | 공식 리뷰·등록 (확정) |
|------|-----------|------------------------|
| ① One Pager | `specs/01-...` | **VKS(Confluence)** 페이지 저장·리뷰 |
| ② One Pager | `specs/02-...` | **VKS(Confluence)** 페이지 저장·리뷰 |
| ③ SRS | `specs/03-...` | **vt-api-gateway** (Azure, es-platforms) `docs/specs/` (PR 리뷰) |
| ③-C Sub-SRS | `specs/03c-...` | **vt-api-gateway-console** (미생성, 생성 전 vt-api-gateway `docs/`) (PR 리뷰) |
| ④ Sub-SRS | `specs/04-...` | **vt-api-gateway** `docs/specs/` (③ 하위, PR 리뷰) |

> 공통: SRS류 정본은 Azure(git, baseline 태그). **추출본 게시는 하지 않고**, 필요 시 VKS PRD/ARD에서 **git URL 링크로 참조**한다. One Pager는 VKS에서 작성·리뷰하므로 그 자체가 통제 게시.

## 초안 완료 후 이관 규칙 (단일 SSOT · 드리프트 0)

> **핵심: 같은 파일을 두 곳에 두지 않는다.** 초안이 완료(baseline 직전)되면 **본체를 공식 저장소(Azure git)로 이동**하고, `scp-architecture` 쪽 자리는 **URL 포인터로 교체**한다. 파일을 복제(또는 심볼릭/하드 링크)하지 않는다 — 복제는 드리프트의 원인이며, git 2개 레포 사이 링크는 clone·CI·Confluence에서 깨진다.

1. **작성 단계**: `scp-architecture/docs/VT_API_Gateway/08.VT_API_Gateway/specs/`에서 자유롭게 작성·수정한다(개인 초안).
2. **이관 단계(초안 완료 시)**: 산출물(SRS·Sub-SRS·`design/openapi`·`design/dbml`)을 **공식 저장소로 PR 이관**한다.
   - SRS류·design 산출물 → **vt-api-gateway** `docs/specs/` (Azure git, PR 리뷰·baseline 태그)
   - One Pager(①②) → **VKS(Confluence)** 페이지
3. **포인터 교체**: 이관 후 `scp-architecture` 쪽 원본 파일은 **삭제하거나, 공식 URL 안내문 1개로 축소**한다. 이후 본문 수정은 **공식 저장소에서만** 한다(§1.5가 이미 이 방식 — 로컬 경로 대신 Azure/VKS URL 링크).
4. **참조 일관성**: 다른 문서에서 인용할 때는 **파일 경로가 아니라 공식 URL**로 링크한다. baseline 이후 정본은 git 태그가 증적이다.

> 결과: 본문은 **공식 저장소 한 곳에만** 존재하고, `scp-architecture`·VKS·PRD/ARD는 **URL로 참조**만 한다. "동일 파일 2벌"이 생기지 않는다.
