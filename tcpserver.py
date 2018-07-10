import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

#arg - max number of requests waiting on backlog queue
#
server.listen(5)

print "[] Listening on %s:%d" % (bind_ip, bind_port)

#Thread to handle client connections
def handle_client(client_socket):

    request = client_socket.recv(1024)

    print "[] Received: %s" % request

    client_socket.send("ACK!")

    client_socket.close()

while True:
    client, address = server.accept()

    print "[] Received connection from %s:%d" % (address[0], address[1])

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
