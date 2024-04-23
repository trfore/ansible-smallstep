# Ansible Role: step_cli

- Install step CLI, `step-cli`, for managing step CA servers and clients.
- Installs the binary at the default path, `/usr/bin/step-cli`.

## Role Variables

| Variable            | Default | Description                                                                             | Required |
| ------------------- | ------- | --------------------------------------------------------------------------------------- | -------- |
| `step_cli_checksum` | URL     | URL to `step-cli` package checksum. If empty, the checksum is skipped.                  | No       |
| `step_cli_pkg_src`  | URL     | URL to `step-cli` package. Can be overridden in playbook when using a proxy.            | No       |
| `step_cli_version`  | latest  | String, SemVer of `step-cli` to install, e.g. `0.15.7`, defaults to the latest version. | No       |

## Example Playbooks

```yaml
---
- hosts: servers
  become: true
  gather_facts: true
  roles:
    - name: Install Step CLI
      role: trfore.smallstep.step_cli
```

### Using a Package Proxy

```yaml
---
- hosts: servers
  become: true
  gather_facts: true
  roles:
    - name: Install Step CLI
      role: trfore.smallstep.step_cli
      vars:
        step_cli_pkg_src: "https://PROXY_URL/step-cli_x.x.x_amd64.deb" # Proxy URL
        step_cli_checksum: "" # Skip checksum
```

## References

- https://github.com/smallstep/cli
