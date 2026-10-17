# DAST Report Interpretation — OWASP ZAP

## Scan summary

- Tool: OWASP ZAP Baseline Scan
- Target: Local lab WAF at `http://127.0.0.1:8080`
- Results: 63 PASS, 0 FAIL, 4 warning types, 0 in progress
- Reports: `reports/zap-baseline-report.html` and `reports/zap-baseline-report.json`

## Findings and triage

1. **Content Security Policy (CSP) missing:** Review whether the application needs a CSP header. Validate on normal application responses before deciding the remediation.
2. **Non-Storable Content:** Review caching headers, particularly where responses might contain sensitive data. The observed findings included error responses.
3. **Permissions Policy missing:** Consider a restrictive Permissions Policy where applicable, then validate normal responses.
4. **Cross-Domain Misconfiguration:** Review the affected responses and relevant cross-origin headers to determine whether any unintended cross-origin access is possible.

The scan also reported that `/` returned HTTP 404 rather than the expected HTTP 200. This may be normal for an API-only service and should be checked against the intended routes.

## Interpretation

The baseline scan did not report any FAIL results, but this does not prove that the application is free of vulnerabilities. The warnings require manual triage, and several were associated with HTTP 403 or 404 responses rather than successful application responses.

## Recommended CI/CD integration

Run a ZAP baseline scan against an isolated staging environment using synthetic data. Publish the HTML and JSON reports as build artifacts, compare findings with the accepted baseline, and fail the pipeline for agreed high-confidence security issues. Run authenticated or active scans separately against explicitly authorized targets.

## Scope limitation

This was a baseline scan of the local WAF entry point. It does not establish that authenticated application workflows, authorization logic, or every API endpoint has been tested.
