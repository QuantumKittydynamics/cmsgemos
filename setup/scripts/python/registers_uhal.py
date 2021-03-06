import sys, os, time, signal, random
sys.path.append('${GEM_PYTHON_PATH}')

import uhal

gMAX_RETRIES = 11
gRetries = 0
class colors:
    WHITE   = '\033[97m'
    CYAN    = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE    = '\033[94m'
    YELLOW  = '\033[93m'
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    ENDC    = '\033[0m'


def readRegister(device, register, debug=False):
    """
    read register 'register' from uhal device 'device'
    returns value of the register
    """
    global gRetries
    nRetries = 0
    if debug:
        print """Trying to read register %s (%s)\n
address 0x%08x  mask 0x%08x  permission %s  mode 0x%08x  size 0x%08x \n
"""%(register,
   device.getNode(register).getPath(),
   device.getNode(register).getAddress(),
   device.getNode(register).getMask(),
   device.getNode(register).getPermission(),
   device.getNode(register).getMode(),
   device.getNode(register).getSize()
   )
        pass
    while (nRetries < gMAX_RETRIES):
        try:
            controlChar = device.getNode(register).read()
            device.dispatch()
            return controlChar
        except uhal.exception, e:
            nRetries += 1
            gRetries += 1
            if ((nRetries % 10)==0):
                print colors.MAGENTA,"read error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),e,colors.ENDC
                continue
        pass
    return 0x0

def readRegisterList(device, registers, debug=False):
    """
    read registers 'registers' from uhal device 'device'
    returns values of the registers in a dict
    """
    global gRetries
    nRetries = 0
    while (nRetries < gMAX_RETRIES):
        try:
            results = {}
            for reg in registers:
                results[reg] = device.getNode(reg).read()
                pass
            device.dispatch()
            return results
        except uhal.exception, e:
            nRetries += 1
            gRetries += 1
            if ((nRetries % 10)==0):
                print colors.MAGENTA,"read error encountered, retrying operation (%d,%d)"%(nRetries,gRetries),e,colors.ENDC
                continue
            pass
        pass
    return 0x0

def readBlock(device, register, nwords, debug=False):
    """
    read block 'register' from uhal device 'device'
    returns 'nwords' values in the register
    """
    global gRetries
    nRetries = 0
    if debug:
        print """Trying to read register %s (%s)\n
address 0x%08x  mask 0x%08x  permission %s  mode 0x%08x  size 0x%08x \n
"""%(register,
   device.getNode(register).getPath(),
   device.getNode(register).getAddress(),
   device.getNode(register).getMask(),
   device.getNode(register).getPermission(),
   device.getNode(register).getMode(),
   device.getNode(register).getSize()
   )
        pass
    while (nRetries < gMAX_RETRIES):
        try:
            if (debug):
                print "reading %d words from register %s"%(nwords,register)
                pass
            words = device.getNode(register).readBlock(nwords)
            device.dispatch()
            if (debug):
                print words
                pass
            return words
        # want to be able to return nothing in the result of a failed transaction
        except uhal.exception, e:
            nRetries += 1
            gRetries += 1
            # if ('amount of data' in e):
            #     print colors.BLUE, "bad header",register, "-> Error : ", e, colors.ENDC
            # elif ('INFO CODE = 0x4L' in e):
            #     print colors.CYAN, "read error",register, "-> Error : ", e, colors.ENDC
            # elif ('INFO CODE = 0x6L' in e or 'timed out' in e):
            #     print colors.YELLOW, "timed out",register, "-> Error : ", e, colors.ENDC
            # else:
            #     print colors.MAGENTA, "other error",register, "-> Error : ", e, colors.ENDC
            if ((nRetries % 10)==0):
                print colors.MAGENTA,"read error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),e,colors.ENDC
            continue
        pass
    # print colors.RED, "error encountered, retried read operation (%d)"%(nRetries)
    return []
    # return 0x0

def writeRegister(device, register, value, debug=False):
    """
    write value 'value' into register 'register' from uhal device 'device'
    """
    global gRetries
    nRetries = 0
    if debug:
        print """Trying to write value 0x%x to register %s (%s)\n
address 0x%08x  mask 0x%08x  permission %s  mode 0x%08x  size 0x%08x \n
"""%(value,register,
   device.getNode(register).getPath(),
   device.getNode(register).getAddress(),
   device.getNode(register).getMask(),
   device.getNode(register).getPermission(),
   device.getNode(register).getMode(),
   device.getNode(register).getSize()
   )
    while (nRetries < gMAX_RETRIES):
        try:
            device.getNode(register).write(0xffffffff&value)
            device.dispatch()
            return
        
        except uhal.exception, e:
            # if ('amount of data' in e):
            #     print colors.BLUE, "bad header",register, "-> Error : ", e, colors.ENDC
            # elif ('INFO CODE = 0x4L' in e):
            #     print colors.CYAN, "read error",register, "-> Error : ", e, colors.ENDC
            # elif ('INFO CODE = 0x6L' in e or 'timed out' in e):
            #     print colors.YELLOW, "timed out",register, "-> Error : ", e, colors.ENDC
            # else:
            #     print colors.MAGENTA, "other error",register, "-> Error : ", e, colors.ENDC
            nRetries += 1
            gRetries += 1
            if ((nRetries % 10)==0) and debug:
                print colors.MAGENTA,"write error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),e,colors.ENDC
                pass
            continue
        pass
    # print colors.RED, "error encountered, retried test write operation (%d)"%(nRetries)
    pass

def writeRegisterList(device, regs_with_vals, debug=False):
    """
    write value 'value' into register 'register' from uhal device 'device'
    from an input dict
    """
    global gRetries
    nRetries = 0
    while (nRetries < gMAX_RETRIES):
        try:
            for reg in regs_with_vals.keys():
                device.getNode(reg).write(0xffffffff&regs_with_vals[reg])
                pass
            device.dispatch()
            return
        
        except uhal.exception, e:
            nRetries += 1
            gRetries += 1
            if ((nRetries % 10)==0) and debug:
                print colors.MAGENTA,"write error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries),e,colors.ENDC
                pass
            continue
        pass
    pass
