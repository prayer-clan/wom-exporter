import requests
import json
import sys

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
limit = 50
offset = 0
increment_offset = 50
max_offset = (member_count - 2)  # starts at 0, -1 from end

# request clan member hiscore records from WOM
hiscores_json = []
while offset <= max_offset:
    params = {'offset': offset, 'limit': limit}
    hiscores_response = requests.get(url=f"https://api.wiseoldman.net/v2/groups/2215/hiscores?metric=overall", params=params)

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


"""Next Steps
    - I'm lazy and just put the JSON into a JSON to CSV converter
    -


"""
# then I'm lazy and just put the JSON into 