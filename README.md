# Web Application Security & SOC Lab

## Project Overview

End-to-end Web Application Security and SOC assessment of an intentionally vulnerable OWASP Juice Shop application running in an isolated local Docker lab.

### Security Activities

- Web reconnaissance
- Endpoint enumeration
- Vulnerability assessment
- Authentication testing
- JWT analysis
- Security evidence collection
- SOC investigation
- Detection engineering
- Remediation
- Security automation

> All testing was performed against a locally hosted OWASP Juice Shop instance for authorized security training.

## Lab Architecture

```text
Ubuntu 24.04 LTS
Security Testing Host
        |
        | 127.0.0.1:3000
        v
Docker Container
OWASP Juice Shop
Node.js / Express
## Environment

| Component | Details |
|---|---|
| Host | Ubuntu 24.04.4 LTS |
| Virtualization | VirtualBox |
| Target | OWASP Juice Shop |
| Deployment | Docker |
| Target Address | 127.0.0.1:3000 |
| Tools | Nmap, WhatWeb, cURL, Python |
| Version Control | Git |

## Methodology

```text
Reconnaissance
      ↓
Enumeration
      ↓
Vulnerability Assessment
      ↓
Authentication Testing
      ↓
Evidence Collection
      ↓
SOC Investigation
      ↓
Detection
      ↓
Remediation
      ↓
Automation
      ↓
Reporting
## Environment

| Component | Details |
|---|---|
| Host | Ubuntu 24.04.4 LTS |
| Virtualization | VirtualBox |
| Target | OWASP Juice Shop |
| Deployment | Docker |
| Target Address | 127.0.0.1:3000 |
| Tools | Nmap, WhatWeb, cURL, Python |
| Version Control | Git |

## Reconnaissance

Nmap, WhatWeb and cURL were used to identify the web application, HTTP behavior, headers and technology indicators.

Evidence is stored under:

`evidence/recon/`

## Endpoint Enumeration

Client-side JavaScript was analyzed to identify candidate API and REST endpoints.

Examples include:

`/api/Products`  
`/api/Users`  
`/api/Feedbacks`  
`/rest/user/login`  
`/rest/user/whoami`  
`/rest/products/search`

Client-side references were treated as candidates and validated against actual server behavior.

## Authentication Testing

Unauthenticated requests to protected endpoints returned:

`401 Unauthorized`

A valid lab account was then used to obtain a JWT.

The observed JWT algorithm was:

`RS256`

An authenticated request using:

A valid laboratory JWT was supplied for authenticated requests.

returned:

`200 OK`

An invalid JWT signature resulted in:

`401 Unauthorized`

Sensitive authentication tokens are excluded from the repository.

## Security Finding

### Verbose Error Messages / Information Disclosure

Unknown REST paths returned HTTP 500 responses containing internal application information.

Observed information included:

`OWASP Juice Shop (Express ^4.22.1)`

and internal application paths such as:

`/juice-shop/build/routes/angular.js`

`/juice-shop/build/routes/verify.js`

`/juice-shop/build/lib/insecurity.js`

### Impact

Verbose errors can disclose:

- Framework information
- Version information
- Internal filesystem paths
- Application architecture
- Request-processing details

### Recommendation

Production applications should:

- Return generic error messages
- Disable verbose stack traces
- Log detailed errors server-side
- Use centralized error handling
- Avoid exposing internal filesystem paths

## SOC Perspective

Potential monitoring scenarios include:

- Repeated authentication failures
- Invalid JWT signatures
- Requests to unusual endpoints
- Endpoint enumeration
- Repeated HTTP 4xx/5xx responses
- Suspicious administrative path probing

Useful log fields include:

- Timestamp
- Source IP
- HTTP Method
- Request Path
- HTTP Status
- User-Agent
- Authentication Result

## Remediation

Recommended controls include:

- Disable verbose production errors
- Implement centralized error handling
- Validate JWT signatures server-side
- Monitor authentication failures
- Monitor endpoint enumeration
- Centralize web application logging

## Skills Demonstrated

- Web Application Security
- Penetration Testing
- API Enumeration
- Authentication Testing
- JWT Security
- HTTP Analysis
- SOC Investigation
- Detection Engineering
- Security Automation
- Git/GitHub
- Technical Documentation

## Disclaimer

OWASP Juice Shop is an intentionally vulnerable application designed for security education.

All testing was performed against a locally hosted instance.

No unauthorized systems were targeted.
