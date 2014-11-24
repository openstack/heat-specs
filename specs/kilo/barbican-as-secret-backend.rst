..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


================================
Using Barbican as secret backend
================================

https://blueprints.launchpad.net/heat/+spec/barbican-as-secret-backend

We store some secret data in the Heat database using a simple symmetric
encryption with a static key. To improve security of the storage, we should
optionally support using Barbican to store those secrets.


Problem description
===================

Heat uses a simple encrypt mechanism to store secret data in its database, with
the key specified in the configuration. While it provides some security, a
compromised Heat node will give the attacker access to all the users' secrets.


Proposed change
===============

Add a new flag to the Heat configuration specifying that Barbican must be used
for storing secret. When set, Heat will query the service catalog for the
Barbican service, and will store the secrets in the user project, with
predictable prefixes.

We already support 2 different methods of decryption, 'heat' being the legacy
one, and 'oslo_v1' being the current version. Current values encrypted using
those methods will keep getting decrypted the same way. When we use Barbican,
the encryption method will be set to 'barbican_v1' and the value will be the
reference of the secret.

It should require a refactoring, as data encryption is today managed at the
SQLAlchemy data layer, whereas it may be easier to manage it above, especially
as we need user credentials to talk to Barbican.


Alternatives
------------

There seems to be an effort to create a key management shim that may use local
secure storage as an option. We may want to wait for that effort.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  therve


Milestones
----------

Target Milestone for completion:
  Kilo-2

Work Items
----------

* Extract encryption management from the SQLAlchemy layer
* Move Barbican client out of contrib
* Add a configuration option to send secrets to the Barbican service


Dependencies
============

None
