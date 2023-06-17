# -*- coding: utf-8 -*-

# (c) 2023, Arslane BAHLEL <arslane.bahlel+openziti@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: openziti_pki
author:
    - "Arslane BAHLEL"
version: 0.1.0
short_description: Manage PKI for OpenZiti through OpenZiti CLI
description:
    - Create Certificate Authority 
    - Create self signed Root certificates
    - Create self signed Intermediate certificates
    - Create self signed client/server certificates
options:
    state:
        description:
            - Indicates the desired PKI component state.
        type: str
        default: present
        choices: [ absent, present ]
    component:
        description:
            - Indicates the PKI component.
        type: str
        default: ca
        choices: [ ca, intermediate, client, server, csr, key ]
    ziti_cli_path:
        description
            - Corresponds to the path to the `ziti cli` binaries
            - If not specified, the modules will try to infer it from the `ziti` command
        type: str
        required: false
    ca_name:
        description:
            - Name of the Certificate Authority
            - Required if component in [ ca, intermediate, client, server, key ]
        type: str
        required: false
    component_file:
        description:
            - Name of the file
            - Corresponds to `--ca-file` for certificate authority
            - Corresponds to `--intermediate-file` for intermediate certificates
            - Corresponds to `--client-file` for client certificates
            - Corresponds to `--server-file` for server certificates
            - Corresponds to `--csr-file` for client certificate signing requests
            - Corresponds to `--key-file` for private keys
        type: str
        required: true
    
