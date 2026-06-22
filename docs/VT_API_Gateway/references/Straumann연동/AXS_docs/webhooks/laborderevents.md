# **Lab order Events**

# **📂 Event Summary**

| **Event Name** | **Description** | **Publisher** | **Subscriber** |
| --- | --- | --- | --- |
| `order.updated` | Event sent after a change on the status of a Lab Order. This event will be used to inform the subscribing third party that an order has been updated, and the third-party system can use this information for getting more information about the order. | AXS LAB ORDERS | Webhook Handler and ultimately the third party intended to get the event |

# **🧩 Event DTO Structure**

# **Lab order Events**

- **order.updated**

```json
{"source":"AXS","messageId":"fa43ea05-1601-4c24-b0ff-98947f4e793c","timestamp":"2025-10-01T15:47:26.853Z","eventType":"order.updated","operationId":"123","organizationId":"8f42b4e6-2d3c-4d8b-9d71-8a77b4b7b0f9","data":{"order":{"orderId":"bccb92f6-3f8e-4a27-a193-86d16d064ebe","customOrderId":"LO_12092025","destinationOrganizationId":"e13a9d2a-6b8c-4e93-91c7-2a3f2d671ca5","status":"IN VALIDATION"}}}
```

The following table describes some of the fields for a better understanding and its possible values to comprehend the webhook information obtained:

| **Field** | **Description** |
| --- | --- |
| `organizationId` | Unique identifier of the organization updating the order status. |
| `destinationOrganizationId` | Unique identifier of the destination organization of the order. |
| `status` | Order current status. Possible values:`UPLOADING` → Order files and data are being uploaded`READY_TO_SEND` → Status achieved when order data and files are ready to be sent to the other organization.`IN_VALIDATION`→ Status achieved when the order is sent.`UPLOAD_UNSUCCESSFUL` → Status achieved when there has been a problem when creating the order with its data or files. |