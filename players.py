from wom import Client, Player


async def getPlayers(players: list[str]) -> list[Player]:
    client = Client()
    await client.start()
    result = await client.players.search_players("P 2 G R", limit=1)
    # result = result.is_ok ? result.unwrap() : result.unwrap_err()
    if result.is_ok:
        result = result.unwrap()
    else:
        result = result.unwrap_err()
        raise ValueError(result)
    await client.close()
    return result
