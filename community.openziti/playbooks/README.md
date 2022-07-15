# Ansible OpenZiti Playbooks

## OpenZiti Download Role
Playbook file : `demo_openziti_download.yaml`.

Example playbook that uses [openziti_download role](/community.openziti/roles/openziti_download).

### Sudo Password
Some tasks needs to be executed with sudo privileges, when using openziti_download role, make sure you have a safe way of storing your sudo passwords.
For example, you could use `ansible-vault` and update your hosts file with the key-value `ansible_become_pass="{{ my_host_become_pass }}"`.

When using your localhost as the `cache-server` (i.e `openziti_cache_localhost` = `true`), run your playbooks with `-K` option, because this role needs sudo privileges to infer which package manager your localhost is using (ref. [required_packages.yaml](/community.openziti/roles/openziti_download/tasks/required_packages.yaml)).

### Hosts file : 
```
all:
  children:
    dev_network:
      hosts:
        host_one:
          ansible_host: XXX.XX.XXX.XXX
          ansible_ssh_user: XXXXX
          openziti_components:
            - ziti-controller
            - ziti-router
            - ziti-tunnel
            - ziti
            - ziti-edge-tunnel
        host_two:
          ansible_host: XXX.XX.XXX.XXX
          ansible_ssh_user: XXXXX
          openziti_components:
            - ziti_console
```