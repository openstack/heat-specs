..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..
 This template should be in ReSTructured text. The filename in the git
 repository should match the launchpad URL, for example a URL of
 https://blueprints.launchpad.net/heat/+spec/awesome-thing should be named
 awesome-thing.rst .  Please do not delete any of the sections in this
 template.  If you have nothing to say for a whole section, just write: None
 For help with syntax, see http://sphinx-doc.org/rest.html
 To test out your formatting, see http://www.tele3.cz/jbar/rest/rest.html

===========================
 Digest Intrinsic Function
===========================

https://blueprints.launchpad.net/heat/+spec/digest-intrinsic-function

It would be useful to the user to have intrinsic functions to perform digest
operations such as MD5 or SHA-512.

Problem description
===================

Certain applications require the user to provide information in a hashed format
(e.g. Chef user resources only take hashed passwords), so it would be useful to
the user to be able to use an intrinsic function to do it for them.

Proposed change
===============

Add another class to run existing digest algorithms (e.g. MD5, SHA-512, etc) on
user provided data and expose it in the HOT functions list.  The class would
take the name of the digest algortihm and the value to be hashed.

Python's ``hashlib`` natively supports md5, sha1 and sha2 (sha224, 256, 384,
512) on most platforms and this will be documented as being the supported list
of algorithms. But the cloud provider may go beyond and support more algortihms
as well, since, depending on the way Python was built, ``hashlib`` can also use
algorithms supported by OpenSSL.


Examples:

::
    # raw string
    gravatar: { digest: ['md5', 'sample@example.com'] }

    # from a user supplied parameter
    pwd_hash: { digest: ['sha512', { get_param: raw_password }] }

Alternatives
------------

There's really no good alternative other than an intrinsic function for this.

Implementation
==============

Assignee(s)
-----------

andersonvom

Milestones
----------

Target Milestone for completion:
  Kilo-2

Work Items
----------

- Add class to perform digest operations;

- Expose new class to HOT templates;

- Update the docs;


Dependencies
============

None.
