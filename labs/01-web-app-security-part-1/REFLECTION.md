# Task 5 — Analysis and Secure Coding Practices

## Finding → OWASP A07 → Fix

| Scanner Finding | OWASP A07 Concern | Secure Coding Fix |
|---|---|---|
| HTTP used for login | Insecure transmission | Use HTTPS and enforce with HSTS |
| No CSRF token | Susceptible to CSRF attacks | Hidden CSRF token + server-side validation |
| No rate-limiting headers | Brute-force attack possible | Backend rate-limiting + lockout logic |

## Why these issues matter
Each finding gives an attacker a different capability, and they compound.
HTTP exposes plaintext credentials to anyone on the network path — confirmed
directly in Task 4, where the submitted password was readable in DevTools
with no decryption needed. Missing CSRF protection lets a different site
submit requests as an authenticated user, no stolen credential required.
Missing rate-limiting removes the last safeguard if credentials leak from
anywhere else — a breached password dump, phishing, or this same HTTP
exposure. OWASP A07 explicitly covers credential stuffing, where compromised
credentials originate from an entirely unrelated breach.

## How they might be exploited in the wild
- **HTTP:** attacker on shared Wi-Fi or a compromised router sniffs traffic
  and reads the POST body directly.
- **No CSRF:** attacker hosts a page with an auto-submitting form targeting
  this endpoint; a logged-in victim unknowingly triggers an action on their
  behalf when they visit it.
- **No rate-limiting:** attacker scripts thousands of login attempts using
  a leaked password list against likely usernames — the automated version
  of the zero-friction repeated submission demonstrated by hand in Task 4.

## Tools to detect and fix this at scale
Per Qadir et al. (2025, PeerJ), DAST tools (OWASP ZAP included) detected
**zero** A07 vulnerabilities across 75 real-world applications; only the
SAST tool Yasca found any, in 16 apps. This scanner is DAST-style — useful
for spot-checking a known suspect endpoint, but not sufficient to catch A07
issues at scale across a whole codebase (e.g. hard-coded credentials,
missing HTTPS-only cookie flags, CSRF middleware present but not wired in).
At scale, the right setup combines both: SAST in CI on every commit to
catch source-level issues, DAST run periodically against the live app to
catch runtime/configuration gaps — matching this scanner's own limitation,
noted back in OBSERVATIONS.md, that a `[!]` means "not observed," not
"proven absent."

## Source
Qadir, S. et al. (2025). *Comparative evaluation of approaches & tools for
effective security testing of Web applications.* PeerJ Computer Science,
11:e2821. https://doi.org/10.7717/peerj-cs.2821
