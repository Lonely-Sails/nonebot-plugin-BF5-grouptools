from httpx import AsyncClient

client = AsyncClient()


async def request(url: str, params: dict, retry_count: int = 3):
    response = await client.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    if retry_count > 0:
        return await request(url, params, retry_count - 1)
    return None


async def request_player(name: str):
    response = await request('https://api.bfvrobot.net/api/v2/bfv/checkPlayer', {'name': name})
    if response:
        return response.get('data')
    return response


async def request_ban(persona_id: int):
    response = await request('https://api.bfvrobot.net/api/v2/bfv/getBannedLogsByPid', {'personaId': persona_id})
    return response.get('data')
