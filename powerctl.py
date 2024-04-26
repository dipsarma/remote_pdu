#!/usr/bin/python

# Licence : GNU Public Licence v2
# Copyright (c) Dipankar Sarma

import argparse
import sys
import json
import tinytuya

def get_device_id(json_file, device_name):
    with open(json_file, 'r') as f:
        data = json.load(f)
        for device in data:
            if device['name'] == device_name:
                return device['id']
    return None

def switch_lookup(json_data, switch_code):
    records = json_data.get("result", [])
    for record in records:
        if record['code'] == switch_code:
            return record['value']
    print(f"No record found with code '{switch_code}'")

def get_credentials(device_id, json_file='cred.json'):
    with open(json_file, 'r') as f:
        data = json.load(f)
        return data

def control_switch(device_id, switch_name, cdown_name, action):
    credentials = get_credentials(device_id)
    if credentials:
        c = tinytuya.Cloud(
            apiRegion=credentials['apiRegion'],
            apiKey=credentials['apiKey'],
            apiSecret=credentials['apiSecret'],
            apiDeviceID=device_id
        )
        if action == 'status':
            # Display Properties of Device
            result = c.getstatus(device_id)
            status = switch_lookup(result, switch_name)
            if status == True:
                print("On")
            else:
                print("Off")
        else:
            if (action == 'on'):
                val = True
            else:
                val = False
            commands = {
                "commands": [
                    {"code": switch_name, "value": val},
                    {"code": cdown_name, "value": 0},
                ]
            }

            print("Sending command...")
            result = c.sendcommand(device_id,commands)
            print("Results\n:", result)
            print(f'Switch {switch_name} turned {action} successfully.')
    else:
        print(f'Credentials not found for device ID: {device_id}')

def main():
    parser = argparse.ArgumentParser(description='Control smart life devices')
    parser.add_argument('-j', '--json', dest='json_file', required=True, help='Path to the JSON file')
    parser.add_argument('-d', '--device', dest='device_name', required=True, help='Name of the device')
    parser.add_argument('-w', '--switch', dest='switch_name', required=True, help='Name of the switch')
    parser.add_argument('-c', '--countdown', dest='cdown_name', required=True, help='Name of the countdown')
    parser.add_argument('-t', '--toggle', dest='toggle', choices=['on', 'off'], help='Toggle the switch on or off')
    parser.add_argument('-s', '--status', action='store_true', help='Get the status of the switch')

    args = parser.parse_args()

    device_id = get_device_id(args.json_file, args.device_name)

    if device_id:
        if args.status:
            action = 'status'
        elif args.toggle:
            action = args.toggle
            if action not in ['on', 'off']:
                print('Action must be "on" or "off"')
                sys.exit(1)
        else:
            print('Please specify either -t or -s option')
    else:
        print(f'Device "{args.device_name}" not found in the JSON file')

    control_switch(device_id, args.switch_name, args.cdown_name, action)

if __name__ == "__main__":
    main()

