anycastrpaddr = '10.0.100.1'
anycastrpmask = '255.255.255.255'
eigrpAS = 25
eigrpName = 'production'
eigrpNetwork = '10.0.0.0'
eigrpNetmask = '0.0.255.255'
eigrpSHA256key = 'xYb92kksv3B0P'
#Create a class for all CSR Nodes
class Node():
    def __init__(self, mgmtip, loopback0, stub, rp, msdp_peer=None,
                 netconfport=830, username='{{CHANGE TO YOUR USERNAME', password='{{CHANGE TO YOUR PASSWORD}}'):
        self.mgmtip = mgmtip
        self.loopback0 = loopback0
        self.stub = stub
        self.rp = rp
        self.msdp_peer = msdp_peer
        self.netconfport = netconfport
        self.username = username
        self.password = password

#Instantiate Node Objects with mgmtip and loopback attributes
csr1 = Node('10.92.77.166', '192.168.0.1', stub=False, rp=True, msdp_peer='192.168.0.2')
csr2 = Node('10.92.77.167', '192.168.0.2', stub=False, rp=True, msdp_peer='192.168.0.1')
csr3 = Node('10.92.77.168', '192.168.0.3', stub=True, rp=False)
csr4 = Node('10.92.77.169', '192.168.0.4', stub=True, rp=False)
csr5 = Node('10.92.77.186', '192.168.0.5', stub=True, rp=False)
csr6 = Node('10.92.77.187', '192.168.0.6', stub=True, rp=False)
csr7 = Node('10.92.77.188', '192.168.0.7', stub=True, rp=False)
csr8 = Node('10.92.77.189', '192.168.0.8', stub=True, rp=False)

FullNodelist = [csr6, csr2, csr3, csr4, csr5, csr8, csr7, csr1]
EdgeNodelist = [csr3, csr4, csr5, csr6, csr7, csr8]
CoreNodelist = [csr1, csr2]