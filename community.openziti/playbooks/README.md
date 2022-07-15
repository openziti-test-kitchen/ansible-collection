# Ansible OpenZiti Playbooks

## OpenZiti Download
Playbook file : `demo_openziti_download.yaml`
Example hosts file : 
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