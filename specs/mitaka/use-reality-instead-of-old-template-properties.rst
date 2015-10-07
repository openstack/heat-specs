..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


================================================
Convergence: Use reality when updating resources
================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/get-reality-for-resources

Make Heat aware of reality and use the reality as basis for comparison
before updating the resource. This spec is proposal to add a
get_reality/collect_reality to resource class.


Problem description
===================

Due to external factors in cloud, a provisioned resource from stack may
diverge from its original state. Since heat is unaware of this change,
it cannot act on it to bring it to desired state. Also, when user tries
to update it, the resource might end-up in error state since it is not
aware of its state and cannot carry-out any corrective action. Heat needs
to detect the changes in reality and compare with the new properties and
update the resource.


Proposed change
===============

A solution discussed at L summit meet-up was to implement get_reality
and handle_get_reality. The idea is to get the resource properties from
the reality and compare it with the current properties from template +
environment, instead of comparing with old template. When a user issues
an update, the resource plugins get the current resource properties from
reality and compare with the current template. If there are any changes,
the resource is updated.

The enable observer config option should be used to decide whether to
get the reality before updating the resource. This feature is enabled
only when the option is set in config.

This is first part of convergence observer specification. The observer
will depend on get_reality and handle_get_reality APIs. The scope of
this change is limited to implementing mechanisms to find the changes
from reality and compare before updating a resource. The bigger effort
involves continuously monitoring the changes and continuously acting on
them.

The changes will mostly reside in heat resource class and plugins if
required.


Alternatives
------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  prazumovsky
  ananta


Milestones
----------

  mitaka-1

Work Items
----------

1. Implement get_reality/collect_reality in resource plugins. The
existing show_resource can be used to get the reality, in addition to
any other queries to reality.

2. Use the existing update/handle_update to take necessary action on
resource based on output of get_reality.


Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/flag-to-enable-observe-reality
