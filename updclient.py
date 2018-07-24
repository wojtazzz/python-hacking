import socket

host = "127.0.0.1"
port = 80

client =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind a server socket
client.bind((host, port))

client.sendto("AASFAFDFD", (host, port))

data = client.recvfrom(4097)

print data
print "-----XXX---------------------------------"
