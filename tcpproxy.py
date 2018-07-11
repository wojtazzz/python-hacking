import sys
import socket
import threading

THREAD_COUNT = 5


def usage():
    print "Like this: python tcpproxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
    print "Example: python tcpproxy.py 127.0.0.1 9000 10.10.10.12 9000 True"
    sys.exit(0)


def server_loop(localhost, localport, remotehost, remoteport, receivefirst):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((localhost, localport))
    except:
        print "[!!] Cannot listen on port %s:%d" % (localhost, localport)
        print "[*] Find yourself a better clean port"
        sys.exit(0)

    print "[*] Listening on:  %s:%d" % (localhost, localport)

    server.listen(THREAD_COUNT)

    while True:
        client_socket, address = server.accept()

        print "[*] Received incomming connection from: %s:%d" % (address[0], address[1])

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remotehost, remoteport, receivefirst))

        proxy_thread.start()

def proxy_handler(client_socket, remotehost, remoteport, receivefirst):
    pass



def main():
    if len(sys.argv[1:]) != 5:
        usage()

    localhost = sys.argv[1]
    localport = int(sys.argv[2])

    remotehost = sys.argv[3]
    remoteport = int(sys.argv[4])

    receivefirst = str(sys.argv[5])

    server_loop(localhost, localport, remotehost, remoteport, receivefirst)
   