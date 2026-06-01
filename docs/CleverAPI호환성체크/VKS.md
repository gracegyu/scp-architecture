# CleverOne에서 EzServer, Clever Space 접근시 API 호환성 체크 (Thomas)

- [PLAN-1191](https://vts.vatech.com/browse/PLAN-1191) - [CleverSpace v1.3.0] WBS와 MMI를 작성한다. **In Progress**
    
    
    - ***추가 문의 사항***
        - 지속적으로 어플리케이션과 웹 제품 간의 호환성 문제가 발생하고 있어, 웹 서비스에서 어플리케이션 버전을 확인한 뒤 최소 지원 미만인 경우 신규 버전 설치 또는 업데이트를 안내하는 구조도 구현 가능한지 검토 요청드립니다.(구현 가능 여부 검토)
- 관련 회의록
    - 2026-05-19 주요 개발 과제 진척 점검
        - 어플리케이션 제품 업데이트 시스템 검토
            1. 지속적으로 어플리케이션과 웹 제품 간의 호환성 문제가 발생할 수 있음
            2. 웹 서비스에서 어플리케이션 버전을 확인한 뒤 최소 지원 미만인 경우, 하는 구조로 구현 가능한지 검토 요청
                
                신규 버전 설치 또는 업데이트를 안내
                
            3. **자사 제품간의 연동에 필요한 기능은 자동으로 업데이트/호환 되는 구조가 필요하다.**
                
                !(warning)
                
        - Tom Idea
            - CleverOne에서 업그레이드가 필요한 일부분만 업데이트 받는 방안 검토
- 이슈
    - Clever Space 에서 새로 제공된 API (유료화 등) 들이 구 버전 CleverOne, EzServer 에서 error code 인식 못하고, 기능들의 제약사항이 생김
    - 현재 EzServer는 버전정보를 제공하지만 Client 측에서 버전 정보만으로 사용가능한지를 알 수 없음
- 논의사항
    - Client 는 UserAgent 에 제품명과 버전, OS명과 버전을 반드시 입력하도록 한다.
        
        !(tick)
        
    - 검토한 후 전사 표준화한다.
    - 현재 상황을 파악한다.
        - CleverOne → EzServer → CleverSpace
        - CleverOne → CleverSpace
        - 위 경로에서 Client 버전 정보가 전달되는지 (UserAgent에 포함되는지, custom header에 전달되는지) 민진우/ Thomas May 29, 2026
            - CleverOne → EzServer
                - UserAgent 에 "CleverOne" 문자열만 넣고 버전 정보는 포함하지 않음
                - CleverOne에서 EzServer의 버전 정보를 체크함
            - CleverOne → CleverSpace
                - UserAgent 에 "CleverOne" 문자열만 넣고 버전 정보는 포함하지 않음
                - CleverOne에서 EzServer의 버전 정보를 체크하지 않음
            - EzServer → CleverSpace
                - UserAgent 에 별도로 저장하지 않음
                - CleverSpace의 버전 정보 API 를 제공하지 않음
        - 소스코드
            - CleverOne
                - http://essvn.vatech.co.kr/svn/vatech/trunk/product/cleveronegroup/
            - EzServer (PMS Integration)
                - https://dev.azure.com/ewoosoft/ezserver/_git/ezserver_pms_integration
                - SRS: Confidential_EzServer_PMS_Integration_v6.2_SRS.docx
                - 관련 이슈: EZSV-2506 - [EzServer PMS Integration] EzCloud 연동 활성화시마다 ezserver uid가 신규 발급되는 문제를 개선한다. **Closed**
                    
                    [](https://vts.vatech.com/secure/viewavatar?size=xsmall&avatarId=12210&avatarType=issuetype)
                    
            - CleverSpace (OneID, CleverSpace)
                - OneID:
                    - Confidential_OneID_v1.0_RestApi.xlsx
                    - https://dev.azure.com/ewoosoft/scp-sharedservice/_git/oneid
                - CleverSpace:
                    - Confidential_EzCloud_v1.1_RestApi.xlsx/srs/Confidential_EzCloud_v1.1_RestApi.xlsx?d=w2f3106e184214691a959c1df68b7c363&csf=1&web=1&e=fKSfwk)
                    - https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud
    - 개선방안 전규현/ Raymond
        - 서버에서 제어
        - 클라이언트에서 제어
        - 클라이언트 정보를 UserAgent에 포함하기 또는 Custom 헤더에 포함하기
        - CleverSpace 버전 호환성 테이블 만들기
            - 참고 EzServer: [EzServer Releases (ES_Internal).xlsx](EzServer Releases (ES_Internal)(EzServer Releases).csv)
        - 1차 최소 수정으로 가능한 방법
        - 2차 근본적으로 가능한 방법
    - 개발환경
        - CleverOne, EzServer는 같은 PC
        - CleverSpace 연동은 staging 에 연결 (EzServer 설정파일 변경)
- 추가 주제
    - CleverOne → CleverSpace 로 Direct로 가는 것을 EzServer를 통하도록 하기 위한 구조
        - EzServer를 Gateway 역할로 하기 위한 효율적인 구조
        - 각 연결의 authentication 에 대한 설명이나 문서, 소스 리포 공유 (Thomas)
        - CleverOne에서 사용하는 Clever Space API 목록 일부 공유 (Nick 확인)
        - CleverSpace, OneID API
            - CleverSpace: https://server.cleverspacecloud.com/api-docs
            - OneID: https://server.oneid.cleverspacecloud.com/api-docs