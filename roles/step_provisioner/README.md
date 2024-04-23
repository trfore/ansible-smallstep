# Ansible Role: step_provisioner

- Add provisioners to Step CA, intended to be run on a step CA server.

## Role Variables

| Variable       | Default         | Description                                                          | Required |
| -------------- | --------------- | -------------------------------------------------------------------- | -------- |
| `step_ca_path` | `/etc/step-ca/` | Path, Step CA folder containing configuration and certificate files. | No       |

### Variable: `step_provisioner`

- `step_provisioner` is intend to be a list of dictionaries, the default list will add an ACME provisioner to the CA.

```yaml default/main.yml
# default list
step_provisioner:
  - name: acme
    type: acme
    ssh: false
    renewal_after_expiry: true
```

- **Warning**: The correct variables for each `type` of provisioner are not validated, therefore it is possible to create an invalid configuration. **See the example playbook below for typical variables and values**.

#### ACME Variables

| Dictionary Key         | Default | Description                                                                             | Required | In-line Var Equivalent         |
| ---------------------- | ------- | --------------------------------------------------------------------------------------- | -------- | ------------------------------ |
| `name`                 |         | String, name of the provisioner.                                                        | Yes      |                                |
| `type`                 |         | String, type of provisioner to create, set to: `acme`.                                  | Yes      | `--type`                       |
| `renewal_after_expiry` | `false` | Allow renewals for expired certificates.                                                | No       | `--allow-renewal-after-expiry` |
| `x509_default_dur`     |         | String, default duration, i.e. `72h`, for x509 certificate. Step will default to `24h`. | No       | `--x509-default-dur`           |
| `x509_max_dur`         |         | String, max duration for x509 certificate.                                              | No       | `--x509-max-dur`               |

#### OIDC Variables

| Dictionary Key         | Default | Description                                                | Required | In-line Var Equivalent         |
| ---------------------- | ------- | ---------------------------------------------------------- | -------- | ------------------------------ |
| `name`                 |         | String, name of the provisioner.                           | Yes      |                                |
| `type`                 |         | String, type of provisioner to create, set to: `oidc`.     | Yes      | `--type`                       |
| `renewal_after_expiry` | `false` | Allow renewals for expired certificates.                   | No       | `--allow-renewal-after-expiry` |
| `ssh`                  |         | Boolean, enable provisioning of SSH certificates.          | No       | `--ssh`                        |
| `client_id`            |         | String, id used to validate the audience in an OIDC token. | Yes      | `--client-id`                  |
| `client_secret`        |         | String, secret used to obtain the OIDC tokens.             | Yes      | `--client-secret`              |
| `config_endpoint`      |         | String, OIDC configuration URL.                            | Yes      | `--configuration-endpoint`     |
| `domain`               |         | String, domain used to validate the email claim.           | Yes      | `--domain`                     |

#### SSHPOP Variables

| Dictionary Key         | Default | Description                                              | Required | In-line Var Equivalent         |
| ---------------------- | ------- | -------------------------------------------------------- | -------- | ------------------------------ |
| `name`                 |         | String, name of the provisioner.                         | Yes      |                                |
| `type`                 |         | String, type of provisioner to create, set to: `sshpop`. | Yes      | `--type`                       |
| `renewal_after_expiry` | `false` | Allow renewals for expired certificates.                 | No       | `--allow-renewal-after-expiry` |
| `ssh`                  |         | Boolean, enable provisioning of SSH certificates.        | No       | `--ssh`                        |

#### X5C Variables

| Dictionary Key         | Default | Description                                                                 | Required | In-line Var Equivalent         |
| ---------------------- | ------- | --------------------------------------------------------------------------- | -------- | ------------------------------ |
| `name`                 |         | String, name of the provisioner.                                            | Yes      |                                |
| `type`                 |         | String, type of provisioner to create, set to: `x5c`.                       | Yes      | `--type`                       |
| `renewal_after_expiry` | `false` | Allow renewals for expired certificates.                                    | No       | `--allow-renewal-after-expiry` |
| `ssh`                  |         | Boolean, enable provisioning of SSH certificates.                           | No       | `--ssh`                        |
| `x5c_root`             |         | Path to Root CA cert (PEM-formatted), e.g. `/etc/step-ca/certs/root_ca.crt` | No       | `--x5c-root`                   |

## Example Playbook

### Using an Encrypted Variable File

- Create an `ca-provisioners.yml` and encrypt it using `ansible-vault`.

```yaml
---
step_provisioner:
  - name: acme
    type: acme
    renewal_after_expiry: true
    x509_default_dur: "48h"
    x509_max_dur: "168h"
  - name: google
    type: oidc
    ssh: true
    client_id: "" # From GCP API Config
    client_secret: "" # From GCP API Config
    config_endpoint: "https://accounts.google.com/.well-known/openid-configuration"
    domain: "gmail.com"
  - name: sshpop
    type: sshpop
    ssh: true
  - name: x5c
    type: x5c
    ssh: true
    x5c_root: "/etc/step-ca/certs/root_ca.crt"
```

- Playbook Example

```yaml
---
- hosts: ca_server
  vars_files:
    - ca-provisioners.yml
  roles:
    - name: Add Smallstep Provisioner
      role: trfore.smallstep.step_provisioner
```

## References

- https://smallstep.com/docs/step-ca/provisioners/
- https://smallstep.com/docs/step-cli/reference/ca/provisioner/add/
