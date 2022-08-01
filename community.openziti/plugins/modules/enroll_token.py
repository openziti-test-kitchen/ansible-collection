"""TODO"""
#!/usr/bin/env python

# Copyright: (c) 2022, Steven Broderick <steven.broderick@netfoundry.io>
from __future__ import absolute_import, division, print_function

import os
import json
from pathlib import Path

import jwt
from ansible.module_utils.basic import AnsibleModule
from openziti import enroll
# from platformdirs import user_config_dir

# pylint: disable=invalid-name
__metaclass__ = type

DOCUMENTATION = r'''
---
module: enroll_token

short_description: Enroll ziti JWT token

version_added: "1.0.0"

description: Enrolls ziti JWT token; generates ziti identity file.

options:
    token_file:
        description: Location of the JWT token file to enroll.
        required: true
        type: path
    identity_file:
        description: Path of generated identity file.
        required: true
        type: path
    backup:
        description: Save token after enrollment.
        required: false
        type: bool
    replace:
        description: Force re-enrollment. Overwrites identity file.
        required: false
        type: bool

extends_documentation_fragment:
    - community.openziti.ziti_log

author:
    - Steven A. Broderick Elias(@sabedevops)
'''

EXAMPLES = r'''
- name: Enroll JWT token
  community.openziti.ziti_enroll:
    token_file: /path/to/my_token.jwt
    identity_file: /path/to/identity.json
'''

RETURN = r'''
token_payload:
    description: The JWT token payload.
    type: dict
    returned: changed
identity_info:
    description: The contents of the identity json.
    type: dict
    returned: always
'''


def run_module():
    """TODO"""
    module_args = dict(
        token_file=dict(type='path', required=True),
        identity_file=dict(type='path', required=True),
        backup=dict(type='bool', required=False, default=False),
        replace=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
        token_payload={},
        identity_info={}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    token_file = module.params['token_file']
    token_p = Path(token_file)
    identity_file = module.params['identity_file']
    identity_p = Path(identity_file)

    if not os.access(identity_p.parent, os.W_OK):
        module.fail_json(msg=f"{identity_p.parent} is not writable", **result)

    try:
        token = token_p.read_text(encoding='utf-8')
    except OSError as err:
        module.fail_json(msg=f"Error reading token_file: {err}", **result)

    try:
        result['token_payload'] = jwt.decode(
                token,
                algorithsms=[jwt.get_unverified_header(token)['alg']],
                options={"verify_signature": False}
            )
    except Exception as err:  # pylint: disable=broad-except
        module.fail_json(msg=f"Could not decode JWT token: {err}", **result)

    if not module.params['replace']:
        if module.check_file_absent_if_check_mode(identity_p):
            module.exit_json(**result)
    elif identity_p.is_file():
        module.exit_json(**result)
    else:
        module.log(f'Re-enrolling. Replacing {identity_p}.')

    if os.getenv('ZITI_LOG') is None:
        os.environ['ZITI_LOG'] = str(module.params['ziti_log_level'])

    try:
        id_json = enroll(token)
    except RuntimeError as err:
        module.fail_json(msg=f"Error invoking zitilib.enroll: {err}", **result)
    else:

        try:
            id_dict = json.loads(id_json)
            result['identity_info']['ztAPI'] = id_dict['ztAPI']

        except json.decoder.JSONDecodeError as err:
            module.fail_json(msg=f"Could not load id_json: {err}", **result)
        except KeyError as err:
            module.fail_json(msg=f"Unexpected schema for id_json: {err}",
                             **result)

        try:
            identity_p.write_bytes(bytes(id_json, 'utf-8'))
        except OSError as err:
            module.fail_json(
                    msg=f"Could not write {identity_file}: {err}",
                    **result
                )
        else:
            result['changed'] = True

    if module.params['backup']:
        target = Path(token_file + '.bak')
        module.atomic_move(token_p, target)
        result['backup_file'] = str(target)
    else:
        token_p.unlink()

    module.exit_json(**result)


def main():
    """TODO"""
    run_module()


if __name__ == '__main__':
    main()
