import asyncio
import platform

import groups
import players

# windows users lol
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

WOM_CLAN_ID = 2215


if __name__ == "__main__":
    # run the async methods synchronously
    sample = asyncio.run(players.getPlayers())
    print(sample)

    other = asyncio.run(groups.getClanMembers(2215))
    print(other)
