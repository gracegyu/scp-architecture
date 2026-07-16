# Cloud Web Viewer의 Section View PoC를 제품화에 필요한 추가 구현을 진행한다.

## Description

**Background**

- [PLAN-1287](https://vts.vatech.com/browse/PLAN-1287)을 통해서 Cloud Web Viewer MMI 리뷰를 진행하였고, 이를 토대로 Section View PoC의 추가 구현이 필요하다.
- 구현·테스트·인계의 **요구사항 정본**은 [Section Module OnePager](./Section-Module-Spec-v1.3.2-OnePager.md)([VKS](https://vks.vatech.com/x/UecSEw))이다.

**Purpose**

- Cloud Web Viewer의 Section View PoC를 제품화에 필요한 추가 구현을 진행한다.

**Process**

1. Section View 추가 구현을 진행한다 (`scp-section-poc`, [데모](http://scp-section-demo.test.scp.esclouddev.com)).
2. 구현 완료 후 기획팀이 데모 사이트에서 **OnePager Spec** 기준으로 기능·UX를 테스트한다.
3. 테스트 중 발견된 버그/이슈는 **[ESCV-138](https://vts.vatech.com/browse/ESCV-138) Sub-Task**로 등록한다 (1건 = 1 Sub-Task). 등록 시 **재현 절차·기대 결과(OnePager·MMI 근거)·실제 결과·스크린샷**을 포함한다.
4. 이슈 반영 후 Cloud Web Viewer 접목 가능 상태로 인계한다. **접목(소스 병합)은 CW 팀** 소관이며, 본 이슈 팀은 인계·지원한다.

**Considerable Factors**

- 구현·테스트·버그 판정 시 [Section Module OnePager](./Section-Module-Spec-v1.3.2-OnePager.md)([VKS](https://vks.vatech.com/x/UecSEw))를 참조한다. 접목 절차는 OnePager §9.9.
- Cloud Web Viewer의 개발환경과 동일한 개발환경에서 PoC를 구현하여 제품화에 이슈를 최소화하도록 한다.
    - Cloud Web Viewer의 vtkjs-wrapper 소스 저장소: https://dev.azure.com/ewoosoft/_git/cloudwebviewer?path=/lib/vtkjs-wrapper
- Section PoC 소스 저장소: https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc

**Result Image**

- Section View PoC가 제품화에 필요한 기능 구현이 완료되어 Cloud Web Viewer에서 적용할 수 있는 상태가 된다.

