# SIL Infosec Analyst Assessment V2
## Implementation Status Report

**Environment:** Kali Linux  
**Project:** `sil-infosec-lab`  
**Purpose:** Document implemented security controls, test results, and outstanding work.

## 1. API Service

- Implemented a FastAPI demonstration service.
- Created `GET /api/v1/health`.
- Created `GET /api/v1/reports/summary`.
- Used synthetic demonstration data.
- Containerized the API using Docker.
- Connected the API to a dedicated Docker network.

## 2. API Gateway Security

- Deployed Kong Gateway in DB-less mode.
- Configured routes to the FastAPI service.
- Protected the reports endpoint using API key authentication.
- Configured a rate limit of five requests per minute.
- Verified that unauthenticated reports requests return HTTP 401.
- Verified that authenticated requests succeed.
- Verified that requests exceeding the configured limit return HTTP 429.
- Confirmed that the health endpoint remains accessible without an API key.

## 3. Web Application Firewall

- Deployed the OWASP ModSecurity Core Rule Set container.
- Enabled the ModSecurity rule engine.
- Verified that legitimate health requests pass through the WAF.
- Tested a SQL injection-style input that was blocked with HTTP 403.
- Reviewed WAF logs and identified the triggered detection rule.
- Verified that API authentication is still enforced by Kong behind the WAF.

## 4. AI Security Guardrails

- Created a local Python guardrails proof of concept.
- Implemented basic prompt-injection pattern detection.
- Implemented email and phone-number redaction.
- Tested input inspection and output redaction.
- Tested a legitimate business request.
- Saved the test results in `evidence/ai-guardrails/test-results.md`.

## 5. Verified Test Outcomes

| Control | Observed result |
|---|---|
| Health endpoint | HTTP 200 |
| Reports endpoint without API key | HTTP 401 |
| Reports endpoint with valid demo key | HTTP 200 |
| Requests exceeding rate limit | HTTP 429 |
| SQL injection-style WAF test | HTTP 403 |
| Prompt-injection pattern test | Blocked |
| Input PII redaction | Passed |
| Output PII redaction | Passed |
| Legitimate business request | Allowed |

## 6. Limitations and Outstanding Work

- The API key is for demonstration purposes only.
- The current API uses synthetic data and is not a production application.
- The AI guardrails use basic regular expressions and are not comprehensive.
- The AI guardrails are not yet integrated with a live AI model.
- Confirm the active WAF configuration and document the deployed request path.
- Capture and organize supporting screenshots, logs, and command outputs.
- Continue with the remaining assessment requirements, including security testing, monitoring, software supply-chain security, secrets management, and secure AI development practices.

## 7. Current Architecture

Client → OWASP WAF → Kong API Gateway → FastAPI Service

The WAF and Kong proxy are bound to localhost on the host machine. The API service is accessible through the internal Docker network rather than a published host port.

## 8. Evidence and Reporting

AI guardrails test report:

`evidence/ai-guardrails/test-results.md`

Architecture and implementation planning files are maintained under the project directory.

## 9. Status Summary

The API, gateway authentication, rate limiting, WAF blocking test, and local AI guardrails have been implemented and tested in a demonstration environment. Remaining controls and assessment requirements must be completed and verified before the project can be considered complete.

**Document status:** Work in progress.
## 10. Rate-Limiting Verification Through WAF

**Test date:** 17 October 2026  
**Request path:** Client → WAF → Kong Gateway → FastAPI

### Test Procedure
Sent six consecutive authenticated requests to the reports endpoint through the WAF at `127.0.0.1:8080`.

### Observed Results

| Request | HTTP Status | Result |
|---|---|---|
| 1 | 200 | Allowed |
| 2 | 200 | Allowed |
| 3 | 200 | Allowed |
| 4 | 200 | Allowed |
| 5 | 200 | Allowed |
| 6 | 429 | Rate limit enforced |

**Expected behavior:** Requests are accepted until the configured limit of five requests per minute is reached. Subsequent requests are rate-limited.

**Observed behavior:** The first five requests returned HTTP 200, and the sixth returned HTTP 429 Too Many Requests.

