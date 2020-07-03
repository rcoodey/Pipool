/**
 *  Pipool
 *
 *  Copyright 2019 Ryan Coodey
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
metadata {
    definition (name: "Pipool Switch", namespace: "rcoodey", author: "Ryan Coodey") {
        capability "Switch"        
        command "statusEvent"
    }

    tiles {
        standardTile("switch", "device.switch", width: 3, height: 2, canChangeIcon: true) {
            state "on", label: 'On', action: "switch.off", icon: "st.Health & Wellness.health2", backgroundColor: "#79b821", nextState:"off"
            state "off", label: 'Off', action: "switch.on", icon: "st.Health & Wellness.health2", backgroundColor: "#ffffff", nextState:"on"
        }
        main(["switch"])
        details(["switch"]) 
    }
}

// handle commands
def statusEvent(state) {
    sendEvent(name: "switch", value: state, isStateChange: true)
}

def on() {
    changeCircuitState("on")
}

def off() {
    changeCircuitState("off")
}

def changeCircuitState(requestedState)
{
    try {
        log.debug "Turning $requestedState $device.name"
        
        //Get URL command and update button label depending on requested state
        def commandPath = null
        if(requestedState == "on") {
            commandPath = "TurnCircuitOn"
            sendEvent(name: "switch", value: "on")
        }
        else if (requestedState == "off") {
            commandPath = "TurnCircuitOff"
            sendEvent(name: "switch", value: "off")
        }
        else
            return
 
        //Setup a hub action to make http request
        def getAction = new physicalgraph.device.HubAction(
            method: "GET",
            path: "/" + commandPath + "/" + device.deviceNetworkId.replace("Pipool", ""),
            headers: [HOST: "192.168.1.4:82"]
        )
        getAction
        //Dont add any code below here, causes the action to not go through for some reason
    } catch (e) {
        log.debug "Error turning $requestedState circuit: $e"
    }
}