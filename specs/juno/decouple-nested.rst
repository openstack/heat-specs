..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================
 Decouple Nested Stacks
=======================

https://blueprints.launchpad.net/heat/+spec/decouple-nested

As step towards the more granular architecture described in the
convegence-engine spec, it has been proposed that we could more effectively
decouple nested stacks within the existing heat architecture.

Problem description
===================

Creating a tree of many nested stacks results in the entire stack tree getting
processed, for every stack operation, by one heat-engine process, with access
to every nested stack serialized by the same global lock (that obtained to
access the top-level stack).

While the arguably more complex and invasive steps described by
convergence-engine are worked out (which may take some time, and will probably
be made simpler by the decoupling described below), it's proposed that we look
at decoupling nested stacks more effectively from their parent, such that we
can make use of the existing RPC round-robin scheduling to enable nested stacks
operations (e.g create/update/delete) to be handled in a more scalable way by
spreading the work for each stack over multiple engine processes or workers.

Proposed change
===============

* Rework the engine RPC interfaces to enable some additional arguments to be
  passed to create/update operations, such that the existing coupling (for
  example passing user_creds ID's) between parent and nested stacks can be
  broken.
* Refactor the StackResource base-class to perform operations via RPC and not
  manipulate parser.Stack objects directly when performing lifecycle operations

Note that the StackResource rework will focus on performing actions which
change the state of the stack via RPC calls (e.g those which are performed
asynchronously via an IN_PROGRESS state), leaving the existing code for stack
introspection unchanged.  This should allow a less risky transition to the
new interfaces with minimal rework of the StackResource subclasses.

One area which may be left for a future enhancement is the polling for COMPLETE
state after triggering the action via RPC, e.g when we triggger a nested stack
create via an RPC call, we will poll the DB directly waiting for the CREATE
COMPLETE state in check_create_complete.  In future, it would be better to wait
for a notification to avoid the overhead of polling the DB.

Alternatives
------------

Wait for the full convergence-engine vision to come together I guess, but it
seems apparent that we need a more immediate mitigation plan for the subset of
users who care primarily about these kind of workloads.

Implementation
==============

Assignee(s)
-----------

Steven Hardy (shardy)

Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

* Rework RPC interfaces
* Convert StackResource create operations to create the stack via RPC
* Convert StackResource delete operations to delete the stack via RPC
* Convert StackResource suspend operations to suspend the stack via RPC
* Convert StackResource resume operations to resume the stack via RPC
* Convert StackResource check operations to check the stack via RPC
* Convert StackResource update operations to update the stack via RPC

Dependencies
============

None, but this could be considered a precursor to the convergence-engine work.
