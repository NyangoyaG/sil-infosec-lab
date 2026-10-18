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

## Log Retention and Access Controls

### Current State
- WAF security events are visible through Docker container logs.
- Docker uses the `json-file` logging driver.
- The WAF container has no per-container log rotation limits configured.
- Centralized ingestion and SIEM retention policies have not been implemented or verified.

### Recommended Policy
- Configure Docker log rotation with a maximum file size of 10 MB and a maximum of 3 files per container.
- Retain security events according to the organization's approved retention schedule and applicable legal requirements.
- Restrict log access to authorized administrators and security analysts.
- Protect logs from unauthorized modification and deletion.
- Avoid collecting unnecessary sensitive request content.
- Monitor log collection failures, storage capacity and ingestion delays.
- Test that rotated logs remain available for investigation within the approved retention period.

### Validation Status
The current WAF log file was measured at approximately 164 KB. This is a point-in-time measurement, not evidence of a retention policy. The rotation settings above are recommendations and have not yet been deployed or tested.

### Implemented Docker Log Rotation

The live WAF container `sil-waf` now uses the Docker `json-file`
logging driver with `max-size=10m` and `max-file=3`. The container
is healthy and uses the `unless-stopped` restart policy.

Validation performed:
- WAF health endpoint returned HTTP 200.
- Unauthenticated reports request returned HTTP 401.
- SQL injection test returned HTTP 403.
- Docker inspection confirmed the configured log rotation values.

This configures per-container Docker log rotation. Centralized SIEM
ingestion, alert delivery, and compliance retention remain separate
requirements and have not been verified by this change.

The previous container, `sil-waf-original`, is retained in a stopped
state for rollback.
