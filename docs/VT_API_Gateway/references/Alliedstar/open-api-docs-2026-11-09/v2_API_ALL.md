# API List
## Patient

### Get Patients List by Page

Developers can use this interface to obtain patients list

- **Request URL:**

`POST open/patient/listPatients`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters:**

| Parameter   | Description                                                                         | Type   | Required | Example                      |
|-------------|-------------------------------------------------------------------------------------|--------|----------|------------------------------|
| openid      | openid obtained from user authorization                                             | String | Yes      | WmizQAMXoG1z8CcpTdMG0-4tLJ17 |
| patientName | patient name(fuzzy search)                                                          | String | No       | John                         |
| patientId   | patient id                                                            | String | No       | FC                           |
| startTime   | time range query </p>filter out users created **after** this time </p> (timestamp)  | String | No       | 1666660440000                |
| endTime     | time range query </p>filter out users created **before** this time </p> (timestamp) | String | No       | 1666660450000                |
| pageNumber  | number of pages                                                                     | String | No       | 1                            |
| pageSize    | page sizedefault is 10maximum is 100                                                | String | No       | 10                           |

- **Response Parameters:**

| Parameter          | Description                                     | Type         | Example                         |
| ------------------ | ----------------------------------------------- | ------------ | ------------------------------- |
| msg                | result description                              | String       | OK                              |
| code               | Response code                                   | int          | 200 (for successful processing) |
| total              | total recordes                                  | Long         | 100                             |
| data               | business data                                   | Object Array |                                 |
| data ->patientId   | unique patient id                               | String       | FC23092008053615616             |
| data ->patientName | patient name                                    | String       | John Lee                        |
| data ->gendar      | gendar<br/>0: unknown<br/>1: male<br/>2: female | Integer      | 1                               |
| data ->birthDate   | birth date<br/>(ISO8601: yyyy-MM-dd)            | String       | 1988-05-11                      |
| data ->phoneNum    | phone number                                    | String       | 1234567                         |
| data ->email       | e-mail                                          | String       | john.lee@gmail.com              |
| data ->remark      | remark                                          | String       | Some remark                     |
| data->updateTime   | Update time                                     | Date         |                                 |



- **Response code**

| Code | Description           |
|------|-----------------------|
| 200  | Success               |
| 400  | Invalid Request       |
| 1002 | Sorry, access denied. |

- **Response Example**

```json
{
  "code":200,
  "msg":"OK",
  "total":8761,
  "sysTime":"2025-04-11 13:44:01",
  "data":[
    {
      "patientId":"PI00008924",
      "patientName":"Lily Pound",
      "gendar":0,
      "birthDate":null,
      "phoneNum":null,
      "email":null,
      "remark":null,
      "updateTime":"2025-04-11T11:31:20.000+08:00"
    },
    {
      "patientId":"3253",
      "patientName":"Lily Pound",
      "gendar":1,
      "birthDate":null,
      "phoneNum":null,
      "email":null,
      "remark":null,
      "updateTime":"2025-04-11T10:40:34.000+08:00"
    },
    {
      "patientId":"PI00008920",
      "patientName":"Mike",
      "gendar":0,
      "birthDate":null,
      "phoneNum":null,
      "email":null,
      "remark":null,
      "updateTime":"2025-04-09T16:09:02.000+08:00"
    }
  ]
}
```



### Create New Patient

Developers can use this API to create patient information.

- **Request URL：**

`POST open/patient/createPatient`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters：**

| Parameter   | Parameter Name                | Type   | Required | Description                                                  | Example                      |
| ----------- | ----------------------------- | ------ | -------- | ------------------------------------------------------------ | ---------------------------- |
| openid      | User Authorization Binding ID | String | Yes      | openid obtained after user authorization                     | WmizQAMXoG1z8CcpTdMG0-4tLJ17 |
| patientId   | Patient ID                    | String | Yes      | Patient ID with a maximum length of 200                      | Example: P202300456789       |
| patientName | Patient Name                  | String | Yes      | Patient name with a maximum length of 100                    | Anthony                      |
| gender      | Gender                        | String | No       | gender<br/>0: Unknown<br/>1: Male<br/>2: Female<br/>3: Other | 1                            |
| birthDate   | Birth Date                    | String | No       | birth date<br/>(ISO8601: yyyy-MM-dd)                         | 1988-05-11                   |
| phoneNum    | Phone Number                  | String | No       | phone number<br/>Regex: ^[-0-9]{3,16}$                       | 1234567                      |
| email       | E-mail                        | String | No       | e-mail<br/>Regex: ^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$ | john.lee@gmail.com           |
| remark      | Remark                        | String | No       | remark                                                       | Some remark                  |




-  **Response Parameters:**

| Parameter           | Parameter Name     | Type   | Example                                                      |
| ------------------- | ------------------ | ------ | ------------------------------------------------------------ |
| msg                 | Result Description | string | OK                                                           |
| code                | Response Code      | int    | 200 (success)                                                |
| data                | Response Data      | object |                                                              |
| data-> patientId    | Patient ID         | string | P202300456789                                                |
| data-> targetUri    | Redirect Link      | string | https://test.allied-star.com/XXXX                            |
| data-> commandParam | Command Parameter  | string | openasconnect://eyJjYWxsZXIiOiJ3ZWJEUE1TIiwic2lnbiI6ImUxMDhMGM5ZjQ2FhZjI4In0= |



- **Response code**

| Code | Description           |
| ---- | --------------------- |
| 200  | Success               |
| 400  | Invalid Request       |
| 502  | Request data is empty |
| 1008 | User does not exist   |



### Refresh Command

Developers can use this API to refresh the patient jump commands. 

- **Request URL：**

`POST open/patient/refreshCommand`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters：**

| Parameter | Parameter Name                | Type   | Required | Description                              | Example                      |
| --------- | ----------------------------- | ------ | -------- | ---------------------------------------- | ---------------------------- |
| openid    | User Authorization Binding ID | String | Yes      | openid obtained after user authorization | WmizQAMXoG1z8CcpTdMG0-4tLJ17 |
| patientId | Patient ID                    | String | Yes      | patient id                               | Example: P202300456789       |




-  **Response Parameters:**

| Parameter           | Parameter Name     | Type   | Example                                                      |
| ------------------- | ------------------ | ------ | ------------------------------------------------------------ |
| msg                 | Result Description | string | OK                                                           |
| code                | Response Code      | int    | 200 (success)                                                |
| data                | Response Data      | object |                                                              |
| data-> patientId    | Patient ID         | string | P202300456789                                                |
| data-> targetUri    | Redirect Link      | string | https://test.allied-star.com/XXXX                            |
| data-> commandParam | Command Parameter  | string | openasconnect://eyJjYWxsZXIiOiJ3ZWJEUE1TIiwic2lnbiI6ImUxMDhMGM5ZjQ2FhZjI4In0= |



- **Response code**

| Code | Description           |
| ---- | --------------------- |
| 200  | Success               |
| 400  | Invalid Request       |
| 502  | Request data is empty |
| 1008 | User does not exist   |



## Case

### Create New Case

- **Request URL：**

`POST open/order/createCase`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters：**

| Parameter        | Parameter Name      | Type   | Required | Description                                            | Example                                                                                          |
| ---------------- | ------------------- | ------ | -------- | ------------------------------------------------------ |--------------------------------------------------------------------------------------------------|
| externalCaseCode | Developer Case Code | String | Yes      | Developer-defined case code with a maximum length of 100 | 2015101400446982                                                                                 |
| caseName         | Case Name           | String | Yes      | Case name with a maximum length of 200                 | Example: Film Case Analysis                                                                      |
| openid           | User Authorization Binding ID | String | Yes      | openid obtained after user authorization              | WmizQAMXoG1z8CcpTdMG0-4tLJ17                                                                     |
| externalPatientCode | Developer Platform Unique Patient Identifier | String | Yes | Developer-defined unique patient identifier with a maximum length of 200 | Example: P202300456789                                                                           |
| patientName      | Patient Name        | String | Yes      | Patient name with a maximum length of 100, encrypted and stored by Alliedstar | Alexandra Blackwood                                                                              |
| birthDate        | Patient Birth Date  | String | No       | Patient's birth date in YYYY-MM-DD format              | 2022-11-16                                                                                       |
| gender           | Patient Gender      | String | No       | Patient gender, options: "male" or "female"           | male                                                                                             |
| caseTreatments | Case Treatements | String | No | Case Treatements | [{"number":"12","clinicalType":0,"workType":"Crown","ageType":0,"implantType":"CustomAbutment"}]<br>[{"clinicalType":0,"ageType":0,"toothSource":"ImplantUpperJaw","isAllOnX":true}] |
| caseTreatments -> clinicalType | Clinical Type  | Integer | true     | Clinical Type  (0: Restoration, 1: Orthodontic, 2: Other) | 0                                                                                                |
| caseTreatments -> number | Tooth Position | String  | false    | Tooth Position                                            | 12                                                                                               |
| caseTreatments -> ageType | Age Type       | Integer | false    | Age Type (0: Adult, 1: Child)                             | 0                                                                                                |
| caseTreatments -> workType | Work Type      | String  | false    | Work Type（Please refer to the CaseTreatementsWorkTypeEnum enumeration） | Crown                                                                                            |
| caseTreatments -> implantType | Implant Type   | String  | false    | Implant Type（StockAbutment、CustomAbutment、None）       | CustomAbutment                                                                                   |
| caseTreatments ->  toothSource | Implant Quick Selection | String | false | Implant Quick Selection<br>（ImplantUpperJaw、ImplantLowerJaw、ImplantFullJaw) | ImplantUpperJaw |
| caseTreatments ->  isAllOnX | All On X （Full Arch） | Boolean | false | All On X （Full Arch） | true |



