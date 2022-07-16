# OpenZiti Download
This role downloads the OpenZiti binaries from Github releases and puts each Ziti component (controller, edge, tunnel, etc) on the appropriate host using host's group name.

The role is idempotent, so it can be easily used with AWX.

## TODO :
- Find a way to support specific version download from Ziti Console
- Maybe set OpenZiti components in host vars and not host groups
- Support version upgrades

## Usage

### Sudo Password
Some tasks needs to be executed with sudo privileges, when using openziti_download role, make sure you have a safe way of storing your sudo passwords.
For example, you could use `ansible-vault` and update your hosts file with the key-value `ansible_become_pass="{{ my_host_become_pass }}"`.

When using your localhost as the `cache-server` (i.e `openziti_cache_localhost` = `true`), you need sudo privileges to make sure that some packages are installed on your localhost (ref. [required_packages.yaml](/community.openziti/roles/openziti_download/tasks/required_packages.yaml)).
Either specify your localhost sudo password with `-K` or `--ask-become-pass` option, or put your password on the variable `localhost_become_pass` while making sure you're storing it in a secure way.

When using a remote host as the `cache-server` (i.e `openziti_cache_localhost` = `false`), you should provide the sudo password in host variables.

### Example hosts
```
---
all:
  children:
    dev_network:
      hosts:
        host_one:
          ansible_host: XXX.XX.XXX.XXX
          ansible_ssh_user: XXXXX
          ansible_become_pass="{{ host_one_become_pass }}"
          openziti_components:
            - ziti-controller
            - ziti-router
            - ziti-tunnel
            - ziti
            - ziti-edge-tunnel
        host_two:
          ansible_host: XXX.XX.XXX.XXX
          ansible_ssh_user: XXXXX
          ansible_become_pass="{{ host_two_become_pass }}"
          openziti_components:
            - ziti_console
```
### Role variables you should care about

 <table>
  <tr>
    <th>Variable</th>
    <th>Default value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>openziti_core_version</td>
    <td>latest</td>
    <td>OpenZiti core binaries version </td>
  </tr>
  <tr>
    <td>openziti_edge_tunnel_version</td>
    <td>latest</td>
    <td>OpenZiti edge tunnel binaries version </td>
  </tr>
  <tr>
    <td>openziti_console_version</td>
    <td>master</td>
    <td>OpenZiti Console branch name</td>
  </tr>
  <tr>
    <td>openziti_remote_path</td>
    <td>/opt/openziti</td>
    <td>Host's directory where to store OpenZiti components</td>
  </tr>
  <tr>
    <td>openziti_cache_downloads_dir</td>
    <td>/tmp/openziti_downloads</td>
    <td>Directory where to store OpenZiti Downloads on cache server</td>
  </tr>
  <tr>
    <td>openziti_cache_releases_dir</td>
    <td>/tmp/openziti_releases</td>5 Allee Saint Exupery 92390 Villeneuve La Garenne
    <td>Directory where to store OpenZiti components on cache server</td>
  </tr>
  <tr>
    <td>openziti_controller_dir</td>
    <td>"{{ openziti_cache_releases_dir }}/remote_install"</td>
    <td>Directory where to store ansible components on ansible controller before pushing to remote</td>
  </tr>
</table> 

