import requests
import json
import csv
import urllib3
import getpass
import time
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##User input varaibles###################################################
username = input("What is your username?") 
passwrd = getpass.getpass() 
auth = username,passwrd
upass_message = " Please check connectivity to director and  username/password and try again."

director_ip = input("What is the primary Director IP or Hostname?")
csv_batch_file = input("What is the full name of the .csv Batch File?")
oss_pack_version = input("What is the OSS pack version(YYYYMMDD)?")

##Set the standard API request headers###################################

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


##URL Variables###########################################################
https = "https://"
appliance_detail_url = ':9182/vnms/appliance/appliance?offset=0&limit=2000'
oss_pack_url = ':9182/vnms/osspack/device/install-osspack'
deep = '?deep=true'
fw_slash =':9182/'


##Appliance check variables################################################
reach_status = "UNREACHABLE"
sync_status = "IN_SYNC"
in_progress = 'IN_PROGRESS'
completed = 'COMPLETED'

##Set time def for print outputs###########################################
def local_time():
    seconds = time.time()
    local_time = time.ctime(seconds)
    return local_time

##Output file name variables###############################################
output_log = csv_batch_file + "_OSS_version_" + oss_pack_version + ".log"
output_csv = csv_batch_file + "_OSS_version_" + oss_pack_version + ".csv"


##Batch file conversion from csv to json#################################
jsonFile = csv_batch_file + ".json"
csv_data = {}

with open(csv_batch_file, encoding="utf-8") as csvFile:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
        key = rows["hostname"]
        csv_data[key] = rows

with open(jsonFile, "w", encoding="utf-8") as jsonFile:
    jsonFile.write(json.dumps(csv_data))
    jsonFile.close


##Load json variables from converted json batch file#################################
with open(csv_batch_file + ".json", "r") as json_batch_file:
    variables = json.load(json_batch_file)
    json_batch_file.close()



#Definitions##############################################################

#Appliance data definitions###
def appliance_detail_response ():
    appliance_detail_response = requests.get((https + director_ip + appliance_detail_url), headers=headers, verify=False, auth=auth)
    appliance_detail_response.close()
    return appliance_detail_response

def appliance_list():
    appliance_detail_json = appliance_detail_response().json()
    appliance_list = appliance_detail_json["versanms.ApplianceStatusResult"]["appliances"]
    return appliance_list

def appliance_name():
    appliance_name = appliance["name"]
    return appliance_name

def appliance_ping():
    appliance_ping = appliance["ping-status"]
    return appliance_ping

def appliance_sync():
    appliance_sync = appliance["sync-status"]
    return appliance_sync

#Update data definition###
def data():
    update_type = '{"update-type":"full","devices":'
    pre_device = '["'
    post_device = '"],'
    pre_version = '"version":"'
    post_version = '"}'
    data = update_type + pre_device + item + post_device + pre_version + oss_pack_version + post_version
    return data

def response_id():
    oss_pack_post_json = oss_pack_post.json()
    response_id = oss_pack_post_json["TaskResponse"]["link"]["href"]
    return response_id

def oss_pack_check_status():
    oss_pack_check_json = oss_pack_check.json()
    oss_pack_check_status = oss_pack_check_json["versa-tasks.task"]["versa-tasks.task-status"]
    return oss_pack_check_status

#Output log and file definitions###
def output_log_create():
    with open(output_log, "w") as output_log_file:
        output_log_file.write("###" + csv_batch_file + "_OSS_version_" + oss_pack_version + "###\n")
        output_log_file.close

def init_log_data():
    init_log_data = local_time() + " " + appliance_name() + " OSS pack upgrade initiated########\n"
    return init_log_data

def issue_log_data():
    issue_log_data = local_time() + " " + appliance_name() + " encountered issues upgrading OSS pack.\n"
    return issue_log_data

def reach_log_data():
    reach_log_data = local_time() + " " + appliance_name() + " is either unreachable or out of sync with Director\n"
    return reach_log_data

def prog_log_data():
    prog_log_data = local_time() + " " + appliance_name() + " OSS pack upgrade " + oss_pack_check_status() + " " + response_id() + "\n"
    return prog_log_data

def output_csv_create():
    with open(output_csv, "w") as output_csv_file:
        output_csv_file.write("hostname;reachability;director_sync;update_status;oss_version\n")
        output_csv_file.close

def issue_csv_data():
    issue_csv_data = appliance_name() + ";" + appliance_ping() + ";" + appliance_sync() + ";issue upgrading OSS;issue upgrading OSS;\n"
    return issue_csv_data

def reach_csv_data():
    reach_csv_data = appliance_name() + ";" + appliance_ping() + ";" + appliance_sync() + ";unreachable or out of sync;unreachable or out of sync;\n"
    return reach_csv_data

def prog_csv_data():
    prog_csv_data = appliance_name() + ";" + appliance_ping() + ";" + appliance_sync() + ";" + oss_pack_check_status() + ";" + oss_pack_version + "\n"
    return prog_csv_data

#cleanup unecessary post script files###
def file_cleanup():
    os.remove( csv_batch_file  + ".json")

#Upgrade OSS pack on all devices and check for status######################
print('##### GET all device status and upgrade#####')
if appliance_detail_response().status_code == 200:
    output_log_create()
    output_csv_create()
    with open(output_log, "a+") as output_log_file, open(output_csv, "a+") as output_csv_file:
        for appliance in appliance_list():
            for item in variables:
                if item in appliance_name():
                    if reach_status not in appliance_ping() and sync_status in appliance_sync():
                        oss_pack_post = requests.post((https + director_ip + oss_pack_url), headers=headers, data = data(), verify=False, auth=auth)
                        oss_pack_post.close
                        response_id()
                        if oss_pack_post.status_code == 201:
                            oss_pack_check = requests.get((https + director_ip + fw_slash + response_id()), headers=headers, verify=False, auth=auth)
                            oss_pack_check.close
                            print(init_log_data())
                            output_log_file.write(init_log_data())
                            for oss in oss_pack_check:
                                if oss_pack_check.status_code == 200 and oss_pack_check_status() == in_progress:
                                    print(prog_log_data())
                                    output_log_file.write(prog_log_data())
                                    oss_pack_check = requests.get((https + director_ip + fw_slash + response_id()), headers=headers, verify=False, auth=auth)
                                    oss_pack_check.close
                                    if oss_pack_check.status_code == 200 and oss_pack_check_status() == completed:
                                        print(prog_log_data())
                                        output_log_file.write(prog_log_data())
                                        output_csv_file.write(prog_csv_data())
                        else:
                            print(init_log_data())
                            output_log_file.write(init_log_data())
                            print(issue_log_data())
                            output_log_file.write(issue_log_data())
                            output_csv_file.write(issue_csv_data())
                    else:
                        print(init_log_data)
                        output_log_file.write(init_log_data())
                        print(reach_log_data()) 
                        output_log_file.write(reach_log_data())
                        output_csv_file.write(reach_csv_data())
else:
    print(upass_message)

file_cleanup()
