"""TODO"""


class ModuleDocFragment():
    """Ziti Log Documentation"""
    # pylint: disable=too-few-public-methods
    DOCUMENTATION = '''
    options:
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
        type: integer
    '''
