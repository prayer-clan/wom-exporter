import asyncio
import platform
import numpy as np
import groups
import players
import os

from wom import Client
from wom.enums import Skills

# windows users lol
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

WOM_CLAN_ID = 2215


async def main():
    client = Client()
    client.set_api_key(os.environ["WOM_API_KEY"])

    await client.start()
    group = await groups.get_group_details(client, WOM_CLAN_ID)
    player_details = []
    target = len(group.memberships)
    current = 0

    for m in group.memberships[0:target]:
        await asyncio.sleep(0.75)
        pd = await players.get_player_details(client, m.player.id)

        total_level = pd.latest_snapshot.data.skills[Skills.Overall].level
        combat_level = pd.combat_level
        player_build = pd.player.build.value
        role = m.membership.role.value

        if total_level < 1500 and combat_level < 110 and player_build == "main":
            player = []
            player.append(m.player.display_name)
            player.append(combat_level)
            player.append(total_level)
            player.append(player_build)
            player.append(role)

            player_details.append(player)

        current += 1
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Checking: {current}/{target}")

    await client.close()

    # Save the numpy array to a csv file
    np.savetxt("requirements_check.csv", player_details, delimiter=",", fmt="%s")


if __name__ == "__main__":
    asyncio.run(main())
