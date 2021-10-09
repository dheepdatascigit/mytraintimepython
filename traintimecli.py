import requests

import json
import os
from datetime import datetime
from dateutil import tz
from azure.storage.blob import BlobClient

# GET Enviroment variables - Configuration settings
## get environment variables for PTV API
devid = os.environ.get("PTVAPI_DEVID")
signature = os.environ.get("PTVAPI_SIG")

## get eviroment variables for storage connection
blobconnstr = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
### blbb settings
blob_container_name = "traintimecontainer"
blob_dstfile_name = "craigieburntraintime.json"


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

def writefile_to_azblob(dstfile="filename.json", conn_str="connection str", container_name="blob_container_name", blob_name="blob_dstfile_name", overwrite=False):
    
    """ write a file to Azure Blob
    """

    blob = BlobClient.from_connection_string(conn_str=conn_str, container_name=container_name, blob_name=blob_name)

    with open(dstfile, "rb") as data:
        outetag = blob.upload_blob(data, overwrite=overwrite)

    return outetag

def writestring_to_azblob(outstr, conn_str="connection str", container_name="blob_container_name", blob_name="blob_dstfile_name", overwrite=False):
    
    """ write a file to Azure Blob
    """

    blob = BlobClient.from_connection_string(conn_str=conn_str, container_name=container_name, blob_name=blob_name)
    outetag = blob.upload_blob(outstr, overwrite=overwrite)

    return outetag


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

# blob connection
## write json file to azure blob
ed = writefile_to_azblob(dstfile="traintime.json", conn_str=blobconnstr, container_name=blob_container_name, blob_name=blob_dstfile_name, overwrite=True)
print(ed)



with open('jsontest.json') as jfp:
    testjson = json.load(jfp)

print(json.dumps(testjson, indent=2))

## write string to azure blob 
ed = writestring_to_azblob(json.dumps(testjson), conn_str=blobconnstr, container_name=blob_container_name, blob_name="test3.json", overwrite=True)
print(ed)

