"""OpenZiti paramiko connection plugin wrapper"""
import os

import openziti
from ansible.plugins.connection.paramiko_ssh import \
    Connection as ParamikoConnection

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.paramiko
      - community.openziti.paramikoz
      - community.openziti.ziti
    '''


class Connection(ParamikoConnection):
    '''Ziti based connection wrapper for paramiko_ssh'''
    # pylint: disable=import-outside-toplevel

    transport = 'paramikoz'

    def _connect(self):
        '''Wrap connection activation object with ziti'''

        self.log_level = self.get_option('ziti_log_level')
        if os.getenv('ZITI_LOG') is None:
            os.environ['ZITI_LOG'] = str(self.log_level)
        self.identities = self.get_option('ziti_identities')
        for identity in self.identities:
            openziti.load(identity)

        with openziti.monkeypatch():
            super()._connect()
