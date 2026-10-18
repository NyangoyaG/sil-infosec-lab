# SIEM Detection Use Cases: Ransomware and Shadow AI

## 1. Ransomware detection

**Log sources:** Endpoint detection and response (EDR), process events, file-integrity monitoring, backup systems, identity logs and firewall events.

**Detection logic:**
- Detect unusually high file modification or rename rates compared with the endpoint's normal baseline.
- Correlate suspicious process activity with attempts to delete recovery snapshots or tamper with backups.
- Raise a critical alert when multiple independent ransomware indicators occur together.

**Response:**
1. Validate the alert and identify affected endpoints and accounts.
2. Isolate confirmed or strongly suspected compromised endpoints using approved response procedures.
3. Preserve relevant endpoint, identity and network evidence.
4. Protect backup systems and investigate lateral movement.
5. Eradicate the threat and validate recovery before reconnecting systems.

## 2. Shadow AI detection

**Log sources:** DNS, secure web gateway or proxy, firewall, endpoint, identity and data-loss-prevention (DLP) events.

**Detection logic:**
- Compare destinations against an approved AI-provider allowlist.
- Alert when a user or device accesses a known consumer AI service that is not approved by organizational policy.
- Increase priority when the event correlates with a DLP alert, sensitive-data upload or repeated policy violations.

**Response:**
1. Validate the destination and the applicable organizational policy.
2. Determine whether sensitive information may have been transmitted.
3. Preserve relevant metadata while minimizing collection of prompt content.
4. Apply proportionate controls and notify the appropriate security and privacy stakeholders.
5. Offer an approved alternative and document the outcome.

## 3. Validation plan

Use synthetic events and benign test files in an isolated lab. Confirm that the source logs contain the expected event fields, the SIEM parses them correctly, the detection rule fires, and the response workflow is documented.

## Implementation status

These are proposed detection use cases and response procedures. Ransomware detection, Shadow AI alerting, and automated SIEM response have not been verified as deployed in this lab.

## 4. SIEM Implementation Roadmap

1. Select and deploy a SIEM or centralized log-collection platform appropriate for the available lab resources.
2. Onboard the existing WAF security logs as the first log source.
3. Validate ingestion using a controlled SQL injection test event and confirm that the event includes the timestamp, source address, rule ID, request path, and blocking result.
4. Configure and test an alert for repeated WAF attack detections.
5. Document ransomware and Shadow AI detection as planned use cases until their required log sources and alert rules are operational.
6. Record test results and limitations as assessment evidence.

**Current status:** WAF log generation and Docker log rotation are implemented. Centralized ingestion and SIEM alerting remain outstanding.
