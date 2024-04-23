.. _ansible_collections.trfore.smallstep.docsite.guide_ssh:

Setup Servers and User Machines to Use SSH Certificates
=======================================================

- This guide will demonstrate how to setup a server and client machine to use SSH certificates to authenticate remote connections. It assumes the following:

  - A CA is already configured to issue SSH certificates, and has a JWK, OIDC and SSHPOP provider configured. For instructions see: :ref:`ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction.ssh`.
  - The root CA certificate fingerprint is known, i.e. on the CA server run ``step certificate fingerprint /etc/step-ca/certs/root_ca.crt``.

- Both the server and user machine will need to trust the central CA server then request:

  - A **host** certificate for server.
  - A **user** certificate for the user machine.

- Currently, the ``step_ssh`` role supports request authentication using the JWK provisioner for **host** certificates. And its recommended to use an **OIDC** provisioner for **user certs** (see below).

Configure Servers to Use SSH Certificates
-----------------------------------------

- To configure a server to use SSH certificate the following playbook will:

  - Use the default JWK provider to request a SSH host certificate.
  - Use the SSHPOP provider for SSH host certificate renewal.

- This is a minimal playbook that demonstrates the server using SSH certificates without requesting x509 certs. To also request x509 certs see: `non-production.yml (link) <https://github.com/trfore/ansible-smallstep/blob/main/playbooks/non-production.yml>`_.

Playbook
^^^^^^^^

.. code-block:: yaml+jinja

    - name: Setup Step CA Clients (Servers)
      hosts: ca_clients
      become: true
      gather_facts: true
      roles:
        - name: Add Step CA Root Certificate to Trust Store
          role: trfore.smallstep.step_ca_cert
          vars:
            step_ca_fingerprint: "CA_FINGERPRINT"
            step_ca_url: "CA_URL" # https://ca.example.com

        - name: Configure Host for SSH Certificates
          role: trfore.smallstep.step_ssh
          vars:
            step_ssh_provisioner: "Example.com" # JWK provisioner
            step_ssh_provisioner_password: "password02" # JWK provisioner password

Step CA Directory Layout
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

    /etc/step-ca/
    |-- certs
    |   |-- root_ca.crt
    |   `-- ssh_user_key.pub
    `-- config
        `-- defaults.json


Configure User Machine for SSH User Certificate
-----------------------------------------------

- This section assumes the following:

  - User is a authorized on the server and their ``USERNAME`` matches one of the principals in the SSH certificate, see below: :ref:`ansible_collections.trfore.smallstep.docsite.guide_ssh.oidc`.

- To configure a user machine to use SSH certificate do the following:

1. Download and Add CA Certificate to Trust Store
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Bootstrap the machine to download root CA certificate and create a step configuration file at ``/home/USER/.step``.

.. code-block:: shell

    # download root CA cert and create step configuration
    $ step ca bootstrap --ca-url [CA_URL] --fingerprint [CA_FINGERPRINT]
    # add root CA cert to trust store, e.g. /etc/ssl/certs
    $ step certificate install $(step path)/certs/root_ca.crt

2. Request SSH User Certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Request a user certificate using a OIDC (recommended) or JWK provisioner:

  - For OIDC, the user will be redirected to the OAuth2 identity provider.
  - For a JWK provisioner, the user will need a token. Note: The default JWK token should only be used in testing, as it provides full access to the CA. Additionally, providing short-lived encrypted single-use tokens is beyond the scope of the role and collection.

.. code-block:: shell

    # OIDC
    $ step ssh login USERNAME@example.com --provisioner "google"
    # JWK
    $ step ssh login USERNAME --provisioner "JWK_NAME"

3. Configure User's SSH client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

    $ step ssh config

4. Test the Connection
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

    $ ssh USERNAME@server01.example.com

- Optional, add SSH options and host server ``USERNAME`` to ``~/.ssh/config``.

.. code-block:: shell

    Host server01.example.com
        User USERNAME
        ControlMaster auto
        ControlPath ~/.ssh/control-%r@%h:%p
        ControlPersist 15s

Directory Layout
^^^^^^^^^^^^^^^^

- Step Directory

.. code-block:: shell

    /home/USER/.step/
    ├── certs
    │   └── root_ca.crt
    ├── config
    │   └── defaults.json
    └── ssh
        ├── config
        ├── includes
        └── known_hosts

- Also creates the following files:

  - ``/usr/local/share/ca-certificates/Example_Root_CA_*.crt``
  - ``/etc/ssl/certs/Example_Root_CA_*.pem``

Principals
----------

.. _ansible_collections.trfore.smallstep.docsite.guide_ssh.oidc:

OIDC Provisioner: Email Addresses With Special Characters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- If an email contains periods, for example ``jordan.doe@example.com``. Step will create multiple principles from the email address - ``jordandoe``, ``jordan.doe`` and ``jordan.doe@example.com``.
- Additionally the default ``USER`` will be ``jordandoe`` in ``~/.step/ssh/config``.

.. code-block:: shell

    $ step ssh login jordan.doe@example.com --provisioner "google"
    $ step ssh list --raw | grep jordan.doe@example.com | step ssh inspect
            Type: ecdsa-sha2-nistp256-cert-v01@openssh.com user certificate
            ...
            Key ID: "jordan.doe@example.com"
            ...
            Principals:
                    jordandoe
                    jordan.doe
                    jordan.doe@example.com

Additional Guides and References
--------------------------------

- :ref:`ansible_collections.trfore.smallstep.docsite.guide_ca_nonproduction`
- :ref:`ansible_collections.trfore.smallstep.docsite.guide_client`
- `GitHub: Example playbooks and group_vars <https://github.com/trfore/ansible-smallstep/blob/main/playbooks/>`_

.. _ansible_collections.trfore.smallstep.docsite.guide_ssh.oauth2:

OAuth2 Credentials
^^^^^^^^^^^^^^^^^^

- `Google Workspace Docs: Create Access Credentials <https://developers.google.com/workspace/guides/create-credentials>`_
- `GitHub Docs: Authorizing OAuth apps <https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps>`_
- For a general list of OAuth provider configuration, see `OAuth2 Proxy Docs (link) <https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/>`_.
