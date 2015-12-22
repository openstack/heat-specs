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

====================
Convergence Rollback
====================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-rollback

Problem description
===================

We need to allow the user to cancel an update that is in progress and roll back
to the previous known good state. We also need to give users the option of
rolling back to the previous known good state in the event of a failure while
updating the stack.

Proposed change
===============

Since convergence removes the Stack-level locking for updates, we can implement
rollback as a simple update to a previously-stored version of the template.
Other parts of the convergence implementation will ensure that this deals
correctly with any resources that may still be in progress. The update will
still get a new traversal ID, even though it is updating to the same template
ID that was seen previously.

In the Stack table, we will store the ID of the most recent template to
successfully complete (if any) alongside the ID of the current target template
(at the completion of an update, these will be the same). Whenever either of
the stored template IDs are overwritten in such a way that we will no longer
refer to a particular Template, delete that Template from the database.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  ananta

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Implement rollback
- Clean up unused templates

Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/convergence-check-workflow
- https://blueprints.launchpad.net/heat/+spec/convergence-concurrent-workflow
- https://blueprints.launchpad.net/heat/+spec/convergence-parameter-storage
- https://blueprints.launchpad.net/heat/+spec/convergence-stack-data
