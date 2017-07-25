
from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService
from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native
from ydk.types import Empty
import netmodel
import logging
import argparse
import xmltodict
from funcs import intobjectselector, nameSelector
from collections import OrderedDict

if __name__ == "__main__":
    """Execute main program."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', "--verbose", help="print debugging messages",
                        action="store_true")
    # parser.add_argument('-n', required=True, help='specify node(s) ; Mandatory', nargs='*')
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                       "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Create a CRUD Service
    crud = CRUDService()

    # Define a function to represent Multicast configuration
    def multicast(obj, node, l3intlist):
        obj.ip.multicast_routing = Cisco_IOS_XE_native.Native.Ip.MulticastRouting()
        obj.ip.multicast_routing.distributed = Empty()
        obj.ip.multicast_routing._is_presence = True
        # Sort the l3intlist so they are grouped by interface type
        l3intlist.sort(key=str.lower)
        # Make the l3intlist all lowercase
        lowerl3intlist = map(lambda x: x.lower(), l3intlist)
        # Add PIM Sparse to all interfaces of l3intlist
        for ints in lowerl3intlist:
            interfacetype = ''.join(i for i in ints if not i.isdigit())
            intconfiglist = None
            intconfiglist = intobjectselector(interfacetype)
            intconfiglist.name = nameSelector(ints)
            intconfiglist.ip.pim.sparse_mode = Cisco_IOS_XE_native.Native.Interface.Loopback.Ip.Pim.SparseModeEnum.sparse_mode
            getattr(obj.interface, interfacetype).append(intconfiglist)
            #obj.interface.interfacetype.append(intconfiglist)
        #IF DEVICE IS NOT RP - SET AUTORP LISTENER and IP PIM SPARSE-MODE ON L3 INTERFACES AND SETUP LOOP1 FIRST!!!
        if node.rp == False:
            obj.ip.pim.autorp = Cisco_IOS_XE_native.Native.Ip.Pim.Autorp()
            obj.ip.pim.autorp.listener = Empty()
            obj.ip.pim.register_source = "Loopback0"
        else:
            rpannounceintlist = obj.Ip.Pim.SendRpAnnounce.Interface_List()
            rpannounceintlist.if_name = "Loopback1"
            rpannounceintlist.scope.pkt_ttl = 30
            obj.ip.pim.send_rp_announce.interface_list.append(rpannounceintlist)
            obj.ip.msdp.originator_id = "Loopback0"
            obj.ip.msdp.peer.addr = node.msdp_peer
            obj.ip.msdp.peer.connect_source = "Loopback0"
            obj.ip.pim.send_rp_discovery.scope = 30
        return obj

    # Define a function to add Loopback interface for AnycastRP
    def addloopback(obj, node):
        if node.rp == True:
            newloopbacklist = obj.Interface.Loopback()
            newloopbacklist.name = 1
            newloopbacklist.ip.address.primary.address = netmodel.anycastrpaddr
            newloopbacklist.ip.address.primary.mask = netmodel.anycastrpmask
            newloopbacklist.ip.pim.sparse_mode = Cisco_IOS_XE_native.Native.Interface.Loopback.Ip.Pim.SparseModeEnum.sparse_mode
            obj.interface.loopback.append(newloopbacklist)
        else:
            modloopbacklist = obj.Interface.Loopback()
            modloopbacklist.name = 0
            modloopbacklist.ip.pim.sparse_mode = Cisco_IOS_XE_native.Native.Interface.Loopback.Ip.Pim.SparseModeEnum.sparse_mode
            obj.interface.loopback.append(modloopbacklist)
            pass
        return obj

    for device in netmodel.FullNodelist:
        # Instantiate an Multicast Configuration opject
        multicastobject = Empty()
        multicastobject = Cisco_IOS_XE_native.Native()
        loopbackobject = Empty()
        loopbackobject = Cisco_IOS_XE_native.Native()
        readintobject = Cisco_IOS_XE_native.Native.Interface()
        l3intlist = []
        # Create Connection parameters
        connection = NetconfServiceProvider(address=device.mgmtip, port=device.netconfport, username=device.username, password=device.password)
        # Read Interface YANG Model
        nativereaddata = crud.read(connection, readintobject)
        provider = CodecServiceProvider(type="xml")
        codec = CodecService()
        xmls = codec.encode(provider, nativereaddata)
        # Convert Read Interface Data to Dictionary and parse for L3 Interface List
        returneddict = xmltodict.parse(xmls)
        xmllist = list(returneddict['interface'].keys())
        xmlmoddedlist = xmllist[1:]

        # Interate over Interfaces to create a list of L3 interfaces
        rawl3intlist = [inttype.capitalize() + intlist['name'] if type(intlist) is OrderedDict else inttype.capitalize() + returneddict['interface'][inttype]['name'] if intlist == 'name' else None
                     for inttype in xmlmoddedlist for intlist in returneddict['interface'][inttype]]
        l3intlist = list(filter(lambda x: x != None, rawl3intlist))
        # l3intlist = [intDictConverter(returneddict, inttype, intlist)for inttype in xmlmoddedlist for intlist in returneddict['interface'][inttype] if intDictConverter(returneddict, inttype, intlist) != None ]
        # for inttype in xmlmoddedlist:
        #     for intlist in returneddict['interface'][inttype]:
        #         if type(intlist) is OrderedDict:
        #             l3intlist.append(inttype.capitalize() + intlist['name'])
        #         elif intlist == 'name':
        #             l3intlist.append(inttype.capitalize() + returneddict['interface'][inttype]['name'])
        #         else:
        #             break
        # Apply the funtion to the object
        loopbackdata = addloopback(loopbackobject, device)
        xaddloopback = crud.create(connection, loopbackdata)
        # Apply Configuration over Connection
        configdata = multicast(multicastobject, device, l3intlist)
        xmulticast = crud.create(connection, configdata)
        connection.close()
