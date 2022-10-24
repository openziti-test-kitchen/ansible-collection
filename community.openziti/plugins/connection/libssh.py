# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti pylibssh connection plugin wrapper"""
import os
import socket
from typing import List

import ansible_collections.ansible.netcommon.plugins.connection.libssh as PyLibSSH
import openziti
from ansible.utils.display import Display

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


class Connection(PyLibSSH.Connection):
    '''OpenZiti based connection wrapper for PyLibSSH'''

    transport = 'community.openziti.libssh'

    def __init__(self, *args, **kwargs) -> None:
        self._ziti_identities: List[str] = []
        self._ziti_log_level = int(os.getenv('ZITI_LOG', '-1'))
        super().__init__(*args, **kwargs)

    @property
    def ziti_log_level(self) -> int:
        "Returns ziti log level"
        return self._ziti_log_level

    @ziti_log_level.setter
    def ziti_log_level(self, log_level: int) -> None:
        if log_level is not None:
            verbosity = log_level
        else:
            verbosity = display.verbosity
        self._ziti_log_level = verbosity
        os.environ['ZITI_LOG'] = str(verbosity)
        display.v(f"OPENZITI LOG LEVEL SET TO: {self.ziti_log_level}",
                  host=self.get_option('remote_addr'))

    @property
    def ziti_identities(self) -> List[str]:
        "Returns loaded identities"
        return self._ziti_identities

    @ziti_identities.setter
    def ziti_identities(self, identities: List[str]) -> None:
        "Loads OpenZiti identities"
        for identity in identities:
            openziti.load(identity)
            self._ziti_identities.append(identity)
            display.vvv(f"OPENZITI LOAD IDENTITY: {identity}",
                        host=self.get_option('remote_addr'))

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        if self.ziti_log_level < 0:
            self.ziti_log_level = self.get_option('ziti_log_level')

        if not self.ziti_identities:
            self.ziti_identities = self.get_option('ziti_identities')
        super()._connect()
