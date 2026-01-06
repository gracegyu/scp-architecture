**E3 - Report**

**Software Requirements Specification**

**Version : 4.3**

**Date : 2016.09.07**

**Writer : 천민경**

**EWOOSOFT Co., Ltd.**

|  |
| --- |
|  |

문서정보 / 수정 내역

|  |  |
| --- | --- |
| 파일명: | e3\_report\_srs.doc |
| 템플릿 버전: | v3.2 |
| 원안작성자 : | 김가영 |
| 수정작업자 : | 천민경 |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 수정날짜 | 수정자 | 버전 | 추가/수정 항목 | 내 용 |
| 2014-07-21 | 김가영 |  | 최초 작성 | 이전 version에 제공된, Report 기능을 토대로 작성 시작. |
| 2014-08-05 | 천민경 |  | Ch1, 2, 3 | 1, 2, 3장 Draft 작성 |
| 2014-08-06 | 천민경 |  | Ch4, 5, 6 | 1, 2, 3장 Draft 작성 |
| 2014-09-16 | 이태선 |  | Ch4 | UIM -> CTR 인터페이스 삭제 |
| 2014-10-21 | 천민경 |  | Ch4 | 약어를 Global Unique하게 수정 |
| 2014-11-8 | 천민경 |  | 전체 | MRD, MMI를 바탕으로 Header/Footer Setting 저장 기능과 Item Box의 Auto Resize 기능 변경 관련 내용 추가 |
| 2014-11-18 | 천민경 |  | 전체 | 1, 2, 7장 Item Box의 Snap 및 Grid 기능 관련내용 추가, 4장 DICOM Print와 Send Email관련 구조체 추가 및 인터페이스 변경 |
| 2014-11-24 | 천민경 |  | 전체 | TBD 내용 반영 및 수정 |
| 2014-1-19 | 이태선 |  | 6.4, 7.1.3 | Report file format 수정, HeaderFooter 설정 파일 위치 명시 |
| 2014-1-20 | 이태선 |  | 1.2, 2.8 | 하위호환성 지원에 관한 정책 변경 |
| 2014-1-20 | 이태선 |  | 6.4 | Report file format 수정 |
| 2015-4-28 | 박윤희 |  | 6.4 | Report file format 수정. (ZoomRate->Scale) |
| 2015-5-15 | 박윤희 |  | 6.4 | File format 수정. (Report/Template 파일포맷 및 샘플 내용 통일 |
| 2015-09-16 | 이태선 |  | Ch4 | 구현 후 인터페이스 수정 |
| 2015-10-13 | 천민경 |  | 전체 | E3 v4.0 FCS3 기준으로 전체 내용 수정 |
| 2017-04-27 | 박진희 | V5.0 | 전체 | 링크 수정 |

목 차

[1 Introduction (개요) 6](#_Toc455145868)

[1.1 Purpose (목표) 6](#_Toc455145869)

[1.2 Product Scope (범위) 6](#_Toc455145870)

[1.3 Document Conventions (문서규칙) 6](#_Toc455145871)

[1.4 Terms and Abbreviations (정의 및 약어) 7](#_Toc455145872)

[1.5 Related Documents (관련문서) 7](#_Toc455145873)

[1.6 Intended Audience and Reading Suggestions (대상 및 읽는 방법) 7](#_Toc455145874)

[1.7 Project Output (프로젝트 산출물) 7](#_Toc455145875)

[1.7.1 Output Format (산출물 형태) 7](#_Toc455145876)

[1.7.2 Output Name and Version (산출물명(가칭) 및 버전) 7](#_Toc455145877)

[1.7.3 Patent Information (특허 출원 유무 및 내용) 7](#_Toc455145878)

[2 Overall Description (전체 설명) 8](#_Toc455145879)

[2.1 Product Perspective (제품 조망) 8](#_Toc455145880)

[2.2 Overall System Configuration (전체 시스템 구성) 8](#_Toc455145881)

[2.3 Overall Operation (전체 동작방식) 8](#_Toc455145882)

[2.4 Product Functions (제품 주요 기능) 10](#_Toc455145883)

[2.5 User Classes and Characteristics (사용자 계층과 특징) 10](#_Toc455145884)

[2.6 Assumptions and Dependencies (가정과 종속 관계) 10](#_Toc455145885)

[2.7 Apportioning of Requirements (단계별 요구사항) 10](#_Toc455145886)

[2.8 Backward compatibility (하위 호환성) 11](#_Toc455145887)

[3 Environment (환경) 12](#_Toc455145888)

[4 External Interface Requirements (외부 인터페이스 요구사항) 13](#_Toc455145889)

[**4.1** System Interfaces **(**시스템 인터페이스**)** 13](#_Toc455145890)

[4.1.1 정의 및 약어 13](#_Toc455145891)

[4.1.2 컴포넌트 정의 13](#_Toc455145892)

[4.1.3 자료구조 13](#_Toc455145893)

[4.1.4 인터페이스 정의 13](#_Toc455145894)

[4.2 User Interface **(**사용자 인터페이스) 13](#_Toc455145895)

[4.3 Hardware Interface (하드웨어 인터페이스**)** 13](#_Toc455145896)

[4.4 Software Interface **(**소프트웨어 인터페이스) 13](#_Toc455145897)

[4.5 Communication Interface **(**통신 인터페이스**)** 14](#_Toc455145898)

[**4.6** Other Interface (기타 인터페이스**)** 14](#_Toc455145899)

[5 Performance requirements (성능 요구사항) 15](#_Toc455145900)

[5.1 Throughput (작업처리량) 15](#_Toc455145901)

[5.2 Concurrent Session (동시 세션) 15](#_Toc455145902)

[5.3 Response Time (대응시간) 15](#_Toc455145903)

[5.4 Performance Dependency (성능 종속 관계) 15](#_Toc455145904)

[5.5 Other Performance Requirements (기타 성능 요구사항**)** 15](#_Toc455145905)

[6 Non-Functional Requirements (기능 이외의 요구사항) 16](#_Toc455145906)

[6.1 Safety requirements (안전성 요구사항) 16](#_Toc455145907)

[**6.2** Security Requirements (보안 요구사항**)** 16](#_Toc455145908)

[6.3 Software System Attributes (소프트웨어 시스템 특성) 16](#_Toc455145909)

[6.4 Logical Database Requirements (데이터베이스 요구사항) 16](#_Toc455145910)

[6.5 Business Rules (비즈니스 규칙) 22](#_Toc455145911)

[6.6 Design and Implementation Constraints (설계와 구현 제한사항) 22](#_Toc455145912)

[6.6.1 Standards Compliance (표준준수) 22](#_Toc455145913)

[6.6.2 Other Constraints (기타 제한 사항) 22](#_Toc455145914)

[6.7 Memory Constraints (메모리 제한 사항) 22](#_Toc455145915)

[6.8 Operations (운영 요구사항**)** 22](#_Toc455145916)

[6.9 Site Adaptation Requirements **(**사이트 적용 요구사항**)** 22](#_Toc455145917)

[6.10 Internationalization Requirements (다국어 지원 요구사항) 22](#_Toc455145918)

[6.11 Unicode Support (유니코드 지원) 22](#_Toc455145919)

[6.12 64bit Support (64비트 지원) 22](#_Toc455145920)

[6.13 Certification **(**제품 인증) 23](#_Toc455145921)

[6.14 Field Test (필드 테스트) 23](#_Toc455145922)

[6.15 Other Requirements (기타 요구 사항) 23](#_Toc455145923)

[7 Functional Requirements (기능요구사항) 24](#_Toc455145924)

[8 Change Management process (변경관리 프로세스) 25](#_Toc455145925)

[9 Document Approvals (최종 승인자) 26](#_Toc455145926)

[10 Reference Materials (참고문헌) 27](#_Toc455145927)

[11 Appendix (부록) 28](#_Toc455145928)

[11.1 Glossary (용어) 28](#_Toc455145929)

# Introduction **(개요)**

## Purpose (목표)

* 이 문서는 이우소프트 내부에서 E3에 대해 아는 개발자들이 E3의 모듈인 Report를 설계, 구현하기 위해 작성하는 문서이다.
  + E3 v1에 대해 전혀 모르는 개발자들을 위한 문서는 아니다.
  + 이우소프트의 2D Viewer Program인 E2의 재건축 작업 시 공통으로 사용할 것을 고려하여 개발한다.

## Product Scope (범위)

* Report는 Report 작성, 관리, Export 기능을 담당하는 모듈이다.
* 기존 제품(E3 v1)에 대한 주요 추가 및 변경 기능은 다음과 같다.
  + Snap, Grid 기능을 지원한다.
  + Image Box에 Real Size로 삽입된 Image의 위치와 크기를 변경할 수 있다.
  + Report가 편집된 상태에서는 용지 사이즈나 방향을 변경해도 Item Box가 Auto Resize 되지 않는다.
  + Header와 Footer에 포함될 항목과 위치 및 크기, 속성을 사용자가 설정할 수 있고, 설정한 내용은 Local에 자동으로 저장된다.
  + E-mail에 Multi Capture Image를 첨부할 수 있다.
  + Report에 삽입된 Image Data를 Report File 내부에 포함시켜 저장하지 않고 저장 경로와 파일명을 저장한다.
    - 저장 방식을 변경하는 이유는 다음과 같다.
      * 저장 방식을 E2와 통일화한다.
      * Single Capture Image와 Multi Capture Image의 저장방식을 통일화한다.
      * Report File 사이즈의 비대화를 방지한다.
      * 서버로 연결되지 않은 환경에서 Report를 확인하는 용도로는 Export 기능을 제공하고 있다.
* E3 하위 버전(v1.1.5 이하) 이 생성한 report file의 migration 지원 정책은 다음과 같다.
  + E3 v1.0.5 이하 버전이 생성한 report file에 대해서는 migration을 지원하지 않는다.(EEEN-1589 참고)
  + E3 v1.1.4 이하 버전이 생성한 report file은 v1.1.5로 migration한 후 다시 v4.0으로 migration한다.
  + 하위 버전에서는 Single Capture Image인 경우 Image Data를 내부에 포함하여 저장한다. 저장 경로와 파일명만을 저장하는 현재의 정책에 위배되기는 하나, 포함된 이미지를 파일명으로 치환하여 migration하기는 어려우므로 예외적으로 지원하기로 한다. 또한 같은 이유로 이러한 파일을 편집 후 저장하는 경우에도 Image Data를 Report File 내부에 저장하는 방식을 유지 한다.

## Document Conventions (문서규칙)

* E3 SRS와 동일하다.

([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Terms and Abbreviations (정의 및 약어)

* E3 SRS와 동일하다.

([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Related Documents (관련문서)

* E3 SRS와 동일하다.

([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Intended Audience and Reading Suggestions (대상 및 읽는 방법)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Project Output (프로젝트 산출물)

### Output Format (산출물 형태)

* 소스 코드로 제공한다.

### Output Name and Version (산출물명(가칭) 및 버전)

* 컴파일 하면 다음과 같이 생성된다.
  + VTPluginReport64.dll (64bit)

### Patent Information (특허 출원 유무 및 내용)

* 특허 출원할 내용이 없다.

# Overall Description (전체 설명)

## Product Perspective (제품 조망)

![](data:image/png;base64...)

* Report – Report 작성, 관리, Export를 위한 화면 및 기능을 담당하는 모듈
* Controller – E3에서 각 모듈들의 실행 제어 및 환경 설정을 주 목적으로 하는 모듈

## Overall System Configuration (전체 시스템 구성)

* 4.1.2 컴포넌트 정의와 동일하다.

## Overall Operation (전체 동작방식)

* 이 제품에서 FileDeliverer를 이용하기 위해서는 반드시 Utility의 DirectoryManager를 이용하여 File Server의 경로를 가져와야 한다. FileDeliverer 사용시 Utility의 DirectoryManager는 항상 호출되어야 하는 것으로, 이하 동작방식에는 Utility의 DirectoryManager는 언급하지 않는다.
* **사용자가 Report 저장을 요청한 경우,**
  + ReportUIManager는 ReportViewManager에 Report의 첫 번째 페이지를 요청한다.
  + ReportUIManager는 Report의 첫 번째 페이지를 렌더링하여 Preview Image로 임시 폴더에 저장한다.
  + ReportUIManager는 Save Report Dialog를 표시하여 Report Preview Image를 보여주고, 사용자에게 Report Title과 Comment를 입력 받는다.
  + ReportUIManager는 ReportIOManager에 Report Data, Page Setting, 환자 차트번호, Report File 정보를 전달하여 저장할 것을 요청한다.
  + ReportIOManager는 Report Data를 Serializing하여 임시 폴더에 저장한다.
  + ReportIOManager는 FileDeliverer에 Report File과 Report Preview 썸네일 File을 File Server에 저장할 것을 요청한다.
  + ReportIOManager는 DBManager에 Report File 정보를 저장할 것을 요청한다.
* **사용자가 Report List를 보여줄 것을 요청한 경우,**
  + ReportUIManager는 환자 차트번호를 ReportIOManager에게 전달하여 해당 환자의 Report File List를 요청한다.
  + ReportUIManager는 전달받은 Report File 정보로 Open Report Dialog를 구성하여 표시한다.
* **사용자가 Report File을 불러오기를 요청한 경우,**
  + ReportUIManager는 Report의 파일명을 ReportIOManager에게 전달하여 불러올 것을 요청한다.
  + ReportIOManager는 FileDeliverer에게서 Report File을 전달받아 Report Data를 Parsing하여 ReportUIManager에 전달한다.
  + ReportUIManager는 Report Data를 ReportViewManager에 전달하여 Report Page를 구성할 것을 요청한다.
* **사용자가 Report File 삭제를 요청한 경우,**
  + ReportUIManager는 환자 차트번호와 Report 파일명을 ReportIOManager에게 전달하여 삭제할 것을 요청한다.
  + ReportIOManager는 환자 차트번호와 Report 파일명을 DBManager에 전달하여 Report File 정보를 DB에서 삭제할 것을 요청한다.
  + ReportIOManager는 Report의 파일명을 FileDeliverer에 전달하여 해당 Report File과 썸네일 Image를 삭제할 것을 요청한다.
* **사용자가 Template List를 보여줄 것을 요청한 경우,**
  + ReportUIManager는 ReportUIManager는 ReportIOManager에 Template List를 요청한다.
  + ReportUIManager는 전달받은 Template List로 Change Template Dialog를 구성하여 표시한다.
* **사용자가 Template 변경을 요청한 경우,**
  + ReportUIManager는 사용자가 선택한 Template의 파일명을 ReportIOManager에 전달한다.
  + ReportIOManager는 Template Data를 Parsing해서 ReportUIManager에게 전달한다.
  + ReportUIManager는 Template Data를 ReportViewManager에 전달하여 Report Page를 구성할 것을 요청한다.
* **사용자가 일반 Page Print를 요청한 경우,**
  + ReportUIManager는 ReportViewManager에서 Report 데이터를 전달받아 ExportReport에 전달하여 Print할 것을 요청한다.
  + ExportReport는 해당 시스템의 Print Dialog를 보여주고 사용자에게 Print 설정을 입력받는다.
  + ExportReport는 Report 데이터를 렌더링하여 Print를 진행한다.
* **사용자가 DICOM Print를 요청한 경우,**
  + ReportUIManager는 ReportViewManager에게 Report 데이터를 요청한다.
  + ReportUIManager는 Report 데이터와 DICOM Print 설정을 ExportReport에 전달하여 Print할 것을 요청한다.
  + ExportReport는 DICOM Printer의 설정 Dialog를 보여주고, 사용자에게 DICOM Print 설정을 입력받는다.
  + ExportReport는 Report 데이터를 렌더링하여 dcm 파일로 저장하고, 파일명을 VTDicomWrapper에 전달해서 Print를 진행한다.
* **사용자가 Export PDF를 요청한 경우,**
  + ReportUIManager는 ReportViewManager에게 Report 데이터를 요청한다.
  + ReportUIManager는 ReportViewManager에서 전달받은 Report 데이터와 사용자가 지정한 저장 경로 및 파일명을 ExportReport에 전달하여 PDF 파일로 저장할 것을 요청한다.
  + ExportReport는 Report 데이터를 렌더링하여 PDF파일로 변환해서 사용자가 지정한 파일명으로 저장한다.
* **사용자가 Send Email을 요청한 경우,**
  + ReportUIManager는 ReportViewManager에게 Report 데이터를 요청한다.
  + ReportUIManager는 ExportReport에 Report 데이터를 전달하여 PDF로 저장할 것을 요청한다.
  + ExportReport는 Report 데이터를 PDF파일로 변환해서 임시 폴더에 저장한다.
  + ReportUIManager는 ExportReport에 Report 데이터를 전달하여 Report에 삽입된 영상을 임시 폴더에 저장할 것을 요청한다.
  + ExportReport는 Report에 삽입된 영상을 png파일로 변환하여 임시 폴더에 저장한다.
  + ReportUIManager는 PDF파일명과 삽입된 Capture 영상 파일명의 List, 그 외 메일 전송에 필요한 정보를 바탕으로 EMail Dialog를 생성하여 사용자에게 보여주고, 수신자 정보와 제목, 본문 내용을 입력받는다.
  + 사용자가 Email 내용을 입력하고 전송을 요청하면 메일을 전송한다.

## Product Functions (제품 주요 기능)

* Report 편집
* Layout Template
* Report Viewer 기능
* Report File 저장/불러오기/삭제
* Export Report 기능
  + 일반 Print, DICOM Print
  + PDF 파일 변환 및 저장
  + E-mail 전송

## User Classes and Characteristics (사용자 계층과 특징)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Assumptions and Dependencies (가정과 종속 관계)

* 해당 사항 없음

## Apportioning of Requirements (단계별 요구사항)

* 해당 사항 없음

## Backward compatibility (하위 호환성)

* 하위 버전에서 생성한 파일은 지원하지 않는다.
  + 하위 버전에 의해 생성된 파일은 Migration 과정을 먼저 거쳐야 한다.

# Environment (환경)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

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

* e3\_diagrams.pptx "Report" diagram을 참고한다.

### 자료구조

### 인터페이스 정의

* 구현이 완료된 내용에 대한 자료구조 및 인터페이스 리스트는 별도로 관리하지 않는다.
  + v4.0 구현 전에 도출되어 있던 인터페이스는 [e3\_interface.xlsx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/v5.0/SRS/e3_interface_v5.0.xlsx) 문서를 참고한다.

## User Interface **(**사용자 인터페이스)

* E3 v4.0 MMI를 참고한다.

## Hardware Interface (하드웨어 인터페이스**)**

* 해당 없음

## Software Interface **(**소프트웨어 인터페이스)

* 해당 없음

## Communication Interface **(**통신 인터페이스**)**

* 해당 없음

## Other Interface (기타 인터페이스**)**

* 해당 없음.

# Performance requirements (성능 요구사항**)**

## Throughput (작업처리량)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Concurrent Session (동시 세션)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Response Time (대응시간)

* 다음 대응 시간은 E3 v1과 동등한 수준이어야 한다.
  + Report Tab이 클릭되었을 때 화면을 구성하고 Display 하는 데까지의 시간
  + Report File을 불러와서 Display하는 데까지의 시간
  + Template를 변경했을 때 반영되는 시간

## Performance Dependency (성능 종속 관계)

* File Server와 연결된 네트워크 속도에 따라 Report Tab 기동, Report 화면 구성, Capture Image List 생성, File Open, Template File Open 등의 속도가 결정된다.
* E-mail에 첨부하는 파일 크기와 네트워크 속도에 따라 E-mail 전송시간이 결정된다.
* Printer와의 통신 속도와 Printer 성능에 따라 인쇄 속도가 결정된다.

## Other Performance Requirements (기타 성능 요구사항**)**

* E3 SRS와 동일하다
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

# Non-Functional Requirements (기능 이외의 요구사항**)**

## Safety requirements (안전성 요구사항)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Security Requirements (보안 요구사항**)**

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Software System Attributes (소프트웨어 시스템 특성)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Logical Database Requirements (데이터베이스 요구사항)

* Report에서 사용하는 Setting 정보는 E3 Controller SRS를 참고한다.
* Log파일
  + E3\_SRS를 참고한다.
    ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))
* Report File Format
  + PageSetting이 설정되지 않은 경우는 Setting의 paper setting 정보를 사용한다.

<?xml version = '1.0' encoding = 'utf-8'>

<Report VERSION="4.0" ARCHIVETYPE="Report">

<!-- Page Setting -->

<Paper>

<PaperSize>...</ PaperSize >

<Orientation>...</Orientation>

<Margin>

<Top>...</Top>

<Bottom>...</Bottom>

<Left>...</Left>

<Right>...</Right>

</Margin>

</Paper>

<Page Number = "">

<!-- ItemBox Setting and Data -->

<ItemBox>

<BoxID>...</BoxID>

<BoxType>...</BoxType>

<Editable>...</Editable>

<BoxPosition>

<X>...</X>

<Y>...</Y>

</BoxPosition>

<BoxSize>

<BoxWidth>...</BoxWidth>

<BoxHeight>...</BoxHeight>

</BoxSize>

<BackgroundColor>...</BackgroundColor>

<BackgroundOpacity>...</BackgroundOpacity>

<BorderLine>

<LineColor>...</LineColor>

<LineOpacity>...</LineOpacity>

<LineWidth>...</LineWidth>

<LineType>...</LineType>

</BorderLine>

<!-- TextBox Setting and Data -->

<Text>

<Font>

<FontFamily>...</FontFamily>

<FontColor>...</FontColor>

<FontSize>...</FontSize>

</Font>

<TextAlignment>...</TextAlignment>

<TextData>...</TextData>

<TextMacro>...</TextMacro>

</Text>

<!-- ImageBox Setting and Data -->

<Image>

<ImageFitMode>...</ImageFitMode>

<ImageCount>...</ImageCount>

<Layout>

<Row>...</Row>

<Column>...</Column>

</Layout>

<Translation>

<TransX>...</TransX>

<TransY>...</TransY>

</Translation>

<Scale>

<ScaleX>...</ ScaleX >

<ScaleY>...</ ScaleY >

</Scale>

<ShowRuler>...</ShowRuler>

<Invert>...</Invert>

<ImageFilename>...</ImageFilename>

<ImageData>...</ImageData>

<ImageMacro>...</ImageMacro>

</Image>

</ItemBox>

</Page>

</Report>

TBD – Position 및 크기 정보가 용지 크기에 대한 비율로 그 값이 결정될 때 margin을 제외한 영역을 대상으로 하는지, margin 영역은 고려하지 않는지에 대해 확인이 필요하다.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Parent** | **Name** | **Description** | **Format** | **Possible** | **Default** |
| **Report** | VERSION | Report Page 버전 |  |  | "4.0" |
| ARCHIVETYPE | 저장타입 |  | Report  Template  HeaderFooter |  |
| **Paper** | Report 용지의 속성 |  |  |  |
| **Page** | Report Page의 속성과 편집내용 |  |  |  |
| Report/**Paper** | PaperSize | 용지 사이즈 |  | 제품에서 지원하는 용지 사이즈 A3|A4|8x10Inch… |  |
| Orientation | 용지 방향 |  | Portrait Landscape |  |
| **Margin** | 여백 |  |  |  |
| Report/**Page** | Number | 페이지 번호 | 1 이상의 integer | Template과 headerfooter는 0 |  |
| **ItemBox** | Item Box의 속성과 편집내용 |  |  |  |
| Page/**Margin** | Left | 페이지 좌단 여백 | mm단위 실수(#.##) |  |  |
| Right | 페이지 우단 여백 | mm단위 실수(#.##) |  |  |
| Top | 페이지 상단 여백 | mm단위 실수(#.##) |  |  |
| Bottom | 페이지 하단 여백 | mm단위 실수(#.##) |  |  |
| Page/**ItemBox** | BoxID | BoxID. 생성 순서대로 부여된다. |  |  |  |
| BoxType | 박스 유형 |  | Text  Image |  |
| Editable | 편집 가능 여부 (Header, Footer 등 사용자가 편집할 수 없는 Item Box를 구별하기 위함) |  | false = 편집불가능 true = 편집가능 |  |
| **BoxPosition** | 박스 위치 |  |  |  |
| **BoxSize** | 박스 크기 |  |  |  |
| BackgroundColor | 배경색 | 16진수 RGB  (#RRGGBB) |  |  |
| BackgroundOpacity | 배경투명도 | 0~1 범위 실수(#.##) |  |  |
| **BorderLine** | 테두리선 속성 |  |  |  |
| **Text** | Text Box의 속성과 편집내용 |  |  |  |
| **Image** | Image Box의 속성과 편집내용 |  |  |  |
| ItemBox/**BoxPosition** | X | Item Box의 왼쪽 위방향 꼭지점의 X좌표 | 0~1 범위 실수(#.###) | 용지의 가로 길이에 대한 비율값.  Margin은 영향 X, 용지 방향 영향 O. |  |
| Y | Item Box의 왼쪽 위방향 꼭지점의 Y좌표 | 0~1 범위 실수(#.###) | 용지의 세로 길이에 대한 비율값.  Margin은 영향 X, 용지 방향 영향 O. |  |
| ItemBox/**BoxSize** | BoxWidth | Item Box의 너비 | 0~1 범위 실수(#.###) | 용지의 가로 길이에 대한 비율값.  Margin은 영향 X, 용지 방향 영향 O. |  |
| BoxHeight | Item Box의 높이 | 0~1 범위 실수(#.###) | 용지의 세로 길이에 대한 비율값.  Margin은 영향 X, 용지 방향 영향 O. |  |
| ItemBox/**BorderLine** | LineColor | 테두리선의 색 | 16진수 RGB  (#RRGGBB) | 16진수 RGB |  |
| LineOpacity | 테두리선의 투명도 | 0~1 범위 실수(#.##) |  |  |
| LineWidth | 테두리선의 굵기 |  |  |  |
| LineType | 테두리선의 모양 |  | SolidLine  DashLine  DotLine |  |
| ItemBox/**Text** | **Font** | 폰트 속성 |  |  |  |
| TextAlignment | 텍스트 맞춤 |  | Left Center Right |  |
| TextData | 사용자가 입력한 Comment | Plain Text |  |  |
| TextMacro | 사용자 편집값이 아닌 Setting 정보로 구성되는 Text Data |  | PatientInfo ReportDate ClinicLogo ClinicName PhoneNumber Address WebSite |  |
| ItemBox/**Image** | ImageFitMode | Image Fit Mode |  | RealSize BoxFit Modified | RealSize |
| ImageCount | 삽입되어있는 Image 개수 |  |  |  |
| **Layout** | Multi Image 배치 |  |  |  |
| **Translation** | Image Panning 이동값 |  |  |  |
| **Scale** | Image Zooming 배율 | 0보다 큰 실수(#.##) | 원본 크기에 대한 비율값 |  |
| ShowRuler | Ruler 표시 여부 |  | false = 비표시 true = 표시 |  |
| Invert | 색상 반전 여부 |  | false = 반전없음 true = 색상반전 | false |
| ImageFilename | 삽입된 Image의 File Server상의 경로와 파일명  첫 번째는 path, 그 이후부터는 파일명들이 “,”을 seperator로 리스트 된다.  ex)20140611\_120651,10.dcm,11.dcm,12.dcm,13.dcm |  |  |  |
| ImageData | Base64로 인코딩된 Image Data. v1에서 저장된 Report File에 삽입된 Image를 저장할 때 사용한다. |  |  |  |
| ImageMacro | 사용자 편집값이 아닌 Setting 정보로 구성되는 Image Data |  | ClinicLogo |  |
| ImageData | type | Image Data의 파일 포멧 |  |  | “dcm” |
| Text/**Font** | FontFamily | 폰트 종류 |  |  |  |
| FontColor | 폰트 색 | 16진수 RGB  (#RRGGBB) |  |  |
| FontSize | 폰트 크기 |  |  |  |
| Image/**Layout** | Row | 가로 배치 개수 |  |  |  |
| Column | 세로 배치 개수 |  |  |  |
| Image/**Translation** | TransX | Image 중심 좌표의 x방향 이동량 | 부호있는 실수(-#.###) | Box Size에 대한 비율값 |  |
| TransY | Image 중심 좌표의 y방향 이동량 | 부호있는 실수(-#.###) | Box Size에 대한 비율값 |  |
| Image/**Scale** | ScaleX | Image중심 기준의 x방향 확대율 | 0보다 큰 실수(#.##) | 원본 크기에 대한 비율값 |  |
| ScaleY | Image중심 기준의 y방향 확대율 | 0보다 큰 실수(#.##) | 원본 크기에 대한 비율값 |  |

* Report Template File Format
  + ARCHIVETYPE으로 ReportData와 Template를 구별한다.
  + 4.0에서 Layout Template는 용지 사이즈와 관련 없이 적용된다.
    - 용지 사이즈 정보가 있더라도 Template를 읽어들일 때 해당 정보를 무시하고 현재 Setting 정보에 맞춘다.

<?xml version = '1.0' encoding = 'utf-8'>

<Report VERSION="4.0" ARCHIVETYPE="Template">

<Page Number = "">

<!-- ItemBox Setting and Data -->

<ItemBox>

<BoxID>...</BoxID>

<BoxType>...</BoxType>

<Editable>...</Editable>

<BoxPosition>

<X>...</X>

<Y>...</Y>

</BoxPosition>

<BoxSize>

<BoxWidth>...</BoxWidth>

<BoxHeight>...</BoxHeight>

</BoxSize>

<BackgroundColor>...</BackgroundColor>

<BackgroundOpacity>...</BackgroundOpacity>

<BorderLine>

<LineColor>...</LineColor>

<LineOpacity>...</LineOpacity>

<LineWidth>...</LineWidth>

<LineType>...</LineType>

</BorderLine>

<!-- TextBox Setting and Data -->

<Text>

<Font>

<FontFamily>...</FontFamily>

<FontColor>...</FontColor>

<FontSize>...</FontSize>

</Font>

<TextAlignment>...</TextAlignment>

<TextData>...</TextData>

<TextMacro>...</TextMacro>

</Text>

<!-- ImageBox Setting and Data -->

<Image>

<ImageFitMode>...</ImageFitMode>

<ImageCount>...</ImageCount>

<Layout>

<Row>...</Row>

<Column>...</Column>

</Layout>

<Translation>

<TransX>...</TransX>

<TransY>...</TransY>

</Translation>

<Scale>

<ScaleX>...</ ScaleX >

<ScaleY>...</ ScaleY >

</Scale>

<ZoomRate>...</ZoomRate>

<ShowRuler>...</ShowRuler>

<Invert>...</Invert>

<ImageFilename>...</ImageFilename>

<ImageData>...</ImageData>

<ImageMacro>...</ImageMacro>

</Image>

</ItemBox>

</Page>

</Report>

* Header/Footer Setting File Format
  + Template File Format과 구조가 동일하다. ARCHIVETYPE은 HeaderFooter로 Template와 구별한다.
  + Header/Footer는 용지 사이즈별, 용지 방향별로 저장된다.

ex) HeaderFooter\_A4\_Landscape.xml, HeaderFooter\_14x14inch\_Portrait.xml, …

## Business Rules (비즈니스 규칙)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Design and Implementation Constraints (설계와 구현 제한사항)

### Standards Compliance (표준준수)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

### Other Constraints (기타 제한 사항)

* 이우소프트 코딩 컨벤션을 준수해야 한다.

## Memory Constraints (메모리 제한 사항)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Operations (운영 요구사항**)**

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Site Adaptation Requirements **(**사이트 적용 요구사항**)**

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Internationalization Requirements (다국어 지원 요구사항)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Unicode Support (유니코드 지원)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## 64bit Support (64비트 지원)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Certification **(**제품 인증)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Field Test (필드 테스트)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

## Other Requirements (기타 요구 사항)

* E3 SRS와 동일하다.
  ([https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Project/Ez3D-i\_v5.0/doc/srs/e3\_srs.docx](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Ez3D-i/srs/old/v5.0/e3_v5.0_srs.docx))

# Functional Requirements (기능요구사항)

* 구현이 완료된 기능에 대한 상세 내용은 생략한다. (실제 제품 및 제품 매뉴얼 참고)

# Change Management process **(**변경관리 프로세스**)**

* 변경 관리 프로세스가 결정될 때까지는 작성자의 승인을 받은 후 수정한다.

# Document Approvals **(**최종 승인자**)**

Identify the approvers of the SRS document. Approver name, signature, and date should be used.

Name Signature Date

# Reference Materials (참고문헌)

모든 문서는 소스코드 관리 시스템의 파일 위치로 기재한다.

# Appendix (부록)

## Glossary (용어)