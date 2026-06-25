**타One ID**

**Software Requirements Specification**

**Version: v1.0**

**Document Version: v1.0**

**Date: 2024-06-19**

**Writer: Ann (김가영)**

**EWOOSOFT Co., Ltd.**

# 1 Introduction (개요)

## 1.1 Purpose (목표)

- 이 문서는 통합 계정 관리 및 관리자 백오피스 기능을 제공하는 OneID에 대한 문서이다.\
  이하, OneID를 내부에서 구축하기 위한 스펙을 작성한다.

## 1.2 Product Scope (범위)

- ES에서 제공하는 제품(Cloud/Desktop)의 통합 계정 관리 및 관리자 백오피스를 제공한다.
  - 다양한 제품을 하나의 계정으로 이용할 수 있게 하여 사용 경험 및 접근성을 향상 시킨다.

  - 사용자 데이터를 법규에 따라 중앙화 된 시스템에서 관리하고 감사 기능을 제공하여 보안 수준을 강화한다.

  - 관리자 백오피스 기능을 통해 사용자 모니터링 및 관리 기능을 제공하여 운영 효율성을 향상시키고, 수집된 데이터를 전략적인 결정의 근거 자료로 활용할 수 있는 기반을 마련한다.

- Identity Service, User Console, Admin Console, API Server 로 구성된다.
  - Identity Service
    - 계정 ID와 Password를 관리하고 다양한 인증 메커니즘을 통해 사용자의 신원을 확인할 수 있는 Server와 Web Page를 제공한다.

