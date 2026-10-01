# Web Application Threat Hunting

## 1. Purpose

This document defines threat hunting hypotheses for the local OWASP Juice Shop security lab.

The objective is to proactively identify suspicious web application activity by correlating:

- Endpoint reconnaissance
- Authentication abuse
- Repeated HTTP 5xx responses
- Invalid JWT signatures
- Suspicious REST endpoint access
- Repeated authentication failures

All activity described in this document is based on an authorized local laboratory environment.

---

## 2. Hunting Scope

### Target

OWASP Juice Shop running locally inside Docker.

### Environment

- Host: Ubuntu 24.04 LTS
- Target: OWASP Juice Shop
- Target address: `127.0.0.1:3000`
- Deployment: Docker
- Testing tools: Nmap, WhatWeb, cURL, Python

### Data Sources

Potential hunting data sources include:

- Web access logs
- Authentication logs
- Application logs
- HTTP status codes
- Source IP addresses
- Requested paths
- HTTP methods
- User-Agent values
- Authentication results
- JWT validation results

---

# 3. Threat Hunting Methodology

The hunting workflow used in this project is:

```text
Hypothesis
    ↓
Collect telemetry
    ↓
Filter suspicious activity
    ↓
Correlate events
    ↓
Investigate context
    ↓
Determine security significance
    ↓
Recommend response

Threat hunting is different from simple alert monitoring.

Detection rules wait for known conditions.

Threat hunting proactively searches for suspicious patterns that may not yet have generated an alert.


---

4. Hunting Hypothesis 1 — Endpoint Reconnaissance

Hypothesis

An attacker performing application reconnaissance may request multiple unusual or non-existent REST endpoints in a short period.

Examples include:

/rest/admin
/rest/debug
/rest/internal
/rest/test
/rest/unknown

Expected Telemetry

Relevant fields:

timestamp
source_ip
http_method
request_path
status_code
user_agent

Suspicious Pattern

A possible reconnaissance pattern is:

Multiple unique paths
        +
Unusual endpoint names
        +
Repeated HTTP 4xx/5xx responses
        +
Same source IP

Lab Evidence

During the authorized lab assessment, requests to unknown /rest paths generated HTTP 500 responses.

The application returned verbose error information including framework and internal application path details.

This behavior was documented in the penetration testing report.

Hunting Query Concept

A SIEM implementation could search for:

source_ip = same
AND
unique(request_path) > threshold
AND
status_code >= 400

A practical starting threshold is:

5 or more suspicious paths
within a short time window

Thresholds should be tuned using normal application traffic.

Analyst Questions

The analyst should ask:

1. Is the source IP expected?


2. Is the activity from a known scanner?


3. Are the requested paths normally used by the application?


4. Are many requests returning 404 or 500?


5. Did authentication failures occur from the same source?


6. Did the activity occur before another suspicious action?




---

5. Hunting Hypothesis 2 — Authentication Abuse

Hypothesis

Repeated failed login attempts against the same authentication endpoint may indicate password guessing, credential testing, automation, or another authentication-related problem.

Example Endpoint

/rest/user/login

Suspicious Pattern

Same source IP
        +
Repeated POST requests
        +
HTTP 401 responses
        +
Short time interval

Example Threshold

A possible initial hunting threshold is:

5 failed authentication attempts
from the same source
within a short time window

This is a detection starting point rather than a universal security threshold.

Lab Validation

Synthetic web access logs generated during the project contained five failed authentication attempts against:

/rest/user/login

The automation script successfully detected this pattern.

Analyst Questions

The analyst should determine:

Is the source a legitimate user?

Did successful authentication occur after the failures?

Were multiple accounts targeted?

Was the activity automated?

Did endpoint reconnaissance occur from the same source?



---

6. Hunting Hypothesis 3 — Repeated Server Errors

Hypothesis

A high concentration of HTTP 5xx responses may indicate application misuse, malformed requests, endpoint probing, or an application-side failure.

Suspicious Pattern

Same source
        +
Multiple unusual paths
        +
Repeated HTTP 5xx

Lab Observation

The Juice Shop application returned HTTP 500 responses for several unexpected /rest paths.

Example:

/rest/admin
/rest/this-route-does-not-exist

The responses exposed framework and internal application path information.

Hunting Value

Repeated server errors become more useful when correlated with:

Endpoint reconnaissance

Authentication failures

Suspicious User-Agent values

Unusual request methods

Invalid authentication tokens


A single 500 response is generally not enough to identify malicious behavior.


---

7. Hunting Hypothesis 4 — Invalid JWT Signature

Hypothesis

Repeated JWT validation failures may indicate malformed tokens, token tampering attempts, replay-related problems, or application/client issues.

Relevant Event

The lab application rejected an altered JWT with an invalid signature.

Observed behavior:

HTTP 401 Unauthorized

with an invalid signature error.

Hunting Pattern

Potentially suspicious activity:

Same source IP
        +
Repeated JWT validation failures
        +
Protected endpoint access

Analyst Questions

The analyst should determine:

1. Was the token generated by the application?


2. Was the token malformed?


3. Did the signature validation fail?


4. Did the same source make multiple attempts?


5. Was there successful authentication afterward?


6. Were other suspicious requests observed?



A single invalid JWT does not automatically establish malicious activity.


---

8. Correlation Hunt

Individual events may have legitimate explanations.

Correlation provides stronger context.

A potentially suspicious sequence is:

Endpoint reconnaissance
        ↓
Repeated 5xx responses
        ↓
Authentication failures
        ↓
JWT validation failures
        ↓
Successful authentication
        ↓
Access to sensitive functionality

The analyst should investigate whether these events originate from:

The same source IP

The same session

The same User-Agent

The same account

The same time period



---

9. Source IP Analysis

For each suspicious event, collect:

source_ip
timestamp
request_path
http_method
status_code
user_agent
username/account
authentication_result

Example investigation table:

Time	Source IP	Method	Path	Status	Interpretation

16:00:10	10.0.2.15	GET	/rest/admin	500	Suspicious endpoint
16:00:20	10.0.2.15	GET	/rest/unknown	500	Endpoint probing
16:01:00	10.0.2.15	POST	/rest/user/login	401	Authentication failure
16:01:10	10.0.2.15	POST	/rest/user/login	401	Authentication failure


The sample data is synthetic and exists only for detection testing.


---

10. User-Agent Analysis

User-Agent values can provide additional context.

Examples:

curl
python-requests
sqlmap
browser User-Agent
unknown/custom client

A command-line client does not automatically mean malicious activity.

The analyst should correlate User-Agent information with:

Request frequency

Endpoint selection

Authentication behavior

Source IP

Response codes



---

11. Endpoint Analysis

Classify endpoints into categories.

Normal

/rest/products
/rest/basket

Authentication

/rest/user/login
/rest/user/whoami
/rest/user/authentication-details/

Sensitive

/rest/user/change-password
/rest/user/reset-password

Suspicious or unexpected

/rest/admin
/rest/debug
/rest/internal
/rest/test

The classification depends on the application's legitimate architecture.


---

12. Timeline Construction

When investigating a suspicious source, construct a timeline.

Example:

16:00:00
GET /rest/products → 200

16:00:10
GET /rest/admin → 500

16:00:20
GET /rest/unknown → 500

16:00:30
GET /rest/test → 500

16:00:40
GET /rest/debug → 500

16:00:50
GET /rest/internal → 500

16:01:00
POST /rest/user/login → 401

16:01:10
POST /rest/user/login → 401

16:01:20
POST /rest/user/login → 401

The sequence provides more context than analyzing each event separately.


---

13. Threat Hunting With the Python Analyzer

The project contains:

scripts/web_log_analyzer.py

The analyzer processes simplified web access logs and identifies:

Repeated authentication failures

Endpoint reconnaissance

Repeated HTTP 5xx responses


Example:

python3 scripts/web_log_analyzer.py soc/logs/sample_web_access.log

Expected findings include:

[AUTHENTICATION_ABUSE]

[ENDPOINT_RECONNAISSANCE]

[REPEATED_SERVER_ERRORS]

The input file is synthetic laboratory data.

It is not production telemetry.


---

14. Detection vs Hunting

Detection

Detection asks:

> Did a predefined suspicious condition occur?



Example:

5 failed logins from one IP

Threat Hunting

Threat hunting asks:

> What suspicious behavior may exist even if no predefined alert fired?



Example:

A source gradually discovers unusual endpoints,
generates several server errors,
then begins authentication attempts.

Hunting therefore provides a broader investigative approach.


---

15. False Positive Considerations

Potential legitimate explanations include:

Developer testing

QA automation

Monitoring systems

Vulnerability scanners

API clients

Browser extensions

Misconfigured applications

Expired or malformed sessions


Therefore:

Suspicious pattern ≠ confirmed attack

Analysts should gather additional evidence before escalation.


---

16. Investigation Priorities

When several suspicious signals occur together, prioritize events based on:

1. Authentication abuse


2. Access to sensitive endpoints


3. Repeated token validation failures


4. Endpoint reconnaissance


5. Repeated server errors



These are investigation priorities for this lab and not universal severity rankings.


---

17. Recommended Investigation Data

A production implementation should retain sufficient telemetry to answer:

Who?
What?
When?
Where?
How?
What happened afterward?

Recommended fields:

timestamp
source_ip
destination
http_method
request_path
status_code
response_size
user_agent
session_id
account_id
authentication_result
jwt_validation_result
request_id

Sensitive credentials and tokens should not be stored unnecessarily.


---

18. Response Workflow

When suspicious activity is confirmed:

Detect
  ↓
Validate
  ↓
Scope
  ↓
Contain
  ↓
Eradicate
  ↓
Recover
  ↓
Lessons Learned

Potential containment actions include:

Blocking abusive sources

Temporarily disabling compromised accounts

Rotating compromised credentials

Revoking affected sessions

Increasing logging

Applying rate limits

Restricting sensitive endpoints


Actions should be based on confirmed evidence and organizational procedures.


---

19. Remediation Mapping

Threat hunting results should connect directly to remediation.

Hunting Observation	Defensive Improvement

Repeated login failures	Rate limiting and authentication monitoring
Endpoint reconnaissance	Endpoint monitoring and access controls
Repeated 5xx responses	Centralized error handling and logging
Invalid JWT signatures	Token validation monitoring
Sensitive endpoint probing	Authorization controls
Excessive application detail	Generic production error responses


Detailed remediation guidance is documented in:

remediation/web-application-remediation.md


---

20. Project Limitations

This threat hunting exercise has important limitations.

The environment is:

Local

Docker-based

Single application

Small-scale

Based partly on synthetic access logs

Not connected to a production SIEM

Not representative of real enterprise traffic volume


Therefore, the thresholds and observations should be treated as laboratory detection-engineering examples.


---

21. Future Improvements

Future versions could integrate:

Wazuh

Elastic Stack

Splunk

Microsoft Sentinel

Zeek

Suricata

Real application access logs

Windows authentication telemetry

Linux audit logs

Automated enrichment

MITRE ATT&CK mapping

Alert severity calculation

Threat intelligence enrichment



---

22. Conclusion

This threat hunting workflow demonstrates how web application telemetry can be investigated proactively.

The project combines:

Pentest
   +
Detection Engineering
   +
Threat Hunting
   +
Automation
   +
Remediation

The objective is not simply to identify vulnerabilities.

The objective is to understand how offensive activity can produce defensive telemetry and how that telemetry can be investigated by a SOC analyst.
