# remote_pdu
This project consists of tooling to implement remote controlled PDU for a kernel development lab using Smart Life power devices like smart plug points and smart power strips. Smart Life power devices can be set up and controlled using a mobile app. However, for automation purposes, we need a command line tool to control power of a PDU. For this purpose, I am using tinytuya cloud to access the Smart Life devices in my home kernel development lab and controlling them using the cloud credentials. For basics of this, see https://pypi.org/project/tinytuya/

First install tinytuya in your workstation :

# Install TinyTuya
python -m pip install tinytuya

To use this tool, use the following steps to set up a Tuya account [See TUYA Account section of https://pypi.org/project/tinytuya/] :
1. Create a Tuya account using these instructions - https://github.com/jasonacox/tinytuya/files/12836816/Tuya.IoT.API.Setup.v2.pdf
2. Create a Tuya Developer account on iot.tuya.com. When it asks for the "Account Type", select "Skip this step..."
3. Create a Tuya cloud project as described in the same section of the guide
4. Link your Smart Life devices using the Add App Account step. After this, you should be able to see all of your Smart devices under the "Devices" tab in the Tuya cloud project
5. Continue with the steps given in the guide to set up the Service API. IoT Core and Authorization must be added to make this work.
6. Invoke the tinytuya wizard to set up the list of devices that can be controlled from the tooling

   python -m tinytuya wizard   # use -nocolor for non-ANSI-color terminals

This will generate a json file devices.json with all the necessary information to control the smart devices using the tooling.

Use the powerctl.py program to control different devices in your devices.json file.

python powerctl.py [-h] -j JSON_FILE -d DEVICE_NAME -w SWITCH_NAME -c CDOWN_NAME [-t {on,off}] [-s]

The <device_name> is the name of the Smart Life device typically given while setting it up using the app. The <switch_name> is the name of a switch that need to be controlled or checked. The <cdown_name> is the countdown field corresponding to the switch to be controlled. -t <on/off> indicated powering on or powering off. If -s is specified, it prints the current status of the switch (On | Off).
