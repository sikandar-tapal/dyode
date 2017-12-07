# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import random
import string
import yaml
import base64
import pickle
import struct
import serial
import snap7

# Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def s7_update(module, properties):
    server = snap7.server.Server()
    size = 1000
    DBdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    #PAdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    # Parse properties to get the DB to instanciate
    s7_databases = properties['databases']
    # For each database
    for i in s7_databases:
        server.register_area(snap7.snap7types.srvAreaDB, i, DBdata)




    #server.register_area(snap7.snap7types.srvAreaPA, 1, PAdata)

    server.start(tcpport=properties['port_out'])
    while True:
        while True:
            # update values coming through the serial Line
            # s7_new_data = get_s7_data_serial()
            # parse_s7_data(s7_new_data)
            # for database in s7_new_data:
                # for startaddress in database:
                    # snap7.util.set_string(DBdata, 0, s7_new_data[database][startaddress], 256)
            event = server.pick_event()
            if event:
                log.info(server.event_text(event))
            else:
                break
        time.sleep(1)

def get_s7_data_serial():
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )

    x=ser.readline()
    if len(x) > 0:
        decoded_data = base64.b64decode(x)
        log.debug(pickle.loads(decoded_data))
	return pickle.loads(decoded_data)
