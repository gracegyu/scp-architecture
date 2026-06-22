# **Getting Started with AXS APIs**

# **1. Prerequisites**

- Active Developer Account (provided by Straumann) (see below).
- Registered client application (see below).
- Basic understanding of REST APIs.

# **2. Registering a Client Applicationand getting a Developer Account**

To integrate with AXS, you must have an active account and your application must be registered before you can access any APIs.

To get the process started, please send an email to **support-axs@straumann.com** with the following information:

- Your **full name**
- **Company name** -The **email address** associated to your developer account.
- **Application name** (integration name).
- **Intended roles or API calls** the application will perform.

Once your request is processed, you will receive an invitation to log in and manage your integration credentials.

**Important notes:**

- The AXS team will review your request and **whitelist your application** before enabling access.
- **Unregistered clients are blocked** and cannot interact with AXS services.

# **3. Making Your First API Call**

Once you are registered and authenticated, you can start interacting with the AXS APIs.

Each API request must include the `Organization-ID` header, which specifies the unique identifier of the target organization.

Example request:

```
GET /orders HTTP/1.1Host: api.axs.straumann.comAuthorization: Bearer <your-access-token>Organization-ID: <your-organization-id>
```

# **4. Next Steps**

- Refer to the **Authentication Guide** to learn how to obtain and use access tokens.
- Explore available APIs in the **APIs** section.
- Contact support-axs@straumann.com for troubleshooting.