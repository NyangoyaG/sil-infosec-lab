# SIL Infosec Analyst Assessment
## Section 1A: API Gateway and AI Guardrails
### Technical Implementation Plan

## 1. Objective

The objective is to implement a secure API architecture that protects incoming application traffic, enforces authentication and authorization, safeguards sensitive data, controls outbound requests to enterprise AI services, and centralizes security monitoring.

The proposed architecture includes:
- A Web Application Firewall (WAF) to inspect incoming HTTP/S traffic.
- An API Gateway to authenticate requests, enforce rate limits, and route traffic.
- An Identity Provider (IdP) supporting OAuth 2.0, OpenID Connect (OIDC), and Multi-Factor Authentication (MFA).
- Two API services demonstrating protected endpoints.
- A private database accessible only by authorized application services.
- An Enterprise AI Proxy enforcing input and output security controls.
- A Secrets Manager for API keys and application credentials.
- A Security Information and Event Management (SIEM) platform for centralized logging and alerting.

## 2. Implementation Approach

## Deployment Platform and Cloud Preference

The proof of concept is deployed locally using Docker containers to demonstrate the WAF, API Gateway, API services, authentication controls, and security testing. The target architecture is cloud-ready and can be deployed on a major cloud platform using private networking, managed secrets, centralized logging, and restricted outbound access to approved Enterprise AI services.

Cloud provider selection will depend on organizational requirements, existing contracts, data residency, regulatory obligations, operational capability, and total cost of ownership. Production deployment will require validation of the proposed controls and services in the selected environment.

### Phase 1: Establish the Network and Security Boundaries

1. Place the WAF in front of the API Gateway to inspect incoming HTTP/S requests.
2. Configure the API Gateway as the single controlled entry point for the demonstration APIs.
3. Restrict direct access to API services so that requests must pass through the gateway.
4. Place the database on a private network and permit access only from authorized application services.
5. Configure outbound network access so AI-related traffic can reach only the approved Enterprise AI Proxy and authorized AI provider endpoints.

### Phase 2: Configure Authentication and API Protection

1. Integrate the API Gateway with an Identity Provider using OAuth 2.0 or OpenID Connect.
2. Validate access tokens, including issuer, audience, signature, and expiry.
3. Require appropriate authorization for protected API operations.
4. Apply rate limits and request-size limits to reduce abuse and denial-of-service risk.
5. Return generic error responses to clients while recording useful diagnostic details securely in server logs.

### Phase 3: Deploy the Demonstration APIs

1. Deploy API Service A with a health-check endpoint.
2. Deploy API Service B with a reports-summary endpoint.
3. Validate request methods, parameters, and content types.
4. Use synthetic test data and enforce least-privilege database access.
5. Test successful requests, invalid requests, unauthorized requests, and rate-limit enforcement.

### Phase 4: Implement AI Guardrails

1. Route AI requests through the Enterprise AI Proxy rather than allowing direct application-to-provider connections.
2. Inspect incoming prompts for suspicious prompt-injection patterns.
3. Detect and block prohibited sensitive data, including configured personally identifiable information (PII) and protected health information (PHI) patterns.
4. Inspect AI responses before returning them to the requesting application.
5. Apply data minimization, safe error handling, and audit logging.
6. Block outbound AI requests by default unless they use an approved destination and policy.

### Phase 5: Centralize Logging and Monitoring

1. Collect security events from the WAF, API Gateway, Identity Provider, API services, and AI Proxy.
2. Forward relevant events to the SIEM.
3. Alert on repeated authentication failures, unusual request rates, suspected prompt injection, sensitive-data policy violations, and unexpected outbound connections.
4. Avoid logging access tokens, passwords, API keys, or unnecessary sensitive request and response content.
5. Test that alerts are generated and that analysts can trace events across the request flow.

## 3. Verification and Acceptance Criteria

The implementation will be considered successful when the following tests pass:

| Test Area | Verification | Expected Result |
|---|---|---|
| WAF | Send benign and controlled malicious test requests | Benign traffic is allowed; configured attack patterns are blocked |
| API Gateway | Submit valid and invalid requests | Valid requests are routed correctly; invalid requests are rejected |
| Authentication | Submit requests with missing, invalid, and expired tokens | Protected operations reject unauthorized requests |
| Rate Limiting | Exceed the configured request threshold | Excess requests receive HTTP 429 responses |
| Database Security | Attempt direct access from an unauthorized network or service | Direct access is denied |
| AI Input Guardrails | Submit synthetic prompt-injection test cases | Suspicious inputs are detected or handled according to policy |
| Sensitive Data Protection | Submit synthetic PII/PHI test patterns | Policy violations are blocked or redacted as configured |
| AI Output Guardrails | Simulate an AI response containing prohibited sensitive data | The response is blocked or redacted before release |
| Secrets Management | Inspect application configuration and source code | No real credentials or API keys are hardcoded |
| SIEM Integration | Generate test security events | Events arrive in the SIEM and trigger the expected alerts |
| Logging | Inspect application and gateway logs | Useful audit records exist without exposing secrets or unnecessary sensitive data |

### 4. Security and Operational Considerations

- Apply least privilege to service accounts, database permissions, and infrastructure access.
- Use TLS for data in transit and encryption at rest where supported.
- Store credentials in a dedicated secrets-management solution.
- Keep software and dependencies updated and scan them for known vulnerabilities.
- Apply request-size limits, timeouts, and appropriate resource limits.
- Establish retention and access policies for security logs.
- Test security controls regularly and document exceptions or residual risks.

### 5. Limitations and Residual Risks

This local demonstration validates selected security behaviours, but it does not establish production readiness by itself.

- WAF signatures may miss novel or obfuscated attacks.
- Prompt-injection detection cannot guarantee that every malicious instruction will be identified.
- Pattern-based PII/PHI detection may miss context-dependent or previously unseen sensitive data.
- SIEM alerts require tuning to reduce false positives and false negatives.
- Production deployment requires additional resilience, access-control testing, operational monitoring, and security review.
