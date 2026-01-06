**E2 - Report**

**Software Requirements Specification**

**Version : 3.0**

**Date : 2018-05-04**

**Writer : Ann (김가영)**

**EWOOSOFT Co., Ltd.**

|  |
| --- |
|  |

문서정보 / 수정 내역

|  |  |
| --- | --- |
| 파일명: | e2\_report\_v3.0\_srs.docx |
| 템플릿 버전: | V0.1 |
| 원안작성자 : | 신지혜 |
| 수정작업자 : |  |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 수정날짜 | 수정자 | 버전 | 추가/수정 항목 | 내 용 |
| 2012-08-17 | 신지혜 | V0.1 |  | 제품 조망, 전체시스템 구조 추가함. |
| 2012-08-20 | 신지혜 |  | Ch02 | 전체시나리오 |
| 2012-08-21 | 신지혜 |  | Ch07,ch04 | Ch7작성, 인터페이스 구조 추가. |
| 2012-08-23 | 신지혜 |  | Ch04 | 내 외부 인터페이스 작성 |
| 2012-08-24 | 신지혜 |  |  | 리뷰 내용 수정 |
| 2012-08-27 | 신지혜 |  |  | 시나리오 변경에 따른 수정 |
| 2012-08-28 | 신지혜 |  | Ch02,04 | 시나리오 변경에 따른 수정 |
| 2012-08-31 | 신지혜 |  |  | CTO리뷰사항 수정 |
| 2012-11-1 | 이태선 | RC-1 | 6.4 | Report Template 구조 추가 |
| 2012-11-1 | 이태선 | RC-1 | 6.4 | Report Template 구조 보완 |
| 2012-11-30 | 이태선 | RC-2 | 4.1.3 | 자료구조 변경 |
| 2012-12-11 | 이태선 | RC-2 | 6.4 | Report Template format 변경 (Width, Height 추가) |
| 2012-12-22 | 이태선 | RC-2 | 2, 4 | 시스템 구성도에 Utility 추가 |
| 2012-12-27 | 김가영 | RC-2 | 4 | Report 저장 방식 변경 |
| 2012-01-16 | 김가영 | R. Alpha1 | 7 | Show/Hide기능 수정 |
| 2012-01-17 | 김가영 | R. Alpha1 | 1 | 1.2수정 |
| 2012-01-22 | 김가영 | R. Alpha1 | 7 | Report 저장 |
| 2013-3-14 | 이태선 | R. Beta1 | 1.5 | FileDeliverer srs 위치 수정 |
| 2013-8-13 | 이태선 | H2 Alpha1 | 1.2 | Report 영상 편집 기능 내용 보완 |
| 2016-06-22 | 이경환 | V2.1 |  | 구현 후 version에 맞춰 전체 내용 Review & 수정 |
| 2016-6-17 | 이태선 |  |  | H2, i-PMS 삭제 |
| 2018-04-23 | 김가영 | V3.0 |  | V3.0 MRD 요구사항 반영 |

목 차

