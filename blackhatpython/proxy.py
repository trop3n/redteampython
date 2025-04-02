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

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port)) # 1
    if receive_first: # 2
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer) # 3
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("")