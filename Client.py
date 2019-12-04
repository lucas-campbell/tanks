#!/usr/bin/env python3
import os
import multiprocessing

from Display import *
#from Memory import *

def main():
    client, gui = multiprocessing.Pipe()
    pid = os.fork()
    if pid == 0:
        GUI(gui)
        print ('Child:  Me:  %s; Parent:  %s' %    \
              (os.getpid(), os.getppid()))
    else:
        Client_loop(client)
        print ('Parent: Me:  %s; Parent:  %s' %    \
              (os.getpid(), os.getppid()))

if __name__ == '__main__':
    main()
