print("Welcome to Pytch: a Python-based command line interface for Hatch.")

import requests
import time

running = True
token = None

APIurl = 'https://api.hatch.lol/'

def handleCommand(command):
    commands = ['help', 'login', 'logout', 'user', 'exit']
    global token
    global running
    if command not in commands:
        return ["Command not found."]
    elif command == commands[0]:
        return ["Available commands: " + commands]
    elif command == commands[1]:
        result = login()
        global token
        if token is not None:
            return [result + " " + token]
        else:
            return [result]
    elif command == commands[2]:
        logout()
        return ["OK"]
    elif command == commands[3]:
        success, result = getUserInfo()
        if success:
            return [
                "ID: " + str(result.get('id')),
                "Name: " + result.get('name'),
                "Display Name: " + result.get('displayName'),
                "Country: " + result.get('country'),
                "Bio: " + result.get('bio').replace('\n', '    '),
                "Followers: " + str(result.get('followerCount')) + ", Following: " + str(result.get('followingCount')),
                "Project Count: " + str(result.get('projectCount')),
                "Hatch Team? true" if result.get('hatchTeam') else "Hatch Team? false" 
            ]
        else:
            return [result]
    elif command == commands[4]:
        token = None
        running = False
        return ['Goodbye.']
    else:
        return ['...']

def login():
    loginEndpoint = 'https://api.hatch.lol/auth/login'
    username = input("Username: ")
    password = input("Password: ")
    login = requests.post(
        loginEndpoint,
        json={
            "username": username,
            "password": password
        }
    )
    if login.status_code == 200:
        global token
        token = login.json()["token"]
        return "Successfully logged in as " + username
    elif login.status_code == 401:
        return "Incorrect username or password."
    else:
        return f"Authentication failed ({login.status_code})"
    
def logout():
    global token
    token = None

def getUserInfo():
    userEndpoint = 'https://api.hatch.lol/users/'
    username = input("Username: ")
    user = requests.get(userEndpoint + username)
    if user.status_code == 200:
        data = user.json()
        return True, data
    else:
        return False, f"Command failed ({user.status_code})"

initialStart = time.time()
initialResponse = requests.get(APIurl)
initialEnd = time.time()
initialLatency = (initialEnd - initialStart) * 1000

if initialResponse.status_code == 200:
    print(f"The Hatch API is up. Latency: {initialLatency:.2f} ms")
    print("To get started, type 'help'.")
else:
    print(f"The Hatch API is currently unreachable. ({initialResponse.status_code}) Please try again later.")
    running = False
    input("Press any key to exit. ")

while running:
    command = input(">>> ")
    commandResult = handleCommand(command=command)
    for i in range(len(commandResult)):
        print(commandResult[i])