# Task 3 — Scanner Output Observations

## Raw output

[+] Connecting to http://localhost:5000/login...

[!] Insecure login detected: Form is submitted over HTTP.
[!] CSRF token not found in form fields.
[!] No rate limiting headers detected.


## What each finding actually proves vs. what it merely suggests

| Finding | What it checks | Scope / limitation |
|---|---|---|
| HTTP detected | String prefix of `LOGIN_URL` | Confirms configuration, not a captured cleartext packet |
| No CSRF token | Presence of `<input name="csrf_token">` | Only detects this exact convention; other implementations would false-negative |
| No rate limiting | Presence of `X-RateLimit-Limit` / `Retry-After` headers on one request | Server-side lockout with no header would also show `[!]` — confirmed manually instead by repeated submission with zero friction |

## Takeaway
A `[!]` here means "expected safeguard not observed," not "vulnerability proven."
Automated scanning narrows where to look manually — it doesn't replace the manual check.
