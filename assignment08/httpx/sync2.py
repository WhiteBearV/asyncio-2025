import requests
import time

urls = ["https://httpbin.org/delay/2"] * 5

start = time.time()
for url in urls:
    response = requests.get(url)
    print(response.status_code)
print(f"Total time taken: {time.time() - start:.2f} seconds")