### Need to run client on windows machine not linu subsytem to work: ###

import requests
import json
import sys
from time import sleep


response = requests.get('http://localhost:5005/esbi/stg1/api_runner?plant_id=34044&server_name=ewis-solarjb&tag_name=PCS1_SAMSUNG_BAT2205_A2_DC_Current&timestamp=2019-03-1007:54:00')
print(response.text)
#response_str = json.dumps(response.text)
#print(response_str)
response_json = json.loads(response.text)
print(response_json)
print(type(response_json))
job_id = response_json["result"].get("job_id")
print("job id: " + str(type(job_id)))

wait_time = 60
while (wait_time > 0):
    check_job = requests.get('http://localhost:5005/esbi/stg1/job_status/'+str(job_id)).text

    if check_job == 'ERROR(202): No Job Result':
        print("Waiting for response to come back.. {} tries left..".format(wait_time))
        wait_time = wait_time - 1
        sleep(2)
    else:
        print("found response!")
        print(check_job)
        wait_time = 0
