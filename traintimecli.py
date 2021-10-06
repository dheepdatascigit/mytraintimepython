import requests
import json
import os

devid = os.environ.get("PTVAPI_DEVID")
signature = os.environ.get("PTVAPI_SIG")

def jsontofile(injson):
    """ write json output to file

    input: json
    output: traintime.json
    """

    with open('traintime.json', 'w') as outfile:
        json.dump(injson, outfile)


url = f'http://timetableapi.ptv.vic.gov.au/v3/departures/route_type/0/stop/1044/route/3?direction_id=1&max_results=3&include_cancelled=false&include_geopath=true&devid={devid}&signature={signature}'
response = requests.get(url)

out = response.json()
print(json.dumps(out, indent=2))

# write output json to local file
jsontofile(out)

#print(len(out["results"]))

# for i in out["results"][0]:
#     print(i, out["results"][0][i], '\n')

