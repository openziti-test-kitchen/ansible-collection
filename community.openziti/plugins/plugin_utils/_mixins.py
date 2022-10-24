# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti Ansible Collection Mixins"""
import os
from abc import ABCMeta, abstractmethod
from typing import List

import openziti
from ansible.plugins.connection import ConnectionBase
from ansible.utils.display import Display

display = Display()


class ConnectionMixin(ConnectionBase, metaclass=ABCMeta):
    """OpenZiti Connection class wrapper"""

    def __init__(self, *args, **kwargs) -> None:
        self._ziti_identities: List[str] = []
        self._ziti_log_level = int(os.getenv('ZITI_LOG', '-1'))
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

    @abstractmethod
    def _connect(self) -> None:
        """Connection class _connect() wrapper impl"""
