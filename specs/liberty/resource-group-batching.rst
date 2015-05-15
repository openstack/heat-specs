..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================================
Implement batch create and update for resource group
====================================================

https://blueprints.launchpad.net/heat/+spec/resource-group-batching

Add possibility to create and update resources in batches

Problem description
===================

Heat doesn't allow to create resources in batches which can lead
to unnecessary high load of the cloud for large number of resources.
In particular nova can fail while deploying large Sahara clusters
because of tons of simultaneous requests to create/update VMs and
polling those resources for status.
Also Heat partially support batch update (only for AutoscalingGroup)

Proposed change
===============

Add batching_policy property to ResourceGroup with similar to
rolling_update structure::

    res_group:
      type: OS::Heat:ResourceGroup
       properties:
         count: 5
         ...
         batching_policy:
           min_in_service:1
           max_batch_size: 2
           pause_time: 10
           batch_actions: ['CREATE', 'UPDATE_EXISTING', 'UPDATE']
        ...

Where:

`max_batch_size`, `pause_time`, `min_in_service` has the same meaning as
in rolling_update with one exception that `min_in_service` can't be applied
to batch `CREATE` action and will be ignored.

``batch_actions`` is actions that will be batched, with the following available
options:

`CREATE`: apply batching on stack creation i.e. add resources in sequence by
`max_batch_size` resources at every batch, possible except for the last one.

`UPDATE_EXISTING`: exactly the same thing as rolling update

`UPDATE`: regular update, existing resources will updated in batches and if it
is needed to add some count of resources they will be added in bathes too.

It is proposed to make old rolling_update property deprecated in favour of
batching_policy as batching_policy has wider possibilities including old
rolling_update.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

ochuprykov

Milestones
----------

Target Milestone for completion:
  Liberty-2

Work Items
----------

* Add batching_policy property to ResourceGroup
* Add required additional unit and functional test cases

Dependencies
============

None
