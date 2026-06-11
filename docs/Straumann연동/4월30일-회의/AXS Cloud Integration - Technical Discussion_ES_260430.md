# Discussion Points​

- **Definition of the Vatech Auth Server’s role and development ownership**

The 'Vatech Auth Server' referenced in the document is understood to function more as an **API Gateway** than an Auth Server. Given its intended purpose, it would be more appropriate for the integration checkpoints with various third-party devices to be **universally reviewed and configured on the AXS Cloud side**. Should ES proceed with developing the API Gateway independently, the development schedule and target completion date will need to be **estimated separately**.

- **Inquiriesㅁ**
1. Prior to integration, how should the **clinic mapping between AXS and EzServer** be handled?
2. What API should be used to **upload 2D/3D images (including IO Scanner images) from EzServer to AXS**? (No relevant endpoint is currently available in the provided AXS API.)
- Given the large file size of image data, a dedicated upload mechanism such as **AWS S3 Pre-signed URL** is anticipated to be required. Is there a AXS's supported approach for this?
1. After uploading an IO Scanner image (Case), should the **Lab Order be placed immediately**, or handled as a **separate subsequent step**? (Currently, the AXS API provides an Order API but no Case API.)