# **File Events**

# **📂 Event Summary**

| **Event Name** | **Description** | **Publisher** | **Subscriber** |
| --- | --- | --- | --- |
| `patient.file.uploaded` | Event sent after a successful first-time file upload, and the third-party system can use this information for reconciliation purposes. | AXSPATIENTS | WebhookHandler → Third-party system |
| `patient.file.updated` | Event sent after a successful File element (or RCF) is updated or the file is updated/uploaded again. This event will be used to inform the subscribing third part that a virtual file element has been updated or an updated blob/file has been uploaded back, and the third-party system can use this information for reconciliation purposes. The updated details are only sent back in the event. | AXSPATIENTS | WebhookHandler → Third-party system |
| `patient.file.deleted` | Event sent after a successful File element (or RCF) deletion. This event will be used to inform the subscribing third part that a virtual file element has been deleted, and the third-party system can use this information for reconciliation purposes. | AXSPATIENTS | WebhookHandler → Third-party system |

---

# **🧩 Event DTO Structure**

# **File/Blob Events**

- **patient.file.uploaded**
- **patient.file.updated**

```json
{"source":"AXS","messageId":"fa43ea05-1601-4c24-b0ff-98947f4e793c","timestamp":"2025-11-10T09:33:12.209Z","eventType":"patient.file.uploaded","organizationId":"ba43ea05-1001-3c24-b0ff-98347f4e793c","data":{"patient":{"id":"bccb92f6-3f8e-4a27-a193-86d16d064ebe","files":[{"id":"b498d324-4035-4512-9536-7003c07d4333","storageUri":"https://test02-api-use-axs.straumann.com/api/fss/b498d324-4035-4512-9536-7003c07d4333/file","name":"test1234.xorder","type":"XOrder","sizeInBytes":2000,"lastModifiedAt":"2025-11-10T09:35:12.209Z"}]}}}
```