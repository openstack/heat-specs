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

==================
Heat Upgrade Tests
==================

https://blueprints.launchpad.net/heat/+spec/upgrade-tests

The new direction of the grenade project is to use devstack-style
plugins to support upgrade testing. This spec aims to get upgrade
testing infrastructure in Heat's tree.

Problem description
===================

Currently, there aren't any tests that check if a patch in-review
would break the upgrade of Heat from a previous release.

Some of the issues a deployer may face during or post upgrade are as follows:

- The deployed database not successfully migrating to the newest schema.
- Stacks created in an older release not updatable/deletable in new release.
  A change in the update/delete workflow may render existing stacks useless
  or be in an IN_PROGRESS state forever.
- Physical resources disappearing when the control plane is taken down.
- Configuration options removed prematurely without notice.

Proposed change
===============

Get upgrade testing in-tree by using grenade's external plugin mechanism.
The upgrade tests should follow what grenade calls the Theory of Upgrade
- https://github.com/openstack-dev/grenade#theory-of-upgrade

To ease developers writing upgrade tests, we will have
(pre/during/post)-upgrade tox envs that will run tests
respectively during the (pre/during/post)-upgrade phases
in grenade.

As an example, the pre-upgrade phase will create stacks before an
upgrade. The during-upgrade phase will check if the resources created by a
stack are still alive even when heat's services are down. The post-upgrade
phase could update/delete these stacks to verify that those old stacks are
still operable.

Once this infrastructure is in place, we should be able to add support
for rolling upgrades of heat-engine with the help of the existing versioned
objects mechanism in Heat. This will use Grenade's partial-upgrade strategy
similar to what is being done for Nova.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  sirushtim

Milestones
----------

Target Milestone for completion:
  liberty-2

Work Items
----------

- In-tree grenade testing.
- Project config changes to add voting grenade job.
- Tag smoke tests in heat_integrationtests that must be run during the
  grenade sanity-check(verify) phase.
- pre/during/post-env env sections in tox that will respectively invoke
  the tests before, during and after the upgrade of Heat.
- Get devstack to use the system level heat binaries instead of the ones
  in the repository to emulate what a user would face when upgrading heat.
- Add Upgrade Impact section to heat-specs.
- Support rolling upgrade of heat-engine.

Dependencies
============

Grenade external plugin mechanism https://review.openstack.org/#/c/185050
