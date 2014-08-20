import socket
import json
import sys
import os

def getExternalIP():  
    #out = os.system("curl ipecho.net/plain")
    out = os.popen("curl ipecho.net/plain").read()
    return out
    
data = {}


data = {'New Connection':sys.argv[2]}


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], 13375))
#s.connect(('127.0.0.1', 13375))

s.send(json.dumps(data))

data = json.loads(s.recv(1024).strip())

print "Connected!"

print "--Game List--"
for key, value in data.iteritems():
    print key, value

    
var = raw_input("\n\nType Join followed by the name of the game you want to join\nOr type New to create a new game\n")

if(var.lower().split(' ', 1)[0] == "new"):
    print "Creating a new game.."
    name = raw_input("\nName for your new game\n")
    map = raw_input("\nWhat Map do you want to play?\n")
    cus = raw_input("\nis this a custom map? True/False\n")
    out = {}
    out['New Game'] = getExternalIP()
    out['New Name'] = name
    out['Map Name'] = map
    out['Custom Bool'] = cus
    s.send(json.dumps(out))
    
    while 1:
        acpt = json.loads(s.recv(1024).strip())
        print acpt
        if('DuplicateName' in acpt):
            nn = raw_input("\n\nThat Name is already taken! Choose a new Name:\n")
            s.send(json.dumps({'New Name':nn}))
        else:
            break
    
    print "Connected"
    while 1:
        try:
            ping = json.loads(s.recv(1024).strip())
            s.send(json.dumps({'ping':''}))
        
        except Exception, e:
            print "Exception while receiving message: ", e
            break
    
if(var.lower().split(' ', 1)[0] == "join"):
    name = raw_input("\nName of the game you would like to join\n")
    out = {}
    out['Join Game'] = name
    s.send(json.dumps(out))
    
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

