#!/usr/bin/env python
"""OpenZiti Edge Client API"""
from __future__ import (absolute_import, annotations, division, print_function)

import json
import os
import tempfile
from typing import Any, Dict, Union

import openziti_edge_client
from ansible.errors import AnsibleRuntimeError
from ansible.module_utils.common.text.converters import to_bytes
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from openziti_edge_client.api import authentication_api, service_api
from openziti_edge_client.model.authenticate import Authenticate
from openziti_edge_client.model.config_types import ConfigTypes

DOCUMENTATION = '''
    name: openziti_identity_inventory
    version_added: "0.3.0"
    short_description: Discovers OpenZiti identities for connection plugins
    requirements:
      - Enabled in configuration
      - OpenZiti identity with dial service policy for target identities
    description:
      - Reads list of OpenZiti identities from service terminator list
      - Sets ansible_connection for matching OpenZiti identities
    extends_documentation_fragment:
      - community.openziti.openziti_connection
'''

display = Display()

IDENTITY_SCHEMA = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "ztAPI": {
      "type": "string"
    },
    "id": {
      "type": "object",
      "properties": {
        "cert": {
          "type": "string"
        },
        "key": {
          "type": "string"
        },
        "ca": {
          "type": "string"
        }
      },
      "required": [
        "cert",
        "key",
        "ca"
      ]
    }
  },
  "required": [
    "ztAPI",
    "id"
  ]
}

CONFIG_TYPE = "ansible-target-discovery.v1"


def gather_identity_data(identity_file: str) -> Dict[str, Any]:
    """
    Gathers Ansible connection variables from OpenZiti identities.

    These variables are read by the OpenZiti connection modules
    to automatically configure how connections are made to
    ziti targets. In particular, identities are discovered
    for configuring the connection clients for dialing
    OpenZiti addressable terminators.

    :param identity_file: path to an identity.json file
    :returns: dictionary of per identity ansible connection variables
    """
    # pylint: disable=too-many-statements, too-many-locals

    display.vvv(f"OPENZITI Gathering connection vars from: {identity_file}")

    with open(identity_file, 'r', encoding='UTF-8') as id_f:
        id_json = json.load(id_f)

    # pylint: disable=consider-using-with
    ca_fp = tempfile.NamedTemporaryFile(buffering=0)
    ca_fp.write(id_json['id']['ca'].encode('UTF-8'))

    cert_fp = tempfile.NamedTemporaryFile(buffering=0)
    cert_fp.write(id_json['id']['cert'].encode('UTF-8'))

    key_fp = tempfile.NamedTemporaryFile(buffering=0)
    key_fp.write(id_json['id']['key'].encode('UTF-8'))

    configuration = openziti_edge_client.Configuration(
        host=id_json['ztAPI'] + "/edge/client/v1",
        ssl_ca_cert=ca_fp.name
    )

    configuration.cert_file = cert_fp.name
    configuration.key_file = key_fp.name

    with openziti_edge_client.ApiClient(configuration) as api_client:
        api_auth = authentication_api.AuthenticationApi(api_client)
        method = "cert"  # pylint: disable=invalid-name

        auth = Authenticate(config_types=ConfigTypes(
            [CONFIG_TYPE]))

        try:
            session = api_auth.authenticate(method, auth=auth)
        except openziti_edge_client.OpenApiException as err:
            raise AnsibleRuntimeError(
                "Error calling OpenZiti.AuthenticationApi->authenticate."
            ) from err

        configuration.api_key['ztSession'] = session.data.token
        api_service = service_api.ServiceApi(api_client)

        try:
            services = api_service.list_services()
        #        filter='tags.ansible_inventory="yes"')
        except openziti_edge_client.exceptions.ApiException as err:
            raise AnsibleRuntimeError(
                "Error calling OpenZiti.ServiceApi->list_services.") from err
        except openziti_edge_client.exceptions.ApiValueError as err:
            raise AnsibleRuntimeError(
                "Error calling OpenZiti.ServiceApi->list_services. "
                "Please check service has at least 1 service config.") from err

        ansible_data: Dict[str, Any] = {}

        if not services.data.value:
            raise AnsibleRuntimeError(
                "Identity cannot dial or bind any services"
            )

        for service in services.data.value:
            try:
                config = service.config
            except KeyError as err:
                raise AnsibleRuntimeError(
                        "OpenZiti service result has no config key.") from err

            config_dict = config.get(CONFIG_TYPE)
            if not config_dict:
                display.vvv(
                        f"OPENZITI Skipping service: {service.name} => "
                        f"Only services with an {CONFIG_TYPE} "
                        "config are considered."
                    )
                continue

            dial_permission_found = False

            for permission in service.permissions.value:
                if 'Dial' == permission.value:
                    dial_permission_found = True

            if not dial_permission_found:
                display.vvv(
                        f"OPENZITI Skipping service: {service.name} => "
                        "Identity does not have permission to Dial service."
                    )
                continue

            try:
                terminators = api_service.list_service_terminators(service.id)
            except openziti_edge_client.ApiException as err:
                raise AnsibleRuntimeError(
                    "Error calling"
                    "OpenZiti.ServiceApi->list_service_terminators."
                ) from err

            for terminator in terminators.data.value:
                identity = terminator.identity
                if ansible_data.get('identity') is not None:
                    continue
                if not identity:
                    raise AnsibleRuntimeError(
                        "No OpenZiti terminator identity found")

                zitivars: Dict[str, str] = {}
                zitivars['ziti_connection_identity_file'] = identity_file
                zitivars['ziti_connection_service'] = service.name
                zitivars['ziti_connection_service_terminator'] = identity

                variables: Dict[str, Union[Dict, Union[str, int]]] = {
                        "ziti_connection_dial_service": zitivars
                    }
                variables['ansible_connection'] = "community.openziti." +\
                    config_dict['connection_plugin']
                ansible_data[identity] = variables
        return ansible_data


class InventoryModule(BaseInventoryPlugin):
    """OpenZiti automatic discovery of targets."""

    NAME = 'community.openziti.connection_autodiscover'

    def __init__(self):
        self._identities = []
        super().__init__()

    def verify_file(self, path: str) -> bool:
        """Enables this plugin when magic value is set."""
        valid = False
        b_path = to_bytes(path, errors='surrogate_or_strict')
        if not os.path.exists(b_path) and not \
                path.split('/')[-1] == "openziti_connection_autodiscover":
            return valid

        self._identities.extend(self.get_option('ziti_identities'))

        for identity in self._identities:
            try:
                with open(identity, 'r', encoding='UTF-8') as identity_file:
                    identity_json = json.load(identity_file)
            except ValueError:
                display.vvv(
                        f"OPENZITI Could not load identity file: {identity}")
            else:
                try:
                    validate(identity_json, IDENTITY_SCHEMA)
                except ValidationError:
                    display.vvv("OPENZITI Identity failed schema validation.")
                else:
                    valid = True
        return valid

    def parse(self, inventory, loader, path, cache=False) -> None:
        """Gathers inventory data from ziti identity files"""

        super().parse(inventory, loader, path, cache)

        for identity in self._identities:
            host_data = gather_identity_data(identity)
            for host, data in host_data.items():
                self.inventory.add_host(host)
                for key, value in data.items():
                    self.inventory.set_variable(host, key, value)
