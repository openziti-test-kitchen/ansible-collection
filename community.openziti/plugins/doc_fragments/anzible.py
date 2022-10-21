# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""AnZible doc_fragment plugin"""


class ModuleDocFragment():
    """AnZible Documentation"""
    # pylint: disable=too-few-public-methods
    DOCUMENTATION = '''
    options:
      ziti_identities:
        description: ziti identities to use for connection
        default: null
        env:
          - name: ANSIBLE_ZITI_IDENTITIES
        ini:
          - section: anzible_connection
            key: ziti_identities
        vars:
          - name: ziti_identities
        required: true
        type: pathlist
    '''
