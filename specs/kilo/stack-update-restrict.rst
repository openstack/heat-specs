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

===========================
Restrict Stack Update Scope
===========================

https://blueprints.launchpad.net/heat/+spec/stack-update-restrict

When updating a stack, there is currently no way to stop an update from
destroying a given resource.

Problem description
===================

Users can (and do) worry about stack update doing wonky things. The
update-preview endpoint addresses this partially by showing what will probably
happen. The limitation of the preview function is that resources can raise
UpdateReplace exceptions at any time, making it impossible to be *certain* of the
results of an update until it is performed.

Proposed change
===============

Use the existing 'update_policy' resource attribute to let users protect
certain resources from being replaced during updates.

If the update_policy can't be satisfied, heat will move the stack to
'UPDATE_FAILED' and halt. If at all possible, constraints should be validated
before applying the update, thus moving the stack straight to 'UPDATE_FAILED'
when the update_policy is incorrect. After the update fails, the user can
adjust the restrictions and try again.

The update_policy attribute is already used for CloudFormation autoscaling
preferences, which are nested into the keys "AutoScalingScheduledAction" and
"AutoScalingRollingUpdate". CFN preferences would be unaffected by the HOT
version of update policies.

A user would specify per-resource how aggressive an update can be with a resource.
The restrictions could be on updating the resource at all, or just on
destroying the resource (including UpdateReplace).

The base cases here are:

* Restrict destroy/replace
* Restrict nondestructive updates
* Restrict both
* Restrict nothing
* Omit the update_policy entirely

The keys for these restrictions would be nested into an 'actions' key as below.

::

    resources:
      myresource:
        type: Foo::Bar::Baz
        update_policy:
          allow:
            update: <bool>
            replace: <bool>

The reason for nesting the allowed actions is to avoid adding top level keys if
there are more actions that users want to restrict in the future.

A user would be able to add or remove restrictions by updating the resource
template. The new restrictions would be effective for the current update. For
example, a resource that would otherwise be replaced would be protected if it
had an update policy added in the current update.

Conflicting directives are possible, for example in nested stacks. If an inner
resource has "replace: true" but the outer scope has "replace: false" then heat
will transfer the stack to UPDATE_FAILED to surface the problem to the user.

Alternatives
------------

An alternatives way to handle conflicting directives may be to honor the most
conservative applicable policy. This method would be much more confusing for
users, so failing the update would be preferable.

Pitfalls
--------

Implementation
==============

Assignee(s)
-----------

Milestones
----------

Targeted for Kilo

Work Items
----------

* Add an actions key to update_policy

Dependencies
============

update-dry-run
