import tkinter as tk
from tkinter import ttk
import requests
import json

def login():
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
        label.config(text=f"Successfully logged in as {uname}!")
    else:
        label.config(text=f"An error occurred ({loginrq.status_code})")

window = tk.Tk()
window.title("Hatch")
window.geometry(f'400x300+{int(window.winfo_screenwidth()/2 - 400 / 2)}+{int(window.winfo_screenheight()/2 - 300 / 2)}')
window.configure(bg="#f0f0f0")
window.resizable(False, False)
try:
    window.iconbitmap('./resources/hatch.ico')
except:
    print('Couldn\'t locate icon.')

style = ttk.Style()
#style.configure('TButton', font=('Arial', 12), background='#ffbd59', foreground='black')
#style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))

title_label = ttk.Label(window, text="Hatch Login", font=("Arial", 16)).pack(pady=10)

uname_label = ttk.Label(window, text="Username:").pack()
uentry = ttk.Entry(window, width=40).pack(pady=5)

passwd_label = ttk.Label(window, text="Password:").pack()
pentry = ttk.Entry(window, width=40, show="*").pack(pady=5)

get_button = ttk.Button(window, text="Log In", command=login).pack(pady=20)

label = ttk.Label(window, text="").pack(pady=10)

window.mainloop()
