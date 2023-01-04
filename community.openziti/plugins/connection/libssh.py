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
    import (ConnectionMixin, SSHMixin)

display = Display()


DOCUMENTATION = '''
    extends_documentation_fragment:
      - community.openziti.libssh
      - community.openziti.openziti
      - community.openziti.openziti_connection
      - community.openziti.openziti_connection_dial_service
    '''


def get_ziti_client(cfg) -> object:
    """Closure around the ZitiSession class"""
    class ZitiSSHSession(SSHMixin, PyLibSSH.Session):
        """pylibssh.session.Session impl"""
        # pylint: disable=attribute-defined-outside-init

        def set_dial_cfg(self):
            """Set dial_cfg"""
            self.dial_cfg = cfg

        def set_sockfd(self) -> None:
            """Set sockopt for sockfd"""
            self.set_ssh_options('fd', self._sockfd)

    return ZitiSSHSession


class Connection(PyLibSSH.Connection, ConnectionMixin):
    '''OpenZiti based connection wrapper for libssh'''

    transport = 'community.openziti.libssh'

    def _get_client_with_context(self):
        ziti_client = get_ziti_client(self.ziti_dial_service_cfg)
        PyLibSSH.Session = ziti_client
        return ziti_client

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        self.init_options()
        super()._connect()
