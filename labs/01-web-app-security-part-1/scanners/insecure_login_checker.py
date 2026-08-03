import requests
from bs4 import BeautifulSoup

# Configurable variables
LOGIN_URL = "http://localhost:5000/login"  # Change if needed


def check_http(url):
    if url.startswith("https://"):
        print("[✓] Secure protocol detected (HTTPS).")
    else:
        print("[!] Insecure login detected: Form is submitted over HTTP.")


def check_csrf_token(form_html):
    soup = BeautifulSoup(form_html, "html.parser")
    token = soup.find("input", {"name": "csrf_token"})
    if token:
        print("[✓] CSRF token detected.")
    else:
        print("[!] CSRF token not found in form fields.")


def check_rate_limiting(headers):
    rate_limit_headers = ["X-RateLimit-Limit", "Retry-After"]
    found = False
    for header in rate_limit_headers:
        if header in headers:
            found = True
            print(f"[✓] Rate limiting header detected: {header} = {headers[header]}")
    if not found:
        print("[!] No rate limiting headers detected.")


def main():
    try:
        print(f"\n[+] Connecting to {LOGIN_URL}...\n")
        response = requests.get(LOGIN_URL)

        if response.status_code != 200:
            print(f"[!] Failed to connect. Status Code: {response.status_code}")
            return

        check_http(LOGIN_URL)
        check_csrf_token(response.text)
        check_rate_limiting(response.headers)

    except requests.exceptions.RequestException as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()
