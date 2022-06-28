# OpenZiti Download
This role downloads the OpenZiti binaries from Github releases and puts each Ziti component (controller, edge, tunnel, etc) on the appropriate host using host's group name.

## Role variables
| Variable                                    | Default value                    | Description                                  |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_version                            | latest                           | OpenZiti binaries version                    |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_supported_os_architecture          | linux: ["arm64", "arm", "amd64"] | Supported OS and OS architecture             ||                                             |                                  |                                              |
|                                             | darwin: ["amd64"]                |                                              |
|                                             | windows: not supported           |                                              |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_cache_downloads_dir                | /tmp/openziti_downloads          | Directory where to store OpenZiti Downloads  |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_cache_releases_dir                 | /tmp/openziti_releases           | Directory where to store OpenZiti components
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_cache_release_version_dir          | Computed                         | OpenZiti components directory on cache server|
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_cache_localhost                    | true                             | Whether to use localhost as Cache server     |
|                                             |                                  | Is set to "false", must set a group          |
|                                             |                                  | cache_server on hosts file                   |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_cache_host                         |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_os_architecture                    |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_os_name                            |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_archive_extension                  |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_archive_name                       |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_binaries_url                       |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_binaries_path_remote               |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_components                         |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_console_version                    |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_console_branch_name                |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |
| openziti_console_repository                 |
| ------------------------------------------- | -------------------------------- | -------------------------------------------- |




















## Example playbook & hosts
ADD EXAMPEL PLAYBOOK HERE

## TODO :
- Find a way to support specific version download from Ziti Console