'''

RETURN = '''
'''
from typing import List

from ansible_collections.community.openziti.plugins.module_utils.openziti_cli import OpenZiti

ARGUMENT_SPEC = dict(
    state=dict(choices=['present', 'absent'], default='present'),
    component=dict(choices=['ca', 'intermediate', 'client', 'server', "csr", "key"], default='ca'),
    ziti_cli_path=dict(type='str', default=None),
    ca_name=dict(type='str'),
    component_file=dict(
        type='str',
        default=None,
        aliases=["ca-file", "intermediate_file", "client_file", "server_file", "csr_file", "key_file"]
    ),
    component_name=dict(
        type='str',
        default=None,
        aliases=["intermediate_name", "client_name", "server_name", "csr_name"]
    ),
    key_file=dict(type='str', default=None),
    key_name=dict(type='str', default=None),
    email=dict(type='str', default=None),
    dns=dict(type='str', default=None),
    ip=dict(type='str', default=None),
    pki_path=dict(required=True, type='str', aliases=["pki_root"]),
    max_path_len=dict(type='int', default=-1),
    private_key_size=dict(type='int', default=None),
    expire_limit=dict(type='int', default=None),
    country=dict(default='US', type='str'),
    locality=dict(default='Charlotte', type='str'),
    organization=dict(default='NetFroundry', type='str'),
    organizational_unit=dict(default='ADV-DEV', type='str'),
    province=dict(default='NC', type='str'),
    spiffe_id=dict(type='str', default=None),
    trust_domain=dict(type='str', default=None)
)

REQUIRED_IF = [
    ("state", "present", ["pki_path", "component"]),
    ('component', 'client', ["key_file", "email"]),
    ('component', 'server', ["key_file", "ip", "dns"]),
    ('component', 'key', ["ca_name"]),
    ('component', "crs", ["key_name"])
]

SUPPORTS_CHECK_MODE = True

def ca_specific_params(module):

    command = [
        "--ca-name", module.params.get('ca_name') or "NetFoundry Inc. Certificate Authority",
        "--ca-file", module.params.get('component_file'),
        "--private-key-size", module.params.get('private_key_size') or 4096,
        "--expire-limit", module.params.get('expire_limit') or 3650,
        "--max-path-len", module.params.get('max_path_len')
    ]

    if "trust_domain" in module.params.keys():
        command = command + ["--trust-domain", module.params.get('trust_domain')]
    
    return command

def intermediate_specific_params(module):

    return [
        "--ca-name", module.params.get('ca_name') or "ca",
        "--intermediate-file", module.params.get('component_file') or "intermediate",
        "--intermediate-name", module.params.get('component_name') or "NetFoundry Inc. Intermediate CA",
        "--private-key-size", module.params.get('private_key_size') or 4096,
        "--expire-limit", module.params.get('expire_limit') or 3650,
        "--max-path-len", module.params.get('max_path_len'),
    ]

def client_specific_params(module):

    command =  [
        "--ca-name", module.params.get('ca_name') or "intermediate",
        "--client-file", module.params.get('component_file') or "client",
        "--client-name", module.params.get('component_name') or "NetFoundry Inc. Client",
        "--private-key-size", module.params.get('private_key_size') or 2048,
        "--expire-limit", module.params.get('expire_limit') or 365,
        "--key-file", module.params.get('key_file'),
        "--email", module.params.get('email'),
        "--max-path-len", module.params.get('max_path_len'),
    ]

    if "spiffe_id" in module.params.keys():
        command = command + ["--spiffe-id", module.params.get("spiffe_id")]
    
    return command

def server_specific_params(module):

    command = [
        "--ca-name", module.params.get('ca_name') or "intermediate",
        "--dns", module.params.get('dns'),
        "--expire-limit", module.params.get('expire_limit') or 365,
        "--ip", module.params.get('ip'),
        "--key-file", module.params.get('key_file'),
        "--max-path-len", module.params.get('max_path_len'),
        "--private-key-size", module.params.get('private_key_size') or 4096,
        "--server-file", module.params.get("server_file") or "server",
        "--server-name", module.params.get("server_name") or "NetFoundry Inc. Server",
    ]

    if "spiffe_id" in module.params.keys():
        command = command + ["--spiffe-id", module.params.get("spiffe_id")]
    
    return command

def csr_specific_params(module):
    return [
        "--csr-file", module.params.get('component_file') or "csr",
        "--csr-name", module.params.get('component_name') or "NetFoundry Inc. CSR",
        "--expire-limit", module.params.get('expire_limit') or 365,
        "--key-name", module.params.get('key_name'),
        "--private-key-size", module.params.get('private_key_size') or 4096,
        "--max-path-len", module.params.get('max_path_len'),
    ]

def key_specific_params(module):
    return [
        "--ca-name", module.params.get('ca_name') or "intermediate",
        "--key-file", module.params.get('expire_limit') or "key",
        "--private-key-size", module.params.get('private_key_size') or 4096,
    ]

def pki_build_args(module):
    pki_args = None
    
    if module.params.get("component") == "ca":
        pki_args = ca_specific_params(module)
    elif module.params.get("component") == "intermediate":
        pki_args = intermediate_specific_params(module)
    elif module.params.get("component") == "client":
        pki_args = client_specific_params(module)
    elif module.params.get("component") == "server":
        pki_args = server_specific_params(module)
    elif module.params.get("component") == "csr":
        pki_args = csr_specific_params(module)
    elif module.params.get("component") == "key":
        pki_args = key_specific_params(module)
    else:
        raise ValueError("Parameter `component` needs to be in [ca, intermediate, client, server, key, csr]")
    
    return module.ziti + [
        "pki", "create", module.params.get('component', 'ca'),
        "--pki-country", module.params.get('country'),
        "--pki-locality", module.params.get('locality'),
        "--pki-province",module.params.get('province'),
        "--pki-organization", module.params.get('organization'),
        "--pki-organizational-unit", module.params.get('organizational_unit'),
        "--pki-root",module.params.get('pki_path')
    ] + pki_args

def ziti_pki(module):
    from os import path, makedirs
    from shutil import rmtree

    component_path = path.join(
        module.params.get("pki_path"),
        module.params.get("component_file")
    )

    if module.params.get("state") == "absent":
        if path.isdir(component_path):
            rmtree(component_path)
            return {
                "changed": True,
                "msg": f"Deleted {component_path}",
                "diff": {
                    "before": component_path,
                    "after": None
                }
            }
        return {
            "changed": False,
            "msg": f"{component_path} doesn't exist.",
            "diff": {
                "before": None,
                "after": None
            }
        }

    if not module.check_mode:
        if not path.isdir(module.params['pki_path']):
            makedirs(module.params['pki_path'])

        command = pki_build_args(module)

        return_code, std_out, std_err = module.run_command(command)
    else:
        return_code = path.isdir(component_path)
        std_out = "Success\n"
        std_err = "error: cannot sign: failed saving generated bundle: "\
        "a bundle already exists for the name {component_name} within CA {ca_name}".format(
            component_name=module.params.get("component_name") or module.params.get("ca_name"),
            ca_name=module.params.get("ca_name")
        )

    
    changed = not return_code

    return {
        "changed": changed,
        "msg": std_out if changed else std_err,
        "diff": {
            "before": None if changed else component_path,
            "after": component_path if changed else component_path
        }
    }

def run_module(ziti_cli):
    
    result = dict(changed=False, msg=None, diff=None)

    result = ziti_pki(
        ziti_cli
    )

    ziti_cli.exit_json(**result)

def setup_module():
    return OpenZiti(
        argument_spec=ARGUMENT_SPEC,
        required_if=REQUIRED_IF,
        supports_check_mode=SUPPORTS_CHECK_MODE,
    )

def main():
    
    ziti_cli = setup_module()
    run_module(ziti_cli)

if __name__ == '__main__':
    main()
