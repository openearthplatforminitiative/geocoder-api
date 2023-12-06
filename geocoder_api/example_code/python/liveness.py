from httpx import Client

with Client() as client:
    response = client.get(url="$api_url$api_path")
    data = response.json()
