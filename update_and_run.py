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

##### Public Variables go here
auth_token = ''

##### Function definitions
def get_auth_token():
    """Gets an authentication token from Front Door using the Key authentication"""
    
    global auth_token
    
    data = {"keyAccess": APIPUBLICKEY, "keySecret": APISECRETKEY}
    resp = requests.post(FRONTDOOR_URL, headers={"Content-Type": "application/json"}, json=data)
    
    if resp.status_code == 200:
        auth_token = resp.headers['apptio-opentoken']
    else:
        raise ValueError("could not authenticate, got response: " + str(resp.status_code) + ": " + resp.json()["error"])

def get_connector_config():
    """Gets the connector configuration JSON for a given connector and agent."""

    if auth_token == '':
      get_auth_token()
    
    connector_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agent_id + "/connector/" + connectorid
    connector_config_resp = requests.get(connector_url, headers={"Content-Type": "application/json", "apptio-opentoken": auth_token})
    if connector_config_resp.status_code == 200:
        return connector_config_resp.json()
    else:
        print ("Error Code: " + str(connector_config_resp.status_code))
        raise ValueError("Could not retrieve the connector configuration, got response: " + str(connector_config_resp.status_code) + ": " + connector_config_resp.json()["error"])

def update_connector_config(connectorid, connectorconfig):
    """Updates the connector configuration for a given connector ID and agent."""

    if auth_token == '':
      get_auth_token()
    
    connector_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agent_id + "/connector/" + connectorid
    connector_config_resp = requests.put(connector_url, headers={"Content-Type": "application/json", "apptio-opentoken": auth_token}, json=connectorconfig)
    if connector_config_resp.status_code == 204:
        print("Connector Update in progress...")
        return None
    else:
        print ("Error Code: " + str(connector_config_resp.status_code))
        raise ValueError("Could not update the connector configuration, got response: " + str(connector_config_resp.status_code) + ": " + str(connector_config_resp.content))

def get_connector_status(connectorid):
    """Gets the connector status for a given connector and agent."""

    if auth_token == '':
      get_auth_token()
    
    connector_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agent_id + "/connector/" + connectorid + "/status"
    connector_config_resp = requests.get(connector_url, headers={"Content-Type": "application/json", "apptio-opentoken": auth_token})
    if connector_config_resp.status_code == 200:
        return connector_config_resp.json()['status']
    else:
        raise ValueError("Could not get the connector status, got response: " + str(connector_config_resp.status_code) + ": " + connector_config_resp.json()["error"])

def kick_off_connector(connectorid):
    """Kicks off the connector for a given agent."""

    if auth_token == '':
      get_auth_token()
    
    connector_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agent_id + "/connector/" + connectorid + "/execute"
    data = {"task": "ExecuteConnector"}
    connector_config_resp = requests.post(connector_url, headers={"Content-Type": "application/json", "apptio-opentoken": auth_token}, json=data)

    if connector_config_resp.status_code == 202:
        print("Connector Kicked Off!")
        return None
    else:
        raise ValueError("Could not kick off the connector, got response: " + str(connector_config_resp.status_code) + ": " + connector_config_resp.json()["error"])

def get_connector_list():
    """Gets the list of connectors attached to an agent"""

    if auth_token == '':
      get_auth_token()
    
    connector_list_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agent_id + "/connector?include=name,type,lastRun,status"
    connector_list_resp = requests.get(connector_list_url, headers={"Content-Type": "application/json", "apptio-opentoken": auth_token})
    if connector_list_resp.status_code == 200:
        return connector_list_resp.json()['result']
    else:
        raise ValueError("Could not retrieve the connector configuration, got response: " + str(connector_list_resp.status_code) + ": " + connector_list_resp.json()["error"])
        
def get_agent_list():
    """Gets the list of agents attached to DataLink Manager"""

    if auth_token == '':
      get_auth_token()
    
    agent_list_url = BASEURL4DATALINK +  "/api/v1/resource/agent/"
    agent_list_resp = requests.get(agent_list_url, headers={"Content-Type": "application/json", "apptio-opentoken": auth_token})
    if agent_list_resp.status_code == 200:
        return agent_list_resp.json()['result']
    else:
        raise ValueError("Could not retrieve the agent list, got response: " + str(agent_list_resp.status_code) + ": " + agent_list_resp.json()["error"])

def get_agent_details(agentid):
    """Gets the details of a specific agent"""

    if auth_token == '':
      get_auth_token()
    
    agent_details_url = BASEURL4DATALINK +  "/api/v1/resource/agent/" + agentid
    agent_details_resp = requests.get(agent_details_url, headers={"Content-Type": "application/json", "apptio-opentoken": auth_token})
    if agent_details_resp.status_code == 200:
        return agent_details_resp.json()
    else:
        raise ValueError("Could not retrieve the agent list, got response: " + str(agent_details_resp.status_code) + ": " + agent_details_resp.json()["error"])
        
def gotosleep(secs):
    """ Function to wait for n seconds """
    print("Sleeping for " + str(secs) + " seconds")
    time.sleep(secs)
     
##### Actual Script starts here
