#!/usr/bin/env python3
##########################
# Cam, Lucas, Omar
# 11/5/19
# TMessage Class
##########################
import sys
from Arena import *

class TMessage:
    def __init__(self, clientTank : Tank, serverTank : Tank, clientXY : Tuple, serverXY : Tuple):
        self._clientTank = clientTank
        self._clientXY = clientXY
        self._serverTank = serverTank
        self._serverXY = serverXY
        
