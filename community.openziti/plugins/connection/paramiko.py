# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti paramiko connection plugin wrapper"""

import openziti
from ansible.plugins.connection.paramiko_ssh import \
    Connection as ParamikoConnection
from ansible.utils.display import Display
from ansible_collections.community.openziti.plugins.plugin_utils._mixins import \
    ConnectionMixin

display = Display()

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.paramiko
      - community.openziti.openziti
      - community.openziti.openziti_connection
    '''


class Connection(ParamikoConnection, ConnectionMixin):
    '''OpenZiti based connection wrapper for paramiko_ssh'''
    # pylint: disable=import-outside-toplevel

    transport = 'community.openziti.paramiko'

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''

        if self.ziti_log_level < 0:
            self.ziti_log_level = self.get_option('ziti_log_level')

        if not self.ziti_identities:
            self.ziti_identities = self.get_option('ziti_identities')

        with openziti.monkeypatch():
            display.vvv("OPENZITI TUNNELED CONNECTION",
                        host=self.get_option('remote_addr'))
            super()._connect()
