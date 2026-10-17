# SIEM Log-Source Onboarding: WAF

## Objective
Document the onboarding and validation process for Web Application Firewall security events.

## Log source
- Source: OWASP ModSecurity WAF
- Environment: Local Docker lab
- Technology: ModSecurity with OWASP Core Rule Set
- Event type: Blocked SQL injection test
- Observed result: HTTP 403 Forbidden

## Validation evidence
A controlled SQL injection-style request triggered ModSecurity rule 942100. Rule 949110 blocked the request after the inbound anomaly score reached 8, exceeding the configured threshold of 5.

The event included a timestamp, request URI, client address, matched rule, severity, response status and unique transaction ID.

## Proposed SIEM onboarding procedure
1. Identify the source owner, log format, expected event volume, sensitivity and retention requirements.
2. Configure a supported collector to forward WAF audit and security events securely to the SIEM.
3. Normalize timestamps, source address, request path, rule ID, action, response status and transaction ID.
4. Generate controlled allowed and blocked requests and confirm that the source and SIEM contain matching events.
5. Measure ingestion delay and check parsing errors, dropped events, collector outages and time synchronization.
6. Alert on missing logs or abnormal changes in event volume.
7. Restrict access to logs and avoid collecting unnecessary sensitive request content.

## Status and limitation
WAF detection and local log generation were demonstrated in this lab. Centralized SIEM ingestion, parsing and automated alert delivery have not yet been verified. They remain deployment and validation tasks.
