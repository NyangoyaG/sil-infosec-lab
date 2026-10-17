# SIEM Evidence: WAF SQL Injection Detection

**Date:** 17 October 2026
**Environment:** Local Kali Linux Docker lab
**Source:** OWASP ModSecurity CRS 4.30.0
**Event:** Controlled SQL injection test

## Detection

A controlled SQL injection-style request was sent to the health endpoint through the WAF. The request was blocked with HTTP 403 Forbidden.

- Detection rule: 942100 — SQL Injection Attack Detected via libinjection
- Blocking rule: 949110 — Inbound Anomaly Score Exceeded
- Observed anomaly score: 8
- Blocking threshold: 5
- Endpoint: `/api/v1/health`
- Request parameter: `q`
- Client address recorded by the WAF: `172.18.0.1`

## Response

The WAF denied the request before it could reach the API. The event was recorded in the ModSecurity and Nginx logs.

## Proposed SIEM Alert

Generate an alert when a SQL injection detection rule is triggered and the request is blocked. Increase priority when the same source triggers multiple attack rules or targets several endpoints within a short period.

## Recommended Follow-up

1. Correlate WAF events with gateway and application logs.
2. Preserve timestamps, source addresses, rule IDs, endpoint paths, and HTTP status codes.
3. Monitor repeated blocked requests and investigate suspicious patterns.
4. Validate detections using additional authorized test cases.

## Scope Limitation

This is a local demonstration of WAF detection and logging. A SIEM platform, centralized correlation, and automated alert delivery have not yet been verified by this test.
