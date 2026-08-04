# Security Misconfigurations & Red Flags to Watch For

A practical checklist of common vulnerabilities, their telltale signs,
and how to detect them during manual or automated testing. Useful as
a quick reference during reconnaissance (Step 2) and interception
(Step 3) of the manual pentesting workflow.

| Vulnerability | What to Watch For | How to Detect It | Exploitation Impact |
|---|---|---|---|
| Unencrypted HTTP | Site uses `http://` instead of `https://` | Check URL bar; use Burp to see plaintext requests | Attacker can intercept credentials, session tokens, sensitive data in transit |
| No Rate Limiting | Rapidly sending requests causes no slowdown or blocking | Send 100+ requests in seconds to login, search, or API endpoint; no 429 errors | Brute force attacks on passwords, credential stuffing, API abuse, DoS |
| Weak/No CORS Headers | API responds to cross-origin requests from any domain | Set `Origin: http://attacker.com` in request; if server accepts it, CORS is misconfigured | Attackers steal data from other users' browsers via XSS |
| Predictable Session Tokens | Session IDs are sequential, short, or based on username | Decode tokens; check if incrementing them lets you access other accounts | Session hijacking, account takeover |
| Debug Mode Enabled | Detailed error messages, stack traces, file paths in responses | Trigger errors; look for verbose logging or `/debug`, `/admin` endpoints | Information disclosure; attackers learn app architecture and find vulnerabilities |
| Default Credentials | App uses factory-default usernames/passwords | Try admin/admin, admin/password, root/root on login & admin panels | Direct account takeover; full system compromise |
| No Input Validation | Forms accept any input (special characters, code, long strings) | Enter SQL syntax, HTML tags, scripts into input fields | SQL injection, XSS, command injection |
| Missing HTTPS on APIs | API endpoints return data over HTTP | Check Network tab in dev tools; test API endpoints directly | Man-in-the-middle attacks on sensitive API calls |
| Exposed API Keys/Secrets | Hardcoded keys in JavaScript, config files, or git history | Search page source for `api_key=`, `token=`, `secret=`; check GitHub for leaked creds | Direct API abuse, impersonation, unauthorized access |
| No Authentication on Endpoints | Sensitive endpoints accessible without login | Try accessing `/admin`, `/api/users`, `/dashboard` without auth | Unauthorized data access, privilege escalation |
| Improper Access Control (IDOR) | User can access other users' data by changing IDs in URL/API | Change URL from `/profile/123` to `/profile/124`; test `/api/orders/999` | View/modify other users' personal data, financial info, documents |
| No CSRF Tokens | Forms lack CSRF protection tokens | Inspect form HTML; try submitting from external site | Attackers force users to perform actions (change password, transfer money) |
| SQL Injection | User input directly concatenated into SQL queries | Enter `' OR '1'='1` or `'; DROP TABLE users; --` into login/search | Database theft, modification, deletion; authentication bypass |
| Reflected XSS | User input immediately displayed without sanitization | Enter `<script>alert(1)</script>` in search/comment; check if it executes | Steal session cookies, redirect users, deface page |
| Stored XSS | Malicious input stored in database and shown to all users | Enter payload in profile/comment; refresh page; check if it persists | Persistent attacks affecting all users who view that content |
| Weak Password Policy | App accepts short, simple, or reused passwords | Try passwords like 123, password, admin123 | Brute force attacks succeed quickly |
| No Encryption for Sensitive Data | PII stored plaintext in database or logs | Check database backups, log files; inspect what's stored in cookies | If database is breached, all sensitive data is immediately exposed |
| Outdated Dependencies | App uses old libraries with known CVEs | Check page source for version numbers; use `npm audit`, `composer audit` | Known exploits available; easy compromise |
| Server-Side Template Injection (SSTI) | User input reflected in template rendering | Try `{{7*7}}` or `${7*7}` in input fields; if it evaluates to 49, SSTI exists | Remote code execution on the server |
| Open Redirects | App redirects to user-supplied URLs without validation | Look for `redirect=`, `return=`, `url=` parameters; try `?redirect=http://attacker.com` | Phishing attacks; users trust the original domain but get redirected to attacker site |
| Missing Security Headers | No `X-Frame-Options`, `X-Content-Type-Options`, CSP headers | Use browser dev tools (Network tab) or curl to inspect response headers | Clickjacking, MIME-type sniffing, inline script injection |
| Path Traversal | App allows accessing files outside intended directory | Try `/../../../../../../etc/passwd` or `..\..\..\windows\win.ini` in file parameters | Read sensitive files (config, source code, system files) |
| Command Injection | App executes system commands with user input | Try `; ls` or `\| whoami` in input fields | Execute arbitrary system commands; full server compromise |
| Insecure Direct Object References (IDOR) | No verification user owns the resource they're accessing | Change user ID in URL `/user/123/documents` to `/user/456/documents` | Access other users' private documents, photos, data |
| No Logging/Monitoring | Attacks leave no trace in logs | Perform attacks; check if anything is logged; test for log manipulation | Attackers cover their tracks; breaches go undetected |

## How this maps to Part 2's five-step process

- **Step 2 (Reconnaissance):** most of the "What to Watch For" column —
  scanning pages for HTTP-only, missing security headers, exposed keys
  in page source, endpoints reachable without auth.
- **Step 3 (Intercept with Burp):** the CORS, session-token, and CSRF
  rows — these need a captured request to actually inspect.
- **Step 4 (Source code review):** debug mode, outdated dependencies,
  and the SSTI/SQLi/command-injection rows — confirming the *why*
  behind what Step 2/3 surfaced.

## Note on the Reflected/Stored XSS rows

These two rows are exactly what Part 2's Technical Lesson and lab test
directly against DVWA. Worth re-reading this checklist's two entries
side by side with `labs/03-web-app-security-part-2/` once that folder
exists, as a sanity check that the payload-and-confirm pattern matches.