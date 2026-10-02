import httpx
def geocode(location: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "format": "json",
        "limit": 1,
        "q": location
    }

    headers = {
        "User-Agent": "TripPlanner/1.0"
    }

    with httpx.Client() as client:
        response =  client.get(
            url,
            params=params,
            headers=headers
        )
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError(f'Could not find location: "{location}"')

    return [
        float(data[0]["lat"]),
        float(data[0]["lon"])
    ]

def get_route(current, pickup, dropoff):
    coords = ";".join([
        f"{current[1]},{current[0]}",
        f"{pickup[1]},{pickup[0]}",
        f"{dropoff[1]},{dropoff[0]}"
    ])

    url = (
        f"https://router.project-osrm.org/"
        f"route/v1/driving/{coords}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson"
    }

    with httpx.Client() as client:
        response =  client.get(
            url,
            params=params
        )

    response.raise_for_status()

    data = response.json()

    if data["code"] != "Ok":
        raise ValueError(f'Routing failed: {data["code"]}')

    route = data["routes"][0]

    MI = 1609.344

    legs = [
        {
            "name": "current → pickup",
            "miles": route["legs"][0]["distance"] / MI,
            "hours": route["legs"][0]["duration"] / 3600,
            "endsWith": "PICKUP"
        },
        {
            "name": "pickup → dropoff",
            "miles": route["legs"][1]["distance"] / MI,
            "hours": route["legs"][1]["duration"] / 3600,
            "endsWith": "DROPOFF"
        }
    ]

    return {
        "distanceMiles": route["distance"] / MI,
        "drivingHours": route["duration"] / 3600,
        "legs": legs,
        "start": current,
        "geometry": [
            [point[1], point[0]]
            for point in route["geometry"]["coordinates"]
        ]
    }