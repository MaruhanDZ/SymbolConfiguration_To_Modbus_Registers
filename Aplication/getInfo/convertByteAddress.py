import re

def getByteAddress(direct_address):

    match = re.match(r"%([A-Z]+)([\d\.]+)", direct_address)

    if not match:
        return None

    area = match.group(1)
    address = match.group(2)

    if area == "MX":
        return int(address.split('.')[0])

    address = int(address)

    if area == "MB":
        return address
    elif area == "MW":
        return address * 2
    elif area == "MD":
        return address * 4
    elif area == "ML":
        return address * 8

    return None
    

if __name__ == "__main__":
    print('input', 'output')
    print("%ML50", getByteAddress("%ML50"))  # Byte 50, retornar 400
    print("%MD100", getByteAddress("%MD100")) # Byte 100, retornar 400
    print("%MW20", getByteAddress("%MW20"))  # Byte 20, retornar 40
    print("%MB30", getByteAddress("%MB30"))  # Byte 30, retornar 30
    print("%MX10.5", getByteAddress("%MX10.5"))   # Byte 10 bit 5, retornar 10
