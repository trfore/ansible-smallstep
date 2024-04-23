# Ansible Role: step_cert

- This role will request x509 certificates from the CA and automatically renew them.
- The default values will request a single certificate from the CA using an ACME provisioner using the host's FQDN.
- The renewal service is via systemd timers and the role will create two systemd templates, `cert-renewer@.service` and `cert-renewer@.timer`.
  - For each certificate, a timer is created `cert-renewer@[step_cert_list.name].timer`.
  - On the client server, view all timers with `$ systemctl list-timers | grep cert-renewer`.
- The systemd renewal timers will attempt to restart the service that matches the `step_cert_list.name`; thus, it is **important to name the certificate after the service**, e.g. set `step_cert_list.name: docker` for the `docker.service`.
  - You can disable this behavior globally by setting `step_cert_renewal_restart_svc: false`.

## Role Variables

| Variable                        | Default         | Description                                                                                                                                              | Required | In-line Var Equivalent |
| ------------------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------- |
| `step_ca_path`                  | `/etc/step-ca/` | Path, Step CA folder containing the CA configuration and root certificate.                                                                               | No       | `STEPPATH`             |
| `step_cert_renewal`             | `true`          | Boolean, Enable automatic renewal of certificate. Creates a systemd service and timer template, and configures `cert-renew@[step_cert_list.name].timer`. | No       |                        |
| `step_cert_renewal_restart_svc` | `true`          | Boolean, Attempt to restart the service that matches the certificate name, `step_cert_list.name`.                                                        | No       |                        |

### Variable: `step_cert_list`

- `step_cert_list` is intend to be a list of dictionaries.

```yaml default/main.yml
# default list
step_cert_list:
  - name: "{{ ansible_fqdn }}"
    subject: "{{ ansible_fqdn }}"
    path: /etc/step/certs/
    provisioner: "acme"
```

| Dictionary Key | Default            | Description                                                                                                                    | Required | In-line Var Equivalent |
| -------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------ | -------- | ---------------------- |
| `name`         | `ansible_fqdn`     | String, Name for the local files - certificate, key, and systemd timer.                                                        | No       |                        |
| `subject`      | `ansible_fqdn`     | String, Common name, DNS name, or IP address that will be set as the subject for the certificate, e.g. `client01.example.com`. | No       |                        |
| `path`         | `/etc/step/certs/` | Path, Folder to store x509 certificate.                                                                                        | No       |                        |
| `san_0`        | not defined        | String, Subject Alternative Name (SAN) for the x509 certificate, useful for setting the host IP in the x509 certificate.       | No       | `--san`                |
| `san_1`        | not defined        | String, Additional SAN for the x509 certificate.                                                                               | No       | `--san`                |
| `not_after`    | not defined        | String, 'Time' (RFC 3339) or 'Duration', i.e. `24h`. Note: This value cannot exceed the provisioners max duration.             | No       | `--not-after`          |
| `provisioner`  | `acme`             | String, Name of provisioner to use.                                                                                            | No       | `--provisioner`        |
| `token`        | not defined        | String, One-time token used to authenticate with the CA.                                                                       | No       | `--token`              |

## Dependencies

- `trfore.smallstep.step_cli`: Requesting an x509 certificate requires `step`(aka `step-cli`), and this role will install it if required.
- `trfore.smallstep.step_ca_cert`: The CA root certificate is required, this role will download the CA root certificate and add it to the system's trust store.

## Example Playbook

### Single Certificate

```yaml
- hosts: ca_clients
  become: true
  gather_facts: true
  roles:
    - name: Request x509 Certificate
      role: trfore.smallstep.step_cert
      vars:
        step_cert_list:
          - name: "{{ ansible_fqdn }}"
            subject: "{{ ansible_fqdn }}"
            path: /etc/step/certs/
            san_0: "{{ ansible_default_ipv4.address }}" # Add IP address to certificate
            provisioner: "acme"
```

### Multiple Certificates

- With `step_cert_renewal: true` (default), two renewal timers will be created

```yaml
- hosts: ca_clients
  become: true
  gather_facts: true
  roles:
    - name: Request x509 Certificate
      role: trfore.smallstep.step_cert
      vars:
        step_cert_list:
          - name: "{{ ansible_fqdn }}"
            subject: "{{ ansible_fqdn }}"
            path: /etc/step/certs/
            provisioner: "acme"
          - name: "docker" # Name matches service name
            subject: "docker.example.com"
            path: /etc/pki/docker.example.com/
            provisioner: "acme"
```

- The following files and timers will be created:

```sh
$ tree /etc/step
/etc/step/
`-- certs
    |-- host01.example.com.crt
    `-- host01.example.com.key

$ tree /etc/pki
/etc/pki
`-- docker.example.com
    |-- docker.crt
    `-- docker.key

$ systemctl list-timers
NEXT                        LEFT              LAST PASSED UNIT                                                 ACTIVATES
Fri XXXX-XX-XX 17:46:10 UTC 1min 18s left     n/a  n/a    cert-renewer@docker.timer                           cert-renewer@docker.service
Fri XXXX-XX-XX 17:48:04 UTC 3min 12s left     n/a  n/a    cert-renewer@host01.example.com.timer               cert-renewer@host01.example.com.service
```

## References

- https://smallstep.com/docs/step-ca/renewal/
- https://smallstep.com/docs/step-cli/reference/ca/certificate/#options
