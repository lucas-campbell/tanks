#!/usr/bin/env python3
import os
import sys
import multiprocessing

from Display import *
#from Memory import *

class Msg:
    def __init__(self, the_msg):
        self.m = the_msg

def main():
    client, gui = multiprocessing.Pipe()
    pid = os.fork()
    if pid == 0:
        for i in range(5):
            gui.send(Msg("Hey" + str(i)))
            c_msg = gui.recv()
            print("Client sent: " + c_msg.m)
        gui.send(Msg("die"))
        print("Closed gui fds")
        sys.exit()
        print("shouldn't happen")

##############################################################
    else:
        try:
            while(True):
                msg = client.recv()
                if msg.m == "die":
                    exit(0)
                print(msg.m)
                client.send(Msg("suh"))
        except Exception:
            print("Nothing left")

if __name__ == '__main__':
    main()

