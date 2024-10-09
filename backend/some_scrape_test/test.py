import requests
url = 'https://ip.smartproxy.com/json'
username = 'sp0jca1g5w'
password = '2Q7lFY+1dqwbeg1vOl'
proxy = f"http://{username}:{password}@dc.smartproxy.com:10000"
result = requests.get(url, proxies = {
    'http': proxy,
    'https': proxy
})
print(result.text)