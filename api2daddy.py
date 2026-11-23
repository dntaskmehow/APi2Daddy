#!/usr/bin/env python3
# Secret Finder for Bug Bounty - finds API keys in JS
# pip install requests
import argparse, re, requests
from urllib.parse import urljoin

# Fire regex patterns - high signal, low false positive
PATTERNS = {
    "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
    "Google OAuth": r"ya29\.[0-9A-Za-z\-_]+",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret": r"[0-9a-zA-Z/+]{40}",
    "Stripe Key": r"(sk|pk)_(test|live)_[0-9a-zA-Z]{10,}",
    "Slack Token": r"xox[bprs]-[0-9a-zA-Z]{10,}",
    "GitHub Token": r"gh[pousr]_[A-Za-z0-9_]{36,}",
    "Generic API Key": r"(?i)(api_key|apikey|secret|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
    "Bearer Token": r"Bearer\s+[A-Za-z0-9\-_\.=]{20,}",
    "Firebase": r"firebase.*\.firebaseio\.com",
    "Private Key": r"-----BEGIN (?:RSA )?PRIVATE KEY-----",
}

def get_js_links(base_url):
    try:
        r = requests.get(base_url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        # find .js files
        js_urls = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', r.text)
        full = []
        for u in js_urls:
            full.append(urljoin(base_url, u))
        return list(set(full))
    except Exception as e:
        print(f"[!] Error getting page: {e}")
        return []

def scan_url(js_url):
    try:
        r = requests.get(js_url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        content = r.text
        found = []
        for name, pattern in PATTERNS.items():
            matches = re.findall(pattern, content)
            for m in matches:
                # clean generic matches
                if len(str(m)) > 400: continue
                found.append((name, str(m)[:200]))
        return found
    except:
        return []

def main():
    parser = argparse.ArgumentParser(description="Fire Secret Finder - JS API Key Hunter")
    parser.add_argument("-u", required=True, help="Target URL e.g. https://example.com")
    parser.add_argument("-o", help="Output file")
    args = parser.parse_args()

    print(f"[+] Scanning {args.u} for secrets...")
    js_files = get_js_links(args.u)
    print(f"[+] Found {len(js_files)} JS files")

    results = []
    for js in js_files:
        print(f"  [>] Checking {js}")
        secrets = scan_url(js)
        for name, secret in secrets:
            print(f"    \033[92m[!] {name}: {secret}\033[0m in {js}")
            results.append(f"{name} | {secret} | {js}")

    # Also scan the main page itself
    print(f"  [>] Checking main page {args.u}")
    for name, secret in scan_url(args.u):
        print(f"    \033[92m[!] {name}: {secret}\033[0m")
        results.append(f"{name} | {secret} | {args.u}")

    if args.o and results:
        open(args.o, "w").write("\n".join(results))
        print(f"\n[+] Saved {len(results)} findings to {args.o}")
    
    if not results:
        print("\n[-] No secrets found - try crawling more pages with gau or waybackurls and feed them in")

if __name__ == "__main__":
    main()
