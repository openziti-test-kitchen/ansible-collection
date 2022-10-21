# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti pylibssh connection plugin wrapper"""
import os
import socket

import ansible_collections.ansible.netcommon.plugins.connection.libssh as PyLibSSH
import openziti

# pylint: disable=too-few-public-methods

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.libssh
      - community.openziti.openziti
      - community.openziti.anzible
    '''


class ZitiSession(PyLibSSH.Session):
    """PyLibSSH Session Wrapper"""
    def __init__(self, *args, **kwargs):
        self.sock = openziti.socket(type=socket.SOCK_STREAM)
        super().__init__(*args, **kwargs)

    def connect(self, **kwargs):
        """PyLibSSH.Session.connect wrapper"""
        self.sock.connect((kwargs['host'], kwargs['port']))
        self.set_ssh_options('fd', self.sock.fileno())
        super().connect(**kwargs)


PyLibSSH.Session = ZitiSession


class Connection(PyLibSSH.Connection):
    '''OpenZiti based connection wrapper for PyLibSSH'''

    transport = 'community.openziti.libssh'

    def _connect(self):
        '''Wrap connection activation object with OpenZiti'''

        log_level = self.get_option('ziti_log_level')
        if os.getenv('ZITI_LOG') is None:
            os.environ['ZITI_LOG'] = str(log_level)
        identities = self.get_option('ziti_identities')
        for identity in identities:
            openziti.load(identity)

        super()._connect()
