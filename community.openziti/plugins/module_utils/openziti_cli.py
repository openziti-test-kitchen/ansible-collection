from typing import List

from ansible.module_utils.basic import AnsibleModule

class OpenZiti:

    def __init__(self, **kwargs):

        self._module = AnsibleModule(**kwargs)
                
    @property
    def module(self):
        return self._module

    @property
    def params(self):
        return self._module.params
    
    @property
    def check_mode(self):
        return self._module.check_mode

    def run_command(self, args: List, **kwargs):
        command = [element if type(element) is str else str(element) for element in args]

        return self._module.run_command(command, **kwargs)
    @property
    def ziti(self):

        ziti = self._module.get_bin_path("ziti") or self.params.get("ziti_cli_path")
        if not ziti:
            self.fail_json(msg="Ziti CLI not found, consider adding it to the path or providing ziti_cli_path parameter.")
            
        return [ziti]
