# **Webhooks**

AXS provides **event-driven integration** through webhooks.

This enables your system to receive notifications whenever events occur — for example, when a **patient is created** or an **order is updated**.

---

# **1. Subscribing for Notifications**

Integrators must register their webhook endpoints using the **Webhook Subscription API**.

# **Request Example**

```
POST /v1/webhooks/subscribe HTTP/1.1Authorization: Bearer <your-access-token>Content-Type: application/json{  "events": ["patient.created", "order.updated"],  "callback": "https://your.api/callback",  "hmac": "shared-secret"}
```

> **Note:** The `hmac` field will be moved to a more secure workflow in the future.
> 

---

# **2. Subscription Parameters**

# **Callback URL**

A publicly accessible **HTTPS endpoint** to receive webhook notifications.

# **Event List**

One or more event types you wish to subscribe to. **Example values:**

- `patient.created`
- `order.updated`
- `patient.all`

# **HMAC Secret**

A shared secret string used to verify the authenticity of incoming messages.

---

# **3. Receiving Events**

When an event occurs, AXS sends an **HTTP POST** request to your callback URL with the following payload:

```json
{"source":"axs","messageId":"c2f8aaf5-d6d1-4f8c-a4a8-c4e9b3cb3545","timestamp":"2025-06-25T12:34:56Z","eventType":"patient.created","operationId":"123","organizationId":"0040694997","data":{"patient":{}},"patientId":"a5437cb7-fffd-4cb2-8fdd-4063b5e43dae","organizationId":"0040694997"}
```

---

# **4. HMAC Signature**

Each webhook request includes a **`Signature`** header for message integrity.

# **How It Is Generated**

1. Convert the payload to a minified JSON string.
2. Apply **HMAC-SHA512** hashing using your shared secret.
3. Example result (with secret `abcd`):

```
71cb563082c57e645c198027e058be704b3923988f6751566e078a76d73af6493d6cbc3aaf2b3b78fb8b4543bb1d946ddc4dd3bc8c88bca5862634e3921037fd
```

1. AXS sends this in the request header:

```
Signature: <calculated-HMAC>
```

---

# **5. Security Expectations**

- Callback URLs **must use HTTPS**.
- Always **validate the HMAC signature** before processing payloads.
- Use **`messageId`** for idempotency to avoid duplicate processing.

---

# **6. Failure & Retry Policy**

If the callback fails or times out:

- AXS retries automatically using **exponential backoff**.
- **Retries** are automatic re-deliveries of a webhook event when the receiving system fails to acknowledge it.
- Messages will be resent up to three times if they are not acknowledged, with a 15-minute interval between each attempt.
- After **3 failed attempts**, the message is moved to the **Dead Letter Queue (DLQ)**.
- The **Dead-Letter-Queue (DLQ)** is the special queue used in the messagnig system to hold the **messages that could not be processed successfully.**
- You should monitor the health of your callback endpoints.

---

# **7. Subscriber Implementation Guide**

Below are sample implementations to help you validate webhook requests.

---

# **Java (Spring Boot)**

```java
import javax.crypto.Mac;import javax.crypto.spec.SecretKeySpec;import java.util.Base64;public boolean validateSignature(String payload, String signature, String secret) throws Exception {    Mac sha512_HMAC = Mac.getInstance("HmacSHA512");    SecretKeySpec keySpec = new SecretKeySpec(secret.getBytes(), "HmacSHA512");    sha512_HMAC.init(keySpec);    byte[] hash = sha512_HMAC.doFinal(payload.getBytes());    String calculated = bytesToHex(hash);    return calculated.equalsIgnoreCase(signature);}private String bytesToHex(byte[] bytes) {    StringBuilder sb = new StringBuilder();    for (byte b : bytes) {        sb.append(String.format("%02x", b));    }    return sb.toString();}
```

---

# **Node.js**

```jsx
const crypto=require("crypto");functionvalidateSignature(payload, signature, secret){const hash= crypto.createHmac("sha512", secret).update(payload).digest("hex");return hash=== signature;}
```

---

# **Python**

```python
import hmacimport hashlibdefvalidate_signature(payload:str, signature:str, secret:str)->bool:    hash_bytes= hmac.new(secret.encode(), payload.encode(), hashlib.sha512).hexdigest()return hmac.compare_digest(hash_bytes, signature)
```

---