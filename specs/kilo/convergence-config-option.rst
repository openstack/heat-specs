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
Add a config option to enable Convergence
=========================================

https://blueprints.launchpad.net/heat/+spec/convergence-config-option

Problem description
===================

The new convergence architecture is a major change to the code base. In order
to decouple landing the necessary changes from the release cycle while
maintaining stability for end users, we need to develop it alongside existing
code and tests and avoid breaking existing code until such time as convergence
can pass the functional test suite.

Proposed change
===============

Add a config option that allows the operator to enable the convergence code
path for new stacks. The option will initially be off by default. We will
enable it as soon as convergence has landed and is in a working state (passes
functional tests), provided that doing so does not create an undue level of
risk (i.e. if this happened to occur right before feature freeze, we would
likely delay changing the default until after the release).

Also add a flag to the Stack table to indicate whether each stack should use
existing legacy code path or convergence code path. All pre-existing stacks
will continue using the legacy code path. New stacks will use the code path
selected by the operator via the config option.

At some point in the future, we will create a tool that allows us to populate
existing legacy stacks with the additional data required to start using them
with the convergence code. Once we have such a migration tool we can deprecate
the legacy code path, and after an appropriate interval and once all of the
legacy 'unit' tests that require it have been converted to functional tests we
can remove that code path altogether.

Alternatives
------------

In addition to the config option, we could also allow the user to select on
each stack create whether to use the legacy or convergence code. This could
make funtional testing easier, as we wouldn't need to change the configuration
to test the two parts. However, the downside is that it exposes to the user
what should be an implementation detail.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  prazumovsky

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

- Implement the config option

Dependencies
============

None
