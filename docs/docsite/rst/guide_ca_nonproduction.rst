.. _ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction:

Setup a Step CA Server (Non-Production)
============================================

- This guide will demonstrate how to setup a Smallstep CA server. Configuration and certificates files are stored on the local disk at ``/etc/step-ca/``, this path is assigned using the ``step_ca_path`` variable.
- These values are for non-production use only, as it will perform the following:

  - Store ``root_ca.crt`` private key on the local disk at ``/etc/step-ca/secrets/root_ca_key``.
  - Creates two password files, ``/etc/step-ca/password.txt`` and ``/etc/step-ca/password-provisioner.txt``, that are read-write only by the system-user ``step``.

- Sensitive values are masked from ansible log, however, it is important to store these values using a form of encryption, e.g. ``ansible-vault``.
- Two configurations are presented, if you would like to issue SSH certificates skip to the next section: :ref:`ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction.ssh`.

  - A complete playbook file is available at `non-production.yml (link) <https://github.com/trfore/ansible-smallstep/blob/main/playbooks/non-production.yml>`_ with example `group_vars (link) <https://github.com/trfore/ansible-smallstep/tree/main/playbooks/group_vars>`_.

CA Server (x509 Certificates)
-----------------------------

Variable Files
^^^^^^^^^^^^^^

Create a ``group_vars/ca_server/vars/ca-vars.yml`` file.

.. code-block:: yaml+jinja

    step_ca_initialize: true
    step_ca_enable_service: true
    step_ca_name: "Example.com CA"
    step_ca_password: "{{ vault_step_ca_password }}"
    step_ca_provisioner_password: "{{ vault_step_ca_provisioner_password }}"

Create a ``group_vars/ca_server/vars/ca-provisioners.yml`` file.

.. code-block:: yaml+jinja

    step_provisioner:
      - name: "acme"
          type: "acme"
          renewal_after_expiry: true
          x509_default_dur: "48h"
          x509_max_dur: "168h"

Create a ``group_vars/ca_server/vault/vault.yml`` file and encrypt it.

.. code-block:: yaml+jinja

    vault_step_ca_password: "password01"
    vault_step_ca_provisioner_password: "password02"

.. code-block:: shell

    $ ansible-vault encrypt vars/vault.yml

Playbook
^^^^^^^^

Create a ``ca-server.yml`` playbook and run it.

.. code-block:: yaml+jinja

    - name: Setup Step CA Server
      hosts: ca-server
      become: true
      gather_facts: true
      vars_files:
        - ca-vars.yml
        - ca-provisioners.yml
      roles:
        - name: Install Step Certificates
          role: trfore.smallstep.step_ca

        - name: Add Smallstep Provisioner
          role: trfore.smallstep.step_provisioner

.. code-block:: shell

    $ ansible-playbook ca-server.yml --vault-password-file ~/.ansible_vault_key

CA Directory Layout
^^^^^^^^^^^^^^^^^^^

- The following files will be created:

.. code-block:: shell

    /etc/step-ca
    |-- certs
    |   |-- intermediate_ca.crt
    |   `-- root_ca.crt
    |-- config
    |   |-- ca.json
    |   `-- defaults.json
    |-- db
    |   |-- 000000.vlog
    |   |-- KEYREGISTRY
    |   |-- LOCK
    |   `-- MANIFEST
    |-- password-provisioner.txt
    |-- password.txt
    |-- secrets
    |   |-- intermediate_ca_key
    |   `-- root_ca_key
    `-- templates

.. _ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction.ssh:

CA Server (x509 and SSH Certificates)
-------------------------------------

- For OIDC, configure external the identity provider. See links below: :ref:`ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction.oauth2`.

Variable Files
^^^^^^^^^^^^^^

Create a ``group_vars/ca_server/vars/ca-vars.yml`` file.

.. code-block:: yaml+jinja

    step_ca_initialize: true
    step_ca_enable_service: true
    step_ca_name: "Example.com CA"
    step_ca_password: "{{ vault_step_ca_password }}"
    step_ca_provisioner_password: "{{ vault_step_ca_provisioner_password }}"
    step_ca_ssh_mgmt: true

Create a ``group_vars/ca_server/vars/ca-provisioners.yml`` file.

.. code-block:: yaml+jinja

    step_provisioner:
      - name: "acme"
          type: "acme"
          renewal_after_expiry: true
          x509_default_dur: "48h"
          x509_max_dur: "168h"
      - name: "google"
          type: "oidc"
          ssh: true
          client_id: "{{ vault_oidc_client_id }}"         # From GCP API Config
          client_secret: "{{ vault_oidc_client_secret }}" # From GCP API Config
          config_endpoint: "https://accounts.google.com/.well-known/openid-configuration"
          domain: "gmail.com"
      - name: "sshpop"
          type: "sshpop"
          ssh: true

Create a ``group_vars/ca_server/vault/vault.yml`` file and encrypt it.

.. code-block:: yaml+jinja

    vault_step_ca_password: "password01"
    vault_step_ca_provisioner_password: "password02"
    vault_oidc_client_id: "123"     # From GCP API Config
    vault_oidc_client_secret: "456" # From GCP API Config

.. code-block:: shell

    $ ansible-vault encrypt vars/vault.yml

Playbook
^^^^^^^^

Create a ``ca-server.yml`` playbook and run it.

.. code-block:: yaml+jinja

    - name: Setup Step CA Server
      hosts: ca-server
      become: true
      gather_facts: true
      vars_files:
        - ca-vars.yml
        - ca-provisioners.yml
      roles:
        - name: Install Step Certificates
          role: trfore.smallstep.step_ca

        - name: Add Smallstep Provisioner
          role: trfore.smallstep.step_provisioner

.. code-block:: shell

    $ ansible-playbook ca-server.yml --vault-password-file ~/.ansible_vault_key

CA Directory Layout
^^^^^^^^^^^^^^^^^^^

- The following files will be created:

.. code-block:: shell

    /etc/step-ca/
    |-- certs
    |   |-- intermediate_ca.crt
    |   |-- root_ca.crt
    |   |-- ssh_host_ca_key.pub
    |   `-- ssh_user_ca_key.pub
    |-- config
    |   |-- ca.json
    |   `-- defaults.json
    |-- db
    |   |-- 000000.vlog
    |   |-- KEYREGISTRY
    |   |-- LOCK
    |   `-- MANIFEST
    |-- password-provisioner.txt
    |-- password.txt
    |-- secrets
    |   |-- intermediate_ca_key
    |   |-- root_ca_key
    |   |-- ssh_host_ca_key
    |   `-- ssh_user_ca_key
    `-- templates
        `-- ssh
            |-- ca.tpl
            |-- config.tpl
            |-- known_hosts.tpl
            |-- sshd_config.tpl
            |-- step_config.tpl
            `-- step_includes.tpl

Additional Guides and References
--------------------------------

- :ref:`ansible_collections.trfore.smallstep.docsite.guide_client`
- `GitHub: Example playbooks and group_vars <https://github.com/trfore/ansible-smallstep/blob/main/playbooks/>`_

.. _ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction.oauth2:

OAuth2 Credentials
^^^^^^^^^^^^^^^^^^

- `Google Workspace Docs: Create Access Credentials <https://developers.google.com/workspace/guides/create-credentials>`_
- `GitHub Docs: Authorizing OAuth apps <https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps>`_
- For a general list of OAuth IdP configurations, see `OAuth2 Proxy Docs (link) <https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/>`_.
