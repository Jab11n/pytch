import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLLabel
import requests
import json
import os

logged_in = False
screens = ['login', 'home', 'user', 'project']
current_screen = screens[0]
me = ['username', 'displayname', 'userid']

# check if token is stored and valid
if os.path.exists("pytch-data.json"):
    with open("pytch-data.json", 'r') as file:
        data = json.load(file)
        if data["token"] != '':
            response = requests.get(
                'https://api.hatch.lol/auth/me',
                headers={
                    'token':data["token"]
                }
            )
            if response.status_code == 200:
                me = [data["username"], data["displayname"], data["userid"]]
                logged_in = True
                print('Logged in successfully! (stored credentials - pytch-data.json)')
                current_screen = screens[1]
            else:
                logged_in = False

def switch_screen(screen_name):
    global current_screen
    current_screen = screen_name
    update_screen()

#login function
def login():
    global me
    uname = uentry.get()
    passwd = pentry.get()
    loginrq = requests.post(
        url='https://api.hatch.lol/auth/login',
        json={
            'username':uname,
            'password':passwd
        }
    )
    if loginrq.status_code == 200:
        getme = requests.get(f"https://api.hatch.lol/users/{uname}")
        logindata = {
            "token": loginrq.json()["token"],
            "username": uname,
            "displayname": getme.json()["displayName"],
            "userid": getme.json()["id"]
        }
        with open('pytch-data.json', 'w') as json_file:
            json.dump(logindata, json_file, indent=4)
        me = [logindata["username"], logindata["displayname"], logindata["userid"]]
        label.config(text=f"Successfully logged in as {uname}!")
        print('Logged in successfully!')
        switch_screen('home')
    else:
        label.config(text=f"An error occurred ({loginrq.status_code})")

def get_project(project_id):
    response = requests.get(f"https://api.hatch.lol/projects/{project_id}")
    if response.status_code == 200:
        project_data = response.json()
        projecttitle.config(text=project_data["title"])
        projectdesc.config(text=project_data["description"])
    else:
        projecttitle.config(text="Failed to load project.")

def update_screen():
    global current_screen, screens, window, uentry, pentry, label, projecttitle, projectdesc, me
    for widget in window.winfo_children():
        widget.destroy()

    if current_screen == screens[0]: #login
        title_label = ttk.Label(window, text="Hatch Login", font=("Arial", 16))
        title_label.pack(pady=10)

        uname_label = ttk.Label(window, text="Username:")
        uname_label.pack()
        uentry = ttk.Entry(window, width=40)
        uentry.pack(pady=5)

        passwd_label = ttk.Label(window, text="Password:")
        passwd_label.pack()
        pentry = ttk.Entry(window, width=40, show="*")
        pentry.pack(pady=5)

        get_button = ttk.Button(window, text="Log In", command=login)
        get_button.pack(pady=20)

        label = ttk.Label(window, text="")
        label.pack(pady=10)

    elif current_screen == screens[1]: #home
        home_label = ttk.Label(window, text=f"Welcome back, {me[1]}", font=("Arial", 16))
        home_label.pack(pady=10)

        user_button = ttk.Button(window, text="User", command=lambda: switch_screen('user'))
        user_button.pack(pady=5)

        project_button = ttk.Button(window, text="Project", command=lambda: switch_screen('project'))
        project_button.pack(pady=5)

    elif current_screen == screens[2]: #user
        user_label = ttk.Label(window, text="User", font=("Arial", 16))
        user_label.pack(pady=10)

        home_button = ttk.Button(window, text="Home Screen", command=lambda: switch_screen('home'))
        home_button.pack(pady=5)

    elif current_screen == screens[3]: #project
        project_label = ttk.Label(window, text="Project", font=("Arial", 16))
        project_label.pack(pady=10)

        home_button = ttk.Button(window, text="Home", command=lambda: switch_screen('home'))
        home_button.pack(pady=5)

        projectid_label = ttk.Label(window, text="Project ID or URL:")
        projectid_label.pack()
        projectid = ttk.Entry(window, width=40)
        projectid.pack(pady=5)
        
        projectgobutton = ttk.Button(window, text="Load Project", command=lambda: get_project(projectid.get()))
        projectgobutton.pack(pady=5)

        projecttitle = ttk.Label(window, text="", font=("Arial", 16))
        projecttitle.pack(pady=10)
        projectdesc = ttk.Label(window, text="")
        projectdesc.pack(pady=5)

window = tk.Tk()
window.title("Hatch")
window.geometry(f'800x600+{int(window.winfo_screenwidth()/2 - 800 / 2)}+{int(window.winfo_screenheight()/2 - 600 / 2)}')
window.configure(bg="#f0f0f0")
window.resizable(False, False)
try:
    window.iconbitmap('./resources/hatch.ico')
except:
    print('Couldn\'t locate icon.')

style = ttk.Style()
#style.configure('TButton', font=('Arial', 12), background='#ffbd59', foreground='black')
#style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))

update_screen()
window.mainloop()