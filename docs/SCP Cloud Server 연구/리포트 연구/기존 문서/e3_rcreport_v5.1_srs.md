RC Report

**Software Requirements Specification**

**Product Version: v5.1.0**

**Document Version: v1.0.0**

**Date: 2018/9/7**

**Writer: 천민경(Elly Chun)**

**EWOOSOFT Co., Ltd.**

|  |
| --- |
|  |

문서정보 / 수정 내역

|  |  |
| --- | --- |
| 파일명: | e3\_rcreport\_v5.1\_srs.docx |
| 템플릿 버전: | v3.2 |
| 원안작성자 : | 천민경 |
| 수정작업자 : | 천민경 |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 수정날짜 | 수정자 | 버전 | 추가/수정 항목 | 내 용 |
| 2018.09.07 | 천민경 | v0.9.0 | 전체 | MRD 요구사항을 바탕으로 초안 작성 |
| 2018.09.13 | 천민경 | v0.9.1 | 전체 | ES 내부 Review 반영 |
| 2018.10.11 | 천민경 | V1.0.0 | Title | 외부 Review 후 문서버전 v1.0으로 변경 |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

목 차

[1 Introduction (개요) 6](#_Toc524096073)

[1.1 Purpose (목표) 6](#_Toc524096074)

[1.2 Product Scope (범위) 6](#_Toc524096075)

[1.3 Document Conventions (문서규칙) 7](#_Toc524096076)

[1.4 Terms and Abbreviations (정의 및 약어) 7](#_Toc524096077)

[1.5 Related Documents (관련문서) 8](#_Toc524096078)

[1.6 Intended Audience and Reading Suggestions (대상 및 읽는 방법) 8](#_Toc524096079)

[1.7 Project Output (프로젝트 산출물) 8](#_Toc524096080)

[1.7.1 Output Format (산출물 형태) 8](#_Toc524096081)

[1.7.2 Output Name and Version (산출물명(가칭) 및 버전) 8](#_Toc524096082)

[1.7.3 Patent Information (특허 출원 유무 및 내용) 8](#_Toc524096083)

[2 Overall Description (전체 설명) 9](#_Toc524096084)

[2.1 Product Perspective (제품 조망) 9](#_Toc524096085)

[2.2 Overall System Configuration (전체 시스템 구성) 10](#_Toc524096086)

[2.3 Overall Operation (전체 동작방식) 10](#_Toc524096087)

[2.4 Product Functions (제품 주요 기능) 11](#_Toc524096088)

[2.5 User Classes and Characteristics (사용자 계층과 특징) 12](#_Toc524096089)

[2.6 Assumptions and Dependencies (가정과 종속 관계) 12](#_Toc524096090)

[2.7 Apportioning of Requirements (단계별 요구사항) 12](#_Toc524096091)

[2.8 Backward compatibility (하위 호환성) 12](#_Toc524096092)

[3 Environment (환경) 13](#_Toc524096093)

[4 External Interface Requirements (외부 인터페이스 요구사항) 14](#_Toc524096094)

[4.1 System Interfaces **(**시스템 인터페이스**)** 14](#_Toc524096095)

[4.1.1 정의 및 약어 14](#_Toc524096096)

[4.1.2 컴포넌트 정의 14](#_Toc524096097)

[4.1.3 자료구조 14](#_Toc524096098)

[4.1.4 인터페이스 정의 17](#_Toc524096099)

[4.2 User Interface **(**사용자 인터페이스) 17](#_Toc524096100)

[4.3 Hardware Interface (하드웨어 인터페이스**)** 17](#_Toc524096101)

[4.4 Software Interface **(**소프트웨어 인터페이스) 18](#_Toc524096102)

[4.5 Communication Interface **(**통신 인터페이스**)** 18](#_Toc524096103)

[4.6 Other Interface (기타 인터페이스) 18](#_Toc524096104)

[5 Performance requirements (성능 요구사항) 19](#_Toc524096105)

[5.1 Throughput (작업 처리량) 19](#_Toc524096106)

[5.2 Concurrent Session (동시 세션) 19](#_Toc524096107)

[5.3 Response Time (대응시간) 19](#_Toc524096108)

[5.4 Performance Dependency (성능 종속 관계) 19](#_Toc524096109)

[5.5 Other Performance Requirements (기타 성능 요구사항**)** 19](#_Toc524096110)

[6 Non-Functional Requirements (기능 이외의 요구사항) 20](#_Toc524096111)

[6.1 Safety requirements (안전성 요구사항) 20](#_Toc524096112)

[6.2 Security Requirements (보안 요구사항**)** 20](#_Toc524096113)

[6.3 Software System Attributes (소프트웨어 시스템 특성) 20](#_Toc524096114)

[6.4 Logical Database Requirements (데이터베이스 요구사항) 20](#_Toc524096115)

[6.4.1 File 20](#_Toc524096116)

[6.4.2 Server Directory 21](#_Toc524096117)

[6.4.3 DB Scheme 21](#_Toc524096118)

[6.5 Business Rules (비즈니스 규칙) 21](#_Toc524096119)

[6.6 Design and Implementation Constraints (설계와 구현 제한사항) 21](#_Toc524096120)

[6.7 Memory Constraints (메모리 제한 사항) 21](#_Toc524096121)

[6.8 Operations (운영 요구사항**)** 21](#_Toc524096122)

[6.9 Site Adaptation Requirements **(**사이트 적용 요구사항**)** 22](#_Toc524096123)

[6.10 Internationalization Requirements (다국어 지원 요구사항) 22](#_Toc524096124)

[6.11 Unicode Support (유니코드 지원) 22](#_Toc524096125)

[6.12 64bit Support (64비트 지원) 22](#_Toc524096126)

[6.13 Certification **(**제품 인증) 22](#_Toc524096127)

[6.14 Field Test (필드 테스트) 22](#_Toc524096128)

[6.15 Other Requirements (기타 요구 사항) 22](#_Toc524096129)

[7 Functional Requirements (기능요구사항) 23](#_Toc524096130)

[7.1 Report Dialog 23](#_Toc524096131)

[7.2 Edit Report 23](#_Toc524096132)

[7.2.1 Report 생성/관리 23](#_Toc524096133)

[7.2.2 Page 추가/삭제/Navigating 23](#_Toc524096134)

[7.2.3 Item Box 추가/삭제/편집 24](#_Toc524096135)

[7.2.4 Insert Image 24](#_Toc524096136)

[7.2.5 Edit Image 26](#_Toc524096137)

[7.2.6 Edit Text Box 27](#_Toc524096138)

[7.2.7 Change Template 27](#_Toc524096139)

[7.2.8 Paper Property 28](#_Toc524096140)

[7.2.9 Annotation 28](#_Toc524096141)

[7.2.10 Item Copy & Paste 29](#_Toc524096142)

[7.2.11 Item Multi Select 29](#_Toc524096143)

[7.3 Captured Image List 29](#_Toc524096144)

[7.4 Template Master 30](#_Toc524096145)

[7.4.1 Template Master 기능 실행/종료 30](#_Toc524096146)

[7.4.2 Template List 30](#_Toc524096147)

[7.4.3 Template 생성/관리 30](#_Toc524096148)

[7.4.4 Edit Template 31](#_Toc524096149)

[7.5 Viewing 32](#_Toc524096150)

[7.5.1 Zoom 32](#_Toc524096151)

[7.5.2 Grid 32](#_Toc524096152)

[7.6 Print 32](#_Toc524096153)

[7.6.1 Print 32](#_Toc524096154)

[7.6.2 DICOM Print 32](#_Toc524096155)

[7.7 Export 32](#_Toc524096156)

[7.7.1 Export PDF 32](#_Toc524096157)

[7.7.2 Send E-mail 32](#_Toc524096158)

[8 Change Management process (변경관리 프로세스) 34](#_Toc524096159)

[9 Document Approvals (최종 승인자) 35](#_Toc524096160)

[10 Reference Materials (참고문헌) 36](#_Toc524096161)

[11 Appendix (부록) 37](#_Toc524096162)

[11.1 Glossary (용어) 37](#_Toc524096163)

# Introduction **(개요)**

## Purpose (목표)

* 이 문서는 ES 내부에서 E3에 대해 알고 있는 구성원들이 E3 v5.1부터 제공되는 RC Report 기능을 개발하기 위해 작성한 문서이다.
  + E3 과거 버전의 Report 기능에 대해 전혀 모르는 구성원들을 위한 문서는 아니다.

## Product Scope (범위)

* RC Report 모듈은 RC 시장을 지원하기 위해, 기존 E3 Report 모듈의 편집 기능을 강화하고 Report Template 편집 및 관리 기능을 추가한 모듈이다.
* E3 v5.1에서 신규 추가 및 변경되는 주요 기능은 다음과 같다.
  + Report 기능을 Dialog로 제공한다.
    - 진단 및 Simulation Tab을 조작하면서 Report를 작성할 수 있다.
    - E3 v5.0 이하에서 제공했던 Report Tab은 더 이상 제공하지 않는다.
      * Report Dialog는 기존 Report Tab에서 제공되었던 편집 기능을 모두 제공한다.
      * v5.0 이하 버전에서 작성한 Report File을 v5.1에서 Open 및 편집 가능하다.
    - Report Dialog는 Report Tab License 활성화 유무와 관계없이 제공된다.
      * Simple Viewer에서는 Report 기능이 제공되지 않으므로, Report Dialog를 실행하는 Button을 Disable한다.
  + Report 작성시 Image Box에 Image를 삽입하는 방법은 아래의 3가지가 제공된다.
    - Drag & Drop Captured Image (v5.0 이하 버전에서 제공)
      * 진단 Tab에서 Capture한 Image를 Image Box에 Drag & Drop하여 채우는 기능이다.
    - Auto Fill
      * Image Box의 Property로 지정된 Source Tab, View Type의 Image를 Report 생성시 또는 Update 요청시에 자동으로 Capture하여 Image Box를 채우는 기능이다.
        + 선택할 수 있는 Source Tab은 License가 활성화된 진단 Tab에 국한된다.

진단 Tab은 MPR, Section, 3D PAN, TMJ Tab을 통칭한다.

* + - Capture & Fill Image
      * Image Box의 Capture Button을 클릭한 후, 진단 Tab에서 Capture할 View를 선택하여 Image Box를 채우는 기능이다.
  + Report Annotation 기능을 제공한다.
    - 제공되는 Annotation의 종류는 아래와 같다.
      * Rectangle
      * Ellipse
      * Line
      * Arrow
      * Free Draw
      * Memo
    - Report Dialog에서 추가하는 Annotation과 진단 Tab에서 추가하는 Annotation은 독립적으로 관리되며, 서로 호환되지 않는다.
  + Report Template 편집 및 관리 기능을 제공한다.
    - Template은 File Server에 저장하여 관리하며, Server를 공유하는 모든 E3에서 사용 및 편집할 수 있다.
    - File Server로 공유되는 Template의 동시 편집이나 편집 내용 Merge 기능은 지원하지 않는다.
      * Server를 공유하는 복수의 E3가 같은 Template을 같은 타이밍에 편집하는 경우, Template은 각각의 E3에서 저장을 수행하는 시점에 Overwrite된다.
  + Preset Comment 편집 및 관리 기능을 제공한다.
    - Text Box및 Memo에 Context Menu를 통해 지정한 Comment를 쉽게 입력할 수 있는 기능이다.
    - E3 v5.0 이하 버전에서는 Setting Dialog를 통해 기능이 제공되었으나, E3의 Sharing Setting의 기능 제약으로 인해 Client E3에서는 Preset Comment를 편집 및 관리할 수 없었다.
    - v5.1부터는 Report Dialog에서 Preset Comment 편집 기능을 제공하며, Preset Comment를 DB에서 관리한다.
      * Server에 연결된 모든 Client E3에서 Preset Comment를 편집 및 관리할 수 있다.
      * Preset Comment의 관리 위치가 Setting File에서 DB로 변경됨에 따라, v5.0 이하 버전에서 설정한 Preset Comment는 v5.1로 Migration되지 않는다.
  + Report Item의 Copy & Paste, Multi Select 기능을 제공한다.
* E3 v5.0 이하 버전에서 작성된 Report File의 Migration을 지원한다.
  + 자세한 내용은 2.8장을 참고한다.
  + Report File의 상위 호환성은 보장하지 않는다.
    - v5.1에서 작성된 Report를 v5.0에서 Open하는 경우의 정상 동작하지 않는다.
* Report 출력물의 품질을 향상하기 위해 다음 수정을 적용한다.
  + Multi Capture시 생성되는 Reference Image에 포함되는 Reference Line의 가시성을 개선하고, Style을 변경할 수 있는 Setting을 제공한다.
  + Auto Fill 및 Capture & Fill로 Image를 삽입하는 경우에 한해, 다음과 같은 개선을 적용한다.
    - 개선 내용
      * Capture하는 Image의 Size를 출력될 Size에 맞추어 변경한다.
      * Capture된 Image에 포함되는 Overlay의 Line Thickness 및 Font Size를 출력될 Size에 맞추어 변경한다.
    - 위 개선은 Image가 출력될 Size를 사전에 알고 있는 경우에만 적용 가능하기 때문에, 이미 Capture된 Image를 Drag & Drop으로 삽입하는 경우에는 적용할 수 없다.
* RC Report 기능을 사용하기 위해서는 EzServer v3.0 (EzWebServer v1.2) 이상이 설치되어 있어야 한다.
  + EzServer Version이 v3.0보다 낮은 경우 Template 편집 기능과 Preset Comment 편집 기능을 사용할 수 없다.
    - EzWebServer v1.2부터 RC Report 기능을 위한 API를 지원한다.
    - EzServer v3.0 설치시,
      * Report Template과 Preset Comment를 관리하기 위한 DB Table을 추가한다.
      * Application이 Default로 제공하는 Report Template File을 설치한다.

## Document Conventions (문서규칙)

* E3 SRS를 참조한다.
* 단, 이 모듈은 E3 v5.1부터 지원하기 시작하므로 다른 문서와는 다른 버전 별 지원계획 표기 방법을 적용하도록 한다.
  + v5.1에서 지원하는 항목은 별도의 표시를 하지 않아도 된다.
  + 이후의 버전에서 지원하는 항목은 문장 앞에 (v5.2)와 같이 붙인다.

## Terms and Abbreviations (정의 및 약어)

* E3 SRS와 동일하다.

## Related Documents (관련문서)

* E3 SRS와 동일하다.

## Intended Audience and Reading Suggestions (대상 및 읽는 방법)

* E3 SRS와 동일하다.

## Project Output (프로젝트 산출물)

### Output Format (산출물 형태)

* 소스 코드로 제공한다.

### Output Name and Version (산출물명(가칭) 및 버전)

* VTPluginRCReport64.dll
  + 단, 개발 과정에서 Plugin으로 동작할 필요가 없다고 판단될 경우 Controller Module에 통합될 가능성이 있다.

### Patent Information (특허 출원 유무 및 내용)

* 특허 출원할 내용이 없다.

# Overall Description (전체 설명)

## Product Perspective (제품 조망)

![](data:image/png;base64...)

* RCReport – Report 작성 및 관리, Template 작성 및 관리, Report Print 등을 위한 화면 및 기능을 담당하는 모듈
* Controller – E3에서 각 모듈들의 실행 제어 및 환경 설정을 주 목적으로 하는 모듈
* E3 Tab – E3에서 Tab 형태로 제공하는 모듈을 통칭한다.
  + Diagnosis Tab
    - MPR
    - Section
    - 3D PAN
    - TMJ
  + Simulation Tab
    - Segment
    - Ortho
  + Support Tab
    - Consult
* EzWebServer – File Server 및 DB 기능을 담당하는 Application

## Overall System Configuration (전체 시스템 구성)

![](data:image/png;base64...)

## Overall Operation (전체 동작방식)

* Report Dialog 실행
  + Controller는 Report Dialog를 생성하고 RCReport 모듈의 인스턴스를 전달한다.
  + RCReport는 Default Template을 File Server에서 다운받는다.
  + RCReport는 Default Template File을 Parsing하여 신규 Report를 생성하여 화면에 보여준다.
    - Report에 포함된 Image Box의 속성 중 Fill Type이 Auto Fill인 Image Box가 있으면 Auto Fill을 수행한다.
* Auto Fill 실행
  + RCReport는 Auto Fill을 수행할 Image Box에서 Auto Fill에 필요한 정보를 조회하여 List를 생성한다.
  + RCReport는 Auto Fill 정보 List를 Controller에 전달하여 Auto Fill Image Capture를 요청한다.
  + Controller는 Auto Fill 정보 중 Source Tab 정보를 확인하여, Source Tab으로 지정된 각각의 Tab 모듈에 Auto Fill Image Capture를 요청한다.
    - Tab은 현재 Project Data를 기준으로, Auto Fill 정보에 지정된 View Type에 맞는 View의 Capture Image를 생성한다.
      * 지정된 View Type에 해당하는 View가 생성되지 않았거나, Project Data가 Load되어있지 않은 경우 Tab은 먼저 View를 생성하거나 Project Data를 Load한다.
    - 모든 Image의 Capture가 완료되면, Controller는 RCReport에 Capture된 Image의 정보를 전달하여 Image Box의 Update를 요청한다.
  + RCReport는 Capture된 Image로 Image Box를 채운다.
* Capture & Fill Image 실행
  + 사용자가 Image Box상의 Capture Button을 Click하면 RC Report는 Capture Mode와 Image Box의 정보를 Controller에 전달하여 Capture 실행을 요청한다.
  + Controller는 현재 활성화된 tab에 Capture Mode와 Image Box 정보를 전달하여 Capture를 실행할 것을 요청한다.
    - Tab은 전달받은 Capture Mode에 맞는 Capture 기능을 실행하여, View 지정 또는 Region 지정 대기 상태로 전환한다.
      * View 지정 또는 Region 지정 대기 상태에서는 Tab의 Control Panel, Toolbar, Tab 전환 Button 등은 모두 Disable 된다.
    - 사용자가 Capture할 View를 Click하면 Tab은 지정된 View를 Capture한다.
  + Capture가 완료되면 Controller는 RCReport에 Capture된 Image의 정보를 전달하여 Image Box의 Update를 요청한다.
  + RCReport는 Capture된 Image로 Image Box를 채운다.
* Save Report
  + 사용자가 Report 저장을 요청하면 RCReport는 저장할 Report의 Title과 Comment를 입력할 수 있는 Dialog를 표시한다.
  + 사용자가 Report Title과 Comment를 입력하고 OK를 Click하면 RCReport는 현재 작성중인 Report에 포함되어 있는 Captured Image 중 File Server에 저장이 필요한 Image를 PNG 포맷으로 저장하고, Report 작업내용을 XML 포맷의 Report File로 저장한다.
  + RCReport는 EzServer에 Report File과 Image File들의 저장을 요청한다.
  + RCReport는 EzServer에 Report File 정보를 DB에 추가할 것을 요청한다.
* Template Master 시작
  + 사용자가 Template Master 모드 시작을 요청하면 RCReport는 현재 작업중인 Report의 저장 여부를 사용자에게 확인한다.
  + RCReport는 사용자의 선택에 따라 작업중인 Report를 저장하고, 작업중인 Report Data를 Clear한 후 Report Dialog의 UI 구성을 Template Preview Mode로 변경한다.
  + RCReport는 DB에 등록되어 있는 Template을 조회하여 Template List를 생성하고, Default Template File을 File Server에서 다운받아 Template Preview를 구성하여 보여준다.
* Add Template
  + 사용자가 Add Template Button을 Click하면, RCReport는 Blank 상태의 Template를 생성하여 화면에 표시하고, Report Dialog의 UI구성을 Template Edit Mode로 변경한다.
    - Blank Template 생성시의 Page Setting은 Setting에 지정된 값을 사용한다.
  + RC Report는 EzServer에 추가된 Template 정보 및 Template File의 저장을 요청한다.

## Product Functions (제품 주요 기능)

* Edit Report
  + Report 생성/관리
  + Page 추가/삭제/Navigating
  + Item Box 추가/삭제/편집
  + Insert Image
    - Auto Fill
    - Drag & Drop Captured Image
    - Capture & Fill Image
  + Edit Image
  + Edit Text Box
  + Change Template
  + Paper Property
  + Annotation
  + Item Copy & Paste
  + Item Multi Select
* Captured Image List
* Template Master
* Print
  + Print
  + DICOM Print
* Export
  + Export PDF
  + Send E-mail

## User Classes and Characteristics (사용자 계층과 특징)

* E3 SRS와 동일하다.

## Assumptions and Dependencies (가정과 종속 관계)

* 해당 사항 없음

## Apportioning of Requirements (단계별 요구사항)

* 해당 사항 없음

## Backward compatibility (하위 호환성)

* E3 v5.0 이하 버전에서 작성된 Report File의 Migration을 지원한다. Report가 작성된 E3 버전에 따른 Migration 지원 방법은 아래와 같다.
  + 4.x, 5.0
    - E3에서 Report File을 Open시에 v5.1 Format으로 Migration한다.
  + 1.x->5.1
    - 제품 설치 시점에 VTE3Migration Tool을 통해 4.x 버전으로 한 차례 Migration을 수행한 후, 사용자가 Report File을 Open시에 v5.1 Format으로 Migration한다.
* v5.0 이하 버전에서 설정한 Preset Comment는 v5.1로 Migration되지 않는다.
  + v5.1부터 Preset Comment의 저장 위치가 Setting File에서 DB로 변경되는데, EzServer의 Update 설치 시점과 E3의 Update 설치 시점, Client가 Preset Comment를 사용하는 시점 등 다양한 변수로 인해 Migration을 지원하기 위한 구현 난이도가 높기 때문이다.

# Environment (환경)

* E3 SRS와 동일하다.

# External Interface Requirements (외부 인터페이스 요구사항)

## System Interfaces **(**시스템 인터페이스**)**

### 정의 및 약어

|  |  |
| --- | --- |
| **약어** | **설명** |
| CTR | Controller |
| RUI | Repot UI Manager |
| RVM | Report View Manager |
| IOM | IO Manager |
| EXR | Export Report |
| CIM | Capture Image Manager |

### 컴포넌트 정의

* 2.2장과 동일하다.

### 자료구조

/\*\*

\* @brief Auto Fill Image Type

\*/

enum EAutoFillImgType

{

eAFIUnknown,

eAFISingleView,

eAFIMultiSliceGroup,

eAFIReference

};

/\*\*

\* @brief Auto Fill의 Source Tab Type

\*/

enum ETabType

{

eTabTypeUnknown,

eTabTypeMPR,

eTabTypeSection,

eTabType3DPAN,

eTabTypeTMJ

};

/\*\*

\* @brief Auto Fill의 View Type

\*/

enum EAutoFillViewType

{

eAFViewTypeUnknown,

eAFViewTypeAxial,

eAFViewTypeSagittal,

eAFViewTypeCoronal,

eAFViewType3D,

eAFViewTypeScout,

eAFViewTypePanorama,

eAFViewType3DPanorama,

eAFViewType3DPANScout,

eAFViewTypeAutoPanorama,

eAFViewTypeBoneDensity,

eAFViewTypeTMJ3D,

eAFViewTypeTMJScout,

eAFViewTypeTMJFrontal,

eAFViewTypeSection

};

/\*\*

\* @brief Auto Fill을 수행할 View의 Group Type

\*/

enum EAutoFillGroupType

{

eAFGroupTypeUnknown,

eAFGroupTypeLeft,

eAFGroupTypeRight,

eAFGroupTypeSingle,

eAFGroupTypeDual

};

/\*\*

\* @brief Reference Image의 Type

\*/

enum ERefImageType

{

eRefImgScout,

eRefImgPanorama

};

/\*\*

\* @brief Auto Fill Image Capture를 Tab에 요청할 때 필요한 정보

\* @remarks Single Image Box일 경우 사용한다.

\*/

struct SAutoFillImageInfo

{

EAutoFillImgType eAFImageType;

ETabType eAFTabType;

EAutoFillViewType eAFViewType;

EAutoFillGroupType eAFGroupType;

VBOOL bWithOverlay;

VBOOL bApplyFilter;

QString strImageBoxID;

QSizeF szImgSize;

};

/\*\*

\* @brief Auto Fill Image Capture를 Tab에 요청할 때 필요한 정보

\* @remarks Multi Image Box일 경우 사용한다.

\*/

struct SAutoFillMultiImageInfo : public SAutoFillImageInfo

{

VINT nRow;

VINT nColumn;

QVector<VINT> vecSliceNumber;

VBOOL bWithScoutReference;

QSize szScoutRefImgSize;

QString strScoutRefImgBoxID;

VBOOL bWithPanoReference;

QSize szPanoRefImgSize;

QString strPanoRefImgBoxID;

};

/\*\*

\* @brief Tab에서 Capture한 Image 정보

\*/

struct SCapturedImg

{

VBOOL bHasPixelSpacing;

VFLOAT fPixelSpacing[2];

QImage capturedImage;

};

/\*\*

\* @brief Tab에서 Capture한 2D View Image 정보

\*/

struct SCaptured2DViewImg : public SCapturedImg

{

VINT nSliceNum;

VINT nTotalSliceNum;

VFLOAT fThickness;

VFLOAT fInterval;

QString strLeftDirection;

QString strRightDirection;

SEffectOption sEffectOption;

SCaptured2DViewImg()

: SCapturedImg()

, nSliceNum(-1)

, nTotalSliceNum(-1)

, fThickness(0)

, fInterval(0)

{}

};

/\*\*

\* @brief Capture한 Image 정보를 Report Module에 전달하기 위해 사용하는 자료구조

\* @remarks Single Image Box일 경우 사용한다.

\*/

struct SAutoFillCapturedData

{

QString strImageBoxID;

QVector<SCapturedImg> vecCapturedImage;

};

/\*\*

\* @brief Capture한 Image 정보를 Report Module에 전달하기 위해 사용하는 자료구조

\* @remarks Multi Image Box일 경우 사용한다.

\*/

struct SAutoFillMultiCapturedData : public SAutoFillCapturedData

{

SCapturedImg sRefScoutImgInfo;

SCapturedImg sRefPanoImgInfo;

};

### 인터페이스 정의

* 구현이 완료된 내용에 대한 자료구조 및 인터페이스 리스트는 별도로 관리하지 않는다.
* 신규 추가될 기능에 대한 상세 인터페이스는 구현 시에 정의한다.

## User Interface **(**사용자 인터페이스)

* E3 v5.1 MMI를 참고한다.

## Hardware Interface (하드웨어 인터페이스**)**

* 해당 없음

## Software Interface **(**소프트웨어 인터페이스)

* 해당 없음

## Communication Interface **(**통신 인터페이스**)**

* 해당 없음

## Other Interface (기타 인터페이스)

* 해당 없음

# Performance requirements (성능 요구사항**)**

## Throughput (작업 처리량)

* 해당 사항 없음.

## Concurrent Session (동시 세션)

* 단일 session만 지원한다.
* EzWebServer의 동시 세션 요구사항에 대해서는 해당 srs를 참고한다.

## Response Time (대응시간)

* RC Report Module에 요구되는 주요 대응시간 요구사항은 E3 SRS를 참고한다.

## Performance Dependency (성능 종속 관계)

* Template의 Page 수, Image Box 수, Multi Image Box의 Cell 분할 개수에 따라 Auto Fill 처리시간이 달라진다.
* EzWebServer와 연결된 네트워크 속도에 따라 다음 기능들의 속도가 결정된다.
  + Captured Image List 생성
  + Open/Save Report
  + Open/Save Template
* E-mail에 첨부하는 파일 크기와 네트워크 속도에 따라 E-mail 전송시간이 결정된다.
* Printer와의 통신 속도 및 Printer 성능에 따라 인쇄 속도가 결정된다.

## Other Performance Requirements (기타 성능 요구사항**)**

* 해당 사항 없음.

# Non-Functional Requirements (기능 이외의 요구사항**)**

## Safety requirements (안전성 요구사항)

* 작업 도중 비정상적으로 종료되는 경우 작업 내용은 보장되지 않는다.

## Security Requirements (보안 요구사항**)**

* E3 SRS를 참고한다.

## Software System Attributes (소프트웨어 시스템 특성)

* E3 SRS와 동일하다.

## Logical Database Requirements (데이터베이스 요구사항)

### File

* Setting
  + Report에서 사용하는 Setting 정보는 E3 Controller SRS를 참고한다.
* Log
  + E3 SRS를 참고한다.
* File Format
  + 별도 문서 e3\_v5.1\_RCReport\_FileFormat.xlsx를 참고한다.
    - Report File Format
    - Report Template File Format
    - Report Header File Format
* Image File
  + Auto Fill 및 Capture & Fill 기능으로 삽입한 Image는 기존 Viewer Tab에서 Capture한 Image와 다른 방식으로 관리된다.
    - DB에 영상 정보가 저장되지 않고, File Server에 File만 저장된다.
    - Consult Tab 및 Report Dialog의 Captured Image List에 표시되지 않는다.
    - Report를 삭제하면 Image도 함께 삭제된다.
  + Image File Format
    - 24bit RGB
      * Open Inventor의 Offscreen Rendering 기능을 사용하여 Capture한 상태에서 별도의 가공/변환을 하지 않는다.
    - PNG Format
      * 무손실압축을 적용하여 저장한다.
      * Pixel Spacing(mm/Pixel) 값은 Image Box의 Image 속성으로서 Report File에 저장한다.

### Server Directory

* 자세한 내용은 관련 문서 [e3\_v5.1\_FileServer\_Directory구조.xlsx](https://vatechcorp.sharepoint.com/%3Ax%3A/s/es/EcTrh96Zqi5HoyEFIU_o1WwBJZmuw80iQUxsNo44-kF-BA?e=PdYMnB)를 참고한다.
* Auto Fill, Capture & Fill Image File
  + File Server에 저장되는 Report File의 File명과 동일한 이름의 Directory를 생성하여 그 하위에 저장한다.
    - Image File이 Report에 종속되어 저장되므로, Report의 Save As가 발생하는 경우 동일한 Image가 File Server에 중복 저장될 수 있다.
      * 하나의 Image를 복수의 Report가 참조하는 방식은 채용하지 않는다.
      * E3의 동작방식상 복수의 E3가 Report를 추가/삭제할 수 있는데, 예를 들어 "PC A에서 Image A를 참조하는 Report A로 작업하는 도중에, PC B에서 Report A를 삭제"하는 경우Image의 삭제 타이밍을 결정하기 어렵기 때문이다.
* Report Template
  + E3 v4.0부터 배포하였으나 실제로는 사용되지 않은 Report Template File을 EzServer Update 설치시 삭제한다.
  + Report Template은 제품이 기본으로 제공하는 Template과 사용자가 추가한 Template을 Directory를 분리하여 관리한다.

### DB Scheme

* 자세한 내용은 관련 문서 [dbmanager\_srs.doc](https://vatechcorp.sharepoint.com/%3Af%3A/s/es/Es50EZEzirVIt_GgR4bd1hkB9ul-uWRbHntUJOgxYVsatw?e=nuTTtO)를 참고한다.
* 다음 정보를 DB에서 관리한다.
  + Report File
  + Report Template
  + Preset Comment
* Report Template과 Preset Comment를 관리하기 위한 DB Table을 EzServer Update 설치시 추가한다.
* E3 v4.0부터 추가되었으나 사용하지 않는 기존 Report Template DB Table을 EzServer Update 설치시 삭제한다.

## Business Rules (비즈니스 규칙)

* 해당사항 없음.

## Design and Implementation Constraints (설계와 구현 제한사항)

* E3 SRS와 동일하다.

## Memory Constraints (메모리 제한 사항)

* E3 SRS와 동일하다.

## Operations (운영 요구사항**)**

* 해당 사항 없음.

## Site Adaptation Requirements **(**사이트 적용 요구사항**)**

* 해당 사항 없음.

## Internationalization Requirements (다국어 지원 요구사항)

* E3 SRS와 동일하다.

## Unicode Support (유니코드 지원)

* E3 SRS와 동일하다.

## 64bit Support (64비트 지원)

* E3 SRS와 동일하다.

## Certification **(**제품 인증)

* E3 SRS와 동일하다.

## Field Test (필드 테스트)

* Field Test를 진행할 계획이 없다.

## Other Requirements (기타 요구 사항)

* 해당 사항 없음.

# Functional Requirements (기능요구사항)

## Report Dialog

* Report를 작성할 수 있는 Report Dialog를 제공한다.
  + Report Dialog는 Modeless 속성으로, 진단 Tab 및 Simulation Tab을 사용하면서 Report Dialog를 통해 Report를 작성할 수 있다.
* E3 v5.0 이하 버전에서 제공되던 Report Tab은 더이상 제공하지 않는다.
  + Report Dialog는 기존 Report Tab이 제공하던 편집 기능을 모두 제공한다.
  + v5.0 이하 버전에서 작성된 Report File을 v5.1에서 Open 및 편집 가능하다.
* Report Dialog는 Report Tab의 License 활성화 유무와 관계없이 제공된다.
  + Simple Viewer에서는 Report 기능이 제공되지 않으므로, Report Dialog를 실행하는 Button을 Disable한다.

## Edit Report

### Report 생성/관리

#### Create New Report

* Default Template을 적용하여 신규 Report를 생성한다.
* 다음 시점에 Create New Report가 발생한다.
  + Control Panel의 "Create New Report" Button을 Click한 경우
  + Report Dialog를 Open한 경우
  + Change Template를 실행한 경우
  + 사용자가 Page 삭제 기능으로 마지막 Page를 삭제한 경우

#### Open Report

* DB에 저장된 Report List를 Dialog로 보여주고, 사용자가 선택한 Report를 Open한다.
* 상세 동작 방식은 v5.0과 동일하다.

#### Save Report to DB

* 작성한 Report를 Rest API를 통해서 DB에 저장한다.
* 상세 동작방식은 v5.0과 동일하다.

### Page 추가/삭제/Navigating

#### Add Page

* 편집중인 Report의 가장 마지막 Page로 Blank Page를 추가한다.
* Blank Page의 Paper Property는 현재 적용되어 있는 Template과 동일하다.
* 최대 10페이지까지 추가할 수 있다.

#### Delete Page

* 사용자가 현재 편집중인 Page를 삭제한다.
* 사용자가 마지막 1Page를 삭제한 경우, Default Template으로 새로운 Report가 생성된다.

#### Page Navigating

* Control Panel의 Button으로 Page를 이동할 수 있다.
* v5.0에서는 Work Space 하단의 UI로 기능이 제공되었으나, v5.1부터는 Control Panel의 UI로 제공된다.
* 상세 동작 방식은 v5.0과 동일하다.

### Item Box 추가/삭제/편집

#### Add Item Box

* Control Panel을 통해 다음 Item Box를 추가할 수 있다.
  + Single Image Box
  + Multi Image Box
    - Multi Image Box를 클릭하면 Image의 Cell 분할(Row & Column)과 Reference Image 추가 여부를 선택할 수 있는 Dialog가 표시된다.
      * Row, Column의 설정 범위는 1~20이다.
      * Reference Image 추가가 선택되어 있으면 Reference Image Box가 생성되어 Report Page에 추가된다.
        + Reference Image Box는 Multi Image Box와 같은 Page에, Multi Image Box보다 상단에 추가된다.
        + Multi Image Box의 Source Tab 설정에 따라 Reference Box는 1개 또는 2개가 추가된다.

1개 추가되는 경우 (MPR Type)

MPR Tab

TMJ Tab

2개 추가되는 경우 (MPR Type, Panorama Type)

Section Tab

3D PAN Tab

* + Text Box
* Item Box는 Application이 지정한 Default Size/Position으로 추가된다.

#### Delete Item Box

* Item Box를 선택한 상태에서 Control Panel의 Button이나 Delete Key 입력, Context Menu의 Delete 선택으로 Item Box를 삭제할 수 있다.

#### Edit Item Box

* Mouse 조작으로 Item Box의 크기, 위치를 변경할 수 있다.
* 크기, 위치 변경은 각 Page의 편집 가능 영역 내에서만 가능하다.
* "편집 가능 영역"이란 각 Page에서 Margin을 제외한 영역이다.
* Header/Footer영역도 편집 가능 영역에 포함된다.
* Item Box의 크기, 위치 변경으로 인해 Item Box가 서로 겹쳐질 수 있다.

#### Copy & Paste

* 선택한 Item Box를 Copy & Paste 할 수 있다.
* 주요 요구사항은 7.1.10장 Item Copy & Paste를 참고한다.

### Insert Image

#### Auto Fill

* Image Box의 Property로 지정된 Source Tab, View Type의 Image를 현재 Project를 기준으로 캡쳐하여 자동으로 Image Box를 채운다.
* 채워진 Image는 Project 변경에 영향을 받지 않는다.
* Update Image
  + Update가 실행되는 조작은 다음과 같다.
    - Toolbar의 Update Image Button을 클릭하면 현재 Report 내에 Image Source Type이 Auto Fill로 지정되어 있는 모든 Image Box를 Update한다.
    - Image Source Type이 Auto Fill인 Image Box의 Property중 Image Update를 발생시키는 Property를 변경하면 해당 Image Box를 Update한다.
      * Source Tab, View Type
      * Image Fit Mode
      * With Overlay
      * Apply Filter
  + Auto Fill Image는 Update시점의 Project를 기준으로 생성되며, Change Slice 기능을 통해 적용한 Slice 번호, Thickness, Interval 정보는 초기화된다.

#### Drag & Drop Captured Image

* Report Dialog 하단에 표시되는 Captured Image List에서 Image의 Thumbnail을 선택, Image Box에 Drag & Drop하여 Image를 삽입할 수 있다.
* Single Image Box에는 Single Capture Image만, Multi Image Box에는 Multi Capture Image만 삽입할 수 있다.
* Reference Image Box에는 Drag & Drop으로 Image를 삽입할 수 없고, 연결된 Multi Image Box에 Image가 삽입되면 자동으로 Image가 채워진다.
* Multi Image Box에 Multi Capture Image를 Drag & Drop하면 Image Box에 추가할 Image를 선택할 수 있는 Dialog가 표시된다. 이 Dialog는 Change Image 기능에서 제공하는 것과 동일한 Dialog를, Thickness/Interval 선택 UI만 Hide하여 제공한다.
* 위에서 언급한 것 외의 다른 기능 동작 방식은 v5.0과 동일하다.

#### Capture & Fill Image

* Image Box의 Capture Button을 클릭한 후, 진단 Tab에서 Capture할 View를 선택하여 Image를 Capture하여 Image Box를 채우는 기능이다.
  + Capture Button은 Image Box의 Fill 속성이 Captured Image이고 Image가 Insert 되어있지 않은 경우, Image Box에 Mouse Hover하면 표시된다.
    - Single Image Box: Window Capture Button과 Region Capture Button이 제공된다.
    - Multi Image Box: Multi Capture Button이 제공된다.
    - Reference Image Box에는 Capture Button이 표시되지 않는다.
* Image Box의 Capture Button을 클릭하면 Capture 영역 지정 대기 모드가 된다.
  + Main Module로 Focusing이 전환되며, Main Module이 Top으로 표시된다.
  + View 지정 대기 모드에서는 Main Menu, Toolbar, Control Panel, Tab Button이 모두 비활성화된다.
  + Single Image Box에서 Window Capture Button을 Click했을 때에는 모든 View에 Mouse Hover시 Capture Button이 표시된다.
  + Multi Image Box에서 Capture Button을 Click했을 때에는 Multi Capture를 지원하는 View에 Mouse Hover 했을 때에만 Capture Button이 표시된다.
  + With Overlay, Without Overlay 선택을 지원하는 View에서는 With Overlay, Without Overlay Button을 제공한다.
* Multi Image Box에서 Capture & Fill Image를 선택한 경우,
  + Capture를 실행하는 View의 Focus된 Slice를 중심으로 Image Box에 지정된 Cell Layout 속성에 정의된 개수만큼 캡쳐되어 Image Box에 추가된다.
  + Reference Image는 자동으로 캡쳐되어 Multi Image Box와 연결된 Reference Image Box에 추가된다.

### Edit Image

#### Move

* Image Box 내에서 Image의 상대적인 위치를 변경할 수 있다.
* 기능 동작 방식은 v5.0과 동일하다.

#### Resize

* Image Box 내에서 Image의 크기를 변경할 수 있다.
* 기능 동작 방식은 v5.0과 동일하다.

#### Change Image Box Property

* 다음 항목을 Property 창에서 변경할 수 있다. 각각의 Property 항목에서 지정 가능한 범위는 별도 문서 e3\_v5.1\_RCReport\_Property.xlsx를 참고한다.
  + Image Fill
    - Image Capture
    - Auto Fill
      * Source Tab
      * View Type
  + Display Option
    - Image Fit Mode
    - With Overlay
    - Ruler
  + Box Property
* Multi Image Box에서는 아래 Option을 추가 제공한다.
  + Multi Image Layout (Row, Column)
  + Reference Image Box 표시 여부
* Image Source Type이 Auto Fill인 상태에서, Source Tab, View Type, Image Fit Model, With Overlay, Apply Filter 설정을 변경하면 Image의 Update가 발생한다.
* Image Source Type이 변경되면 Image Box에 삽입되어 있는 Image를 Clear한다.

#### Change Image (Select Slice)

* Report Tab에서 제공하는 Dialog를 통해 Auto Fill된 Image의 Slice를 변경할 수 있다.
* Change Image 기능은 Image Box의 속성이 아래와 같은 조건일 때 사용할 수 있다.
  + Image Fill Type이 Auto Fill인 경우
  + Source View Type이 2D View에 속하는 경우
* Change Image Dialog를 실행하면 2D Image의 Preview를 표시한다.
  + Preview Image는 Update Performance를 위해 실제 Report에 삽입될 것보다 저해상도로 캡쳐될 수 있다.
  + Preview Image의 생성은 Select Slice Dialog 실행 시점의 Project를 기반으로 한다.
    - Select Slice 기능을 실행하기 전에 Image Box에 추가되어 있던 Image와는 다른 Image가 보여질 수 있다.
  + Preview Image의 with overlay, apply filter Property는 Image Box의 Property를 따르며, Select Slice Dialog 내에서 변경할 수 없다.
* Preview에 표시되는 이미지상에서 Mouse Wheel을 하거나, 좌측의 Scroll Bar를 조작하여 Slice를 변경할 수 있다.
* Single Image Box
  + 사용자는 Preview창에서 추가할 Slice를 한 장만 선택할 수 있다.
* Multi Image Box
  + 사용자는 Multi Slice Image Preview 창에서 추가할 Slice를 복수 선택할 수 있다.
    - Slice 연속 선택/불연속 선택 모두 가능하다.
    - Multi Image Box의 Cell 분할 속성으로 지정된 Slice 개수보다 적을 수 있으나, 지정된 Slice 개수를 초과하여 선택할 수 없다.
* Change Image Dialog에서 Slice의 Thickness, Interval을 변경할 수 있다.
* 사용자가 Slice를 선택 후 OK 버튼으로 종료하면,
  + 지정된 Slice를 인쇄 품질로 캡쳐하여 Image Box를 채운다.
  + Multi Image Box와 연결된 Reference Image Box도 함께 Update된다.

#### Delete Image

* + Image Box의 Context Menu를 통해 삽입된 Image를 삭제할 수 있다.
  + Auto Fill 속성일 경우 Delete Image 기능을 사용할 수 없다.
  + Reference Image Box에서는 Delete Image 기능을 사용할 수 없다.
  + Multi Image Box일 경우 연결되어 있는 Reference Image Box의 Image도 삭제된다.

### Edit Text Box

#### Edit Text

* Text Box에 자유롭게 Text를 입력하거나, Preset Comment를 입력할 수 있다.
* Text Box를 더블클릭하면 Text 편집 모드가 된다.
* Text Box 편집 모드에서 Context Menu를 통해 Preset Comment를 입력할 수 있다.

#### Preset Command

* Preset Comment Dialog를 통해 Preset Comment를 추가/수정/삭제할 수 있다.
* Preset Comment는 DB에 저장되어 관리된다.
  + E3 v5.0에서 Setting으로 관리되던 Preset Comment는 Migration 되지 않는다.

#### Change Text Box Property

* 다음 항목을 Property 창에서 변경할 수 있다. 각각의 Property 항목에서 지정 가능한 범위는 별도 문서 e3\_v5.1\_RCReport\_Property.xlsx를 참고한다.
  + Font Size
    - Font Size가 변경되었을 때의 Text Box 크기는 자동 조절된다.
  + Font Color
  + Text Alignment
  + Box Property

### Change Template

#### Template List Dialog

* 사용자가 Change Template Button을 Click하면,
  + 편집 중이던 Report가 있을 경우 해당 Report의 저장 여부를 확인하고 저장한다.
* Template List Dialog는 DB에 등록되어 있는 Template을 List로 보여준다.
* 사용자가 Template을 선택하면 해당 Template의 Preview를 보여준다.
  + Preview 화면에서 Template의 모든 Page를 확인 가능하다.
  + Template Preview에서는 Box의 종류, Image Box의 경우에는 Image Source Type을 Watermark 형태로 보여준다.

#### Change Template

* 사용자가 Change Template Dialog에서 변경할 Template을 선택하고 OK로 종료하면,
  + 사용자가 선택한 Template으로 신규 Report를 생성한다.

### Paper Property

* Report 편집중에 편집 용지에 대한 아래 속성을 변경할 수 있다.
  + Paper Size
  + Orientation
  + Margin
* 변경한 속성은 Report의 모든 Page에 공통으로 적용된다.
* Paper Size를 변경한 경우,
  + Report에 포함되는 Item의 크기 및 위치는 변경되지 않는다.
    - 단, 편집 영역을 완전히 벗어나는 Item의 경우 정해진 규칙에 맞추어 재배치된다.
      * 재배치 규칙: <https://vks.vatech.co.kr/pages/viewpage.action?pageId=22982111>

### Annotation

#### Insert Annotation

* Toolbar의 Button을 통해 Annotation을 입력할 수 있다.
* Annotation 입력 중에는 Mouse Cursor가 해당 Annotation에 해당하는 Cursor로 변경된다.
* Annotation의 입력 방식은 크게 다음 3가지로 분류된다.
  + 1점 입력
    - Memo
  + 2점 입력
    - Rectangle
    - Ellipse
    - Line
    - Arrow
  + Left Button Press & Drag로 연속 입력
    - Free Draw
* Annotation은 편집 가능 영역 내에서만 입력할 수 있다.
* 입력되는 Annotation의 Default Style은 Setting을 따른다.
* 각각의 Annotation를 추가한 후에도 입력 모드가 유지되어 연속 입력이 가능하다.
* 편집 영역에서 Mouse 우클릭을 하거나 Esc Key 입력, Toolbar Button 클릭으로 입력 모드를 종료한다.

#### Edit Annotation

* Annotation을 선택하면 표시되는 Control Point를 조작하여 Annotation의 크기를 변경할 수 있다.
* Annotation을 선택한 상태에서 Control Point외의 부분을 Click & Drag하여 위치를 이동할 수 있다.

#### Delete Annotation

* Annotation을 선택한 상태에서 Context Menu의 Delete 선택, Delete Key 입력으로 Annotation을 삭제할 수 있다.

#### Memo

* 입력 방법 및 편집 방법은 진단 Tab의 Memo와 동일하다.
* Memo 입력 모드에서 Context Menu를 통해 Preset Comment를 입력할 수 있다.
  + Preset Comment는 Text Box에서 제공되는 것과 동일하다.

#### Change Annotation Property

* Annotation의 Line Color, Line Style 속성을 변경할 수 있다.
* Memo의 경우 추가적으로 Font Size, Font Color, Background Color, Background Transparency를 변경할 수 있다.
* 변경한 속성은 Report File에 저장된다.

#### Turn On/Off Annotation

* 편집 중인 Report에 포함된 모든 Annotation의 Show/Hide를 변경할 수 있다.
* Turn On/Off 기능으로 Show/Hide한 상태는 Report File에 저장되지 않는다.

#### Delete All Annotation

* 편집 중인 Report에 포함된 모든 Annotation을 일괄 삭제할 수 있다.

### Item Box Copy & Paste

* 선택한 Item Box를 Copy & Paste 할 수 있다.
  + 단축키 및 Context 메뉴를 통해 실행할 수 있다.
* Copy를 실행하면 Item Box에 입력된 Contents도 함께 Copy된다.
  + Reference Image Box는 선택되어 있지 않더라도, Copy된 Multi Image Box의 Property에 사용으로 설정되어 있으면 함께 복사된다.
  + Multi Image Box를 선택하지 않은 상태로 Reference Image Box만 Copy를 시도할 경우 Reference Image Box는 Copy되지 않는다.
* Header, Footer Item Box는 Copy & Paste 기능을 제공하지 않는다.
* Copy한 내용을 Clear 하는 조건은 다음과 같다.
  + 다음 Copy를 실행하면 이전에 Copy된 내용은 Clear된다.
    - Item을 선택하지 않은 상태로 Copy를 실행하면 클립보드는 빈 상태가 된다.
  + Template Master 실행
  + Report Dialog 종료
* Copy한 내용은 Create New Report나 Change Template을 실행한 후에도 Paste 할 수 있다.
* Copy & Paste는 Item Box를 Multi Select 한 상태에서도 사용할 수 있다.

### Item Box Multi Select

* Item Box를 Multi 선택하여 편집할 수 있다.
  + Shift Key를 Press한 상태에서 Item을 클릭하여 추가 Item을 선택한다.
  + Shift Key를 Release한 상태에서 다른 Item을 선택하거나 Item 이외의 곳을 클릭하면 Multi Selection이 해제된다.
* Multi Selection 상태에서 편집 가능 항목은 다음과 같다.
  + Move
  + Resize
  + Delete
  + Copy
  + Paste
* Multi Select 상태에서는 Context Menu에서 사용 가능한 항목(Delete, Copy, Paste)만 표시된다.
* v5.1에서는 Multi 선택 Item에 대한 Property 편집 기능은 지원하지 않는다.

## Captured Image List

* 진단 Tab에서 사용자가 Capture한 Image의 Thumbnail을 보여준다.
  + 동작방식은 E3 v5.0과 동일하다.

## Template Master

### Template Master 기능 실행/종료

* Report Dialog의 Control Panel에서 Template Master Button을 Click하면 Template Master Mode가 실행된다.
  + 작성 중인 Report가 있을 경우 저장 여부를 사용자에게 확인한다.
  + Control Panel와 Toolbar, Workspace가 Template Master Mode로 변경된다.
    - Toolbar, Control Panel
      * MMI, 별도 문서(e3\_v5.1\_RCReport\_UIState.xlsx) 참고
    - Workspace
      * Report Item Box는 Template Mode로 표시된다.
        + Item Box의 종류 및 속성이 Watermark로 표시된다.
  + Captured Image List가 Hide된다.
  + Default Template이 선택 상태로 표시된다.
* Template Master Mode 실행 중에 Control Panel의 Close Master Mode Button을 클릭하면,
  + Template Master Mode 종료 여부를 사용자에게 확인하고, 사용자가 OK를 선택시 Master Mode가 종료된다.
  + 저장되지 않은 Template 변경 정보가 있는 경우 Template 저장 여부를 사용자에게 확인하여 저장을 수행한다.
* Master Mode가 종료된 후 Default Template로 신규 Report가 생성된다.

### Template List

* Template Master가 실행되면 Template Master 실행 시점에 DB에 기록되어 있는 Template의 List를 조회하여 List를 생성하여 보여준다.
* Template List가 보여주는 정보는 다음과 같다.
  + Template Name
  + Template Show/Hide 설정 상태
    - Show/Hide 설정은 Change Template Dialog에서의 Template 표시 여부를 결정한다.
    - Show/Hide 설정 정보는 DB에 저장된다.
  + Default Template
    - Default Template 설정 정보는 DB에 저장된다.
    - Default Template으로 지정된 Template은 삭제할 수 없다.

### Template 생성/관리

#### Add Template

* Blank Template을 생성하여 편집을 시작한다.
* Add Template Button을 Click하면 Template Name, 용지 크기, 방향을 지정하는 Dialog가 팝업된다.
  + Dialog에서 표시하는 용지 크기 및 방향 Default 값은 Setting 값을 사용한다.
  + Dialog에서 표시하는 Template Name의 Default 값은 “User Template\_[Number]”로 부여된다.
* 사용자가 Template Name, 용지 크기, 방향을 선택하고 OK를 Click하면, Blank Template이 생성되어 Template 편집 화면에 표시되고, Template List에 추가된다.
  + 추가한 Template은 List에서 선택 상태로 표시되고, Edit Button이 자동으로 Check되어 편집 모드가 시작된다.

#### Copy & Add Template

* 이미 존재하는 Template을 복사하여 편집을 시작한다.
* Add Template Button을 Click하면 Template Name, 용지 크기, 방향을 지정하는 Dialog가 팝업된다.
  + Dialog에서 표시하는 용지 크기 및 방향을 변경하는 UI는 Disable 상태로 제공되며, 값은 복사한 Template과 동일하게 부여된다.
  + Dialog에서 표시하는 Template Name의 Default 값은 “[복사 대상 Template Name]\_[Number]”로 부여된다.
* 사용자가 Template Name을 지정하고 OK를 Click하면, 복사 대상 Template을 복사한 Template이 생성되어 Template 편집 화면에 표시되고, Template List에 추가된다.
  + Edit Button은 자동으로 Check되어 편집 모드가 시작된다.

#### Save Template

* Template Editing 중에 Template 저장이 필요한 상황이 발생하면 저장 확인 Message를 보여준다.
  + Template 저장이 필요한 조작
    - Change Template
    - Add Template
    - Click [Save] Button
    - Close Master Mode
  + Template이 편집되었음을 판정하는 기준
    - Paper Property가 변경됨
    - Header, Footer 위치나 속성이 변경됨
    - Item Box가 추가되거나 위치, 크기, 속성이 변경됨

#### Delete Template

* Template의 Context Menu를 통해 Template를 삭제할 수 있다.
* Template 삭제는 Server/Client 구별없이 가능하다.
* Template을 삭제하면 DB 및 File Server에서도 Template 정보가 삭제된다.
* Default Template은 삭제할 수 없다.

#### Rename Template

* Template의 Context Menu를 통해 Template Name을 변경할 수 있다.
* Template Name 변경은 Server/Client 구별없이 가능하다.
* 변경된 Template Name은 DB에 저장되어 공유된다.
* Template Name은 중복될 수 없으며, 중복시 사용자에게 Message Dialog로 안내하고 Name이 변경되지 않는다.

#### Show/Hide Template

* Template의 Checkbox를 통해 Template의 Show/Hide 설정을 변경할 수 있다.
* Template Show/Hide 설정은 DB에 저장된다.

### Edit Template

* Edit Report와 동일한 요령으로 Template를 편집할 수 있다.
  + Page를 생성하고 Image Box 및 Text Box를 추가, 위치 및 크기를 결정하고 속성을 설정한다.
  + Header, Footer를 편집할 수 있다.
  + Paper Property를 설정할 수 있다.
* Template 편집 중에 마지막 1페이지를 삭제하는 경우, Blank Page를 생성하여 페이지를 추가한다.

## Viewing

### Zoom

#### Manual Zoom

* v5.0과 동일한 Mouse 조작을 통한 Zoom 기능을 제공한다.

#### Page Fit

* v5.0과 동일한 Vertical, Horizontal Page Fit 기능을 제공한다.

### Grid

* v5.0과 동일한 Grid 표시 기능 및 Item Box의 Grid Snap 기능을 제공한다.

## Print

### Print

* v5.0과 동일한 일반 Print 기능을 제공한다.
* Print 실행 UI의 위치가 Toolbar에서 Control Panel로 변경된다.

### DICOM Print

* v5.0과 동일한 DICOM Print 기능을 제공한다.
* Print 실행 UI의 위치가 Toolbar에서 Control Panel로 변경된다.

## Export

### Export PDF

* v5.0과 동일한 Export PDF 기능을 제공한다.

### Send E-mail

* v5.0과 동일한, PDF Format으로 Export한 Report와 Report에 포함되는 Image File을 첨부하여 E-mail로 전송하는 기능을 제공한다.
* Image File은 File Server에 저장되는 것과 동일한 Format으로 첨부한다.
  + 진단 Tab에서 기존 Capture 기능으로 Capture한 영상을 삽입한 경우에는 dcm 포맷으로 첨부한다.
  + Auto Fill 및 Capture & Fill Image기능을 통해 삽입한 영상은 PNG 포맷으로 첨부한다.

# Change Management process **(**변경관리 프로세스**)**

* 변경관리 프로세스에 따라 SRS의 변경을 요청한다.
  + SRS의 변경 사항이 발생하면, VTS의 제품 프로젝트(E3: EEEN)에 변경 요청을 등록한다.
    (Assignee: Project Manager, Issue Type: Change Request)
  + PM은 변경 내용을 확인하고, 승인에 필요한 CCB를 구성하여 Stakeholder에 추가한다.
    (CCB: Change Control Board, 변경관리 위원회)
  + 모든 CCB 멤버의 승인 의견에 따라 변경 또는 기각 처리를 한다.

# Document Approvals **(**최종 승인자**)**

Identify the approvers of the SRS document. Approver name, signature, and date should be used.

Name Signature Date

# Reference Materials (참고문헌)

모든 문서는 소스코드 관리 시스템의 파일 위치로 기재한다.

# Appendix (부록)

## Glossary (용어)