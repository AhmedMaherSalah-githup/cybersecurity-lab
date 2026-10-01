# Web Application SOC Investigation

## 1. Investigation Overview

This document describes a simulated SOC investigation based on security-relevant behaviors observed during the authorized OWASP Juice Shop laboratory assessment.

The investigation demonstrates how a SOC analyst can correlate web application events and determine whether multiple events form a suspicious activity pattern.

No production incident is claimed.

---

## 2. Investigation Scenario

The simulated investigation begins with a sequence of web application events:

```text
1. Endpoint reconnaissance
2. Requests to unexpected REST paths
3. Repeated HTTP 500 responses
4. Authentication attempts
5. Invalid JWT signature
6. Continued access attempts

Individually, these events may have legitimate explanations.

When correlated by source IP, timestamp, endpoint, and authentication result, they can provide stronger investigative context.


---

3. Initial Indicators

Potential indicators include:

Indicator	Example

Unusual endpoint	/rest/admin
Unknown endpoint	/rest/this-route-does-not-exist
Server error	HTTP 500
Authentication failure	HTTP 401
JWT validation failure	invalid signature
Endpoint enumeration	Multiple unique paths
Authentication endpoint	/rest/user/login


These indicators should be investigated together rather than treated as independent proof of malicious activity.


---

4. Investigation Timeline

A hypothetical timeline for the laboratory scenario:

T+00:00
        |
        | Request to unexpected REST endpoint
        v
T+00:05
        |
        | Additional unknown endpoint requests
        v
T+00:10
        |
        | Repeated HTTP 500 responses
        v
T+00:15
        |
        | Authentication attempt
        v
T+00:16
        |
        | Invalid JWT signature
        v
T+00:20
        |
        | Additional protected-resource access attempts

This timeline is a simulated investigation sequence derived from behaviors observed during testing.

It is not a record of a real production attack.


---

5. Investigation Questions

The SOC analyst should answer the following questions.

Source Analysis

What source IP generated the activity?

Is the source internal or external?

Is the source associated with an approved security scanner?

Is the source associated with a known user?


Endpoint Analysis

Which endpoints were requested?

How many unique endpoints were accessed?

Were administrative or authentication endpoints targeted?

Were nonexistent endpoints requested?


Authentication Analysis

Were authentication attempts successful?

Were multiple accounts targeted?

Were invalid JWTs observed?

Did authentication failures occur before endpoint probing?


Timing Analysis

How quickly did the requests occur?

Were multiple events generated within a short period?

Did the behavior continue after authentication failure?



---

6. Event Correlation

The following correlation model can be used:

Source IP
    |
    +--> Endpoint count
    |
    +--> Request frequency
    |
    +--> HTTP status pattern
    |
    +--> Authentication failures
    |
    +--> JWT validation failures
    |
    v
Investigation Context

A high number of unique endpoints combined with repeated errors and authentication failures provides more context than any single event.


---

7. Example Analyst Investigation

Event A

GET /rest/admin
HTTP 500

Initial interpretation:

Unexpected REST endpoint requested.

This event alone does not establish malicious activity.


---

Event B

GET /rest/this-route-does-not-exist
HTTP 500

Initial interpretation:

Another unexpected REST endpoint was requested.

Correlation with Event A increases the number of unusual paths associated with the same source.


---

Event C

POST /rest/user/login
HTTP 401

Initial interpretation:

Authentication failure.

The analyst should determine whether the authentication attempt is related to the earlier endpoint activity.


---

Event D

Protected endpoint
HTTP 401
Authentication error: invalid signature

Initial interpretation:

JWT validation failed.

The analyst should determine whether this was caused by an expired client token, malformed state, application testing, or possible token manipulation.


---

8. Evidence Collection

During an investigation, preserve relevant evidence before modifying the environment.

Recommended evidence includes:

HTTP access logs
Application logs
Authentication events
Reverse-proxy logs
Web application firewall events
Relevant request paths
HTTP status codes
Timestamps
User-agent values
Source IP information

Sensitive authentication tokens should not be copied into public GitHub repositories.

If tokens must be referenced in an internal investigation, they should be redacted.


---

9. Investigation Findings

Based on the laboratory behaviors observed during the assessment:

Finding 1 — Endpoint Reconnaissance

Unexpected REST endpoints generated server-side error responses.

This behavior is useful as a reconnaissance indicator when repeated across multiple paths.

Finding 2 — Authentication Protection

Protected authentication-related functionality returned HTTP 401 when authorization was missing.

Finding 3 — JWT Validation

A valid laboratory JWT allowed authenticated access, while an invalid signature was rejected.

Finding 4 — Verbose Errors

Unexpected REST paths generated detailed error responses containing application and framework information.


---

10. Analyst Assessment

The available laboratory evidence supports the conclusion that the application generates security-relevant signals that can be monitored by a SOC.

The evidence does not by itself establish that a real attacker compromised the application.

Further investigation would require correlation with source IP information, timestamps, authentication logs, and surrounding application activity.


---

11. Recommended Response

If similar correlated activity were observed in a production environment, the analyst should:

1. Validate the source and context.


2. Determine whether the source is authorized.


3. Preserve relevant logs.


4. Identify affected accounts and endpoints.


5. Review authentication activity.


6. Check for successful access following failed attempts.


7. Review application and reverse-proxy logs.


8. Escalate according to the organization's incident-response process.


9. Apply remediation after evidence preservation.


10. Document the investigation and final disposition.




---

12. Investigation Limitations

This investigation has several limitations:

The target application runs in an isolated local laboratory.

No production SIEM was deployed.

The investigation does not represent a real-world compromise.

Source IP analysis is limited by the local laboratory architecture.

The simulated timeline is not a historical production timeline.

Detection thresholds require tuning against normal traffic.


These limitations should be considered when interpreting the results.


---

13. SOC Learning Outcomes

This investigation demonstrates the ability to:

Analyze web application security events

Correlate multiple HTTP indicators

Investigate authentication failures

Analyze JWT validation failures

Identify endpoint reconnaissance patterns

Preserve security evidence

Distinguish suspicious behavior from confirmed compromise

Document an investigation professionally


The investigation methodology can be adapted to SIEM platforms such as Splunk, Elastic Security, Microsoft Sentinel, or Wazuh.
