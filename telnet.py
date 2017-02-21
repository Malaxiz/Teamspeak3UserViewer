import getpass
import telnetlib
import time
import re
import sys

from ctypes import *                            # color stuff
STD_OUTPUT_HANDLE_ID = c_ulong(0xfffffff5)
windll.Kernel32.GetStdHandle.restype = c_ulong
std_output_hdl = windll.Kernel32.GetStdHandle(STD_OUTPUT_HANDLE_ID)

print "Malaxiz's teamspeak 3 query client viewer"
print "-----------"

serverip = raw_input("ServerIP: ")
username = raw_input("Name: ")
password = getpass.getpass("Password: ")

print ""
print "-----------"

tn = telnetlib.Telnet(serverip, "10011")

tn.read_until("")
tn.write("login " + username + " " + password + "\n")
tn.write("use port=9987\n")

old_users = []

def get_output():
    fullinfo = ""
    while True:
        info = tn.read_eager()
        if info == "":
            break
        fullinfo += info
    tn.read_until("")
    return fullinfo

def find_clients(data):
    if data == "":
        return ""
    pattern = re.compile(r'client_nickname=(.*?) ')
    clients = re.findall(pattern, data)
    return clients

def show_users():
    global old_users
    tn.write("clientlist\n")
    clients = list(set(find_clients(get_output())))
    if len(clients) != 0 and clients != old_users:
        new_users = list(set(clients) - set(old_users))
        disconnected_users = list(set(old_users) - set(clients))
        for client in clients:
            if client in new_users:
                windll.Kernel32.SetConsoleTextAttribute(std_output_hdl, 10) # green
            client = client.replace("\\s", " ")
            print client
            windll.Kernel32.SetConsoleTextAttribute(std_output_hdl, 15) # white
        for client in disconnected_users:
            windll.Kernel32.SetConsoleTextAttribute(std_output_hdl, 12) # red
            client = client.replace("\\s", " ")
            print client
            windll.Kernel32.SetConsoleTextAttribute(std_output_hdl, 15) # white
        print "-----------"
        old_users = clients

def main():
    while True:
        show_users()
        time.sleep(1)

main()
    
