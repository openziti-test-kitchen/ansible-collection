# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti paramiko connection plugin wrapper"""
from __future__ import (absolute_import, annotations, division, print_function)

import socket
from typing import Dict, Optional

import openziti
from openziti.context import ZitiContext
from ansible.plugins.connection.paramiko_ssh import \
    Connection as ParamikoConnection
from ansible.plugins.connection.paramiko_ssh import paramiko
from ansible.utils.display import Display
# pylint: disable=import-error, no-name-in-module
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


def get_ziti_ssh_client_with_context(cfg: Optional[Dict[str, str]] = None) -> object:
    """
    Closure around paramiko.SSHClient

    :param cfg:
        Dictionary with openziti connection variables.
        See the ziti_connection_dial_service suboptions for details.
    :returns: ZitiSSHClient class
    """

    class ZitiSSHClient(paramiko.SSHClient):
        # pylint: disable=too-few-public-methods
        """OpenZiti paramiko.SSHClient wrapper"""
        def __init__(self) -> None:
            self._cfg = cfg
            self._ztx: Optional[ZitiContext] = None
            self._sock: Optional[socket.socket] = None
            self._sockfd: Optional[int] = None
            if self._cfg is not None:
                self._ztx = openziti.load(self._cfg['ziti_connection_identity_file'])
                service = self._cfg['ziti_connection_service']
                terminator = self._cfg.get('ziti_connection_service_terminator')
                display.vvv(f"OPENZITI DIALING SERVICE: {terminator}@{service}")

                self._sock = self._ztx.connect(service, terminator=terminator)
                self._sockfd = self._sock.fileno()
            super().__init__()

        def connect(self, *args, **kwargs) -> None:
            """paramiko.SSHClient.connect wrapper"""
            if self._sock is None:
                self._sock = openziti.socket(type=socket.SOCK_STREAM)
                self._sock.connect((kwargs['host'], kwargs['port']))
                self._sockfd = self._sock.fileno()
            kwargs.update({"sock": self._sock})
            display.vvv(f"OPENZITI TUNNELED CONNECTION via fd={self._sockfd}")
            super().connect(*args, **kwargs)

    return ZitiSSHClient


class Connection(ParamikoConnection, ConnectionMixin):
    '''OpenZiti based connection wrapper for paramiko_ssh'''
    # pylint: disable=access-member-before-definition
    # pylint: disable=attribute-defined-outside-init

    transport = 'community.openziti.paramiko'

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''

        if self.ziti_log_level < 0:
            self.ziti_log_level = self.get_option('ziti_log_level')

        if not self.ziti_identities:
            self.ziti_dial_service_cfg = self.get_option(
                    'ziti_connection_dial_service')

        if self.ziti_dial_service_cfg is not None:
            # We lie to Ansible, because we're gonna dial
            # by addressable terminator
            self.set_option('host_key_checking', False)
            self.set_option('remote_addr', '127.0.0.1')

        if not self.ziti_identities:
            self.ziti_identities = self.get_option('ziti_identities')

        paramiko.SSHClient = get_ziti_ssh_client_with_context(
                cfg=self.ziti_dial_service_cfg)
        super()._connect()
