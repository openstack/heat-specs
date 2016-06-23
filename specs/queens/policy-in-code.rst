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

====================================
Register and Document Policy in Code
====================================

https://blueprints.launchpad.net/heat/+spec/policy-in-code

Operators need to maintain a (possibly complex) policy.json file that might
differ only slightly from the default one,
and some values in the policy.json file are tied to config options
without explicit dependency between them.

Problem description
===================

As an operator, I would like to specify in the ``policy.json`` file only those
policies that are different from defaults.

Such support was declared as cross-project OpenStack community goal
for Queens release [#]_.

Proposed change
===============

Since version 1.9.0 oslo.policy supports handling policies in the way
similar to how oslo.config handles config options [#]_.
Policies now can be declared inside Python code with provided defaults,
and registered in the policy engine.
The policy engine then loads these and the policy.json file on start,
with entries in the latter overriding the defaults specified in the code.

This way, a service with default policies can run without
``policy.json`` file, and operators only need to fill this file in the case
their rules are different.

Another nice benefit is that this allows to use values from config file in
the default policy - as example, the name of the temporary user's role in Heat
currently is defined both in config file and default policy.json file, so
operators need to update both heat.conf and policy.json file when
changing this role.

A small performance penalty during service startup is expected,
as well as marginal performance improvements during run-time,
as there's no need to re-read a possibly large policy.json file.

Sample policy file can be generated based on the registered policies
rather than needing to manually maintain one.

A number of additional ways to generate policy-related files are supported
by oslo.policy >= 1.10:

- Merged policy file - a policy file can be generated which is a merge
  of registered defaults and policies loaded from a file.
  This shows the effective policy in use.
- Redundant policies file - a list can be generated which contains policies
  defined in a file which match defaults registered in code.
  These are candidates for removal from the file in order to keep it
  small and understandable.

Heat already depends on oslo.policy >= 1.23 in its requirements, so no bump
in dependencies is required.

Alternatives
------------

None. Required to complete the cross-project goal.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  pshchelo <Pavlo Shchelokovskyy> IRC: pas-ha

Milestones
----------

Target Milestone for completion:
  queens-1

Work Items
----------

- accumulate, define and register policies in the Python code
- change invocations of ``Enforcer.enforce`` to ``Enforcer.authorize``
  (the call signature is unchanged)
- amend genconfig tox environment to also generate sample policy.json file
- remove policy.json file and update DevStack / Heat's DevStack plugin
  to not use policy.json
- (see dependencies) provide configs/scripts to generate merged policy file
  and redundant policy file.
- amend documentation accordingly

Dependencies
============

None.


.. [#] https://governance.openstack.org/tc/goals/queens/policy-in-code.html
.. [#] https://docs.openstack.org/oslo.policy/latest/user/usage.html
