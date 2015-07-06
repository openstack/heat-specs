..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
Special form of get_attr which returns all attributes
=====================================================

https://blueprints.launchpad.net/heat/+spec/get-attr-all-attributes

Add new functionality for ``get_attr`` function which allows to return dict of
all attributes.

Problem description
===================

There are resources which have attribute *show* which returns result of command
:code:`<client> <resource name>-show`, but in some cases may be useful to get
dict of all resource's attributes, so there was decision to add some new
functionality for ``get_attr`` intrinsic function which allows to return dict
of all attributes.

Proposed change
===============

Add some special form of ``get_attr`` as next::

 { get_attr: [resource_name] }

with no extra arguments, which will returns dict of all attributes' outputs.

This behaviour of get_attr can be used only when the latest
heat_template_version is selected, so this case should be noted in the
documentation.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <prazumovsky>

Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

* Add new functionality to ``get_attr``
* Add note to documentation about new functionality of ``get_attr``


Dependencies
============

None
