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


def receive_from(socket):
    buffer = ""

    socket.settimeout(21)

    try:
        while True:
            data = socket.recv(4096)

            if not data:
                break
            buffer+=data
    except:
        print "Failed to receive data"

    return buffer

def hexdump(remote_buffer):
    pass


def response_modifier(buffer):
    return buffer

def request_modifier(buffer):
    return buffer

def proxy_handler(client_socket, remotehost, remoteport, receivefirst):

    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remotehost, remoteport))

    if receivefirst:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # Optionally modify data in transit
        # remote_buffer = response_modyfier(remote_buffer)

        if len(remote_buffer):
            print "[<==] Sending %s bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)

    while True:

        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print "Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)

            # local_buffer = request_modifier(local_buffer)
            remote_socket.send(local_buffer)
            print "[==>] Sent data to remote host"

            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):

                print "[<==] Received %d bytes from remote host." % len(remote_buffer)

                hexdump(remote_buffer)

                # remote_buffer = response_modifier(remote_buffer)

                client_socket.send(remote_buffer)

                print "[<==] Send to localhost."

            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print "[*] No more data. Closed all connections."

                break


def main():
    if len(sys.argv[1:]) != 5:
        usage()

    localhost = sys.argv[1]
    localport = int(sys.argv[2])

    remotehost = sys.argv[3]
    remoteport = int(sys.argv[4])

    receivefirst = str(sys.argv[5])

    server_loop(localhost, localport, remotehost, remoteport, receivefirst)
