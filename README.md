<img src="https://user-images.githubusercontent.com/1143921/28404945-020c2d66-6cc7-11e7-8829-8129b7eb5ce6.png" align="right" />

# Routing-and-Multicast-using-YDK

> This is an example of a ***modeled*** network configuration.  It's modeled in that the configuration data is abstracted from the instructions and that it interacts with the devices YANG data models.


## The IOS-XE campus topology that this model was based on
![topology](https://user-images.githubusercontent.com/1143921/28403228-8b04ae02-6cbf-11e7-8f57-e7e91595cd18.png)




## Configuration Pre-reqs
* Python3
* IOS-XE 16.5(1) devices
* Mgmt address reachability but otherwise no routing setup
* NETCONF/YANG is setup on these devices
  ```
  csr1000v-1(config)#netconf-yang
  ```
 
## Installation

Follow the instructions to install YDK (these scripts were tested with YDK 0.5.5)

http://ydk.cisco.com/py/docs/getting_started.html

## Examples
- [netmodel.py](https://github.com/rkido/Routing-and-Multicast-using-YDK/blob/master/netmodel.py) - Holds the node class and all node objects with attributes.  Includes routing configuration data.
- [funcs.py](https://github.com/rkido/Routing-and-Multicast-using-YDK/blob/master/funcs.py) - Contains helper functions for the primary scripts.
- [routing_config.py](https://github.com/rkido/Routing-and-Multicast-using-YDK/blob/master/routing_config.py) - Main script to configure routing protocol across the topology with **SHA256 authentication** and **EIGRP stub** at the edge.
- [multicast_config.py](https://github.com/rkido/Routing-and-Multicast-using-YDK/blob/master/multicast_config.py) - Main script to configure **PIM ASM**.  Includes new loopbacks for **Anycast RPs**, **MSDP peers**, and it finds all L3 interfaces, then adds "ip pim sparse-mode" to them.
- [read_native.py](https://github.com/rkido/Routing-and-Multicast-using-YDK/blob/master/read_native.py) - A catch all script to read the entire [IOS-XE Native YANG model](https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1651/Cisco-IOS-XE-native.yang)
## Usage example

Clone the repo, modify the netmodel.py for your environment, then run routing_config.py first, followed by multicast_config.py

*Hint* - If you are using VIRL and are annoyed that your SSH and NETCONF/YANG doesn't survive reboots, add this to your configs:
```
event manager applet ssh-script
 event timer countdown time 10
 action 1.0 cli command "enable"
 action 1.1 cli command "config t"
 action 1.2 cli command "file prompt quiet"
 action 1.3 cli command "crypto key generate rsa modulus 2048"
 action 1.7 cli command "end"
event manager applet pki
 event timer countdown time 20
 action 1.0 cli command "enable"
 action 1.1 cli command "config t"
 action 2.0 cli command "no netconf-yang"
 action 2.1 cli command "netconf-yang" pattern "yes/no"
 action 2.2 cli command "yes"
```

### To Do
- Build routing model with OSPF
- Build multicast model with BiDir-PIM
