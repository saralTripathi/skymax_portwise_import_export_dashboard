import requests
import urllib3

urllib3.disable_warnings()

url = "https://example.com"

response = requests.get(url, verify=False)

print("Status Code:", response.status_code)
print("Page Length:", len(response.text))