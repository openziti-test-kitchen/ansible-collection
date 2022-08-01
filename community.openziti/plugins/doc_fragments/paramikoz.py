"""TODO"""


class ModuleDocFragment():
    """Paramikoz Documentation"""
    # pylint: disable=too-few-public-methods
    DOCUMENTATION = '''
    options:
      ziti_identities:
        description: ziti identities to use for connection
        default: null
        env:
          - name: ANSIBLE_ZITI_IDENTITIES
        ini:
          - section: paramikoz_connection
            key: ziti_identities
        vars:
          - name: ziti_identities
        required: true
        type: pathlist

      ziti_log_level:
        description: verbosity of ziti library
        default: 0
        env:
          - name: ANSIBLE_ZITI_LOG_LEVEL
        ini:
          - section: paramikoz_connection
            key: ziti_log_level
        vars:
          - name: ziti_log_level
        required: false
        type: int
    '''
