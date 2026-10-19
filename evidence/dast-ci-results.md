
# CI/CD DAST Results — OWASP ZAP

## Scan Summary

- **Platform:** GitHub Actions
- **Workflow:** Security Scans
- **Commit:** `61b1419`
- **Tool:** OWASP ZAP Baseline Scan
- **ZAP version:** 2.17.0
- **Target:** `http://127.0.0.1:8080/`
- **Target type:** Disposable Nginx test container
- **Workflow result:** Success
- **Total workflow duration:** 1 minute 21 seconds
- **Artifacts:** 2 reported by GitHub Actions
- **High-risk alerts:** 0
- **Medium-risk alerts:** 2
- **Low-risk alerts:** 7
- **Informational alerts:** 1
- **False positives:** 0 reported

## Medium-Risk Findings

### 1. Content Security Policy (CSP) Header Not Set

- **Instances:** 3
- **Risk:** Medium
- **Description:** The scanned responses did not provide a Content Security Policy header.
- **Recommended action:** Define an appropriate CSP for the actual application, test it in report-only mode where supported, and enforce it after validating legitimate content sources.

### 2. Missing Anti-clickjacking Header

- **Instances:** 1
- **Risk:** Medium
- **Description:** A response lacked the expected anti-clickjacking protection.
- **Recommended action:** Review whether the application must be embedded in frames. Where appropriate, implement a CSP `frame-ancestors` policy or `X-Frame-Options` header and verify the resulting behavior.

## Other Findings

The report also identified seven low-risk alerts and one informational alert. These included:

- Missing or invalid cross-origin policy headers.
- Missing Permissions Policy header.
- Server version information disclosure.
- Missing `X-Content-Type-Options` header.
- An informational finding concerning storable and cacheable content.

These findings require contextual review against the actual application before remediation decisions are made.

## Interpretation

The GitHub Actions workflow completed successfully. Secret scanning, SAST, software composition analysis, and the DAST job all passed.

The ZAP report recorded no high-risk alerts, but this does not establish that the target is vulnerability-free. A successful workflow indicates that the configured jobs completed according to their current settings; it is not equivalent to a security certification.

## Scope Limitations

The DAST job scanned a disposable Nginx container rather than the project's FastAPI API or ModSecurity WAF. Consequently, these findings are evidence of the CI/CD DAST integration test only.

They must not be represented as results from testing the actual application.

The scan did not establish coverage of authenticated API routes, authorization controls, AI guardrails, sensitive-data handling, or business logic.

## Next Actions

1. Configure an isolated staging environment for the actual application.
2. Run OWASP ZAP against the staging API and WAF using synthetic test data.
3. Review findings by risk, confidence, affected endpoint, and practical exploitability.
4. Publish HTML and JSON reports as GitHub Actions artifacts.
5. Define agreed security thresholds for pipeline failures.
6. Retain scan results and document remediation or accepted risks.

