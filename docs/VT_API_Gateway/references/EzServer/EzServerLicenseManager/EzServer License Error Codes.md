# New error codes

| 01 | License | VERR_LICENSE_KEYEXPIRED | -110701 | "License key has expired" | When activating expired license key without sync. | 1. Activate license key
2. Wait till it expires
3. Click Sync.
4. Click Activate. |
| --- | --- | --- | --- | --- | --- | --- |
| 02 | License | VERR_LICENSE_NOT_FOUND | -110709 | "Please enter a valid serial number." | When license key is existing in LMP. | 1. Click "Add" button
2. Select license key and click "Next" button
3. Type any invalid string(ex. 123)
4. Click "Next" button. |
| 03 | License | VERR_LICENSE_MACHINE_FINGERPRINT | -110712 | "Machine fingerprint has changed since activation." | LA_E_MACHINE_FINGERPRINT(63) | N/A |
| 04 | License | VERR_LICENSE_STATUS_INVALID | -110713 | "Invalid license status.Please synchronize the license information then retry." | It occurs when activating license whose status is not "created".
Reference: LM-LMP-100 | Case 1.
Try to activate to "Expired" license.
Case 2.
Try to activate a license that already activated. |
| 05 | License | VERR_LICENSE_INVALID_CLINIC_ID | -110714 | "Invalid clinic ID." | When failed to update clinic information due to invalid clinic ID. | 1. Click "Change" button
2. Type any invalid string
3. Clik "Save" |
| 06 | License | VERR_LICENSE_FAILED_UPDATE_CLINIC | -110715 | "Failed to update clinic information." | When failed to update clinic information due to unknown reason. | 1. Set Clinic ID to empty string from DB.
2. Click "Add" button from License Panel.
3. Select "license key" and click "next".
4. Use any license key from LMP and click "next"
5. Input invalid data for clinic info.
6. Click "next" |
| 07 | License | VERR_LICENSE_ACTIVATION_FAILURE_REVOKED_LICENSE | -110716 | "A revoked license cannot be activated." | LA_E_REVOKED(53) | N/A |
| 08 | License | VERR_LICENSE_COUNTRY_NOT_ALLOWED | -110717 | "Country is not allowed." | LA_E_COUNTRY(81) | N/A |
| 09 | License | VERR_LICENSE_REACHED_ACTIVATION_LIMIT | -110718 | "The activation limit has been exceeded." | LA_E_ACTIVATION_LIMIT(58) | N/A |
| 10 | License | VERR_LICENSE_REACHED_DEACTIVATION_LIMIT | -110719 | "The deactivation limit has been exceeded." | LA_E_DEACTIVATION_LIMIT(60) | 1. Activate license from Web Console.
2. Check license status is changed to Activated in LMP
3. Deactivate license from Web Console.
4. Check license status is changed to Deactivated in LMP
5. repeat step 1. ~ step 4. till it reaches deactivation limit. |
| 11 | License | VERR_LICENSE_SYSTEM_TIME_TAMPERED | -110720 | "Failed to activate due to system time tampered." | LA_E_TIME_MODIFIED(69) | N/A |
| 12 | License | VERR_LICENSE_FLOAT_SERVER_ALREADY_ACTIVATED | -110721 | "A floating server has been already activated for the same product." | When tried to activate new floating license server for the same product. | N/A |
| 13 | License | VERR_LICENSE_SYNC_ERROR | -110722 | "An error has occurred while synchronizing data." | Error(s) occurred while syncing. | 1. Activate Node Locked license from Desktop app.
2. wait about 1 minute.
3. Go to Web Console.
4. Click sync for that license.
5. Error code could be displayed otherwise no error message.
6. wait about 30 minutes
7. Click sync for that license
8. Sync should succeed |
| 14 | License | VERR_LICENSE_DUPLICATED_PRODUCT | -110723 | "A license has been already activated for the same product." | Duplicated license for the same product which applied to floating licenses for desktop apps and web apps and node-locked licenses for web apps. | 1. Activate Floating license from Web Console.
2. Create Floating license key for the same product.
3. Add created license key from Web Console. |
| 15 | License | VERR_LICENSE_UNKNOWN | -110799 | "An unknown license error has occurred." | Unknown/Unhandled License Manager error. | N/A |
| 16 | LexFloatServer | VERR_LICENSE_LEXFLOATSERVER_ERROR | -110761 | "Unknown LexFloatServer error." | Unknown/Unhandled LexFloatServer error. | N/A |
| 17 | LexFloatServer | VERR_LICENSE_LEXFLOATSERVER_NOT_RESPONDING | -110762 | "LexFloatServer is not responding." | LexFloatServer is not responding. | N/A |
| 18 | LexActivator | VERR_LICENSE_LEXACTIVATOR_ERROR | -110765 | "Unknown LexActivator error." | Unknown/Unhandled LexActivator error. | N/A |
| 19 | LexActivator | VERR_LICENSE_LEXACTIVATOR_NOT_RESPONDING | -110766 | "LexActivator is not responding." | LexActivator is not responding. | N/A |
| 20 | LMP | VERR_LICENSE_LMP_NOT_RESPONDING | -110772 | "LMP is not responding." | LMP is not responding. | N/A |
| 21 | LMP | VERR_LICENSE_PORTAL_ERROR | -110771 | "An error has occurred in License Management Portal." | LMP returns error | 1. Go to License.
2. Click "Sync" button. |
| 22 | LexActivator, LexFloatServer | VERR_LICENSE_KEYEXPIRED | -110701 | "The license is expired." | Tried to activate with expired license. | TBD |

