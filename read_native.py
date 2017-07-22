from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService
from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native
import logging
import argparse
from ydk.types import READ

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

    connection = NetconfServiceProvider(address="10.92.77.167", port=830, username="{{CHANGE TO YOUR USERNAME}}", password='{{CHANGE TO YOUR PASSWORD}}')

    crud = CRUDService()

    nativeobject = Cisco_IOS_XE_native.Native()
    nativedata = crud.read(connection, nativeobject)
    provider = CodecServiceProvider(type="xml")
    codec = CodecService()
    xmls = codec.encode(provider, nativedata)
    print (xmls)

    connection.close()