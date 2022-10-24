# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti paramiko connection plugin wrapper"""

import os
from typing import List

import openziti
from ansible.plugins.connection.paramiko_ssh import \
    Connection as ParamikoConnection
from ansible.utils.display import Display

display = Display()

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.paramiko
      - community.openziti.openziti
      - community.openziti.openziti_connection
    '''


class Connection(ParamikoConnection):
    '''OpenZiti based connection wrapper for paramiko_ssh'''
    # pylint: disable=import-outside-toplevel

    transport = 'community.openziti.paramiko'

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

    @property
    def identities(self) -> List[str]:
        "Returns loaded identities"
        return self._ziti_identities

    @identities.setter
    def identities(self, identity_list: List[str]) -> None:
        "Loads OpenZiti identities"
        for identity in identity_list:
            openziti.load(identity)
            self._ziti_identities.append(identity)
            display.vvv(f"OPENZITI LOAD IDENTITY: {identity}",
                        host=self.get_option('remote_addr'))

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''

        if self.ziti_log_level < 0:
            self.ziti_log_level = self.get_option('ziti_log_level')

        display.v(f"OPENZITI LOG LEVEL: {self.ziti_log_level}",
                  host=self.get_option('remote_addr'))

        if not self.identities:
            self.identities = self.get_option('ziti_identities')

        with openziti.monkeypatch():
            display.vvv("OPENZITI TUNNELED CONNECTION",
                        host=self.get_option('remote_addr'))
            super()._connect()
