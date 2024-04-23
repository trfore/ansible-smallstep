=========================================
trfore.smallstep Collection Release Notes
=========================================

.. contents:: Topics

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