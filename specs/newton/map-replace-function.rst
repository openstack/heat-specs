..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


=====================
Support YAQL function
=====================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/map-replace-function

This blueprint adds support for a new map_replace function.


Problem description
===================

Currently it's difficult to perform key/value replacements on mappings
(e.g json parameters).  There are ways (ab)using str_replace or yaql, but
there are problems with both approaches such as avoiding partial matches
in the case of str_replace, and raising a validation error for key/value
collisions in the case of either yaql or str_replace.

Proposed change
===============

This spec proposes to add a new function that can iterate over a mapping
and replace keys or values based on optional mappings for each::

  map_replace:
    - k1: v1
      k2: v2
    - keys:
        k1: K1
      values:
        v2: V2

In this case, the result will be evaluated to {'K1': 'v1', 'k2', 'V2'}

Validation checks will be added so that the replacement fails if key
collisions occur, e.g if replacing "k2" with "k1" above, the function
will fail because it's going to overwrite an existing key.


Alternatives
------------

I tried to do this in yaql, and after some ML help I got it to work::

     yaql:
        expression: let(root => $) -> dict($root.data.service.items().select(
                                           [$[0], $root.data.ip[$[1]]]))
        data:
          service: { get_param: ServiceNetMap }
          ip: {get_param: NetIpMap}

However this doesn't allow for raising an error when key collisions occur,
and the syntax is pretty hard to remember.


Implementation
==============

Implement a new function and tests.


Assignee(s)
-----------

Primary assignee:
  shardy


Milestones
----------

  newton-3

Work Items
----------

1. Implement map_replace intrinsic function.
2. Add related tests.
3. Add corresponding docs.
4. Add examples of usage to heat-templates.


Dependencies
============

None
