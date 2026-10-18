# SIEM Implementation Status

## Overview

This document records the implementation and validation status of the SIEM components developed for the SIL Infosec Analyst Assessment.

## Implemented and Verified

### 1. WAF Log Collection
- OWASP ModSecurity WAF logs are collected by Grafana Alloy.
- Alloy forwards the logs to Grafana Loki.
- Loki is accessible locally on `127.0.0.1:3100`.
- WAF logs were successfully queried in Loki.

### 2. SQL Injection Detection
- Created the `WAFSQLInjectionDetected` alert rule.
- The rule searches for ModSecurity rule `942100` in WAF logs over a one-minute window.
- The rule evaluates every 30 seconds.
- Rule health was verified as `ok`, with zero evaluation failures.
- Controlled SQL injection test requests were blocked by the WAF with HTTP `403`.
- The alert was observed transitioning to `firing` in Loki.

### 3. Alert Management and Delivery
- Deployed Prometheus Alertmanager.
- Configured Alertmanager to route alerts to the `local-webhook` receiver.
- Deployed a local Python HTTP webhook receiver for lab validation.
- Verified that Alertmanager received the `WAFSQLInjectionDetected` alert.
- Verified webhook delivery for both `firing` and `resolved` notifications.
- The webhook returned HTTP `200` for received notifications.

## SIEM Event Flow

WAF → Grafana Alloy → Grafana Loki → Loki Alert Rule → Alertmanager → Local Webhook Receiver

## Configuration and Operational Notes

- Loki and Alertmanager host ports are bound to loopback addresses for local lab access.
- Loki data is stored in a Docker volume.
- The alert rule file is stored inside Loki's rules directory and also maintained in the repository.
- The local webhook receiver is a demonstration component, not a production notification service.
- Alert delivery has been validated using controlled test traffic.

## Limitations and Further Work

- Integrate additional log sources, such as authentication, endpoint, and operating system logs.
- Add further detection rules for ransomware indicators and Shadow AI activity.
- Configure production-grade notification channels and escalation procedures.
- Implement monitoring for log ingestion failures and alert delivery failures.
- Review access controls, retention, backup, and recovery procedures before production use.
- Extend detection coverage and test against additional attack scenarios.

## Evidence

Validation was performed using Loki's query and rule APIs, Alertmanager's alerts API, WAF HTTP response codes, and webhook receiver logs.
