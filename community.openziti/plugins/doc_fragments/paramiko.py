# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""Paramiko connection documentaiton as doc_fragment"""

from ansible.plugins.connection.paramiko_ssh import \
    DOCUMENTATION as PARAMIKO_DOCUMENTATION


class ModuleDocFragment():
    """Base Paramiko Documentation"""
    # pylint: disable=too-few-public-methods
    DOCUMENTATION = PARAMIKO_DOCUMENTATION
