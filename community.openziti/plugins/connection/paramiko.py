# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti paramiko connection plugin wrapper"""
from __future__ import absolute_import, annotations, division, print_function

# pylint: disable=import-error, no-name-in-module
# pylint: disable=too-few-public-methods

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


class PatchedClient:
    """Context manager for Ziti SSH Client"""
    def __init__(self, module, class_name: str, cfg: dict):
        self.module = module
        self.class_name = class_name
        self.dial_cfg = cfg
        self.original_class = getattr(module, class_name)

    def __enter__(self):
        cfg = self.dial_cfg

        class ZitiClient(SSHMixin, self.original_class):
            """paramiko.SSHClient impl"""
            # pylint: disable=attribute-defined-outside-init

            def set_dial_cfg(self) -> None:
                """Set dial_cfg"""
                self.dial_cfg = cfg

            def connect(self, host, **kwargs) -> None:
                """paramiko patched connect"""
                self._connect((host, kwargs['port']))

                kwargs.update({"sock": self._sock})

                super().connect(host, **kwargs)

        setattr(self.module, self.class_name, ZitiClient)

    def __exit__(self, exc_type, exc_value, traceback):
        setattr(self.module, self.class_name, self.original_class)


class Connection(ParamikoConnection, ConnectionMixin):
    '''OpenZiti based connection wrapper for paramiko_ssh'''

    transport = 'community.openziti.paramiko'

    # This gets called multiple times
    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        self.init_options()

        with PatchedClient(paramiko, 'SSHClient', self.ziti_dial_service_cfg):
            super()._connect()
