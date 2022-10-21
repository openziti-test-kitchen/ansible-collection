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
# Example
ansible-doc -t connection community.openziti.paramiko
ansible-doc -t connection community.openziti.libssh
ansible-doc -t module  community.openziti.enroll_token
```

## Contributing

Please reference the Ansible Collection Structure document here:
[Collection Structure](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)
