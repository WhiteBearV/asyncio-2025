import requests

response = requests.get("https://httpbin.org/delay/3")
print(response.status_code)