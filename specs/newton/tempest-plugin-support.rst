..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================
Tempest plugin support
======================

https://blueprints.launchpad.net/heat/+spec/tempest-plugin-support

Migrate existing integration tests to use tempest plugin, so these
tests can run under tempest framework. And add negative API tests for
heat.

Problem description
===================

Tempest support external plugin since BP `Tempest External Plugin Interface
<https://specs.openstack.org/openstack/qa-specs/specs/tempest/tempest-
external-plugin-interface.html>`_ . Basic idea for tempest plugin is that
each project can implement tempest like tests in their repo and provide
those as tempest plugin. So that those tests can be run as part of tempest run.

Currently integration tests are running with tox and not compatible with
tempest plugin, it's better to migrate our tests to support tempest plugin.
Then refstack can use tempest framework to score this project.

Proposed change
===============

1. Introduce tempest plugin.

   Refractor heat_integrationtests structure::

        heat_integrationtests/
            config.py
            plugin.py
            functional/
            scenario/

    Two new file will be added:config.py and plugin.py. Options in
    heat_integrationtests/common/config.py will be copied and adjust to
    heat_integrationtests/config.py.

   Create a entrypoint in setup.cfg::

        [entry_points]
        tempest.test_plugins =
            heat_tests = heat_integrationtests.plugin:HeatTempestPlugin

2. Make functional tests compatible with tempest plugin.

3. Make scenario tests compatible with tempest plugin

4. Change gate to use heat tempest plugin, might need some modification on
   setup scripts.

Alternatives
------------

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ethan Lynn <xjunlin@cn.ibm.com>

Milestones
----------

Target Milestone for completion:
  newton-1

Work Items
----------

- Create tempest plugin framework.
- Adapt existing integration tests to tempest plugin.
- Change gate to use heat tempest plugin.

Dependencies
============
