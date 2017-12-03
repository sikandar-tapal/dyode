# -*- coding: utf-8 -*-

import sys
import time
import logging
import pickle
import snap7

# Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Frequency at which to get s7 values
WAIT_TIME = 3

# Connect to the Siemens PLC
s7_plc = snap7.client.Client()

def get_s7(properties):
    print "Performing an action which may throw an exception."

    #Parse the config file and get the data
    log.debug(properties['databases'])
    s7_values = {}
    s7_databases = properties['databases']

    # For each database
    for i in s7_databases:

        # For each set of values
        for j in s7_databases[i]:
            s7_db_start_nb = j.split('-')[0]
            s7_db_end_nb = j.split('-')[1]
            log.debug('DB %s start value : %s' % (i, s7_db_start_nb))
            log.debug('DB %s end value : %s' % (i, s7_db_end_nb))
            s7_db_values_count = int(s7_db_end_nb) - int(s7_db_start_nb)
            log.debug('Number of values to read : %s' % s7_db_values_count)

            # Send the read request to the PLC
            try:
                s7_plc.connect(properties['ip'], 0, 1)
                s7_read_values = s7_plc.db_read(int(i), int(s7_db_start_nb), int(s7_db_values_count))
                s7_plc.disconnect()
                s7_send_serial(pickle.dumps(s7_read_values), properties)
            except Exception, error:
                log.debug('Error connecting to %s to read DB' % properties['ip'])
                log.debug(str(error))

def s7_send_serial(data, properties):
    data_length = len(data)
    encoded_data = base64.b64encode(data)
    data_size = sys.getsizeof(encoded_data)
    log.debug('Data size : %s' % data_size)

    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5
        )

    ser.write(encoded_data)
    log.debug(encoded_data)

def s7_loop(module, properties):
    log.debug('s7 Loop')
    while(1):
        try:
            data = get_s7(properties)
        except Exception, error:
            log.debug('Error while updating s7 values')
            log.debug(str(error))
            continue
        time.sleep(WAIT_TIME)
