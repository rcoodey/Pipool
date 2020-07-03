/**
 *  Pipool Status
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
	definition (name: "Pipool Status", namespace: "rcoodey", author: "Ryan Coodey") {
		capability "Temperature Measurement"
        capability "Sensor"
        
        command "statusEvent"
	}
    
	simulator {
		// TODO: define status and reply messages here
	}
    
	tiles {
		// Main Row 
        valueTile("temperature", "device.temperature", width: 1, height: 1) {
        	state "temperature", label:'${currentValue}', unit: "dF"
        }
 
	    // This tile will be the tile that is displayed on the Hub page. 
	    main(["temperature"])
        
	    // These tiles will be displayed when clicked on the device, in the order listed here. 
	    details(["temperature"]) 
	}
}

// parse events into attributes
def parse(String description) {
	log.debug "Parsing '${description}'"
	// TODO: handle 'contact' attribute
}

// handle commands
def statusEvent(eventVal) {
    sendEvent(name: "temperature", value: eventVal)
    //log.debug event
}