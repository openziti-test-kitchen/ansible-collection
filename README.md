# OpenZiti Ansible Collection

Add to your `requirements.yaml` file:

```yaml
---
collections:
  - name: community.openziti
    source: https://github.com/netfoundry/ansible-collection.git
    type: git
...
```

Then run:

```bash
ansible-galaxy collection install -r requirements.yaml
```

Install Python dependencies

```bash
pip install --requirements ./ansible_collections/community/openziti/requirements.txt
```

You can read the docs using `ansible-doc`:

```bash
# === Connection Plugins ===
ansible-doc -t connection community.openziti.paramiko
ansible-doc -t connection community.openziti.libssh
# === Modules Plugins ===
ansible-doc -t module community.openziti.enroll_token
# === Inventory Plugins ===
ansible-doc -t inventory community.openziti.connection_autodiscovery
```

## Notes

* The `community.openziti.libssh` connection plugin is experimental.
  Prefer the paramiko connection plugin instead.
* The `connection_autodiscover` connection plugin involves some OpenZiti setup
  to function. Please see this GitHub project's
  [wiki](https://github.com/openziti-test-kitchen/ansible-collection/wiki/OpenZiti-Inventory-Autodiscovery-Setup) for details.

## Contributing

Please reference the Ansible Collection Structure document here:
[Collection Structure](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)
