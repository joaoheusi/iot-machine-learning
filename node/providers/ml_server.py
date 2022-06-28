import httpx

url = "http://localhost:5000/predictions/predict"


async def post_data(data):
    try:
        response = await httpx.post(url, json=data)
        return response.json()
    except Exception as e:
        print(e)
        return None
