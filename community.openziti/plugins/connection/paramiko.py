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
from ansible_collections.community.openziti.plugins.plugin_utils._decorators \
    import zitify_client
from ansible_collections.community.openziti.plugins.plugin_utils._mixins \
    import ConnectionMixin

display = Display()

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.paramiko
      - community.openziti.openziti
      - community.openziti.openziti_connection
      - community.openziti.openziti_connection_dial_service
    '''


def get_client_with_context(cfg: Optional[Dict[str, str]] = None) -> object:
    """
    Closure around paramiko.SSHClient

    :param cfg:
        Dictionary with openziti connection variables.
        See the ziti_connection_dial_service suboptions for details.
    :returns: ZitiSSHClient class
    """
    @zitify_client(cfg)
    class ZitiSSHClient(paramiko.SSHClient):
        # pylint: disable=too-few-public-methods
        """OpenZiti paramiko.SSHClient wrapper"""

        def connect(self, *args, **kwargs) -> None:
            """paramiko.SSHClient.connect wrapper"""
            kwargs.update({"sock": self._sock})
            super().connect(*args, **kwargs)

    return ZitiSSHClient


class Connection(ParamikoConnection, ConnectionMixin):
    '''OpenZiti based connection wrapper for paramiko_ssh'''

    transport = 'community.openziti.paramiko'

    def _get_client_with_context(self):
        paramiko.SSHClient = get_client_with_context(
                cfg=self.ziti_dial_service_cfg)

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        self.init_options()
        super()._connect()