**Status:** PASS

**Evidence:** Terminal output from the six-request test.

### Conclusion
The test confirms that Kong's configured rate-limiting control is enforced when requests pass through the WAF. This is a local demonstration; production deployment would require further validation of distributed rate limiting, monitoring, and operational controls.

## 11. WAF SQL Injection Detection Evidence

### Test Procedure
Sent a SQL injection-style query parameter to the health endpoint through the WAF:

`GET /api/v1/health?q=1' OR '1'='1`

### Observed Results

- **HTTP response:** `403 Forbidden`
- **Detection rule:** `942100`
- **Detection message:** SQL Injection Attack Detected via libinjection
- **Blocking rule:** `949110`
- **Inbound anomaly score:** 8
- **Blocking threshold:** 5
- **OWASP CRS version:** 4.30.0

### Conclusion
The WAF detected the SQL injection-style input and blocked the request. The logs identify the detection rule and confirm that the inbound anomaly score exceeded the configured blocking threshold.

**Status:** PASS

**Evidence source:** Docker logs from the `sil-waf` container.

**Scope limitation:** This test confirms detection of the specific payload tested. It does not establish protection against every SQL injection technique.

## 12. Docker Container Restart Policies

### Configuration
Configured the following containers with the Docker restart policy `unless-stopped`:

- `sil-waf`
- `sil-kong-gateway`
- `sil-assessment-api`

### Verification
Verified the configuration using `docker inspect`.

**Observed result:** All three containers report `unless-stopped`.

**Status:** PASS

### Security and Operational Note
The restart policy improves service recovery after Docker daemon restarts and unexpected container exits. It does not replace health checks, monitoring, dependency management, or recovery testing.

## 13. API Container Health Check

### Configuration
Configured a Docker health check for `sil-assessment-api` using Python's standard library to request the internal endpoint:

`http://127.0.0.1:8000/api/v1/health`

- Check interval: 30 seconds
- Check timeout: 5 seconds
- Start period: 10 seconds
- Retries: 3

### Verification
- Docker reports the API container as `healthy`.
- The configured health-check command was verified using `docker inspect`.
- A request through the WAF and Kong gateway returned HTTP 200.
- The response reported the API service status as `healthy`.

**Status:** PASS

### Operational Note
The health check verifies that the API health endpoint responds successfully from inside the container. It complements the `unless-stopped` restart policy but does not, by itself, restart an unhealthy container or verify every API function.

**Evidence sources:** Docker container status, Docker inspection output, and the successful health endpoint request through the WAF.

## 14. Restricting Direct Access to Kong

### Security Improvement
Recreated the Kong Gateway container without publishing its proxy port on the host. Kong remains accessible to the WAF over the internal Docker network `sil-api-network`.

### Verification Results

- Direct request to `127.0.0.1:8000/api/v1/health`: curl returned HTTP `000`, with no HTTP response.
- Health request through the WAF at `127.0.0.1:8080/api/v1/health`: HTTP `200`.
- Reports request through the WAF without an API key: HTTP `401`.
- Authenticated reports request through the WAF: HTTP `200`.
- Kong container status: healthy.

**Status:** PASS

### Security Benefit
Removing the host port publication prevents direct access to Kong through the host's port 8000. Requests through the intended local entry point must use the WAF.

### Scope Limitation
This change removes the host port mapping; it does not prove that Kong is unreachable from every possible network path. Docker network access and host-level controls should be reviewed as part of a production deployment.

**Evidence sources:** Docker container inspection, container status output, and HTTP tests through the WAF and against the former direct Kong endpoint.

## 15. API Security Hardening and Deployment Verification

**Objective:** Remediate the container security finding and verify the hardened API deployment.

### Dockerfile Hardening
- Added a dedicated non-root account named `appuser` with UID 10001.
- Configured the container to run the application using `USER appuser`.
- Built the hardened image `sil-assessment-api:1.1`.
- Verified the image runs under UID 10001.

