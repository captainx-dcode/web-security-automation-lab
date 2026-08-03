# Lab 02 — Reflected XSS Scanner

## Finding → OWASP A03 → Fix

| Scanner Finding | OWASP A03 Concern | Secure Coding Fix |
|---|---|---|
| Payload reflected unescaped in response | Reflected Cross-Site Scripting (CWE-79) | Output-encode all user input before rendering into HTML (e.g. Flask's `escape()` / Jinja2 autoescaping) |

## Why it matters
The `/search` route concatenates the raw `q` parameter into an HTML
string with an f-string — no encoding, no sanitization. Per OWASP
A03:2021, this is the textbook injection pattern: untrusted data used
directly by an interpreter (here, the browser's HTML parser) without
context-aware escaping. A real attacker would craft a URL containing
a payload and send it to a victim; the victim's own browser executes
the attacker's script in the victim's authenticated session.

## Fix applied conceptually
Replacing:
    return f"<h1>Search Results for: {q}</h1>"
with:
    from markupsafe import escape
    return f"<h1>Search Results for: {escape(q)}</h1>"
would cause `<` and `>` to render as `&lt;` and `&gt;`, breaking the
script tag before the browser ever parses it as executable HTML.
