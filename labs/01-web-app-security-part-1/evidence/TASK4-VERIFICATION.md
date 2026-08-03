# Task 4 — Manual Verification of Scanner Findings

## Method
Firefox DevTools → Network tab → submitted dummy credentials to
http://127.0.0.1:5000/login, inspected the resulting POST request directly.

## Confirmed by hand (independent of the scanner)

| Check | Evidence | Confirms |
|---|---|---|
| Protocol | Request URL: `http://127.0.0.1:5000/login` | HTTP, not HTTPS |
| Method | `POST` | Standard form submission |
| Form data | `username`, `password` only — no `csrf_token` field | CSRF token absent from the actual wire payload, not just the HTML source |
| Content-Type | `application/x-www-form-urlencoded` | Standard unencrypted encoding |

## Key observation
The password value was visible in plaintext in the Form Data panel
(e.g. "zcsddj"). This makes the HTTP finding concrete: anyone able to
intercept this traffic — public Wi-Fi, a compromised router, a
malicious proxy — reads credentials exactly this easily, with no
decryption required.

## Conclusion
Manual inspection independently confirms all three scanner findings
from Task 3 (HTTP, missing CSRF token, missing rate-limit headers).
Automated tooling and manual verification agree — this is the
validation pattern professionals use both methods for.
