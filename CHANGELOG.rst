=========================================
trfore.smallstep Collection Release Notes
=========================================

.. contents:: Topics

v1.2.4
======

Release Summary
---------------

Fix issues setting certificate valid periods

Minor Changes
-------------

- extend test coverage for var options in 'step_certs' and 'step_provisioner' (https://github.com/trfore/ansible-smallstep/pull/53).

Bugfixes
--------

- Add missing 'x509_max_dur variable' in the 'step_provisioner' task (https://github.com/trfore/ansible-smallstep/pull/51).
- Fix 'not-after' variable, works as expected for the 'step_certs' task (https://github.com/trfore/ansible-smallstep/pull/50).

Known Issues
------------

- The collection can fail to pull the latest step-ca and step-cli versions from GitHub when use in large deployments or during repetitive testing. This is due to hitting GitHub's API rate limiter (60 unauthenticated request per hour), we recommend setting 'step_ca_version' and 'step_cli_version' (https://github.com/trfore/ansible-smallstep/issues/42#issuecomment-3075048226).

v1.2.3
======

Release Summary
---------------

Allow for blank spaces in the CA name

Minor Changes
-------------

- add test for CA names with spacing (https://github.com/trfore/ansible-smallstep/pull/46).

Bugfixes
--------

- quote CA name to handle spaces in step_ca init (https://github.com/trfore/ansible-smallstep/pull/45).
- update SSH task to accept spacing in provisioner name (https://github.com/trfore/ansible-smallstep/pull/47).

Known Issues
------------

- The collection can fail to pull the latest step-ca and step-cli versions from GitHub when use in large deployments or during repetitive testing. This is due to hitting GitHub's API rate limiter (60 unauthenticated request per hour), we recommend setting 'step_ca_version' and 'step_cli_version' (https://github.com/trfore/ansible-smallstep/issues/42#issuecomment-3075048226).

v1.2.2
======

Release Summary
---------------

Add testing for Ansible 2.18, and remove testing/support for Ubuntu 20.04

Minor Changes
-------------

- Pin Ansible python packages 'ansible-compat' and 'molecule', see issue 30.
- Update tox test matrix to test Ansible 2.18.

Breaking Changes / Porting Guide
--------------------------------

- Remove testing support for Ubuntu 20 as it approaches EOL on 31 May 2025.

Bugfixes
--------

- Align tox dependencies with dev-requirements file to keep local molecule calls and tox testing at parity.

Known Issues
------------

- The collection can fail to pull the latest step-ca and step-cli versions from GitHub when use in large deployments or during repetitive testing. This is due to hitting GitHub's API rate limiter (60 unauthenticated request per hour), we recommend setting 'step_ca_version' and 'step_cli_version' (https://github.com/trfore/ansible-smallstep/issues/42#issuecomment-3075048226).

v1.2.1
======

Release Summary
---------------

Fix installing Smallstep CA > 0.28.0

Bugfixes
--------

- Pulls the correct smallstep CA package for versions 0.28+, see issue 25

v1.2.0
======

Release Summary
---------------

Fix installing Smallstep CLI > 0.27.2, add testing for Ansible 2.17, and remove testing/support for CentOS 8

Breaking Changes / Porting Guide
--------------------------------

- Remove testing support for CentOS 8 due to EOL.
- Remove testing support for Debian 10 due to EOL.

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
