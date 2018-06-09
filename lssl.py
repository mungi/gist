#!/usr/bin/env python
"""
List SoftLayer Servers.

The SoftLayer Python API client is required. Use `pip install softlayer` to install it.
The SoftLayer Python client has a built in command for saving this configuration file via the command `sl config setup`.
You can pass environment variables `SL_USERNAME` and `SL_API_KEY`.
For more information see the SL API at:
- https://softlayer-python.readthedocs.org/en/latest/config_file.html
"""

import SoftLayer
import argparse
import itertools
from prettytable import PrettyTable

class ListSoftlayer(object):
    VSI='VirtualServerInstance'
    BMS='BareMetalServer'

    common_col_simple = ['datacenter', 'id', 'fullyQualifiedDomainName', 'primaryIpAddress', 'primaryBackendIpAddress']
    common_col_detail= ['location.pathString', 'id', 'hostname,domain', 'primaryIpAddress', 'primaryBackendIpAddress', 'operatingSystem.passwords']
    vsi_col = ['maxCpu', 'maxMemory', 'activeTransaction.transactionStatus.friendlyName']
    bms_col = ['processorPhysicalCoreAmount', 'memoryCapacity', 'hardwareStatusId']

    def __init__(self):
        self.parse_options()
        self.set_column()

        if self.args.sort not in self.Titles:
            print('The SORT value is invalid. It must exactly match the item title.')
            return

        client = SoftLayer.create_client_from_env()
        self.accountClient = client['SoftLayer_Account']
        self.list_servers()

    def set_column(self):
        if self.args.detail:
            self.Titles = ['Location', 'ServerId', 'Hostname', 'Domain', 'CPU', 'Memory', 'PublicIP', 'PrivateIP', 'Password', 'OS', 'Transaction']
        else:
            self.Titles = ['Location', 'ServerId', 'FQDN', 'CPU', 'Memory', 'PublicIP', 'PrivateIP']
        self.listSL = PrettyTable(self.Titles)

        if self.args.detail:
            self.listSL.align['Location'] = 'l'
            self.listSL.align['Hostname'] = 'r'
            self.listSL.align['Domain'] = 'l'

    def parse_options(self):
        '''Parse all the arguments from the CLI'''

        parser = argparse.ArgumentParser(description='Print Server list of SoftLayer')
        parser.add_argument('-t', '--type', action='store', default='all',choices=['all','vm','bm'],
                            help='Select Server Type (default: all)')
        parser.add_argument('-d', '--detail', action='store_true', default=False,
                            help='Display detail information like a Server Location, Password, Status (default: false)')
        parser.add_argument('-s', '--sort', action='store', default='Location',
                            help='Sort by the Column Title (default: Location)')
        self.args = parser.parse_args()

    def add_servers(self, type):
        type_col = self.vsi_col if type == self.VSI else self.bms_col
        if self.args.detail:
            common_col = self.common_col_detail
        else:
            common_col = self.common_col_simple
            type_col = type_col[0:2]

        self.mask = "mask[%s]" % ','.join(itertools.chain(common_col, type_col))
        servers = self.accountClient.getVirtualGuests(mask=self.mask) if type == self.VSI else self.accountClient.getHardware(mask=self.mask)

        for srv in servers:
            if self.args.detail:
                location = srv['location'].get('pathString') if srv.get('location') else '-'
                passwd = srv['operatingSystem'].get('passwords')[0].get('password') if srv.get('operatingSystem') and srv['operatingSystem'].get('passwords') else '-'
                osVer = srv['operatingSystem'].get('softwareLicense').get('softwareDescription').get('referenceCode') if (srv.get('operatingSystem') and srv['operatingSystem'].get('softwareLicense')) else '-'
                if type == self.VSI:
                    transaction = 'VM: ' + srv['activeTransaction'].get('transactionStatus').get('friendlyName') if srv.get('activeTransaction') else 'VM'
                else:
                    transaction = 'BM: ' + str(srv.get('hardwareStatusId'))

                self.listSL.add_row([
                    location,
                    srv['id'],
                    srv['hostname'],
                    srv['domain'],
                    srv[type_col[0]],
                    srv[type_col[1]],
                    srv.get('primaryIpAddress'),
                    srv.get('primaryBackendIpAddress'),
                    passwd,
                    osVer,
                    transaction
                ])
            else:
                dcname = srv['datacenter'].get('longName') if srv.get('datacenter') else '-'
                self.listSL.add_row([
                    dcname,
                    srv['id'],
                    srv['fullyQualifiedDomainName'],
                    srv[type_col[0]],
                    srv[type_col[1]],
                    srv.get('primaryIpAddress'),
                    srv.get('primaryBackendIpAddress'),
                ])

    def list_servers(self):
        if self.args.type == 'all' or  self.args.type == 'vm':
            self.add_servers(self.VSI)
        if self.args.type == 'all' or  self.args.type == 'bm':
            self.add_servers(self.BMS)
        print(self.listSL.get_string(sortby=self.args.sort))

ListSoftlayer()
