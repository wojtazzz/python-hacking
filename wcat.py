import sys
import socket
import getopt
import threading
import subprocess

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
    print "-e --execute=file"
    print "-c --command"
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
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",
                                   ["help","listen","execute","target","port","command","upload"])
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

        if listen
            server_loop()

main()
