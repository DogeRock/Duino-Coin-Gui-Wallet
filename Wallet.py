#!/usr/bin/python3

from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import socket, os, urllib.request

try: 
  import popup
except:
    f = open("popup.py", "a")
    f.write("""
#!/usr/bin/python3\n
\n
from tkinter import *\n
from tkinter import ttk\n
\n
def popupmsg(msg, title):\n
    popup = Tk()\n
    popup.wm_title(title)\n
    label = ttk.Label(popup, text=msg)\n
    label.pack(side="top", fill="x", pady=10)\n
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)\n
    B1.pack()\n
    popup.mainloop()\n
""")
    f.close()

import popup

top = Tk()

top.configure(background="#7d796e")
top.geometry("500x500")
top.title("DogeRock Duino-Coin Gui Wallet")

L1 = Label(top, text = "User Name")
L1.place(x = 1,y = 200)
L2 = Label(top, text = "Password")
L2.place(x = 1, y = 250)
E1 = Entry(top, bd = 5)
E1.place(x = 200,y = 200)
E2 = Entry(top, bd = 5)
E2.config(show="•");
E2.place(x = 200,y = 250)

def GetBalance():
  username = E1.get()
  password = E2.get()
  
  serverip = "https://raw.githubusercontent.com/revoxhere/duino-coin/gh-pages/serverip.txt" 
  with urllib.request.urlopen(serverip) as content:
       content = content.read().decode().splitlines() 
       pool_address = content[0] 
       pool_port = content[1] 

  soc = socket.socket()
  soc.connect((str(pool_address), int(pool_port)))
  soc.recv(3).decode()

  soc.send(bytes("LOGI," + username + "," + password, encoding="utf8"))
  response = soc.recv(2).decode()           
  if response != "OK":
    popup.popupmsg("Error loging in - check account credentials!", "Error")
    return
  else:
    soc.send(bytes("FROM,Multithreaded PC Miner,"+str(username), encoding="utf8")) 

  soc.send(bytes("BALA", encoding="utf8"))
  balance = soc.recv(1024).decode()
  soc.close()

  L3 = Label(top, text = "Duino balance:")
  L3.place(x = 200, y = 325)
  L4 = Label(top, text = balance)
  L4.place(x = 200, y = 350)

B = Button(top, text = "Check balance", command=GetBalance)
B.place(x = 200, y = 400)
