# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti pylibssh connection plugin wrapper"""
from __future__ import absolute_import, annotations, division, print_function

# pylint: disable=import-error, no-name-in-module
# pylint: disable=too-few-public-methods

import ansible_collections.ansible.netcommon.plugins.connection.libssh \
    as PyLibSSH
from ansible.utils.display import Display
from ansible_collections.community.openziti.plugins.plugin_utils._mixins \
    import ConnectionMixin, SSHMixin

display = Display()


DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.libssh
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
            """pylibssh.session.Session impl"""
            # pylint: disable=attribute-defined-outside-init

            def set_dial_cfg(self) -> None:
                """Set dial_cfg"""
                self.dial_cfg = cfg

            def connect(self, **kwargs) -> None:
                """libssh patched connect"""
                self._connect((kwargs['host'], kwargs['port']))

                self.set_ssh_options('fd', self._sockfd)

                super().connect(**kwargs)

        setattr(self.module, self.class_name, ZitiClient)

    def __exit__(self, exc_type, exc_value, traceback):
        setattr(self.module, self.class_name, self.original_class)


class Connection(PyLibSSH.Connection, ConnectionMixin):
    '''OpenZiti based connection wrapper for libssh'''

    transport = 'community.openziti.libssh'

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        self.init_options()

        with PatchedClient(PyLibSSH, 'Session', self.ziti_dial_service_cfg):
            super()._connect()
