# Section View PoC를 Cloud Web Viewer 에 반영한다.

## Description

**Background**

- [ESCV-138](https://vts.vatech.com/browse/ESCV-138)을 통해 Clever Space v1.3.2 Cloud Web Viewer용 Section View 모듈 구현·기획팀 테스트가 완료되면, 본 이슈에서 **Cloud Web Viewer(`cloudwebviewer`)에 접목(embed)** 한다.
- 접목 범위·절차·정합 요건의 **정본**은 [Section Module OnePager](./Section-Module-Spec-v1.3.2-OnePager.md)([VKS](https://vks.vatech.com/x/UecSEw)) **§9**(특히 §9.9 실행 절차)이다.

**Purpose**

- Section View PoC를 Cloud Web Viewer에 반영하여 Clever Space에서 Section Layout을 사용할 수 있게 한다.

**Process**

1. [ESCV-138](https://vts.vatech.com/browse/ESCV-138) 인계물(패키지·공개 API·[데모](http://scp-section-demo.test.scp.esclouddev.com)·OnePager §10)을 수령한다.
2. OnePager **§9.9**에 따라 `scp-section-poc` 소스를 `cloudwebviewer` 모노레포에 **소스 병합**한다(`section-core` 내부 패키지·`section` 뷰 병합·스코프 `@cloudwebviewer/*`). PoC 데모 셸(`apps/section-demo`)은 **이동하지 않는다**.
3. CW 셸에 Section을 연결한다 — ContentHandler 등록·Store/Toolbar 배선·CT provider·Title bar/다이얼로그·Save/Load prj 어댑터(§9.4~9.8·§9.7). **§9.10**에 따라 CW 정본으로 중복 제거(Pointer·계측 편집·커서 등). **§9.9 9단계** MPR 연동(Scout Th/INT·Image Adjust 동기, §12-D18).
4. 접목·통합 검증 중 이슈는 **[ESCV-139](https://vts.vatech.com/browse/ESCV-139) Sub-Task**로 등록한다 (1건 = 1 Sub-Task). **OnePager·MMI 근거·재현·스크린샷** 포함.
5. [EzCloud Test 컨테이너](https://container.test.ezcloud.ezcld.net/)에서 Clever Space 내 Toolbar·ContentTitleBar·Pan/Zoom·계측 UX 정합을 확인하고 완료한다(§9.9 10단계).

**Considerable Factors**

- **접목 원칙(§9.1):** CW vtk 파이프라인(`Layout3DPAN` 등)은 사용하지 않는다. **`SectionViewer` WebGL 컴포넌트를 CW content로 embed**한다.
- **절차·매핑:** OnePager §9.9(실행)·§9.10(중복 제거)·§9.7(embed 매핑)·§7(prj)을 따른다. prj 필드·MPR 연동 범위는 §12-D5·D18 확정 후 어댑터를 완성한다.
- **CW 선행 개선 권고(§9.11):** CW-1 폰트 override(`!important`)·CW-2 i18n(한국어 카탈로그) — 접목 품질에 영향, 가능하면 접목 전 CW에서 처리.
- **저장소:** 인계 원본 [scp-section-poc](https://dev.azure.com/ewoosoft/prototypes/_git/scp-section-poc) · 접목 대상 [cloudwebviewer](https://dev.azure.com/ewoosoft/cloudwebviewer/_git/cloudwebviewer).
- **지원:** Section 모듈 팀(ESCV-138)은 인계·기술 지원. 기획팀 QA는 ESCV-138 단계(데모 사이트)에서 선행.

**Result Image**

- Section View가 Cloud Web Viewer에 반영되어 Clever Space CT Viewer에서 MPR/Section Layout 전환·Section 진단 워크플로를 사용할 수 있다.
