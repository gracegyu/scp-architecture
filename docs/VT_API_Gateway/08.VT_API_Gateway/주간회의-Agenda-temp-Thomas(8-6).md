# VT API Gateway 프로젝트

- 논의사항
    - EzServer와 Vatech API Gateway targets 연동 계획 (Thomas)
        - 추가 대상
            - (v)AXS: 연내 연동 예정
            - (v)CleverSpace: 연내 연동 예정
            - (?)CleverRC, Clever Dent, Weclever: 3가지 모두 동일 API 로 EzServer와 연동된 상태
                - EVNCRC-3142 - Jira issue doesn't exist or you don't have permission to view it.
            - (?)Dentbird 연동: ~10/30
                - [[예정] 2026-08-04 주요 개발 과제 진척 점검#%5B%EC%98%88%EC%A0%95%5D20260804%EC%A3%BC%EC%9A%94%EA%B0%9C%EB%B0%9C%EA%B3%BC%EC%A0%9C%EC%A7%84%EC%B2%99%EC%A0%90%EA%B2%80-EzServer](https://vks.vatech.com/spaces/ESMN/pages/323276461/%EC%98%88%EC%A0%95+2026-08-04+%EC%A3%BC%EC%9A%94+%EA%B0%9C%EB%B0%9C+%EA%B3%BC%EC%A0%9C+%EC%A7%84%EC%B2%99+%EC%A0%90%EA%B2%80#id-[%EC%98%88%EC%A0%95]20260804%EC%A3%BC%EC%9A%94%EA%B0%9C%EB%B0%9C%EA%B3%BC%EC%A0%9C%EC%A7%84%EC%B2%99%EC%A0%90%EA%B2%80-%5B%EC%98%88%EC%A0%95%5D20260804%EC%A3%BC%EC%9A%94%EA%B0%9C%EB%B0%9C%EA%B3%BC%EC%A0%9C%EC%A7%84%EC%B2%99%EC%A0%90%EA%B2%80-EzServer)
                - PLAN-1270 - 이마고웍스사와 Dentbird 서비스 연동을 위한 협업을 검토한다. **In Progress**
                    
                    [](https://vts.vatech.com/secure/viewavatar?size=xsmall&avatarId=12218&avatarType=issuetype)
                    
        - 이슈
            - Dentbird와 같이 EzServer는 중개 역할만 하는데 이를 지원하려면 EzServer Upgrade가 필요함.
                - EzServer가 중계역할만 하는 추가연동에 대해서는 VAG, EzServer 에서 미리 고려할 방안이 필요해 보임.
            - Dentbird와 같은 연동은 동시에 1개가 아니라 다중이 될 수도 있을 거 같음
                - CleverSpace 사용하면서, Dentbird 동시 사용 (이 경우 EzServer의 reverse proxy가 2개 설정되어야 함)
                - EzServer에 target 정보와 region 정보를 VAG로부터 동적으로 받아서 설정가능하도록 할 필요가 있음
                    - 사용자는 target과 region을 설정하면 EzServer는 VAG로부터 endpoint를 받도록 한다.
    - User Agent 제약사항 공유 및 SRS 업데이트 요청 (Thomas)
        - SRS: VT API Gateway — 개발 Roadmap 결정#5.%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EC%8B%9D%EB%B3%84%ED%97%A4%EB%8D%94%ED%91%9C%EC%A4%80(%ED%99%95%EC%A0%95))
        - Web Frontend App들의 경우,
            - Browser에서 설정해주는 User-Agent를 변경할 수 없다.
                - 단, EzWebAgent (Electron) 위에서 동작하는 Frontend App은 Browser 에서 설정한 것에 App의 User-Agent를 덧붙일 수 있다.
            - Vatech-OS 값을 Frontend 자체적으로는 구할 수 없다. EzServer API로도 제공되지 않음.
            - Vatech-Clinic-Id 값은 관련된 일부 Backend 들만 가질 수 있고, Frontend, Desktop App들은 자체적으로 설정할 수 없다.
                - (?)EzWebServer API를 사용하면 가져올 수도 있지만 그 정도로 반드시 넣어야 하는 값인가?