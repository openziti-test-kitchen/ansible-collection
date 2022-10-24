# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti pylibssh connection plugin wrapper"""
import socket

import ansible_collections.ansible.netcommon.plugins.connection.libssh as PyLibSSH
import openziti
from ansible.utils.display import Display
from ansible_collections.community.openziti.plugins.plugin_utils._mixins import \
    ConnectionMixin

display = Display()

# pylint: disable=too-few-public-methods

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.libssh
      - community.openziti.openziti
      - community.openziti.openziti_connection
    '''


class ZitiSession(PyLibSSH.Session):
    """PyLibSSH Session Wrapper"""
    def __init__(self, *args, **kwargs) -> None:
        self.sock = openziti.socket(type=socket.SOCK_STREAM)
        super().__init__(*args, **kwargs)

    def connect(self, **kwargs) -> None:
        """PyLibSSH.Session.connect wrapper"""
        self.sock.connect((kwargs['host'], kwargs['port']))
        __fd = self.sock.fileno()
        self.set_ssh_options('fd', __fd)
        display.vvv(f"OPENZITI TUNNELED CONNECTION via ZitiSocket fd={__fd}",
                    host=kwargs['host'])
        super().connect(**kwargs)


PyLibSSH.Session = ZitiSession


class Connection(PyLibSSH.Connection, ConnectionMixin):
    '''OpenZiti based connection wrapper for PyLibSSH'''

    transport = 'community.openziti.libssh'

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        if self.ziti_log_level < 0:
            self.ziti_log_level = self.get_option('ziti_log_level')

        if not self.ziti_identities:
            self.ziti_identities = self.get_option('ziti_identities')
        super()._connect()