**All On X**

To use the All On X (Full Arch) function, please refer to the caseTreatments example below and place toothSource and isAllOnX at the beginning of the collection.

```json
[
    {
        "clinicalType": 0,
        "ageType": 0,
		"toothSource": "ImplantUpperJaw",
		"isAllOnX" : true
    }
]
```




-  **Response Parameters:**

| Parameter    | Parameter Name     | Type   | Example |
| -------------| ------------------ | ------ | ------- |
| msg          | Result Description | string | OK      |
| code         | Response Code | int    | 200 (success) |
| data         | Response Data      | object |         |
| data-> caseCode | AS Case Code    | string | 2015101400446982 |
| data-> targetUri | Redirect Link   | string | https://test.allied-star.com/XXXX |
| data-> commandParam | Command Parameter | string | openasconnect://eyJjYWxsZXIiOiJ3ZWJEUE1TIiwic2lnbiI6ImUxMDhkNDk4MDk4MDQ4MGM5ZjQ2NTRmNzU2YWFhZjI4In0= |

**Note:**

The corresponding registry location for ASConnect is  `HKEY_LOCAL_MACHINE\SOFTWARE\Classes\openASConnect`, with the value name is  `URL Protocol`.

- **Response Codes**

| Code | Description                          |
| ---- | ------------------------------------ |
| 200  | Success                              |
| 400  | Invalid Request                      |
| 500  | Internal Exception                   |
| 501  | Operation Frequent, Please Retry Later |
| 2025 | Current User Not Authorized           |

**Note:**

The `open/order/createCase` in the request URL represents the interface for developers to create a new case.


### Refresh Command

Developers can use this API to refresh the case jump command.



- **Request URL：**

`POST /open/v3/case/refreshCommand`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters：**

| Parameter        | Parameter Name      | Type   | Required | Description                                            | Example                  |
| ---------------- | ------------------- | ------ | -------- | ------------------------------------------------------ | ------------------------ |
| caseCode     | AS Case Code | string | Yes      | AS Case Code     | 21080500017918484864 |
| openid           | User Authorization Binding ID | string | Yes      | openid obtained after user authorization              | WmizQAM1z8CcpTdMG0-4tLJ17 |

-  **Response Parameters:**

| Parameter    | Parameter Name     | Type   | Example |
| -------------| ------------------ | ------ | ------- |
| msg          | Result Description | string | OK      |
| code         | Response Code | int    | 200 (success) |
| data         | Response Data      | object |         |
| data-> caseCode | AS Case Code    | string | 2015101400446982 |
| data-> targetUri | Redirect Link   | string | https://test.allied-star.com/XXXX |
| data-> commandParam | Command Parameter | string | openasconnect://eyJjYWxsZXIiOiJ3ZWJEUE1TIiwic2lnbiI6ImUxMDhkNDk4MDk4MDQ4MGM5ZjQ2NTRmNzU2YWFhZjI4In0= |



- **Response Codes**

| Code | Description                          |
| ---- | ------------------------------------ |
| 200  | Success                              |
| 400  | Invalid Request                      |
| 403 | Sorry, access denied |
| 500  | Internal Exception                   |
| 501  | Operation Frequent, Please Retry Later |
| 502 | Request data is empty |
| 2025 | Current User Not Authorized           |






### Get Case Detail

After the scan is completed, developers can use this interface to get the scan results.

-  **Request URL：**

`POST open/order/getCaseDetail`

`Content-Type: application/x-www-form-urlencoded`

-  **Request Parameters：**

| Parameter | Parameter Name | Type   | Required | Description                                      | Example          |
| --------- | -------------- | ------ | -------- | ------------------------------------------------ | ---------------- |
| caseCode  | AS Case Code   | String | Yes      | Used to query order details on the Open Platform | 2015101400446982 |

-  **Response Parameters:**

