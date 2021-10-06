import requests

import json
import os
from datetime import datetime
from dateutil import tz


# get environment variables for PTV API
devid = os.environ.get("PTVAPI_DEVID")
signature = os.environ.get("PTVAPI_SIG")

# setup time zone to local => Melbourne
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Australia/Melbourne')

def jsontofile(injson):

    """ write json output to file
    input: json
    output: traintime.json
    """

    with open('traintime.json', 'w') as outfile:
        json.dump(injson, outfile)

def utctolocaltime(strtime, localzone='Australia/Melbourne'):
    """ covert input string time to local time
    eg. 
    - utctolocaltime('2021-10-06T17:33:00Z', localzone='Australia/Melbourne')
    - output: 2021-10-07 04:33:00+11:00
    """

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(localzone)

    outtime = datetime.strptime(strtime, '%Y-%m-%dT%H:%M:%SZ')
    outtime = outtime.replace(tzinfo=from_zone)
    outtime = outtime.astimezone(to_zone)
    #print(type(outtime))
    #return outtime.strftime("%c")
    return outtime

def showtraintimes(injson):
    """ show only train times in local time and departure platform
    """
    for i, ttid in enumerate(injson["departures"]):
        print(f"next train {i+1}:")
        print(f"platform_number: {ttid['platform_number']}")
        deptime = {ttid['scheduled_departure_utc']}
        #print(str(deptime))
        print(f"scheduled_departure_utc: {utctolocaltime(list(deptime)[0])}")
        

url = f'http://timetableapi.ptv.vic.gov.au/v3/departures/route_type/0/stop/1044/route/3?direction_id=1&max_results=3&include_cancelled=false&include_geopath=true&devid={devid}&signature={signature}'
response = requests.get(url)

out = response.json()
#print(json.dumps(out, indent=2))

# write output json to local file
jsontofile(out)
showtraintimes(out)
