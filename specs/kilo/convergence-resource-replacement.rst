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

================================
Convergence Resource replacement
================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-resource-replacement

Problem description
===================

During a stack update, some resources will need to be replaced (rather than
updated in-place). In general, we can't know in advance for which resources
that will be the case, so we need to be able to create replacements on the fly.

Proposed change
===============

When we detect that a resource needs to be replaced (i.e. Resource.update
raises UpdateReplace), create a new resource with the same name in the same
stack. Fill in a the `replaces` and `replaced_by` fields of the new and
existing resources, respectively. Do *not* create a SyncPoint for the new
resource.

Once the new Resource has been stored in the database, retrigger the current
check with the same data except passing the key of the new resource. Then
return immediately, without triggering any dependent nodes.

Note that no modification of the graph stored in the Stack is required. When we
come to trigger the SyncPoints of nodes that are dependent on the replaced
resource, the replacement should just use the old resource's graph key to
impersonate it. However the contents of the input data (not the keys) to the
next resource will contain the resource ID of the replacement, so that
dependent resources will update their dependency lists. The previous resource
will be visited again in the clean-up phase of the graph, at which point it
will be deleted.

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

- Create a replacement resource and link it to its predecessor
- Trigger the check on the new resource
- Create developer documentation

Dependencies
============

- https://blueprints.launchpad.net/heat/+spec/convergence-check-workflow
