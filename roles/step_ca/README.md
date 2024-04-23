# Ansible Role: step_ca

- Install step CA, `step-ca`, for generating SSL/TLS certificates. The default values will only install the `step-ca` binary, if you would like to initialize a public key infrastructure (PKI) set `step_ca_initialize: true`.
  - **Note**: The default initialization values are for **non-production** use only, as it will generate the PKI on the local disk at `/etc/step-ca/`; this path is assigned using the `step_ca_path` variable. Additionally, it will create two password files, `/etc/step-ca/password.txt` and `/etc/step-ca/password-provisioner.txt`, that are read-write only by the system-user `step`.
- Sensitive values are masked from ansible log, however, it is important to store these values using a form of encryption, e.g. ansible-vault.
- It is possible to automate this role and initialize the PKI on a removable usb-drive; followed by a custom ansible task to move the keys to a security device, such as Yubikey. However, this is beyond the scope of the role and collection.

## Role Variables

| Variable           | Default | Description                                                                            | Required |
| ------------------ | ------- | -------------------------------------------------------------------------------------- | -------- |
| `step_ca_checksum` | URL     | URL to `step-ca` package checksum. If empty, the checksum is skipped.                  | No       |
| `step_ca_pkg_src`  | URL     | URL to `step-ca` package. Can be overridden in playbook when using a proxy.            | No       |
| `step_ca_version`  | latest  | String, SemVer of `step-ca` to install, e.g. `0.15.7`, defaults to the latest version. | No       |

### CA Initialize Values

| Variable                       | Default         | Description                                                                  | Required            | In-line Var Equivalent        |
| ------------------------------ | --------------- | ---------------------------------------------------------------------------- | ------------------- | ----------------------------- |
| `step_ca_initialize`           | `false`         | Boolean, initializes a public key infrastructure (PKI) to be used by the CA. | No                  |                               |
| `step_ca_enable_service`       | `false`         | Boolean, create systemd service for `step-ca`.                               | No                  |                               |
| `step_ca_path`                 | `/etc/step-ca/` | Path, Step CA folder containing configuration and certificate files.         | No                  |                               |
| `step_ca_address`              | `:443`          | String, address the CA will listen at.                                       | No                  | `--address`                   |
| `step_ca_name`                 | not defined     | String, name of the public key infrastructure (PKI).                         | Yes, if initialized | `--name`                      |
| `step_ca_password`             | not defined     | String, password to encrypt the root and intermediate keys.                  | Yes, if initialized | `--password-file`             |
| `step_ca_provisioner_password` | not defined     | String, password for default JWK provisioner.                                | Yes, if initialized | `--provisioner-password-file` |
| `step_ca_root_cert`            | not defined     | Path to existing PEM file to be used as the root CA.                         | No                  | `--root`                      |
| `step_ca_root_key`             | not defined     | Path to key file for the existing PEM certificate.                           | No                  | `--key`                       |
| `step_ca_root_key_password`    | not defined     | Path to file with decryption password for the existing PEM certificate key.  | No                  | `--key-password-file`         |
| `step_ca_ssh_mgmt`             | `false`         | Boolean, enable ssh certificate management.                                  | No                  | `--ssh`                       |

## Dependencies

- `trfore.smallstep.step_cli`: Initializing the CA server, offline or using this role, requires `step`(aka `step-cli`). If you attempt to initialize the CA server using this role, it will install `step` if required.

## Example Playbooks

### Basic Playbook With Clear Text Passwords

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
```

### Using an Encrypted Variable File

- Create an `vars/ca-vars.yml`.

```yaml
---
step_ca_initialize: true
step_ca_enable_service: true
step_ca_name: "Example.com CA" # Required
step_ca_password: "{{ vault_step_ca_password }}" # Required
step_ca_provisioner_password: "{{ vault_step_ca_provisioner_password }}" # Required
```

- Create an `vars/vault.yml` and encrypt it using `ansible-vault`.

```yaml
---
vault_step_ca_password: "password01"
vault_step_ca_provisioner_password: "password02"
```

- Playbook Example

```yaml
---
- name: Setup Step CA Server
  hosts: ca-server
  become: true
  gather_facts: true
  vars_files:
    - ca-vars.yml
  roles:
    - name: Install Step Certificates
      role: trfore.smallstep.step_ca
```

### Using a Package Proxy

```yaml
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
        step_ca_name: "Example.com CA"
        step_ca_password: "password01"
        step_ca_provisioner_password: "password02"
        step_ca_pkg_src: "https://PROXY_URL/step-ca_x.x.x_amd64.deb" # Proxy URL
        step_ca_checksum: "" # Skip checksum
```

## References

- https://github.com/smallstep/certificates/releases/
- https://smallstep.com/docs/step-ca/certificate-authority-server-production/
- https://smallstep.com/docs/step-cli/reference/ca/provisioner/add/
- Using a Yubikey as an alternative to a HSM, https://smallstep.com/blog/build-a-tiny-ca-with-raspberry-pi-yubikey/
