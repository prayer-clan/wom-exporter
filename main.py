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

    for m in group.memberships:
        await asyncio.sleep(0.75)
        pd = await players.get_player_details(client, m.player.id)

        if pd.latest_snapshot.data.skills[Skills.Overall].level >= 1500:
            continue
        if pd.combat_level >=110:
            continue
        if pd.player.build.value != "main":
            continue

        player = [
            m.player.display_name,
            pd.combat_level,
            pd.latest_snapshot.data.skills[Skills.Overall].level,
            pd.player.build.value,
            m.membership.role.value,
        ]

        player_details.append(player)

        current += 1
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Checking: {current}/{target}")

    await client.close()

    # Save the numpy array to a csv file
    np.savetxt("requirements_check.csv", player_details, delimiter=",", fmt="%s")


if __name__ == "__main__":
    asyncio.run(main())