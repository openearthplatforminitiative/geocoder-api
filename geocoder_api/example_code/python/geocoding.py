from httpx import Client

with Client() as client:
    response = client.get(
        url="$endpoint_url",
        params={"q": "Berlin"},
    )

    data = response.json()

    # prints the coordinates of the first result
    print(data["features"][0]["geometry"]["coordinates"])
