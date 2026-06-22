# **Authentication**

# **Authentication guide**

To ensure secure and standardized access to our platform APIs, we use **Azure AD B2C** as our authentication provider.

As a integrator, you need to authenticate using the **OAuth 2.0 Client Credentials Flow**, which is specifically designed for backend-to-backend communication without user interaction.

---

# **Flow Steps (Client Credentials Flow)**

1. Authenticate with Azure AD B2C token endpoint using:
- `client_id`
- `client_secret`
- `scope`
1. **AXS** validates the credentials and issues an **access token**.
2. Uses this **access token** in the `Authorization: Bearer <token>` header when calling our APIs.

---

# **Token validation**

**1. Token Endpoint (Azure AD B2C)**

Environment

- Preproduction/Staging:

https://stgoneportalppr.b2clogin.com/stgoneportalppr.onmicrosoft.com/b2c_1a_partnerIntegration_v1/oauth2/v2.0/token

- Production

https://stgoneportalprd.b2clogin.com/stgoneportalprd.onmicrosoft.com/b2c_1a_partnerIntegration_v1/oauth2/v2.0/token

**2. Request parameters**

| **Parameter** | **Value** |
| --- | --- |
| `grant_type` | `client_credentials` |
| `client_id` | *Provided during your onboarding* |
| `client_secret` | *Provided during your onboarding* |

---

**3. Sample Token Request/Response (cURL)**

```json
 curl -X POST https://stgoneportalppr.b2clogin.com/stgoneportalppr.onmicrosoft.com/b2c_1a_partnerIntegration_v1/oauth2/v2.0/token \  -H"Content-Type: application/x-www-form-urlencoded" \  -d"grant_type=client_credentials" \  -d"client_id=YOUR_CLIENT_ID" \  -d"client_secret=YOUR_CLIENT_SECRET"
```

Response JSON:

```json
{"token_type":"Bearer","expires_in":1800,"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIn..."}
```

---

**4. Using Access Token**

Include the access token in the `Authorization` header of each API call:

```json
GET /orders HTTP/1.1Host: api.axs.straumann.comAuthorization: Bearer eyJ0eXAiOiJKV1Qi...
```

---

# **Common Errors**

| **HTTP Status** | **Meaning** | **Resolution Tip** |
| --- | --- | --- |
| 401 | Unauthorized/Invalid token | Ensure token is valid and correctly set in header |
| 403 | Forbidden | Check scope, roles, or API permissions |
| 400 | Bad request | Check formatting and parameter names in token call |

---

# **Access Token Overview**

Once successfully authenticated via the Client Credentials flow, your application will receive an **OAuth 2.0 access token**.

This token is a **JWT (JSON Web Token)** — a compact, self-contained token that includes information about the client, its permissions, and the token validity window.

---

# **How to use the Token**

Include the access token in the Authorization header of **every API request**:

```json
GET /api/resource HTTP/1.1Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOi...
```

Tokens are valid for **1800 seconds**. After expiry, the app must request a new one using the same client credentials.

---

# **Sample Decoded JWT Payload**

Below is an example decoded access token returned by Azure AD B2C for a client credentials request:

```json
{"aud":"9a942c36-2d72-4e5f-bb86-c1a460b21484","iss":"https://stgoneportaldev.b2clogin.com/15ffdd0b-d70d-43b9-ac10-56bc20deb9e3/v2.0/","exp":1753187433,"nbf":1753185633,"tid":"15ffdd0b-d70d-43b9-ac10-56bc20deb9e3","scp":"User.Read.All File.Read Organization.Read.All Patient.Read Patient.Write","ipaddr":"192.168.1.1","azpacr":"1","sub":"6ab0ba22-a3b1-4d9c-82ae-15e5ab8549c8","oid":"6ab0ba22-a3b1-4d9c-82ae-15e5ab8549c8","ver":"2.0","azp":"69bfd158-bd1a-4f43-bcb0-881365d779d5","iat":1753185633}
```

---

# **Fields explained**

| **Parameter** | **Value** |
| --- | --- |
| `aud` | Audience — identifies the *API* this token is intended for. This must match the `client_id` issued to the requestion service/application. |
| `iss` | Issuer — Azure AD B2C URL that issued the token. |
| `exp` | Expiration — timestamp when the token expires. |
| `nbf` | Not Before — token is not valid before this time. |
| `iat` | Issued At — time the token was issued. |
| `tid` | Tenant ID — Azure AD B2C directory ID. |
| `scp` | Scopes — permissions granted to this token. These correspond to what the client app is allowed to access. |
| `azp` | Authorized party (client ID of the app making the request). |
| `sub/oid` | Subject/Object ID — unique identifier for the client identity (same in client credentials flow). |
| `ver` | Token version. Should be `2.0.` |

---

# **Token Validation**

Backend services should:

- **Validate the token signature** using Azure AD’s public keys
- Verify `aud` **matches your API’s expected audience**
- Validate `scp` if you're doing fine-grained access control

---

# **Onboarding Checklist**

- Receive your `client_id` and `client_secret` from our team.
- Test token generation with your credentials.
- Call API with `Authorization: Bearer <token>` header.
- Handle token expiration (tokens are valid for 1800s by default).