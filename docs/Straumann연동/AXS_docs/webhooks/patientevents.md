# **Patient Events**

The **AXS Vault** provides webhook notifications to third-party systems whenever patient-related events occur.

These events help external systems reconcile patient data in real time.

---

# **📂 Event Summary**

| **Event Name** | **Description** | **Publisher** | **Subscriber** |
| --- | --- | --- | --- |
| `patient.created` | This event is triggered after a Patient is successfully created. It notifies the subscribing third-party system that a Patient record has been created, allowing the third party to use this information for reconciliation purposes. | AXSPATIENTS | Webhook Handler and ultimately the third party intended to get the event |
| `patient.updated` | This event is triggered after patient information is successfully updated, allowing the third-party system to use the updated details for reconciliation purposes. | AXSPATIENTS | Webhook Handler and ultimately the third party intended to get the event |
| `patient.deleted` | This event is triggered after patient information is successfully deleted, allowing the third-party system to use the updated details for reconciliation purposes. | AXSPATIENTS | Webhook Handler and ultimately the third party intended to get the event |

---

# **🧩 Event DTO Structure**

# **Patient Events**

- **patient.created**
- **patient.updated**
- **patient.deleted**

**note**

- In case of `patient.deleted` event, only the Patient ID information is sent back in the event.

```json
{"source":"axs","messageId":"17af7ff6-2568-4e22-9c96-b7410c12eee9","timestamp":"2025-11-12T11:28:36.705Z","eventType":"patient.created","organizationId":"e407b34d-c4b0-4db3-bbcd-cc11770eae7b","data":{"patient":{"id":"3da6be5b-666b-4a7e-859d-a2de913f255b","firstName":"John","lastName":"Doe","gender":"MALE","dateOfBirth":"1967-06-07"}}}
```

**note**

- In case of `patient.updated` event, only the relevant updated information is sent back in the event.

```json
{"source":"axs","messageId":"cfcfee93-a304-4582-a6e5-7818441d3d0e","timestamp":"2025-11-12T11:30:00.052Z","eventType":"patient.updated","organizationId":"e407b34d-c4b0-4db3-bbcd-cc11770eae7b","data":{"patient":{"id":"3da6be5b-666b-4a7e-859d-a2de913f255b","firstName":"John","lastName":"Doe","middleName":"K","gender":"MALE","dateOfBirth":"1967-06-07"}}}
```