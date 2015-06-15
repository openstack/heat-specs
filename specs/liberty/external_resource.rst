..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
 Add support for external resources.
====================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/external-resources


Problem description
===================

We have no way to instruct Heat to use an existing (external) physical
resource id.

Use case 1:
-----------
When running a stack over a period of time a user might find it necessary
to operate on a server (rebuild it) out of band. But that then left
it out of sync with Heat's perspective of it. So this is a mechanism
to tell Heat "this is the new resource id, and I am now taking control
of it". At some stage later (s)he might want to tell Heat to take control
of it again - by removing the "external_reference" section. This fills
TripleO's needs (and we assume many other users that have to operate
an important stack for an extended time) by allowing the
get_attr/get_resource to keep functioning when they are working on a
resource externally and for Heat to leave it alone. Then when the user
is happy with the state of it they can return it to Heat's control.

Use case 2:
-----------
There is an existing resource that we would like to use get_attr
on to retrieve useful information instead of doing this manually
and passing the info in via the Parameters.

In all these cases once this is done the resource can be marked
as external and any update or delete will be ignored (unless the user
removes the "external" information first).

Proposed change
===============

To achieve this the user would add the following to the template::

  resources:
    ...
    res_a:
      type: OS::Nova::Server
      external_id: the-server-id
      properties:
        ...


Note:
1. There is no place for "resource_data or Metadata" as these are
used by actions that once it becomes external are not possible. There
will be some resource types that will not survive going from external
to normal resources because of the missing resource data/metadata.
This will be documented as best as possible, and the use of
resource_data should be discouraged by Heat developers.

2. Once the resource has the "external_id" attribute present the properties
will be ignored (but be allowed to be present). If the "external_id"
is then removed the resource will be updated with the properties.


Creating a resource with external_id.
-------------------------------------
This covers the second use case. Here we see that there is an
external_id and logically do an adopt and check (to make sure
the resource actually exists).


Updating a resource with external_id.
-------------------------------------
This covers the first use case. We overwrite the resource_id that Heat
has previously written and ignore all the properties. Check will also
be called here to make sure the resource exists. If the external_id is
different to the existing physical_resource_id then the existing one
will be deleted.


Removing the external_id.
-------------------------
To convert the resource into a "normal" resource the user must
remove the "external_id" attribute from the resource and do
a stack update. If the resource requires some missing resource_data
or metadata that is missing (and can't be recovered) this will fail
and it will remain as external.


Deleting a stack with a resource that has external_reference.
-------------------------------------------------------------
When we have an external_reference, a deletion policy of RETAIN is
assumed (it will not be deleted).


Alternatives
------------

The user *could* use the current adopt/abandon mechanism, but it has
some slightly different behaviour. Also switching physical resource_id
is difficult with 2 API calls.


Implementation
==============


Assignee(s)
-----------

Primary assignee:
  asalkeld


Milestones
----------

Target Milestone for completion:
  Liberty-2

Work Items
----------

 * Code
 * Functional tests.
 * Documentation needs to be added to the template guide.
 * Document limitations (resources that require resource_data
   and metadata).

Dependencies
============

None
