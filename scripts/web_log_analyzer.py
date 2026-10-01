#!/usr/bin/env python3

"""
Web Application Security Log Analyzer

Analyzes simplified web access logs and identifies
security-relevant patterns for SOC investigation.

This script is designed for the authorized cybersecurity lab.
It does not perform network scanning or exploitation.
"""

import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path


LOGIN_PATH = "/rest/user/login"

SUSPICIOUS_PATH_KEYWORDS = (
    "/admin",
    "/unknown",
    "/test",
    "/debug",
    "/internal",
)

TIME_WINDOW_MINUTES = 5
AUTH_FAILURE_THRESHOLD = 5
UNIQUE_PATH_THRESHOLD = 5


def parse_log_line(line):
    """
    Parse a simplified access-log format:

    timestamp source_ip method path status user_agent

    Example:
    2026-10-01T16:00:00 10.0.2.15 GET /rest/admin 500 curl/8.5.0
    """

    pattern = (
        r"^(?P<timestamp>\S+)\s+"
        r"(?P<source_ip>\S+)\s+"
        r"(?P<method>\S+)\s+"
        r"(?P<path>\S+)\s+"
        r"(?P<status>\d{3})\s+"
        r"(?P<user_agent>.+)$"
    )

    match = re.match(pattern, line.strip())

    if not match:
        return None

    event = match.groupdict()
    event["status"] = int(event["status"])

    return event


def analyze_events(events):
    """Analyze parsed web events and generate security findings."""

    findings = []

    auth_failures = defaultdict(list)
    paths_by_ip = defaultdict(set)
    server_errors = Counter()
    jwt_failures = Counter()

    for event in events:
        source_ip = event["source_ip"]
        path = event["path"]
        status = event["status"]

        paths_by_ip[source_ip].add(path)

        if path == LOGIN_PATH and status == 401:
            auth_failures[source_ip].append(
                datetime.fromisoformat(event["timestamp"])
            )

        if status >= 500:
            server_errors[source_ip] += 1

        if "invalid" in path.lower() and "signature" in path.lower():
            jwt_failures[source_ip] += 1

    for source_ip, timestamps in auth_failures.items():
        timestamps.sort()

        for index, start_time in enumerate(timestamps):
            window_end = start_time + timedelta(minutes=TIME_WINDOW_MINUTES)

            window_count = sum(
                1
                for timestamp in timestamps[index:]
                if timestamp <= window_end
            )

            if window_count >= AUTH_FAILURE_THRESHOLD:
                findings.append(
                    {
                        "type": "AUTHENTICATION_ABUSE",
                        "source_ip": source_ip,
                        "details": (
                            f"{window_count} failed authentication attempts "
                            f"against {LOGIN_PATH} within "
                            f"{TIME_WINDOW_MINUTES} minutes"
                        ),
                    }
                )
                break

    for source_ip, paths in paths_by_ip.items():
        suspicious_paths = [
            path
            for path in paths
            if any(keyword in path.lower()
                   for keyword in SUSPICIOUS_PATH_KEYWORDS)
        ]

        if len(paths) >= UNIQUE_PATH_THRESHOLD or suspicious_paths:
            findings.append(
                {
                    "type": "ENDPOINT_RECONNAISSANCE",
                    "source_ip": source_ip,
                    "details": (
                        f"{len(paths)} unique paths observed; "
                        f"suspicious paths: {len(suspicious_paths)}"
                    ),
                }
            )

    for source_ip, count in server_errors.items():
        if count >= 3:
            findings.append(
                {
                    "type": "REPEATED_SERVER_ERRORS",
                    "source_ip": source_ip,
                    "details": f"{count} HTTP 5xx responses observed",
                }
            )

    for source_ip, count in jwt_failures.items():
        if count > 0:
            findings.append(
                {
                    "type": "JWT_VALIDATION_FAILURE",
                    "source_ip": source_ip,
                    "details": f"{count} possible JWT validation failures",
                }
            )

    return findings


def main():
    if len(sys.argv) != 2:
        print(
            f"Usage: {Path(sys.argv[0]).name} <access_log_file>"
        )
        sys.exit(1)

    log_file = Path(sys.argv[1])

    if not log_file.exists():
        print(f"Error: file not found: {log_file}")
        sys.exit(1)

    events = []

    with log_file.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            event = parse_log_line(line)

            if event is None:
                print(
                    f"[WARN] Could not parse line {line_number}",
                    file=sys.stderr,
                )
                continue

            events.append(event)

    print(f"Parsed events: {len(events)}")
    print()

    findings = analyze_events(events)

    if not findings:
        print("No security-relevant patterns detected.")
        return

    print("Security findings:")
    print("=" * 60)

    for finding in findings:
        print(f"[{finding['type']}]")
        print(f"Source IP: {finding['source_ip']}")
        print(f"Details: {finding['details']}")
        print("-" * 60)


if __name__ == "__main__":
    main()
