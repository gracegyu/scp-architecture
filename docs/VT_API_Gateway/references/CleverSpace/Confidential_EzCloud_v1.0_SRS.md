**EzCloud**

**Software Requirements Specification**

**Version: v1.0**

**Document Version: v1.0**

**Date: 2024-10-28**

**Writer : Ann (김가영)**

**EWOOSOFT Co., Ltd.**

# 1 Introduction **(개요)**

## 1.1 Purpose (목표)

- 이 문서는 ES에서 제공 중인 on-prem server인 EzServer에 저장된 환자
  데이터를 클라우드에 업로드하고, 이를 활용한 다양한 서비스를 제공하는
  Cloud Solution인 EzCloud에 대한 문서 이다.

  - EzCloud v1.0 개발을 위해 수정이 필요한 OneID 스펙을 포함한다. 해당
    사항은 문서 내 (**OneID**)로 표기하고, 개발 완료 후 각 제품의 SRS로
    이동한다.

  - 이 문서의 이해를 위해 OneID SRS를 먼저 확인하는 것을 권장한다.

- 이하, EzCloud를 내부에서 구축하기 위한 스펙을 작성한다.

## 1.2 Product Scope (범위)

- 이 제품은 ES에서 제공 중인 on-prem server인 EzServer에 저장된 환자
  데이터를 클라우드에 업로드하고, 이를 활용한 다양한 서비스를 제공하는
  Cloud Solution이다.

- v1.0은 조직 데이터 관리 서비스와 공유 서비스를 제공한다.

  - 조직 데이터 관리 (Organization Data)

    - EzServer에 저장된 환자 데이터(환자 정보 및 환자 영상 파일)을
      업로드하기 위한 API를 제공한다.

      - 업로드 대상 정보 및 파일 관련 정보는
        [Confidential_EzCloud_v1.0_Features.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/Ed0skjpt1FJMv9f9Sksas50Bo9xHs5bFZIDm8BuyIXddUA?e=3THDGH)
        ezserver_data sheet를 참고한다.

      - 대상 파일은 zip 형식으로 압축한 후 업로드해야 하며, 아래와 같은
        제한 사항이 있다.

        - 압축 전 최대 용량: 1GB

        - 최대 파일 개수: 10개

      - 중복된 환자 및 환자 영상의 업로드를 요청하는 경우, 데이터를
        overwrite한다.

        - 중복 데이터를 판단하기 위해 조직에 EzServer를 등록하고 고유
          ID를 발급하는 기능을 OneID에 추가한다. (**OneID**)

          - 이는 조직 내에서 여러 개의 EzServer를 운영하는 환경을 고려한
            기능이지만, v1.0은 아래와 같은 이유로 조직당 EzServer를
            1개로 제한한다.

            - 조직 내에서 여러 개의 EzServer를 운영하는 환경은
              제한적이다.

            - EzCloud v1.0에서 해당 환경을 대응하는 기능이 지원되지
              않는다.

          - 이후 버전에서 조직의 멀티 EzServer 지원을 고려한다.
            (**Next**)

        - 중복 데이터 판단 기준은 아래와 같다.

          - 환자: 사용자가 속한 조직 UID, EzServer UID, 차트번호 모두
            일치

          - 이미지: 사용자가 속한 조직 UID, EzServer UID, 원본
            파일명(EzServer File Name) 모두 일치

      - 자동으로 EzServer의 데이터를 동기화하는 기능은 제공하지 않는다.\
        이 기능은 별도의 서비스로 기획될 예정이므로, EzCloud 범위에
        포함하지 않는다.

    - 업로드 된 환자 데이터를 확인하고 삭제할 수 있는 기능을 제공한다.

    - 환자 데이터 다운로드 기능은 제공하지 않는다.\
      비용 대비 다운로드 된 데이터의 활용 방안이 명확하지 않다.

  - 공유 서비스 (Shared)

    - 조직 데이터를 다른 조직 및 비회원과 공유할 수 있는 기능을
      제공한다.

      - 공유 시점의 조직 데이터를 복사하여 공유하며, 이후 조직 데이터의
        변경 사항은 공유된 데이터에 반영되지 않는다.

        - 원본 데이터의 무결성을 보호하고 공유 시점의 정확한 정보를
          보장하기 위함이다.

      - EzServer에서 조직 데이터 업로드 후, 해당 데이터를 공유하기 위한
        API를 제공한다.

      - 공유된 데이터는 14일 이후 만료 되며, 만료일 3개월 이후 완전
        삭제된다.

    - Local PC에 저장된 데이터를 업로드 후 공유 하는 기능을 이후
      버전에서 제공할 수 있다. (**Next**)

    - 수신/발신 공유 데이터를 확인하고 관리할 수 있는 기능을 제공한다.

    - 공유 데이터의 다운로드 기능을 제공한다. 공유 시점의 케이스 단위로
      다운로드를 제공하며, 개별 이미지를 선택적으로 다운로드 하는 기능은
      제공하지 않는다.

    - 공유된 데이터의 편집(수정, 이미지 추가/삭제 등) 기능을 제공하지
      않는다.

