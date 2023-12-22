from httpx import Client

with Client() as client:
    response = client.get(
        url="$endpoint_url", params={"lon": 13.438596, "lat": 52.519854}
    )

    data = response.json()

    # prints the name of the first result
    print(data["features"][0]["properties"]["name"])
