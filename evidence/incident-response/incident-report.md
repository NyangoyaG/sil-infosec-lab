# Incident Report: Simulated PHI Exposure to Public AI

**Incident ID:** SIL-IR-2026-001  
**Status:** Simulated tabletop exercise  
**Severity:** High initially, pending investigation  
**Data note:** No real patient data was used in this exercise.

## 1. Executive Summary

A developer accidentally submitted a prompt containing simulated patient identifiers and clinical notes to an unapproved public AI service while seeking help debugging an application. The event may represent unauthorized disclosure of patient-related information. The actual scope, provider retention, and accessibility of submitted content must be verified.

## 2. Detection and Scope

- **Detection method:** Developer self-report.
- **Time:** Illustrative exercise time, 10:15 EAT; replace with the actual exercise time if known.
- **Potentially affected assets:** Developer workstation, public AI account/session, and the information included in the prompt.
- **Initial assessment:** Treat as a potential data exposure until the information submitted and its sensitivity are confirmed.

## 3. Immediate Response and Containment

1. Thank the developer for reporting the event and stop further submissions.
2. Notify the incident response lead, privacy/compliance team, legal counsel, and relevant data owner.
3. Preserve relevant timestamps, account details, session metadata, and available audit logs.
4. Determine whether real PHI, personal information, credentials, or only synthetic data was submitted.
5. If credentials were exposed, revoke or rotate them and review relevant access logs.
6. Request deletion from the provider where supported, without assuming that this proves all copies have been removed.

## 4. Investigation and Impact Assessment

Establish the data categories and volume involved, the time of submission, the account and provider used, applicable retention and sharing settings, and whether credentials or other sensitive material were included. Correlate available endpoint, identity, network, and AI access logs.

Document missing evidence and distinguish confirmed facts from assumptions. The provider's actual handling and retention of the content must be verified rather than assumed.

## 5. Communications and Notification

Use one incident lead and provide need-to-know updates. The legal and privacy teams should determine applicable contractual, regulatory, and notification obligations based on confirmed facts and jurisdiction.

## 6. Recovery and Preventive Actions

- Provide an approved Enterprise AI route for authorized business use.
- Strengthen data-loss prevention and outbound access controls.
- Test synthetic PHI/PII detection and blocking or redaction policies.
- Train developers on approved AI tools and safe handling of sensitive data.
- Review the incident response process and assign owners and deadlines for corrective actions.

## 7. Closure Criteria

Close the incident only after the scope has been assessed, required containment and credential actions are complete, notification decisions are documented, evidence is preserved, and corrective actions have assigned owners.

**Exercise limitation:** This report describes a simulated scenario. It does not claim that a real PHI exposure occurred or that provider-side deletion or containment has been verified.
