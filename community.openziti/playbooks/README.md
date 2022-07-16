# Ansible OpenZiti Playbooks

## OpenZiti Download Role
Playbook file : `demo_openziti_download.yaml`.

Example playbook that uses [openziti_download role](/community.openziti/roles/openziti_download).

### Sudo Password
Some tasks needs to be executed with sudo privileges, when using openziti_download role, make sure you have a safe way of storing your sudo passwords.
For example, you could use `ansible-vault` and update your hosts file with the key-value `ansible_become_pass="{{ my_host_become_pass }}"`.

When using your localhost as the `cache-server` (i.e `openziti_cache_localhost` = `true`), you need sudo privileges to make sure that some packages are installed on your localhost (ref. [required_packages.yaml](/community.openziti/roles/openziti_download/tasks/required_packages.yaml)).
Either specify your localhost sudo password with `-K` or `--ask-become-pass` option, or put your password on the variable `localhost_become_pass` while making sure you're storing it in a secure way.

When using a remote host as the `cache-server` (i.e `openziti_cache_localhost` = `false`), you should provide the sudo password in host variables.

### Hosts file : 

### Localhost cache
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

### Remote cache server
```
all:
  children:
    dev_network:
      hosts:
        host_one:
          ansible_host: XXX.XX.XXX.XXX
          ansible_ssh_user: XXXXX
          ansible_become_pass: XXXX
          openziti_components:
            - ziti-controller
            - ziti-router
            - ziti-tunnel
            - ziti
            - ziti-console
            - ziti-edge-tunnel
        cache_server:
          ansible_host: XXX.XX.XXX.XXX
          ansible_ssh_user: XXXXX
          ansible_become_pass: XXXX
```