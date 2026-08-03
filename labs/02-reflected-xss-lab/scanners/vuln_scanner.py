import requests

# This is your target — an intentionally insecure search page that
# echoes input.
BASE_URL = "http://localhost:5000/search?q="

# These payloads are commonly used to test for reflected XSS.
payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(2)>",
    "<svg/onload=alert(3)>"
]


def test_payload(payload):
    """Submit the payload and check if it is reflected in the response."""
    try:
        full_url = BASE_URL + payload
        response = requests.get(full_url, timeout=5)

        # Stop early if the server did not return a successful response.
        if response.status_code != 200:
            print(f"[!] Unexpected response status: {response.status_code} for payload: {payload}")
            return

        # Check if payload appears in the response body
        if payload in response.text:
            print(f"[!] Potential XSS vulnerability detected with payload: {payload}")
        else:
            print(f"[✓] No reflection found for payload: {payload}")

    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed for payload: {payload}")
        print(f"    Error: {e}")


def main():
    print("\n[+] Starting reflected XSS test...\n")

    for payload in payloads:
        test_payload(payload)


if __name__ == "__main__":
    main()
