"""OpenZiti paramiko connection plugin wrapper"""
import os

import openziti
from ansible_collections.ansible.netcommon.plugins.connection.libssh import \
        Connection as LibSSHConnection

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.libssh
      - community.openziti.ziti
'''


class Connection(LibSSHConnection):
    '''Ziti based connection wrapper for libssh'''
    # pylint: disable=import-outside-toplevel

    transport = 'libsshz'

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
