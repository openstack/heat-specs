..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


=====================================================
OpenStack Heat Orchestration Template (HOT) Generator
=====================================================

https://blueprints.launchpad.net/heat/+spec/os-hot-gen

An python library used to generate a given HOT template with given version.

Problem description
===================

There are different users, who needs a library to generate an valid
HOT template, as given below:

1. Automation

OpenStack heat service is getting used widely in other OpenStack services such
as Murano, Magnum, Tacker, etc and some of these projects generate HOT
template during the runtime as part of the automation supported by them.

2. Cloud providers

Every Cloud providers uses different designer tools for drawing topology
visually and each of these tool use it's own way to generate the HOT template,
as heat does not provide sdk for hot template generation. It's an redundant
effort and maintaining them over HOT template schema changes is an overhead.


Proposed change
===============

HOT template has following aspects and model each of them as python
programmable construct such as class and provide required/supporting python
api for generating HOT template by writing the python code.

* Version
* Description
* Parameters and Parameter group
* Resources and Properties
* Intrinsic Functions
* Outputs
* Environment

An sample SDK is provided `here`_ as POC.

.. _here: https://github.com/mkr1481/os-hot-gen

This POC has modeled almost everything of above mentioned aspects and
for functions it does provide only for get_param as an sample one, which
can be extended further for other supported functions.


Alternatives
------------
None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
    kanagaraj-manickam

    jdob

Milestones
----------
Target Milestone for completion:
newton-2

Work Items
----------
* Make POC into stable version
* Create new repository under OpenStack github and migrate the POC code under
  it. Also, add the new repository under OpenStack heat goverenance.
* Provide example python snippets to generate sample HOT templates
* Add option to generate the Resource properties and outputs based on given
  resource type schema generated from heat service.
* Add functional test cases to validate the generated HOT template using heat
  template validation command.

Dependencies
============

None