- v1.0은 프리티어 플랜만 제공되며, 가입한 사용자에게 자동으로 해당
  플랜을 부여한다.

  - 프리티어 플랜은 10GB의 Organization Data를 제공하며, 기간 제한은
    없다.

    - Organization Data 사이즈는 원본 이미지 파일의 용량으로 측정한다.\
      meta file, thumbnail file 사이즈는 포함하지 않는다.

  - 프리티어 플랜은 조직당 최대 월간 공유 회수(1,000회) 및 다운로드
    횟수(5회)로 제한하지만, 이 수치는 사용자에게 표시하지 않는다. 이는
    악의적인 사용으로 인한 과도한 비용 발생을 방지하기 위한 조치이며,
    향후 유료 플랜에서 이 속성을 제공할 가능성을 고려해 시스템 제한이
    아닌 플랜 속성으로 설계한다.

- v1.0에서 과금이 적용되는 플랜을 제공할 계획이 없으므로 결제 기능은
  제공하지 않는다.

  - 추후, 플랜 기반의 구독형 솔루션으로 제공할 예정이다. (**Next**)

- v1.0의 타겟 국가는
  [Confidential_EzCloud_v1.0_TargetCountries.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EY7zmNZNl15HifAe751Qo8oBEJcn5CQ88xJAbtwzCy8Xtg?e=VX6s19)을
  참고한다.

- 사용자 인증 및 조직 관리를 위해 ES에서 제공하는 통합 계정 관리 제품인
  OneID와 연동한다.

- 클라우드에 저장된 환자 영상을 웹브라우저를 통해 확인하고 진단 및 협업
  기능을 제공하기 위해 ES에서 제공하는 Cloud Web Viewer와 연동한다.

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

  - 지원 계획이 정해지지 않았고 미래에 지원할 항목은 문장의 뒤에
    (**Next**)를 표시한다.

## 1.4 Terms and Abbreviations (정의 및 약어)

- ES: 이우소프트의 약어

## 1.5 Related Documents (관련문서)

