..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================================
Operator Tool to migrate stacks to the convergence mode.
========================================================

https://blueprints.launchpad.net/heat/+spec/convergence-migrate-stack

It would be useful for operators to make sure all stacks are being run
under the same logic in order to support the service better.

Problem description
===================

Whether or not a stack action is run under convergence is sticky,
meaning that if the current "convergence_engine" setting is True when
the stack-create is run, then that stack will always be run with the
convergence logic (the same is also true for convergence_engine=False).

Proposed change
===============

This spec proposes a new tool for operators that migrates any stack created
under the legacy mode to convergence mode.

This will only convert stack that are in a sane state (\*_COMPLETE) and
will warn the operator if they need to re-run the command to catch
stacks currently have actions in progress.

The steps the operator will need to take are:

1. edit /etc/heat/heat.conf change convergence_engine to what they want
2. restart heat-engine
3. run "heat-manage migrate-convergence-1 <stack_id>"


Alternatives
------------

1. Stacks could be left to run in both modes and eventually users would
   re-create stacks thus migrating them to the new mode (this could take
   a long time though).
2. We could automatically convert stacks on the next
   stack-update. This takes the control out of the operators hands,
   but has the advantage of doing this operation piecemeal and the
   end-user could fix any issues that arise. (asalkeld: I think this could be
   an attractive option).
3. Grow some balls and decide that we are going with convergence and
   make this a migration script (aka no-going-back).

Implementation
==============

Extend *heat-manage* as follows::

    heat-manage migrate-convergence-1 <stack_id>

This command will call code in stack.py to get stack with stack_id and
all it nested stuff. We need to set convergence = True,
prev_raw_template_id = None and remove appropriate raw template,
generate and add new traversal_id and set current_template_id for all
resources in these stacks.
Also we need to fill `needed_by` and `requires` columns in the database
with corresponding dependencies.

Assignee(s)
-----------

Primary assignee:
   ochuprykov


Milestones
----------

Target Milestone for completion:
  newton-2

Work Items
----------

- add the new command to heat-manage.
- add code to stack.py to do the migration.
- unit tests.
- functional tests: https://review.openstack.org/#/c/230292/

Dependencies
============

None
