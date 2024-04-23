.. _ansible_collections.trfore.smallstep.docsite.guide_client:

Setup a Step Client (Machine / Server)
===========================================

- This guide will demonstrate how to setup servers to request x509 certificates from the CA.

  - A complete playbook file is available at `clients-server.yml (link) <https://github.com/trfore/ansible-smallstep/blob/main/playbooks/clients-server.yml>`_ with example `group_vars (link) <https://github.com/trfore/ansible-smallstep/tree/main/playbooks/group_vars>`_.

- The ``step_ca_cert`` and ``step_cert`` roles will do the following:

  - Download the CA root certificate and add it to the system's CA trust store.
  - Request an x509 certificate from the CA using an ACME provisioner (default) - configure using the ``step_cert_list.provisioner`` variable.
  - The certificate will automatically renew via a systemd timer, ``cert-renewer@[step_cert_list.name].timer``.
  - The systemd renewal timer will attempt to restart the service that matches the ``step_cert_list.name``; thus, it is **important to name the certificate after the service**, e.g. set ``step_cert_list.name: docker`` for the ``docker.service``. You can disable this behavior globally by setting ``step_cert_renewal_restart_svc: false``.

- This guide assumes a CA is already configured with a ACME provisioner using: :ref:`ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction`.

Single Certificate
------------------

- This approach works well for a group of servers in which you only need a single certificate matching the FQDN of the server.

Playbook
^^^^^^^^

.. code-block:: yaml+jinja

    - name: Extract Root CA Information
      hosts: ca-server
      become: true
      gather_facts: true
      tasks:
        - name: Get Root CA Fingerprint
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

        - name: Add Step CA Root Certificate to Trust Store
          role: trfore.smallstep.step_ca_cert
          vars:
            step_ca_fingerprint: "{{ hostvars['ca-server'].ca_fingerprint.stdout }}"
            step_ca_url: "https://ca.example.com"

        - name: Request x509 Certificate
          role: trfore.smallstep.step_cert

Multiple Certificates
---------------------

- This approach works well for a single server hosting multiple services.

Playbook
^^^^^^^^

.. code-block:: yaml+jinja

    - name: Extract Root CA Information
      hosts: ca-server
      become: true
      gather_facts: true
      tasks:
        - name: Get Root CA Fingerprint
          ansible.builtin.command: step certificate fingerprint /etc/step-ca/certs/root_ca.crt
          register: ca_fingerprint
          changed_when: false
          failed_when: ca_fingerprint.rc == 1

    - name: Setup Step CA Clients (Servers)
      hosts: host01
      become: true
      gather_facts: true
      roles:
        - name: Install Step CLI
          role: trfore.smallstep.step_cli

        - name: Add Step CA Root Certificate to Trust Store
          role: trfore.smallstep.step_ca_cert
          vars:
            step_ca_fingerprint: "{{ hostvars['ca-server'].ca_fingerprint.stdout }}"
            step_ca_url: "https://ca.example.com"

        - name: Request x509 Certificate
          role: trfore.smallstep.step_cert
          vars:
            step_cert_list:
              - name: "{{ ansible_fqdn }}"
                subject: "{{ ansible_fqdn }}"
                path: /etc/step/certs/
                san_0: "{{ ansible_default_ipv4.address }}" # Add IP address to certificate
                provisioner: "acme"
              - name: "docker" # Name matches service name
                subject: "docker.example.com"
                path: /etc/pki/docker.example.com/
                provisioner: "acme"

Directory Layout
^^^^^^^^^^^^^^^^

- The following files will be created:

.. code-block:: shell

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

- The following timers will be created:

.. code-block:: shell

    $ systemctl list-timers
    NEXT                        LEFT              LAST PASSED UNIT                                                 ACTIVATES
    Fri XXXX-XX-XX 17:46:10 UTC 1min 18s left     n/a  n/a    cert-renewer@docker.timer                           cert-renewer@docker.service
    Fri XXXX-XX-XX 17:48:04 UTC 3min 12s left     n/a  n/a    cert-renewer@host01.example.com.timer               cert-renewer@host01.example.com.service

Additional Guides and References
--------------------------------

- :ref:`ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction`
- `GitHub: Example playbooks and group_vars <https://github.com/trfore/ansible-smallstep/blob/main/playbooks/>`_