| Parameter                  | Parameter Name                         | Description                                                                                                                                                                             | Type    | Example                                                      |
| -------------------------- | -------------------------------------- |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------- | ------------------------------------------------------------ |
| msg                        | Result Description                     | Result description                                                                                                                                                                      | String  | OK                                                           |
| code                       | Response Code             | Response code                                                                                                                                                                           | int     | 200 (for successful processing)                              |
| data                       | Returned Data                          | Returned data                                                                                                                                                                           | object  | object                                                       |
| data->caseCode             | AS Case Code                           | AS case code                                                                                                                                                                            | String  | 2015101400446982                                             |
| data->caseName | AS Case Name | AS Case Name | String | Alexandra Blackwood's case |
| data->externalCaseCode     | Developer Case Code                    | Developer case code                                                                                                                                                                     | String  | 21080500017918484864                                         |
| data->serialNumber         | Scanner series number                  | Scanner series number                                                                                                                                                                   | String  | EM310                                                        |
| data->caseStatus           | Case Status                            | Case status (0: Registered, 1: To be processed, 2: Scan completed, 3: Uploaded, 4: Ordered, 5: Completed)                                                                               | Integer | 3                                                            |
| data->scanTime             | Scan Time                              | Scan time (time when the CASE scan is completed)                                                                                                                                        | long    | 1665975588000                                                |
| data->orderTime            | Order Time                             | Order time (time when the order is sent to the dental laboratory)                                                                                                                       | long    | 1665975588000                                                |
| data->userOpenid           | Current User OpenID                    | Unique identifier of the current user<br/>(openid: the unique identifier of the user on the developer platform corresponding to the AS platform user)                                   | String  | rjpIUmubkUsw7YKrJMAl4xQvcsdh                                 |
| data->userEmail            | Current User Email                     | Email of the current user                                                                                                                                                               | String  | Alexandra.Blackwood@gmail.com                 |
| data->userPhone            | Current User Phone Number              | Phone number of the current user                                                                                                                                                        | String  | 13766668888                                                  |
| data->patientId            | Developer Platform Patient ID          | Unique identifier of the patient in the developer platform                                                                                                                              | String  | FC2021040613041460433                                        |
| data->patientName          | Patient Name                           | Name of the patient                                                                                                                                                                     | String  | Alexandra Blackwood                                     |
| data->patientMemo          | Patient Memo                           | Patient memo                                                                                                                                                                            | String  | Patient memo                                                 |
| data->toothNumberingSystem | Tooth Numbering System (fdi;universal) | Tooth numbering system (fdi;universal)                                                                                                                                                  | String  | fdi                                                          |
| data->reqDeliveryDate      | Requested Delivery Date                | Requested delivery date (timestamp)                                                                                                                                                     | long    | 1666660440000                                                |
| data->comment              | Comment                                | Comment<br/>(Note provided by the clinic when sending the order to the dental laboratory)                                                                                               | String  | Comment                                                      |
| data->audioComment         | Audio Comment                          | Audio comment                                                                                                                                                                           | array   | [<br/>"https://images-en.allied-star.com/order/230419438412345678/audio/voice_memo1.wav"<br/>] |
| data->thumbnailUrl | Thumbnail | Thumbnail | String | https://images-en.allied-star.com/order/230419438412345678/model/private/thumbnail.png |
|  data->labUnionId  |  Lab's unionId  | Lab's unionId                                                                                                                                                                           | String ||
|  data->userName  |  Doctor's name  | Doctor's name                                                                                                                                                                           | String ||
|  data->clinicId  |  Clinic's ID  | Clinic's ID                                                                                                                                                                             | String ||
|  data->attachments  |  Attachments  | Attachments information:<br/>1. 2D and 3D files generated by AS scanner;<br/>2. Other attachments uploaded by the user;<br/>3. 2D and 3D files generated by applications in AS Connect. |  array  |  \[ { "category": "marginLine", "fileCode": "F2305151601260738381004805", "fileFormat": "a3d", "fileName": "lower\_margin\_line.a3d", "lastModifiedTime":1666660440000 "url": "" } \]  |
|  data->attachments->category  |  File Category  | File category ([CategoryEnum](files/v2_API_ALL.md#CategoryEnum))                                                                                                |  String  |  marginLine  |
|  data->attachments->fileCode  |  File Code  | File code (unique identifier of the file)                                                                                                                                               |  String  |  F2210260815931942401  |
|  data->attachments->fileFormat  |  File Format  | File format<br/>(stl, ply, jpg, jpeg, image/jpeg, image/png, image/gif, etc.)                                                                                                           |  String  |  ply  |
|  data->attachments->fileName  |  File Name  | File name                                                                                                                                                                               |  String  |  upper.ply  |
|  data->attachments->url  |  Storage Path  | Storage path of the file in the cloud object storage                                                                                                                                    |  String  |  [https://images.allied-star.com.com/order/221023377606746801152/io\_image/image\_1.jpg](https://images.allied-star.com.com/order/221023377606746801152/io_image/image_1.jpg)  |
|  data->attachments->lastModifiedTime  |  Last Modified Time  | Last modified time of the file (timestamp)                                                                                                                                              |  Long  |  1666660440000  |
| data->treatments                    | Treatment Details                                            | Treatment details                                                | array   |  |
| data->treatments->clinicalType          | Clinical Type     | Clinical type (0: Restoration, 1: Orthodontic, 2: Other)     | Integer | 0                         |
| data->treatments->ageType               | Age Type          | Age type (0: Adult, 1: Child)                                | Integer | 0                         |
| data->treatments->workType              | Work Type         | Work type                                                    | String  | Crown                     |
| data->treatments->jawType               | Jaw Type          | Jaw type（1:Upper Jaw；2:Lower Jaw；3:Upper Jaw And Lower Jaw） | Integer | 1                         |
| data->treatments->toothSource           | Tooth Source      | Tooth source                                                 | String  | ImplantUpperJaw           |
| data->treatments->scanbodyType          | Scanbody Type     | Scanbody type (0: None, 1: Alliedstar, 2: Tektonik, 3: Medentika, 99: Other) | Integer | 0                         |
| data->treatments->isAllOnX              | All-on-X          | Full-arch implant (0: false, 1: true)                        | Integer | 0                         |
| data->treatments->number                | Tooth Position    | Tooth position                                               | String  | 28                        |
| data->treatments->implantType           | Implant Type      | Implant type                                                 | String  | CustomAbutment            |
| data->treatments->scanPreOp             | Scan Pre-op       | Scan pre-operation (0: false, 1: true)                       | Integer | 0                         |
| data->treatments->mesialConnected       | Mesial Connected  | Mesial connection (0: false, 1: true)                        | Integer | 0                         |
| data->treatments->inlayCore             | Inlay Core        | Inlay core (0: false, 1: true)                               | Integer | 0                         |
| data->treatments->material              | Material          | Material                                                     | String  | PMMA                      |
| data->treatments->abutmentMaterial      | Abutment Material | Abutment material                                            | String  | Zirconia                  |
| data->treatments->shadeGuide            | Shade Guide       | Shade guide                                                  | String  | VitaClassic               |
| data->treatments->shade                 | Shade             | Shade (code)                                                 | String  | D3                        |
| data->treatments->implantKit | Implant Kit | Implant Kit | object |  |
| data->treatments->implantKit->brand    | Brand             | Brand (name)                                                 | String  | Anthogyr                  |
| data->treatments->implantKit->connection | Connection        | Connection (name)                                            | String  | Axiom BL                  |
| data->treatments->implantKit->platform | Platform          | Platform (name)                                              | String  | BL                        |
| data->treatments->implantKit->scanBody | Scan Body         | Scan body (name)                                             | String  | Straumann Scanbody SRA 35 |




-  **Response  Example**

```json
{
  "code":"200",
  "data":{
    "caseCode":"250121016244386840576",
    "caseStatus":3,
    "serialNumber":"EIAA0300",
    "scanTime":1737445405000,
    "userEmail":"lily@gmail.com",
    "patientId":"PI00000002",
    "patientName":"Ruby",
    "toothNumberingSystem":"fdi",
    "treatments": [
      {
        "clinicalType": 0,
        "ageType": 0,
        "workType": "Crown",
        "jawType": null,
        "toothSource": "",
        "scanbodyType": 0,
        "isAllOnX": 0,
        "number": "46",
        "implantType": "None",
        "scanPreOp": 0,
        "mesialConnected": 0,
        "inlayCore": null,
        "material": "MLZirconia",
        "abutmentMaterial": "",
        "shadeGuide": "VitaClassic",
        "shade": "D3",
        "implantKit": null
      },
      {
        "clinicalType": 0,
        "ageType": 0,
        "workType": "Crown",
        "jawType": null,
        "toothSource": "",
        "scanbodyType": null,
        "isAllOnX": null,
        "number": "47",
        "implantType": "None",
        "scanPreOp": 0,
        "mesialConnected": 0,
        "inlayCore": 0,
        "material": "None",
        "abutmentMaterial": "",
        "shadeGuide": "",
        "shade": "",
        "implantKit": null
      }
    ],
    "attachments":[
      {
        "fileCode":"F2501210123743197505126402",
        "fileFormat":"vertex_type",
        "category":"vertexTypeFiles",
        "fileName":"lower_pre-op.vertex_type",
        "url":"https://alliedstar-sh-test.oss-cn-shanghai.aliyuncs.com/order/250121016244386840576/model/lower_pre-op.vertex_type?x-oss-signature=Tb5HdT4xRs21W9XiJkQ4K0hOuc5cN3VsJnWWdffX7Eg%3D&x-oss-signature-version=OSS2&x-oss-expires=1744336834&x-oss-access-key-id=LTAI5tJe9UCXFYcRG4XV9FFZ",
        "lastModifiedTime":1737445405054
      },
      {
        "fileCode":"F2501210123743198343987204",
        "fileFormat":"vertex_type",
        "category":"vertexTypeFiles",
        "fileName":"upper.vertex_type",
        "url":"https://alliedstar-sh-test.oss-cn-shanghai.aliyuncs.com/order/250121016244386840576/model/upper.vertex_type?x-oss-signature=4QUFjUl7fOfLxtsMKT40GcHhfkPDRpE7OEcT%2Fgg1Ess%3D&x-oss-signature-version=OSS2&x-oss-expires=1744336834&x-oss-access-key-id=LTAI5tJe9UCXFYcRG4XV9FFZ",
        "lastModifiedTime":1737445405046
      },
      {
        "fileCode":"F2501210123801637162188801",
        "fileFormat":"ply",
        "category":"plyFiles",
        "fileName":"upper.ply",
        "url":"https://alliedstar-sh-test.oss-cn-shanghai.aliyuncs.com/order/250121016244386840576/model/upper.ply?x-oss-signature=PEhjnJlr0iSxd%2Bw5%2Bx7DEiZawvvsbNBHsnN28jaJN0Y%3D&x-oss-signature-version=OSS2&x-oss-expires=1744363234&x-oss-access-key-id=LTAI5tJe9UCXFYcRG4XV9FFZ",
        "lastModifiedTime":1737445547526
      },
      {
        "fileCode":"F2501210123801647647948801",
        "fileFormat":"stl",
        "category":"stlFiles",
        "fileName":"upper.stl",
        "url":"https://alliedstar-sh-test.oss-cn-shanghai.aliyuncs.com/order/250121016244386840576/model/upper.stl?x-oss-signature=6KJ6VDyW%2FW1yhjDmVjIeaO9zOiBYv20G50K5fSw3Dgk%3D&x-oss-signature-version=OSS2&x-oss-expires=1744363234&x-oss-access-key-id=LTAI5tJe9UCXFYcRG4XV9FFZ",
        "lastModifiedTime":1737445547550
      },
      {
        "fileCode":"F2501210123801676588646401",
        "fileFormat":"ply",
        "category":"plyFiles",
        "fileName":"lower_pre-op.ply",
        "url":"https://alliedstar-sh-test.oss-cn-shanghai.aliyuncs.com/order/250121016244386840576/model/lower_pre-op.ply?x-oss-signature=PrOVOntCNMh9qpnEImoPxBe5sGC5CP%2BWMdmib1ZlquA%3D&x-oss-signature-version=OSS2&x-oss-expires=1744363234&x-oss-access-key-id=LTAI5tJe9UCXFYcRG4XV9FFZ",
        "lastModifiedTime":1737445547619
      },
      {
        "fileCode":"F2501210123801682041241601",
        "fileFormat":"stl",
        "category":"stlFiles",
        "fileName":"lower_pre-op.stl",
        "url":"https://alliedstar-sh-test.oss-cn-shanghai.aliyuncs.com/order/250121016244386840576/model/lower_pre-op.stl?x-oss-signature=iSjLZjXwAmR%2F%2FGcoD4%2BS6NT9%2FvPzn09LDo3obKOxPOo%3D&x-oss-signature-version=OSS2&x-oss-expires=1744363234&x-oss-access-key-id=LTAI5tJe9UCXFYcRG4XV9FFZ",
        "lastModifiedTime":1737445547632
      }
    ]
  },
  "msg":"OK",
  "total":0
}
```

-   **Response Codes**


| Code | Description         |
| ---- | ------------------- |
| 200  | Successful response |
| 400  | Illegal request     |
| 502  | Request data is empty |
| 2023 | The case has been deleted |



### Get Case Treatment PDF

Developers can use this API to get case treatment PDF.

-  **Request URL：**

`POST open/order/getCaseTreatmentPdf`

`Content-Type: application/x-www-form-urlencoded`

-  **Request Parameters：**

| Parameter | Parameter Name                | Type   | Required | Description                                                  | Example                      |
| --------- | ----------------------------- | ------ | -------- | ------------------------------------------------------------ | ---------------------------- |
| openid    | User Authorization Binding ID | String | Yes      | openid obtained after user authorization                     | WmizQAMXoG1z8CcpTdMG0-4tLJ17 |
| caseCode  | AS Case Code                  | String | Yes      | case code                                                    | 2015101400446982             |
| language  | Language                      | String | No       | language；<br>Optional Range: ["da","de","el","en","es","fr","hr","hu","it","ja","ko","nl","no","pl","pt","ru","sk","sl","sv","tr","vi","en-US","zh-CN","zh-TW"]<br/>If not within the above range, the default value will be used. | en-US, ja                    |
| timeZone  | Time Zone                     | String | No       | time zone; <br/>Standard Specifications: IANA Time Zone Database | America/New_York             |

**Note:**

| Region         | language（Default） | timeZone（Default） |
| -------------- | ------------------- | ------------------- |
| China          | zh-CN               | Asia/Shanghai       |
| Europe         | en                  | Europe/Paris        |
| United Kingdom | en                  | Europe/London       |
| US & Canada    | en-US               | America/New_York    |
| Japan          | ja                  | Asia/Tokyo          |
| Others         | en                  | Asia/Singapore      |



-  **Response Parameters:**

| Parameter                 | Parameter Name     | Description        | Type   | Example                                                      |
| ------------------------- | ------------------ | ------------------ | ------ | ------------------------------------------------------------ |
| msg                       | Result Description | Result description | String | OK                                                           |
| code                      | Response Code      | Response code      | int    | 200 (for successful processing)                              |
| data                      | Returned Data      | Returned data      | object | object                                                       |
| data->caseCode            | AS Case Code       | AS case code       | String | 2015101400446982                                             |
| data->caseTreatmentPdfUrl | Case Treatment Pdf | Case treatment pdf | String | https://alliedstar-sh-test.oss-cn-shanghai.aliyuncs.com/order/2015101400446982/treatment-report.pdf |



- **Response code**

| Code | Description           |
| ---- | --------------------- |
| 200  | Success               |
| 400  | Invalid Request       |
| 502  | Request data is empty |
| 1002 | Sorry, access denied  |
| 1008 | User does not exist   |



### Get Case List by Page

Developers can use this interface to get a list of cases.

Only openid is required, other parameters are used for filtering result list. If the request parameter contains only "openid", then all cases belonging to that user will be returned.

- **Request URL：**

`POST open/order/listCases`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters：**

| Parameter        | Parameter Name                              | Type   | Required | Description                                                         | Example                    |
| ----------- |---------------------------------------------|--------| -------- | ------------------------------------------------------------ |----------------------------|
| openid      | User Unique Identifier                      | String | Yes      | Unique identifier of the AS platform user corresponding to the developer platform user | jkadhsjk821nkjzd89q1nw2e89 |
| caseStatus  | Case Status                                 | String | No       | Case status, multiple comma-separated <br/>(0: Registered, 1: To be processed, 2: Scan completed, 3: Uploaded, 4: Ordered, 5: Completed) | 0,3                        |
| patientName | Patient Name                                | String | No       | Name of the patient                                          | Alexandra Blackwood   |
| patientId   | Unique patient id                           | String | No       | Unique patient id  | FC23092008053615616        |
| startTime   | Last modified time - start time (timestamp) | String | No       | Last modified time - start time (timestamp); Time range query; | 1666660440000              |
| endTime     | Last modified time - end time (timestamp)   | String | No       | Last modified time - end time (timestamp); Time range query; | 1666660450000              |
| pageNumber  | number of pages                             | String | No       | number of pages                                              | 1                          |
| pageSize    | Number of records per page                  | String | No       | Number of records per page;default is 10, maximum is 100     | 10                         |

- **Response Parameters:**

| Parameter                     | Parameter Name         | Type    | Description                                                         | Example                       |
| ------------------------ |------------------------|---------| ------------------------------------------------------------ | ---------------------------- |
| msg                      | Result Message         | String  | Response message                                             | OK                           |
| code                     | Response Code | Integer | Response Code                                   | 200                          |
| total                    | Total Recordes         | Long    | Total Recordes                                               | 100                          |
| data                     | Response data          | Array   | Response data                                                |                              |
| data -> caseCode         | AS Case Code           | String  | AS Case Code                                                 | 2015101400446982             |
| data -> caseName         | AS Case Name           | String  | AS Case Name                                                 | Alexandra Blackwood's case |
| data -> caseStatus       | Case Status            | Integer | Case status (0: Registered, 1: To be processed, 2: Scan completed, 3: Uploaded, 4: Ordered, 5: Completed) | 3                            |
| data -> patientName      | Patient Name           | String  | Name of the patient                                          | Alexandra Blackwood     |
| data -> scanTime         | Scan Time              | Long    | Scan time (time when the CASE scan is completed)             | 1665975588000                |
| data -> userOpenid       | User OpenID            | String  | Unique identifier of the user<br/>(openid: the unique identifier of the user on the developer platform corresponding to the AS platform user) | rjpIUmubkUsw7YKrJMAl4xQvcsdh |
| data -> userName         | User Name              | String  | User Name                                                    | Lily                 |
| data->thumbnailUrl | Thumbnail | String | Thumbnail | https://images-en.allied-star.com/order/230419438412345678/model/private/thumbnail.png |
| data -> lastModifiedTime | Last modification time | Long    | Last modification time                                       | 1665975587000                |

**Note:** The returned results are displayed in descending order according to the last modification time.

- **Business Codes**

| Code | Description     |
| ---- | --------------- |
| 200  | Success         |
| 400  | Invalid Request |

-  **Response  Example**

```json
{
  "code":200,
  "msg":"OK",
  "total":10797,
  "sysTime":"2025-04-11 10:32:05",
  "data":[
    {
      "caseCode":"250409015919102664704",
      "caseName":"Ruby's Case",
      "caseStatus":3,
      "patientName":"Ruby",
      "scanTime":1744186736000,
      "userOpenid":null,
      "userName":"TOM",
      "lastModifiedTime":1744186737820
    },
    {
      "caseCode":"250409014544406945792",
      "caseName":"Alex's Case",
      "caseStatus":3,
      "patientName":"Alex",
      "scanTime":1744186570000,
      "userOpenid":null,
      "userName":"Bob",
      "lastModifiedTime":1744186572109
    },
    {
      "caseCode":"250409014033226145792",
      "caseName":"Tom's Case",
      "caseStatus":3,
      "patientName":"Tom",
      "scanTime":1744186268000,
      "userOpenid":null,
      "userName":"Bob",
      "lastModifiedTime":1744186268944
    },
    {
      "caseCode":"250409013490768420864",
      "caseName":"TOM clone case",
      "caseStatus":3,
      "patientName":"TOM",
      "scanTime":1744186141000,
      "userOpenid":null,
      "userName":"Bob",
      "lastModifiedTime":1744186141972
    },
    {
      "caseCode":"250409017876789673984",
      "caseName":"Mike05 case",
      "caseStatus":3,
      "patientName":"Mike",
      "scanTime":1744185989000,
      "userOpenid":null,
      "userName":"Bob",
      "lastModifiedTime":1744185990521
    },
    {
      "caseCode":"250408018082329100288",
      "caseName":"27-9 Clone Clone",
      "caseStatus":3,
      "patientName":"27-9",
      "scanTime":1743070644000,
      "userOpenid":null,
      "userName":"Mike",
      "lastModifiedTime":1744095691000
    },
    {
      "caseCode":"250407012141783785472",
      "caseName":"27-9 Clone",
      "caseStatus":3,
      "patientName":"27-9",
      "scanTime":1743070644000,
      "userOpenid":null,
      "userName":"Mike",
      "lastModifiedTime":1744095689000
    },
    {
      "caseCode":"250408016910787813376",
      "caseName":"LIly Clone",
      "caseStatus":3,
      "patientName":"LIly",
      "scanTime":1743503428000,
      "userOpenid":null,
      "userName":"Bob",
      "lastModifiedTime":1744092054000
    },
    {
      "caseCode":"250325014851921420288",
      "caseName":"LIly's case",
      "caseStatus":3,
      "patientName":"LIly",
      "scanTime":1743503428000,
      "userOpenid":null,
      "userName":"Bob",
      "lastModifiedTime":1744090922000
    }
  ]
}
```



### Show Case Without Logging In

Developers can use this interface to obtain the case show URL and view case details without logging in. The expiration time is **5 minutes**.

- **Request URL：**

`POST open/order/caseShow`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters：**

| Parameter | Parameter Name                | Type   | Required | Description                               | Example                    |
| --------- | ----------------------------- | ------ | -------- | ----------------------------------------- | -------------------------- |
| openid    | User Authorization Binding ID | String | Yes      | openid, obtained after user authorization | jkadhsjk821nkjzd89q1nw2e89 |
| caseCode  | AS Case Code                  | String | Yes      | AS Case Code                              | 2015101400446982           |

- **Response Parameters:**

| **Parameter**       | **Parameter Name**       | **Type** | Description              | Example                                                      |
| ------------------- | ------------------------ | -------- | ------------------------ | ------------------------------------------------------------ |
| msg                 | Result message           | String   | Result message           | OK                                                           |
| code                | Response Code            | Integer  | Response Code            | 200                                                          |
| data                | Response data            | object   | response data            |                                                              |
| data -> caseShowUrl | URL for viewing the case | String   | URL for viewing the case | https://test.allied-star.com/case-show?shareId=5530a38b44c042898d4fc66df80b8a61 |

- **Response Codes**

| Code | Description           |
| ---- |-----------------------|
| 200  | Success               |
| 400  | Invalid Request       |
| 1002 | Sorry, access denied. |


- **Response  Example**

```json
{
  "code":200,
  "msg":"OK",
  "data":{
    "caseShowUrl":"https://test.allied-star.com/case-show?shareId=5530a38b44c042898d4fc66df80b8a61"
  },
  "sysTime":"2025-04-11 10:44:58"
}
```





## Order

### Set Order Status

To accept or reject, ship orders, and update order status in AS Connect.

- **Request URL:**

`POST open/order/setOrderStatus`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters:**

| Parameter          | Description                                    | Type     | Required  | Example                               |
|-------------|------------------------------------------------|--------|-----|----------------------------------|
| openid      | openid obtained from user authorization        | String | Yes | jXHSJaAKD32Sd4sH5Af6dJDSA-4tLJ17 |
| orderCode   | AS order code                                  | String | Yes   | 230927801606929142528            |
| orderStatus | order status（3：accepted；4：rejected；5：shipped；） | String | Yes   | 3                                |

- **Response Parameters:**

| Parameter       | Description             | Type           | Example                 |
|----------|----------------|--------------|-------------------------|
| msg      | Result description | String       | OK                      |
| code     | Response Code | int          | 200 (for successful processing) |


- **Response Codes**

| Code   | Description                             |
|------|-----------------------------------------|
| 200  | Success                                 |
| 400  | Invalid Request                         |
| 502  | Request data is empty                   |
| 2001 | Current status does not allow operation |



### Get Order List by Page
Developers can use this interface to get a list of orders.

- **Request URL:**

`POST open/order/listOrders`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters:**

|  Parameter  |  Type  |  Description  |  Required  |  Example  |
| --- | --- | --- | --- | --- |
| unionid | String | unionid; <br/>Unique identifier corresponding to the organization in the developer platform and AS platform | NO | f40acc85394c46fe8f3bbc872d4f9bfe |
|  openid  |  String  |  openid obtained from user authorization  |  NO  |  jXHSJaAKD32Sd4sH5Af6dJDSA  |
|  patientName  |  String  |  Patient Name  |  NO  |  Tom  |
|  orderStatus  |  String  |  Order status, multiple comma-separated <br/>（2：hadSend；3：accepted；4：rejected；5：shipped；6：finished；9：ready）  |  NO  |  2,3  |
|  startTime  |  String  |  order time (timestamp)  |  NO  |  1666660440000  |
|  endTime  |  String  | order time(timestamp) |  NO  |  1666660450000  |
|  pageNumber  |  String  |  number of pages  |  NO  |  1  |
|  pageSize  |  String  |  Number of records per page;default is 10, maximum is 100  |  NO  |  10  |

Note:

- `unionid`, and `openid` cannot be empty simultaneously. 
- If the `unionid` or `openid` corresponds to a clinic on the AS platform, the `openid` parameter is mandatory.



- **Response Parameters:**

|  Parameter  |  Type  |  Description  |  Example  |
| --- | --- | --- | --- |
|  msg  |  String  |  Response message  |  OK  |
|  code  |  Integer  |  Response Code  |  200  |
|  total  |  Long  |  Total Recordes  |  100  |
|  data  |  Array  |  Response data  |   |
|  data ->  orderCode  |  String  |  AS Order Code  |  2015101400446982  |
|  data ->  orderName  |  String  |  AS Order Name  |  Ruby's order  |
|  data -> orderStatus  |  String  |  Order status, multiple comma-separated <br/>（2：hadSend；3：accepted；4：rejected；5：shipped；6：finished；9：ready）  |  3  |
|  data -> clinicName  |  String  |  Clinic Name  |  Tom's Clinic  |
|  data -> labName  |  String  |  Lab Name  |  Test Lab  |
|  data -> patientName  |  String  |  Patient Name  |  Ruby  |
| data->thumbnailUrl | String | Thumbnail | https://images-en.allied-star.com/order/230419438412345678/model/private/thumbnail.png |
|  data -> scanTime  |  Long  |  Scan completion time（CASE Scan completion time）  |  1665975588000  |
|  data -> orderTime  |  Long  |  Send order time  |  1665975589000  |


- **Response Codes**

|  Code  |  Description  |
| --- | --- |
|  200  |  Success  |
|  504  |  Invalid request parameters  |
|  1008  |  User does not exist  |
|  1014  |  Unavailable organization status. Please contact the administrator.  |



### Get Order Detail

Developers can get order details through this interface .

- **Request URL:**

`POST open/order/getOrderDetail`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters:**

| Parameter | Type   | Description                                                  | Required | Example                          |
| --------- | ------ | ------------------------------------------------------------ | -------- | -------------------------------- |
| unionid   | String | unionid; <br/>Unique identifier corresponding to the organization in the developer platform and AS platform | NO       | f40acc85394c46fe8f3bbc872d4f9bfe |
| openid    | String | openid obtained from user authorization                      | NO       | jXHSJaAKD32Sd4sH5Af6dJDSA        |
| orderCode | String | AS order code                                                | YES      | 2015101400446982                 |

Note:

- `unionid`, and `openid` cannot be empty simultaneously. 
- If the `unionid` or `openid` corresponds to a clinic on the AS platform, the `openid` parameter is mandatory.



- **Response Parameters:**

| Parameter                           | Type    | Description                                                                                                               | Example                                                                                                                                                                             |
| ----------------------------------- | ------- |---------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| msg                                 | String  | Result Description                                                                                                        | OK                                                                                                                                                                                  |
| code                                | int     | Response Code                                                                                                             | 200                                                                                                                                                                                 |
| data                                | object  | Response Data                                                                                                             |                                                                                                                                                                                     |
| data->orderCode                     | String  | AS order code                                                                                                             | 2015101400446982                                                                                                                                                                    |
| data->orderName | String | AS Order Name | Alexandra Blackwood's case |
| data->serialNumber                  | String  | Scanner series number                                                                                                     | CKAA0025                                                                                                                                                                            |
| data->orderStatus                 | String  | Order status, multiple comma-separated<br/>（2：hadSend；3：accepted；4：rejected；5：shipped；6：finished；9：ready）                 | 3                                                                                                                                                                                   |
| data->clinicName                  | String  | Clinic Name                                                                                                               | Tom's Clinic                                                                                                                                                                        |
| data->clinicUnionid | String | Clinic Unionid | GEB_mlc3XFYJ3rIhN8WSKQtN2WnK |
| data->clinicAddressCountryName                  | String  | Clinic country name                                                                                                       | America                                                                                                                                                                             |
| data->clinicAddressLocation                  | String  | Clinic location                                                                                                           | New York                                                                                                                                                                            |
| data->clinicAddressDetail                  | String  | Clinic address detail                                                                                                     | King Street                                                                                                                                                                         |
| data->doctorUserCode                  | String  | Clinic doctor user code                                                                                                   | xxxxxxxxxx                                                                                                                                                                          |
| data->labName                     | String  | Lab Name                                                                                                                  | Test Lab                                                                                                                                                                            |
| data->scanTime                      | Long    | Scan completion time（CASE Scan completion time）                                                                           | 1665975588000                                                                                                                                                                       |
| data->orderTime                     | Long    | Send order time                                                                                                           | 1665975588000                                                                                                                                                                       |
| data->doctorUserName                | String  | Doctor's name                                                                                                             | Ruby                                                                                                                                                                                |
| data->doctorUserEmail               | String  | Doctor's Email                                                                                                            | Ruby@gmail.com                                                                                                                                                                      |
| data->doctorUserPhone               | String  | Doctor's phone                                                                                                            | 13766668888                                                                                                                                                                         |
| data->patientId                     | String  | Unique identifier of the patient in the developer platform                                                                | FC2021040613041460433                                                                                                                                                               |
| data->patientName                   | String  | Name of the patient                                                                                                       | Alexandra Blackwood                                                                                                                                                                 |
| data->patientMemo                   | String  | Patient memo                                                                                                              | Patient memo                                                                                                                                                                        |
| data->toothNumberingSystem          | String  | Tooth numbering system (fdi;universal)                                                                                    | fdi                                                                                                                                                                                 |
| data->reqDeliveryDate               | Long    | Requested Delivery Date (timestamp)                                                                                       | 1666660440000                                                                                                                                                                       |
| data->comment                       | String  | Comment<br/>(Note provided by the clinic when sending the order to the dental laboratory)                                 | comment                                                                                                                                                                             |
| data->audioComment                  | array   | Audio Comment                                                                                                             | \[“https://images-en.allied-star.com/order/230419438412345678/audio/voice\_memo1.wav”\]                                                                                             |
| data->thumbnailUrl | String | Thumbnail | https://images-en.allied-star.com/order/230419438412345678/model/private/thumbnail.png |
| data->attachments                   | array   | Attachments information:<br/>\1. 2D and 3D files generated by AS scanner;<br/>\2. Other attachments uploaded by the user; | \[ { “category”: “marginLine”, “fileCode”: “F2305151601260738381004805”, “fileFormat”: “a3d”, “fileName”: “lower\_margin\_line.a3d”, “lastModifiedTime”:1666660440000 “url”: ““ }\] |
| data->attachments->category         | String  | File Category ([CategoryEnum](files/v2_API_ALL.md#CategoryEnum))                                                          | marginLine                                                                                                                                                                          |
| data->attachments->fileCode         | String  | File code (unique identifier of the file)                                                                                 | F2210260815931942401                                                                                                                                                                |
| data->attachments->fileFormat       | String  | File format<br/>(stl, ply, jpg, jpeg, image/jpeg, image/png, image/gif, etc.)                                             | ply                                                                                                                                                                                 |
| data->attachments->fileName         | String  | File Name                                                                                                                 | upper.ply                                                                                                                                                                           |
| data->attachments->url              | String  | Storage path of the file in the cloud object storage                                                                      | https://images.allied-star.com.com/order/221023377606746801152/io\_image/image\_1.jpg                                                                                               |
| data->attachments->lastModifiedTime | Long    | Last modified time of the file (timestamp)                                                                                | 1666660440000                                                                                                                                                                       |
| data->treatments                    | Array   | Treatment Details                                                                                                         |                                                                                                                                                                                     |
| data->treatments->clinicalType          | Integer | Clinical type (0: Restoration, 1: Orthodontic, 2: Other)     | 0                         |
| data->treatments->ageType               | Integer | Age type (0: Adult, 1: Child)                                | 0                         |
| data->treatments->workType              | String  | Work type                                                    | Crown                     |
| data->treatments->jawType               | Integer | Jaw type（1:Upper Jaw；2:Lower Jaw；3:Upper Jaw And Lower Jaw） | 1                         |
| data->treatments->toothSource           | String  | Tooth source                                                 | ImplantUpperJaw           |
| data->treatments->scanbodyType          | Integer | Scanbody type (0: None, 1: Alliedstar, 2: Tektonik, 3: Medentika, 99: Other) | 0                         |
| data->treatments->isAllOnX              | Integer | Full-arch implant (0: false, 1: true)                        | 0                         |
| data->treatments->number                | String  | Tooth position                                               | 28                        |
| data->treatments->implantType           | String  | Implant type                                                 | CustomAbutment            |
| data->treatments->scanPreOp             | Integer | Scan pre-operation (0: false, 1: true)                       | 0                         |
| data->treatments->mesialConnected       | Integer | Mesial connection (0: false, 1: true)                        | 0                         |
| data->treatments->inlayCore             | Integer | Inlay core (0: false, 1: true)                               | 0                         |
| data->treatments->material              | String  | Material                                                     | PMMA                      |
| data->treatments->abutmentMaterial      | String  | Abutment material                                            | Zirconia                  |
| data->treatments->shadeGuide            | String  | Shade guide                                                  | VitaClassic               |
| data->treatments->shade                 | String  | Shade (code)                                                 | D3                        |
| data->treatments->implantKit | object | Implant Kit |  |
| data->treatments->implantKit->brand    | String  | Brand (name)                                                 | Anthogyr                  |
| data->treatments->implantKit->connection | String  | Connection (name)                                            | Axiom BL                  |
| data->treatments->implantKit->platform | String  | Platform (name)                                              | BL                        |
| data->treatments->implantKit->scanBody | String  | Scan body (name)                                             | Straumann Scanbody SRA 35 |



**Note：**Please see [Reference](files/v2_API_ALL.md#Reference) Enumeration values for details.

- **Response Codes**

| **Code** | Description           |
| -------- | --------------------- |
| 200      | Successful response   |
| 400      | Illegal request       |
| 502      | Request data is empty |
| 1002     | Sorry, access denied  |



### Get Order Treatment PDF

Developers can use this API to get order treatment PDF.

-  **Request URL：**

`POST open/order/getOrderTreatmentPdf`

`Content-Type: application/x-www-form-urlencoded`

-  **Request Parameters：**

| Parameter | Parameter Name                | Type   | Required | Description                                                  | Example                      |
| --------- | ----------------------------- | ------ | -------- | ------------------------------------------------------------ | ---------------------------- |
| openid    | User Authorization Binding ID | String | Yes      | openid obtained after user authorization                     | WmizQAMXoG1z8CcpTdMG0-4tLJ17 |
| orderCode | AS Order Code                 | String | Yes      | order code                                                   | 2015101400446982             |
| language  | Language                      | String | No       | language；<br/>Optional Range: ["da","de","el","en","es","fr","hr","hu","it","ja","ko","nl","no","pl","pt","ru","sk","sl","sv","tr","vi","en-US","zh-CN","zh-TW"]<br/>If not within the above range, the default value will be used. | en-US, ja                    |
| timeZone  | Time Zone                     | String | No       | time zone; <br/>Standard Specifications: IANA Time Zone Database | America/New_York             |

**Note:**

| Region         | language（Default） | timeZone（Default） |
| -------------- | ------------------- | ------------------- |
| China          | zh-CN               | Asia/Shanghai       |
| Europe         | en                  | Europe/Paris        |
| United Kingdom | en                  | Europe/London       |
| US & Canada    | en-US               | America/New_York    |
| Japan          | ja                  | Asia/Tokyo          |
| Others         | en                  | Asia/Singapore      |



-  **Response Parameters:**

| Parameter                  | Parameter Name      | Description         | Type   | Example                                                      |
| -------------------------- | ------------------- | ------------------- | ------ | ------------------------------------------------------------ |
| msg                        | Result Description  | Result description  | String | OK                                                           |
| code                       | Response Code       | Response code       | int    | 200 (for successful processing)                              |
| data                       | Returned Data       | Returned data       | object | object                                                       |
| data->orderCode            | AS Order Code       | AS order code       | String | 2015101400446982                                             |
| data->orderTreatmentPdfUrl | Order Treatment Pdf | Order treatment pdf | String | https://alliedstar-sh-test.oss-cn-shanghai.aliyuncs.com/order/2015101400446982/treatment-report.pdf |



- **Response code**

| Code | Description           |
| ---- | --------------------- |
| 200  | Success               |
| 400  | Invalid Request       |
| 502  | Request data is empty |
| 1002 | Sorry, access denied  |
| 1008 | User does not exist   |



### Send Order

For clinic to send an order to lab

- **Request URL:**

`POST open/order/sendOrder`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters:**

| Parameter          | Type                                | Description                         | Required | Example                   |
|-------------|------------------------------------------------|-----------------------------------------|----------|---------------------------|
| openid   | String | openid obtained from user authorization | Yes      | jXHSJaAKD32Sd4sH5Af6dJDSA |
| caseCode | String | AS case code                            | Yes      | 2015101400446982          |
| memo     | String | Memorandum                              | No       | Memo Example              |
| labCode     | String | laboratory code                         | Yes      | C2015101400446982         |
| requestedDeliveryDate     | Long   | Timestamp for requested delivery date   | Yes      | 1759042182607             |

- **Response Parameters:**

| Parameter       | Description             | Type           | Example                 |
|----------|----------------|--------------|-------------------------|
| msg      | Result description | String       | OK                      |
| code     | Response Code | int          | 200 (for successful processing) |


- **Response Codes**

| Code | Description                     |
|------|---------------------------------|
| 200  | Success                         |
| 400  | Invalid Request                 |
| 502  | Request data is empty           |
| 1002 | Access denied                   |
| 2027 | Case not exist                  |
| 2030 | You can only send your own case |
| 2037 | Order is already sent           |
| 2033 | Case files are not uploaded     |



## User


### Create User

Developers can use this API to create a user.



- **Request URL:**

`POST /open/v3/user/createUser`

`Content-Type: application/x-www-form-urlencoded`



- **Request Parameters:**

| Parameter        | Parameter Name      | Type    | Required | Description                                                  | Example                      |
| ---------------- | ------------------- | ------- | -------- | ------------------------------------------------------------ | ---------------------------- |
| username         | Username            | String  | No       | Username; globally unique; if empty, a username is auto-generated | test                         |
| password         | Password            | String  | No       | Password                                                     | XXXXXX                       |
| externalUserCode | Developer User Code | String  | No       | Developer platform user code                                 | IA201810136446956253         |
| unionid          | unionid             | String  | Yes      | unionid; <br>Unique identifier corresponding to the organization in the developer platform and AS platform | ZYMW7P2riutDaF2Fj9MG0-4tLJ17 |
| phone            | Phone Number        | String  | No       | Phone number; unique within the developer platform; considered the same user if already exists | 13766668888                  |
| email            | Email               | String  | No       | Email; unique within the developer platform                  | zhangsan@163.com             |
| fullName         | Full Name           | String  | Yes      | Full name                                                    | Zhang San                    |
| gender           | Gender              | Integer | No       | Gender (0: unknown, 1: male, 2: female)                      | 1                            |
| age              | Age                 | Integer | No       | Age                                                          | 18                           |
| nickName         | Nickname            | String  | No       | Nickname                                                     | Zhang San Feng               |
| roleCode         | Role code           | String  | No       | Role code, the default role is staff (ROLE_ADMIN, ROLE_STAFF) | ROLE_STAFF                   |

Note:

- `username`, `email`, and `phone` cannot be empty simultaneously.



- **Response Parameters:**

| Parameter      | Parameter Name                                               | Type   | Example          |
| -------------- | ------------------------------------------------------------ | ------ | ---------------- |
| msg            | Result Message                                               | string | OK               |
| code           | Business Code                                                | int    | 200 (success)    |
| data           | Response data                                                | object |                  |
| data -> openid | openid (Unique identifier of the AS platform user corresponding to the developer platform user) | string | 2015101400446982 |



- **Business Codes**

| Code | Description           |
| ---- | --------------------- |
| 200  | Success               |
| 400  | Invalid Request       |
| 403  | Sorry, access denied  |
| 500  | Internal Exception    |
| 1007 | User Already Exists   |
| 1030 | Full Name is Required |



## Service

### Tooth split

Developers can access the tooth splitting function through this API.

- **Request URL:**

`POST open/service/toothsplit`

`Content-Type: application/x-www-form-urlencoded`

- **Request Parameters:**

| Parameter | Type   | Description                                                  | Required | Example                             |
| --------- | ------ | ------------------------------------------------------------ | -------- | ----------------------------------- |
| uniqueKey | String | Unique identifier for current request<br>Regex: ^[a-zA-Z0-9_-]{1,30}$ | Yes      | 53209fe277064ae698f56b1a8166a496    |
| upper     | String | Upper jaw - cloud storage address                            | No       | https://cloud.example.com/upper.stl |
| lower     | String | Lower jaw - cloud storage address                            | No       | https://cloud.example.com/lower.stl |

Note:

​	upper and lower cannot be empty simultaneously.

- **Response Parameters:**

| Parameter       | Type   | Description                                                  | Example                                        |
| --------------- | ------ | ------------------------------------------------------------ | ---------------------------------------------- |
| msg             | String | Response message                                             | OK                                             |
| code            | int    | Response Code                                                | 200                                            |
| data            | object | Response data                                                |                                                |
| data->uniqueKey | String | Unique identifier for current request                        | 53209fe277064ae698f56b1a8166a496               |
| data->upper     | String | Upper tooth split calculation result - cloud storage address | https://cloud.example.com/toothsplit/upper.txt |
| data->lower     | String | Lower tooth split calculation result - cloud storage address | https://cloud.example.com/toothsplit/lower.txt |

- **业务编码**

| 编码 | 描述                                  |
| ---- | ------------------------------------- |
| 200  | Success                               |
| 400  | Invalid Request                       |
| 513  | Network error, please try again later |
| 2019 | Processing failed                     |



## Callback

### Asynchronous Notification of Scan Results to Developers

Developers need to provide a callback URL.

After the scan is completed, the Open Platform will asynchronously send the scan results to the callback URL provided by the developer. The callback request will include the cloud storage attachment path of the current scan result. Since the scan information is stored in a file-private format on the development platform, the attachment link in the callback URL has a certain validity period. Developers need to download the attachment within the valid period. If the attachment is not downloaded during this period, the "Request Scan Result Interface" can be called for active synchronization.

- **Request Type:**

`Request-Type: POST`

`Content-Type: application/json; charset=utf-8`

- **Request Headers：**

| Header Name | Header Value Example | Header Value Description                                     |
| ----------- | -------------------- | ------------------------------------------------------------ |
| site        | us                   | **cn** : China; <br/>**eu** : European Union; <br/>**uk** : U.K.; <br/>**us** : USA; <br/>**jp** : Japan; <br/>**global** : Singapore; <br/>**outtest** : Test; |

- **Asynchronous Notification Request Parameter Description**

| Parameter                                | Parameter Name                         | Description                                                  | Type    | Example                                                      |
| ---------------------------------------- | -------------------------------------- | ------------------------------------------------------------ | ------- | ------------------------------------------------------------ |
| caseCode                                 | AS Case Code                           | AS case code                                                 | String  | 2015101400446982                                             |
| externalCaseCode                         | Developer Case Code                    | Developer case code                                          | String  | 21080500017918484864                                         |
| serialNumber                             | Scanner series number                  | Scanner series number                                        | String  | EM310                                                        |
| scanTime                                 | Scan Time                              | Scan time (time when the CASE scan is completed)             | Long    | 1665975588000                                                |
| orderTime                                | Order Time                             | Order time (time when the order is sent to the dental laboratory) | Long    | 1665975588000                                                |
| userOpenid                               | Current User OpenID                    | Unique identifier of the current user<br/>(openid: the unique identifier of the user on the developer platform corresponding to the AS platform user) | String  | rjpIUmubkUsw7YKrJMAl4xQvcsdh                                 |
| userEmail                                | Current User Email                     | Email of the current user                                    | String  | Lily@gmail.com                                               |
| userPhone                                | Current User Phone Number              | Phone number of the current user                             | String  | 13766668888                                                  |
| patientId                                | Developer Platform Patient ID          | Unique identifier of the patient in the developer platform   | String  | FC2021040613041460433                                        |
| patientName                              | Patient Name                           | Name of the patient                                          | String  | Alexandra Blackwood                                          |
| patientMemo                              | Patient Memo                           | Patient memo                                                 | String  | Patient memo                                                 |
| toothNumberingSystem                     | Tooth Numbering System (fdi;universal) | Tooth numbering system (fdi;universal)                       | String  | fdi                                                          |
| reqDeliveryDate                          | Requested Delivery Date                | Requested Delivery Date (timestamp)                          | Long    | 1666660440000                                                |
| comment                                  | Comment                                | Comment<br/>(Note provided by the clinic when sending the order to the dental laboratory) | String  | Comment                                                      |
| audioComment                             | Audio Comment                          | Audio Comment                                                | array   | [<br/>"https://images-en.allied-star.com/order/230419438412345678/audio/voice_memo1.wav"<br/>] |
| attachments                              | Attachments                            | Attachments information:<br/>1. 2D and 3D files generated by AS scanner;<br/>2. Other attachments uploaded by the user;<br/>3. 2D and 3D files generated by applications in AS Connect. | array   | [<br/>{<br/>"category": "marginLine",<br/>"fileCode": "F2305151601260738381004805",<br/>"fileFormat": "ply",<br/>"fileName": "lower_margin_line.ply",<br/>"lastModifiedTime": 1666660440000,<br/>"url": ""<br/>}] |
| attachments->category                    | File Category                          | File category                                                | String  | marginLine                                                   |
| attachments->fileCode                    | File Code                              | File code (unique identifier of the file)                    | String  | F2210260815931942401                                         |
| attachments->fileFormat                  | File Format                            | File format<br/>(stl, ply, jpg, jpeg, image/jpeg, image/png, image/gif, etc.) | String  | ply                                                          |
| attachments->fileName                    | File Name                              | File name                                                    | String  | upper.ply                                                    |
| attachments->url                         | Storage Path                           | Storage path of the file in the cloud object storage         | String  | https://images.allied-star.com.com/order/221023377606746801152/io_image/image_1.jpg |
| attachments->lastModifiedTime            | Last Modified Time                     | Last modified time of the file (timestamp)                   | Long    | 1666660440000                                                |
| treatments                               | Treatment Details                      | Treatment details                                            | array   |                                                              |
| data->treatments->clinicalType           | Clinical Type                          | Clinical type (0: Restoration, 1: Orthodontic, 2: Other)     | Integer | 0                                                            |
| data->treatments->ageType                | Age Type                               | Age type (0: Adult, 1: Child)                                | Integer | 0                                                            |
| data->treatments->workType               | Work Type                              | Work type                                                    | String  | Crown                                                        |
| data->treatments->jawType                | Jaw Type                               | Jaw type（1:Upper Jaw；2:Lower Jaw；3:Upper Jaw And Lower Jaw） | Integer | 1                                                            |
| data->treatments->toothSource            | Tooth Source                           | Tooth source                                                 | String  | ImplantUpperJaw                                              |
| data->treatments->scanbodyType           | Scanbody Type                          | Scanbody type (0: None, 1: Alliedstar, 2: Tektonik, 3: Medentika, 99: Other) | Integer | 0                                                            |
| data->treatments->isAllOnX               | All-on-X                               | Full-arch implant (0: false, 1: true)                        | Integer | 0                                                            |
| data->treatments->number                 | Tooth Position                         | Tooth position                                               | String  | 28                                                           |
| data->treatments->implantType            | Implant Type                           | Implant type                                                 | String  | CustomAbutment                                               |
| data->treatments->scanPreOp              | Scan Pre-op                            | Scan pre-operation (0: false, 1: true)                       | Integer | 0                                                            |
| data->treatments->mesialConnected        | Mesial Connected                       | Mesial connection (0: false, 1: true)                        | Integer | 0                                                            |
| data->treatments->inlayCore              | Inlay Core                             | Inlay core (0: false, 1: true)                               | Integer | 0                                                            |
| data->treatments->material               | Material                               | Material                                                     | String  | PMMA                                                         |
| data->treatments->abutmentMaterial       | Abutment Material                      | Abutment material                                            | String  | Zirconia                                                     |
| data->treatments->shadeGuide             | Shade Guide                            | Shade guide                                                  | String  | VitaClassic                                                  |
| data->treatments->shade                  | Shade                                  | Shade (code)                                                 | String  | D3                                                           |
| data->treatments->implantKit             | Implant Kit                            | Implant Kit                                                  | object  |                                                              |
| data->treatments->implantKit->brand      | Brand                                  | Brand (name)                                                 | String  | Anthogyr                                                     |
| data->treatments->implantKit->connection | Connection                             | Connection (name)                                            | String  | Axiom BL                                                     |
| data->treatments->implantKit->platform   | Platform                               | Platform (name)                                              | String  | BL                                                           |
| data->treatments->implantKit->scanBody   | Scan Body                              | Scan body (name)                                             | String  | Straumann Scanbody SRA 35                                    |
| sign                                     | Signature                              | Signature is used to prevent the data information sent from being tampered with. The generation rules for signatures can be referred to in the Integration Solution Introduction - Signature Algorithm. <br/>The developer platform can validate the signature, but it is also possible to not validate it. | String  | IuFteb+zRAHcfWqK9E7sBEht+mJ63bQcDLXpgrc6hsEbTAm4B3JugfyDJdYbgT5ggWoMpe<br/>2SUlcUvKM4/wxC8KHTSzsywFvAqqMR6HBeQntp9YETXTp9ugngfrrDAUH6f00NF4lkzv55k<br/>qqzd4ZDo1YYDpeGOnDHFjcVcoZf2glEfQGGpsbekPV0z8PkpVBSeBSVVCu119jox10DFS6D<br/>+9q3mE9+6MB+/TOlT3XLf8las+JghUfXRTGDHOMeA85nJcNYNsD2H18TXn2IzCn+MvpI8j+I<br/>www5a4MISq5MvUzSNrbim5Y9nsHDyn7QpOVHUZOkUHcZ7VPovPPsIK/ydQ== |


- **Sample Response Parameters from Developer Platform**

**Note:** The success response should have a business code of 200.

```json
{
    "code": "200",
    "msg": "Success"
}
```



### Asynchronous Notification of Order Information to Developers

Developers need to provide a callback URL. When an order is sent, the Open Platform will asynchronously send the order information to the provided callback URL.



- **Request Type:**

`Request-Type: POST`

`Content-Type: application/json; charset=utf-8`

- **Request Headers：**

| Header Name | Header Value Example | Header Value Description                                     |
| ----------- | -------------------- | ------------------------------------------------------------ |
| site        | us                   | **cn** : China; <br/>**eu** : European Union; <br/>**uk** : U.K.; <br/>**us** : USA; <br/>**jp** : Japan; <br/>**global** : Singapore; <br/>**outtest** : Test; |

- **Asynchronous Notification Request Parameter Description**

| Parameter       | Parameter Name                | Description                                                  | Type    | Example                    |
| --------------- | ----------------------------- | ------------------------------------------------------------ | ------- | -------------------------- |
| orderCode       | Order Code                    | AS Order Code                                                | String  | 2015101400446982           |
| orderName       | Order Name                    | AS Order Name                                                | String  | Alexandra Blackwood's case |
| orderStatus     | Order Status                  | Order status, multiple comma-separated<br/>（2：hadSend；3：accepted；4：rejected；5：shipped；6：finished；9：ready） | Integer | 3                          |
| clinicName      | Clinic Name                   | Clinic Name                                                  | String  | Tom's Clinic               |
| labName         | Lab Name                      | Lab Name                                                     | String  | Test Lab                   |
| labUnionid      | Lab Unionid                   | Lab Unionid                                                  | String  | GEB_mlc3XFYJ3rIjdaih328Nm  |
| patientId       | Developer Platform Patient ID | Unique identifier of the patient in the developer platform   | String  | FC2021040613041460433      |
| patientName     | Patient Name                  | Name of the patient                                          | String  | Alexandra Blackwood        |
| reqDeliveryDate | Requested Delivery Date       | Requested Delivery Date (timestamp)                          | Long    | 1666660440000              |
| orderTime       | Order Time                    | Order time (time when the order is sent to the dental laboratory) | Long    | 1665975588000              |
| sign            | Signature                     | Signature is used to prevent the data information sent from being tampered with. The generation rules for signatures can be referred to in the Integration Solution Introduction - Signature Algorithm. <br/>The developer platform can validate the signature, but it is also possible to not validate it. | String  |                            |



- **Sample Response Parameters from Developer Platform**

**Note:** The success response should have a business code of 200.

```json
{
    "code": "200",
    "msg": "Success"
}
```





## Reference

### Enumerations

#### CategoryEnum:

**In the attachment information, the enumeration value and description related to the file category (category)**

```json
{
    "app2D": "2D Application File",
    "appOther": "Other Application File",
    "appPlyFiles": "PLY Application File",
    "appStlFiles": "STL Application File",
    "audioFiles": "Audio File",
    "broadsidePhoto": "Screen Snapshot",
    "marginLine": "Margin Line",
    "mouthPhoto": "Intraoral Photo",
    "otherImgFiles": "Other Image Attachment",
    "plyBiteFiles": "Bite PLY File",
    "plyFiles": "PLY File",
    "report": "Scan Report",
    "splitTeeth": "Split Teeth Result",
    "stlBiteFiles": "Bite STL File",
    "stlFiles": "STL File"
}
```



#### TreatementWorkTypeEnum:

**In the treatment details, the enumeration value and description related to the work type (workType)**

```json
clinicalType = 0（Restoration）
{
  "Crown": "Crown",
  "PostCore": "Post & Core",
  "Inlay": "Inlay/Onlay",
  "Pontic": "Pontic",
  "Veneer": "Veneer",
  "FullDenture": "Full Denture",
  "PartialDenture": "Partial Denture",
  "SurgicalGuide": "Surgical Guide"
}
```



```json
clinicalType = 1（Orthodontic）
{
	"ClearAligner": "Clear Aligner",
	"DentalBraces": "Dental Braces",
	"ModelArchiving": "Model Archiving",
	"Retainer": "Retainer"
}
```



```json
clinicalType = 2（Other）
{
	"SmileDesign": "Smile Design",
	"OralCheck": "Oral Check",
	"StudyModel": "Study Model",
	"BiteSplint": "Bite Splint"
}
```



#### TreatmentImplantTypeEnum:

**In the treatment details, the implant type(implantType) related enumeration value and its description**

```json
{
    "None": "No implant",
    "StockAbutment": "Stock Abutment",
    "CustomAbutment": "Custom Abutment"
}
```



#### TreatmentMeterialEnum:

**In the treatment details, material code (material) related enumeration value and its description**

```json
{
    "None": "None",
    "Composite": "Composite",
    "Feldspar": "Feldspar",
    "Zirconia": "Zirconia",
    "MLZirconia": "Multilayer Zirconia",
    "GlassCeramic": "Glass Ceramic",
    "HybridCeramic": "Hybrid Ceramic",
    "LithiumDisilicate": "Lithium Disilicate",
    "NobleMetal": "Noble Metal",
    "NPMetal": "NP Metal",
    "Titanium": "Titanium",
    "Wax": "Wax",
    "PFM": "PFM",
    "PMMA": "PMMA"
}
```



### Response Code

| Code | Description                                    |
|------| --------------------------------------- |
| 200  | Success                                 |
| 400  | Invalid Request                         |
| 500  | Internal Exception                      |
| 501  | Operation Frequent, Please Retry Later  |
| 502  | Request data is empty                   |
| 1002 | Sorry, access denied                    |
| 2001 | Current status does not allow operation |
| 2025 | Current User Not Authorized             |

