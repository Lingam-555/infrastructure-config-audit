# Infrastructure Configuration Audit Tool

## Author

Infrastructure automation learning project.

## Overview

The Infrastructure Configuration Audit Tool compares server configurations against a defined baseline and detects configuration drift.

It identifies missing configurations, mismatched values, and unexpected extra configurations for each server.

## Features

- Compares server configurations against a defined baseline
- Detects missing configuration settings
- Detects mismatched configuration values
- Detects unexpected extra configurations
- Identifies compliant and non-compliant servers
- Generates a configuration audit summary
- Logs non-compliant configuration findings
- Handles invalid or malformed configuration data

## Project Structure

- `server_audit.py` - Main audit script
- `baseline.json` - Expected configuration baseline
- `servers.json` - Actual server configurations
- `.gitignore` - Excludes generated files such as logs

## How It Works

1. Loads the baseline configuration.
2. Loads server configuration data.
3. Compares each server against the baseline.
4. Detects missing, mismatched, and extra configuration values.
5. Marks servers as compliant or non-compliant.
6. Prints an audit summary and logs non-compliant findings.

## Technologies Used

- Python
- JSON
- Python logging
- Git

## How to Run

```bash
python3 server_audit.py

## Sample Output

```text
==== SERVER CONFIGURATION AUDIT ====

Server: web-01
Status: COMPLIANT

Server: db-01
Status: NON-COMPLIANT
MISMATCH: ssh_port expected=22 actual=2222

==== AUDIT SUMMARY ====
Total Servers: 2
Compliant: 1
Non-Compliant: 1
