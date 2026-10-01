# Web Application Security & SOC Lab Architecture
## 1. Architecture Overview

This project uses an isolated local laboratory to demonstrate a complete web application security lifecycle.

The environment combines:

- Web application penetration testing
- Application reconnaissance
- Endpoint enumeration
- Authentication testing
- JWT security analysis
- SOC detection engineering
- Security investigation
- Remediation
- Security validation
- Git-based evidence and documentation

The environment is designed for authorized security testing only.

---

## 2. High-Level Architecture

```text
                         Ubuntu 24.04 LTS
                    Security Testing Host
                              |
                              |
                       127.0.0.1:3000
                              |
                              v
                    +--------------------+
                    |   Docker Engine    |
                    +--------------------+
                              |
                              v
                    +--------------------+
                    |   OWASP Juice Shop |
                    |                    |
                    |   Node.js          |
                    |   Express          |
                    |   Web Application   |
                    +--------------------+
                              |
                 +------------+------------+
                 |                         |
                 v                         v
          Pentest Activities          SOC Activities
                 |                         |
        +--------+--------+       +-------+--------+
        |                 |       |                |
   Recon/Enum       Auth Testing Detection      Investigation
        |                 |       |                |
        +--------+--------+       +-------+--------+
                 |                         |
                 +------------+------------+
                              |
                              v
                       Remediation


---

3. Host Environment

Component	Configuration

Operating System	Ubuntu 24.04.4 LTS
Virtualization	Oracle VirtualBox
CPU	Intel Core i5-12450HX
VM Memory	Approximately 2.9 GiB
VM CPU	2 vCPU
Disk	40 GB
Network Interface	enp0s3
Host Address	10.0.2.15/24
Docker	Docker Engine
Git	Git
Python	Python 3
Nmap	Nmap 7.94SVN


The target application is intentionally bound to localhost.


---

4. Target Environment

The target application is:

OWASP Juice Shop

The application runs inside Docker.

Target URL:

http://127.0.0.1:3000

Docker port mapping:

127.0.0.1:3000
        |
        v
Container port 3000

The localhost binding reduces exposure of the deliberately vulnerable application to the surrounding network.


---

5. Container Architecture

The target is deployed using Docker.

Conceptually:

Ubuntu Host
     |
     v
Docker Engine
     |
     v
Juice Shop Container
     |
     +--> Node.js
     |
     +--> Express
     |
     +--> OWASP Juice Shop
     |
     +--> HTTP :3000

The container provides an isolated application environment for security testing.


---

6. Security Testing Flow

The penetration-testing workflow follows:

Reconnaissance
      |
      v
Service Identification
      |
      v
Web Enumeration
      |
      v
Endpoint Discovery
      |
      v
Vulnerability Assessment
      |
      v
Authentication Testing
      |
      v
Controlled Security Validation
      |
      v
Evidence Collection
      |
      v
Reporting

All activities are performed against the authorized local laboratory.


---

7. Reconnaissance Layer

The reconnaissance phase identifies the exposed application and supporting technologies.

Tools used include:

Nmap
WhatWeb
cURL
Browser

Collected information includes:

Open TCP port

HTTP service behavior

Application title

HTTP headers

Technology indicators

JavaScript resources

Client-side endpoint references


Evidence is stored under:

evidence/recon/


---

8. Web Enumeration Layer

The enumeration phase analyzes application behavior and client-side resources.

The JavaScript bundle was inspected to identify references to application endpoints.

Examples include:

/api/Products
/api/Users
/api/Feedbacks
/rest/user/login
/rest/user/whoami
/rest/products/search
/rest/user/authentication-details/

Endpoint discovery supports subsequent authorized testing.


---

9. Authentication Testing Layer

Authentication testing evaluates how protected functionality behaves under different authentication states.

The project tested:

Unauthenticated request
        |
        v
HTTP 401

Valid laboratory authentication:

Login
  |
  v
JWT issued
  |
  v
Protected endpoint
  |
  v
HTTP 200

Invalid JWT signature:

Modified/invalid token
        |
        v
JWT validation
        |
        v
HTTP 401

Real authentication tokens are excluded from public GitHub evidence.


---

10. SOC Architecture

The SOC side of the project focuses on transforming application events into security detections.

Conceptual flow:

Web Application
       |
       v
HTTP / Application Logs
       |
       v
Log Collection
       |
       v
Detection Rules
       |
       v
SOC Investigation
       |
       v
Evidence Correlation
       |
       v
Remediation

The project documents detection logic but does not claim that a production SIEM was deployed.


---

11. Detection Layer

Detection logic focuses on:

Authentication abuse
Invalid JWT signatures
Endpoint probing
Repeated server errors
Web reconnaissance

The detection rules are documented in:

soc/detection-rules/web-application-detections.md

The rules correlate multiple events rather than treating one HTTP status code as proof of malicious activity.


---

12. Investigation Layer

The SOC investigation process correlates:

Source IP
Timestamp
Request path
HTTP method
HTTP status
Authentication result
User-agent
User identity
Request frequency

Example:

Endpoint Probing
       |
       v
Repeated HTTP 500
       |
       v
Authentication Attempts
       |
       v
JWT Validation Failure
       |
       v
Investigation

The investigation methodology is documented in:

soc/investigation/web-application-investigation.md


---

13. Remediation Layer

Security findings are mapped to remediation recommendations.

Primary remediation areas include:

Error handling
Authentication monitoring
JWT security
Endpoint authorization
Rate limiting
Security headers
Logging
Detection engineering

The remediation documentation is stored in:

remediation/web-application-remediation.md


---

14. Evidence Architecture

Evidence is organized according to security-testing activities.

evidence/
├── authentication/
└── recon/

Examples include:

HTTP headers
WhatWeb output
Endpoint discovery
Authentication responses
Reconnaissance data

Sensitive authentication evidence is excluded from Git tracking.


---

15. Reporting Architecture

The assessment report is stored in:

reports/pentest-report.md

The report connects:

Technical Observation
        |
        v
Security Impact
        |
        v
Evidence
        |
        v
Recommendation

The report avoids exposing sensitive authentication material.


---

16. Git Security

The repository uses .gitignore to prevent sensitive or generated evidence from being committed.

Examples include:

evidence/authentication/authenticated.txt
evidence/recon/main.js

This is important because security-testing artifacts may contain:

Authentication tokens

Session data

Large generated files

Potentially sensitive application information


Repository hygiene is treated as part of the security assessment.


---

17. Project Lifecycle

The complete project lifecycle is:

Lab Setup
    |
    v
Reconnaissance
    |
    v
Enumeration
    |
    v
Vulnerability Assessment
    |
    v
Authentication Testing
    |
    v
Evidence Collection
    |
    v
SOC Detection Engineering
    |
    v
SOC Investigation
    |
    v
Remediation
    |
    v
Validation
    |
    v
Automation
    |
    v
Professional Reporting


---

18. Security Boundaries

The project intentionally separates:

Testing Environment

Ubuntu Host
    |
    +--> Docker
          |
          +--> OWASP Juice Shop

Public Repository

Only sanitized documentation and appropriate evidence should be committed.

Sensitive values must remain outside the public repository.


---

19. Threat-to-Detection Mapping

The project maps offensive observations to defensive monitoring.

Pentest Observation	SOC Detection

Endpoint enumeration	Unique endpoint frequency
Unexpected REST paths	Suspicious path detection
Repeated HTTP 500	Server-error correlation
Failed authentication	Repeated 401 detection
Invalid JWT signature	JWT validation detection
Reconnaissance	Multi-endpoint behavioral correlation
Verbose errors	Information-disclosure remediation


This mapping demonstrates how offensive security findings can directly improve defensive monitoring.


---

20. Project Security Model

The project follows a continuous security lifecycle:

ATTACK SIMULATION
       |
       v
OBSERVATION
       |
       v
DETECTION
       |
       v
INVESTIGATION
       |
       v
REMEDIATION
       |
       v
VALIDATION
       |
       +------------------+
                          |
                          v
                   IMPROVED SECURITY

The purpose is not simply to identify vulnerabilities, but to demonstrate how security teams can discover, detect, investigate, remediate, and validate application security issues.


---

21. Authorization Statement

All security testing documented in this project was performed against an intentionally vulnerable application deployed locally for authorized educational and portfolio purposes.

No unauthorized external systems were targeted.

The project should not be interpreted as authorization to test systems that the tester does not own or have explicit permission to assess.
