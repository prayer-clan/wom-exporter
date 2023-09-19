import asyncio
import platform

from wom import Client
from wom.enums import Skills

import groups
import players

# windows users lol
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

WOM_CLAN_ID = 2215


async def main():
    client = Client()
    await client.start()
  
    group = await groups.get_group_details(client, WOM_CLAN_ID)
    player_details = []
    for m in group.memberships[0:5]:
        pd = await players.get_player_details(client, m.player.id)
        print(
            f"""
            Name: {m.player.display_name}
            Combat Level: {pd.combat_level}
            Total Level: {pd.latest_snapshot.data.skills[Skills.Overall].level}
            """
        )
        player_details.append(pd)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
