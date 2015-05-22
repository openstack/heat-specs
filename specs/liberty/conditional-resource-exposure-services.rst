..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================================
Conditionally expose resources based on available services
==========================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/keystone-based-resource-availability

Expose resources as available based on presence of the service.

Problem description
===================

Currently we unconditionally register and present to the user all resource
plugins that we have in-tree, even though the actual service might not be
installed in a particular cloud (e.g. Neutron resources on Nova-network
based cloud or Sahara resources though Sahara is not that usually installed).
This is confusing to the user as (s)he sees resources that can not actually
be used as available, and facilitates late failure of instantiated template
instead of failing at validation.

The situation is only going to get worse as we move the contrib/ resources
back in-tree, and we will probably accept in-tree resources for many more
projects under the "Big Tent" governance model.

Proposed change
===============

Add an additional validation step in the resource class that checks
if the required endpoint is present.
Endpoints can be accessed from the request context that is already available
in the resource class as ``stack.context``.
This method should be called from ``Resource.__new__`` and raise
a ``StackResourceUnavailable`` exception
(new subclass of ``StackValidationError``) when appropriate.

The ``list_resource_types`` method should tolerate the
``StackResourceUnavailable`` and do not output resources raising this as part
of available resources list.

Client plugins must implement a ``service_type`` property to be used during
validation and also during client instantiation.

Every resource type must implement the ``default_client_plugin``
class attribute to be used in the base ``Resource`` class to validate
the endpoints presence in the context.

Alternatives
------------

Keep the things as they are continuing to confuse users and fail later than
earlier for templates with resources for services unavailable
in the current deployment.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Kanagaraj Manickam <kanagaraj-manickam>

Assisted by:
  Pavlo Shchelokovskyy <pshchelo>

Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

- changes in the client plugins
- add ``default_client_plugin`` to all resource plugins
- changes in the base resource class
- changes in the ``list_resource_types`` and ``show_resource_type`` service
  methods
- unit tests
- scenario integration tests (based on some "exotic" resource)
  - check if resource is listed as available
  - check if template with resource validates

Dependencies
============

None
