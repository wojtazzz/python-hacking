import getopt
import socket
import subprocess
import sys
import threading

MAX_LISTENING_THREADS = 5
RECV_BUFFER = 14096
FILE_BUFFER_SIZE = 1024

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print "Use it like this:"
    print "wnet.py -t target_host - p port"
    print "-l --listen"
    print "-e --execute=command"
    print "-c --commandshell "
    print "-u --upload=file"
    sys.exit(0)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for option, argument in opts:
        if option in ("-h", "--help"):
            usage()
        elif option in ("-l", "--listen"):
            listen = True
        elif option in ("-e", "--execute"):
            execute = argument
        elif option in ("-c", "--command"):
            command = True
        elif option in ("-u", "--upload"):
            upload_destination = argument
        elif option in ("-t", "--target"):
            target = argument
        elif option in ("-p", "--port"):
            port = int(argument)
        else:
            assert False, "Option unavailable"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()

        client_sender(buffer)

    if listen:
        server_loop()


def client_sender(xbuffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "[] Client socket created"

    try:

        client.connect((target, port))

        print "[] Client connected to %s:%d" % (target, port)

        if len(xbuffer):
            print "[] Stuff found in STDIN buffer. Sending %s to server..." % xbuffer
            client.send(xbuffer)

        while True:

            recv_len = 1
            response = ""

            print "[] Now we are reading response from server. "

            while recv_len:

                data = client.recv(RECV_BUFFER)

                data_length = len(data)
                response += data

                if data_length < RECV_BUFFER:
                    break

            print response,

            xbuffer = raw_input("XX")
            print "after requesting raw input"
            xbuffer += "\n"

            client.send(xbuffer)

    except:
        print "[] Fuckup! Closing..."
        client.close()


def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(MAX_LISTENING_THREADS)

    print "[] Listening on %s:%d" % (target, port)

    while True:
        client_socket, address = server.accept()
        print "[] Received connection from %s" % str(address)
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.rstrip()

    try:
        print "[] Running command: %s" % command
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        print "Executed! Output: %s" % output
    except:
        output = "Could not execute command. \r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):

        file_buffer = ""

        while True:
            data = client_socket.recv(FILE_BUFFER_SIZE)

            if not len(data):
                break
            else:
                file_buffer += data

            save_uploaded_file(client_socket, file_buffer)

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:

        print "[] Received command shell request"
        while True:
            client_socket.send("<WCAT-SHELL:#> ")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(FILE_BUFFER_SIZE)


            output = run_command(cmd_buffer)

            print "Server executed command. Sending back output to client: %s" % output

            client_socket.send(output)


def save_uploaded_file(client_socket, file_buffer):
    try:
        # wb = write to file, binary file (matters on windows)
        file_descriptor = open(upload_destination, "wb")
        file_descriptor.write(file_buffer)
        file_descriptor.close()

        client_socket.send("Saved uploaded file to %s" % upload_destination)

    except:
        client_socket.send("Cound not save file to %s" % upload_destination)


main()
