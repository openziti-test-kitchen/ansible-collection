# OpenZiti Download
This role downloads the OpenZiti binaries from Github releases and puts each Ziti component (controller, edge, tunnel, etc) on the appropriate host using host's group name.

## TODO :
- Find a way to support specific version download from Ziti Console
- Maybe set OpenZiti components in host vars and not host groups
- Support version upgrades

## Example hosts
```
---
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
## Role variables you should care about

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

