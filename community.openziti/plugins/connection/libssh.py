# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti pylibssh connection plugin wrapper"""
from __future__ import (absolute_import, annotations, division, print_function)

from typing import Dict, Optional

import socket

import ansible_collections.ansible.netcommon.plugins.connection.libssh as PyLibSSH
import openziti
from openziti.context import ZitiContext
from ansible.utils.display import Display
from ansible_collections.community.openziti.plugins.plugin_utils._mixins \
    import ConnectionMixin

display = Display()

# pylint: disable=too-few-public-methods

DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.libssh
      - community.openziti.openziti
      - community.openziti.openziti_connection
      - community.openziti.openziti_connection_dial_service
    '''


def get_ziti_ssh_session_with_context(cfg: Optional[Dict[str, str]]) -> object:
    """
    Closure around pylibss.Session

    :param cfg:
        Dictionary with openziti connection variables.
        See the ziti_connection_dial_service suboptions for details.
    :returns: ZitiSession class
    """

    class ZitiSession(PyLibSSH.Session):
        """OpenZiti pylibssh.Session Wrapper"""
        def __init__(self, *args, **kwargs) -> None:
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
            super().__init__(*args, **kwargs)

        def connect(self, **kwargs) -> None:
            """PyLibSSH.Session.connect wrapper"""
            if self._sock is None:
                self._sock = openziti.socket(type=socket.SOCK_STREAM)
                self._sock.connect((kwargs['host'], kwargs['port']))
                self._sockfd = self._sock.fileno()

            self.set_ssh_options('fd', self._sockfd)
            display.vvv(f"OPENZITI TUNNELED CONNECTION via fd={self._sockfd}",
                        host=kwargs['host'])
            super().connect(**kwargs)
    return ZitiSession


class Connection(PyLibSSH.Connection, ConnectionMixin):
    '''OpenZiti based connection wrapper for libssh'''
    # pylint: disable=access-member-before-definition
    # pylint: disable=attribute-defined-outside-init

    transport = 'community.openziti.libssh'

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        self.init_options()

        PyLibSSH.Session = get_ziti_ssh_session_with_context(
                self.ziti_dial_service_cfg)

        super()._connect()