# Existing error codes in VTError.h

```
// License -110700 ~ -110799
  VTERROR_REGISTER(VERR_LICENSE_NOKEY,                                 -110700,  "Required key not available")
//VTERROR_REGISTER(VERR_LICENSE_KEYEXPIRED,                            -110701,  "Key has expired")
//VTERROR_REGISTER(VERR_LICENSE_KEYREVOKED,                            -110702,  "Key has been revoked")
//VTERROR_REGISTER(VERR_LICENSE_KEYREJECTED,                           -110703,  "Key was rejected by service")
// LicenseManager
  VTERROR_REGISTER(VERR_LICENSE_CLINIC_NOT_FOUND,                      -110704,  "Unable to find clinic information.")
  VTERROR_REGISTER(VERR_LICENSE_NOT_ACTIVATED,                         -110705,  "License not activated.")
  VTERROR_REGISTER(VERR_LICENSE_NOT_DEACTIVATED,                       -110706,  "License not deactivated.")
  VTERROR_REGISTER(VERR_LICENSE_PACKAGE_INVALID,                       -110707,  "Invalid license package.")
  VTERROR_REGISTER(VERR_LICENSE_PACKAGE_NOT_FOUND,                     -110708,  "Unable to find a license package.")
  VTERROR_REGISTER(VERR_LICENSE_NOT_FOUND,                             -110709,  "Unable to find a license.")
  VTERROR_REGISTER(VERR_LICENSE_FAIL_TO_RENEW,                         -110710,  "Failed to renew the license.")
  VTERROR_REGISTER(VERR_LICENSE_FAIL_TO_DROP,                          -110711,  "Failed to drop the license.")
  VTERROR_REGISTER(VERR_LICENSE_MANAGER_ERROR,                         -110751,  "An error has occurred in License Manager.")
// License Management Portal
  VTERROR_REGISTER(VERR_LICENSE_PORTAL_ERROR,                          -110771,  "An error has occurred in License Management Portal.")
  VTERROR_REGISTER(VERR_LICENSE_UNKNOWN,                               -110799,  "An unknown license error has occurred.")
```

# Details

## VERR_LICENSE_NOT_ACTIVATED

