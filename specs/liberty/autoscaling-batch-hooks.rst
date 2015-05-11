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

======================================
Autoscaling Group Rolling Update Hooks
======================================

Hooks are included in Kilo, but don't address a helpful use for hooks.
Currently, there are pre-create and pre-update hooks, but this would add a
special hook to OS::Heat::AutoScalingGroup to set a hook before each batch in a
rolling update.


Problem description
===================

Working with TripleO it's often desirable to pause to check that an update is
doing what you want (which is why hooks exist at all), and the "pause_time"
provided by the rolling_updates policy can be used for a similar purpose.

The problem is that you may not be able to sufficiently test the result of a
rolling update batch within the pause_time set, but you don't have a way to
signal to heat to add more time. Or the pause_time may be excessively long,
making the update time too slow.

Being able to set a breakpoint between batches is a much better solution, so
the operator can take an arbitrarily long (up to stack timeout) or short time
to confirm the upgrade went as planned.

Proposed change
===============

To make debugging and verifying rolling updates easier, I propose adding a
'batch_hook' parameter to rolling_updates like below.::

    my_asg:
      type: "OS::Heat::AutoScalingGroup"
      properties:
        desired_capacity: 4
        ...
        rolling_updates:
          batch_hook: true
          min_in_service: 1
          ...

The batch_hook option and pause_time will be mutually exclusive, since it
doesn't make much sense to have both a set pause time *and* hooks between
batches.

This will be confined to AutoScalingGroup, won't break any existing templates,
and won't affect other grouped resources.

Alternatives
------------

1. The name "batch_hook" seems descriptive enough for me, but another option
   for the parameter name would be "pre_batch_hook" to denote that the hook is
   set before each batch (not after).

2. Another alternative would be to add a hook type that would be set by in the
   environment, not in the rolling_update policy. I think localizing this to
   the AutoScalingGroup scaling policy is a better choice and use stack updates
   to toggle the hooks for each group.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  sb~p (Ryan Brown)

Milestones
----------

liberty-1

Work Items
----------

Dependencies
============

None
