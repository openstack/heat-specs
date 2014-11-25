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

==============================================================
Use oslo-versioned-objects to help with dealing with upgrades.
==============================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/versioned-objects


Problem description
===================
We are looking to improve the way we deal with versioning (of all sorts db/rpc/rest/templates/plugins).
Nova has come up with the idea of versioned objects, that Ironic has also now used.
This has now been proposed as an oslo library:  https://review.openstack.org/#/c/127532/

https://etherpad.openstack.org/p/kilo-crossproject-upgrades-and-versioning

Versioned-objects will help us deal with DB schema being at a
different version than the code expects. This will allow Heat to be
operated safely during upgrades.

Looking forward as we pass more and more data over RPC we can make use
of versioned-objects to ensure upgrades happen without spreading the
version dependant code across the code base.

Proposed change
===============

Since it will take some time before versioned-objects goes into the oslo
library, the plan is to get an early version of it for Heat and
transition to oslo-versioned-objects when it is ready.

Create a directory heat/objects/ that will contain wrapper objects that
are a layer above the db objects. This allows the remainder of Heat to
not having to worry about dealing with older DB objects.

Once the objects are in place the rest of the code will be changed to
use the versioned objects instead of the db_api directly. This can be
done object-by-object to avoid overly large changes.


Alternatives
------------


Data model impact
-----------------

None. The objects being introduced are not stored in the database. Instead,
these objects are a replacement for sqlalchemy objects that is being used to
represent stack, resource, etc throughout Heat internals.

Developer impact
----------------

It will take some time to convert heat internals over to the object
model, so the existing convention of direct database calls should be
accepted until all object models are in place.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Angus Salkeld <asalkeld@mirantis.com>
  <others are welcome to help out>

Milestones
----------

Target Milestone for completion:
  Kilo-2

Work Items
----------

* (If needed) Obtain an early version of oslo.versionedobjects.
* Implement the objects for each DB object type we have.
* Update code that uses the DB to use versioned-objects instead.
* Write some developer docs on how to deal with older schema.
* Transition to oslo-versioned-objects as soon as it is available.

Dependencies
============

* oslo-versioned-objects
