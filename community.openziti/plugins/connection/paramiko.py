# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti paramiko connection plugin wrapper"""

import os

from ansible.plugins.connection.paramiko_ssh import \
    Connection as ParamikoConnection
import openziti

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.paramiko
      - community.openziti.openziti
      - community.openziti.anzible
    '''


class Connection(ParamikoConnection):
    '''OpenZiti based connection wrapper for paramiko_ssh'''
    # pylint: disable=import-outside-toplevel

    transport = 'community.openziti.paramiko'

    def _connect(self):
        '''Wrap connection activation object with OpenZiti'''

        log_level = self.get_option('ziti_log_level')
        if os.getenv('ZITI_LOG') is None:
            os.environ['ZITI_LOG'] = str(log_level)
        identities = self.get_option('ziti_identities')
        for identity in identities:
            openziti.load(identity)

        with openziti.monkeypatch():
            super()._connect()