- Keycloak (Open Source Identity Solution: <https://www.keycloak.org/>)을 이용한다.

- v1.0은 ID + Password 인증과 Social Login(Google)을 지원한다.
  - v1.0은 다단계 인증(MFA)은 지원하지 않는다.

  - Single Sign-On (SSO)을 지원한다.

  <!-- -->
  - 이전 계정과의 혼동을 방지하고 데이터를 보호하기 위해 탈퇴한 계정의 이메일로 재가입할 수 없다.

  <!-- -->
  - User Console
    - 서비스 사용자의 계정 관리 및 테넌트 관리 기능을 지원하는 WebApp을 제공한다.

    - 테넌트란 서비스를 구독하는 주체로 개별 고객(개인) 또는 조직을 의미하며, 소유자 1인과 0명 이상의 멤버로 구성된다.
      - 계정은 복수의 테넌트에 소속될 수 없다.
        - 계정이 복수의 테넌트에 소속될 수 있어야 한다는 요구사항이 있었지만, 기능의 가치에 비해 복잡성이 높아 지원하지 않기로 결정했다.

        - 이후 버전에서 복수의 테넌트를 지원하기 위해서는 대규모의 재설계 및 변경이 필요하므로, 수정 규모 대비 비즈니스 가치를 평가하여 지원 여부를 결정해야 한다.

    - v1.0은 테넌트의 계층 구조를 지원하지 않는다.
      - 테넌트의 계층 구조에 대한 요구사항(ex. DSO, 네트워크 치과)이 있었지만, 구체적인 요구사항 및 사용 사례가 확인되지 않아 v1.0에서는 지원하지 않기로 결정했다. (next)

  - Admin Console
    - 관리자의 계정 관리 및 서비스 운영을 위해 필요한 기능을 지원하는 백오피스 Web App을 제공한다.

  - API Server
    - Web App에 서비스를 지원하는 Rest API Server를 제공한다.

- Global Service로 제공하며 타겟 국가는 [Confidential_OneID_v1.0_Countries.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EQOYDigMDmJEk024q2ItAFMBKMIIOBcw4acVpHklNT77_A?e=4tDJr1)을 참고한다.

- 타겟 국가 리스트는 VCSM(바텍 고객 지원 시스템) 및 LMP(License Management Portal)에 등록된 국가를 기준으로 정의되었다.

- v1.0은 2024년 출시 예정인 EzCloud v1.0 및 ES의 Desktop 제품군(EzDent-i 등)에서 사용할 예정 이다.

- v1.0을 사용 예정인 제품에서 유료 서비스를 제공할 계획이 없으므로, 유료 서비스를 고려하지 않는다. (next)

- 관계사(바텍네트웍스 내 타 계열사)에서 제공하는 제품에서 OneID를 활용할 계획이 있으나, 구체적인 요구사항은 현 시점에서 예측할 수 없다. 따라서 v1.0에서 고려하지 않는다.

## 1.3 Document Conventions (문서규칙)

본 문서는 다음과 같은 문서 규칙을 따른다.

- 우선순위
  - 각 기능의 중요도에 따라 아래와 같이 3가지 Priority로 표시한다.
    - P1: 높음, 중요한 기능으로 반드시 구현해야 함.

    - P2: 보통, 일반적인 기능으로 구현해야 함.

    - P3: 낮음, 부가적인 기능으로 필요 시 배제할 수 있음.

  - Priority가 표시되지 않은 항목은 P1로 간주한다.

  - 우선순위의 표시는 해당 항목의 문장 뒤에 (P2)와 같이 표시한다.

- 버전 별 지원 계획 표기 방법
  - 이번 버전에서 지원하는 항목은 별도의 표시를 하지 않는다.

  - 지원 계획이 정해지지 않았고 미래에 지원할 항목은 문장의 뒤에 (Next)를 표시한다.

## 1.4 Terms and Abbreviations (정의 및 약어)

- ES: 이우소프트㈜의 약어

## 1.5 Related Documents (관련문서)

- MRD: VKS \> [OneID MRD](https://vks.vatech.com/display/ES/OneID+MRD)

- MMI: Share Point \> [Confidential_OneID_v1.0_MMI_Kor.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/EbvE-_1_X7ZJi0C-9MNNHtgBsx4u1wTTlqhyBM7xyrOUTg?e=NGo4no)

- SDS
  - Diagrams: Share Point \> [Confidential_OneID_v1.0_Diagrams.vsdx](https://vatechcorp.sharepoint.com/:u:/s/es/EWRSfiC_vRlJkCM_FghmSnEB2NLDnESSb9QozAQF4zLKHA?e=bKwbb5)

  - DB: Share Point \> [Confidential_OneID_v1.0_DBSchema.png](https://vatechcorp.sharepoint.com/:i:/s/es/EcziHkCvx4ZNirDX2CVMBFkBEqdnug1dzZZw1nbK-yQN-A?e=4JvwvC)

  - Rest API: Share Point \> [Confidential_OneID_v1.0_RestApi.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/ET7AgeivUQFDuRq4HCc3QU0Biik-w7LkUlAgpdypWNiG4A?e=nRioPK)

## 1.6 Intended Audience and Reading Suggestions (대상 및 읽는 방법)

표 1은 본 프로젝트에 참여하는 부서 및 인력 별로 본 문서를 활용하는데 있어 참고하거나 숙지해야 할 항목이다.

| 역할 Chapter                     | PM  | TL  | SW 개발자 | UI 디자인 | 기획/ 마케팅 | QA  | 영업 | SE  |
| -------------------------------- | --- | --- | --------- | --------- | ------------ | --- | ---- | --- |
| 1.Introduction                   | ◉   | ⚪  | O         |           | ⚪           | O   |      |     |
| 2.Overall Description            | ◉   | ⚪  | ⚪        | ⚪        |              | ⚪  | ⚪   | ⚪  |
| 3.Environment                    | ⚪  | ⚪  | ⚪        |           |              | ⚪  |      | ⚪  |
| 4.External Interface Requirement | ⚪  | ◉   | ⚪        | ⚪        |              |     |      |     |
| 5.Performance Requirement        | ⚪  | ◉   | ⚪        |           |              | ◉   |      |     |
| 6.Non-Functional Requirement     | ⚪  | ◉   | ⚪        |           |              | ⚪  |      |     |
| 7.Functional Requirement         | ⚪  | ⚪  | ⚪        | ⚪        |              | ⚪  |      |     |
| 8.Change Management Process      | ⚪  | ⚪  |           |           | ⚪           |     |      |     |
| 9.Document Approval              | ⚪  |     |           |           |              |     |      |     |

: 표 1 대상 및 읽는 방법 정의

- 범례
  - ◉: 거의 암기해야 한다.

  - ⚪: 완전히 숙지해야 한다.

  - 빈칸: 시간이 남으면 읽어봐도 된다.

- 역할
  - PM: Project Manager

  - TL: Technical Leader

  - SW 개발자: 분석/설계/구현 담당자

  - UI 디자인: UI 담당자

  - 마케팅: 기획 및 마케팅 담당자

- QA(Quality Assurance): 기능 테스트 수행 및 품질 담당자
  - 영업: 바텍 글로벌 영업 담당자

  - SE: Technical Support

## 1.7 Project Output (프로젝트 산출물)

### 1.7.1 Output Format (산출물 형태)

- Identity Service
  - Container Image

  - Custom Theme File

- Keycloak 설정 가이드

- User Console
  - 웹브라우저로 접근할 수 있는 Web Application (React)

- Admin Console
  - 웹브라우저로 접근할 수 있는 Web Application (React)

- API Server
  - Container Image

  - Node.js Backend Application

  - API document

- Infra
  - EKS 배포를 위한 docker, manifest file

- IaC(Infrastructure as Code) 이용하여 자동으로 구축된 AWS Infra

### 1.7.2 Output Name and Version (산출물명(가칭) 및 버전)

- Identity Service

- ESIdentityService v1.0

- User Console

- ESUserConsole v1.0

- Admin Console

- ESAdminConsole v1.0

- API Server

- ESAPIServer v1.0

### 1.7.3 Patent Information (특허 출원 유무 및 내용)

- 특허 출원할 내용 없음

# 2 Overall Description (전체 설명)

## 2.1 Product Perspective (제품 조망)

## 2.2 Overall System Configuration (전체 시스템 구성)

![A diagram of a network Description automatically
generated](./images/media/image1.png){width="6.6930555555555555in" height="6.014583333333333in"}

## 2.3 Overall Operation (전체 동작방식)

- [테넌트 가입]{.underline}
  - User Console은 API Server에 테넌트 가입을 요청한다.

  - API Server는 DB에 테넌트 및 소유자 정보를 저장하고, Identity Service에 테넌트 소유자 계정 생성을 요청하여 소유자 계정을 생성한다.

- [테넌트 탈퇴]{.underline}

- User Console은 API Server에 테넌트의 서비스(ex: EzCloud) 구독 정보를 조회한다.
  - User Console은 조회한 정보 중, 구독 해지 URL을 이용하여 서비스 구독 해지 화면으로 이동한다.
    - 이후 버전에서 유료 플랜을 지원하는 경우, 탈퇴 시 사용자가 직접 구독 리스트를 확인하고 해지한 후 탈퇴해야 한다.

    - 서비스 구독 해지 화면은, 구독 해지 후 User Console의 탈퇴 페이지로 이동할 수 있는 Back button을 제공해야 한다.

  - 서비스 구독 해지 후 User Console 탈퇴 페이지로 이동하면, User Console은 API Server에 테넌트 멤버 삭제 및 테넌트 탈퇴를 요청한다.

  - API Server는 테넌트 멤버 및 관련 데이터를 삭제한다.

- [관리자/테넌트 멤버 가입 초대]{.underline}

- Admin Console/User Console(이하, Console로 칭함)은 API Server에 초대를 요청한다.
  - API Server는 DB에 초대 이력을 저장하고, AWS SES에 이메일 전송을 요청하여 초대 메일을 전송한다.

- [관리자/테넌트 멤버 가입]{.underline}
  - Console은 API Server에 가입을 요청한다.

  - API Server는 DB에 사용자 정보를 저장하고, Identity Service에 사용자 계정 생성을 요청하여 사용자 계정을 생성한다.

- [관리자/테넌트 멤버 탈퇴]{.underline}
  - Console은 API Server에 탈퇴를 요청한다.

  - API Server는 DB에서 관련 정보를 삭제(계정 정보는: soft delete, 이외는 : hard delete)하고, Identity Service에 계정 삭제를 요청하여 사용자 계정을 삭제한다.

- [로그인]{.underline},
  - Console/App Services는 Identity Service의 Login Page로 이동하여 사용자를 인증하고 Access Token을 발급 받는다.

- [로그아웃]{.underline}
  - Console/App Services는 Identity Service에 로그아웃을 요청하고, Identity Service는 로그아웃 처리한다.

- [테넌트/관리자 관리]{.underline}
  - Console은 API Server에 테넌트/관리자 정보 조회/수정/삭제를 요청한다.

  - API Server는 DB에서 데이터를 처리한다.

- [참고]{.underline}: EzCloud 동작 방식
  - 테넌트 가입/구독

- 테넌트 소유자가 EzCloud에 최초 로그인 후 약관에 동의한다.

- EzCloud v1.0은 약관 동의 시점에 무료 플랜을 부여한다. 이후 버전에서 유료 플랜 제공 시 동작방식을 변경해야한다.

- EzCloud는 테넌트에 무료 플랜을 부여하고 테넌트를 프로비저닝한다.

- EzCloud는 API Server에 구독 정보 저장을 요청하고, API Server는 DB에 정보를 저장한다.
  - 테넌트 사용자 가입/탈퇴

- 가입: 테넌트 사용자가 EzCloud에 최초 로그인하면, EzCloud에 사용자를 프로비저닝한다.

- 탈퇴: EzCloud는 주기적으로 삭제된 테넌트 사용자의 데이터를 삭제한다.\
  (OneID 계정은 삭제되었으므로 사용자의 서비스 접속은 불가능하다.)

## 2.4 Product Functions (제품 주요 기능)

- [Share Point \> Confidential_OneID_v1.0_Features.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EVNrpGi7tjVBtBbRkZbMmq4BPLPlvfhSlnKG3BP4NFDdAg?e=iIPPLj) 참고

## 2.5 User Classes and Characteristics (사용자 계층과 특징)

- 테넌트
  - v1.0의 테넌트는 Dental Clinic, Lab, 개인이다.

  - 테넌트 사용자
    - 테넌트의 소유자를 포함한 구성원으로, 역할에 따라 자원 접근 권한을 제한할 수 있다.
      - Owner (소유자)
        - 테넌트를 생성한 사용자 또는 테넌트 소유권을 이관 받은 사용자이다.

        - 테넌트의 모든 자원에 접근할 수 있는 권한을 부여한다.

      - Member (멤버)
        - 테넌트 소유자의 초대를 통해 가입한 구성원이다.

        - 테넌트의 일부 자원에 접근할 수 있는 권한을 부여한다.

- 서비스 관리자
  - 서비스를 관리/운영하는 관리자로, 역할 및 영업지역에 따라 자원 접근 권한을 제한할 수 있다.
    - 역할
      - Admin
        - 모든 테넌트 및 관리자 데이터에 접근할 수 있는 권한을 부여한다.

- OneID 서비스 개발/운영을 담당하는 ES 직원이 Admin에 해당한다.
  - Manager
    - Admin이 지정한 영업 지역내의 테넌트 및 관리자 데이터에 접근할 수 있는 권한을 부여한다.

    - 바텍네트웍스 법인의 법인장 또는 그에 준하는 역할을 보유한 운영자가 Manager에 해당한다.

  - Staff
    - Manager가 지정한 영업 지역내의 테넌트 데이터에 접근할 수 있는 권한을 부여한다.\
      서비스 관리자의 데이터는 접근할 수 없다.

    - 바텍네트웍스 법인의 소속 직원이 Staff에 해당한다.

  <!-- -->
  - 영업 지역 (Sales Area)
    - 바텍네트웍스의 해외 법인 기준으로 정의된 국가의 그룹이다.

    - 각 국가는 하나의 영업 지역에만 속할 수 있다.

    - 영업 지역의 상세 목록은 [Confidential_OneID_v1.0_Countries.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EQOYDigMDmJEk024q2ItAFMBKMIIOBcw4acVpHklNT77_A?e=4tDJr1) 문서를 참고한다.

- 접근 권한의 상세 정보는 아래 문서를 참고한다.
  - [Confidential_OneID_v1.0_Authorizations.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EcIU4CTu8ndHt6SBsKxf-9EByjyjGKIvWO9lxydXQjD2Sw?e=CFCyEX)

## 2.6 Assumptions and Dependencies (가정과 종속 관계)

- 이메일 전송을 위해 AWS SES를 이용한 메일링 시스템이 구축되어 있어야 한다.

- 로그 수집/분석을 위해 중앙 로그 수집 아키텍처가 구축되어 있어야 한다.

- AWS 인프라 구축은 외주 활용을 검토 중이다. 외주 활용이 불가한 경우 추가 검토가 필요하며, 내부 인력 활용 계획을 수립해야한다.

## 2.7 Apportioning of Requirements (단계별 요구사항)

- v1.0

- ES에서 2024년 내에 출시할 예정인 EzCloud v1.0 대응

- Next

- EzCloud 이후 버전의 과금 정책 대응
  - 관계사 제품 요구사항 대응

## 2.8 Backward compatibility (하위 호환성)

- 최초의 제품이므로 하위 호환성은 없다.

# 3 Environment (환경)

## 3.1 Operating Environment (운영 환경)

### 3.1.1 Hardware Environment (하드웨어 환경)

- AWS에 운영 환경을 구축한다.
  - AWS Region은 미국 버지니아 북부(us-east-1)로 지정한다.

- 서비스의 주 사용자인 Vatech 장비 구매 고객이 미국 동부에 가장 많다.
  - AWS의 가장 오래된 Region 중 하나로 가장 많은 AWS 서비스를 제공한다.

  - v1.0은 성능 최적화를 위한 Multi Region을 고려하지 않는다.
    - 초기 출시 단계에서는 비용 최적화 및 관리 용이성을 확보하기 위해 Single Region로 운영한다.

- 출시 이후 국가별 MAU(Monthly Active User) 추이 및 사용자 피드백을 확인한 후, Multi Region 적용을 계획한다. (next)
  - Infra Architecture: [Confidential_SharedService_v1.0_Infra_Architecture.jpg](https://vatechcorp.sharepoint.com/:i:/s/es/EZrQjeZFuHRGlrYbUPpUTjkBcwRDInTJPvXaJ8NlahHu1A?e=EUntBc)

    ![A computer screen shot of a diagram Description automatically
generated](./images/media/image2.jpeg){width="5.832994313210849in" height="6.0625in"}
    - 계약 검토 중인 인프라 구축 외주 요청 범위에 리소스 상세 스펙 정의가 포함되어 있으므로, 이 SRS에서는 제외한다.

    - 인프라 구축 외주를 진행하지 않는 경우, 리소스 상세 스펙을 내부에서 검토/정의해야 한다.

### 3.1.2 Software Environment (소프트웨어 환경)

#### 3.1.2.1 OS Environment (운영체제환경)

- 3.1.2.2를 지원하는 OS

#### 3.1.2.2 OS 외 software 환경

- Desktop Web Browser
  - Chrome (v126 or later)

  - Safari (v17 or later)

  - Edge (v125 or later)

- Mobile Web Browser
  - v1.0은 주요 기능을 안정적으로 제공하는 것에 집중하기 위해 Mobile Web Browser를 대응하지 않는다.
    - Web Application로 Cloud에 호스팅 되므로 Mobile Web Browser에서도 접근할 수 있겠지만, 모든 기능의 정상 동작은 보장하지 않는다. 테스트 범위에서 제외한다.

  - 이후 버전에서 모바일 대응을 계획한다. (next)

## 3.2 Product Installation and Configuration (제품 설치 및 설정)

- Cloud에서 운영되므로 제품 설치는 따로 필요 없다.

## 3.3 Distribution Environment (배포 환경)

### 3.3.1 Master Configuration (마스터 구성)

- Backend (Identity Service, API Server)
  - Container Image

- Keycloak Configuration: [Confidential_OneID_v1.0_KeycloakConfiguration.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EX18bR23QeJLvWeEBdeRaWgBCKZLIcubTbTBgiaLjjN30g?e=j9qhGt)

- Frontend (User Console, Admin Console)
  - 배포 가능한 상태로 빌드 된 결과물 (Static Assets, JavaScript files, Resource)

### 3.3.2 Distribution Method (배포 방법)

- Backend (Identity Service, API Server)
  - 고가용성 및 확장성을 위해 AWS EKS(<https://aws.amazon.com/ko/eks/>)에 배포한다.
    - Container Image를 AWS ECR에 배포한다.

    - AWS EKS 클러스터에 Container Image를 배포하고 실행한다.

    - 수동 구축 방법은 <https://dev.azure.com/ewoosoft/ezicloud/_git/oneid-poc> \> read me \> Infra Provisioning을 참고한다.

- Frontend (User Console, Admin Console)
  - 정적 파일 관리를 위해 AWS S3(<https://aws.amazon.com/ko/s3/>)에 배포하고, 전세계 사용자에게 빠르고 안정적인 서비스를 제공하기 위해 AWS CloudFront(<https://aws.amazon.com/ko/cloudfront/>)를 사용한다.

- IaC 배포는 계약 검토 진행 중인 인프라 구축 외주 요청 범위에 포함되어 있으므로, 이 SRS에서는 제외한다. 인프라 구축 외주를 진행하지 않는 경우, 내부에서 검토 및 설계가 필요하다.

### 3.3.3 Patch/Update Method (패치와 업데이트 방법)

- 3.3.2와 동일하다.

## 3.4 Development Environment (개발 환경)

### 3.4.1 Hardware Environment (하드웨어 환경)

- ES 표준 개발자 Windows PC

### 3.4.2 Software Environment (소프트웨어 환경)

- Visual Studio Code (최신 버전)

- Node.js v20.x (LTS)

- Package Manager: pnpm v8.x (<https://pnpm.io/ko/>)

- Identity Service

- Keycloak v24.x (<https://www.keycloak.org/>)

- Backend
  - Framework: Nest.js v10.x (<https://nestjs.com>)

  - AWS SDK for JavaScript v3.x (<https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/>)

- Frontend
  - Build & Dev: Vite v5.x (<https://ko.vitejs.dev/guide/>)

  - Framework: React v18.x(<https://ko.legacy.reactjs.org/>), Refine v4.x (<https://refine.dev/>)

## 3.5 Test Environment (테스트 환경)

- 3.1에 작성된 인프라를 목적에 따라 dev, test, prod로 분리하여 구축/운영한다.
  - dev: 개발자의 개발 및 테스트를 위한 환경이다.

  - test: QA의 품질 테스트를 위한 환경이다.

  - prod: 최종 사용자에게 제공 되는 환경이다.

  - 참고: Cloud 배포 프로세스 결정([QATM-2107](https://vts.vatech.com/browse/QATM-2107))에 따라 stage 환경을 추가로 운영할 수 있다.

## 3.6 Configuration Management (형상관리)

### 3.6.1 Location of Outputs (산출물 위치)

#### 3.6.1.1 Location of Source Code (소스코드 위치)

- <https://dev.azure.com/ewoosoft/scp-sharedservice>

#### 3.6.1.2 Location of Documents (문서 위치)

- [Share Point \> ES Project \> ESCloudPlatform \> SharedService \> OneID](https://vatechcorp.sharepoint.com/:f:/s/es/Ev9NRE4RyilLhp8vazs1Ex8B7-CwYGSelYOpZ24JF-Lt5g?e=KteLsw)

### 3.6.2 Build Environment (빌드 환경)

- Azure DevOps Pipeline을 이용하여 Build한다.

## 3.7 Bug track System (버그트래킹)

- VTS로 issue를 관리한다.

- VTS Project: [SCPS](https://vts.vatech.com/projects/SCPS) \> component: OneID

## 3.8 Other Environment (기타 환경)

- None

# 4 External Interface Requirements (외부 인터페이스 요구사항)

## 4.1 System Interfaces (시스템 인터페이스)

### 4.1.1 컴포넌트 정의

- 2.2 Overall System Configuration을 참고한다.

### 4.1.2 인터페이스 정의

#### 4.1.2.1 UserConsole, AdminConsole, AppServices-\> APIServer

- [Confidential_OneID_v1.0_RestApi.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/ET7AgeivUQFDuRq4HCc3QU0Biik-w7LkUlAgpdypWNiG4A?e=nRioPK)

#### 4.1.2.2 UserConsole, AdminConsole, AppServices -\> IdentityService

- Keycloak JavaScript Adapter를 이용한다.
  - <https://www.keycloak.org/docs/latest/securing_apps/index.html#_javascript_adapter>

- Javascript 이외의 개발 환경을 가진 프로젝트는 각 환경에 따라 OAuth2 Library를 선정하여 이용한다.

- Identity Service에서 발급하는 Access Token은 아래 정보를 포함한다.

- Keycloak ID
  - email

- email_verified

- oneid_account_type ('admin'\|'user')

- oneid_uid

- oneid_tenant_uid

#### 4.1.2.3 ESProduct -\> UserConsole

- User Console 페이지로 이동한다.

- User Console 페이지 url은 API Server에 요청하여 조회할 수 있다.

#### 4.1.2.4 APIServer-\> IdentityService

- Keycloak Admin API를 호출하여 필요한 데이터를 처리한다.
  - <https://www.keycloak.org/docs-api/latest/rest-api/index.html> 를 참고한다.

#### 4.1.2.5 IdentityService -\> GoogleIDP

- Keycloak의 Social Login 연동 기능을 이용한다.
  - <https://www.keycloak.org/docs/latest/server_admin/#_google> 을 참고한다.

#### 4.1.2.6 APIServer-\>AWSSES

- AWS SDK의 SES API를 이용하여 메일을 전송한다.
  - <https://docs.aws.amazon.com/ko_kr/sdk-for-javascript/v3/developer-guide/ses-examples-sending-email.html>

#### 4.1.2.7 APIServer, IdentityService -\>CentralizedLogging

- fluentbit(<https://www.fluentbit.io/>)를 이용하여 EKS에서 운영하는 API Server, Identity Service의 로그를 CentralizedLogging(OpenSearch/S3)로 전송한다.

- EKS 클러스터에 fluentbit(<https://www.fluentbit.io/>)를 설치하고, config를 구성한다.

- fluentbit는 config에 따라 주기적으로 Log를 대상지로 전송한다.

- 필요에 따라 OpenSearch API를 이용하여 Log를 저장/조회한다.
  - 참고: <https://opensearch.org/docs/1.0/opensearch/rest-api/index/>

- 상세 로깅 정책은 구현 시점에 검토하여 확정한다.
  - 참고:
    - 법규에 따라 보관이 필요한 로그 항목은, [Confidential*OneID_v1.0*약관요청자료.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/ESGMIQobdbxGtrI18jiRiMsBLqfDGFN3Am1VxQ0Wyl8u9Q?e=0K1ux5) \> 로그 보관 항목 Sheet 참고

    - [VKS \> ESCloudPlatform Log Collection Architecture](https://vks.vatech.com/display/ESDEVELOPER/ESCloudPlatform+Log+Collection+Architecture)

## 4.2 User Interface **(**사용자 인터페이스)

- [Confidential_OneID_v1.0_MMI_Kor.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/EbvE-_1_X7ZJi0C-9MNNHtgBsx4u1wTTlqhyBM7xyrOUTg?e=NGo4no)

- [03.OneID_GUI_Guideline_v1.0.0](https://xd.adobe.com/view/f95eb528-13d7-4dbf-8180-9a324c7b6447-ac0d/)

## 4.3 Hardware Interface (하드웨어 인터페이스**)**

- None

## 4.4 Software Interface **(**소프트웨어 인터페이스)

- 4.1에 포함한다.

## 4.5 Communication Interface **(**통신 인터페이스**)**

- 4.1에 포함한다.

## 4.6 Other Interface (기타 인터페이스)

- None

# 5 Performance requirements (성능 요구사항**)**

## 5.1 Throughput (작업 처리량)

- AWS Service 성능에 종속된다.
  - v1.0은 아래 목표를 기준으로 AWS 리소스 스펙을 결정한다.

- MAU(Monthly Active Users): 10,000명

- DAU(Daily Active Users): MAU의 10%, 1,000명
  - Concurrent User: DAU의 20%, 200명

  - Response Time: 500ms 이내

## 5.2 Concurrent Session (동시 세션)

- 5.1과 동일

## 5.3 Response Time (대응시간)

- API 응답은 500ms 이내를 목표로 하며 최대 1sec을 넘기지 않아야 한다.

- 페이지 로딩은 500ms \~ 1sec를 목표로 하며 최대 3sec은 넘기지 않아야 한다.

## 5.4 Performance Dependency (성능 종속 관계)

- 사용자의 네트워크 속도에 종속된다.

- AWS Service의 성능에 종속된다.

## 5.5 Other Performance Requirements (기타 성능 요구사항**)**

- None

# 6 Non-Functional Requirements (기능 이외의 요구사항**)**

## 6.1 Safety requirements (안전성 요구사항)

- 모든 데이터의 유실을 방지해야 한다.
  - DB는 daily automated backup을 수행하여 데이터 손실에 대비한다.

  - S3는 AWS가 99.999999999%의 object durability를 보장하므로 별도로 backup을 하지는 않는다.

- 장애 발생 시, 빠르게 감지하고 복구 할 수 있어야 한다.
  - 중앙 로깅 시스템을 이용하여 모든 서비스의 상태 및 로그를 지속적으로 감시하고, 장애 발생시 빠르게 감지하여 복구를 수행한다.

## 6.2 Security Requirements (보안 요구사항**)**

- 개인 정보 보호를 위한 법규를 준수해야 한다.
  - 관련 법규 및 대응 방안의 상세 내용은 [Confidential_OneID_v1.0_Privacy_CheckList.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/ES7PLBz_sxBBk75tTReOZiIBYgwLXxaiS5uAUYzJZ_30GQ?e=9gUPsN)을 참고한다.

- 중요 데이터 및 서비스가 운영되는 인스턴스는 VPC의 Private Subnet에 배치하여 외부 접근을 제한해야한다.

- AWS IAM Role을 부여할때는 최소 권한 원칙을 준수하여, 개발자 및 운영자가 필요 이상의 인프라 접근권한을 가지지 않도록 제한해야한다.

- 외부 공격으로부터 Web Application을 보호하기 위해 AWS WAF(Web Application Firewall)을 도입한다.

- 정기적으로 취약점을 스캔하여 잠재적인 보안 취약점을 식별하고 평가하여 대응해야 한다.

## 6.3 Software System Attributes (소프트웨어 시스템 특성)

### 6.3.1 Availability (가용성)

- 24/7 동작해야 한다.
  - DB는 AWS RDS의 Multi-AZ로 구성하여 고가용성을 보장한다.

  - Backend Server는 AWS EKS에서 운영하여 고가용성을 보장한다.
    - 클러스터 내의 워커 노드를 3개 운영하고 각각 다른 가용 영역에 배치하여 특정 가용 영역의 장애 발생 시에 대응한다.

- 자동화된 Scaling 기능을 제공하여 트래픽 증가에 따라 자동으로 새로운 워커 노드를 추가한다. (next: 출시 이후 사용량 증가에 따라 적용한다.)

### 6.3.2 Maintainability (유지보수성)

- 모듈화 된 설계를 적용하여, 부분적인 변경이 전체 시스템에 영향을 미치지 않도록 한다.

- 자동화된 배포 및 인프라 프로비저닝을 통해 업데이트 및 패치가 신속하고 안전하게 적용되도록 한다.

- 최신 보안 패치 및 업데이트를 적용해야 한다.
  - AWS EKS
    - 정기적으로 EKS Kubernetes 버전을 점검하고 업데이트 계획을 수립하여 실행해야 한다.
      - AWS의 버전 지원 정책에 따라 이전 버전을 사용하는 경우 시간당 비용이 추가로 부가되고, 특정 기간이 지나면 AWS에서 자동으로 업데이트를 진행한다.

      - 자동 업데이트로 인해 기존 동작에 영향을 미칠 수 있으므로, 자동 업데이트가 발생하기 전에 계획을 수립하여 적용해야 한다.

      - <https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/kubernetes-versions.html>

    - EKS 클러스터 내의 워커 노드나 추가적으로 설치한 소프트웨어의 버전을 정기적으로 관리하고 업데이트해야 한다.

  - AWS RDS
    - 정기적으로 DB Engine의 버전을 점검하고 업데이트 계획을 수립하여 실행해야 한다.
      - <https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.PostgreSQL.html>

### 6.3.3 Portability (이식성)

- AWS가 아닌 다른 Cloud Platform 또는 on-premise로 구축한 Private Cloud로의 이식은 고려하지 않는다.

### 6.3.4 Reliability (신뢰성)

- None

### 6.3.5 Remaining Attributes (나머지 특성)

- None

## 6.4 Logical Database Requirements (데이터베이스 요구사항)

- DB Schema
  - [Confidential_OneID_v1.0_DBSchema.png](https://vatechcorp.sharepoint.com/:i:/s/es/EcziHkCvx4ZNirDX2CVMBFkBEqdnug1dzZZw1nbK-yQN-A?e=4JvwvC)
    - <https://dbdiagram.io/d/oneid-v1-0-6632fc245b24a634d049ca93> (pw: es0519)

- File
  - Identity Service

- Keyclaok에서 제공하는 페이지에 프로젝트의 고유 디자인을 적용하기 위해 Theme(<https://www.keycloak.org/docs/latest/server_development/#_themes>) 기능을 이용하여 Customize 한다.

- Customize한 Theme File은 AWS EFS에 저장하고, AWS EKS의 PV(Persist Volume)로 Mount한다.
  - AWS EKS에 배포된 Identity Service Pod가 종료 되어도 파일을 보관하고, 각 Pod에서 Custom Theme File을 공유하기 위함이다.

- AWS에서 제공하는 Storage 서비스 중 AWS EBS는 다른 AZ(가용 영역)으로 공유가 불가하며, S3는 EKS의 PV로 Mount할 수 없으므로 사용하지 않는다.

- AWS EFS Directory Structure는 Keycloak의 theme directory 구조와 동일하다.

- 참고: poc \> <https://dev.azure.com/ewoosoft/ezicloud/_git/oneid-poc?path=/resource/keycloak>
  - API Server
    - 약관은 AWS S3에 html format로 저장한다. 추후 edit 기능을 제공할 수 있다. (next)
      - Object Key: /terms/{language}/title.html

## 6.5 Business Rules (비즈니스 규칙)

- None

## 6.6 Design and Implementation Constraints (설계와 구현 제한사항)

### 6.6.1 Standards Compliance (표준준수)

- [ES Coding Convention](https://vks.vatech.co.kr/display/ESDEVELOPER/ES+Coding+Convention)을 준수한다.

- [ESCloudPlatform Log Standard](https://vks.vatech.com/display/ESDEVELOPER/ESCloudPlatform+Log+Standard)를 준수한다.

### 6.6.2 Other Constraints (기타 제한 사항)

- None

## 6.7 Memory Constraints (메모리 제한 사항)

- None

## 6.8 Operations (운영 요구사항**)**

- None

## 6.9 Site Adaptation Requirements **(**사이트 적용 요구사항**)**

- None

## 6.10 Internationalization Requirements (다국어 지원 요구사항)

- JavaScript용 다국어 지원 library인 LinguiJS를 사용하여 다국어를 지원한다.

- 이 모듈을 사용하는 서비스에서 요청이 있는 경우 지원 언어를 추가한다.

- v1.0은 EzCloud의 다국어 요구사항이 결정된 이후에 업데이트한다.

## 6.11 Unicode Support (유니코드 지원)

- None

## 6.12 64bit Support (64비트 지원)

- None

## 6.13 Certification **(**제품 인증)

- None

## 6.14 Field Test (필드 테스트)

- None

## 6.15 Other Requirements (기타 요구 사항)

- None

# 7 Functional Requirements (기능요구사항)

- [Confidential_OneID_v1.0_MMI_Kor.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/EbvE-_1_X7ZJi0C-9MNNHtgBsx4u1wTTlqhyBM7xyrOUTg?e=NGo4no)

# 8 Change Management process **(**변경관리 프로세스**)**

Identify the change management process to be used to identify, log, evaluate, and update the SRS to reflect changes in project scope and requirements.

1.  How are you going to control changes to the requirements?

2.  Can the customer just call up and ask for something new?

3.  Does your team have to reach consensus?

4.  How do changes to requirements get submitted to the team?

5.  Formally in writing, email or phone call?

This process can be specified in the one of the '[Process Diagram]{.underline}'s of the company.

# 9 Document Approvals **(**최종 승인자**)**

Identify the approvers of the SRS document. Approver name, signature, and date should be used.

[Name Signature Date]{.underline}

# 10 Reference Materials (참고문헌)

모든 문서는 소스코드 관리 시스템의 파일 위치로 기재한다.

# 11 Appendix (부록)

## 11.1 Glossary (용어)
