import requests

url = 'http://localhost:9999/chat/completions'  # Replace with your actual server URL
data = {'message': 'print hello world'}
response = requests.post(url, json=data)

if response.status_code == 200:
    print("Response from server:", response.json())
else:
    print("Error:", response.status_code)