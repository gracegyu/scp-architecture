**Clever One**

**Software Requirements Specification**

**Version : v0.9**

**Date : 2023-09-06**

**Writer : Nick**

**EWOOSOFT CO., Ltd.**

# 1 Introduction **(개요)**

## 1.1 Purpose (목표)

- ES의 2D, 3D 통합 뷰어인 Clever One을 개발하기 위한 문서이다.

- 이 문서는 EzDent-i와 Ez3D-i를 사용해 본 사람을 대상으로 작성됨으로,
  만일 두 제품에 대한 이해와 지식이 부족한 경우는 두 제품을 설치하여
  사용하거나 메뉴얼을 읽어보는 것을 권장한다.

## 1.2 Product Scope (범위)

- Clever One은 ES의 차세대 2D, 3D 통합 SW 솔루션이다.

  - 현재의 ES Viewer SW는 2D와 3D가 분리된 SW로 제공되고 있어 2D, 3D
    영상을 하나의 SW에서 볼 수 없는 불편함이 있고, 데이터 공유에
    어려움이 있다. 또한, 타사에서도 모든 데이터를 통합 관리하여 사용할
    수 있는 All In One 솔루션을 개발하고 출시하고 있다.

- Ez3D-i에서 사용하고 있는 3D Engine인 Open Inventor는 Graphic Card에
  따른 제약, 라이센스 비용 문제, 퀄리티의 문제 등이 있다. ES의 장기적인
  SW 개발 관점에서 자체 3D Engine을 개발하고 이를 내제화 하여 Clever
  One에 적용한다.

- Clever One은 EzDent-i와 Ez3D-i를 사용하던 기존 고객보다 신규 개원하는
  병원의 설치를 우선순위로 한다.

- Clever One은 EzDent-i(Console)와 동시에 설치되어 운영될 수 없다.

  - Clever One도 FileManagerAgent(FMA)를 포함하게 된다. FMA가 중복으로
    설치되어 운영되면 예상치 못한 문제가 발생할 수 있다.

- Clever One에서는 EzDent-i와 Ez3D-i에서 제공하는 대부분의 기능(Major
  기능)을 제공한다. 단, 개발 단계에 따라 v0.9 이후에 개발되는 기능들이
  존재한다. V0.9에서 제외되는 기능은 다음과 같다.

  - EzPicker를 이용한 타사 PMS와의 환자 연동

  - Linkage.xml을 이용한 타사 PMS와의 환자 연동

  - Report 기능

  - Endo

  - Segment

  - TMJ

  - 구독 기능

- EzDent-i와 Ez3D-i의 Minor한 기능은 v0.9에서 제외될 수도 있다.

- 동일한 이미지를 서로 다른 PC에서 동시에 편집할 수 없게 하는 기능이
  새롭게 추가된다. (v0.9 제외)

- EzDent-i와 Ez3D-i에서 생성한 일부 데이터는 Clever One에서 호환이 된다.

  - 호환되는 데이터

    - 환자 정보

    - 이미지와 이미지의 부가 정보

      - Tag: EzDent-i

      - Project: Ez3D-i

    - 계정 정보

    - SmartPay 정보 (결제된 이미지를 계속 볼 수 있음)

    - EzWebServer 정보

    - Favorite Equipment (User Calibration)

    - 이외 EzWebSever의 DB에서 관리되는 데이터

  - 호환되지 않는 데이터

    - EzDent-i와 Ez3D-i의 Settings에서 설정한 정보

    - 사용자가 생성한 External Link

    - Acquisition Tab에서 FMX 타입으로 촬영 시의 User Capture Sequence

    - FMX Layout Editor에서 생성한 Layout

- 최대 2개의 CT 데이터를 동시에 로딩이 가능하다. (P1)

  - 2개를 초과하는 CT 데이터를 한번에 로딩하면 속도나 메모리 등의 문제가
    있을 수 있다.

  - 동일한 CT를 한 PC에서 중복 Open 하는 기능을 제한적으로 제공할 수
    있다. (v0.9 제외)

- AI를 통한 자동화 기능이 추가될 예정이다.

  - 기존의 Tooth Segment(DAVIS Toolkit for 3D) 기능은 그대로 사용될
    예정이다.

- 설치 옵션, 라이선스에 따라 일부 기능이 비활성화 되거나 사용 불가능할
  수 있다.

- 제한된 범위 내에서 ODM 제공이 가능하다.

  - 소스 코드는 하나의 트리를 유지하되, 리소스 파일(UI, Text, License,
    Settings 등)은 ODM 별로 다르게 설정하여 배포가 가능하다.

- 자사의 Desktop Application과 연동 기능을 제한적으로 제공한다. 시장의
  요구 사항에 따라 연동되는 자사 SW의 범위와 연동 기능이 변경될 수 있다.

- 4K Monitor를 지원한다.

  - 4K Monitor에서도 UI가 깨지거나 사이즈의 변경 없이 일반 모니터와
    동일한 UI를 제공해야한다.

- EzUpdater를 통한 자동 업데이트 기능을 제공한다.

- 통합 인증 기능(SSO)을 제공한다.

  - EzServer를 사용하는 제품들과 SSO가 가능하다. SSO를 위해서는
    EzCommonTools를 설치해야 한다.

  - One ID와의 연동 기능을 제공한다.(TBD)

- Mirage 라이선스는 사용하지 않는다. Cryptlex의 Floating 라이선스와
  Node-Lock 라이선스, Trial 라이선스만 제공된다.

  - Offline 라이선스 활성화 기능은 제공하지 않는다.

- EzShare와 연동 기능을 제공한다. EzShare와 연동을 위해서는 One ID로
  인증을 받아야 한다.

- 기존의 TCP/IP 기반의 FileManager는 연동 범위에 포함되지 않는다. REST
  API를 제공하는 EzWebServer와만 연동이 된다.

- 구매한 라이선스의 옵션에 따라 일부 기능들을 사용하지 못할 수 있다.

- Vatech의 Console SW는 차기버전부터 "관리자 권한 획득" 권한이 제거될
  예정이다. 따라서, Clever One도 관리자 권한을 획득하지 않도록 한다.

  - 하지만 기존의 Console SW (관리자 권한을 요하는)과도 문제없이 연동이
    되어야 한다.

- GDPR을 준수한다.

- EzDent-i와 Ez3D-i의 기존 소스를 활용하거나 공통 모듈화 할 수 있는
  기능들을 검토하고 이를 적용한다.

  - 2D Viewer는 EzDent-i의 Viewer 모듈을 공통 라이브러리화 하여
    사용한다.

  - 3D Viewer는 ES의 신규 3D Engine으로 개발되고 있는 라이브러리를
    사용한다.

  - 촬영은 EzImagingAcquisition을 사용한다.

  - EzWebServer와 연동을 위해 ESWebServerClient를 개발하여 사용한다.

- 기존에 개발되어 있는 Common 모듈을 활용하여 개발한다.

- EzDent-i와 Ez3D-i의 SRS를 참고한다.

## 1.3 Document Conventions (문서규칙)

- 본 문서의 구성에 있어서, 다음과 같은 문서 규칙을 따른다.

  - 우선순위는 각 기능은 중요도에 따라 다음과 같은 3가지 개발 Priority로
    표시한다.

    - P1: 높음, 중요한 기능으로 반드시 구현해야 함.

    - P2: 보통, 일반적인 기능으로 구현해야 함.

    - P3: 낮음, 부가적인 기능으로 필요 시 배제할 수 있음.

  - 우선순위 표시 방법

    - Priority가 표시되지 않은 항목은 P1으로 간주한다.

    - 우선순위의 표시는 해당 항목의 문장 뒤에 (P1)과 같이 붙인다.

    - e.g.

      - 기능1 (P2)

      - 기능2 (P3)

  - 버전 별 지원계획 표기 방법

    - 이번 버전(v1.0)에서 지원하는 항목은 별도의 표시를 하지 않아도
      된다.

    - 다음 버전(v2.0)에서 지원하는 항목은 문장의 뒤에 (v2.0)과 같이
      붙인다.

    - 지원계획이 정해지지 않았고 미래에 지원할 항목은 문장의 뒤에
      (NEXT)와 같이 붙인다.

    - 지원하지 않을 기능은 문장의 뒤에 (지원 안함)과 같이 붙인다.

## 1.4 Terms and Abbreviations (정의 및 약어)

- ES - Ewoosoft의 약어

- EzServer - ES 제품군들이 공통으로 사용하는 Server

- PMS(Practice Management System) - 환자 및 병원 관리를 위한 시스템

- DICOM - Digital Imaging and Communications in Medicine 의 약어로 의료
  영상 표준 규약

- HIPAA - Health Insurance Portability and Accountability Act의 약어로
  미국 보건복지부가 의료정보의 프라이버시를 보호하기 위해 제정한 법

- Qt - GUI 프로그램 개발을 위한 크로스 플랫폼 위젯 툴킷. 주로 C++로
  개발. Windows, Mac, Linux 등을 지원한다.

- RC - Radiology Center의 약자

- 3DDX - Surgical Guide 제작업체

- EasyDent4 - 이우소프트에서 개발한 2D Image management SW

- TMJ - 턱관절(Temporomandibular Joint)

