# Ansible Collection - trfore.smallstep

[![CI](https://github.com/trfore/ansible-smallstep/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/trfore/ansible-smallstep/actions/workflows/ci.yml)
[![CD](https://github.com/trfore/ansible-smallstep/actions/workflows/cd.yml/badge.svg)](https://github.com/trfore/ansible-smallstep/actions/workflows/cd.yml)
[![Release Check](https://github.com/trfore/ansible-smallstep/actions/workflows/release-check.yml/badge.svg)](https://github.com/trfore/ansible-smallstep/actions/workflows/release-check.yml)

- This collection is for setting up a a public key infrastructure (PKI) using Smallstep. It will install CA server and, optionally, configure the CA server and host servers ("clients") to request x509 certificates from the CA.
- The default values for the collection are set with the intention of being used in production and **initializing the CA server offline, outside of an Ansible play**. However, you can set `step_ca_initialize: true` and initialize the PKI via an Ansible playbook, for more details see:
  - [`step_ca` readme](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_ca/README.md) or [scenario guide: ca](https://trfore.github.io/ansible-smallstep/branch/main/docsite/guide_ca_nonproduction.html)
- For client servers, the default argument values for the roles are designed for generating a single ACME certificate and automatically renew it on each host. Yet, you can configure the roles to generate and request multiple x509 certificates and **SSH certificates** as well. See the example playbook below, READMEs and scenario guides for more details:
  - [`step_cert` readme](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_cert/README.md) or [scenario guide: client](https://trfore.github.io/ansible-smallstep/branch/main/docsite/guide_client.html)
  - [`step_ssh` readme](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_ssh/README.md) or [scenario guide: ssh](https://trfore.github.io/ansible-smallstep/branch/main/docsite/guide_ssh.html)

## Install the Collection

You can install this collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install trfore.smallstep
```

## Roles

- Variables and default values are listed in each role's README and available at the documentation website: https://trfore.github.io/ansible-smallstep/branch/main
  - [`step_ca`](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_ca) - Install and Initialize Step CA
  - [`step_ca_cert`](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_ca_cert) - Download and add the CA root certificate to trust stores
  - [`step_cert`](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_cert) - Request an x509 certificate from the CA and automatically renew it
  - [`step_cli`](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_cli) - Install Step CLI
  - [`step_provisioner`](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_provisioner) - Add provisioners to Step CA
  - [`step_ssh`](https://github.com/trfore/ansible-smallstep/tree/main/roles/step_ssh) - Generate SSH host certificate and configure server to accept user certificates

## Tested Platforms

- `ansible-core` 2.16, 2.17 & 2.18
- CentOS Stream 9
- Debian 11 & 12
- Ubuntu 22.04 & 24.04

## Example Playbook

### Production Workflow

**NOTE**: For installs with numerous end-points (50+) or repetitive playbook testing, **we highly recommend using `STEP_*_VERSION` variables in your playbook**
**to avoid hitting GitHub's API rate limiter** (60 unauthenticated request per hour).

```yaml
- name: Setup Step CA Server
  hosts: ca-server
  become: true
  gather_facts: true
  roles:
    - name: Install Step CLI
      role: trfore.smallstep.step_cli
      vars:
        step_cli_version: "0.28.7"

    - name: Install Step Certificates
      role: trfore.smallstep.step_ca
      vars:
        step_ca_version: "0.28.4"
```

- Phase I: Create a step CA server.

```yaml
---
- name: Setup Step CA Server
  hosts: ca-server
  become: true
  gather_facts: true
  roles:
    - name: Install Step CLI
      role: trfore.smallstep.step_cli

    - name: Install Step Certificates
      role: trfore.smallstep.step_ca
### Initialize the CA Offline, storing the root key in an encrypted drive ###
```

- Phase II: Configure clients to request certificates from the CA.

```yaml
---
- name: Extract Root CA Information
  hosts: ca-server
  become: true
  tasks:
    - name: Get Root CA Fingerprint
      ansible.builtin.command: step certificate fingerprint /etc/step-ca/certs/root_ca.crt
      register: ca_fingerprint
      changed_when: true

- name: Setup Step CA Clients (Servers)
  hosts: ca_clients
  become: true
  gather_facts: true
  roles:
    - name: Install Step CLI
      role: trfore.smallstep.step_cli

    - name: Bootstrap Step CA Root Certificate
      role: trfore.smallstep.step_ca_cert
      vars:
        step_ca_fingerprint: "{{ hostvars['ca-server'].ca_fingerprint.stdout }}"
        step_ca_url: "https://ca.example.com"

    - name: Request x509 Certificate
      role: trfore.smallstep.step_cert
```

### Non-production Example with CA Initialization

- A complete playbook file is available under [playbooks/non-production.yml (link)](https://github.com/trfore/ansible-smallstep/blob/main/playbooks/non-production.yml) with example [playbooks/group_vars (link)](https://github.com/trfore/ansible-smallstep/tree/main/playbooks/group_vars).

```yaml
---
- name: Setup Step CA Server
  hosts: ca-server
  become: true
  gather_facts: true
  roles:
    - name: Install Step Certificates
      role: trfore.smallstep.step_ca
      vars:
        step_ca_initialize: true
        step_ca_enable_service: true
        step_ca_name: "Example.com CA" # Required
        step_ca_password: "password01" # Required
        step_ca_provisioner_password: "password02" # Required
        step_ca_ssh_mgmt: true # For SSH certificates

    - name: Add Provisioner to Step CA
      role: trfore.smallstep.step_provisioner
      vars:
        step_provisioner:
          - name: acme
            type: acme
            renewal_after_expiry: true
            x509_default_dur: "48h"
            x509_max_dur: "168h"
          - name: google
            type: oidc
            ssh: true # For SSH certificates
            client_id: "" # From GCP API Config
            client_secret: "" # From GCP API Config
            config_endpoint: "https://accounts.google.com/.well-known/openid-configuration"
            domain: "gmail.com"
          - name: sshpop # For SSH certificate renewal
            type: sshpop
            ssh: true

  tasks:
    - name: Get root CA fingerprint
      ansible.builtin.command: step certificate fingerprint /etc/step-ca/certs/root_ca.crt
      register: ca_fingerprint
      changed_when: false
      failed_when: ca_fingerprint.rc == 1

- name: Setup Step CA Clients (Servers)
  hosts: ca_clients
  become: true
  gather_facts: true
  roles:
    - name: Install Step CLI
      role: trfore.smallstep.step_cli

    - name: Bootstrap Step CA Root Certificate
      role: trfore.smallstep.step_ca_cert
      vars:
        step_ca_fingerprint: "{{ hostvars['ca-server'].ca_fingerprint.stdout }}"
        step_ca_url: "https://ca.example.com"

    - name: Request x509 Certificate
      role: trfore.smallstep.step_cert

    # For SSH certificates
    - name: Configure Host for SSH Certificates
      role: trfore.smallstep.step_ssh
      vars:
        step_ssh_provisioner: "Example.com" # JWK provisioner name extracted from 'Example.com CA'
        step_ssh_provisioner_password: "password02" # Same value passed to 'step_provisioner_password', see 'step_ssh' README for details.
```

## Author and License Information

Taylor Fore (https://github.com/trfore)

See LICENSE file for this Ansible collection.

Smallstep (`certificates` and `cli`) is Apache 2.0 license software from Smallstep Labs, Inc. For additional information see:

- https://smallstep.com/terms-of-use/
- https://github.com/smallstep/certificates/blob/master/LICENSE
- https://github.com/smallstep/cli/blob/master/LICENSE

## References

- https://smallstep.com/docs/step-ca/certificate-authority-server-production/
- https://smallstep.com/docs/step-ca/provisioners/
- https://smallstep.com/docs/step-cli/reference/ca/provisioner/add/

### Using Smallstep in Production

- Using a Yubikey as an alternative to a HSM, https://smallstep.com/blog/build-a-tiny-ca-with-raspberry-pi-yubikey/
- https://smallstep.com/docs/step-ca/certificate-authority-server-production/
