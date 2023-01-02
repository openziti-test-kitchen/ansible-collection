# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""Decorators for OpenZiti integration"""

import functools
import socket
from typing import Dict, Optional, no_type_check

import openziti
from ansible.utils.display import Display
from openziti.context import ZitiContext

display = Display()


@no_type_check
def zitify_client(cfg: Dict):
    """Common functionality wrapper for SSH Client classes"""
    # pylint: disable=protected-access
    def cls_decorator(cls):
        cls_init = cls.__init__
        cls_connect = cls.connect

        @functools.wraps(cls_init)
        def zitified_init(self, *args, **kwargs):
            self._cfg: Dict = cfg
            self._ztx: Optional[ZitiContext] = None
            self._service: Optional[str] = None
            self._terminator: Optional[str] = None

            if self._cfg is not None:
                self._ztx = openziti.load(
                        self._cfg['ziti_connection_identity_file'])
                self._service = self._cfg['ziti_connection_service']
                self._terminator = self._cfg.get(
                        'ziti_connection_service_terminator')
                display.vvv(
                    "OPENZITI DIALING SERVICE: "
                    f"{self._terminator}@{self._service}")

                self._sock = self._ztx.connect(
                        self._service, terminator=self._terminator)
            else:
                self._sock = openziti.socket(type=socket.SOCK_STREAM)
            self._sockfd = self._sock.fileno()
            display.vvv(f"OPENZITI TUNNELED CONNECTION via fd={self._sockfd}")
            return cls_init(self, *args, **kwargs)

        @functools.wraps(cls_connect)
        def zitified_connect(self, *args, **kwargs):
            if self._service is None:
                self._sock.connect((kwargs['host'], kwargs['port']))
            return cls_connect(self, *args, **kwargs)

        cls.__init__ = zitified_init
        cls.connect = zitified_connect

        return cls
    return cls_decorator
