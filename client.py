import socket
import json
import sys
import os

#python client.py IpAddr UserName
#python client.py 127.0.0.1 Mintybacon

def getExternalIP():  
    out = os.popen("curl ipecho.net/plain").read()
    return out
    
data = {}

#First Send a request to Connect Key = 'New Connection' Value = Username
data = {'New Connection':sys.argv[2]}


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], 13375))
#s.connect(('127.0.0.1', 13375))

s.send(json.dumps(data))

#recieve List of games Key = GameName Value = JSON of all game components
data = json.loads(s.recv(1024).strip())

print "Connected!"

print "--Game List--"
for key, value in data.iteritems():
    print key, value

#Logic for New Game vs Join Game   
var = raw_input("\n\nType Join followed by the name of the game you want to join\nOr type New to create a new game\n")

#Logic for New Game
if(var.lower().split(' ', 1)[0] == "new"):
    print "Creating a new game.."
    #Collect Name, Map, and custom map boolean for new game
    name = raw_input("\nName for your new game\n")
    map = raw_input("\nWhat Map do you want to play?\n")
    cus = raw_input("\nis this a custom map? True/False\n")
    out = {}
    #Send out in JSON using the Following Keys
    out['New Game'] = getExternalIP()
    out['New Name'] = name
    out['Map Name'] = map
    out['Custom Bool'] = cus
    s.send(json.dumps(out))
    #Loop for Duplication Errors
    while 1:
        #Recieve either a connection ping with Game data OR DuplicatName which prompts the client to choose a new name for the game
        acpt = json.loads(s.recv(1024).strip())
        print acpt
        if('DuplicateName' in acpt):
            nn = raw_input("\n\nThat Name is already taken! Choose a new Name:\n")
            s.send(json.dumps({'New Name':nn}))
        else:
            #Server sent back a message confirming the game has been made and we can continue
            break
    #Connection Loop
    print "Connected"
    while 1:
        try:
            #We recieve a JSON with all Game Data can do what ever with this
            ping = json.loads(s.recv(1024).strip())
            s.send(json.dumps({'ping':''}))
        
        except Exception, e:
            print "Exception while receiving message: ", e
            break
#Logic for Join Game    
if(var.lower().split(' ', 1)[0] == "join"):
    #Get the name of the game we want to join
    name = raw_input("\nName of the game you would like to join\n")
    out = {}
    out['Join Game'] = name
    s.send(json.dumps(out))
    #maybe do a connection check? maybe? if this connection fails I guess we want to start over anyways..
    print "Connected"
    while 1:
        try:
            ping = json.loads(s.recv(1024).strip())
            #ping contains the ip of the host for now {'Update':'127.0.0.1'}
            s.send(json.dumps({'ping':''}))
        
        except Exception, e:
            print "Exception while receiving message: ", e
            break


s.close()

