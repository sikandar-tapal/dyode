# -*- coding: utf-8 -*-
import time
import os
import sys
import yaml
import modbus
import s7
import logging
import multiprocessing
import asyncore

# Logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def launch_agents(module, properties):
    log.debug(module)
    log.debug(properties)
    if properties['type'] == 'folder':
        log.error('Folder syncing is not supported on this version')
        exit()
    elif properties['type'] == 'modbus':
        log.debug('Modbus agent: %s' % module)
        modbus.modbus_master(module, properties)
    elif properties['type']  == 's7':
        log.debug('Siemens agent: %s' % module)
        # INSERT SIEMENS STUFF HERE
        s7.s7_update(module, properties)
    elif properties['type'] == 'screen':
        log.error('Screen sharing is not supported on this version')
        exit()


if __name__ == '__main__':
    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file)

    # Log info about the configuration file
    log.info('Loading config file')
    log.info('Configuration name : ' + config['config_name'])
    log.info('Configuration version : ' + str(config['config_version']))
    log.info('Configuration date : ' + str(config['config_date']))

    # Iterate on modules
    modules = config.get('modules')
    for module, properties in modules.iteritems():
        #print module
        log.debug('Parsing "' + module + '"')
        log.debug('Trying to launch a new process for module "' + str(module) +'"')
        p = multiprocessing.Process(name=str(module), target=launch_agents, args=(module, properties))
        p.start()

    # TODO : Check if all modules are still alive and restart the ones that are not