- Unknown activation fail.

```
[2021-04-30 09:33:24] Error: License not activated! Please activate the license using a license key. Error code: 1
```

## VERR_LICENSE_LEXFLOATSERVER_SYSTEM_TIME_TAMPERED

- Tried to start lexfloatserver after system time changed.

```
 /*
 CODE: LA_E_TIME_MODIFIED

 MESSAGE: The system time has been tampered (backdated).
 */
 LA_E_TIME_MODIFIED = 69,
```

```
[2021-03-01 11:43:40] Error: License not activated! Please activate the license using a license key. Error code: 69
[2021-03-01 11:43:40] Info: Starting floating license server...
[2021-03-01 11:43:41] Info: Listening on port: 44405
[2021-03-01 11:43:41] Info: Total number of available floating licenses: 0
```

```
[2021-04-27 17:25:27] Info: Request failed! HTTP status code: 500 Error code: SERVER_TIME_MODIFIED
```

## VERR_LICENSE_LEXFLOATSERVER_ERROR

- When total number of licenses are not matched between LMP and Cryptlex(LexFloatServer)
- It should NOT be happened.

## VERR_LICENSE_LEXFLOATSERVER_ERROR

- When execute LexFloatServer with relative path of config/data file.
- It should NOT be happened.

```
[2021-04-30 09:33:24] Error: Service is already installed!
```

## VERR_LICENSE_ACTIVATION_FAILURE_REVOKED_LICENSE

- Tried to activate deactivated(revoked in cryptlex) license.

```
/*
 CODE: LA_E_REVOKED

 MESSAGE: The license has been revoked.
 */
 LA_E_REVOKED = 53,
```

### **case1**

```
[2021-04-29 17:12:02] Info: Starting service...
[2021-04-29 17:12:02] Info: Service has been started successfully!
[2021-04-29 17:12:04] Error: License activation failed: 53
```

### **case2**

```
[2021-04-30 09:33:24] Info: Starting service...
[2021-04-30 09:33:24] Error: Service is already running!
[2021-04-30 09:33:25] Error: License activation failed: 53
```

## VERR_LICENSE_LEXFLOATSERVER_ERROR

- Unknown/Unhandeld/Unexpected LexFloatServer error.
- Tried to run LexFlaotServer non-admin user account.
- It should NOT be happened.

```
[2021-04-21 11:46:29] Error: Access denied! Make sure you have admin rights. Error code: 44
```

## VERR_LICENSE_NOT_ACTIVATED

- Unknown error on actiation

```
(TBD)
```

## VERR_LICENSE_NOT_DEACTIVATED

- Unknown error on deactivation

```
[2021-04-30 10:20:30] Error: License deactivation failed! Error code: 1
```

## VERR_LICENSE_PORTAL_ERROR

- Unkonwn LMP error

## VERR_LICENSE_KEYEXPIRED

- license expired
- LA_EXPIRED(20)

## VERR_LICENSE_PACKAGE_INVALID

- LMP error message: "license_package_invalid"
- VCSM does not response or verified false, Error status 404 with message

## VERR_LICENSE_PACKAGE_NOT_FOUND

- LMP error message: "license_package_not_found"
- No license package found in LMP corresponding USB SN, Error 404 with message

## VERR_LICENSE_NOT_FOUND

- LMP error message: "license_not_found"
- No available Licenses found with in license package, Error 404 with message.
- No license found in LMP corresponding license key, Error 404 with message.

## VERR_LICENSE_STATUS_INVALID

- LMP error message: "license_status_invalid"
- If license status is not "created" Error 404 with message

## VERR_LICENSE_INVALID_CLINIC_ID

- LMP error message: "invalid_clinic_id"
- No clinic_id or clinic_id length is not 32, error status 404 with message.
- Not found clinic in LMP by clinic_id, error 404 with message.

# Links

- VTError
- Cryptlex Error Code: Cryptlex error code