- EzCloud

  - MRD: [Secret_EzShare
    v1.0.0_MRD.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EfmpRDIgaRJOi-zItaakTioBGVDTnYQQLTExjctg6oTPVA?e=t7gMBV)

  - MMI:
    [Confidential_EzCloud_v1.0_MMI_Kor_v4.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/EU3X9Y5DlSFPvOd1A7MfHTYBj-kzZaByS2MnTMkz1g4Kbg?e=hLIofH)

  - SDS

    - Diagrams:
      [Confidential_EzCloud_v1.0_Diagrams.vsdx](https://vatechcorp.sharepoint.com/:u:/s/es/EVLLVXUJsBBFuNTwhD53kucBagqqNsyY66ccRciZ72yxPg?e=imPhiR)

    - DB: <https://dbdiagram.io/d/ezcloud-v1-6578138b56d8064ca0da3a88>
      \> pw: escloud1024

    - Rest API:
      [Confidential_EzCloud_v1.0_RestApi.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=1viGB6)

- OneID

  - [Confidential_OneID_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/Edu7ctQwDwRGrlFlEYJhmo4BMe58HlQ-Qa5u3Bp7TDiUvg?e=3mlQUF)

- Cloud Web Viewer

  - [Confidential_CloudWebViewer_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EZfUnai1bK9Hlyq0TPmdUfQBxjPIKWSrR1uvIG2PGfSoEA?e=mluJv5)

- ESLogging

  - [VKS \> ESCloudPlatform Log Colletion
    Architecture](https://vks.vatech.com/display/ESDEVELOPER/ESCloudPlatform+Log+Collection+Architecture)

## 1.6 Intended Audience and Reading Suggestions (대상 및 읽는 방법)

표 1은 본 프로젝트에 참여하는 부서 및 인력 별로 본 문서를 활용하는데
있어 참고하거나 숙지해야 할 항목이다.

| 역할 Chapter | PM | TL | SW 개발자 | UI 디자인 | 기획/ 마케팅 | QA | 영업 | SE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.Introduction | ◉ | ⚪ | O |  | ⚪ | O |  |  |
| 2.Overall Description | ◉ | ⚪ | ⚪ | ⚪ |  | ⚪ | ⚪ | ⚪ |
| 3.Environment | ⚪ | ⚪ | ⚪ |  |  | ⚪ |  | ⚪ |
| 4.External Interface Requirement | ⚪ | ◉ | ⚪ | ⚪ |  |  |  |  |
| 5.Performance Requirement | ⚪ | ◉ | ⚪ |  |  | ◉ |  |  |
| 6.Non-Functional Requirement | ⚪ | ◉ | ⚪ |  |  | ⚪ |  |  |
| 7.Functional Requirement | ⚪ | ⚪ | ⚪ | ⚪ |  | ⚪ |  |  |
| 8.Change Management Process | ⚪ | ⚪ |  |  | ⚪ |  |  |  |
| 9.Document Approval | ⚪ |  |  |  |  |  |  |  |

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

- EzCloud App

  - 웹브라우저로 접근할 수 있는 Single Page Application

  - Remote-app

    - Viewer (cloudwebviewer/core)

      - 웹 브라우저로 접근할 수 있는 Single Page Application

    - Comment (cloudwebviewer/comment)

      - 웹 브라우저로 접근할 수 있는 Single Page Application

- API Server

  - Container Image

  - Node.js Backend Application

  - API document

- Lock Server

  - Container Image

  - Node.js Backend Application

- Y-Socket Server

  - Container Image

  - Node.js Backend Application

- Infra

  - EKS 배포를 위한 docker, manifest file

  - AWS CDK를 이용하여 구축된 AWS Infra

### 1.7.2 Output Name and Version (산출물명(가칭) 및 버전)

- EzCloud App

  - EzCloudApp v1.0

  - EzCloudViewer v1.0

  - EzCloudViewerComment v1.0

- API Server

  - EzCloudAPIServer v1.0

- Lock Server

  - EzCloudLockServer v1.0

- Y-Socket Server

  - EzCloudY-SocketServer v1.0

### 1.7.3 Patent Information (특허 출원 유무 및 내용)

- 특허 출원할 내용 없음.

# 2 Overall Description (전체 설명)

## 2.1 Product Perspective (제품 조망)

![A diagram of a software company Description automatically
generated](./images/media/image1.png){width="6.6930555555555555in"
height="5.03125in"}

| 분류 | 구성요소 | 설명 |
| --- | --- | --- |
| **On-prem Imaging Solution** | EzServer | ES에서 제공 중인 On-premise Imaging Server이다. |
|  | Imaging App | ES에서 제공 중인 On-premise Imaging Client App을 통칭한다. (ex. EzDent-i, CleverOne) |
| **Cloud Shared Service** | OneID | ES에서 제공하는 제품의 통합 계정 관리 서비스이다. |
|  | ESLogging | ES에서 제공하는 제품의 중앙 로깅 수집 서비스이다. |
| **Cloud App Service** | EzCloud | EzServer에 저장된 환자 데이터를 클라우드에 업로드하고, 이를 활용한 다양한 서비스를 제공하는 Cloud Solution이다. |

## 2.2 Overall System Configuration (전체 시스템 구성)

![A diagram of a network Description automatically
generated](./images/media/image2.png){width="6.6930555555555555in"
height="5.669444444444444in"}

| 분류 | 구성요소 | 설명 |
| --- | --- | --- |
| **EzCloud** | EzCloud App (SPA) | 웹 브라우저를 통해 EzCloud의 리소스를 확인할 수 있는 Single Page Application(SPA)이다. - Viewer/core와 Viewer/Comment App을 Remote-app으로 포함한다. - Viewer/core: 환자 영상을 표시하고 분석을 위한 Tool을 제공하는 SPA이다. - Viewer/comment: 환자 영상 기반으로 코멘트를 활용하여 협업 기능을 제공하는 SPA이다. |
|  | EzCloud API Server | 클라이언트(EzCloud App, EzServer, Imaging App)와의 통신을 담당하며, 데이터 요청 및 처리를 위한 RESTful endpoint를 제공한다. |
|  | Y-Socket Server | 실시간 데이터 전송을 지원하는 서버로, WebSocket 프로토콜을 사용하여 즉각적인 데이터의 동기화를 제공한다. - v1.0: Viewer/Comment App의 실시간 데이터 동기화 |
|  | Lock Server | 리소스의 동시 접근을 제어하는 서버로, 여러 클라이언트가 동시에 특정 리소스 접근 시 충돌을 방지를 제공한다. - v1.0: Viewer/Core App의 이미지 동시 편집 제어 |
|  | File | AWS S3를 이용하여 파일을 관리한다. |
|  | DB | AWS RDS, Redis를 이용하여 데이터를 관리한다. |

## 2.3 Overall Operation (전체 동작방식)

- [\[OneID 계정 가입 (**OneID**)\]]{.underline}

  - [Confidential_OneID_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/Edu7ctQwDwRGrlFlEYJhmo4BMe58HlQ-Qa5u3Bp7TDiUvg?e=3mlQUF)
    참고

- [\[EzCloud \> 가입 / 로그인\]]{.underline}

  - OneID 로그인

    - 사용자가 "EzCloud App/Imaging App/EzServer-Console(이하,
      Client)"에서 EzCloud 로그인을 요청한다.

    - "Client"는 "OneID" 로그인 페이지를 표시하고, 사용자는 해당
      페이지에서 로그인한다.

  - EzCloud 로그인

    - "Client"는 "OneID" 로그인에 성공하여 토큰을 발급 받으면, 해당
      토큰을 "EzCloud API Server"에 전달하여 EzCloud 리소스 토큰 발급을
      요청한다.

    - "EzCloud API Server"는 전달 받은 OneID 토큰을 검증하고, EzCloud
      리소스 접근 허용 여부를 확인하기 위한 JWT 형태의 토큰을 발급한다.

    - "Client""는 발급 받은 리소스 토큰을 이용하여 EzCloud API를
      호출하여 리소스에 접근한다.

  - EzCloud 가입

    - "Client"는 EzCloud 토큰 발급에 실패(가입되지 않은 사용자)하면,
      "EzCloud App"에 약관 페이지 표시를 요청한다.

    - "EzCloud App"은 "EzCloud API Server"에 약관 정보를 요청하여 약관을
      표시한다.

    - 사용자가 약관에 동의하면, "EzCloud App"은 "EzCloud API Server"에
      사용자 가입을 요청한다.

    - "EzCloud API Server"는 사용자 온보딩을 위한 정보를 DB에 저장한다.

- [\[EzServer-Console \> OneID 연동 설정 (**OneID**)\]]{.underline}

  - 테넌트 소유자가 "EzServer"에서 "OneID" 연동 설정을 요청한다.

  - "EzServer"는 "OneID" 로그인 페이지를 표시하고, 테넌트 소유자는 해당
    페이지에서 로그인한다.

  - "EzServer"는 "OneID" 로그인에 성공하여 토큰을 발급 받으면, 해당
    토큰을 "OneID"에 전달하여 로그인된 테넌트에 "EzServer" 등록을
    요청하고 EzServer UID를 발급 받는다.

- [\[Imaging App \> EzCloud 조직 데이터 업로드 / 공유\]]{.underline}

  - 업로드/공유 데이터 선택

    - 사용자가 "Imaging App"에서 업로드/공유를 요청할 데이터를 선택한다.

    - "Imaging App"은 가입/로그인이 필요한 경우, \[[EzCloud
      가입/로그인\]]{.underline} 절차에 따라 처리한다.

    - "Imaging App"은 "EzCloud API Server"에 데이터 업로드/공유 가능
      여부 체크를 요청한다.

      - 업로드/공유 불가능한 경우, 사용자에게 에러를 표시한다.

    - 사용자가 공유 수신자 검색을 요청하면, "Imaging App"은 "EzCloud API
      Server"에 공유 수신자 검색을 요청한다.

  - 업로드/공유 요청

    - 사용자가 선택된 데이터의 업로드/공유를 요청하면, "Imaging App"은
      "EzServer"에 선택된 데이터 정보를 전달하여 업로드/공유를 요청한다.

    - "EzServer"는 "EzCloud API Server"에 데이터 업로드/공유를 요청한다.

    - "EzCloud API Server"는 전달 받은 파일 및 데이터를 File/DB에
      저장한다.

- [\[EzCloud App\]]{.underline}

  - 조직 데이터 및 공유 데이터 관리

    - 사용자가 "EzCloud App"에서 조직 데이터 및 공유 데이터
      확인/수정/삭제 등을 요청한다.

    - "EzCloud App"은 "EzCloud API Server"에 데이터 조회/변경/삭제를
      요청한다.

      - 요청 데이터에 파일이 포함되어 있는 경우, "EzCloud App"은
        "EzCloud API Server"에서 파일에 접근 가능한 url을 전달 받아서
        파일에 접근한다.

    - "EzCloud API Server"는 요청 받은 데이터를 처리한다.

  - 조직 데이터 및 공유 데이터 Viewer 확인

    - "EzCloud App" / "Cloud Web Viewer" / "Y-SocketServer" / "Lock
      Server" 컴포넌트의 동작 방식은
      [Confidential_CloudWebViewer_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EZfUnai1bK9Hlyq0TPmdUfQBxjPIKWSrR1uvIG2PGfSoEA?e=mluJv5)
      참고

## 2.4 Product Functions (제품 주요 기능)

- [Confidential_EzCloud_v1.0_Features.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/Ed0skjpt1FJMv9f9Sksas50Bo9xHs5bFZIDm8BuyIXddUA?e=3THDGH)를
  참고한다.

## 2.5 User Classes and Characteristics (사용자 계층과 특징)

- OneID SRS "2.5 User Classes and Characteristics (사용자 계층과 특징)의
  "테넌트"와 동일하다.

  - [Confidential_OneID_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/Edu7ctQwDwRGrlFlEYJhmo4BMe58HlQ-Qa5u3Bp7TDiUvg?e=3mlQUF)

## 2.6 Assumptions and Dependencies (가정과 종속 관계)

- 사용자 인증 및 조직 관리를 위해 OneID가 구축되어 있어야 한다.

- 환자 영상을 확인하고 진단 및 협업을 위한 Cloud Web Viewer가 구축되어
  있어야 한다.

- 로그 수집/분석을 위해 중앙 로그 수집 아키텍처가 구축되어 있어야 한다.

## 2.7 Apportioning of Requirements (단계별 요구사항)

- v1.0

  - "조직 데이터 관리", "공유 서비스" 제공

- Next

  - 플랜 구독 및 결제 기능 제공

  - 타겟 국가 추가

  - 지원 언어 추가

  - Lab order 서비스 제공

## 2.8 Backward compatibility (하위 호환성)

- EzShare v0.9의 후속 버전 이지만, v0.9와 완전히 분리된 구조로 설계되어
  하위 호환성은 없다.

- 단, EzShare v0.9의 deprecated 시점과 이에 대한 대응 방안은 추후 결정이
  필요하다.

# 3 Environment (환경)

## 3.1 Operating Environment (운영 환경)

### 3.1.1 Hardware Environment (하드웨어 환경)

- AWS에 운영 환경을 구축한다.

  - AWS Region은 미국 버지니아 북부(us-east-1)로 지정한다.

    - 서비스의 주 사용자인 Vatech 장비 구매 고객이 미국 동부에 가장
      많다.

    - AWS의 가장 오래된 Region 중 하나로 가장 많은 AWS 서비스를
      제공한다.

  - 법규로 인해 데이터 국외 이전이 불가한 국가에 서비스를 지원해야 하는
    경우, Multi Region 운영을 고려할 필요가 있다. 단, Multi Region 구축
    시 비용은 Region 수에 비례하여 증가하므로, 비용 대비 가치를 판단하여
    결정해야 한다. (**Next**)

  - Infra Architecture:
    [Confidential_EzCloud_v1.0_Infra_Architecture.jpg](https://vatechcorp.sharepoint.com/:i:/s/es/EY9iFXaDBq1Du5yrTHFy4p4BPVBfjen0iup5KSnEUJ1lcQ?e=k7fy49)\
    Resource 상세 스펙은 인프라 구축 시, 정의한다.

> ![A computer screen shot of a diagram Description automatically
> generated](./images/media/image3.jpeg){width="6.026087051618548in"
> height="5.920833333333333in"}

### 3.1.2 Software Environment (소프트웨어 환경)

3.1.2.1 OS Environment (운영체제 환경)

- 3.1.2.2를 지원하는 OS

3.1.2.2 OS외 software 환경

- Desktop Web Browser

  - Chrome (v130 or later)

  - Safari (v18 or later)

  - Edge (v140 or later)

- Mobile Web Browser

  - v1.0은 주요 기능을 안정적으로 제공하는 것에 집중하기 위해 Mobile Web
    Browser를 대응하지 않는다.

    - Web Application로 Cloud에 호스팅 되므로 Mobile Web Browser에서도
      접근할 수 있겠지만, 모든 기능의 정상 동작은 보장하지 않는다.
      테스트 범위에서 제외한다.

  - 이후 버전에서 모바일 대응을 계획한다. (**Next**)

## 3.2 Product Installation and Configuration (제품 설치 및 설정)

- Cloud에서 운영되므로 제품 설치는 따로 필요 없다.

## 3.3 Distribution Environment (배포 환경)

### 3.3.1 Master Configuration (마스터 구성)

- Backend Server (API Server, Lock Server, Y-Socket Server)

  - Container Image

- Frontend App (EzCloud App, EzCloud Viewer App, EzCloud Viewer Comment
  App)

  - 배포 가능한 상태로 빌드 된 결과물 (Static Assets, JavaScript files,
    Resource)

### 3.3.2 Distribution Method (배포 방법)

- AWS CDK를 이용하여 인프라를 정의하고, AWS 리소스를 자동으로
  프로비저닝하여 클라우드 환경에 배포한다.

  - Backend Server는 고가용성 및 확장성을 위해 컨테이너화하여 AWS ECR /
    EKS에 배포한다.

  - Frontend App(SPA)은 정적 파일 관리를 위해 AWS S3에 배포한다.

### 3.3.3 Patch/Update Method (패치와 업데이트 방법)

- 3.3.2와 동일하다.

- 이후 버전에서 무중단 업데이트를 고려한 업데이트 전략 수립이 필요하다.
  (**Next**)

## 3.4 Development Environment (개발 환경)

### 3.4.1 Hardware Environment (하드웨어 환경)

- ES 표준 개발자 Windows PC

### 3.4.2 Software Environment (소프트웨어 환경)

- Visual Studio Code (최신 버전)

- Node.js v20.x (LTS)

- Package Manager: pnpm v9.x (<https://pnpm.io/ko/>)

- Backend

  - Framework: Nest.js v10.x (<https://nestjs.com>)

  - AWS SDK for JavaScript v3.x
    (<https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/>)

- Frontend

  - Build & Dev: Vite v5.x (<https://ko.vitejs.dev/guide/>)

  - Framework: React v18.x(<https://ko.legacy.reactjs.org/>), Refine
    v4.x (<https://refine.dev/>)

## 3.5 Test Environment (테스트 환경)

- 3.1에 작성된 인프라를 목적에 따라 dev, test, prod로 분리하여
  구축/운영한다.

  - dev: 개발자의 개발 및 테스트를 위한 환경이다.

  - test: QA의 품질 테스트를 위한 환경이다.

  - prod: 최종 사용자에게 제공 되는 환경이다.

  - 참고: Cloud 배포 프로세스
    결정([QATM-2107](https://vts.vatech.com/browse/QATM-2107))에 따라
    stage 환경을 추가로 운영할 수 있다.

- 타겟 국가 이외의 서비스 접속을 제한할 예정이지만, 테스트를 위해
  EVN/ES의 IP를 White List에 추가하여 접속을 허용한다.

## 3.6 Configuration Management (형상관리)

### 3.6.1 Location of Outputs (산출물 위치)

#### 3.6.1.1 Location of Source Code (소스코드 위치)

- <https://ewoosoft@dev.azure.com/ewoosoft/ezicloud/_git/ezcloud>

- <https://ewoosoft@dev.azure.com/ewoosoft/ezicloud/_git/ezcloud-infra>

#### 3.6.1.2 Location of Documents (문서 위치)

- [Shre Point \> ES Project \> ESCloudPlatform \>
  EzCloud](https://vatechcorp.sharepoint.com/:f:/s/es/EoLGxT8hPK1DibYa8AjRV7gBlYgFZ3EQ4y6mu1N_OiVZAQ?e=X2mZEd)

### 3.6.2 Build Environment (빌드 환경)

- Azure DevOps Pipeline을 이용하여 Build한다.

## 3.7 Bugtrack System (버그트래킹)

- VTS(JIRA)로 issue를 관리한다.

  - VTS Project: [EZCLD](https://vts.vatech.com/projects/EZCLD)

## 3.8 Other Environment (기타 환경)

- None

# 4 External Interface Requirements (외부 인터페이스 요구사항)

## 4.1 System Interfaces **(**시스템 인터페이스**)**

### 4.1.1 컴포넌트 정의

- 2.2 Overall System Configuration을 참고한다.

### 4.1.2 인터페이스 정의

#### 4.1.2.1 EzServer -- OneID (**OneID**)

- [Confidential_OneID_v1.0_RestApi.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/ET7AgeivUQFDuRq4HCc3QU0Biik-w7LkUlAgpdypWNiG4A?e=nRioPK)
  \> v1.0.0.a2 sheet

#### 4.1.2.2 ESImagingApp / EzCloudApp -- OneID (**OneID**)

- [Confidential_OneID_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/Edu7ctQwDwRGrlFlEYJhmo4BMe58HlQ-Qa5u3Bp7TDiUvg?e=3mlQUF)
  \> 4.1.2.2. UserConsole, AdminConsole, AppServices -\> IdentityService

#### 4.1.2.3 EzCloudAPIServer - OneID (**OneID**)

- [Confidential_OneID_v1.0_RestApi.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/ET7AgeivUQFDuRq4HCc3QU0Biik-w7LkUlAgpdypWNiG4A?e=nRioPK)

#### 4.1.2.4 ESImagingApp/EzServer/EzCloudApp -- EzCloudAPIServer

- [Confidential_EzCloud_v1.0_RestApi.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=WcMBON)

#### 4.1.2.5 EzCloudApp - Viewer/Core, Viewer/Comment

- [Confidential_CloudWebViewer_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EZfUnai1bK9Hlyq0TPmdUfQBxjPIKWSrR1uvIG2PGfSoEA?e=I1QQkq)

  - 4.1.2.2 Service/ContainerApp -\> CloudWebViewer/Core

  - 4.1.2.3 CloudWebViewer/Core -\> Service/ContainerApp

  - 4.1.2.4.Service/ContainerApp -\> CloudWebViewer/Addon-Comment

#### 4.1.2.6 EzCloudApp -- LockServer

- [Confidential_ESLockServer_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EUu2H0EFU5BMijyJxENn_FcBsLLxfCmd2rq9zuw1M3LYdg?e=HVCRWf)

#### 4.1.2.7 EzCloudApp -- YsocketServer

- [Confidential_CloudWebViewer_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EZfUnai1bK9Hlyq0TPmdUfQBxjPIKWSrR1uvIG2PGfSoEA?e=I1QQkq)

  - 4.1.2.5. CloudWebViewer/Addon-Comment -\> Service/WebSocketServer

#### 4.1.2.8 EzCloud -- ESLogging

- fluentbit(<https://www.fluentbit.io/>)를 이용하여 EKS에서 운영하는 API
  Server 의 로그를 CentralizedLogging(OpenSearch/S3)로 전송한다.

  - EKS 클러스터에 fluentbit(<https://www.fluentbit.io/>)를 설치하고,
    config를 구성한다.

  - fluentbit는 config에 따라 주기적으로 Log를 대상지로 전송한다.

- 필요에 따라 OpenSearch API를 이용하여 Log를 저장/조회한다.

  - 참고: <https://opensearch.org/docs/1.0/opensearch/rest-api/index/>

- 상세 로깅 정책은 구현 시점에 검토하여 확정한다.

  - 법규에 따라 보관이 필요한 로그 항목은
    [Confidential_EzCloud_v1.0_MMI_Kor_v4.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/EU3X9Y5DlSFPvOd1A7MfHTYBj-kzZaByS2MnTMkz1g4Kbg?e=hLIofH)
    \> Appendix를 참고한다.

#### 4.1.2.9 \[참고: EzServer/ESImagingApp Sequence\]

![A diagram of a project Description automatically
generated](./images/media/image4.jpeg){width="4.589040901137357in"
height="6.027397200349956in"}

![A close-up of a diagram Description automatically
generated](./images/media/image5.jpeg){width="6.146118766404199in"
height="9.223744531933509in"}

![A screenshot of a computer Description automatically
generated](./images/media/image6.jpeg){width="4.34251968503937in"
height="6.984251968503937in"}

## 4.2 User Interface **(**사용자 인터페이스)

- [Confidential_EzCloud_v1.0_MMI_Kor_v4.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/EU3X9Y5DlSFPvOd1A7MfHTYBj-kzZaByS2MnTMkz1g4Kbg?e=tCroqj)

- [01.EzCloud_Cloud_GUI_Guideline_v1.0.0_Design_Change](https://xd.adobe.com/view/2e983722-4123-4183-8f20-b16c44e2b8ea-7bcb/)

## 4.3 Hardware Interface (하드웨어 인터페이스**)**

- None

## 4.4 Software Interface **(**소프트웨어 인터페이스)

- 4.1에 포함한다.

## 4.5 Communication Interface **(**통신 인터페이스**)**

- 4.1에 포함한다.

## 4.6 Other Interface (기타 인터페이스**)**

- None

# 5 Performance requirements (성능 요구사항**)**

## 5.1 Throughput (작업처리량)

- AWS Service 성능에 종속된다.

  - v1.0은 아래 목표를 기준으로 AWS 리소스 스펙을 결정한다.

    - MAU(Monthly Active Users): 10,000명

    - DAU(Daily Active Users): MAU의 10%, 1,000명

    - Concurrent User: DAU의 20%, 200명

    - Response Time: 500ms 이내

## 5.2 Concurrent Session (동시 세션)

- 5.1과 동일하다.

## 5.3 Response Time (대응시간)

- 타겟국가의 Infra Region과의 지리적 위치 및 평균 네트워크
  속도(<https://www.speedtest.net/global-index>), 사용성을 고려하여 대응
  시간을 산정하였다.

  - API 응답은 500ms 이내를 목표로 하며 최대 1sec을 넘기지 않아야 한다.

  - 페이지 로딩은 500ms \~ 1sec를 목표로 하며 최대 3sec은 넘기지 않아야
    한다.

  - 500MB 사이즈 파일을 5분 이내 다운로드/업로드해야 한다.

## 5.4 Performance Dependency (성능 종속 관계)

- 사용자의 네트워크 속도에 종속된다.

- AWS Service의 성능에 종속된다.

## 5.5 Other Performance Requirements (기타 성능 요구사항**)**

- None

# 6 Non-Functional Requirements (기능 이외의 요구사항**)**

## 6.1 Safety requirements (안전성 요구사항)

- 모든 데이터의 유실을 방지해야 한다.

  - DB는 daily automated backup을 수행하여 데이터 손실에 대비한다.

  - S3는 AWS가 99.999999999%의 object durability를 보장하므로 별도로
    backup을 하지는 않는다.

- 장애 발생 시, 빠르게 감지하고 복구 할 수 있어야 한다.

  - 중앙 로깅 시스템을 이용하여 서비스의 상태 및 로그를 지속적으로
    감시하고, 장애 발생시 빠르게 감지하여 복구를 수행한다.

## 6.2 Security Requirements (보안 요구사항**)**

- 개인 정보 보호를 위한 법규를 준수해야 한다.

  - 사용자에게 개인 정보 관련 활용 내역을 고지하고 서비스 이용에 대한
    동의를 받아야 한다.

  - 이외 상세 내용은 OneID와 동일하다.
    [Confidential_OneID_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/Edu7ctQwDwRGrlFlEYJhmo4BMe58HlQ-Qa5u3Bp7TDiUvg?e=3mlQUF)를
    참고한다.

- AWS BAA(Business Associate Addendum)을 체결해야 한다.

- HIPAA Eligible AWS Service를 이용한다. ([[HIPAA Eligible AWS Services
  Reference]{.underline}](https://aws.amazon.com/compliance/hipaa-eligible-services-reference/?nc1=h_ls))

  - [Confidential_EzCloud_v1.0_Infra_Check_AWS_HIPAA_Eligible.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/ETRmipkrF6tOjkEYK555pOIBMr5xaAOHifseeU8GZ9sz1A?e=rankcf)

- 중요 데이터 및 서비스가 운영되는 인스턴스는 VPC의 Private Subnet에
  배치하여 외부 접근을 제한한다.

- AWS IAM Role을 부여할 때는 최소 권한 원칙을 준수하여, 개발자 및
  운영자가 필요 이상의 인프라 접근권한을 가지지 않도록 제한한다.

- 주요한 모든 기능의 로그를 남겨야 한다.

  - 구현시점에 보안을 위해 작성이 필요한 로그 항목을 결정하고 로그 저장
    방식을 확정하여 반영한다.

## 6.3 Software System Attributes (소프트웨어 시스템 특성)

### 6.3.1 Availability (가용성)

- 24/7 동작해야 한다.

  - DB는 AWS RDS의 Multi-AZ로 구성하여 고가용성을 보장한다.

  - Backend Server는 AWS EKS에서 운영하여 고가용성을 보장한다.

    - 클러스터 내의 워커 노드를 2개 이상 운영하고 각각 다른 가용 영역에
      배치하여 특정 가용 영역의 장애 발생 시에 대응한다.

    - 자동화된 Scaling 기능을 제공하여 트래픽 증가에 따라 자동으로
      새로운 워커 노드를 추가한다. (**Next**: 출시 이후 사용량 증가에
      따라 적용한다.)

### 6.3.2 Maintainability (유지보수성)

- 코드의 구조와 스타일의 일관성 유지를 위해 코드 포맷팅 도구(ESLint,
  Prettier)를 사용한다.

- 외부 라이브러리는 최신 버전으로 주기적으로 업데이트하며, 종속성
  취약점을 확인하고 이에 대한 보안 패치를 수행한다.

- 단위 테스트, 통합 테스트를 자동화하고 테스트 커버리지를 정기적으로
  검토하여 품질을 유지한다.

- 자동화된 배포 및 인프라 프로비저닝을 통해 업데이트 및 패치가 신속하고
  안전하게 적용되도록 한다.

- 최신 보안 패치 및 업데이트를 적용해야 한다.

  - AWS EKS

    - 정기적으로 EKS Kubernetes 버전을 점검하고 업데이트 계획을 수립하여
      실행해야 한다.

      - AWS의 버전 지원 정책에 따라 이전 버전을 사용하는 경우 시간당
        비용이 추가로 부가되고, 특정 기간이 지나면 AWS에서 자동으로
        업데이트를 진행한다.

      - 자동 업데이트로 인해 기존 동작에 영향을 미칠 수 있으므로, 자동
        업데이트가 발생하기 전에 계획을 수립하여 적용해야 한다.

      - <https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/kubernetes-versions.html>

    - EKS 클러스터 내의 워커 노드나 추가적으로 설치한 소프트웨어의
      버전을 정기적으로 관리하고 업데이트해야 한다.

  - AWS RDS

    - 정기적으로 DB Engine의 버전을 점검하고 업데이트 계획을 수립하여
      실행해야 한다.

      - <https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.PostgreSQL.html>

### 6.3.3 Portability (이식성)

- AWS가 아닌 다른 Cloud Platform 또는 on-premise로 구축한 Private
  Cloud로의 이식은 고려하지 않는다.

### 6.3.4 Reliability (신뢰성)

- None

### 6.3.5 Remaining Attributes (나머지 특성)

- None

## 6.4 Logical Database Requirements (데이터베이스 요구사항)

- DB

  - AWS RDS에 데이터를 저장한다.

  - Schema

    - <https://dbdiagram.io/d/ezcloud-v1-6578138b56d8064ca0da3a88> \>
      pw: escloud1024

  - Multi tenancy

    - 예상되는 데이터 양 대비 관리 오버헤드 및 비용 효율성을 고려하여,
      다수 테넌트의 환자 데이터를 단일 데이터 베이스/공유 스키마를
      사용하여 저장한다.

      - 예상 데이터 양은 최대 10억 레코드(10만 테넌트 \* 100명 환자 \*
        100개 이미지)이며, 이는 단일 데이터베이스 / 공유 스키마를
        이용하여 처리 가능한 수준이다.\
        이후 버전에서 법적 규제에 따라 데이터가 Region별로 분리될 경우,
        각 데이터 베이스의 레코드 수는 감소하여 시스템 처리 부담은 보다
        적을 것으로 예상한다.

    - 레코드 수가 증가함에 따른 검색 효율을 높이기 위해 인덱스를
      적용한다.

    - 테넌트별 데이터 접근 제한은 Application Server에서 제어한다.\
      데이터베이스의 RLS(Row Level Security)는 적용하지 않는다.

    - 참고:
      [Confidential_ezcloud_db_multitenancy.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EXQ2D0al9PBDnE6V8t0A8cwB3oT7aanF2esJvKwKB7PsrA?e=p7AesH)

- File

  - AWS S3에 파일을 저장한다.

  - S3 Trigger, Lifecycle은 구현 과정에서 상세 요구사항에 따라 적용한다.

| **Bucket Name** | **Description** | **Structure** |
| --- | --- | --- |
| ezcloud-assets | 다양한 유형의 asset 파일을 저장하는 버킷이다. | **ezcloud-assets** ├── documents ├── promotions ├── images └── templates |
| ezcloud-organization-data | 조직 데이터를 저장하는 버킷이다. | **ezcloud-organization-data** └── {tenant_uid} └── {chart_no} ├── images ├── thumbnails └── metafiles |
| ezcloud-shared-data | 여러 사용자 간에 공유되는 데이터를 저장하는 버킷이다. | **ezcloud-shared-data** └── {case_uid} ├── images ├── thumbnails └── metafiles └── download |
| ezcloud-temporary-data | 일시적인 데이터 저장을 위한 버킷이다. - 파일 처리 과정에서 발생하는 임시 데이터 관리에 사용한다. | **ezcloud-temporary-data** ├── upload └── error |
| ezcloud-container-app | EzCloud Container Static App을 저장하는 버킷이다. | - |
| ezcloud-viewer-app | EzCloud Viewer Static App을 저장하는 버킷이다. | - |
| ezcloud-comment-app | EzCloud Comment Static App을 저장하는 버킷이다. | - |

## 6.5 Business Rules (비즈니스 규칙)

- None

## 6.6 Design and Implementation Constraints (설계와 구현 제한사항)

### 6.6.1 Standards Compliance (표준준수)

- [ES Coding
  Convention](https://vks.vatech.co.kr/display/ESDEVELOPER/ES+Coding+Convention)을
  준수한다.

- [ESCloudPlatform Log
  Standard](https://vks.vatech.com/display/ESDEVELOPER/ESCloudPlatform+Log+Standard)를
  준수한다.

- DICOM 표준을 준수한다.

### 6.6.2 Other Constraints (기타 제한 사항)

- None

## 6.7 Memory Constraints (메모리 제한 사항)

- None

## 6.8 Operations (운영 요구사항**)**

- None

## 6.9 Site Adaptation Requirements **(**사이트 적용 요구사항**)**

- None

## 6.10 Internationalization Requirements (다국어 지원 요구사항)

- JavaScript용 다국어 지원 library인 LinguiJS를 사용하여 다국어를
  지원한다.

- 사용자는 개인화된 설정을 통해 선호하는 언어를 선택할 수 있다.

  - 사용자가 언어 설정을 하지 않은 경우, 기본 언어는 브라우저의 설정을
    따른다.

  - OneID의 설정 언어와 연동하지 않는다. OneID와 EzCloud의 언어 설정은
    별도이다.

- v1.0은 영어, 한국어를 지원한다.

## 6.11 Unicode Support (유니코드 지원)

- None

## 6.12 64bit Support (64비트 지원)

- None

## 6.13 Certification **(**제품 인증)

- EzCloud 연동 기능을 제공할 예정인 On-premise Imaging App(ex. EzDent-i,
  CleverOne)의 인증에 포함된다.

- EzCloud를 위한 별도 인증은 진행하지 않는다.

## 6.14 Field Test (필드 테스트)

- EzCloud 연동 기능을 제공할 예정인 On-premise Imaging App(ex. EzDent-i,
  CleverOne)의 필드 테스트 계획에 따른다.

- EzCloud 별도 필드 테스트 계획은 없다.

## 6.15 Other Requirements (기타 요구 사항)

- None

# 7 Functional Requirements (기능요구사항)

- [Confidential_EzCloud_v1.0_MMI_Kor_v4.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/EU3X9Y5DlSFPvOd1A7MfHTYBj-kzZaByS2MnTMkz1g4Kbg?e=tCroqj)

# 8 Change Management process **(**변경관리 프로세스**)**

Identify the change management process to be used to identify, log,
evaluate, and update the SRS to reflect changes in project scope and
requirements.

1)  How are you going to control changes to the requirements?

2)  Can the customer just call up and ask for something new?

3)  Does your team have to reach consensus?

4)  How do changes to requirements get submitted to the team?

5)  Formally in writing, email or phone call?

This process can be specified in the one of the '[Process
Diagram]{.underline}'s of the company.

# 9 Document Approvals **(**최종 승인자**)**

Identify the approvers of the SRS document. Approver name, signature,
and date should be used.

[Name Signature Date]{.underline}

# 10 Reference Materials (참고문헌)

모든 문서는 소스코드 관리 시스템의 파일 위치로 기재한다.

# 11 Appendix (부록)

- None
