import sys
import socket
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]) # 1 

def hexdump(src, length=16, show=True):
    if isinstance(src, bytes): # 2
        src = src.decode()

    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])  # 3

    printable = word.translate(HEX_FILTER) # 4
    hexa = ' '.join([f'{ord(c):02X}' for c in word])
    hexwidth = length*3

    results.append(f'{i:04x}{hexa:<{hexwidth}}{printable}') # 5
    if show:
        for line in results:
            print(line)
        else:
            return results
        
def receive_from(connection): # 1
    buffer = b"" 
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096) # 2
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

def request_handler(buffer):
    # perform packet modifications
    return buffer
def response_handler(buffer):
    # perform packet modifications
    return buffer

