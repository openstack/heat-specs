..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


=============================
 Multi-region scenario test
=============================

https://blueprints.launchpad.net/heat/+spec/multi-region-test

Add a scenario test for Multi-Region Orchestration.

Problem description
===================

Heat supports Multi-Region Orchestration through remote stacks. While remote
stacks themselves are tested with unit and functional tests, there are no
scenario tests which test the creation of remote stacks across multiple
regions.

Proposed change
===============

This change will add a scenario test which creates two remote stacks in
different regions and checks if their creation was successful.

This will require a multinode test setup with two distinct devstack instances,
each configured with its own region. Multinode test setups are already possible
in infra, but the configuration of regions requires changes to devstack-gate
and openstack-infra/project-config to allow this test to run as a gate test.

Alternatives
------------

In case it turns out to be impossible to create an multinode test setup with
multiple regions in the openstack infrastructure, this scenario test could also
be added as a local-only test which is not ran at the gate.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  dgonzalez

Milestones
----------

Target Milestone for completion:
  liberty-3

Work Items
----------

  1. Implement scenario test which does the following:

    - Create a stack containing two simple remote stacks
    - Both remote stacks target different regions
    - After sucessful creation, the output of the remote stacks is checked

  2. Include scenario test in devstack-gate

    - Configure devstack multinode setup in project-config
    - Assign regions to the devstack nodes

Dependencies
============

None
