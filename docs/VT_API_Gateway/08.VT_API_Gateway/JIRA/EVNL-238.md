# 일부 클리닉에서 Clinic ID가 변경되는 문제

## Description

**Background**

- It has been reported that the clinic ID registered in the LMP and the ID confirmed in the EzServer WebConsole (License Manager) are different due to the automatic change of Clinic ID in some clinics.
    - **https://vts.vatech.com/browse/EZSV-1213**
    - Malaysia, Mexico, etc.
- Situation
    - Case1
        - Clinic Information
            - TBD
        - EzServer log analysis results (Reported from Malaysia on 12/12)
            - Clinic ID - dc559b5b94854dbaaad5926a9f456feb and usbSN-2206-00234, machineSN-061-008446 was registered to EzServer before 2022-Nov-16
            - No action til 2022-12-11
                - License were working
            - Tried to Acitvate/Deactivate/Sync license from Web console and failed
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-11 16:16:40"}
                - {"message":"GET /licenses via LMP API with param: clinicId-dc559b5b94854dbaaad5926a9f456feb","level":"debug","timestamp":"2022-12-11 16:17:02"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-11 16:18:31"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-11 16:18:40"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-11 17:38:59"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-11 17:39:02"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 10:08:33"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 10:08:41"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 10:24:46"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 10:46:16"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 12:23:46"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 12:23:52"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 12:26:57"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 12:29:11"}
                - {"message":"Get LMP license via lmp API from POST /acts.","level":"info","timestamp":"2022-12-12 13:28:30"}
            - Tried to register usb S/N and failed
                - {"message":"parameter used: lmpLicenseKey-, usbSN-2206-00234, machineSN-061-008446, clinicId-dc559b5b94854dbaaad5926a9f456feb","level":"debug","timestamp":"2022-12-12 13:32:46"
            - Tried to change Clinic ID to c21c048d20d25398f7f618a54dbb0e7a and failed
                - {"message":"POST /clinicsforid is requested for clinic id - c21c048d20d25398f7f618a54dbb0e7a.","level":"info","timestamp":"2022-12-12 13:49:50"}
        - Case1 log에 대한 Clinic 상황 확인 결과
            - Clinic situation check result for Case1 log
                - In the LMP, the Clinic ID was looked up as c21c048d20d25398f7f618a54dbb0e7a, but the Clinic ID of the Clinic PC was different. So They tried to change it to c21c048d20d25398f7f618a54dbb0e7a, but it was not changed.
                - Clinic users or corporate CS managers have never tried to change the Clinic ID, but it was changed to a Clinic ID (dc559b5b94854dbaaad5926a9f456feb) other than c21c048d20d25398f7f618a54dbb0e7a, which is looked up in LMP.
        - EzServer, License Manager confirmation result for Case 1 situation (ES)
            - Clinic ID cannot be changed in EzServer's License Manager.
            - It was confirmed that the operation in the log is normal and not an issue in the EzServer program
        - LMP Verification Results for Case 1 Situation (EVN)
            - The Clinic ID on the LMP must not change.
            - However, when checking the current code, if the changed Clinic ID is passed over when syncing with VCSM, it is supposed to be changed to the corresponding Clinic ID value.
            - This content needs correction.
- Additional confirmation required
    - For Case 1 Clinic, it is necessary to check whether a situation in which the Clinic ID is changed in VCSM has occurred. (IT Solution Team VCSM Manager)
    - It is necessary to confirm whether the change of the Clinic ID of Case 1 Clinic occurred in VCSM, and if so, why it occurred.

**Purpose**

- Check the reason why the Clinic ID was changed in a specific Clinic.
- Measures are taken to prevent situations in which the Clinic ID automatically changes.

**Process**

1. Check the cause of Clinic ID change
2. Measures to prevent Clinic ID from changing (LMP, VCSM)

**Considerable Factors**

- 이 내용은 복수의 Clinic에서 발생했다. 정확한 원인 파악을 위해 해당 Clinic들의 정보를 담당자에게 추가 확인하여 Description에 반영한다.
- Test Procedure (~~EVNL-239~~)
    - **Precondition**
        - EzServer 설치 (v5.2)
        - EzDent-i 설치
    - **Reproduction steps**
        1. EzServer License Manager에서 LMP Production USB SN/Machine SN를 등록하여 라이선스를 활성화한다.
            1. Clinic id 생성, Clinic 정보가 LMP에 등록됨
            2. EzServer License Manager에 등록된 Clinic ID 확인 후 기록
        2. VCSM에서 등록된 Clinic의 Clinic Information을 수정한다.
            1. Clinic name, address, phone number 등 무엇이든 상관없음
        3. LMP Production 환경 접속하여 Clinic list에서 2를 수행한 날짜를 선택하여 sync 버튼을 누른다.
    - **Expected Result**
        - 2에서 변경한 Clinic Information이 LMP에 동기화된다.
        - EzServer License Manager의 Clinic ID가 1-b에서 기록한 것과 동일하다.
        - EzDent-i를 실행했을 때 USB SN/Machine SN로 등록한 Floating License가 정상 등록되어 있다.
    - **Actual Result**
        - 2에서 변경한 Clinic Information이 LMP에 동기화된다.
        - EzServer License Manager의 라이선스 상태에 -110799 error code가 출력된다.
        - EzDent-i를 실행했을 때 USB SN/Machine SN로 등록한 Floating License가 정상 동작하지 않는다.
            - Trial로 작동한다.
        - LMP에서 USB SN/Machine SN를 조회하면 출력되는 Clinic ID가 1-b에서 기록한 것과 달라졌다.
    - **Notes**
        - Reproduction step의 2 과정은 VCSM ES에서 수행할 수 없으므로 VCSM 권한을 가진 Johnny에게 요청하여 진행한다.
        - Reproduction step의 3번은 LMP Production 환경 권한을 가지고 있는 Claire, Johnny에게 요청하여 진행한다.

**Result Image**

- The reason why the Clinic ID was changed in a specific Clinic was confirmed.
- Measures have been taken to prevent situations in which the Clinic ID automatically changes.