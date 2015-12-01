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

============================
Support for pre-delete hooks
============================

https://blueprints.launchpad.net/heat/+spec/pre-delete-hook

Adds a new type of hook which is triggered before resource deletion.


Problem description
===================

We provide hooks for pre-create and pre-update, but not for pre-delete. Such a
hook would allow users to make specific actions when a resource is deleted,
like deregistration with external systems, and will provide the ability to
validate deletion of critical elements.


Proposed change
===============

The hook will be mirrored strictly on pre-create, such as it's called only on
resource deletion and not resource replacement. This part will be handled in a
future spec.

This will look like this::

  resource_registry:
    resources:
      my_server:
        hooks: pre-delete
      my_database:
        hooks: [pre-create, pre-delete]

Alternatives
------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  therve

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

* Add the new hook in the environment and add the appropriate breakpoint in
  resource deletion


Dependencies
============

None
