# APi2Daddy

**APi2Daddy** is a Python command-line tool for authorized security reviews. It discovers JavaScript files on a target page and scans their source for recognizable credentials, API keys, tokens, and private-key markers.

> [!IMPORTANT]
> Only scan systems you own or have explicit permission to test. APi2Daddy does not verify whether a detected value is active or exploitable.

## Features

- Discovers `script src` JavaScript assets on a target page
- Scans both the main page and discovered JavaScript files
- Detects common key and token formats
- Supports text or JSON Lines output
- De-duplicates repeated findings
- Includes configurable HTTP timeouts and scan limits
- Uses clear, copy-friendly CLI output

## Requirements

- Python 3.9+
- `pip`
- Network access to the target

## Installation

```bash
git clone https://github.com/dntaskmehow/APi2Daddy.git
cd APi2Daddy
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install requests
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install requests
```

## Quick start

```bash
python3 api2daddy.py -u https://example.com
```

Save findings:

```bash
python3 api2daddy.py -u https://example.com -o findings.txt
```

Save machine-readable findings:

```bash
python3 api2daddy.py -u https://example.com -o findings.jsonl --json
```

Scan one JavaScript file directly:

```bash
python3 api2daddy.py -u https://example.com/app.js --js-only
```

## Command reference

```text
usage: api2daddy.py [-h] -u URL [-o OUTPUT] [--json] [--js-only]
                    [--timeout SECONDS] [--limit COUNT]

options:
  -u, --url             Target URL or JavaScript URL
  -o, --output          Save findings to a file
  --json                Write JSON Lines instead of pipe-separated text
  --js-only             Treat -u as a JavaScript URL and skip page discovery
  --timeout SECONDS     HTTP timeout for each request (default: 10)
  --limit COUNT         Maximum number of JavaScript files to scan (default: 50)
```

## Output

Text output:

```text
Google API Key | AIza... | https://example.com/app.js
```

JSON Lines output:

```json
{"type":"Google API Key","match":"AIza...","source":"https://example.com/app.js"}
```

Detected values are intentionally truncated in console and export output so credentials are not displayed in full.

## Detection coverage

| Detector | What it looks for |
|---|---|
| Google API Key | `AIza` followed by 35 key characters |
| Google OAuth | OAuth access-token prefix |
| AWS Access Key | `AKIA` followed by 16 uppercase characters/digits |
| Stripe Key | Test or live Stripe key prefix |
| Slack Token | Slack bot, user, config, or refresh token prefixes |
| GitHub Token | GitHub token prefixes and payload |
| Generic Credential | Named API-key, secret, or password assignments |
| Bearer Token | Authorization bearer values |
| Firebase URL | Firebase Realtime Database hostnames |
| Private Key | PEM private-key block headers |

## Security and false positives

This tool performs pattern matching only. It may report:

- Example or placeholder values
- Revoked or expired credentials
- Public publishable keys
- Build metadata or documentation
- Repeated strings with innocuous context

Rotate or revoke any real exposed credential through the issuing provider. Avoid publishing raw findings in tickets or public logs.

## Project files

```text
api2daddy.py  - scanner implementation
README.md     - project documentation
```

## License

No license has been added to this repository yet. All rights are reserved until a license is chosen.
