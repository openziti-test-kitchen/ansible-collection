# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti paramiko connection plugin wrapper"""
from __future__ import absolute_import, annotations, division, print_function

# pylint: disable=import-error, no-name-in-module
from typing import Dict, Optional

import openziti
from ansible.plugins.connection.paramiko_ssh import \
    Connection as ParamikoConnection
from ansible.plugins.connection.paramiko_ssh import paramiko
from ansible.utils.display import Display
from ansible_collections.community.openziti.plugins.plugin_utils._mixins \
    import ConnectionMixin, SSHMixin

display = Display()

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.paramiko
      - community.openziti.openziti
      - community.openziti.openziti_connection
      - community.openziti.openziti_connection_dial_service
    '''


def get_ziti_client(cfg) -> object:
    """
    Closure around paramiko.SSHClient
    """
    class ZitiSSHClient(SSHMixin, paramiko.SSHClient):
        # pylint: disable=too-few-public-methods
        """OpenZiti paramiko.SSHClient wrapper"""

        def set_dial_cfg(self):
            """Set dial_cfg"""
            self.dial_cfg = cfg

        def set_sockfd(self) -> dict:
            """Set sockopt for sockfd"""
            return {"sock": self._sock}

    return ZitiSSHClient


class Connection(ParamikoConnection, ConnectionMixin):
    '''OpenZiti based connection wrapper for paramiko_ssh'''

    transport = 'community.openziti.paramiko'

    def _get_client_with_context(self):
        ziti_client = get_ziti_client(self.ziti_dial_service_cfg)
        paramiko.SSHClient = ziti_client
        return ziti_client

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        self.init_options()
        super()._connect()
