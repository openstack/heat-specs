..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================================
Property translation mechanism fixing and improving
===================================================

https://bugs.launchpad.net/heat/+bug/1620859

Currently translation mechanism has several mistakes, depended on modifying
data before it's using - so functions cannot be correctly translated; heavy
dependence on HOT and Cfn functions; muddy code full of tricks. This spec is
designed to discuss with community better way to re-implement translation
mechanism.

Problem description
===================

Translation mechanism (TM) has been implemented in Kilo, refactored in Newton
and still works incorrectly. There are several cases, which should be mandatory
fixed:

  1. TM incorrectly handles functions - if TM found function in the middle of
     translation path, it doesn't resolve it and raises error, because cannot
     get next item in translation path. For example, if property `networks`
     equals function, and translation path equals to `[networks, network]`,
     then `network` won't get in case of function has no get method.

     Current workaround suggests just to skip such translation rules, where
     there is such situation.

  2. TM modifies properties data before it's using, which is useless. At first,
     modifying data is unsafe. At second, if first step will be fixed,
     functions resolved and return resolved data every time they called, so
     translations cannot work with them.

  3. TM depends on HOT and Cfn template formats - this makes it impossible for
     third-party template format plugins to be first-class citizens in Heat, as
     they are liable to break whenever someone adds a translation rule.

  4. TM code has many muddy and tricky places, which should be facilitated and
     made clearer.


Proposed change
===============

Before suggesting solution need to note, that changes concerned translation
mechanism, but don't translation rules and how they specified in resource
plugins for support third-party resources.

Next changes should fix TM and improve it:

  1. Make translation phase during getting properties. It assume that functions
     will be resolved before translation, properties will always return
     translated value.

     a) improve currently useless *name* variable in `Property` class, which
        will store full name of property, for example `networks.network`;

     b) operate with translation rules inside of properties - store TM object
        and pass it to properties sub-schemas;

     c) call translation before cast to defined property type - if there's any
        translation.

  2. Store translated result for already called properties - it helps doesn't
     translate property every time it's called. Translated values will be
     stored by full name as `networks.network`.

     Result should not stored during validation phase.

     Also, instead of storing translated result in explicitly in some dict,
     we can use cache instead, but there could be issues, like in `LP#1609787`_
     bug.

  3. Refactor and facilitate huge code of TM due to previous steps try to do
     code more clear to understand.

  4. Add functional tests to cover different risky cases.


Alternatives
------------

Change current version TM, adding fixes for mentioned problems.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  prazumovsky


Milestones
----------

Target Milestone for completion:
  ocata-3

Work Items
----------

* Move making translation during properties get.
* Refactor TM to clear code and fix unnecessary dependencies.
* Add functional tests to cover risky cases.

Dependencies
============

None


.. _LP#1609787: https://bugs.launchpad.net/heat/+bug/1609787
