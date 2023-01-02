# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti pylibssh connection plugin wrapper"""
from __future__ import (absolute_import, annotations, division, print_function)

from typing import Dict, Optional

import ansible_collections.ansible.netcommon.plugins.connection.libssh as PyLibSSH
import openziti
from ansible.utils.display import Display
from ansible_collections.community.openziti.plugins.plugin_utils._decorators \
    import zitify_client
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


def get_client_with_context(cfg: Optional[Dict[str, str]]) -> object:
    """
    Closure around pylibss.Session

    :param cfg:
        Dictionary with openziti connection variables.
        See the ziti_connection_dial_service suboptions for details.
    :returns: ZitiSession class
    """
    @zitify_client(cfg)
    class ZitiSession(PyLibSSH.Session):
        """OpenZiti pylibssh.Session Wrapper"""

        def connect(self, **kwargs) -> None:
            """PyLibSSH.Session.connect wrapper"""
            self.set_ssh_options('fd', self._sockfd)
            super().connect(**kwargs)
    return ZitiSession


class Connection(PyLibSSH.Connection, ConnectionMixin):
    '''OpenZiti based connection wrapper for libssh'''
    # pylint: disable=access-member-before-definition
    # pylint: disable=attribute-defined-outside-init

    transport = 'community.openziti.libssh'

    def _get_client_with_context(self):
        PyLibSSH.Session = get_client_with_context(
                cfg=self.ziti_dial_service_cfg)

    def _connect(self) -> None:
        '''Wrap connection activation object with OpenZiti'''
        self.init_options()
        super()._connect()
