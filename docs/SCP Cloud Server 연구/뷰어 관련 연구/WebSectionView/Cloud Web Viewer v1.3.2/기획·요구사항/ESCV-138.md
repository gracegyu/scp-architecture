# Cloud Web Viewer의 Section View PoC를 제품화에 필요한 추가 구현을 진행한다.

## Description

**Background**

- [PLAN-1287](https://vts.vatech.com/browse/PLAN-1287)을 통해서 Cloud Web Viewer MMI 리뷰를 진행하였고, 이를 토대로 Section View PoC의 추가 구현이 필요하다.
- 구현·테스트·인계의 **요구사항 정본**은 [Section Module OnePager]({VKS})([VKS](https://vks.vatech.com/x/UecSEw))이다.

**Purpose**

- Cloud Web Viewer의 Section View PoC를 제품화에 필요한 추가 구현을 진행한다.

**Process**

1. Section View 추가 구현을 진행한다 (`scp-section-poc`, [데모](http://scp-section-demo.test.scp.esclouddev.com)).
2. 구현 완료 후 기획팀이 데모 사이트에서 **OnePager Spec** 기준으로 기능·UX를 테스트한다.
3. 테스트 중 발견된 버그/이슈는 **[ESCV-138](https://vts.vatech.com/browse/ESCV-138) Sub-Task**로 등록한다 (1건 = 1 Sub-Task). 등록 시 **재현 절차·기대 결과(OnePager·MMI 근거)·실제 결과·스크린샷**을 포함한다.
4. 이슈 반영 후 Cloud Web Viewer 접목 가능 상태로 인계한다. **접목(소스 병합)은 CW 팀** 소관이며, 본 이슈 팀은 인계·지원한다.

**Considerable Factors**

- 구현·테스트·버그 판정 시 [Section Module OnePager]({VKS})([VKS](https://vks.vatech.com/x/UecSEw))를 참조한다. 접목 절차는 OnePager §9.9.
- Cloud Web Viewer의 개발환경과 동일한 개발환경에서 PoC를 구현하여 제품화에 이슈를 최소화하도록 한다.
    - Cloud Web Viewer의 vtkjs-wrapper 소스 저장소: https://dev.azure.com/ewoosoft/_git/cloudwebviewer?path=/lib/vtkjs-wrapper
- Section PoC 소스 저장소: https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc

**Result Image**

- Section View PoC가 제품화에 필요한 기능 구현이 완료되어 Cloud Web Viewer에서 적용할 수 있는 상태가 된다.


# comment by Raymond

**To. Jessi**

Section View PoC 추가 구현이 **7/16 완료**되어, 기획팀 검증을 요청드립니다.

이번 구현 범위는 **Scout + Panorama + 3×3 Section** 전체이며, 데모 사이트에서 바로 확인하실 수 있습니다.

- **데모 사이트:** http://scp-section-demo.test.scp.esclouddev.com
- **기준 문서(정본):** [Section Module OnePager — VKS](https://vks.vatech.com/x/UecSEw)

**요청 드리는 것**

데모 사이트를 **OnePager Spec 및 MMI 기준**으로 검토하시고, 아래에 해당하는 항목을 등록해 주세요.
- **버그** — Spec/MMI대로 동작하지 않는 것
- **누락** — Spec/MMI에 있는데 구현되지 않은 것
- **개선사항** — Spec/MMI에는 없지만 제품화를 위해 필요하다고 판단되는 것

**등록 방법** (§Process 3)

- **1건 = 1 Sub-Task**로 본 이슈([ESCV-138](https://vts.vatech.com/browse/ESCV-138)) 하위에 등록해 주세요.
- 각 Sub-Task에는 다음을 포함해 주세요.
    - **재현 절차** (어떤 화면에서 무엇을 했는지)
    - **기대 결과** (OnePager·MMI 근거, 가능하면 해당 항목/절 번호)
    - **실제 결과**
    - **스크린샷** (가능한 경우)
- 버그/누락/개선 **구분**을 라벨 또는 제목에 표시해 주시면 우선순위 정리에 도움이 됩니다.

**참고**

- OnePager에는 MMI에 정의되지 않아 개발실에서 정한 값·동작(예: Initialize All 의미, 국제화 범위 등)이 §3.4·§12 Decision Log에 정리되어 있으니, 관련 판정 시 함께 참조 부탁드립니다.
- 접목(소스 병합)은 CW 팀 소관이며, 본 이슈 팀은 인계·지원합니다. 검증 중 궁금한 점은 언제든 편하게 문의 주세요.

