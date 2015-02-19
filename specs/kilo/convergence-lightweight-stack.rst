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

=========================================
Lightweight Stack loading for convergence
=========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/convergence-lightweight-stack

Problem description
===================

When we load the resources for a stack from the database, we load all of them
at once. We also assume that resource names are unique within a stack (i.e.
there is only one version of each resource). In convergence there will be
multiple versions of each resource coexisting in the same stack, and we'll want
to load only the one we're going to perform operations on at any given time.

Proposed change
===============

Allow the stack to provide cached values for all of the `get_resource` and
`get_attr` references in the template when they are resolved. Don't load the
whole list of resources when this cached data is available.

Alternatives
------------

Continue to load every resource from the database whenever we need resource ID
or attribute data.

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

- Substitute reading from a cache for loading resources when resolving template
  functions

Dependencies
============

The cached values will be obtained by the code for
https://blueprints.launchpad.net/heat/+spec/convergence-push-data
