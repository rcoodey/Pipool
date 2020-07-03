import os
import configparser 
import time
import socket
import requests
import threading
import logging
import socketserver
from http.server import BaseHTTPRequestHandler

from PipoolConnectionMessage import ConnectionMessage
from PipoolChallengeMessage import ChallengeMessage
from PipoolLoginMessage import LoginMessage
from PipoolPoolStatusMessage import PoolStatusMessage
from PipoolControllerConfigMessage import ControllerConfigMessage
from PipoolSetCircuitStateMessage import SetCircuitStateMessage

#Open configuration file
config = configparser.ConfigParser()
script_dir = os.path.dirname(__file__) 
config.read(os.path.join(script_dir, 'PipoolServer.conf'))

smartthings_application_id = config.get('SmartThings', 'application_id') 
smartthings_access_token = config.get('SmartThings', 'access_token') 
smartthings_event_url = "https://graph.api.smartthings.com/api/smartapps/installations/" + smartthings_application_id + "/{0}/{1}?access_token=" + smartthings_access_token 
smartthings_pool_status_event_url = smartthings_event_url.format("pipool", "poolStatusEvent")
smartthings_update_frequency = int(config.get('SmartThings', 'update_frequency'))

http_port = int(config.get('Pipool', 'http_port'))
screenlogic_ip = config.get('Pipool', 'screenlogic_ip')
screenlogic_port = int(config.get('Pipool', 'screenlogic_port'))
 
#Define circuit ids (can use ControllerConfigMessage to look up by name)
SpaCircuitId = 500
WaterfallCircuitId = 501
PoolLightCircuitId = 502
SpaLightCircuitId = 503
PoolCircuitId = 505

#Define additional ids for SmartThings
AirTempId = 1
PoolTempId = 2
SpaTempId = 3

connection = None

def ListCircuits():
  #Send, receive and process controller config message
  print("Retrieving Controller Config")
  ControllerConfigMessage.SendMessage(connection)
  controllerConfig = ControllerConfigMessage.ReceiveMessage(connection)

  #Print circuit ids and names
  for i in range(len(controllerConfig.Circuits)):
    print("Circuit Id:", controllerConfig.Circuits[i].Id)
    print("Circuit Name:", controllerConfig.Circuits[i].Name)

def ConnectToScreenLogic():
  #Create socket connection to ScreenLogic device
  global connection 
  connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connection.connect((screenlogic_ip, screenlogic_port))

  #Send initial connection message
  ConnectionMessage.SendMessage(connection)

  #Send and receive challenge message
  ChallengeMessage.SendMessage(connection)
  ChallengeMessage.ReceiveMessage(connection) #Receive and ignore challenge response (since only local)

  #Send and receive login message, this is needed for even local connections without password
  LoginMessage.SendMessage(connection)
  LoginMessage.ReceiveMessage(connection) #Receive and ignore login response

def DisconnectFromScreenLogic():
  connection.close()

def SetScreenLogicCircuit(circuitId, state):
  ConnectToScreenLogic()
  SetCircuitStateMessage.SendMessage(connection, circuitId, state)
  DisconnectFromScreenLogic()

def GetPoolStatusJSON():
  ConnectToScreenLogic()

  #Send, receive and process pool status message
  print("Getting Pool Status")
  PoolStatusMessage.SendMessage(connection)
  poolStatus = PoolStatusMessage.ReceiveMessage(connection)

  DisconnectFromScreenLogic()

  json = '{'
  json += '"' + str(AirTempId) + '":"' + str(poolStatus.AirTemp) + '",'
  json += '"' + str(PoolTempId) + '":"' + str(poolStatus.CurrentTemp[0]) + '",'
  json += '"' + str(SpaTempId) + '":"' + str(poolStatus.CurrentTemp[1]) + '",'
  json += '"' + str(PoolCircuitId) + '":"' + str(int(poolStatus.IsPoolActive())) + '",' 
  json += '"' + str(SpaCircuitId) + '":"' +  str(int(poolStatus.IsSpaActive())) + '",'
  json += '"' + str(WaterfallCircuitId) + '":"' +  str(int(poolStatus.IsCircuitActive(WaterfallCircuitId))) + '",'
  json += '"' + str(PoolLightCircuitId) + '":"' +  str(int(poolStatus.IsCircuitActive(PoolLightCircuitId))) + '",'
  json += '"' + str(SpaLightCircuitId) + '":"' +  str(int(poolStatus.IsCircuitActive(SpaLightCircuitId))) + '"'
  json += '}'

  #Show current pool info
  #print("Air Temp:", poolStatus.AirTemp)
  #print("Pool Temp:", poolStatus.CurrentTemp[0])
  #print("Spa Temp:", poolStatus.CurrentTemp[1])
  #print("Pool On:", poolStatus.IsPoolActive())
  #print("Spa On:", poolStatus.IsSpaActive())
  #print("Waterfalls On:", poolStatus.IsCircuitActive(WaterfallCircuitId))
  #print("Pool Light On:", poolStatus.IsCircuitActive(PoolLightCircuitId))
  #print("Spa Light On:", poolStatus.IsCircuitActive(SpaLightCircuitId))

  return json

#Parses and responds to incoming HTTP requests
class GetHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try: 
      #Get index for commands that need it
      indexSplit = self.path.split('/')
      index = None
      if len(indexSplit) > 2 and indexSplit[2].isdigit():
        index = int(indexSplit[2])

      #Parse URL command and send response
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      #if '/GetPCStatus' in self.path and index is not None:
      #    self.wfile.write(bytes(get_pc_status_json(index),'utf-8'))
      #elif self.path == '/GetAllPCStatuses':
      #    self.wfile.write(bytes(get_all_pc_statuses_json(),'utf-8'))
      if '/TurnCircuitOn' in self.path and index is not None:
        SetScreenLogicCircuit(index, 1)  
        self.wfile.write(bytes(str(index) + " turned on",'utf-8'))
      elif '/TurnCircuitOff' in self.path and index is not None:
        SetScreenLogicCircuit(index, 0)
        self.wfile.write(bytes(str(index) + " turned on",'utf-8'))
      else:
          self.wfile.write(bytes("Invalid command",'utf-8'))

    except Exception as e:
      logging.exception("Error processing HTTP request: " + str(e))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): 
     pass 

logging.info('Initializing Pipool')

#Setup and start http server
httpServer = ThreadedTCPServer(("", http_port), GetHandler)
http_server_thread = threading.Thread(target=httpServer.serve_forever) 
http_server_thread.daemon = True 
http_server_thread.start() 

logging.info('Beginning Pipool loop')

#Program loop to send status events to SmartThings
while True:
  try:
    
    requests.put(smartthings_pool_status_event_url, data=GetPoolStatusJSON())
         
    #Wait for next loop
    time.sleep(smartthings_update_frequency)

    #Handle all errors so alarm loop does not end
  except Exception as e:
    logging.exception("Error in loop: " + str(e))
    time.sleep(smartthings_update_frequency)

#print("Turning on Waterfall")
#SetCircuitStateMessage.SendMessage(connection, WaterfallCircuitId, 0)
