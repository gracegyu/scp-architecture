# DAVIS Toolkit for Segmentation 과 ES제품간 연동 버전

: DAVIS Toolkit for Segmentation(이하 DTKS)와 ES제품간의 연동되는 제품 호환 버전을 정리한다.

- 출시날짜는 ReleaseNote(ES출시)를 기준으로 한것으로 최종 VN출시날짜와 일부 다를 수 있습니다.

> **DTKS 버전**과 **DTKS 3D Segmentation Server (EAI Engine)** 두 열은 DAVIS Toolkit for Segmentation(DTKS)의 하위 두 버전 축이다(원문 표는 병합 헤더).

| 출시 날짜 | DTKS 버전 | DTKS 3D Segmentation Server (EAI Engine) | EzServer | Clever One | Ez3D-i | EzDent-i | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-03-31 | v1.0.0.3 | v1.4.0 | v5.2.2, v6.1.0, v6.2.0 | v1.0.0.3 | v5.5.10.1 | v3.5.15 | • 제품 출시 |
| 2025-07-10 | v1.1.0.0 | v1.4.1/v2.0.1 | v5.5.2, v6.2.1 | v1.0.2 | v5.5.10 | v3.5.16 | • A compatible **NVIDIA display driver (version ≥ 576.02)** is required |
| 2025-07-25 | v1.1.1.1 | v2.0.2 | v5.5.2, v6.2.1 | v1.0.3 | v5.5.10 | v3.5.16 | • Included GPU RTX 50 Series |
| 2025-10-29 | v1.1.2.0 | v3.0.2 | v5.5.2, v6.2.1 | v1.0.7 | v5.5.10 | v3.5.16 | • A compatible **NVIDIA display driver (version ≥ 570.65)** is required |
| 2025-12-15 | v1.2.0.4 | v3.1.0 | v5.5.2, v6.2.1 or higher | v1.0.7, v1.5.0 or higher | v5.5.11.4 | v3.5.20.6 or higher | • Clever One v1.5.0 이상 부터 DTKS v1.2.0 이상에서만 사용 가능<br>• DTKS에 3rdParty 연동 기능 포함(Byzz) |
| 2026-02-20 | v1.2.1.1 | v3.2.1 | v5.5.2, v6.2.1 or higher | v1.0.7, v1.5.0 or higher | v5.5.12.3 | v3.5.20.7 | • EAI Engine의 License Deactivaion 주요 이슈 개선버전 (US 대응) |
| 2026-03-24 | v1.2.2.0 | v3.2.3 | v5.5.2, v6.2.1 or higher | v1.0.7, v1.5.0 or higher | v5.5.12.3 | v3.5.20.7 | • Green X 21 의 12 X 5(FOV) CT 파일 Segmentation 실패 오류 개선 |
| ~~2026-04-13~~<br>~~(출시전, 공급날짜)~~<br>• **최종 출시 안함** | (TBD) | v3.2.4 | v5.5.2, v6.2.1 or higher | v1.0.7, v1.5.0 or higher | v5.5.12.3 | v3.5.20.7 | • EAI Engine이 License Deativation 되는 증상원인을 확인하기 위해서 별도의 Cryptlex의 Log를 기록하는 버전<br>　◦ Log: C:\ProgramData\LexLog.txt<br>• 미출시 버전으로 출시 여부 결정 후 진행 예정 |
| 2026-07-06 | v1.2.3.2 | v3.3.0 | v5.5.2, v6.2.1 or higher | v1.0.7, v1.0.8, v1.0.9<br>v1.5.0, v1.5.1 or higher | v5.5.12.3(TBD) | v3.5.20.7(TBD) | • EAI Engine v3.3.0 에서 License Deactivation 문제 해결 (Cryptlex 내부 오류 개선 적용)<br>• Engine의 "Smart App Control" 환경에서 사용 개선<br>• Engine의 다중 호출 방지<br>• DTKS의 안정화 작업 개선<br>• DTKS의 유동 IP환경에서 IP재설정 기능 추가 |
