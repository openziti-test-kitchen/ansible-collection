# OpenZiti Download
This role downloads the OpenZiti binaries from Github releases and puts each Ziti component (controller, edge, tunnel, etc) on the appropriate host using host's group name.

## TODO :
- Find a way to support specific version download from Ziti Console


## Example playbook & hosts
ADD EXAMPEL PLAYBOOK HERE

## Role variables
 <table>
  <tr>
    <th>Variable</th>
    <th>Default value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>openziti_version</td>
    <td>latest</td>
    <td>OpenZiti binaries version </td>
  </tr>
  <tr>
    <td>openziti_supported_os_architecture</td>
    <td><ul>
        <li>linux: ["arm64", "arm", "amd64"]</li>
        <li>darwin: ["amd64"] </li>
        <li>windows: not supported </li>
    </td></ul>
    <td>Supported OS and OS architecture</td>
  </tr>
  <tr>
    <td>openziti_cache_downloads_dir</td>
    <td>/tmp/openziti_downloads</td>
    <td>Directory where to store OpenZiti Downloads on cache server</td>
  </tr>
  <tr>
    <td>openziti_cache_releases_dir</td>
    <td>/tmp/openziti_releases</td>
    <td>Directory where to store OpenZiti components</td>
  </tr>
  <tr>
    <td>openziti_cache_release_version_dir</td>
    <td>Computed usin `openziti_cache_releases_dir` and `openziti_archive_name` </td>
    <td>OpenZiti components directory on cache server</td>
  </tr>
  <tr>
    <td>openziti_cache_localhost</td>
    <td>true</td>
    <td>Whether to use localhost as Cache server</br>Is set to "false", must set a group 'cache_server' on hosts file</td>
  </tr>
  <tr>
    <td>openziti_os_architecture</td>
    <td>Computed from ansible facts</td>
    <td>Host's os architecture</td>
  </tr>
  <tr>
    <td>openziti_os_name</td>
    <td>Computed from ansible facts</td>
    <td>Host's OS (Windows, Linux or Mac)</td>
  </tr>
  <tr>
    <td>openziti_archive_extension</td>
    <td>tar.gz</td>
    <td>OpenZiti compressed binaries file extension</td>
  </tr>
  <tr>
    <td>openziti_archive_name</td>
    <td>ziti-{{ openziti_os_name }}-{{ openziti_os_architecture}}-{{ openziti_version }}</td>
    <td>OpenZiti binaries compressed file name</td>
  </tr>
  <tr>
    <td>openziti_binaries_url</td>
    <td>https://github.com/openziti/ziti/releases/download/v{{ openziti_version }}/{{ openziti_archive_name }}.{{ openziti_archive_extension }}</td>
    <td>OpenZiti binaries download URL</td>
  </tr>
  <tr>
    <td>openziti_binaries_path_remote</td>
    <td>/opt/openziti</td>
    <td>Host's directory where to store OpenZiti components</td>
  </tr>
  <tr>
    <td>openziti_components</td>
    <td>ziti-controller, ziti-router, ziti-tunnel, ziti and ziti-console</td>
    <td>List of OpenZiti components</td>
  </tr>
  <tr>
    <td>openziti_console_version</td>
    <td>latest</td>
    <td>OpenZiti console version</td>
  </tr>
  <tr>
    <td>openziti_console_branch_name</td>
    <td>master</td>
    <td>Github branch used to clone OpenZiti console binaries</td>
  </tr>
  <tr>
    <td>openziti_console_repository</td>
    <td>https://github.com/openziti/ziti-console</td>
    <td>OpenZiti console github repository URL</td>
  </tr>
</table> 

