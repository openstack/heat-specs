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

=================================
Implement check_resource workflow
=================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-check-workflow

Problem description
===================

Rather than working on the whole stack in-memory, in convergence we want to
distribute tasks across workers by sending out notifications when individual
resources are ready to be operated on.

Proposed change
===============

The workflow has been prototyped in
https://github.com/zaneb/heat-convergence-prototype/blob/resumable/converge/converger.py

After calculating the traversal graph, the stack update call triggers the leaf
nodes of the graph. After each node is processed, examine the traversal graph
(which is stored in the Stack table) to determine which nodes are waiting for
this one. Store input data for each of those nodes in their SyncPoints, and
trigger a check on any which now contain their full complement of inputs.

The SyncPoint for the stack works similarly, except that when complete we
notify the stack itself to mark the update as complete.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  sirushtim

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Kick off the workflow from the stack update
- Implement skeleton check_resource
- Notify the stack of the result when complete (or on failure)
- Create developer documentation

Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/convergence-graph-progress
- https://blueprints.launchpad.net/heat/+spec/convergence-prepare-traversal
- https://blueprints.launchpad.net/heat/+spec/convergence-lightweight-stack
- https://blueprints.launchpad.net/heat/+spec/convergence-message-bus
