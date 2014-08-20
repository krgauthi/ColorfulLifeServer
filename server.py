import SocketServer
import json
import urllib2
import os
import sys
from threading import Lock
import Queue
from urllib2 import urlopen

#define
print_lock = Lock()
list_lock = Lock()

#Game list
gameList = {};

#TODO: Implement a Lock in the game for adding and removing players
#TODO: Add Map name String and Custom Map Bool
class Game():
    
    def __init__(self,gameName, ipAdd, hostName):
        self.name = gameName
        self.ip = ipAdd
        self.players = 1

    def isOpen(self):
        return self.players < 4
        
    def addPlayer(self):
        self.players += 1
        return
    
    def removePlayer(self):
        self.players -= 1
        return
    
    def getName(self):
        return self.name
        
    def getIP(self):
        return self.ip
        
    def getSize(self):
        return self.players
    

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:

            data = json.loads(self.request.recv(1024).strip())
            # process the data, i.e. print it:

            for key, value in data.iteritems():
                with print_lock:
                    print key, value

                if(key == 'New Connection'):
                    #From here we could Validate the user or IP possible Black list implementation
                    #Send back a JSON of Current Games
                    if(len(gameList) < 1):
                        self.request.sendall(json.dumps({'no':"games :("}))
                    else:
                        outgoingJson = {}
                        with list_lock:
                            for n,g in gameList.iteritems():
                                if g.isOpen():
                                    #TODO: Send back Game as a JSON with all game details
                                    outgoingJson[n] = g.getSize()
                        self.request.sendall(json.dumps(outgoingJson))
                        
                    #Connected now Join Game or Create Game    
                    action = json.loads(self.request.recv(1024).strip())
                    if('New Game' in action):
                        
                        with list_lock:
                            newName = {'New Name':action['New Name']}
                            if(gameList.has_key(action['New Name'])):
                                #Duplicate name 
                                while(gameList.has_key(newName['New Name'])):
                                    self.request.sendall(json.dumps({'DuplicateName':''}))
                                    newName = json.loads(self.request.recv(1024).strip())
                                action['New Name'] = newName['New Name']
                            
                            print "Creating new game: "+action['New Name']+" on IP: "+action['New Game']
                            g = Game(action['New Name'],action['New Game'],value)
                            gameList[g.getName()] = g
                        while 1:
                            try:
                                #should update with any thing you want i.e. game capacity
                                self.request.sendall(json.dumps({'Update':''}))
                                up = json.loads(self.request.recv(1024).strip())
                            except Exception, b:
                                    with print_lock:
                                        print "Lost connection to host ",action['New Game']
                                    break
                        with list_lock:
                            del gameList[g.getName()]
                        with print_lock:
                            print "Closed"
                    elif('Join Game' in action):
                        
                        g = 0
                        with list_lock:
                            if(action['Join Game'] in gameList):
                                g = gameList[action['Join Game']]
                        if(g != 0):
                            #TODO: Error with Locks here..
                            print "Joining game: "+action['Join Game']
                            
                            g.addPlayer()
                            while 1:
                                try:
                                    #should update with any thing you want
                                    #TODO: Send more than just IP
                                    self.request.sendall(json.dumps({'Update':g.getIP()}))
                                    up = json.loads(self.request.recv(1024).strip())
                                    
                                except Exception, b:
                                    with print_lock:
                                        print value,"Left the Game"
                                    break
                                           
                            g.removePlayer()
                            with print_lock:
                                print "Closed"

                
        except Exception, e:
            print "Exception while receiving message: ", e




#StartUp
try:
    g = Game("Minty's Game",'127.0.0.1',"Mintybacon")
    gameList[g.getName()] = g
    server = MyTCPServer(('0.0.0.0', 13375), MyTCPServerHandler)
    server.serve_forever()
    
    

except Exception, e:
    print "Exception while forking: ", e
