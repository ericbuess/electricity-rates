import os
import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj,sort_keys=True,indent=4)
    print(text)

os.chdir("/Users/ericbuess/Git/electricity-rates")
os.getcwd()
directory = os.fsencode(os.getcwd())

file_name = "choose-texas-power.json"

with open(file_name, 'r') as file:
    file_data = file.read()
    data = json.loads(file_data)['data']
    utilities = data['utilities']
    options = []

    for utility in utilities:
        plans = utility['plans']
        for plan in plans:
            name = plan['name']
            id = plan['id']
            rates = plan['rates']
            options.append({
                'plan': {
                    'name': name,
                    'id': id,
                    'rates': rates
                }
            })
    
    jprint(options)
    # for week in weeks:
    #         unit = week['unit']
    #         week_id = unit['id']
    #         week_ids.append(week_id)