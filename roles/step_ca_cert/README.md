# Ansible Role: step_ca_cert

- This role will download and add the CA root certificate into the system's trust store. Optionally, add it to Firefox and Java's trust stores.

## Role Variables

| Variable               | Default         | Description                                                                | Required | In-line Var Equivalent |
| ---------------------- | --------------- | -------------------------------------------------------------------------- | -------- | ---------------------- |
| `step_ca_fingerprint`  | not defined     | String, Fingerprint of the CA root certificate.                            | Yes      | `--fingerprint`        |
| `step_ca_url`          | not defined     | String, URI of the step CA.                                                | Yes      | `--ca-url`             |
| `step_ca_path`         | `/etc/step-ca/` | Path, Step CA folder containing the CA configuration and root certificate. | No       | `STEPPATH`             |
| `step_ca_cert_firefox` | `false`         | Boolean, Add CA root certificate to the Firefox NSS security database.     | No       | `--firefox`            |
| `step_ca_cert_java`    | `false`         | Boolean, Add CA root certificate to the Java key store.                    | No       | `--java`               |

## Dependencies

- `trfore.smallstep.step_cli`: Bootstrapping the CA root certificate requires `step`(aka `step-cli`), and this role will install it if required.

## Example Playbook

```yaml
- hosts: ca_clients
  become: true
  gather_facts: true
  roles:
    - name: Bootstrap CA Root Certificate
      role: trfore.smallstep.step_ca_cert
      vars:
        step_ca_fingerprint: "" # CA root certificate fingerprint
        step_ca_url: "https://ca.example.com"
```

## References

- https://smallstep.com/docs/step-cli/reference/ca/bootstrap/
- https://smallstep.com/docs/step-cli/reference/certificate/install/
