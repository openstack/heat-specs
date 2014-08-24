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

====================================================================
 Make tempest orchestration scenario tests the heat functional tests
====================================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/functional-tests

Having all OpenStack functional tests in tempest is no longer scalable,
so heat functional tests need to live in the heat repository.

Problem description
===================

Existing tempest orchestration scenario tests need to be moved into the heat
repository in a way which requires no dependency on the tempest code, and
which can be done with minimal development effort.

The heat gate needs to switch over to running the heat functional tests,
as well as whatever orchestration tests remain in tempest.

Proposed change
===============

The proposed plan for this work will be:

* Forklift tempest.scenario.orchestration into heat functionaltests
* Copy and modify any supporting tempest code into a subpackage of
  functionaltests to make it possible for the tests to run
* Replace configuration loaded from tempest.conf with a solution which
  initially requires no configuration file, specifically:

    * Tests will be run with credentials sourced from the environment, which
      heatclient does by default anyway
    * Configuration which refers to cloud resources will hard-code values
      which correspond to values set up by devstack, and tests will fail
      if cloud resources with those names do not exist. This applies to
      configuration values:
      image_ref, keypair_name, instance_type, network_for_ssh
    * build_timeout will be given a default value which is overridable from
      an environment variable

* Modify devstack, devstack-gate and openstack-infra/config to check and
  gate on the heat functional tests. This job will replace the current
  heat-slow job
* Ensure there are no tempest.api.orchestration tests running in the heat-slow
  job, specifically:

    * Do not tag test_nova_keypair_resources as a slow test
    * Modify test_neutron_resources to run with cirros, or rewrite it as a
      functional test
* Delete the heat-slow job, and tests in tempest.scenario.orchestration

Alternatives
------------

The following alternative design points could be considered:

* A dedicated conf file to replace the current tempest.conf, or read
  test configuration values from heat.conf
* Failing tests instead of skipping for missing credentials or required cloud
  resources
* Modifying tox.ini to filter out functional tests on a unit test run instead
  of skipping based on current environment

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Steve Baker <sbaker@redhat.com>

Milestones
----------

Target Milestone for completion:
  Juno-3, but work can continue during feature freeze

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

* devstack
