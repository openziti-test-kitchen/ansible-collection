#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: NetFoundry Inc.
# Apache License, Version 2 (see http://www.apache.org/licenses/LICENSE-2.0)
"""OpenZiti JWT token enrollment Ansible module."""

from __future__ import absolute_import, division, print_function

import json
import os
from pathlib import Path
from typing import Any, Dict

import jwt
from ansible.module_utils.basic import AnsibleModule
from openziti import enroll

__metaclass__ = type  # pylint: disable=invalid-name

DOCUMENTATION = r'''
---
module: enroll_token

short_description: Enroll ziti JWT token

version_added: "0.1.0"

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
        default: false
    replace:
        description: Re-enroll token, overriding identity file.

extends_documentation_fragment:
    - community.openziti.openziti

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


def run_module() -> None:
    # pylint: disable=too-many-statements, too-many-branches
    """Enrolls JWT token."""
    module_args = dict(
        token_file=dict(type='path', required=True),
        identity_file=dict(type='path', required=True),
        backup=dict(type='bool', required=False, default=False),
        replace=dict(type='bool', required=False, default=False),
        ziti_log_level=dict(type='int', required=False, default=0)
    )

    result: Dict[str, Any] = dict(
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

    if identity_p.is_file():
        id_dict = json.loads(identity_p.read_bytes())
        result['identity_info']['ztAPI'] = id_dict['ztAPI']

        if not module.params['replace']:
            module.exit_json(**result)

    if module.check_mode and module.params['replace']:
        result['changed'] = True
        module.exit_json(**result)

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
    except jwt.exceptions.PyJWTError as err:
        module.fail_json(msg=f"Could not decode JWT token: {err}", **result)

    if module.check_file_absent_if_check_mode(identity_p):
        result['changed'] = True
        module.exit_json(**result)

    if os.getenv('ZITI_LOG') is None:
        os.environ['ZITI_LOG'] = str(module.params['ziti_log_level'])

    try:
        id_json = enroll(token)
    except RuntimeError as err:
        module.fail_json(msg=f"Error invoking zitilib.enroll: {err}", **result)

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


def main() -> None:
    """Execution wrapper around run_module"""
    run_module()


if __name__ == '__main__':
    main()
