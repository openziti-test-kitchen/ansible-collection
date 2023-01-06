# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti connection dial service doc_fragment plugin"""


class ModuleDocFragment():
    """OpenZiti Connection Dial Service Plugin Documentation"""
    # pylint: disable=too-few-public-methods
    DOCUMENTATION = '''
    options:
      ziti_connection_dial_service:
        description: |
            Dial ziti service directly by name.
            Can specify terminator identity to
            dial specific service terminator.
        vars:
          - name: ziti_connection_dial_service
        default: null
        required: false
        type: dict
        suboptions:
          ziti_connection_identity_file:
            description: Identity file to load for the connection.
            type: path
            required: true
          ziti_connection_service:
            description: Specific service name to connect to.
            type: str
            required: true
          ziti_connection_service_terminator:
            description: Specific terminator identity to connect to.
            type: str
            required: false
    '''
