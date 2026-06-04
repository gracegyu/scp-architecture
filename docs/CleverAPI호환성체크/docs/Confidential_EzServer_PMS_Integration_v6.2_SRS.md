**EzServer PMS Integration**

**Software Requirements Specification**

**Version : v6.2.0**

**Date : 2024-11-22**

**Writer : Roman Seo(서현덕)**

**EWOOSOFT Co., Ltd.**

문서정보 / 수정 내역

| 파일명:      | Confidential_EzServer_PMS_Integration_v6.2_SRS.doc |
| ------------ | -------------------------------------------------- |
| 템플릿 버전: | 3.2                                                |
| 원안작성자 : | Roman Seo(서현덕)                                  |
| 수정작업자 : |                                                    |

| 수정날짜   | 수정자    | 버전   | 추가/수정 항목 | 내 용                  |
| ---------- | --------- | ------ | -------------- | ---------------------- |
| 2025-04-10 | Roman Seo | V6.2.1 |                | 기능 개선 사항 반영    |
| 2025-03-27 | Roman Seo | V6.2.0 |                | 구현 시 변경 사항 반영 |
| 2024-11-22 | Roman Seo | V6.2.0 |                | 최초 작성              |
|            |           |        |                |                        |
|            |           |        |                |                        |
|            |           |        |                |                        |

목 차

