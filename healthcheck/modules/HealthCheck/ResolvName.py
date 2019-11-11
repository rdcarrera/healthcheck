import socket
def main(host):
    try:    
        socket.gethostbyname(host)
        return True
    except:
        return False