# **Integration Scenarios Guide**

This guide describes supported integration patterns for partner systems connecting with **AXS**.

Currently, AXS supports **backend integrations only** (no UI-based integrations).

---

# **1. Data Producer Integration**

**Backend Integration – One-way inbound**

# **Description**

In this pattern, an integration system acts as a **data sender**, pushing information into AXS. AXS accepts and processes the data, but does not send any response back.

# **Example**

- A cloud provider uploading scans or order information into AXS.

# **Authentication**

- **OAuth 2.0 – Client Credentials Flow** (machine-to-machine; no user context required)

# **Consent**

As data is shared **from the partner system into AXS**, the **partner system is responsible for managing consent** prior to sharing data with AXS.

---

# **2. Data Reader Integration**

**Backend Integration – One-way outbound**

# **Description**

In this pattern, integrators **read data from AXS**, typically for downstream tasks such as printing, manufacturing, or analytics.

These integrations do not update or send feedback back to AXS once the data is consumed.

Two models are supported:

- **Pull-based access** – The consumer system queries AXS using secure APIs.
- **Event-driven access** – The consumer subscribes to specific events (e.g., *order created*, *file generated*).AXS notifies them via **webhooks**, allowing the consumer to pull the relevant data.

AXS remains **stateless** in terms of downstream process awareness.

# **Examples**

- A print partner retrieves a job file once AXS notifies them via webhook.
- A reporting system periodically queries AXS for newly completed orders.

# **Authentication**

- **OAuth 2.0 – Client Credentials Flow** (machine-to-machine)

# **Consent**

As data is shared **from AXS to the partner system**, AXS will release data **only after an organization admin has granted consent**.

This ensures that data sharing aligns with privacy and contractual obligations.

---

# **3. Bidirectional Integration**

**Backend Integration – Two-way interaction**

# **Description**

In this pattern, AXS and the integrating system **exchange data in both directions**, enabling richer workflows, live updates, and status synchronization.

# **Examples**

- An order management system pulls case data from AXS and pushes back order updates.
- A cloud-based print aggregation service retrieves job data from AXS and notifies AXS when a print is completed or fails.

# **Authentication**

- **OAuth 2.0 – Client Credentials Flow**Both systems must authenticate securely, and **entity mapping** is usually involved.

# **Consent**

Since data is exchanged **in both directions**, consent is required at both ends:

- When **partners send data to AXS**, they must ensure their system has **managed consent prior to sharing**.
- When **AXS sends data externally**, it will do so **only after an organization admin has provided consent**.

---

# **Summary Comparison**

| **Integration Type** | **Direction** | **Typical Use Case** | **Authentication** | **Consent Handling** |
| --- | --- | --- | --- | --- |
| **Data Producer** | Inbound (to AXS) | Upload scans, order information | OAuth 2.0 Client Credentials (M2M) | Partner manages consent before sending data |
| **Data Reader** | Outbound (from AXS) | Retrieve job files, reporting, analytics | OAuth 2.0 Client Credentials (M2M) | AXS shares data only after admin provides consent |
| **Bidirectional** | Two-way | Order management, print aggregation workflows | OAuth 2.0 Client Credentials (M2M) | Both sides must ensure consent before data sharing |

---

# **Final Note**

Contact your **AXS point of contact** to further discuss possible integration options.