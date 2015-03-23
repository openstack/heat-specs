..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================================
 Cache r/o API requests to OS components during constraint validation
=====================================================================

https://blueprints.launchpad.net/heat/+spec/constraint-validation-cache

Heat does a lot of request to the other clients in OpenStack. These
requests leads to some overhead when we are trying to deploy a lot of instances
at the same moment. One of these requests Heat is doing during validation of
property constraints that checks external resources existence (image, flavor
or something else). In order to reduce that overhead the some kind of
validation cache has proposed in the current spec.

Problem description
===================

The detailed description of the problem is described in the following use case:

  1. User prepares a template with N stacks that use the same resource (image,
     flavor, keypair, etc)
  2. User requests Heat to create the stack
  3. During custom constraint validation for resources Heat does the following:

     - Find appropriate class that validates custom constraint
     - Request the other clients about constraint (check that the volume,
       server, flavor, etc exists)
     - If request was successful then pass validation

This approach leads to some overhead requests because we need to request the
same info (existence of image, flavor, etc) several times. In addition, current
realization doubles this overhead because we are checking property constraints
twice (during resource creation and stack validation).

Proposed change
===============

The desired use case is the following:

  0. Heat initializes a cache back-end and cache regions for each client plugin
     with using dogpile.cache (cache configuration is defined in heat.conf).
     Heat also registers generation functions for them (see
     http://dogpilecache.readthedocs.org/en/latest/usage.html for more info)
  1. User prepares a template with N stacks that use the same resource (image,
     flavor, keypair, etc)
  2. User requests Heat to create the stack
  3. During custom constraint validation for resource Heat does the following:

     - Find appropriate class that validates custom constraint
     - Request client plugin about the data from another OS component
     - if caching is enabled then
       check cache region for client plugin and
       return result of API request to client with the same resource name
       (volume, server, flavor, etc) and the same context.
       If no results have found in cache then cache region automatically
       requests the new value using generation function (see note below)
       else
       request the new value with using client_plugin
     - Pass validation if no exceptions were raised during request
     - If exception has been raised then delete the value from cache because
       we need to request it every time.

Note: if cache size exceeds size option in heat then we need to
flush the oldest values. This logic should be managed by cache back-end.

To support the case above the following steps should be executed:

 - The cache configuration options should be supported in heat.conf
 - The cache back-end should be configured using the options in heat.conf.
   Please note that using dogpile we can use several types of cache back-ends
   (in-memory, memcached, file system, DB, self-written etc). Each back-end
   requires specific input arguments.
 - The cache region should be configured for each client. In addition
   time-to-live value and cache size options should be defined for clients
   using heat.conf options.
 - The sub-classes of heat.engine.clients.ClientPlugin should request cache
   regions about new values if caching has enabled
 - The requests to client plugin should have an attribute(use_cache=False)
   that allows to define should we use caching or not. It allows to use
   caching for constraint validation only and avoid unintentional using of
   caches.

Alternatives
------------

1. Implement cache and integrate it into BaseCustomConstraint. In this case
   caching will be used for custom constraint validation only but this is not
   the best solution because of 2 reasons:

   - Cache cannot be used in future for other purposes
   - ClientPlugin is more appropriate place for caching in conceptual terms.
     There is no strict relationships in terms of OOP between Constraint
     and cache.

2. Implement light-weight cache in client plugins. This solution was declined
   during review. Please see the details below:
   "client plugins are instantiated on the first access from a resource since
   the Stack object is created. Since we now have decouple-nested this is
   going to be of less value as every nested stack is going to recreate these
   clients. And in convergence all resources will recreate the client object
   as the resource actions will be rpc'd to be worked on. So given this
   wouldn't something like memcached be better?"

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  kkushaev


Milestones
----------

Target Milestone for completion:
  Liberty-1

Work Items
----------

- Implement cache back-end - leverage dogpile back-end that tracks
  timeouts and results of previous requests
- Implement initialization of cache regions
- Integrate caching into subtypes of ClientPlugin that make requests to other
  clients
- Prepare tests for each step

Dependencies
============

None
