from wom import Client, GroupMembership, PlayerDetail


async def get_player_details(client: Client, player_id: id) -> PlayerDetail:
    result = await client.players.get_details_by_id(player_id)
    if not result.is_ok:
        raise ValueError(result.unwrap_err())
    return result.unwrap()


async def get_players_details_from_group(memberships: list[GroupMembership]) -> list[PlayerDetail]:
    client = Client()
    await client.start()
    player_details = []
    for member in memberships:
        result = await client.players.get_details_by_id(member.player.id)
        if result.is_ok:
            player_details.append(result.unwrap())
        else:
            raise ValueError(result.unwrap_err())
 
    return player_details
