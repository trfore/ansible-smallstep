# Ansible Role: step_ssh

- This role will request an SSH host certificate from a step CA server and automatically renew it.
  - It will use the default JWK provider for the initial request and the SSHPOP provider for renewal.
  - SSH host certificates have a default expiration of 30 days, the renewal service is a systemd timer that checks on a daily basis (07:00 UTC / 02:00 EST ± 00:15) and renews when the certificate exceeds 66% of its lifetime.
- The role will also configure the host to accept user certificates.

## Requirements

- `expects`, this role will temporarily install it using the OS package manager.
- `openssh-server`, this role **does not** install openssh.

## Role Variables

### CA Root Certificate Variables

| Variable       | Default         | Description                                                                | Required | In-line Var Equivalent |
| -------------- | --------------- | -------------------------------------------------------------------------- | -------- | ---------------------- |
| `step_ca_path` | `/etc/step-ca/` | Path, Step CA folder containing the CA configuration and root certificate. | No       | `STEPPATH`             |

### SSH Certificate Variables

- This role currently supports using the **JWK** provisioner to generate **host certs**. Yet, `step` supports both **JWK** and **Cloud** provisioners, see `step ssh certificate --help`.
- A `step_ssh_provisioner_password` **OR** `step_ssh_token` is required, **do not supply both**.
  - Using `step_ssh_provisioner_password` passes the value via the CLI using `expects`. This is intended for use during the initial setup of a Step CA server and clients. However, its best practice to change the JWK password after initialization, `step ca provisioner update [JWK_NAME]` , **OR** remove the JWK provisioner.

| Variable                        | Default              | Description                                                                                                                                           | Required | In-line Var Equivalent |
| ------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------- |
| `step_ssh_key_pair_name`        | `ssh_host_ecdsa_key` | String, name of the SSH key pair within `/etc/ssh/` to use for generating a certificate.                                                              | No       |                        |
| `step_ssh_provisioner`          | not defined          | String, the **name** of the provisioner to use. The default JWK provisioner is the first word in the CA name, e.g. `Example.com` in 'Example.com CA'. | Yes      | `--provisioner`        |
| `step_ssh_provisioner_password` | not defined          | String, password for provisioner. Do not combine with `step_ssh_token`.                                                                               | Yes\*    |                        |
| `step_ssh_token`                | not defined          | String, one-time token used to authenticate with the CA. Do not combine with `step_ssh_provisioner_password`.                                         | Yes\*    | `--token`              |
| `step_ssh_principal_0`          | `ansible_fqdn`       | Primary principle to add the certificate, defaults to the to the FQDN of the host.                                                                    | No       | `--principal`          |
| `step_ssh_principal_1`          | not defined          | String, optional additional principle to add the certificate, e.g. host name or IP address.                                                           | No       | `--principal`          |

## Dependencies

- `trfore.smallstep.step_ca_cert`: The CA root certificate is required, this role will download the CA root certificate and add it to the system's trust store.

## Example Playbooks

### During Initial Setup of CA Server and Clients using JWK

```yaml
- hosts: ca_clients
  roles:
    - name: Configure Host for SSH Certificates
      role: trfore.smallstep.step_ssh
      vars:
        step_ssh_provisioner: "Example.com" # JWK provisioner name extracted from 'Example.com CA'
        step_ssh_provisioner_password: "{{ step_ca_provisioner_password }}"
```

## References

- https://smallstep.com/docs/ssh/hosts-step-by-step/
- https://support.smallstep.com/ssh-troubleshooting
