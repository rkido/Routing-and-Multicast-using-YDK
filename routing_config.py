
from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService
#from ydk.services import CodecService
#from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native
from ydk.types import Empty
import netmodel
import logging
import argparse

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

    # Define a function to represent EIGPR configuration
    def eigrp(x, y):
        x.id = netmodel.eigrpName
        addconfig = x.AddressFamily()
        addconfig.type = Cisco_IOS_XE_native.Native.Router.Eigrp.AddressFamily.TypeEnum.ipv4
        iplist = x.AddressFamily.AfIpList()
        iplist.unicast_multicast = Cisco_IOS_XE_native.Native.Router.Eigrp.AddressFamily.AfIpList.UnicastMulticastEnum.unicast
        iplist.autonomous_system = netmodel.eigrpAS
        # iplist.maximum_paths = 16
        iplist.eigrp.router_id = y.loopback0
        aflist = Cisco_IOS_XE_native.Native.Router.Eigrp.AddressFamily.AfIpList.AfInterface()
        aflist.name = 'default'
        # aflist.passive_interface = Empty()
        aflist.authentication.mode.hmac_sha_256.auth_type = 7
        aflist.authentication.mode.hmac_sha_256.auth_key = netmodel.eigrpSHA256key
        # CREATE IF STATEMENT TO MAKE PRESENCSE CLASS FOR STUB ROUTING
        if y.stub == True:
            iplist.eigrp.stub = Cisco_IOS_XE_native.Native.Router.Eigrp.Eigrp_.Stub()
            iplist.eigrp.stub.connected = Empty()
            iplist.nsf = None
        else:
            iplist.eigrp.stub = None
            iplist.nsf = Empty()

        iplist.topology.base = Cisco_IOS_XE_native.Native.Router.Eigrp.AddressFamily.AfIpList.Topology.Base()

        def netlistappender(appendto, network):
            obj = Cisco_IOS_XE_native.Native.Router.Eigrp.AddressFamily.AfIpList.Network()
            obj.number = network[0]
            obj.wild_card = network[1]
            appendto.append(obj)

        for eigrpnetlist in netmodel.eigrpNetworks.items():
            netlistappender(iplist.network, eigrpnetlist)

        iplist.af_interface.append(aflist)
        addconfig.af_ip_list.append(iplist)
        x.address_family.append(addconfig)

    for device in netmodel.FullNodelist:
        # Instantiate an EIGRP opject
        eigrpobject = Cisco_IOS_XE_native.Native.Router.Eigrp()
        # Create Connection parameters
        connection = NetconfServiceProvider(address=device.mgmtip, netconfport=device.netconfport, username=device.username, password=device.password)
        # Apply the funtion to the object
        eigrp(eigrpobject, device)
        # Apply Configuration over Connection
        x = crud.create(connection, eigrpobject)
        connection.close()


        # BELOW ARE PROVIDER AND CODEC SERVICES IF NEEDED FOR FURTHER VISIBILITY
        # provider = CodecServiceProvider(type="xml")
        # codec = CodecService()
        # xmls = codec.encode(provider, eigrpobject)
        # print xmls

