import json
import sys

import requests
from wom import Client, GroupDetail


async def get_group_details(client: Client, groupId: int) -> GroupDetail:
    result = await client.groups.get_details(groupId)

    if result.is_ok:
        result = result.unwrap()
    else:
        result = result.unwrap_err()
        raise ValueError(result)

    return result


def get_group_details_sync(groupId, metric):
    # request clan details from WOM
    groups_response = requests.get("https://api.wiseoldman.net/v2/groups?name=Prayer&limit=1")

    # get a reference of the JSON data from the response
    clan_data = groups_response.json()
    member_count = clan_data[0]['memberCount']

    # some notes on the below...
    """ limit: 
            amount of records that can be returned from API (max is 50)
        
        offset: 
            which records to return (e.g. offset 0 gives members 0-49, offset 50 gives, 50-99)
        
        increment_offset:
            the static amount we will increase offset by in each iteration

        max_offset:
            this value comes from the total number of clan member, querying past it would result in 0 records
    """
    groupId = 2215
    metric = 'overall'
    limit = 50
    offset = 0
    increment_offset = 50
    max_offset = (member_count - 2)  # starts at 0, -1 from end

    # request clan member hiscore records from WOM
    hiscores_json = []
    while offset <= max_offset:
        params = {'offset': offset, 'limit': limit}
        hiscores_response = requests.get(
            url=f"https://api.wiseoldman.net/v2/groups/{groupId}/hiscores?metric={metric}",
            params=params)

        # if not HTTP Status OK (200), exit quickly
        if hiscores_response.status_code != 200:
            print("Something went wrong, get fucked")
            sys.exit()

        # increase offset for next iteration of loop
        offset += increment_offset

        # get a reference to the JSON data from the response
        hiscores_data = hiscores_response.json()

        # add these to our hiscores_json
        hiscores_json.extend(hiscores_data)

    # save the JSON into a file
    with open('clan_members.json', 'w') as json_file:
        json_string = json.dumps(hiscores_json)
        json_file.write(json_string)

    """
    Next Steps
        - I'm lazy and just put the JSON into a JSON to CSV converter
        - https://www.convertcsv.com/json-to-csv.htm
        - Then import to Google Sheets, done!
    """
