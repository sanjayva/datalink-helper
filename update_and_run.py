# -*- coding: utf-8 -*-
    
import requests
import json
import urllib
import time

##### Declarations go here
FRONTDOOR_URL = 'https://frontdoor.apptio.com/service/apikeylogin'
APIPUBLICKEY = 'PLEASE_ADD_THIS'
APISECRETKEY = 'PLEASE_ADD_THIS'
BASEURL4DATALINK = 'https://CUSTOMER-manager.apptio.com' #<< Please update this too
agent_id = 'PLEASE_ADD_THIS'

##### Function definitions
def get_auth_token(public_key, secret_key):
    """Gets an authentication token from Front Door using the Key authentication"""
    data = {"keyAccess": public_key, "keySecret": secret_key}
    resp = requests.post(FRONTDOOR_URL, headers={"Content-Type": "application/json"}, json=data)

    if resp.status_code == 200:
        return resp.headers['apptio-opentoken']
    else:
        raise ValueError("could not authenticate, got response: " + str(resp.status_code) + ": " + resp.json()["error"])

def get_connector_config(authtoken, agentid, connectorid):
    """Gets the connector configuration JSON for a given connector and agent."""
    connector_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agentid + "/connector/" + connectorid
    connector_config_resp = requests.get(connector_url, headers={"Content-Type": "application/json", "apptio-opentoken": authtoken})
    if connector_config_resp.status_code == 200:
        return connector_config_resp.json()
    else:
        print ("Error Code: " + str(connector_config_resp.status_code))
        raise ValueError("Could not retrieve the connector configuration, got response: " + str(connector_config_resp.status_code) + ": " + connector_config_resp.json()["error"])

def update_connector_config(authtoken, agentid, connectorid, connectorconfig):
    """Updates the connector configuration for a given connector ID and agent."""
    connector_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agentid + "/connector/" + connectorid
    #print(connector_url)
    #data={'apptioSource': {'specificDateV2': 'Feb:FY2016'}}
    #jsonconnectorconfig = connectorconfig
    #json.dumps(connectorconfig) 
    #print(jsonconnectorconfig)
    connector_config_resp = requests.put(connector_url, headers={"Content-Type": "application/json", "apptio-opentoken": authtoken}, json=connectorconfig)
    if connector_config_resp.status_code == 204:
        print("Connector Update in progress...")
        return None
    else:
        print ("Error Code: " + str(connector_config_resp.status_code))
        raise ValueError("Could not update the connector configuration, got response: " + str(connector_config_resp.status_code) + ": " + str(connector_config_resp.content))

def get_connector_status(authtoken, agentid, connectorid):
    """Gets the connector status for a given connector and agent."""
    connector_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agentid + "/connector/" + connectorid + "/status"
    connector_config_resp = requests.get(connector_url, headers={"Content-Type": "application/json", "apptio-opentoken": authtoken})
    if connector_config_resp.status_code == 200:
        return connector_config_resp.json()['status']
    else:
        raise ValueError("Could not get the connector status, got response: " + str(connector_config_resp.status_code) + ": " + connector_config_resp.json()["error"])

def kick_off_connector(authtoken, agentid, connectorid):
    """Kicks off the connector for a given agent."""
    connector_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agentid + "/connector/" + connectorid + "/execute"
    data = {"task": "ExecuteConnector"}
    connector_config_resp = requests.post(connector_url, headers={"Content-Type": "application/json", "apptio-opentoken": authtoken}, json=data)
    #print(connector_config_resp.status_code)
    if connector_config_resp.status_code == 202:
        print("Connector Kicked Off!")
        return None
    else:
        raise ValueError("Could not kick off the connector, got response: " + str(connector_config_resp.status_code) + ": " + connector_config_resp.json()["error"])

def get_connector_list(authtoken, agentid):
    """Gets the list of connectors attached to an agent"""
    connector_list_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agentid + "/connector?include=name,type,lastRun,status"
    connector_list_resp = requests.get(connector_list_url, headers={"Content-Type": "application/json", "apptio-opentoken": authtoken})
    if connector_list_resp.status_code == 200:
        return connector_list_resp.json()['result']
    else:
        raise ValueError("Could not retrieve the connector configuration, got response: " + str(connector_list_resp.status_code) + ": " + connector_list_resp.json()["error"])
        
def gotosleep(secs):
    """ Function to wait for n seconds """
    print("Sleeping for " + str(secs) + " seconds")
    time.sleep(secs)
     
##### Actual Script starts here

##### List of Connectors to update
connector_list = ["6970bdbe-916f-4295-a181-4392ef1d8019",
                  "8e18c840-b215-4e41-8772-1204aa2651f7",
                  "4b9b530d-9e45-4abd-9bfe-6019046526d0",
                  "b31d34e0-d834-475c-8748-3374f513584a",
                  "fb08b3e9-d9c0-467e-be0a-26a419ba1b4a",
                  "e59396cd-3a69-4ed4-a612-27fa6328d7a1"]
      
  
month_list = [["2018", "SEPTEMBER", "Sep:FY2018"]]

Run_Connectors = True

auth_token = get_auth_token(APIPUBLICKEY, APISECRETKEY)



for ctmonth in month_list:
    print("Starting iteration for: " +ctmonth[0] + " / " + ctmonth[1] + " / " + ctmonth[2])
    for connector_id in connector_list:

        # Get the connector configuration json
        connector_config = get_connector_config(auth_token, agent_id, connector_id)

        #print (connector_config)
        print("Working on Datalink Connector: " + connector_config['identity']['name'] + " - the current date is " + connector_config['apptioSource']['specificDateV2'] + " and month/year to " + connector_config['apptioSource']['month'] + "-" +  str(connector_config['apptioSource']['year']) + ".")
        # update json to the current month
        connector_config['apptioSource']['timePeriod'] = 'SPECIFIC'
        connector_config['apptioSource']['calendarType'] = 'FISCAL'
        connector_config['apptioSource']['useDateV2'] = True
        connector_config['apptioSource']['specificDateV2'] = ctmonth[2]
        connector_config['apptioSource']['month'] = ctmonth[1]
        connector_config['apptioSource']['year'] = ctmonth[0]
        connector_config['schedule']['enabled'] = True
                              
        # update connector on datalink with updated json (effectively making it run for the new month)
        update_connector_config(auth_token, agent_id, connector_id,connector_config)
        print("Successfully updated Datalink Connector: " + connector_config['identity']['name'] + " date to " + connector_config['apptioSource']['specificDateV2'] + " and month/year to " + connector_config['apptioSource']['month'] + "-" +  str(connector_config['apptioSource']['year']) + ".")
        
        while Run_Connectors:
            # Kick off the connecter
            kick_off_connector(auth_token, agent_id, connector_id)
            
            #Stopping this block
            # check every 15 seconds on the status of the connector
            while True:
                gotosleep(15)
                current_connector_status = get_connector_status(auth_token, agent_id, connector_id)
                if current_connector_status == 'SUCCESS':
                    print("Connector Run is complete.")
                    break
                if current_connector_status == 'FAILURE':
                    print("Connector Failed :(. Going to rerun after 5 mins.")
                    gotosleep(285)
                    kick_off_connector(auth_token, agent_id, connector_id)
            break