- SmartPay - 3D 장비를 2D 장비 가격으로 판매하되, Ez3D-i의 모든 기능을
  사용하기 위해서는 추가 비용을 지불하도록 하여 수익 모델을 창출하는
  VM의 사업 모델

- GDPR - 유럽 연합 일반 데이터 보호 규칙(General Data Protection
  Regulation). 유럽 연합의 모든 개인에 대한 데이터 프라이버시 보호를
  강화하고 표준화하기 위해 제정된 법규

## 1.5 Related Documents (관련문서)

- MRD (v0.9)

  - Link

- MMI (v0.9)

  - Link

- SRS

  - Feature List

    - Sharepoint의 [ES Project \> Clever One \>
      SRS](https://vatechcorp.sharepoint.com/:x:/s/es/EWR2HWD2Dt1EtcbMdXjtMxwBF3f2X0hrfnjaGlURGk8YoQ?e=gocIUd)

  - ES3DEngin

    - Link

  - EzImagingAcquisition

    - Sharepoint의 [ES Project \> common \>
      ESImagingAcquisition](https://vatechcorp.sharepoint.com/:f:/s/es/Ekw6jdPCtnRBt4Ru7nJQy9QBZTMtCLNzGCuMFNX1LWYZ1g?e=htE4bq)

  - ESImageCapture

    - Link

  - DB Manager SRS

    - Sharepoint의 [ES Project \> common \> VTDBManager \>
      SRS](https://vatechcorp.sharepoint.com/:f:/s/es/Es50EZEzirVIt_GgR4bd1hkBRhlDQYuGJqi9jRKUr7Ghjw?e=CYSBa5)

- Reference

  - EzDent-i SRS

    - Sharepoint의 [ES Project \> EzDent-i \>
      SRS](https://vatechcorp.sharepoint.com/:f:/s/es/EvDkQquD_wpLni9-UDOXeJYBptfEZ2j6xrLLN7-I_Y6pfQ?e=516MPM)

  - Ez3D-i SRS

    - Sharepoint의 [ES Project \> Ez3D-i \>
      SRS](https://vatechcorp.sharepoint.com/:f:/s/es/ElIyDG9LpQ9Plo6-ou03GuMBCUaU6pMDmWA2SdLMn7XeOg?e=aAGOVb)

  - EzWebAgent

    - Sharepoint의 [ES Project \> common \> EzWebAgent \>
      SRS](https://vatechcorp.sharepoint.com/:f:/s/es/Eqj4wSUQMllNrTBWi2yb2QABPx5yyvveG02GKRDvTVSlNg?e=8lNSba)

  - EzShare

    - Link

  - REST API

    - <http://esapi.from.io>

## 1.6 Intended Audience and Reading Suggestions (대상 및 읽는 방법)

[표 1](#_Ref185190661)은 본 프로젝트에 참여하는 부서 및 인력 별로 본
문서를 활용하는데 있어 참고하거나 숙지해야 할 문서 항목을 제시하고 있다.

| 역할 Chapter | PM | PL | SW 개발자 | UI 디자인 | 마케팅 | QA | 영업 | SE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.Introduction | OO | O | O |  | O | O |  |  |
| 2.Overall Description | OO | O | O | O | O | O | O | O |
| 3.Environment | O | O | O |  | O | O |  | O |
| 4.External Interface Requirement | O | OO | O | O |  | O |  |  |
| 5.Performance Requirement | O | O | O |  |  | OO |  |  |
| 6.Non-Functional Requirement | O | OO | O |  |  | O |  |  |
| 7.Functional Requirement | O | O | O | O |  | O |  |  |
| 8.Change Management Process | O | O |  |  | O |  |  |  |
| 9.Document Approval | O |  |  |  |  |  |  |  |

: []{#_Ref185190661 .anchor}표 1 대상 및 읽는 방법 정의

> 범례)
>
> OO : 거의 암기 해야 한다.
>
> O : 완전히 숙지해야 한다.
>
> 빈칸 : 시간이 남으면 읽어봐도 된다.

- PM -- 프로젝트 관리자

- PL(Project Leader) -- 프로젝트의 Technical Leader

- SW 개발자 -- 프로젝트의 분석/설계/구현 담당자

- UI 디자인 -- 제품의 UI 담당

- 마케팅 -- 제품의 기획 및 마케팅 담당

- 영업 -- VM, 바텍 해외법인, ES의 기획파트

- SE -- Technical Support

## 1.7 Project Output (프로젝트 산출물)

### 1.7.1 Output Format (산출물 형태)

- 본 제품의 최종 산출물은 PC에 설치되는 Desktop Application Software
  이다.

### 1.7.2 Output Name and Version (산출물명(가칭) 및 버전)

- Clever One v0.9

### 1.7.3 Patent Information (특허 출원 유무 및 내용)

- 특허 출원이 필요한 내용은 미리 찾아서 신청해야 한다.

- 사전에 타 특허 침해를 하지 않도록 미리 검색을 해서 조사를 해야 한다.

# 2 Overall Description (전체 설명)

## 2.1 Product Perspective (제품 조망)

![A picture containing text, diagram, circle, screenshot Description
automatically generated](media/image1.png)

## 2.2 Overall System Configuration (전체 시스템 구성)

![A picture containing text, diagram, circle, drawing Description
automatically generated](media/image2.png)

- Main Controller - 다른 컴포넌트를 컨트롤 하기 위한 모듈이다.

- Patient -- 환자 및 이미지를 관리하기 위한 모듈이다.

- Viewer -- 2D, 3D Image의 Viewing 과 Consult Contents의 Viewing 및
  관리를 위한 모듈이다.

- Report -- Print와 DICOM Print 등을 활용한 Reporting을 위한 모듈이다.

- 2D Diagnosis -- 2D 이미지의 Viewing 및 시뮬레이션을 위한 모듈이다.

- 3D Diagnosis -- 3D 이미지의 Viewing 및 시물레이션을 위한 모듈이다.

- MPR - CT 이미지를 3D와 2D(Axial/Sagittal/Coronal View)로 보여주는
  기본적인 Viewer이다.

- Section - 사용자가 지정한 Curve를 따라 2D panorama 및 Section View를
  생성한다.

- 3D PAN - Implant Simulation을 위한 기능을 포함한다.

- TMJ -- TMJ 진단을 위한 모듈이다.

- Acquisition -- 영상 촬영을 위한 모듈이다.

- EzBridge -- 3rd Party App과 환자, 이미지 연동을 위한 모듈이다.

- External Link -- 3rd Party App 실행한다.

- FileManagerAgent - EOX에서 촬영된 이미지를 EzWebServer에 전송한다.

- EzMtDICOMSender -- 이미지를 PACS로 전송한다.

- Vatech Console SW -- EOX 장비를 컨트롤 하기 위한 바텍의 촬영
  프로그램이다.

- EzOrtho -- ES의 교정 전문 프로그램이다.

- PMS -- 환자, 진료 차트, 이미지 등을 관리하는 SW 이다.

- VTDICOMWrapper-- DICOM 라이브러리를 Wrapping한 라이브러리이다. (DCMTK
  3.6을 사용한다.)

- 3DDX -- Surgical Guide 제작업체의 Web Server

- NobelClinician -- Nobel Biocare사의 Surgical Guide Application

- SimPlant - Materialise사의 Surgical Guide Application

- EzWebServer -- File Server 및 DB 기능을 담당하는 Application이다.

- Auth Server -- 통합로그인 기능을 제공하는 서버이다.

- EzWebAgent -- Client Side에서 통합 로그인 기능을 제공하는 Tool이다.

- License Server -- License 인증정보 관리 및 Floating License 관리
  기능을 제공하는 서버이다.

<!-- -->

- 3DDX -- Surgical Guide 제작업체의 Web Server

- NobelClinician -- Nobel Biocare사의 Surgical Guide application

- SimPlant - Materialise사의 Surgical Guide application

## 2.3 Overall Operation (전체 동작방식)

- 실행

  - 사용자가 Clever One을 실행한다.

  - Clever One이 실행되면 Controller는,

    - Clever One 초기화에 필요한 설정 파일을 읽어온다.

    - EzWebServer와 연결을 확인한다.

      - 연결이 되어 있지 않은 경우, 이를 사용자에게 알리고 서버 연결을
        위한 Dialog를 띄운다.

    - License Server로부터 라이선스 활성화 상태를 확인한다.

    - 사용자로부터 전달받은 계정 정보를 EzWebServer에게 전달하고 인가된
      사용자인지 확인하여, 인가된 사용자라면 인증 정보(토큰)를 전달한다.

      - 전달받은 토큰은 주기적으로 갱신 해야한다.

    - 설정 파일 및 라이선스 정보, 플러그인 데이터를 참조하여 UI를
      구성하고 화면에 표시한다.

    - 만약 Clever One 실행 시, Parameter로 전달받은 환자 정보나 이미지
      정보가 있는 경우 해당 데이터를 표시해준다.

- 환자 검색 및 선택

  - 사용자가 차트 번호나 이름을 입력하고 환자 검색을 요청하면,

    - EzWebServer로부터 전달받은 값에 해당하는 환자 리스트를 조회한다.

    - 사용자가 조회된 환자 리스트 중 임의 환자를 선택하면 해당 환자의
      상세 정보를 화면에 표시한다.

    - 선택된 환자 정보를 Sharing Data에 업데이트 한다.

      - Sharing Data는 환자가 변경되었음을 모든 플러그인에 Notify 한다.

      - Sharing Data로부터 Notify를 받은 플러그인은 Activate 상태(현재
        선택된 탭 여부)에 따라 아래와 같이 동작한다.

        - Deactivate 되어있는 플러그인들은 Flag에 환자 변경 여부를
          업데이트 한다.

        - Activate 되어있는 플러그인은 Flag에 업데이트 할 필요가 없이
          바로 환자 변경과 관련된 작업을 수행한다.

      - 플러그인들은 Tab(플러그인)이 Activate 될 때, Flag를 체크하여
        환자가 변경된 경우 환자 정보를 갱신 한다.

        - 환자 정보의 갱신이 완료되었으면 환자 변경 Flag를 초기화 한다.

    - 선택된 환자의 이미지 리스트를 조회하여 썸네일을 다운로드 받는다.

      - 다운로드 된 썸네일을 썸네일 썸네일 리스에에 표시한다.

      - 환자의 이미지 리스트를 Sharing Data에 업데이트 하고, 이를 다른
        플러그인과 공유한다.

        - 환자 검색을 통한 이미지 리스트 갱신, 촬영이나 이미지 삭제등을
          통한 이미지 리스트가 변경된 경우도 환자 변경과 동일한
          워크플로우로 동작한다.

- 촬영

  - 사용자가 촬영을 원하는 Modality의 촬영 버튼을 실행한다.

    - CT, Cephalo, Panorama를 선택한 경우 (EOX로 촬영되는 Modality),

      - Acquisition 모듈은 PatientInfo 파일을 생성하여, Vatech Console
        SW를 실행한다.

      - Console SW에서 촬영이 완료되면 Windows Global Message가
        Broadcasting 된다.

      - FileManagerAgent는 Console SW로부터 Global Message를 받으면
        Console SW에서 생성한 Output 파일을 참조하여 촬영된 이미지를
        EzWebServer로 전송한다.

      - FileManagerAgent는 전송 시작, 전송 진행률, 전송 완료를 Clever
        One에게 Notify 한다.

        - Windows Global Message를 이용한다.

      - Clever One은 전송 진행률 및 전송 완료 여부를 화면에 표시해준다.

      - 전송이 완료된 경우, EzWebServer로부터 다시 해당 환자의 이미지
        리스트를 검색하고, 이를 Sharing Data에 업데이트 한다.

        - 이미지 리스트가 변경된 경우임으로 각 플러그인들은 Activate 될
          때, 이미지 리스트를 갱신한다. (환자 변경과 동일한 워크플로우로
          동작한다.)

    - IO Sensor, IO Camera, VSP, TWAIN을 선택한 경우

      - 선택한 Modality에 맞는 UI를 구성하여 화면에 표시한다.

      - 사용자가 원하는 Tooth Code, FMX Layout을 선택한다.

        - 선택된 장비(모드)에 따라 선택이 불가능한 경우도 있다.

      - 촬영을 원하는 장비를 선택하고, 장비별 옵션을 선택한다.

        - 옵션은 Modality 마다 상이하다. IO Sensor의 경우 Image
          Processing을 IO Camera는 Resolution을 선택할 수 있다. VSP에는
          옵셥이 없고 TWAIN의 경우는 Modality를 선택할 수 있다.

      - 촬영이 완료되면 자동/수동으로 촬영 이미지를 Server로 저장한다.

        - 위와 동일하게 각 플러그인에서 이미지 갱신이 필요하다.

      - IO Sensor로 촬영된 이미지는 반드시 DCM 파일로 변환하여 저장한다.

    - DSLR을 선택한 경우

      - 설정에 DSLR 이미지가 생성될 폴더의 위치를 지정한다.

      - Acquisition 모듈은 위에서 설정된 폴더를 Watching 하고 있다가,
        해당 폴더에 이미지 파일이 생성되면 이를 Clever One으로 Import
        한다.

      - 사용자는 촬영된 DSLR 이미지를 Server로 저장한다.

        - 위와 동일하게 각 플러그인에서 이미지 갱신이 필요하다.

- 탭 전환

  - 사용자의 선택에 따라 Controller는 Patient, Viewer, 2D Diagnosis, 3D
    Diagnosis Component를 활성화 한다.

  - Patient Tab에서 선택(더블클릭)된 이미지의 Modality에 따라
    Controller는 2D Diagnosis, 3D Diagnosis, Viewer Tab으로 전환하여
    해당 이미지를 표시한다.

    - 2D Image인 경우는 2D Diagnosis Tab으로 전환

    - 3D Image인 경우는 3D Diagnosis Tab으로 전환

    - Capture Image인 경우는 Consult Tab으로 전환

  - Deactivate 되는 Tab은 변경된 이미지 정보(Tag, Project)를 Sharing
    Data에 업데이트 한다.

    - Flag를 업데이트 해야한다.

  - Activate 되는 Tab은 Flag 체크하여 "환자/이미지 리스트/ 이미지
    정보"의 수정이 있는 경우 Sharing Data를 참조하여 해당 값을 갱신한다.

    - Deactivate 된 플러그인에서 보여지던 이미지와 Activate 되는
      플러그인에서 보여지는 이미지가 동일한 경우에만 갱신한다.

      - 이미지 정보가 변경된 경우에는 변경 여부 뿐 아니라, 변경된
        이미지의 이름도 각 플러그인에서 기록하고 있어야 한다.

      - 환자 검색, 변경과 같은 원리로 동작한다.

<!-- -->

- Multi Window View

  - 2D Tab에서 3D 이미지를 보는 경우, 3D Tab에서 2D 이미지를 보는 경우,
    3D Tab에서 2개의 3D 데이터를 보는 경우는 Multi Window 방식으로
    Viewer를 구성한다.

    - EzDent-i와 Ez3D-i의 레이아웃 개념과는 다르다.

    - 하나의 독립적인 Window로 해당 Window 내부에서 다시 레이아웃을
      변경할 수 있다.

    - Multi Window는 Vertical, Horizontal 방향이 섞여서 구성될 수 없다.

  - 선택된 Window에 따라 Control Panel의 Function들이 Show/Hide 혹은
    Enable/Disable 된다.

  - Multi Window는 Split Bar를 통해 사이즈 조절이 가능하다.

  - 3D Tab에서 3D 이미지와 함께 Open 되었던 2D 이미지 혹은 3D 이미지가
    있다면(Multi Window),

    - 다른 CT를 Open하거나 프로그램이 종료될 때 이를 Project에 저장하고,

    - 다음 번 동일한 3D 이미지를 Open 하는 경우, Multi Window로 이전과
      동일하게 2D, 3D 이미지와 함께 Open 되어야 한다.

    - Split 사이즈(비율)도 Project에 저장 후 적용 되어야 한다.

  - Sub Window(Multi Window로 생성된 Windows )는 Popup 형태로 Main
    Window에서 분리될 수 있다.

    - Dual Screen Mode처럼 동작한다.

    - Popup된 Sub Window는 사용자의 조작에 의해 다시 Docking 될 수 있다.

## 2.4 Product Functions (제품 주요 기능)

- 환자 및 환자 이미지 관리

  - EzDent-i/Ez3D-i/EzOrtho/EzDent Web과 환자, 이미지 데이터를 공유

  - 환자 추가, 삭제, 변경, 숨기기

  - 환자 검색

    - Recently

    - Doctor

  - 이미지 검색

    - Modality

    - Acquisition Date

  - 이미지 삭제

  - 이미지 Export

    - CD

    - Local

    - E-Mail

    - Clipboard

    - PACS

    - Print

  - 이미지 공유 (EzShare)

  - 해쉬태그

    - 환자 검색

    - 이미지 검색

  - 이미지 Transfer

  - 데이터 그룹핑

<!-- -->

- 제품간 연동

  - ES의 Desktop App과의 연동

  - 타사 PMS와의 연동

  - 타사 3^rd^ Party App과 연동

  - External Link

<!-- -->

- 다양한 Modality의 촬영 및 저장

  - Extra Oral X-Ray 촬영(CT, Panorama, Cephalo, ...)

  - SDK 연동을 통한 촬영

    - EzSensor (IO Sensor)

    - VSP (IO Scanner)

  - TWAIN 연동 제공

  - IO Camera

  - IO Scanner

  - Auto DSLR

  - Import

- Consult Contents 관리

  - 2D, 3D 이미지의 동시 Viewing 기능

    - Free Draw 정도의 간단한 Simulation만 가능

  - Consult Contents Management

    - 동영상, 이미지와 일반 문서 등의 저장 기능

    - Favorite, Cart, Playlist 기능

  - Consult Contents(Video) 뷰어

  - Consult Contents의 다국어 지원

  - Presentation Mode

- 2D Diagnosis

  - 2D 이미지 Viewing

    - Split View를 통한 분할 View

      - Split View에서 3D 이미지도 Viewing 가능

  - 레이아웃 변경 및 관리

  - Image Adjust

  - Measurements

  - Annotations

  - Simulation

  - Capture

  - Overlay Management

  - Presentation Mode

- 3D Diagnosis

  - 3D 이미지 Viewing

    - Split View를 통한 분할 View

      - Split View에서 2D 이미지도 Viewing 가능

  <!-- -->

  - 3D Volume Panorama & Auto Panorama 기능

    - 3D Volume Panorama 전용 Controller(Navigator) 지원

    - 3D Pan Tab 내 3D Volume Panorama ↔3D VR 전환 기능

  - 2D & 3D 영상 표시 및 분석 기능 강화

    - Oblique View 기능

    - 3D Length, Angle 기능

    - 영상 판독 지원을 위한 2D영상처리 기능

    <!-- -->

    - Bone의 진단 용이성을 향상시키는 VR Image Processing

    - Multi Length, Pointer, Grid tool

  <!-- -->

  - Simulation 기능

    - Implant Simulation

    - Canal Simulation

    - Draw Curve

    - Multi Curve 기능

    - 두 가지 Type의 Bone Density 표시 기능 지원

    - Crown 단독 Simulation 기능

    - Implant Collision Detection

    - Crown 크기 조절 기능

    - Implant Guide / Implant Path 제공

  - 장치사업 연계 지원 기능

    - Surgical Guide 제작 기능을 지원하기 위한 STL Import / Export

    - STL Import

    - STL Export

  - Airway 진단 기능

    - Airway Volume 추출 및 단면적 계산

    - Airway Volume의 Axial view 제공

    - Airway Smoothing 적용

  - Dual Monitor 지원

- 기타 기능

  - SmartPay

  - 4K Monitor 지원

  - GDPR Compliance

  - External App / 3^rd^ Party App과 연동

  - FMX Layout Editor (v0.9 제외)

  - FMX Auto Crop (v0.9 제외)

  - ES 제품간 SSO (Authentication)

  - License를 통한 제품 관리

  - AI를 통한 자동화 솔루션

## 2.5 User Classes and Characteristics (사용자 계층과 특징)

- 치과 의사

  - 특징

    - 치아를 포함한 구강질환을 진단 및 치료책임을 가지는 사람

  - 사용 목적

    - 정확한 임상적 진단을 위한 목적

    - 질환(우식증,발육성/후천성 치아이상,염증 등)을 영상으로 확인

    - 임상학적 구조물에 대한 정보(두께, 크기, 모양 등)를 영상으로 확인

    - 환자에게 질환에 대한 설명을 하기 위한 목적 (과거 또는 다른 환자
      영상 활용)

    - 의사 및 치과에 대한 전문성 및 신뢰성을 높이기 위한 목적

    - 환자 관리를 위한 목적 (환자의 상태 관리 등)

    - 치료 계획 수립을 위한 목적 (각종 Simulation 기능)

    - 학회, 논문 등의 자료로 활용하기 위한 목적

- 치위생사

  - 특징

    - 치과의사의 치료 보조 및 진료를 위한 환경을 준비하는 사람 (영상
      촬영, 차트 준비 등)

    - 치위생사의 그 외 업무는 다음과 같이 구분

      - 병원관리 업무: 환자의 건강 상태를 기록하고 관리하며, 진료 기구
        및 장비 소독과 배치 등의 업무

      - 행정적인 업무: 의료 보험 청구 업무 등의 업무

      - Clinic 여건에 따라 코디네이터 업무를 겸하기도 한다.

  - 사용 목적

    - 진료 준비를 하기 위한 목적

      - 영상 촬영 후 영상에 대한 정상 유무 확인

      - 의사가 진단할 수 있도록 영상 Open

> • 코디네이터

- 특징

  - 환자에게 현재 구강 상태 및 진료 계획을 설명하는 사람

  - 상담 이외에 코디네이터의 업무는 고객 관리(접수, 예약, 수납 등)등의
    병원 서비스 업무

- 사용 목적

  - 환자와 상담(현 구강 상태, 진료 후 모습 등)를 통해 Clinic 매출을
    증대시키기 위한 목적

  - 환자 관리(보험, 접수, 수납)를 위한 목적

<!-- -->

- 환자

  - 특징

    - 치과를 방문하는 환자는 다음과 같이 구분된다.

    - 구강질환에 대한 치료를 위해 치과를 방문하는 사람

    - 예방(구강 검진)/미용(교정)/일상생활의 불편함(보철물, 임플란트)을
      해소하기 위해 치과를 방문하는 사람

  - 사용 목적

    - 본인의 구강 상태를 쉽고 정확하게 확인하기 위한 목적

- Radiology Center 환경

  - 방사선사 (의료기사로 방사선사 면허를 취득한 사람)

    - 특징

      - 치과 의사의 Order에 따라 X-ray 영상 촬영 및 장비를 관리하는 사람

    - 사용 목적

      - 촬영 영상에 대한 정상 유무 확인 목적

      - 임상학적 구조물의 구분을 향상 시키기 위한 목적 (Contrast,
        Brightness, Windowing 등)

  - 방사선 전문의 (의사면허 취득 후 방사선 전문의 과정을 거친 사람)

    - 특징

      - 촬영한 영상을 판독한 후 전문의에게 소견을 전달하여 진단의
        정확도를 높여주는 사람

    - 사용 목적

      - 임상적 진단(길이, Density측정) 및 소견서 작성을 위한 목적

## 2.6 Assumptions and Dependencies (가정과 종속 관계)

- 2D 기능 개발을 위한 2D Common Library의 개발이 완료되어야 한다.

- 3D 기능 개발을 위한 3D Engine의 개발이 완료되어야 한다.

- 이미지 촬영 기능 개발을 위한 ESImagingAcqusition의 개발이 완료되어야
  한다.

- Clever One을 위한 EzWebServer 신규 버전이 개발 되어 Clever One과 함께
  배포 되어야 한다.

- EzWebServer의 속도는 제품의 반응 속도에 많은 영향을 미치므로 속도가
  최적화 되어야 한다.

  - EzWebServer의 속도는 환자 검색 및 변경, 이미지 조회 등 거의 모든
    기능에 영향을 미쳐 제품의 사용성이 매우 떨어지게 된다.

  - 불필요하게 여러번 호출하는 REST API를 최적화 한다.

- AI 기능이 포함될 경우, 해당 모듈이 개발 완료되어야 한다.

- One ID로 Authentication를 위한 관련 System이 구축되어야 한다.

- EzShare와 연동을 위해 관련 System이 구축되어야 한다.

- EzDent-i에 포함된 Tools 중 Clever One에서도 사용할 Tool은 Common으로
  SVN 위치 변경을 해야한다.

  - EzBridge

  - FileManagerAgent

  - FMX Auto Crop

  - FMX Layout Editor (Dependency 복잡도가 매우 높음)

<!-- -->

- 64bit 환경에서 EzSensor를 TWAIN으로 촬영하기 위해서는 EzSensor TWAIN
  Driver의 수정이 필요하다.

  - 현재 64bit 환경에서 TWAIN으로 EzSensor 촬영을 시도하면 제품이 Crash
    된다. 32bit는 정상 동작한다.

## 2.7 Apportioning of Requirements (단계별 요구사항)

- Clever One v0.9

  - Patient Tab

  - Consult Tab

  - 2D Diagnosis Tab

  - 3D Diagnosis Tab

  - Acquisition

  - 3^rd^ Party, PMS, ES 제품간 연동 기능

- Clever One 차기 버전

  - 3D Diagnosis의 TMJ, Endo, Segment 기능

  - Report

## 2.8 Backward compatibility (하위 호환성)

- EasyDent3, EasyDent4의 환자, 이미지 정보는 VTMigrator(Tool)를 통해
  EzServer로 Migration 될 수 있다.

  - EzServer로 Migration 된 데이터는 Clever One에서 볼 수 있다.

- EzDent-i / Ez3D-i의 데이터는 별도의 Migration 없이 Clever One에서 볼
  수 있다.

  - Clever One은 EzDent-i/Ez3D-i의 환자, 이미지(Tag, Project), Account
    등의 정보와 호환성을 갖는다.

- 3^rd^ Party App 연동 프로토콜은 일부 기능만 유지한다.

  - Linkage.xml을 이용한 환자 정보 연동은 기능에서 제외하도록 한다.

    - 추후 시장에서 강력한 요구 사항이 있는 경우 다시 고려한다.

  - EzPicker를 통한 환자 정보 연동은 기능에서 제외하도록 한다.

  - EzBridge를 통한 환자 및 이미지 연동은 Clever One에 포함한다.

  - 사용자에겐 EzWebServer REST API를 통한 3^rd^ Party App 연동을
    권장한다.

- Clever One은 Extra Oral X-Ray 촬영 SW가 Link Type으로 SDK Link를
  지원하지 않는 경우, 제품간 호환성을 지원하지 않는다.

- [EzWebServer]{.mark}는 최소 v5.x.x 이상 버전부터 호환성이 유지된다...

# 3 Environment (환경)

## 3.1 Operating Environment (운영 환경)

### 3.1.1 Hardware Environment (하드웨어 환경)

- Clever One은 OpenGL과 GPU를 이용하여 Image를 Rendering 할 예정이므로,
  GPU가 없는 Hardware는 지원하지 않는다.

- 이 제품에서 요구하는 최저 하드웨어 사양과 권장 하드웨어 사양은 아래
  표와 같다.

- **3D Engine에서 요구하는 하드웨어 사양에 따라 변경될 수 있다.**

  [\[하드웨어 사양\]]{.mark}

| **구분** | **최소 사양** | **권장 사양** |
| --- | --- | --- |
| 운영 체제(OS) | 지원 OS: Windows 10 이상 (x64) |  |
| CPU | 듀얼 코어 @3.4GHz | 쿼드 코어 @3.4GHz 이상 |
| RAM | 4 GB | 8 GB 이상 |
| HDD | 20 GB | 512 GB (7,500 RPM SATA 이상) |
| 그래픽 사양 | GPU Memory 1GB의 GPU | GPU Memory 4GB 이상의 GPU |
| 화면해상도 | 1280×1024 | 1920×1080 |

### 3.1.2 Software Environment (소프트웨어 환경)

#### 3.1.2.1 OS Environment (운영체제 환경)

- Windows

  - [Windows XP, Windows Vista, Windows 7, Windows 8, Windows 8.1에 대한
    공식적인 지원은 하지 않는다.]{.mark}

    - Windows 7에 대한 MS의 지원은 2020년 1월 종료되었다.

    - Windows 8에 대한 MS의 지원은 2016년 1월 종료되었다.

    - Windows 8.1에 대한 MS의 지원은 2023년 1월 종료되었다.

  - 3D 기능의 퀄리티 및 Micro Soft의 32bit 기술 지원 종료에 따라 Clever
    One은 64bit만 지원한다.

    - MS는 Windows 10의 32bit 기술 지원을 종료하였다.

  - Clever One이 지원하는 Windows OS는 아래와 같다.

    - Windows 11 (x64)

    - Windows 10 (x64)

- Mac OS

  - OS X는 지원하지 않는다.

  - Boot Camp를 이용해서 Mac을 지원한다. Parallels Desktop은 지원하지
    않는다.

#### 3.1.2.2 OS외 software 환경

- Database

  - PostgreSQL 9.2.2.1

- Web Browser

  - Chromium Browser 106.0.5249.103.

## 3.2 Product Installation and Configuration (제품 설치 및 설정)

## 3.3 Distribution Environment (배포 환경)

### 3.3.1 Master Configuration (마스터 구성)

- 제품의 마스터는 실행 파일 형태의 인스톨 프로그램이다.

  - Clever One v1.0.0 Setup.exe

- 인스톨 프로그램은 Console, Client를 구분하여 설치할 수 있는 구조여야
  한다.

  - Console: FileManagerAgent와 Clever One이 동시에 설치되는 방식

  - Client: Clever One만 설치되는 방식

- 하나의 설치 마스터로 모듈 별로 설치하거나, 분리된 설치 마스터로 모듈
  별로 설치하는 등의 마스터 구성과 관련된 세부 사항은 추후 요구사항을
  파악하여 제공한다.

### 3.3.2 Distribution Method (배포 방법)

- USB Memory에 설치파일을 포함시켜 고객에게 전달한다.

  - 라이선스는 USB Memory에 함께 전달된다.

- <http://space.ewoosoft.com>에 설치 파일을 업로드 하여, 고객이 직접
  다운로드 받을 수 있도록 한다.

  - CS를 통해 라이선스를 요청하여 발급받아야 한다.

### 3.3.3 Patch/Update Method (패치와 업데이트 방법)

- [space.ewoosoft.com](http://space.ewoosoft.com/index.php/login)에서
  최신 버전을 다운로드 받아 설치한다.

  - 제품을 Update 할 때는 호환되는 EzServer 버전을 확인 후 적절한 버전의
    EzServer를 설치해야 한다.

    - EzServer는 최신 버전을 설치할 것을 권장한다.

  - Update 설치시에 데이터나 User Settings은 변경하지 않는다.

- EzUpdate를 통한 제품의 Update를 제공한다.

  - EzServer v5.4.0 이상, EzCommonTools v1.1 이상의 버전이 설치된 경우
    업데이트 기능이 제공된다.

    - EzCommonTools 인스톨 시, 설치되는 EzLauncher에서 EzUpdater를
      실행하면 제품의 버전 History를 확인할 수 있고 다운로드 받을 수
      있다.

  - 제품을 실행할 때도 배포된 상위 버전이 있는 경우 이를 사용자에게
    알리고, 업데이트를 진행 할 수있다.

## 3.4 Development Environment (개발 환경)

### 3.4.1 Hardware Environment (하드웨어 환경)

- Monitor

  - 24인치 이상의 모니터

  - 서브 모니터

  - 4K 모니터

- PC

  - 권장 하드웨어 사양 이상

### 3.4.2 Software Environment (소프트웨어 환경)

- Qt Library ver. 5.15.5 for Visual Studio 2019 64bit version

  - built from qt-everywhere-opensource-src-5.15.5.zip

- Qt Creator ver. 10.0.0 이상

  - 최신 버전을 추천

- Visual Studio Professional 2019 (Visual C++ 2019)

- [Server]{.mark}

  - EzServer v5.X.X

  - PostgreSQL v9.2

- 기타 외부 라이브러리

  - vtk 9.0.3

  - TBD

## 3.5 Test Environment (테스트 환경)

- 3.1장에 명시된 운영 환경과 동일하다.

## 3.6 Configuration Management (형상관리)

### 3.6.1 Location of Outputs (산출물 위치)

#### 3.6.1.1 Location of Source Code (소스코드 위치)

- <http://essvn.vatech.co.kr/svn/vatech/trunk/product/cleveronegroup>

#### 3.6.1.2 Location of Documents (문서 위치)

- Sharepoint의 [ES Project \> Clever
  One](https://vatechcorp.sharepoint.com/:f:/s/es/EhNBDjWDzK1JkOlnK-PNkmQBQcq9bb4E2T-oUoJwufDoqg?e=u60VET)

### 3.6.2 Build Environment (빌드 환경)

- 별도의 빌드 장비를 구성한다.

- 빌드 장비의 환경은 Software Environment와 동일하다.

## 3.7 Bugtrack System (버그트래킹)

- VTS Project Name: ES_CleverOne_PJT관리 (CONE)

## 3.8 Other Environment (기타 환경)

- 없음

# 4 External Interface Requirements (외부 인터페이스 요구사항)

## 4.1 System Interfaces **(**시스템 인터페이스**)**

### 4.1.1 Component Definition

- 2.2장의 다이어그램을 참조한다.

### 4.1.2 Plug-in Interface

- Main Controller은 Dynamic Plugin 방식으로 Plugins를 Load한다. 다음은
  제품에서 사용할 Plugin Interface이다. 상세 설계시 필요한 Interface를
  추가한다.

```cpp
namespace cone
{
class IPlugin
{
public:
virtual void Initialize() = 0;
virtual void Release() = 0;
virtual void SetInitialized(VBOOL bInitialized) = 0;
virtual VBOOL IsInitialized() const = 0;
virtual void OnActivated() = 0;
virtual void OnDeactivated() = 0;
virtual void SetActivated(VBOOL bActivated) = 0;
virtual VBOOL IsActivated() const = 0;
virtual void SetPluginID(const QString &strPluginID) = 0;
virtual QString GetPluginID() const = 0;
virtual void SetTitle(const QString &strTitle) = 0;
virtual QString GetTitle() const = 0;
virtual void SetMainWidget(QWidget *pMainWidget) = 0;
virtual QWidget *GetMainWidget() = 0;
virtual void SetPluginWidget(QWidget *pPlguinWidget) = 0;
virtual QWidget *GetPluginWidget() = 0;
};
} // namespace cone
#define IPLUGIN_IID "com.ewoosoft.clever.one.IPlugin"
Q_DECLARE_INTERFACE(IPlugin, IPLUGIN_IID)
```

### 4.1.3 인터페이스 정의

#### 4.1.3.1 Clever One -- EzWebServer

- [EzWebServer의 DB
  스키마](https://vatechcorp.sharepoint.com/:x:/s/es/EW5Z2EvRhTxFspXioIFzgAMBW2oKaSieU9jgkjVqCMJsfw?e=ZKiRrs)를
  참고한다.

- [EzWebServer REST API](http://esapi.from.io/posts?id=home)를 이용한다.

  - REST API는
    [ESWebServerClient](http://essvn.vatech.co.kr/svn/vatech/trunk/product/common/ESWebServerClient)를
    사용하여 호출한다.

```cpp
class WEBSERVERCLIENT_EXPORT CWebServerClient
{
private:
CWebServerClient();
public:
static CWebServerClient &GetInstance()
{
static CWebServerClient instance;
return instance;
}
static CE2DataService *E2DataService()
{
return GetInstance().GetE2DataService();
}
static CE3DataService *E3DataService()
{
return GetInstance().GetE3DataService();
}
static CConsultDataService *ConsultDataService()
{
return GetInstance().GetConsultDataService();
}
static CImplantDataService *ImplantDataService()
{
return GetInstance().GetImplantDataService();
}
static CSettingsService *SettingsService()
{
return GetInstance().GetSettingsService();
}
static CAnalyticsService *AnalyticsService()
{
return GetInstance().GetAnalyticsService();
}
static CAuthService *AuthService()
{
return GetInstance().GetAuthService();
}
static CFileService *FileService()
{
return GetInstance().GetFileService();
}
static CFileServiceUsingCM *FileServiceUsingCM()
{
return GetInstance().GetFileServiceUsingCM();
}
static CInfoService *InfoService()
{
return GetInstance().GetInfoService();
}
private:
void Initialize();
public:
void ReleaseInstance();
void SetHttp(EzWebLegacy::CHttp *pHttp, VBOOL bUseCacheManager =
VTRUE);
void SetToken(const QString &strToken);
CE2DataService *GetE2DataService();
CE3DataService *GetE3DataService();
CConsultDataService *GetConsultDataService();
CImplantDataService *GetImplantDataService();
CSettingsService *GetSettingsService();
CAnalyticsService *GetAnalyticsService();
CAuthService *GetAuthService();
CFileService *GetFileService();
CFileServiceUsingCM *GetFileServiceUsingCM();
CInfoService *GetInfoService();
private:
EzWebLegacy::CHttp *m_pHttp;
CE2DataService *m_pE2DataService;
CE3DataService *m_pE3DataService;
CConsultDataService *m_pConsultDataService;
CImplantDataService *m_pImplantDataService;
CFileService *m_pFileService;
CFileServiceUsingCM *m_pFileServiceUsingCM;
CSettingsService *m_pSettingsService;
CAnalyticsService *m_pAnalyticsService;
CAuthService *m_pAuthService;
CInfoService *m_pInfoService;
};
```

#### 4.1.3.2 Clever One -- Smartpay Payment System

- Smartpay SRS, IRS를 참조한다.

  - [smartpay_irs.doc](https://vatechcorp.sharepoint.com/:w:/s/es/EfWKtqztgqFNiKsmhgmUL2IBCEO6bL2PR8--6CCqlEZfrw?e=RJYoHY)

  - [smartpay_srs.doc](https://vatechcorp.sharepoint.com/:w:/s/es/ES287JcZxMdDi9kdnLYPJJoBuruQ4zsH_iywjrMgEndE6Q?e=8OjfLZ)

- 추가적으로 EzDent-i의 소스 코드를 참조한다.

#### 4.1.3.3 Clever One -- 3^rd^ Party App

- 3^rd^ Party App에서 제공하는 연동 방식을 따라 인터페이스를 정의한다.

- External Link 방식을 제공하여 3^rd^ Party App을 실행할 수 있다.

  - EzDent-i의 External Link 방식을 참조한다.

#### 4.1.3.4 Clever One -- DICOM Print

- VTDICOMWrapper을 이용한다.

```cpp
/**
* @brief Print
* @param pFilename [in] File name(Full path)
* @param sPrintOption [in] Print Option
* @param nNumberOfCopies [in] Number of Copies(Tag : (2000,0010)
/ VR, VM : <IS/1>)
* @param pSCUAETitle [in] SCU AE Title
* @param sPeerOption [in] Peer AE Title, Peer Host Name, Peer
Port
* @param sNetworkOption [in] Maximum PDU(Protocol Data Unit)
Size / DIMSE(DICOM Message Service Element) Timeout,
ACSE(Association Control Service Element) Timeout
* @parma nMinResolutionW [in] Minimum resolution for a print
bitmap(width in pixel)
* @parma nMinResolutionH [in] Minimum resolution for a print
bitmap(height in pixel)
* @parma nMaxResolutionW [in] Maximum resolution for a print
bitmap(width in pixel)
* @parma nMaxResolutionH [in] Maximum resolution for a print
bitmap(height in pixel)
* @param funcProgressCallback [in] Progress Callback Function
* @param pCallbackContext [in] Callback Context
* @return
* 'VSUCCESS' : 성공 / error code : 실패
* @details
* 'funcProgressCallback'으로 전달되는 'nProgress' 값은 최상위
bit에 따라 의미가 다름
* - 최상위 bit(0) : 인쇄요청 진행률(%, 0 ~ 100)
* - 최상위 bit(1) : 인쇄장수 진행률(%, 0 ~ 100, 최상위 bit를
제외한 값)
* - ex) 5장 인쇄요청 시
* - 1번째 장[0 ~ 100 -> 0x80000014(최상위 bit 제외시 : 20)]
* - 2번째 장[0 ~ 100 -> 0x80000028(최상위 bit 제외시 : 40)]
* - 3번째 장[0 ~ 100 -> 0x8000003C(최상위 bit 제외시 : 60)]
* - 4번째 장[0 ~ 100 -> 0x80000050(최상위 bit 제외시 : 80)]
* - 5번째 장[0 ~ 100 -> 0x80000064(최상위 bit 제외시 : 100)]
*/
VRET VTDICOMWrapper::print(const VCHAR *pFilename,
const SPrintOption &sPrintOption,
VUSHORT nNumberOfCopies,
const VCHAR *pSCUAETitle,
const SPeerOption &sPeerOption,
const SNetworkOption &sNetworkOption,
VULONG nMinResolutionW,
VULONG nMinResolutionH,
VULONG nMaxResolutionW,
VULONG nMaxResolutionH,
ProgressCallback funcProgressCallback,
void *pCallbackContext)
```

#### 4.1.3.5 Clever One -- EzWebAgent

- Clever One과 EzWebAgent와의 인터페이싱은
  [VTAuthentication](http://essvn.vatech.co.kr/svn/vatech/trunk/product/common/VTAuthentication/src)을
  사용한다.

- VTAuthentication에 EzWebServer의 IP, Port, Protocol과 인증에 필요한
  정보를 전달하면 Auth 기능을 사용할 수 있다.

- VTAuthentication의 생성자

```cpp
VTAuthenticationHelper::VTAuthenticationHelper(const QString &strIp,
const QString &strPort,
const QString &strClientId,
const QString &strSecret,
VBOOL bUseHttps)
```

- EzWebAgent의 주요 API

```
// Login Dialog의 실행
EAuthHelperError authorize(const SAuthInfo &sInfo);
// Logout을 요청
EAuthHelperError logout(const SAuthInfo &sInfo);
// 세션 연장을 요청
EAuthHelperError detectUserAction();
// authorize() 통해 Login이 정상적으로 이뤄진 경우, Token을 요청
EAuthHelperError requestTokenWithPKCE(const QString &strCode,
const QString &strRedirectUri,
SAuthToken &sAuthToken);
// 로그인 없이 ClientCredentials로 토큰을 요청
EAuthHelperError requestTokenWithClientCredentials(SAuthToken
&sAuthToken, const QString &strScopes = "");
// 토큰이 만료되기 전, 토큰 갱신을 요청
EAuthHelperError requestTokenWithRefresToken(SAuthToken
&sAuthToken);
```

#### 4.1.3.6 Acquisition -- Vatech Console SW

- Vatech의 Capture SW를 실행한다. Capture SW 실행 시, PatientInfo.ini를
  약속된 위치에 생성하고, Modality를 파라미터로 전달한다.

  - Modality 파라미터를 전달하지 않으면 아무런 Modality가 선택되지 않은
    상태로 Capture SW가 실행된다.

- PatientInfo.ini 예시

```
[PATIENT_INFO]
ChartNumber=20200309_163615
FNAME=Wilson^Grace // First Name^LastName
AGE=32
GENDER=F // F: Female, M: Male, O: Other
BIRTHDAY=19910123 // yyyyMMdd
```

- Capture SW를 실행 시, 파라미터에 따른 촬영 Modality

```
CT = -1
Panorama = -2
Cephalo = -4
3D Photo = -5
CT + 3D Photo = -6
```

#### 4.1.3.7 Acquisition -- IO Sensor, IO Camera, IO Scanner

- 촬영 Device와의 인터페이스는
  [ESImagingAcquisition](http://essvn.vatech.co.kr/svn/vatech/trunk/product/common/ESImagingAcquisition)을
  사용한다.

  - [Secret_imagingdevice_command_list.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EejYm3QTMJxNjWd6EP8EyWMBUuedWHjLxXe2W6jL02hZlA?e=CaZhga)를
    참조한다.

- ESImagingAcquisition에서 사용되는 Command

| **Name** | **Description** | **Parameter name : type** |
| --- | --- | --- |
| OpenCommand | Prepare to run the sdk. +----------------+ | mapSDK: QMap<int, QString> hWnd: HWND (Optional) |
| MakeInfoFileCommand | Make the information file needed to acquire the image. (ex. PatientInfo.ini ...) +----------------+ | jsonInfo: QJsonObject sFile: SFileInfo |
| FetchDeviceListCommand | Fetch the list of device. | N/A |
| OpenTargetDeviceCommand | Open the handle of the selected specific device with options. (Prepare to use a specific device.) | sDevice: SDeviceInfo |
| CloseTargetDeviceCommand | Close the handle of the selected specific device. | sDevice: SDeviceInfo |
| GetTargetDeviceConfigCommand | Gets configuration information for a specific device that is ready or has a handle. | sDevice: SDeviceInfo |
| ChangeDeviceOptionCommand | Change the device option. (ex. Resolution) | jsonOption: QJSonObject |
| FetchImageCommand | Fetch the image. +----------------+ | sImage: SImageInfo sProgress: SProgress (Optional) |
| ExecuteUtilProcessorCommand | Execute the util processor. (ex. PostImageProcessor, ecalibrationProcessor.) | sProcessor: SProcessorInfo |
| CloseCommand | Close the plugin. | N/A |
| StartFetchMultiImageCommand | Start to fetch multi image files. The same command is not allowed until the process started by StartFetchMultiImageCommand is finished. +----------------+ | sImage: SImageInfo sProgress: SProgress (Optional) |
| FinishFetchMultiImageCommand | Finish to the watch process started by StartFetchMultiImageCommand. | N/A |

#### 4.1.3.8 PMS & 3^rd^ Party App -- EzBridge

- PMS나 3^rd^ Party App에서 Clever One을 실행(연동)하는 인터페이스는
  EzBridge를 통한 방식만을 제공한다.

- PMS나 3^rd^ Party App가 EzBridge를 정해진 인터페이스에 따라 호출하면
  Clever One을 실행할 수 있다.

- Clever One의 실행과 관련된 인터페이스는 아래와 같다.

```
// 차트번호에 해당하는 환자를 선택하여 Clever One을 실행
{EzBridge의 실행 경로} **/main:chart_no="차트번호"**
Example) .\EzBridge.exe /main:chart_no="20230505_123456"
// 차트번호에 해당하는 환자를 선택하고, 전달받은 이미지가 Viewer
Tab에서 보여진 상태로 Clever One을 실행
{EzBridge의 실행 경로} **/main:chart_no="차트번호" /img:"이미지 파일
이름"**
Example) .\EzBridge.exe /main:chart_no="20230505_123456"
/img:"DX20220505_123.jpg"
[// 차트번호에 해당하는 환자를 선택하고, 전달받은 Modality의 촬영
Mode에 진입한 상태로 Clever One을 실행]{.mark}
{EzBridge의 실행 경로} **/main:chart_no="차트번호"
/acq:selectedModality="모달리티"**
Example) .\EzBridge.exe /main:chart_no="20230505_123456"
/acq:selectedModality="IOSensor"
- selectedModality에 들어갈 수 있는 Modality
- CT
- Cephalo
- Panorama
- IOSensor
- IOCamera
- TWAIN
```

- 이 외에도 환자 등록, 조회, 이미지 등록, 다운로드 등과 관련된
  인터페이스는 EzBridge 메뉴얼을 참조한다.

#### 4.1.3.9 Clever One -- NobelClinician/3DDX/Simplant

- Ez3D-i의 SRS를 참조한다.

## 4.2 User Interface **(**사용자 인터페이스)

- MMI를 참조한다.

## 4.3 Hardware Interface (하드웨어 인터페이스**)**

- 4.1에 포함된다.

## 4.4 Software Interface **(**소프트웨어 인터페이스)

- 4.1에 포함된다.

## 4.5 Communication Interface **(**통신 인터페이스**)**

- 4.1에 포함된다.

## 4.6 Other Interface (기타 인터페이스**)**

- 해당사항 없음

# 5 Performance requirements (성능 요구사항**)**

## 5.1 Throughput (작업처리량)

- Response Time, Concurrent Session의 정의를 따른다.

## 5.2 Concurrent Session (동시 세션)

- 사용자의 Request를 Serial하게 처리하므로 하나의 Session만 존재한다.

## 5.3 Response Time (대응시간)

| **[대응시간(SW 항목)]{.mark}** | **시간(최대)** | **비고** |
| --- | --- | --- |
| 프로그램 실행 | 15초 |  |
| CT 영상 오픈 +-----------+----------------+ +-----------+----------------+ | FOV 8x8 FOV 10x9 FOV 24x19 | 17초 17초 21초 |
| CT 영상 재오픈 +-----------+----------------+ +-----------+----------------+ | FOV 8x8 FOV 10x9 FOV 24x19 | 7초 7초 17초 |
| 탭 이동 | 3초 |  |
| 환자 검색 | 1초 | 기본 설정인 최근 15명의 환자를 검색하는데 걸리는 시간 |
| 환지 썸네일 로딩 |  |  |
| [3D 관련..]{.mark} |  |  |

- 위 표의 시간은 최저 사양 환경에서의 대응 시간이다.

- 탭 이동 시간은 탭을 이동하여 모든 이미지의 렌더링 및 사용자가 조작한
  모든 항목이 적용되는데 까지 소요되는 시간이다.

## 5.4 Performance Dependency (성능 종속 관계)

- 3D 이미지의 렌더링 속도는 ES3DEngine 및 하드웨어의 성능에 영향을
  받는다.

- 데이터 파일 저장 및 조회 속도에 영향을 주는 요인은 다음과 같다.

  - Network 환경과 EzWebServer의 성능에 영향을 받는다.

    - EzWebServer에 동시 접속하는 Client의 수가 많아질수록, 주고 받는
      데이터의 크기가 커질수록 성능은 저하된다.

  - 데이터 파일 조회 속도를 높이기 위해 디스크에 파일 Caching을 위한
    공간을 두고 관리한다. 데이터 파일 조회 속도는 Caching 디스크 크기와
    Policy 및 사용 Pattern에 영향을 받는다.

<!-- -->

- 촬영 속도는 외부 프로그램 및 외부 모듈의 성능에 영향을 받는다.

<!-- -->

- AI 기능은 AI Module의 성능에 영향을 받는다.

## 5.5 Other Performance Requirements (기타 성능 요구사항**)**

- 초고해상도 DSLR 영상은 파일 사이즈가 너무 커서 보관에 부담을 주므로
  Full HD(1920X1080)를 기준으로 그보다 큰 사이즈는 기준 영상의 크기로
  줄인다.

- 한명의 환자당 저장할 수 있는 이미지의 갯수는 1000개 이하 이다.

# 6 Non-Functional Requirements (기능 이외의 요구사항**)**

## 6.1 Safety requirements (안전성 요구사항)

- 촬영 중 System이 Crash 되거나, Shutdown 되었을 경우 촬영 데이터는
  유실된다.

  - CT, Cephalo, Panorama의 경우 촬영은 완료 되었으나 저장되기 전이라면
    Console SW의 Recon 기능으로 유실된 이미지를 복구할 수 있다.

  - 그 외의 촬영 장비로 촬영된 이미지의 경우 촬영은 완료 되었으나
    저장되기 전이라면 Import 기능으로 해당 이미지를 복구할 수 있다. 단,
    이런 경우 Calibration과 같은 정보는 유실될 수 있다.

- 이미 촬영되어서 DB 및 파일서버에 저장된 Data는 System Crash로 인하여
  유실되면 안된다.

- 전원이 끊기거나, 시스템 Crash 등 비정상적으로 종료하는 경우 마지막으로
  사용자가 저장하지 않은 data는 저장되지 않으며 복구할 수 없다.

- Network이나 EzWebServer에 문제가 발생한 경우에도 작업 내용은 저장되지
  않고 복구할 수도 없다.

## 6.2 Security Requirements (보안 요구사항**)**

- 의료기기 사이버 보안 가이드라인을 준수한다.

- 통합 인증 기능(SSO)을 제공한다.

  - EzWebAgent를 통하여 Ewoosoft 제품군 통합 인증을 기능을 제공한다.

  - Login 옵션이 On 인 경우에만 동작하며, Login 옵션이 Off 인경우
    EzWebAgent가 필요하지 않다.

  - 통합 인증은 VTAuthenticationHelper Module을 이용한다.

  - 통합 인증을 위해서 EzWebServer에 Clever One의 Client/Secret 등록해야
    한다.

  - 통합 인증에 관한 상세내용은 [ESAuth
    SRS](https://vatechcorp.sharepoint.com/:f:/s/es/EgJt1k5ZttVEt3yhEo4FXIYB64SNlHWXGC687r27DaPBOA?e=IjbrzP)와
    [EzWebAgent
    SRS](https://vatechcorp.sharepoint.com/:f:/s/es/Eqj4wSUQMllNrTBWi2yb2QABPx5yyvveG02GKRDvTVSlNg?e=xk3AqI)를
    참조한다.

- 개인 정보 보호 문제

  - Data 송수신시 HTTPS를 적용해 암호화한다.

    - Server Search시 UDP Protocol을 통해 서버의 HTTP/HTTPS 지원여부를
      확인한다.

    - EzWebSer의 Option 설정에 따라 HTTPS 기능의 제공 여부가 결정된다.

  - UDP Protocol은 [DBManager
    SRS](https://vatechcorp.sharepoint.com/:x:/s/es/EW5Z2EvRhTxFspXioIFzgAMBW2oKaSieU9jgkjVqCMJsfw?e=5smjk8)의
    UDP Protocol Sheet 참조 한다.

  - EzWebServer v5.0에서 HTTPS에 Self-Signed Certificate를
    사용하기때문에 발생하는 SSL error는 무시한다.

- HIPAA, GDPR, 개인정보보호법, 정보통신망법을 준수한다.

  - 환자로부터 개인 정보수집동의서에 서명을 받을 것을 Guide한다.

  - GDPR 준수를 위해 제공되는 기능은 아래와 같다.

    - Display Option

    - Anonymization

    - Authorization 

    - Encryption

    - Audit Tracing

    - Image와 Tag file은 삭제하지 않는다. 그 외의 파일들은 모두
      삭제한다.

    - 패스워드는 암호화 하여 보관하고, 패스워드 설정 옵션을 제공한다.

## 6.3 Software System Attributes (소프트웨어 시스템 특성)

### 6.3.1 Availability (가용성)

- 병원의 상황에 따라서 24/7 동작해야 할 수 있다.

  - Clever One은 항상 실행된 상태에서 외부 촬영 장비에서 촬영된 이미지를
    EzWebServer에 전송해야 한다. 따라서 Clever One의 FileManagerAgent는
    컴퓨터가 켜지면 자동으로 실행되어 대기하는 데몬 형태로 개발되어야
    한다.

- 사용자의 요청에 의해서만 실행된다.

  - 비정상 종료되었을 때에도 자동으로 재실행되지 않는다.

### 6.3.2 Maintainability (유지보수성)

- 다국어 지원이 용이하도록 gettext 방식을 사용한다.

- On/Off가 가능한 debug library를 사용하여, debug log를 남긴다.

### 6.3.3 Portability (이식성)

- Desktop 이외에 다른 Platform으로의 이식성은 고려하지 않는다.

  - 다른 Platform에서의 Application이 필요하다면 EzMobile이나 EzDent
    Web을 사용하거나 새롭게 개발되어야 한다.

- Windows 이외에 다른 OS로의 이식성은 고려하지 않는다.

### 6.3.4 Reliability (신뢰성)

- MTBF(Mean Time Between Failures)는 7일이다.

  - 병원에서는 통상적으로 하루에 한 번 재부팅을 하기 때문에 7일이면
    충분한 신뢰성을 가질 수 있다.

  - 병원의 상황에 따라서 계속 켜 놓는 경우에는 최소한 1주일에 한번은 이
    제품을 재시작 해야 하며, 이 소프트웨어의 안정적인 운용을 위해서는
    하루에 한번은 재시작 하는 것을 권장한다.

### 6.3.5 Interoperability (연동성)

- Clever One과 각 촬영 장비는 제조사에서 제공하는 SDK 또는 TWAIN
  Driver에 의해 연동한다.

- 자사 제품과의 연동 기능을 제공한다.

- 타사 3^rd^ Party SW와의 연동 기능을 제공한다.

- 타사 PMS와의 연동은 3^rd^ Party REST API(권장), EzBridge를 통한 방법을
  지원한다.

  - EzPicker, Linkage.xml을 통한 연동 방식은 시장의 요구사항이 있을 경우
    제공한다.

- Clever One에서 임의의 3^rd^ Party SW를 실행시킬 수 있는 External Link
  기능을 제공한다.

### 6.3.6 Remaining Attributes (나머지 특성)

- 해당 사항 없음

## 6.4 Logical Database Requirements (데이터베이스 요구사항)

### 6.4.1 Relational Database

- ES의 다른 제품들과 Database를 공유한다. Database와 관련된 정보는 다음
  파일을 참고한다.

  - [Secret_dbmanager_srs_db_schema.xlsx](https://vatechcorp.sharepoint.com/:x:/s/es/EW5Z2EvRhTxFspXioIFzgAMBW2oKaSieU9jgkjVqCMJsfw)

- 독립적으로 실행되는 Database를 지원해야 한다.

  - Cache 기능을 위해 독립적인 Database를 사용한다. (SQLite)

### 6.4.2 Files

- ES의 다른 제품들과 File Server를 공유한다.

  - 기존 File Server에 Clever One에 필요한 Folder, File을 추가한다.

  - 제품에서 생성하고 사용하는 파일들의 리스트와 위치, 포맷 등에 대한
    자세한 설명은 다음 링크를 참고한다.

    - [Link](https://vatechcorp-my.sharepoint.com/personal/nick_tak_ewoosoft_com/Documents/07.%20CleverOne/SRS/Confidential_CleverOne_v1.0_srs_files.xlsx)

### 6.4.3 Audit Log

- 환자, 이미지의 추가/수정/삭제/export는 Server에서 log를 남겨 추적
  가능하도록 한다.

  - Log file의 위치, format은 EzWebServer의 문서 및 code를 참조한다.

- VTDebug에 의해 생성되는 log는 각 client의 Log 폴더에 저장한다.

## 6.5 Business Rules (비즈니스 규칙)

- 해당 사항 없음

## 6.6 Design and Implementation Constraints (설계와 구현 제한사항)

### 6.6.1 Standards Compliance (표준준수)

- HIPAA, GDPR를 준수한다.

- 개인정보보호법, 정보통신망법, 의료기기 사이버 보안 가이드라인을
  준수한다.

- DICOM 표준을 준수한다.

- PACS 표준을 준수한다.

- OAuth 2.0 표준을 준수한다.

### 6.6.2 Other Constraints (기타 제한 사항)

- 각 Tab들은 Qt Plugin 방식으로 구현한다.

  - Plugin interface는 4장을 참조한다.

- ES3DEngine 개발을 위한 Library는 VTK를 사용한다.

  - 자세한 내용은 ES3DEngine의 SRS를 참고한다.

- ES의 Coding Convention을 준수한다.

- 국제화 library는 ES common의 VTIntl을 사용한다.

## 6.7 Memory Constraints (메모리 제한 사항)

- 가용 메모리 대비 Volume Data의 사이즈가 클 경우에는 Volume Data를
  Binning한다.

- 환자가 선택되었을 때 메모리에 Load 될 Thumbnail 이미지의 최대 수는
  1000이다.

  - Thumbnail 이미지의 크기는 최대 240X180이다.

  - 따라서, Thumbnail 이미지만을 위한 메모리는 42Kb X 1000 = 약 42Mb가
    된다.

- 1Mb의 원본 이미지를 8개 load 한다면 이미지만을 위한 메모리는 50Mb가
  필요하다

## 6.8 Operations (운영 요구사항**)**

- 해당 사항 없음

## 6.9 Site Adaptation Requirements **(**사이트 적용 요구사항**)**

- 해당 사항 없음

## 6.10 Internationalization Requirements (다국어 지원 요구사항)

- 다음 언어별 Text (LC_MESSAGING)과 OS가 지원하는 Locale 설정에 따른
  기능을 지원한다. 그 외에 결재시스템, 세금제도, ID 증명번호 등 언어나
  국가별로 상이한 어떤 기능도 지원하지 않는다.

  .

  ----------------------------
       언어         Locale
  -------------- -------------
     미국영어        en_US

      한국어         ko_KR

      일본어         ja_JP

      중국어         zh_CN

   중국어(대만)      zh_TW

     프랑스어        fr_FR

     러시아어        ru_RU

      체코어         cs_CZ

    포르투갈어       pt_PT

      터키어         tr_TR

     헝가리어        hu_HU

     폴란드어        pl_PL

      독일어         de_DE

     스페인어        es_ES

     이태리어        it_IT

      아랍어         ar_SA

    카자흐스탄       kk_KZ

    키르키스탄       ky_KG

    우크라이나       uk_UA

   우즈베키스탄      uz_UZ

     베트남어        vi_VN

    포르투갈어       pt_PT

    이탈리아어       it_IT

   인도네시아어      id_ID
  ----------------------------

- 숫자 및 날짜 표시 포맷에 대해서만 해당 국가의 포맷을 지원한다.

- LC_MONETARY는 이 제품에는 존재하지 않는다.

## 6.11 Unicode Support (유니코드 지원)

- 문자열의 유니코드를 지원 하기 위해 다음과 같은 규칙을 따른다.

  - 유니코드 Application으로 개발한다.

  - Application 내부에서는 UCS2 (UTF-16의 Subset)로 한다.

  - 파일 저장 시는 UTF-8 포맷으로 저장한다.

  - Network으로 전송 시는 UTF-8 포맷으로 전송한다.

## 6.12 64bit Support (64비트 지원)

- Clever One은 64bit만을 지원한다.

  - Volume Rendering 기능을 포함하므로 32bit은 메모리 문제를 일으킬 수
    있으므로, Ez3D-i와 마찬가지로 64bit만 지원하기로 한다.

## 6.13 Certification **(**제품 인증)

- MFDS(한국), CE(유럽), FDA(미국) 인증을 받는다.

  - 진행 방법 및 필요한 자료는 인증팀이 issue
    [ESRA-86](https://vts.vatech.co.kr/browse/ESRA-86)를 통해 결정하고
    요청한다.

  <!-- -->

  - 제품 인증은 Release 일정에 맞추어 완료되어야 한다.

<!-- -->

- HIPAA 는 Certified 되는 법이 아니기 때문에 인증은 존재하지 않는다.

## 6.14 Field Test (필드 테스트)

- 현재 예정되어 있는 필드 테스트는 없다.

  - 추후 유관부서와 논의하여 필드 테스트 계획을 수립한다.

## 6.15 Other Requirements (기타 요구 사항)

- 해당 사항 없음

# 7 Functional Requirements (기능요구사항)

- 기능 요구 사항
  [Link](https://vatechcorp-my.sharepoint.com/personal/nick_tak_ewoosoft_com/Documents/07.%20CleverOne/SRS/Confidential_CleverOne_v1.0_FeatureList.xlsx)를
  참조한다.

# 8 Change Management process **(**변경관리 프로세스**)**

- Follows EWOOSOFT's current SRS change management process.

# 9 Document Approvals **(**최종 승인자**)**

Identify the approvers of the SRS document. Approver name, signature,
and date should be used.

[Name Signature Date]{.underline}

# 10 Reference Materials (참고문헌)

모든 문서는 소스코드 관리 시스템의 파일 위치로 기재한다.

# 11 Appendix (부록)

## 11.1 Glossary (용어)
