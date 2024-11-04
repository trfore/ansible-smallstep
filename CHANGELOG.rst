=========================================
trfore.smallstep Collection Release Notes
=========================================

.. contents:: Topics

v1.2.0
======

Release Summary
---------------

Fix installing Smallstep CLI > 0.27.2, add testing for Ansible 2.17, and remove testing/support for CentOS 8

Breaking Changes / Porting Guide
--------------------------------

- Remove testing support for CentOS 8 due to EOL.

Bugfixes
--------

- Pulling the latest smallstep CLI package, due to the GitHub tag not aligning with the package name.

v1.1.2
======

Release Summary
---------------

Improve development workflow with format/lint configs and GH workflows

v1.1.1
======

Release Summary
---------------

Adds files to improve development workflow; validates collection against step-ca & cli `0.26.1`

v1.1.0
======

Release Summary
---------------

New feature, request SSH certificates from step CA.

Major Changes
-------------

- Added SSH role for generating SSH certificates.
- Added support for CentOS 8-9 and Debian 10-12.

New Roles
---------

- trfore.smallstep.step_ssh - Request SSH Certificates from step CA Server

v1.0.0
======

Release Summary
---------------

Initial collection release, deploy a PKI using Smallstep.

Major Changes
-------------

- Consolidated numerous step roles into a single collection.

New Roles
---------

- trfore.smallstep.step_ca - Install and Initialize Step CA
- trfore.smallstep.step_ca_cert - Download and add the CA root certificate to trust stores
- trfore.smallstep.step_cert - Request an x509 certificate from the CA and automatically renew it
- trfore.smallstep.step_cli - Install Step CLI
- trfore.smallstep.step_provisioner - Add provisioners to Step CA