[1 Introduction (개요) 4](#_Toc512327975)

[1.1 Purpose (목표) 4](#_Toc512327976)

[1.2 Product Scope (범위) 4](#_Toc512327977)

[1.3 Document Conventions (문서규칙) 4](#_Toc512327978)

[1.4 Terms and Abbreviations (정의 및 약어) 5](#_Toc512327979)

[1.5 Related Documents (관련문서) 5](#_Toc512327980)

[1.6 Intended Audience and Reading Suggestions (대상 및 읽는 방법) 5](#_Toc512327981)

[1.7 Project Output (프로젝트 산출물) 5](#_Toc512327982)

[1.7.1 Output Format (산출물 형태) 5](#_Toc512327983)

[1.7.2 Output Name and Version (산출물명(가칭) 및 버전) 6](#_Toc512327984)

[1.7.3 Patent Information (특허 출원 유무 및 내용) 6](#_Toc512327985)

[2 Overall Description (전체 설명) 7](#_Toc512327986)

[2.1 Product Perspective (제품 조망) 7](#_Toc512327987)

[2.2 Overall System Configuration (전체 시스템 구성) 7](#_Toc512327988)

[2.3 Overall Operation (전체 동작방식) 7](#_Toc512327989)

[2.4 Product Functions (제품 주요 기능) 8](#_Toc512327990)

[2.5 User Classes and Characteristics (사용자 계층과 특징) 9](#_Toc512327991)

[2.6 Assumptions and Dependencies (가정과 종속 관계) 9](#_Toc512327992)

[2.7 Apportioning of Requirements (단계별 요구사항) 9](#_Toc512327993)

[2.8 Backward compatibility (하위 호환성) 9](#_Toc512327994)

[3 Environment (환경) 9](#_Toc512327995)

[4 External Interface Requirements (외부 인터페이스 요구사항) 10](#_Toc512327996)

[4.1 System Interfaces **(**시스템 인터페이스**)** 10](#_Toc512327997)

[4.2 User Interface **(**사용자 인터페이스) 10](#_Toc512327998)

[**4.3** Main Hardware Interface (하드웨어 인터페이스**)** 10](#_Toc512327999)

[4.4 Software Interface **(**소프트웨어 인터페이스) 10](#_Toc512328000)

[4.5 Communication Interface **(**통신 인터페이스**)** 10](#_Toc512328001)

[**4.6** Other Interface (기타 인터페이스**)** 10](#_Toc512328002)

[5 Performance requirements (성능 요구사항) 10](#_Toc512328003)

[6 Non-Functional Requirements (기능 이외의 요구사항) 10](#_Toc512328004)

[7 Functional Requirements (기능요구사항) 10](#_Toc512328005)

[8 Change Management process (변경관리 프로세스) 11](#_Toc512328006)

[9 Document Approvals (최종 승인자) 11](#_Toc512328007)

[10 Reference Materials (참고문헌) 12](#_Toc512328008)

[11 Appendix (부록) 12](#_Toc512328009)

[11.1 Glossary (용어) 12](#_Toc512328010)

# Introduction (개요)

## Purpose (목표)

* 이 문서는 내부에서 E2에 대해서 아는 개발자들이 E2의 모듈인 Report를 설계와 구현하기 위해 작성하는 문서이다.
  + E2를 전혀 모르는 개발자를 위한 문서는 아니다.

## Product Scope (범위)

* E2의 환자 Report를 작성하고 관리하는 기능을 담당한다.
* report에서 편집한 내용은 serializing하여 rpt 파일로 저장한다.
  + - 저장 경로는 사용자가 설정할 수 없다.
* Report의 Image Box에 보여지는 Image는 Viewer Tab에서 작업한 내용을 저장하는 Tag file을 적용하여 화면에 표시된다.
  + Report 저장 시점에 Image에 적용된 Tag File 정보를 Report File에 저장하여, Report를 다시 Open한 경우에도 저장시점의 Tag를 적용한다. (Server에 저장된 최신 영상 tag 정보를 적용하지 않는다.)
  + Image Processing (Brightness / Contrast)
  + Overlay (Measurement, Annotation, EzNAVI Overlay- **v3.0**)
  + Simulation (Implant, Canal 등)
  + Filter (Sharpen, Max Sharpen, Inverse, Film Effect) **(v3.0)**
    - Viewer Tab의 Inverse와 Report Tab의 Invert 기능은 독릭접으로 수행된다.
      * Viewer Tab에서 Inverse된 영상을 Report Tab에서 Open -> Report Tab에서 Invert 수행 시, Viewer Tab의 Inverse된 영상을 기준으로 Invert가 수행된다.
* Report탭을 선택하면 Default로 설정된 Template을 화면에 보여주어야 한다.
* Template Layout 구성 정보는 tpl파일로 관리된다.
  + 자세한 내용은 [E2-Layout(template)](https://vks.vatech.co.kr/display/ESDEVELOPER/E2%2B-%2BLayout) VKS를 참고한다.
* 사용자가 report 작성 중에 “ChangeTemplate” 을 하면 작성 중이던 Report의 내용은 모두 초기화 된다.
  + 사용자에게 저장 경고 메시지 창을 보여준다.
* 사용자가 report 편집을 하는 중에 환자를 변경하는 경우, Report화면은 초기화(clear)되어야 한다.
  + Report를 작성하다 Tab을 전환 시에는 작업된 부분은 유지하고, 환자 변경이 이루어지기 전까지 계속 입력 가능 하지만, 환자를 변경 할 시 기존 작성 Report는 저장 여부는 묻지 않고 삭제 처리한다.
* Print는 일반 페이지 프린트와 DICOM 프린트를 지원한다.
* Report File을 E-mail로 전송 가능하다.
  + E-mail 전송을 위해 chillkat library를 이용한다.
  + E-mail 기능에 첨부되는 File 명칭 변경이 가능하다. **(v3.0)**
    - 첨부 파일이 CT인 경우에는 Rename할 수 없다.
    - 확장자는 수정할 수 없다.

## Document Conventions (문서규칙)

* E2 SRS와 동일하다.

## Terms and Abbreviations (정의 및 약어)

* E2 SRS와 동일하다.

## Related Documents (관련문서)

* E2 SRS와 동일하다.

## Intended Audience and Reading Suggestions (대상 및 읽는 방법)

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 역할  Chapter | PM | PL | SW  개발자 | 마케팅 | QA | 영업 | SE |
| 1.Introduction | 🞊 | ⭘ |  | ⭘ |  |  |  |
| 2.Overall Description | 🞊 | ⭘ | ⭘ | ⭘ | ⭘ | ⭘ | ⭘ |
| 3.Environment | ⭘ | ⭘ | ⭘ | ⭘ | ⭘ |  | ⭘ |
| 4.External Interface Requirement | ⭘ | 🞊 | ⭘ |  | ⭘ |  |  |
| 5.Performance Requirement | ⭘ | ⭘ | ⭘ | ⭘ | 🞊 |  |  |
| 6.Non-Functional Requirement | ⭘ | 🞊 | ⭘ | ⭘ | ⭘ |  |  |
| 7.Functional Requirement | ⭘ | ⭘ | ⭘ | 🞊 | ⭘ | ⭘ |  |
| 8.Change Management Process | ⭘ | ⭘ |  | ⭘ |  |  |  |
| 9.Document Approval | ⭘ |  |  |  |  |  |  |

표 1 대상 및 읽는 방법 정의

범례)

🞊: 거의 암기 해야 한다.

O: 완전히 숙지해야 한다.

빈칸: 시간이 남으면 읽어봐도 된다.

* PM – 프로젝트 관리자
* PL(Project Leader) – 프로젝트의 Technical Leader
* SW 개발자 – 프로젝트의 분석/설계/구현 담당자
* 마케팅 – 제품의 기획 및 마케팅 담당
* QA(Quality Assurance) – 기능 테스트 수행 및 품질 인증 부서
* 영업 – 바텍코리아, 바텍글로벌
* SE – Technical Support

## Project Output (프로젝트 산출물)

### Output Format (산출물 형태)

* 소스코드로 SVN에서 공유한다.

### Output Name and Version (산출물명(가칭) 및 버전)

* VTReport32.dll로 제공한다.

### Patent Information (특허 출원 유무 및 내용)

* 해당 사항 없음 (N/A)

# Overall Description (전체 설명)

## Product Perspective (제품 조망)

* [e2\_v3.0\_diagrams](https://vatechcorp.sharepoint.com/%3Af%3A/s/es/Es2RyfxDy2dHiYOrXfCROhwBhtA1DjiSU6wexrnMBXzy_Q?e=B7inBy)의 Report Diagram을 참고한다.

## Overall System Configuration (전체 시스템 구성)

* [e2\_v3.0\_diagrams](https://vatechcorp.sharepoint.com/%3Af%3A/s/es/Es2RyfxDy2dHiYOrXfCROhwBhtA1DjiSU6wexrnMBXzy_Q?e=B7inBy)의 Report Diagram을 참고한다.

## Overall Operation (전체 동작방식)

* 사용자가 report 탭을 선택했을 때,
  + Image List와 환자 이미지 가져오기
  + controller는 선택된 환자정보와 이미지리스트를 Report의 UIManager에게 전달하여 display한다.
  + UIManager는 FileDeliverer에게 요청하여 FileManager를 통해 Thumbnail 이미지를 받는다.
  + UIManager는 전달받은 Thumbnail을 화면에 표시한다.
* 사용자가 Report 편집 중에 다른 탭을 선택 했을 때,
  + Controller는 Report의 UIManager에게 Report 저장 메시지 창을 보여줄 것을 요청한다.
  + 사용자가 “Report 저장”을 선택하면, UIManager는 DB Save dialog 를 보여주고,
  + 사용자가 “Report 저장하지 않음”을 선택하면, 그대로 화면을 숨긴다.
* 사용자가 환자를 검색하고자 할 때,
  + UIManager에서 이름이나 차트번호를 구분 없이 입력 한 값을 Search Patient에게 전달한다.
    - 촬영 조건으로 검색을 원할 때는 검색 창이 확장되어 촬영일자나 영상을 Import한 날짜를 기준으로 검색 할 수 있다.
  + SearchPatient는 전달 받은 검색 조건을 DBManager에게 전달하여 DB에서 해당 환자 정보리스트를 얻어 오고 그것을 UIManager에게 전달한다.
  + UIManager는 전달 받은 해당 환자들의 정보를 화면에 표시한다.
  + 환자를 선택하면, UIManager는 해당 환자를 SearchPatient에게 전달하여 DBManager를 통해 DB에서 환자의 Thumbnail Image정보리스트를 요청한다.
  + UIManager는 FileDeliverer에게 썸네일 이미지를 요청하고, 환자정보와 썸네일 이미지를 화면에 display하고, 다른 모듈에서도 변경된 환자가 동일하게 적용이 되도록 Controller에게 변경된 환자정보를 전달한다.
* 사용자가 SaveDB를 선택했을 때,
  + UIManager는 IOReport에게 환자차트번호, report 이름, comment와 report Preview이미지, report 편집 값(사용자가 편집한 데이터 값)을 전달한다.
    - UIManager는 Report preview를 이미지로 캡쳐 한다.
  + IOReport는 report 편집 값을 serializing하여.rpt파일에 Write하고, Report preview는 썸네일 이미지로 저장하여 두 파일과 Report Comment를 FileDeliverer를 통해 FileManager에게 전달하여 FileServer에 저장한다.
* 사용자가 ReportList를 선택했을 때,
  + UIManager는 선택된 환자차트번호를 IOReport에게 전달하여 DBManager에게 해당 환자의 Report List를 요청한다.
  + DBManager는 해당 환자의 Report List를 DB에서 탐색하여 IOReport를 통해 UIManager에게 전달한다.
  + UIManager는 전달받은 ReportList 정보로 preview 썸네일 이미지를 FileDeliverer를 통해 FileManager에게 요청한다.
  + UIManager는 전달받은 Report List와 preview이미지를 화면에 display한다.
* 사용자가 ReportList에서 Report를 선택했을 때,
  + UIManager는 선택한 Report정보를 IOReport에게 전달하여 report 편집 값을 요청한다.
  + IOReport는 FileDeliverer에게 전달받은 rpt파일에서 report 편집 값을 deserializing하여 해당 값들을 UIManager에게 전달해 준다.
  + UIManager는 전달받은 선택된 report 편집 값으로 화면에 저장할 때의 report page를 표시한다.
* 사용자가 Delete Report를 선택했을 때,
  + UIManager가 선택된 Report 파일의 이름을 IOReport에 전달하고, IOReport는 FileDeliverer에게 해당 report파일과 썸네일 이미지를 삭제할 것을 요청한다.
  + UIManager는 해당 Report 썸네일을 report list에서 삭제한다.
* 사용자가 ChangeTemplate을 선택했을 때,
  + UIManager는 FileDeliverer에게 Template List(Template 이름, Template preview이미지)를 요청하고, Setting file에서 Default Template 이름을 읽어와 그것들을 ChangeTemplate 창에 display한다.
    - Controller SRS API 참고
  + GetTemplate은 선택된 Template 이름을 FileDeliverer에게 전달하고 FileManager에게 template파일을 요청한다.
  + GetTemplate은 template파일을 파싱하고, Template정보를 UIManager에게 전달한다.
  + UIManager는 전달받은 Template정보를 토대로 Template의 Layout을 구성하고, Report WorkSpace에 Display한다.
* 사용자가 선택한 Template을 Default값으로 설정했을 때,
  + GetTemplate는 Local Setting파일에 선택한 Template의 이름을 Default Template 이름으로 등록한다.
* 사용자가 일반 Page Print를 선택했을 때,
  + UIManager는 Report Page 영역을 이미지로 렌더링하여 ExportReport에 전달한다.
  + ExportReport는 해당 시스템 프린터 dialog를 보여주고 인쇄를 진행한다.
* 사용자가 DICOM Print를 선택했을 때,
  + UIManager는 Report Page 영역을 이미지로 렌더링하여 ExportReport에 전달한다.
  + ExportReport는 VTDCMTK 라이브러리를 통해 DICOM Printer 인쇄를 진행한다.
    - VTDCMTK라이브러리가 제공하는 기능에 따라 프린트 dialog가 보여질 수 있다.
* 사용자가 Send to Email을 선택했을 때,
  + UIManager는 Report Page 영역을 이미지로 렌더링하여 ExportReport에 전달한다.
  + ExportReport는 해당 Report Page를 PDF 파일로 변환하여 VTEmail라이브러리에 전달하고 이메일 전송을 요청한다.
  + VTEmail은 report page를 PDF파일로 첨부하여 email로 전송한다.
* 사용자가 Export PDF를 선택했을 때,
  + UIManager는 Report Page 영역을 이미지로 렌더링하여 ExportReport에 전달한다.
  + ExportReport 는 해당 Report Page를 PDF파일로 변환하여 사용자가 지정한 경로에 저장한다.

## Product Functions (제품 주요 기능)

* 검색 조건(환자이름, 환자차트번호, Modality, 촬영날짜)으로 환자 검색을 제공, 타 모듈과 독립적으로 동작 할 수 있다.
* Image Box, TextBox 편집을 제공함으로써 사용자가 원하는 대로 Report편집이 가능하게 한다.
  + ImageBox를 삽입하고 위치와 크기를 조절할 수 있으며, Image Box에 이미지를 삽입할 수 있다.
  + TextBox를 삽입하고 위치와 크기를 조절할 수 있으며, TextBox내용을 편집하고 그 속성을 변경할 수 있다.
* Logo, PatientInfo, ReportDate, Image Info를 Report에서 보이게 하거나 숨기게 함으로써, Report의 정보를 환자에게 쉽게 제공할 수 있다.
* Page 추가, Page 이동(before/Next), Page 삭제, Page Zoom in/out, Horizontal Fit, Vertical Fit 같은 PageTool을 제공함으로써, 사용자가 용이하게 Report 페이지 편집 및 확인을 하게 한다.
* Report Template을 선택하여 사용자가 원하는 Report layout 배치를 쉽게 할 수 있다.
* Report 페이지를 rpt 파일로 저장하여 사용자가 이전 작업 내용을 쉽게 확인 및 편집 할 수 있다.
* 저장된 Report에 대하여 Report List를 제공하여 사용자가 용이하게 Report를 불러오거나 삭제할 수 있다.
* Print, Send to email, Export to PDF 기능으로 환자에게 빠르고 쉽게 Report 페이지를 제공할 수 있다.

## User Classes and Characteristics (사용자 계층과 특징)

* E2 SRS와 동일하다.

## Assumptions and Dependencies (가정과 종속 관계)

* 해당 사항 없음 (N/A)

## Apportioning of Requirements (단계별 요구사항)

* 해당 사항 없음 (N/A)

## Backward compatibility (하위 호환성)

* 해당 사항 없음 (N/A)

# Environment (환경)

* E2 SRS와 동일하다.

# External Interface Requirements (외부 인터페이스 요구사항)

## System Interfaces **(**시스템 인터페이스**)**

* [e2\_v3.0\_diagrams](https://vatechcorp.sharepoint.com/%3Af%3A/s/es/Es2RyfxDy2dHiYOrXfCROhwBhtA1DjiSU6wexrnMBXzy_Q?e=B7inBy)의 Report Diagram 참고한다.
* Source Code를 참고한다.

## User Interface **(**사용자 인터페이스)

* MMI를 참고한다.

## Main Hardware Interface (하드웨어 인터페이스**)**

* 해당 사항 없음 (N/A)

## Software Interface **(**소프트웨어 인터페이스)

* 4.1에 포함한다.

## Communication Interface **(**통신 인터페이스**)**

* 해당 사항 없음 (N/A)

## Other Interface (기타 인터페이스**)**

* 해당 사항 없음 (N/A)

# Performance requirements (성능 요구사항)

* E2 SRS와 동일하다.

# Non-Functional Requirements (기능 이외의 요구사항)

* E2 SRS와 동일하다.

# Functional Requirements (기능요구사항)

* 세부 기능 요구사항은 MMI를 참고한다.

# Change Management process (변경관리 프로세스)

* E2 SRS와 동일하다.

# Document Approvals (최종 승인자)

Identify the approvers of the SRS document. Approver name, signature, and date should be used.

Name Signature Date

# Reference Materials (참고문헌)

* 해당 사항 없음

# Appendix (부록)

## Glossary (용어)