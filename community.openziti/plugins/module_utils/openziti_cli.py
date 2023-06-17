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
    
    @property
    def ziti(self):

        ziti = self.get_bin_path("ziti") or self.params.get("ziti_cli_path")
        if not ziti:
            self.fail_json(msg="Ziti CLI not found, consider adding it to the path or providing ziti_cli_path parameter.")
            
        return [ziti]
    
    def get_bin_path(self, arg, required=False, opt_dirs=None):
        return self._module.get_bin_path(arg, required=required, opt_dirs=opt_dirs)

    def run_command(self, args: List, **kwargs):
        command = [element if type(element) is str else str(element) for element in args]

        return self._module.run_command(command, **kwargs)
    
    def exit_json(self, **kwargs):
        return self._module.exit_json(**kwargs)
    
    def fail_json(self, msg, **kwargs):
        return self._module.fail_json(msg, **kwargs)