[1 Introduction (개요) 5](#_Toc271897741)

[1.1 Purpose (목표) 5](#_Toc271897742)

[1.2 Product Scope (범위) 5](#_Toc271897743)

[1.3 Document Conventions (문서규칙) 5](#_Toc271897744)

[1.4 Terms and Abbreviations (정의 및 약어) 5](#_Toc271897745)

[1.5 Related Documents (관련문서) 5](#_Toc271897746)

[1.6 Intended Audience and Reading Suggestions (대상 및 읽는 방법) 5](#_Toc271897747)

[1.7 Project Output (프로젝트 산출물) 6](#_Toc271897748)

[1.7.1 Output Format (산출물 형태) 6](#_Toc271897749)

[1.7.2 Output Name and Version (산출물명(가칭) 및 버전) 6](#_Toc271897750)

[1.7.3 Patent Information (특허 출원 유무 및 내용) 6](#_Toc271897751)

[2 Overall Description (전체 설명) 7](#_Toc271897752)

[2.1 Product Perspective (제품 조망) 7](#_Toc271897753)

[2.2 Overall System Configuration (전체 시스템 구성) 7](#_Toc271897754)

[2.3 Overall Operation (전체 동작방식) 7](#_Toc271897755)

[2.4 Product Functions (제품 주요 기능) 7](#_Toc271897756)

[2.5 User Classes and Characteristics (사용자 계층과 특징) 8](#_Toc271897757)

[2.6 Assumptions and Dependencies (가정과 종속 관계) 8](#_Toc271897758)

[2.7 Apportioning of Requirements (단계별 요구사항) 9](#_Toc271897759)

[2.8 Backward compatibility (하위 호환성) 9](#_Toc271897760)

[3 Environment (환경) 10](#_Toc271897761)

[3.1 Operating Environment (운영 환경) 10](#_Toc271897762)

[3.1.1 Hardware Environment (하드웨어 환경) 10](#_Toc271897763)

[3.1.2 Software Environment (소프트웨어 환경) 10](#_Toc271897764)

[3.2 Product Installation and Configuration (제품 설치 및 설정) 11](#_Toc271897765)

[3.3 Distribution Environment (배포 환경) 11](#_Toc271897766)

[3.3.1 Master Configuration (마스터 구성) 11](#_Toc271897767)

[3.3.2 Distribution Method (배포 방법) 12](#_Toc271897768)

[3.3.3 Patch/Update Method (패치와 업데이트 방법) 12](#_Toc271897769)

[3.4 Development Environment (개발 환경) 12](#_Toc271897770)

[3.4.1 Hardware Environment (하드웨어 환경) 12](#_Toc271897771)

[3.4.2 Software Environment (소프트웨어 환경) 12](#_Toc271897772)

[3.5 Test Environment (테스트 환경) 12](#_Toc271897773)

[3.5.1 Hardware Environment (하드웨어 환경) 12](#_Toc271897774)

[3.5.2 Software Environment (소프트웨어 환경) 12](#_Toc271897775)

[3.6 Configuration Management (형상관리) 13](#_Toc271897776)

[3.6.1 Location of Outputs (산출물 위치) 13](#_Toc271897777)

[3.6.1.1. Location of Source Code (소스코드 위치) 13](#_Toc271897778)

[3.6.1.2. Location of Documents (문서 위치) 13](#_Toc271897779)

[3.6.2 Build Environment (빌드 환경) 13](#_Toc271897780)

[3.7 Bugtrack System (버그트래킹) 13](#_Toc271897781)

[3.8 Other Environment (기타 환경) 13](#_Toc271897782)

[4 External Interface Requirements (외부 인터페이스 요구사항) 14](#_Toc271897783)

[4.1 System Interfaces **(**시스템 인터페이스**)** 14](#_Toc271897784)

[4.2 User Interface **(**사용자 인터페이스) 15](#_Toc271897785)

[4.3 Hardware Interface (하드웨어 인터페이스**)** 15](#_Toc271897786)

[4.4 Software Interface **(**소프트웨어 인터페이스) 15](#_Toc271897787)

[4.5 Communication Interface **(**통신 인터페이스**)** 16](#_Toc271897788)

[**4.6** Other Interface (기타 인터페이스**)** 16](#_Toc271897789)

[5 Performance requirements (성능 요구사항) 17](#_Toc271897790)

[5.1 Throughput (작업처리량) 17](#_Toc271897791)

[5.2 Concurrent Session (동시 세션) 17](#_Toc271897792)

[5.3 Response Time (대응시간) 17](#_Toc271897793)

[5.4 Performance Dependency (성능 종속 관계) 18](#_Toc271897794)

[5.5 Other Performance Requirements (기타 성능 요구사항**)** 18](#_Toc271897795)

[6 Non-Functional Requirements (기능 이외의 요구사항) 19](#_Toc271897796)

[6.1 Safety requirements (안전성 요구사항) 19](#_Toc271897797)

[6.2 Security Requirements (보안 요구사항**)** 19](#_Toc271897798)

[6.3 Software System Attributes (소프트웨어 시스템 특성) 19](#_Toc271897799)

[6.3.1 Availability (가용성) 19](#_Toc271897800)

[6.3.2 Maintainability (유지보수성) 20](#_Toc271897801)

[6.3.3 Portability (이식성) 20](#_Toc271897802)

[6.3.4 Reliability (신뢰성) 20](#_Toc271897803)

[6.3.5 Remaining Attributes (나머지 특성) 20](#_Toc271897804)

[6.4 Logical Database Requirements (데이터베이스 요구사항) 21](#_Toc271897805)

[6.5 Business Rules (비즈니스 규칙) 21](#_Toc271897806)

[6.6 Design and Implementation Constraints (설계와 구현 제한사항) 21](#_Toc271897807)

[6.6.1 Standards Compliance (표준준수) 21](#_Toc271897808)

[6.6.2 Other Constraints (기타 제한 사항) 21](#_Toc271897809)

[6.7 Memory Constraints (메모리 제한 사항) 22](#_Toc271897810)

[6.8 Operations (운영 요구사항**)** 22](#_Toc271897811)

[6.9 Site Adaptation Requirements **(**사이트 적용 요구사항**)** 22](#_Toc271897812)

[6.10 Internationalization Requirements (다국어 지원 요구사항) 23](#_Toc271897813)

[6.11 Unicode Support (유니코드 지원) 23](#_Toc271897814)

[6.12 64bit Support (64비트 지원) 23](#_Toc271897815)

[6.13 Certification **(**제품 인증) 23](#_Toc271897816)

[6.14 Field Test (필드 테스트) 24](#_Toc271897817)

[6.15 Other Requirements (기타 요구 사항) 24](#_Toc271897818)

[7 Functional Requirements (기능요구사항) 25](#_Toc271897819)

[7.1 대분류 기능1 26](#_Toc271897820)

[7.1.1 …… 26](#_Toc271897821)

[7.1.2 …… 26](#_Toc271897822)

[7.2 대분류 기능2 26](#_Toc271897823)

[7.3 대분류 기능3 26](#_Toc271897824)

[8 Change Management process (변경관리 프로세스) 27](#_Toc271897825)

[9 Document Approvals (최종 승인자) 28](#_Toc271897826)

[10 Reference Materials (참고문헌) 29](#_Toc271897827)

[11 Appendix (부록) 30](#_Toc271897828)

[11.1 Glossary (용어) 30](#_Toc271897829)

# Introduction **(개요)**

## Purpose (목표)

## Product Scope (범위)

- v5.5에서 다음 PMS 연동 기능을 제공한다. 자세한 기능은 [Onepager](https://dev.azure.com/ewoosoft/ezserver/_git/ezserver-pms-integration-onepager?path=/Confidential_ezserver_pms_integration_onepager.md) 참고
  - Weclever
  - Clever RC
- v6.2에서 EzCloud v1.0 연동 관련 기능을 추가 제공한다.
  - EzCloud 연동 설정 관련 DB data 갱신
  - EzCloud upload/share history 제공
  - EzCloud upload/share 결과 알림
  - 영상을 EzCloud에 upload하는 기능 제공
  - 영상을 EzCloud에 share하는 기능 제공
- v6.2에서 다음 기능은 지원하지 않는다.
  - 사용자가 upload 또는 share 재시도 요청

## Document Conventions (문서규칙)

- 본 문서를 읽는데 필요한 기본 규칙을 기술한다.
  - 우선순위
    - 각 기능의 중요도에 따라 아래와 같이 3가지 Priority로 표시한다.
      - P1: 높음, 중요한 기능으로 반드시 구현해야 함.
      - P2: 보통, 일반적인 기능으로 구현해야 함.
      - P3: 낮음, 부가적인 기능으로 필요 시 배제할 수 있음.
    - Priority가 표시되지 않은 항목은 P1로 간주한다.
    - 우선순위의 표시는 해당 항목의 문장 뒤에 (P2)와 같이 표시한다.

## Terms and Abbreviations (정의 및 약어)

- ES: 이우소프트의 약어
- EPI: EzServer PMS Integration의 약어
- E2: EzDent-i의 약어
- C1: Clever One의 약어
- 케이스
  - 환자정보 및 환자의 복수 영상 파일 및 관련 정보를 포함한 데이터 집합
  - 케이스 단위로 Organization Data에 업로드하거나, 다른 사용자에게 공유
- 테넌트
  - 서비스를 구독하는 주체로 개별 고객(개인) 또는 조직을 의미하며, 소유자 1인과 0명 이상의 멤버로 구성된다.
  - EzCloud의 테넌트는 Clinic, Lab, 개인이다.

## Related Documents (관련문서)

- EzCloud
  - SRS: [Confidential_EzCloud_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EaoqWfCkjPZEhgwM0WnGCK8BA2LRaHDO9qSe_DRaY3ZANg?e=EYBR8h)
  - MMI: [Confidential_EzCloud_v1.0_MMI_Kor_v5.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/ER9Xz50uoMlIvkzQLpjn05sB6D56tj71KdS_DIPdZ69ZJQ?e=5vNRIe)
  - REST API: [Confidential_EzCloud_v1.0_RestApi.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=aPg8ul)
- One ID
  - SRS: [Confidential_OneID_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/Edu7ctQwDwRGrlFlEYJhmo4BMe58HlQ-Qa5u3Bp7TDiUvg?e=gVMHtO)
  - REST API: [Confidential_OneID_v1.0_RestApi.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/ET7AgeivUQFDuRq4HCc3QU0Biik-w7LkUlAgpdypWNiG4A?e=uneo2N)
- EzServer
  - MMI: [Confidential_20241002_EzServer_V6_2_0_MMI_Kor.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/EahEkqv3GDlArTjN2XfOJpgB57FLgblhriDDO0AkI_D_GA?e=9sBXdW)
  - REST API: [epi_api.yaml](https://vatechcorp.sharepoint.com/:u:/s/es/EVevRLXvZMtOk-Z2_pAI1NoBv7XCKDPwfFQZuWCsAfunyg?e=YklDdA)
  - DB: [Confidential_EzServer-PMS_Integration_db_schema_v6.2.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EVRUrYC4C_JLiej32a_YvaIBqDFdBe4zlLEnUbqIc6rZ-w?e=FxXIZP)

## Intended Audience and Reading Suggestions (대상 및 읽는 방법)

표 1은 본 프로젝트에 참여하는 부서 및 인력 별로 본 문서를 활용하는데 있어 참고하거나 숙지해야 할 문서 항목을 제시하고 있다.

&nbsp;

| 역할 <br><br>Chapter             | PM  | PL     | SW <br><br>개발자 | UI <br><br>디자인 | 마케팅 | QA     | 영업   | SE     |
| -------------------------------- | --- | ------ | ----------------- | ----------------- | ------ | ------ | ------ | ------ |
| 1.Introduction                   | OO  | O      | O                 | &nbsp;            | O      | O      | &nbsp; | &nbsp; |
| 2.Overall Description            | OO  | O      | O                 | O                 | O      | O      | O      | O      |
| 3.Environment                    | O   | O      | O                 | &nbsp;            | O      | O      | &nbsp; | O      |
| 4.External Interface Requirement | O   | OO     | O                 | O                 | &nbsp; | O      | &nbsp; | &nbsp; |
| 5.Performance Requirement        | O   | O      | O                 | &nbsp;            | &nbsp; | OO     | &nbsp; | &nbsp; |
| 6.Non-Functional Requirement     | O   | OO     | O                 | &nbsp;            | &nbsp; | O      | &nbsp; | &nbsp; |
| 7.Functional Requirement         | O   | O      | O                 | O                 | &nbsp; | O      | &nbsp; | &nbsp; |
| 8.Change Management Process      | O   | O      | &nbsp;            | &nbsp;            | O      | &nbsp; | &nbsp; | &nbsp; |
| 9.Document Approval              | O   | &nbsp; | &nbsp;            | &nbsp;            | &nbsp; | &nbsp; | &nbsp; | &nbsp; |

**표 1 대상 및 읽는 방법 정의**

범례)

OO : 거의 암기 해야 한다.

O : 완전히 숙지해야 한다.

빈칸 : 시간이 남으면 읽어봐도 된다.

&nbsp;

- PM - 프로젝트 관리자
- PL(Project Leader) - 프로젝트의 Technical Leader
- SW 개발자 - 프로젝트의 분석/설계/구현 담당자
- UI 디자인 - 제품의 UI 담당
- 마케팅 - 제품의 기획 및 마케팅 담당
- 영업 - 바텍 MCIS, 바텍 글로벌마케팅부문
- SE - Technical Support

## Project Output (프로젝트 산출물)

### Output Format (산출물 형태)

- Single Page Application
- REST API Server

### Output Name and Version (산출물명(가칭) 및 버전)

- Single Page Application
  - EzServer WebConsole v6.2.0
- REST API Server
  - EzServer PMS Integration v6.2.0

### Patent Information (특허 출원 유무 및 내용)

- 특허 출원할 내용 없음.

# Overall Description (전체 설명)

## Product Perspective (제품 조망)

- [Confidential_EzServer_PMS_Integration_v6.2_diagram.vsdx](https://vatechcorp.sharepoint.com/:u:/s/es/EdQYeKnoaQ9LjNHFNusYHlsBw2daZjpdYAQOgYL5XOi-ww?e=hzgJWE) - Product Perspective참고

## Overall System Configuration (전체 시스템 구성)

- [Confidential_EzServer_PMS_Integration_v6.2_diagram.vsdx](https://vatechcorp.sharepoint.com/:u:/s/es/EdQYeKnoaQ9LjNHFNusYHlsBw2daZjpdYAQOgYL5XOi-ww?e=hzgJWE) - Overall Perspective 참고

## Overall Operation (전체 동작방식)

- \[EzServer Web Console > EzServer PMS Integraion\] EzCloud 연동 요청
- ~~사용자가 EzCloud 연동 정보를 입력한다.~~
- 사용자가 "~~connection check"~~ "Login to OneID" 버튼을 클릭한다.
  - EzServer WebConsole이 One ID 로그인 UI를 popup으로 표시
  - 사용자가 popup에서 One ID에 로그인을 시도한다.
    - 로그인 완료시, Popup이 종료된다.
  - 사용자가 "save" 버튼을 클릭한다.
- \[EzServer Web Console > EzServer PMS Integraion\] EzCloud 연동 중지 요청
  - 사용자가 EzCloud 연동을 비활성화한다.
    - EzServer WebConsole이 사용자에게 EzCloud 연동 정보 유지/제거 여부 확인을 위한 UI를 표시한다.
  - 사용자가 EzCloud 연동 정보 유지/제거 여부를 선택한다.
- \[Imaging App > EzServer PMS Integraion\] EzCloud 연동 정보 조회 요청
- \[Imaging App > EzServer PMS Integraion\] 영상 업로드 요청
  - 사용자가 선택한 영상을 업로드 요청한다. (EPI는 영상을 무조건 EzCloud로 업로드 한다.)
    - EPI가 영상 업로드 결과를 공유한다.
- \[Imaging App > EzServer PMS Integraion\] 영상 공유 요청
  - 사용자가 선택한 영상을 공유 요청한다. (EPI는 영상을 무조건 EzCloud로 업로드 한다.)
    - EPI가 영상 공유 결과를 공유한다.
- \[Imaging App > EzServer PMS Integraion\] 영상 업로드 및 공유 이력 조회 요청
  - Imaging App에서 영상 업로드/공유 내역을 UI에 표시한다.

## Product Functions (제품 주요 기능)

- [7\. Functional Requirements](#_Functional_Requirements_%28기능요구사항%29) 참조

## User Classes and Characteristics (사용자 계층과 특징)

- EzDent-i를 사용하는 모든 customer와 바텍의 CS 직원이 사용자이다.
  - 기술적인 지식이 높지 않은 사용자들이므로 쉽게 사용할 수 있어야 한다.

## Assumptions and Dependencies (가정과 종속 관계)

- 연동을 위해 OneID 및 EzCloud가 구축되어 있어야 한다.

## Apportioning of Requirements (단계별 요구사항)

- v6.2
  - EzCloud 영상 업로드 및 공유 기능 제공

## Backward compatibility (하위 호환성)

- EzCloud 연동을 지원하는 최초의 제품이므로 하위 호환성은 없다.
- 참고
- EzCloud v1.0은 Ez-i Cloud v0.9와 무관한 제품이다.

# Environment (환경)

## Operating Environment (운영 환경)

### Hardware Environment (하드웨어 환경)

- EzServer와 같은 hardware 사양([ESRA-451](https://vts.vatech.co.kr/browse/ESRA-451))을 따른다.

| **Classification**    | **Minimum**                                                 | **Recommended**                                                       |
| --------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------- |
| CPU                   | 듀얼 코어 @3.40GHz                                          | 쿼드 코어 @ 3.40GHz 이상                                              |
| RAM                   | 4GB                                                         | 8GB 이상                                                              |
| OS                    | Windows 10                                                  | Windows 10                                                            |
| Ethernet Network Card | 100M 이터넷 LAN(CAT 5 cable) <br>또는 무선 네트워크 802.11n | 1G 이터넷 LAN(CAT 5E cable) 이상 <br>또는 무선 네트워크 802.11ac 이상 |
| Screen Resolution     | 1280x1024                                                   | 1920×1080                                                             |

- 이 소프트웨어는 EzServer 설치시 함께 설치되는 tool이므로, EzServer의 hardware 환경을 기준으로 한다.

### Software Environment (소프트웨어 환경)

3.1.2.1 OS Environment (운영체제 환경)

- Windows 플랫폼
- 64bit만 모두 지원한다.
- 지원되는 운영 체제
  - - Windows 11
      - Windows 10
      - Windows Server 2021
      - Windows Server 2019
      - Windows 7 이하는 지원하지 않는다.
- Unix/Linux 플랫폼
  - 지원하지 않는다.

  3.1.2.2 OS외 software 환경

- OS 외의 사용자의 환경에 설치되어야 할 필수 software는 없다.

## Product Installation and Configuration (제품 설치 및 설정)

- 이 소프트웨어는 ES 제품 사용에 필수적인 프로그램인 EzServer를 통해 설치된다.

## Distribution Environment (배포 환경)

### Master Configuration (마스터 구성)

- 이전 version과 동일하다.

### Distribution Method (배포 방법)

- EzServer와 함께 USB 메모리에 저장되어 공급되거나 다음 Azure Blob Storage의 Download path에서 download 받을 수 있다.
- essw > Latest Ver > Multi Install Utility V1.0.1 > EzServer >
- EzServer V6.2.0 setup(x64).exe
- 4M 변경 이후, EzUpdater 기능을 통해 LMP로부터 다운로드 가능하다.

### Patch/Update Method (패치와 업데이트 방법)

- 이전 version과 동일하다.

## Development Environment (개발 환경)

### Hardware Environment (하드웨어 환경)

- ES 표준 개발자 Windows PC

### Software Environment (소프트웨어 환경)

- Windows 10 64 bit
- Visual Studio Code
- Git
- Rust 1.76
- Axum 0.6.20
- Tokio 1.28.1
- Sqlx 0.7.4
- ES Product
  - EzServer v6.2
  - EzLauncher v6.2

## Test Environment (테스트 환경)

- 3.1장에 명시된 운영 환경과 동일하다.

## Configuration Management (형상관리)

### Location of Outputs (산출물 위치)

#### Location of Source Code (소스코드 위치)

- <https://ewoosoft@dev.azure.com/ewoosoft/ezserver/_git/ezserver_pms_integration>

#### Location of Documents (문서 위치)

- SharePoint의 [ES Project > EzServer > srs](https://vatechcorp.sharepoint.com/:f:/s/es/ElMbTALCqv1IsFWAKvesyWIBnvFrtQpZtO17p-RVb5lK5w?e=Xh1yto)

### Build Environment (빌드 환경)

- Azure DevOps에서 제공하는 CI를 이용하여 자동 build한다.
  - Cargo를 사용하여 ezserver_pms_integration.exe 실행 파일이 build된다.
  - 패키징 결과물은 Azure DevOps artifact에 자동 upload한다.
  - ezserver-pms-integration- v6.2.0

## Bugtrack System (버그트래킹)

- VTS Project Name : ES_EzServer_PJT관리 - [EZSV](https://vts.vatech.co.kr/projects/EZSV?selectedItem=com.atlassian.jira.jira-projects-plugin%3Asummary-page)
  - 단 여러 tool이 공유하는 project이므로 component를 반드시 PMS Integration으로 설정하여 구분한다

## Other Environment (기타 환경)

# External Interface Requirements (외부 인터페이스 요구사항)

## System Interfaces **(**시스템 인터페이스**)**

### 컴포넌트 정의

| **Abbreviation** | **Description**          |
| ---------------- | ------------------------ |
| EPI              | EzServer PMS Integration |
| EAP              | EzServer AuthProvider    |
| EWS              | EzWebServer              |
| WCN              | EzServer WebConsole      |
| IMA              | Imaging Application      |
| E2DB             | E2 DB                    |
| OID              | OneID                    |
| EZC              | EzCloud                  |

### 인터페이스 정의

#### EzServer WebConsole - EzServer PMS Integration - [link](https://vatechcorp.sharepoint.com/:u:/s/es/EVevRLXvZMtOk-Z2_pAI1NoBv7XCKDPwfFQZuWCsAfunyg?e=bTnYeS)

##### POST /ezcloud/auth-clients

- - - Description - EzServer를 OneID의 client로 등록하도록 요청한다. - EzServer Access token을 요구한다.

##### POST /ezcloud/clients

- - - Description - EzServer를 EzCloud의 client로 등록하도록 요청한다. - EzServer Access token을 요구한다.

##### POST /settings

- - - Description - EzCloud 연동 관련된 setting 저장 요청한다. - EzServer Access token을 요구한다.

#### EzServer PMS Integration - OneID - [link](https://vatechcorp.sharepoint.com/:x:/s/es/ET7AgeivUQFDuRq4HCc3QU0Biik-w7LkUlAgpdypWNiG4A?e=chT6YS) (v1.0.0.a2 sheet 참조)

##### GET /.well-know/server-configuration.json

- - - Description - OneID 설정 및 구성 정보 조회 요청한다.

##### POST /auth/token

- - - Description - Access token 발급 요청한다.

##### POST /auth/clients

- - - Description - OneID auth client 등록 요청한다. - OneID Access token을 요구한다.

##### PUT /auth/clients

- - - Description - OneID auth client 등록 요청한다. - OneID auth client 정보 변경 요청한다. - OneID Access token을 요구한다.

##### POST /tenants/{tenant_uid}/ezserver

- - - Description - EzServer UID 발급 요청한다. - OneID Access token을 요구한다.

##### DELETE /tenants/{tenant_uid}/ezserver/{ezserver_uid}

- - - Description - EzServer UID 삭제 요청한다. - OneID Access token을 요구한다.

##### GET /services

- - - Description - 사용 가능한 서비스 목록 조회 요청한다. - OneID Access token을 요구한다.

#### EzServer PMS Integration - EzCloud - [link](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=Nd9Lmf) (sysconfig sheet 참조)

##### GET /.well-know/server-configuration.json

- - - Description - EzCloud 설정 및 구성 정보 조회 요청한다.

#### EzServer PMS Integration - EzCloud - [link](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=Nd9Lmf) (auth sheet 참조)

##### POST /auth/token/ezserver

- - - Description - EzServer가 사용 가능한 Access token 발급 요청한다. - OneID Access token을 요구한다.

#### EzServer PMS Integration - EzCloud - [link](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=Nd9Lmf) (organization_data sheet 참조)

##### POST /organization-data/upload/presigned-url

- - - Description - "EzCloud로 환자 정보 및 영상 업로드할 수 있는 url" 발급 요청한다. - EzCloud Access token을 요구한다.

##### POST /organization-data

- - - Description - 환자 정보 및 영상 정보 저장 요청한다. - EzCloud Access token을 요구한다.

##### POST /organization-data/shared

- - - Description - 환자 정보 및 영상 정보 공유 요청한다. - EzCloud Access token을 요구한다.

##### POST /organization-data/create-and-share

- - - Description - 환자 정보 및 영상 정보 공유 요청한다. - EzCloud Access token을 요구한다.

#### Imaging Application - EzServer PMS Integration - [link](https://vatechcorp.sharepoint.com/:u:/s/es/EVevRLXvZMtOk-Z2_pAI1NoBv7XCKDPwfFQZuWCsAfunyg?e=bTnYeS)

##### GET /ezcloud/settings

- - - Description - EzCloud 연동 관련된 setting 조회 요청한다. - EzServer access token을 요구한다.

##### POST /ezcloud/cases/filesizes

- - - Description - 원본 영상의 파일 용량 조회 요청한다. - EzServer access token을 요구한다.ㅈ

##### POST /ezcloud/cases/upload

- - - Description - 환자 정보 및 영상을 EzCloud에 업로드 요청한다. - EzServer access token을 요구한다.

##### POST /ezcloud/cases/share

- - - Description - 환자 정보 및 영상을 EzCloud에 업로드 후 공유 요청한다. - EzServer access token을 요구한다.

##### GET /ezcloud/cases

- - - Description - EzCloud 업로드 및 공유 이력 조회 요청한다. - EzServer access token을 요구한다.

#### Imaging Application - OneID - [link](https://vatechcorp.sharepoint.com/:x:/s/es/ET7AgeivUQFDuRq4HCc3QU0Biik-w7LkUlAgpdypWNiG4A?e=chT6YS) (v1.0.0.a2 sheet 참조)

##### POST /auth/token

- - - Description - Access token 발급 요청한다.

##### POST /auth/clients

- - - Description - OneID auth client 등록 요청한다. - OneID Access token을 요구한다.

#### Imaging Application - EzCloud - [link](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=Nd9Lmf) (auth sheet 참조)

##### POST /auth/token

- - - Description - Imaging Applicaion이 사용 가능한 Access token 발급 요청한다. - OneID Access token을 요구한다.

#### Imaging Application - EzCloud - [link](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=Nd9Lmf) (tenants sheet 참조)

##### GET /tenants/memberships?email={email}

- - - Description - 특정 email을 가진 tenant 정보 조회 요청한다. - EzCloud Access token을 요구한다.

#### Imaging Application - EzCloud - [link](https://vatechcorp.sharepoint.com/:x:/s/es/EeEGMS8hhJFGqVnB32i3w2MBXzLqo1AY5UH3MTWp4O6KQw?e=Nd9Lmf) (organization_data sheet 참조)

##### GET /organization-data/upload/limit

- - - Description - 환자 정보 및 영상 업로드 제약 사항 조회 요청한다. - EzCloud Access token을 요구한다

## User Interface **(**사용자 인터페이스)

- [Confidential_EzCloud_v1.0_MMI_Kor_v5.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/ER9Xz50uoMlIvkzQLpjn05sB6D56tj71KdS_DIPdZ69ZJQ?e=D0peeI)

## Hardware Interface (하드웨어 인터페이스**)**

- None

## Software Interface **(**소프트웨어 인터페이스)

- 4.1에 포함한다.

## Communication Interface **(**통신 인터페이스**)**

- None

## Other Interface (기타 인터페이스**)**

- None

# Performance requirements (성능 요구사항**)**

## Throughput (작업처리량)

- 다음 요인을 고려하여 Axum framework에 대한 benchmark를 참고한다.
- EzServer PMS Integration은 Rust로 작성된 Axum framework를 기반으로 개발되었다.
- Cloud에서 운영되는 EzCloud 관련 처리 속도가 지역에 따라 상이할 것으로 예상된다.
- Benchmark - [link](https://sharkbench.dev/web/rust-axum)
- 초당 요청 처리 개수
- 14,730 (median)
- 13,721 (99th percentile)
- 요청 별 지연
- 2.2ms (median)
- 3.9ms (99th percentile)
- 메모리 사용량
- 5.1MB (median)
- 5.2MB (99th percentile)

## Concurrent Session (동시 세션)

- CPU core 개수와 동일한 수의 동시 세션을 지원한다.
  - Rust tokio runtime은 기본값으로 CPU core 개수와 동일한 개수의 thread를 생성한다.
  - EPI는 multi thread 개수에 대한 설정을 하지 않는다.
- EzCloud 영상 업로드시 최대 3개의 동시 세션을 지원한다.

## Response Time (대응시간)

- 이 소프트웨어 자체에 대한 대응시간 요구사항은 없다.

## Performance Dependency (성능 종속 관계)

- HTTP로 통신하는 OneID 및 EzCloud, network 속도 및 system 성능에 종속된다.

## Other Performance Requirements (기타 성능 요구사항**)**

- None

# Non-Functional Requirements (기능 이외의 요구사항**)**

## Safety requirements (안전성 요구사항)

- 전원이 끊기거나, 시스템 crash 등 비정상적으로 종료하는 경우 마지막으로 사용자가 저장하지 않은 data나 환경은 저장되지 않으며 복구할 수 없다.

## Security Requirements (보안 요구사항**)**

- EzCloud로 업로드되는 환자 및 영상 관련 보안 요구 사항은 이미 검토 완료되었다.
  - [Confidential_EzCloud_v1.0_SRS.docx](https://vatechcorp.sharepoint.com/:w:/s/es/EaoqWfCkjPZEhgwM0WnGCK8BA2LRaHDO9qSe_DRaY3ZANg?e=qA7Jyp) - 6.2 보안 요구사항 참조
- 제품은 단일 exe binary 파일로 패키징하여 보기 어렵게 만드는 정도로 소스코드 보안조치를 한다.
- 소프트웨어 인증 방식 사용
  - 설치 파일의 코드 서명을 확인하여 인증된 설치 파일을 사용한다.

## Software System Attributes (소프트웨어 시스템 특성)

### Availability (가용성)

- 병원의 상황에 따라서 24/7 동작해야 할 수 있다.

### Maintainability (유지보수성)

- Rust로 application을 개발하여 다음 측면에서 유지보수성을 증대한다.
  - Modularity: rust의 모듈 시스템 및 trait 정의를 통해 각 모듈을 독립적으로 개발 및 테스트한다.
  - Complexity Management: rust의 타입 시스템과 소유권을 통해 메모리 안정성을 보장한다.

### Portability (이식성)

- Rust로 application을 개발하여 다음 측면에서 이식성을 증대한다.
- Windows이외에서 다른 OS 지원 가능(Linux / macOS)
- 다양한 CPU architecture 지원 가능

### Reliability (신뢰성)

- EPI의 MBTF는 7일이다.
- 통상적으로 하루에 한 번 재부팅을 하기 때문에 7일이면 충분하다.
- 병원의 상황에 따라 PC를 계속 켜 놓는 경우, 최소한 1주일에 한 번은 EzServer를 재시작해야 한다.

### Remaining Attributes (나머지 특성)

- None

## Logical Database Requirements (데이터베이스 요구사항)

### E2 DB

- DB Schema 문서 E2 참조 - [link](https://vatechcorp.sharepoint.com/:x:/s/es/EVRUrYC4C_JLiej32a_YvaIBqDFdBe4zlLEnUbqIc6rZ-w?e=37OCKK)

## Business Rules (비즈니스 규칙)

- None

## Design and Implementation Constraints (설계와 구현 제한사항)

### Standards Compliance (표준준수)

- [ES Coding Convention](https://vks.vatech.co.kr/display/ESDEVELOPER/ES+Coding+Convention)을 준수한다.

### Other Constraints (기타 제한 사항)

- None

## Memory Constraints (메모리 제한 사항)

- TBD

## Operations (운영 요구사항**)**

- EzServer PMS Integration 프로세스는 EzServer Service에서 관리한다.

## Site Adaptation Requirements **(**사이트 적용 요구사항**)**

- None

## Internationalization Requirements (다국어 지원 요구사항)

- EzServer Web Console의 다국어 지원 요구사항과 동일하다.

## Unicode Support (유니코드 지원)

- None

## 64bit Support (64비트 지원)

- 32bit와 64bit 모두 지원한다.
  - EzServer는 windows 64bit를 Target OS로 build되지만 windows 32bit와 64bit에서 모두 사용 가능하다.

## Certification **(**제품 인증)

- EzServer PMS Integration 연동 기능을 제공할 예정인 Imaging Application(EzDent-i)의 인증에 포함된다.

## Field Test (필드 테스트)

- EzServer PMS Integration 연동 기능을 제공할 예정인 Imaging Application (EzDent-i)의 필드 테스트 계획에 포함된다.

## Other Requirements (기타 요구 사항)

- None

# Functional Requirements (기능요구사항)

- UI - [Confidential_EzCloud_v1.0_MMI_Kor_v5.pptx](https://vatechcorp.sharepoint.com/:p:/s/es/ER9Xz50uoMlIvkzQLpjn05sB6D56tj71KdS_DIPdZ69ZJQ?e=bUJuzv)
  - 영상 업로드 기능
    - **EP02_F002_EzDent-iUpload** 참조
  - 영상 공유기능
    - **EP02_F002_EzDent-iShare** 참조
  - 영상 업로드/공유 내역 조회 기능
    - **EP02_F003_EzDent-iRetry** 참조
- Sequence
  - \[EzServer Web Console > EzServer PMS Integraion\] EzCloud 연동 요청
    - ~~사용자가 EzCloud 연동 정보를 입력한다.~~
    - 사용자가 "Login to OneID" 버튼을 클릭한다.
    - EzServer WebConsole이 EPI에 OneID client 등록 요청한다. [POST /ezcloud/auth-clients](#_POST_/ezcloud/auth-clients)
      - EPI가 EzCloud DB에 저장된 EzCloud 연동 정보를 조회한다.
        - EzCloud 연동 정보가 없는 경우에만 다음 절차를 수행한다.

EPI가 OneID에 endpoint 조회를 요청한다. [GET /.well-know/server-configuration.json](#_GET_/.well-know/server-configuratio)

OneID에서 endpoint를 반환한다.

EPI가 OneID에 token 발급 요청한다. [POST /auth/token](#_POST_/auth/token)

OneID가 token을 발급 반환한다.(Hard coded client 정보 사용)

EPI가 OneID에 auth client, redirect url 등록 요청한다. [POST /auth/clients](#_POST_/auth/clients)

OneID가 EzServer를 auth client로 등록한다.

- - - - EPI가 EzServer WebConsole에 OneID login을 위한 정보를 반환한다.
        - EzServer WebConsole이 popup을 통해 URL에 접근한다.
        - 사용자가 popup에서 One ID에 로그인을 시도한다.
- One ID가 EzServer WebConsole에 access token을 반환한다.
  - - - Popup이 종료된다.
      - 사용자가 "save" 버튼을 클릭한다.
- EzServer WebConsole이 EPI에 EzCloud client 등록 요청한다. [POST /ezcloud/clients](#_POST_/ezcloud/clients)
  - EPI가 OneID가 발급한 access token으로부터 tenant UID, oneid UID를 확인한다.
    - EPI가 EzCloud DB에 저장된 EzCloud 연동 정보를 조회한다. EzCloud 연동 정보가 일치하지 않는 경우에만 다음 절차를 수행한다.
      - EPI가 OneID에 token 발급을 요청한다. [POST /auth/token](#_POST_/auth/token)
        - OneID가 token을 발급 반환한다.
      - EPI가 OneID에 EzServer 연동 요청한다. [POST /tenants/{tenant_uid}/ezserver](#_POST_/tenants/{tenant_uid}/ezserver)
        - OneID에서 EzServer UID를 발급한다.
      - EPI가 OneID에 service 정보 조회를 요청한다 [GET /services](#_GET_/services)
        - OneID가 service 정보를 반환한다.
    - EPI가 EzCloud에 endpoint 조회를 요청한다. [GET /.well-know/server-configuration.json](#_GET_/.well-know/server-configuratio_1)
      - EzCloud에서 endpoint를 반환한다.
    - EPI가 EzServer WebConsole에 EzCloud 연동 결과를 반환한다.
    - EzServer Web Console이 EPI API를 통해 다음 settings 정보를 업데이트한다. [POST /settings](#_POST_/settings)

| Section                      | Key                                                               | Value             |
| ---------------------------- | ----------------------------------------------------------------- | ----------------- |
| ThirdPartyIntegration        | authEndpoint                                                      |                   |
|                              | authApiEndpoint                                                   |                   |
|                              | apiEndpoint                                                       |                   |
|                              | appEndpoint                                                       |                   |
|                              | pmsName                                                           | EzCloud           |
|                              | pmsClinicId                                                       |                   |
|                              | tenantUid                                                         |                   |
|                              | ezServerUid                                                       |                   |
|                              | isIntegrated                                                      | true              |
|                              | integrationMode                                                   | tightlyIntegrated |
|                              | syncImagesToPmsOnAcquisition                                      | false             |
| ThirdPartyIntegrationSecrets | ezServerClientIdForPMSAPI / ezServerClientIdForEzCloudAPI         |                   |
| ThirdPartyIntegrationSecrets | ezServerClientSecretForPMSAPI / ezServerClientSecretForEzCloudAPI |                   |

- - \[Imaging App > EzServer PMS Integraion\] EzCloud 연동 정보 조회 요청 [GET /ezcloud/settings](#_GET_/ezcloud/settings) - EPI가 EzCloud 연동 정보를 반환한다.(Section-ThirdPartyIntegration data)
    - \[Imaging App > EzServer PMS Integraion\] 원본 영상 파일 크기 조회 요청 [POST /ezcloud/cases/filesizes](#_POST_/ezcloud/cases/filesizes)
      - EPI가 원본 영상의 파일 크기를 확인한다.
      - EPI가 원본 영상의 파일 크기를 반환한다.
    - \[Imaging App > EzServer PMS Integraion\] 영상 업로드 요청 [POST /ezcloud/cases/upload](#_POST_/ezcloud/cases/upload)
      - \[_업로드 절차_\] - 실패시 최대 3회 재시도
        - ~~EPI가 tenant ID를 검증한다.~~
        - EPI가 DB에 영상 업로드 정보를 저장한다.
        - EPI가 업로드할 zip 파일을 생성한다.
        - EPI가 EzCloud API Server에 signed URL 발급을 요청한다. [POST /organization-data/upload/presigned-url](#_POST_/organization-data/upload/pres)
        - EPI가 zip 파일을 signed URL으로 업로드 한다.
        - EPI가 DB의 영상 업로드 상태를 갱신한다.
        - EPI가 EzCloud API Server에 영상 공유 관련 정보 저장을 요청한다. [POST /organization-data](#_POST_/organization-data)
          - Tenant ID, EzServer ID, 환자/영상 정보
        - EPI가 영상 업로드 결과를 공유한다.
    - \[Imaging App > EzServer PMS Integraion\] 영상 공유 요청 [POST /ezcloud/cases/share](#_POST_/ezcloud/cases/share)
      - 위의 \[_업로드 절차_\]와 동일
      - EPI가 EzCloud API Server에 영상 공유를 요청한다. [POST /organization-data/shared](#_POST_/organization-data/shared)
        - EzCloud가 영상 공유 결과를 반환한다.
      - EPI가 영상 공유 결과를 공유한다.
    - \[Imaging App > EzServer PMS Integraion\] 영상 업로드 및 공유 이력 조회 요청 [GET /ezcloud/cases](#_GET_/ezcloud/cases)
      - EPI가 DB에서 영상 업로드 및 공유 이력을 조회한다.
      - EPI가 영상 업로드 및 공유 이력을 반환한다.
    - \[EzServer Web Console > EzServer PMS Integraion\] EzCloud 연동 중지 요청
      - 사용자가 EzCloud 연동을 중지한다.
        - EzServer WebConsole이 사용자에게 EzCloud 연동 정보 유지/제거 여부 확인을 위한 UI를 표시한다.
      - 사용자가 EzCloud 연동 정보 유지/제거 여부를 선택한다.
      - EzServer WebConsole이 EPI에 EzCloud 연동 중지를 요청한다. [POST /settings](#_POST_/settings)

| Section               | Key          | Value |
| --------------------- | ------------ | ----- |
| ThirdPartyIntegration | isIntegrated | false |
|                       | tenantUid    |       |

- - - - EzCloud 연동 정보 유지를 선택하는 경우, 기존 EzCloud 연동 시 사용한 tenantUid 값을 사용한다. - EzCloud 연동 정보 제거를 선택하는 경우, tenantUid 값으로 빈 문자열("") 을 사용한다.
        - EPI가 EzCloud 연동 정보 유지/제거 여부를 확인한다.
          - EzCloud 연동 정보를 제거하는 경우,
            - EPI가 OneID에 연동 중지를 요청한다. [DELETE /tenants/{tenant_uid}/ezserver/{ezserver_uid}](#_DELETE_/tenants/{tenant_uid}/ezserv)

OneID가 EPI에 연동 중지 결과를 반환한다.

- - - - - EzCloud 연동 정보를 DB에서 제거한다.
          - EzCloud 연동 정보를 유지하는 경우,
            - PMS 연동을 비활성화한다.
          - EPI가 EzServer Web Console에 EzCloud 연동 중지 결과를 반환한다.
    - ~~\[EzServer PMS Integraion > One ID\] One ID client 정보의 redirect url 변경 요청~~
      - ~~EPI 재시작시, EzCloud 연동 여부를 확인한다.~~
        - ~~EzCloud 연동이 활성화되어 있는 경우~~
          - ~~One ID client 정보 변경을 요청한다.~~ [~~PUT /auth/clients~~](#_PUT_/auth/clients)

~~One ID가 EzServer의 client 정보를 변경한다.~~

- - - ~~불필요한 기능으로 판단되면 구현을 생략한다.~~

# Change Management process **(**변경관리 프로세스**)**

Identify the change management process to be used to identify, log, evaluate, and update the SRS to reflect changes in project scope and requirements.

- How are you going to control changes to the requirements?
- Can the customer just call up and ask for something new?
- Does your team have to reach consensus?
- How do changes to requirements get submitted to the team?
- Formally in writing, email or phone call?

This process can be specified in the one of the 'Process Diagram's of the company.

# Document Approvals **(**최종 승인자**)**

Identify the approvers of the SRS document. Approver name, signature, and date should be used.

Name Signature Date

# Reference Materials (참고문헌)

모든 문서는 소스코드 관리 시스템의 파일 위치로 기재한다.

# Appendix (부록)

## Glossary (용어)