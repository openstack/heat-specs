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

============================================
Display more user information in stack lists
============================================

https://blueprints.launchpad.net/heat/+spec/stack-display-fields


Stacks are launched by users but scoped to tenants, so users in the same tenant
currently have no way to know who stacks belong to.  The same is especially
true to unscoped stack lists.  Since humans are much better with names than
they are with numbers, it would be great if this list also contained other
information to allow for better identification of stack owners.


Problem description
===================

There is currently no way to know what user created a stack, since only the
tenant ID is displayed with a stack and multiple users can be in the same
tenant.

Also, when listing unscoped stacks (with the flag ``global_tenant=True``), all
stacks are returned, regardless of the tenant who owns them.  This list
contains information about the stacks, including some info about the stack
owner (e.g. the Tenant ID is included, but usernames are not).

This is helpful for cloud providers to be able to more easily support their
customers.  However, humans are better at dealing with names than with numbers,
so returning just the Tenant ID is not ideal.

In order to make it possible for supporters to easily identify their clients,
it would be great to also include the username of the stack owners in the stack
information.


Proposed change
===============

The proposed implementation would add the extra information when formatting a
stack.

Currently, the username is already saved to the database but not parsed back
into the stack when loaded from the DB.  This would parse it back from the DB
into the stack at all times, but only exposed to the API response when
formatting stacks to a ``global_tenant`` call::

  {
    "stacks": [
      {
        "creation_time": "...",
        "description": "...",
        "id": "...",
        "links": [...],
        "project": "TENANT_ID",
        "stack_owner": "USERNAME",    // Additional info
        "stack_owner_id": "USER_ID",  // ----------------
        "stack_name": "...",
        "stack_status": "...",
        "stack_status_reason": "...",
        "updated_time": "..."
      }
    ]
  }

The necessary changes will primarily reside in:

* heat.api.openstack.v1.views.stacks_view.py
* heat.engine.api.py
* heat.engine.parser.py
* heat.engine.service.py
* heat.rpc.api.py


Alternatives
------------

None, since this is just field additions.


Implementation
==============

Assignee(s)
-----------

Primary assignees:

* rblee88
* andersonvom


Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* Read username into the Stack back from the DB
* Display username when displaying stacks


Dependencies
============

None