### Static Application Security Testing (SAST)
- Tool: Semgrep OSS.
- Scan command: `semgrep scan --config auto api/`
- Files scanned: 3 Git-tracked files.
- Rules executed: 296.
- Findings: 0.
- Result: The scan completed successfully with zero findings. This result applies only to the files and rules scanned and does not establish that the entire project is vulnerability-free.

### Deployment Verification
- Deployed image: `sil-assessment-api:1.1`.
- Container health: Healthy.
- Runtime identity: `appuser` (UID 10001, GID 10001).
- API health endpoint through WAF and Kong: HTTP 200 OK.
- Reports endpoint without API key: HTTP 401 Unauthorized.
- Reports endpoint with the configured demonstration API key: HTTP 200 OK.
- Kong rate-limiting headers confirmed a limit of 5 requests per minute.

### Outcome
The API was redeployed successfully with non-root execution. Health checks, gateway routing, API-key authentication, and rate-limiting behavior were verified after deployment. The previous image `sil-assessment-api:1.0` remains available for rollback.

**Limitations:** The API key is a hardcoded demonstration credential and must not be used in production. Further security testing, secrets management, dependency vulnerability assessment, and production monitoring remain necessary.

## 16. AI Guardrails API Integration and Verification

### Implementation
- Packaged the existing guardrails module into the API image.
- Added `POST /api/v1/ai/inspect`.
- Added a request text limit of 4,000 characters.
- Integrated input inspection and output PII redaction.
- Configured the Kong route for `/api/v1/ai/inspect` with the POST method.
- Preserved the API's non-root execution using `appuser` (UID 10001).

### Verification Results

| Test | Observed Result | Status |
|---|---|---|
| Legitimate AI inspection request through WAF and Kong | HTTP 200 | PASS |
| Prompt-injection test through WAF and Kong | HTTP 400 | PASS |
| Email redaction | Email replaced with `[REDACTED_EMAIL]` | PASS |
| Phone redaction | Phone replaced with `[REDACTED_PHONE]` | PASS |
| Health endpoint on new image | HTTP 200 | PASS |
| Reports endpoint on new image | HTTP 200 in direct container test | PASS |
| Container runtime identity | UID 10001 (`appuser`) | PASS |
| Production API container | Image `sil-assessment-api:1.3`, healthy | PASS |

### Limitations
- The endpoint uses a simulated response and does not call a live AI model.
- Prompt-injection detection relies on limited regular-expression patterns and is not comprehensive.
- Email and phone detection may miss some formats or incorrectly match benign text.
- The AI route now has a Kong API-key authentication plugin; production readiness still requires broader security testing, secrets management, dependency scanning, monitoring, and secure AI controls.
- Production readiness still requires broader security testing, secrets management, dependency scanning, monitoring, and secure AI controls.

### Conclusion
The demonstration AI guardrails are integrated into the API and reachable through the WAF and Kong gateway. The tested prompt-injection pattern is blocked, and tested email and phone values are redacted. These results validate the tested cases only and do not establish comprehensive AI security.

Demo credential warning: The Kong configuration contains the hardcoded demonstration API key SIL-DEMO-KEY-2026. It is intended for this lab only and must not be reused in production. Production deployment should use securely managed credentials, rotation, and appropriate access controls.

## 17. AI Route Authentication Hardening

- Added Kong `key-auth` to `sil-ai-inspect-route`.
- AI inspection requests without an API key were rejected with HTTP 401.
- AI inspection requests with the configured lab key returned HTTP 200.
- Reports requests without an API key continued to return HTTP 401.
- Reports requests with the configured lab key returned HTTP 200 and synthetic demonstration data.
- Kong configuration validation completed successfully using `kong config parse`.
- Kong restarted successfully and returned to a healthy state.

### Remaining Limitations

- `SIL-DEMO-KEY-2026` remains a hardcoded demonstration credential in the Kong declarative configuration.
- The same lab key is used by both protected routes; separate credentials and rotation should be considered.
- The AI inspection endpoint still uses a simulated response and limited regular-expression guardrails.
- These tests validate the tested authentication cases only and do not establish comprehensive security.
