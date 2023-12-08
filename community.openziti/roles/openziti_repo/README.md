Role Name
=========

This role configures the OpenZiti package repository for APT or YUM, depending on Linux distro family.

Requirements
------------

GnuPG is installed if not present because it's needed to de-armor the repo metadata signing pubkey.

Role Variables
--------------

The role has no variables.

Dependencies
------------

No deps.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - community.openziti.openziti_repo

License
-------

Apache 2.0

Author Information
------------------

The OpenZiti Maintainers can be reached in Discourse: https://openziti.discourse.group/
