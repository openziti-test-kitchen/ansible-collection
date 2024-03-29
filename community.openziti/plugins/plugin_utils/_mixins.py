# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti Ansible Collection Mixins"""
import os
import socket
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional

import openziti
from ansible.errors import AnsibleRuntimeError
from ansible.plugins.connection import ConnectionBase
from ansible.utils.display import Display
from openziti.context import ZitiContext

display = Display()


class ConnectionMixin(ConnectionBase, metaclass=ABCMeta):
    """OpenZiti Connection class wrapper"""

    def __init__(self, *args, **kwargs) -> None:
        self._ziti_identities: List[str] = []
        self._ziti_log_level = int(os.getenv('ZITI_LOG', '-1'))
        self._ziti_dial_service_cfg: Optional[Dict[str, str]] = None
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

    @property
    def ziti_dial_service_cfg(self) -> Optional[Dict[str, str]]:
        "Returns dial service configuration"
        return self._ziti_dial_service_cfg

    @ziti_dial_service_cfg.setter
    def ziti_dial_service_cfg(self, cfg: Optional[Dict[str, str]]) -> None:
        "Loads dial service configuration"
        if cfg is not None:
            self.ziti_identities = [cfg['ziti_connection_identity_file']]
            self._ziti_dial_service_cfg = cfg
            display.vvv(f"OPENZITI SET DIAL SERVICE CONFIGURATION: {cfg}",
                        host=self.get_option('remote_addr'))

    def init_options(self) -> None:
        """Helper to initialize _connect() method options"""
        if self.ziti_log_level < 0:
            self.ziti_log_level = self.get_option('ziti_log_level')

        if not self.ziti_identities:
            self.ziti_dial_service_cfg = self.get_option(
                    'ziti_connection_dial_service')

        if self.ziti_dial_service_cfg is not None:
            # We lie to Ansible, because we're gonna dial
            # by addressable terminator
            self.set_option('host_key_checking', False)
            self.set_option('remote_addr', '0.0.0.1')
            self.set_option('remote_port', 0)

        if not self.ziti_identities:
            self.ziti_identities = self.get_option('ziti_identities')

    @abstractmethod
    def _connect(self) -> None:
        """Connection class _connect() wrapper impl"""


class SSHMixin:
    """SSH client mixin"""
    def __init__(self, *args, **kwargs) -> None:
        self.set_dial_cfg()
        self._identity: Optional[str] = None
        self._ztx: Optional[ZitiContext] = None
        self._service: Optional[str] = None
        self._terminator: Optional[str] = None

        if self._dial_cfg is not None:
            self._identity = self._dial_cfg['ziti_connection_identity_file']
            display.vvv(f"OPENZITI CLIENT LOAD IDENTITY: {self._identity}")
            self._ztx = openziti.load(self._identity)
            self._service = self._dial_cfg['ziti_connection_service']
            self._terminator = self._dial_cfg.get(
                    'ziti_connection_service_terminator')
        else:
            self._sock = openziti.socket(type=socket.SOCK_STREAM)

        super().__init__(*args, **kwargs)

    def _connect(self, addr: tuple[str, int]) -> None:
        if self._ztx is not None:
            display.vvv("OPENZITI DIALING SERVICE: "
                        f"{self._terminator}@{self._service}")
            self._sock = self._ztx.connect(
                    self._service, terminator=self._terminator)
        else:
            display.vvv(f"OPENZITI DIALING INTERCEPT: {addr[0]}:{addr[1]}")
            self._sock.connect((addr[0], addr[1]))

        self._sockfd = self._sock.fileno()
        display.vvv(f"OPENZITI TUNNELED CONNECTION via fd={self._sockfd}")

    @property
    def dial_cfg(self) -> Optional[Dict]:
        """Return dial_cfg"""
        return self._dial_cfg

    @dial_cfg.setter
    def dial_cfg(self, dial_cfg: Optional[Dict] = None):
        self._dial_cfg = dial_cfg

    @abstractmethod
    def set_dial_cfg(self, cfg: Optional[Dict] = None) -> None:
        """Sets config from closure"""
