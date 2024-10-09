import requests

proxy = "http://213.204.18.38:50100"
proxies = {
    "http": proxy,
    "https": proxy,  # Using the same HTTP proxy for HTTPS
}

try:
    # Bypass SSL verification (for testing purposes only)
    response = requests.get("https://www.eurocali.it", proxies=proxies, timeout=10, verify=False)
    print(f"Status Code: {response.status_code}")
    print(response.text[:100])  # Print first 100 characters of the response

except requests.exceptions.ProxyError as e:
    print(f"Proxy error: {e}")
except requests.exceptions.SSLError as e:
    print(f"SSL error: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
except requests.exceptions.Timeout as e:
    print(f"Timeout error: {e}")
except requests.exceptions.RequestException as e:
    print(f"General error: {e}")
