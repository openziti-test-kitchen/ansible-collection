# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti doc_fragment plugin"""


class ModuleDocFragment():
    """OpenZiti Documentation"""
    # pylint: disable=too-few-public-methods
    DOCUMENTATION = '''
    options:
      ziti_log_level:
        description: verbosity of ziti library
        default: 0
        env:
          - name: ANSIBLE_ZITI_LOG_LEVEL
        ini:
          - section: openziti
            key: ziti_log_level
          - section: openziti_connection
            key: ziti_log_level
        vars:
          - name: ziti_log_level
        required: false
        type: int
    '''
