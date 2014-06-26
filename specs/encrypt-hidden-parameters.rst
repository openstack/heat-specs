..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
 Hidden Parameters Encryption
=============================

https://blueprints.launchpad.net/heat/+spec/encrypt-hidden-parameters

Encrypt template parameters that were marked as hidden before storing them in
database.

Problem description
===================

Heat template parameters can be marked as hidden, but currently these values
are stored in database in plain text.

A template author currently marks a parameter as hidden so that it will not be
logged or displayed to the user in user interfaces.

The problem itself is that these are probably sensitive pieces of data and thus
it would provide some safety against a database attacker if they were encrypted
in the database.

Leaving sensitive customer data at rest unencrypted provides many more options
for that data to get in the wrong hands or be taken outside the company.  It is
quick and easy to do a MySQL dump if the DB linux system is compromised, which
has nothing to do with Heat having a vulnerability.  Encrypting the data helps
in case if a leak of arbitrary DB data does surface in Heat.

Proposed change
===============

* Provide a configuration option to enable/disable hidden parameter encryption.
  (Default is to disable parameter encryption)

* Encrypt parameters that were marked as hidden before storing Stack data in
  the database.

* Decrypt parameters as soon as the stack data is read from database and
  use decrypted parameters to create Stack object.

* This implementation uses same key and encryption mechanism that is currently
  being used for encrypting/decrypting user credentials, trust tokens, and
  resource data. (Encryption key is defined in Heat configuration file)

Alternatives
------------

* Instead of encrypting hidden parameters, we could encrypt all the parameters
  as a dictionary.

* Encrypt full disk where entire MySQL database is being stored or encrypt
  files where specific tables are stored.

* Another alternative is to use CryptDB:

  www.cs.berkeley.edu/~istoica/classes/cs294/11/papers/sosp2011-final53.pdf

* Integrate Barbican with Heat and use Barbican to store secrets.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  vijendar-komalla


Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* Modify Stack 'store' method to encrytpt parameters before storing in database

* Modify Stack 'load' method to decrypt parameters

* Create a migration script to encrypt parameters that are already stored

* Create a tool/script to change the encryption key and re-encrypting all the
  parameters

Dependencies
============

None
