..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


===================================
Improvements in deprecation process
===================================

https://blueprints.launchpad.net/heat/+spec/deprecating-improvements

These changes should make deprecation process obvious and safe for users.

Problem description
===================

Current deprecation process contains some issues:
 - there is no clear information for all deprecated properties and
   attributes, when each one was deprecated and will be deleted.
 - there are no notes about how and when we plan to remove support for option.
 - undeletable code in property/attribute schemas.
 - backward compatibility with old templates.

Proposed change
===============

Suggested changes should solve issues mentioned above:

 1. Need to add new page in Heat documentation with detailed description of
    deprecation process.
    Add new page in Heat documentation to Developers Documentation section
    named 'Heat support status usage' with description of using support status
    for resources, properties and attributes:
    - how long legacy option will be available
    - what will happen, when deprecation period is over
    - how to use support_status for properties, attributes and resources
    - what will happen with deprecated resources
    Also, add information about support_status parameter in Heat Resource
    Plug-in Development Guide page.

 2. Improve SupportStatus.
    Add to SupportStatus `previous_status` option for displaying previous
    status of object and it's version::

     support_status=support.SupportStatus(
         status=support.DEPRECATED,
         version='2015.2',
         previous_status=support.SupportStatus(version='2014.1')
     )

    Also, add HIDDEN status for DEPRECATED objects, which become absolutely
    obsolete. Objects with this status will be hidden from documentation and
    resource-type-list.

 3. Improvement in documentation status code.
    Improve generating documentation for new SupportStatus option
    `previous_status`. Documentation must show full life cycle of resource.

Besides that, next features can be implemented:

 1. Add option in attribute/property schema, which shows legacy names::

     property_schema = {
         subnet:
             ....
             legacy_names: [subnet_id]
     }

 2. Add migration mechanism, which allows to support two following cases:
    - New stacks deployed from old templates continue to work during
    the period the element is in the deprecated state.
    - Old stacks are correctly interpreted by new code after the element
    was deprecated.
    - When deprecation period ends, templates should be updated, otherwise
    Validation Error will be raised. Old created stacks will be available, but
    can not be updated with old templates. For comfortable work will be
    recommended to update old stacks with new templates.

Alternatives
------------

Optionally we may add an API which updates old template and returns user new
updated template or information about which option should be changed.

Note, that it doesn't make sense if we start returning validation error on old
templates.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <prazumovsky>

Assisted by:
  <skraynev>

Milestones
----------

Target Milestone for completion:
  Liberty-1

Work Items
----------

* Add section in documentation about how we deprecate options.
* Add status HIDDEN to SupportStatus and improve documentation generating.
* Add parameter previous_status and improve SupportStatuses for heat objects.
* Add option "legacy_names" for property schema.
* Create auto-upgrade mechanism for old templates.


Dependencies
============

None
