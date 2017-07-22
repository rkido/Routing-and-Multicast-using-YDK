from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native

def intobjectselector(inttype):
    try:
        if inttype == 'loopback':
            return Cisco_IOS_XE_native.Native.Interface.Loopback()
        elif inttype == 'fortygigabitethernet':
            return Cisco_IOS_XE_native.Native.Interface.Fortygigabitethernet()
        elif inttype == 'gigabitethernet':
            return Cisco_IOS_XE_native.Native.Interface.Gigabitethernet()
        elif inttype == 'tengigabitethernet':
            return Cisco_IOS_XE_native.Native.Interface.Tengigabitethernet()
        elif inttype == 'tunnel':
            return Cisco_IOS_XE_native.Native.Interface.Tunnel()
        elif inttype == 'vlan':
            return Cisco_IOS_XE_native.Native.Interface.Vlan()
        elif inttype == 'fastethernet':
            return Cisco_IOS_XE_native.Native.Interface.Fastethernet()
        elif inttype == 'multilink':
            return Cisco_IOS_XE_native.Native.Interface.Multilink()
        elif inttype == 'port_channel':
            return Cisco_IOS_XE_native.Native.Interface.PortChannel()
        elif inttype == 'serial':
            return Cisco_IOS_XE_native.Native.Interface.Serial()
        else:
            raise NameError
    except NameError:
        print ('inttype did not match a valid YDK Interface type')

def nameSelector(fullInterface):
    try:
        if ''.join(i for i in fullInterface if not i.isdigit()) == 'loopback':
            return int(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'fortygigabitethernet':
            return str(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'gigabitethernet':
            return str(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'tengigabitethernet':
            return str(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'tunnel':
            return int(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'vlan':
            return int(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'fastethernet':
            return str(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'multilink':
            return int(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'port_channel':
            return int(''.join(i for i in fullInterface if not i.isalpha()))
        elif ''.join(i for i in fullInterface if not i.isdigit()) == 'serial':
            return str(''.join(i for i in fullInterface if not i.isalpha()))
        else:
            raise NameError
    except NameError:
        print ('inttype did not match a valid YDK Interface type')
