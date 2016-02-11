..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


======================
Heat custom guidelines
======================

https://blueprints.launchpad.net/heat/+spec/custom-guidelines

Need to add custom guidelines to facilitate reviewing new resources and improve
descriptions writing.

Problem description
===================

Currently there are several rules on how to write descriptions of resources,
properties, attributes and methods. For facilitate reviewing and improve
description writing, need to add heat custom guidelines and start it during tox
pep8 running.

Proposed change
===============

Currently there are several obvious rules of description writing:

 1. Terminator at the end of resources, properties, attributes and methods
    descriptions.
 2. No double or more whitespaces in descriptions.
 3. Resource should contain description about it's purpose in
    addition to summary.
 4. No leading whitespaces in the lines - if description string is long and
    split into a few lines, whitespaces should be at the end of lines and not
    at the begin of next lines.

Proposed solution is to write custom heat guidelines to cover these rules and
to add it to tox pep8 check.

Alternatives
------------

None.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  prazumovsky


Milestones
----------

Target Milestone for completion:
  mitaka-3

Work Items
----------

* Add custom guideline rules for current heat descriptions.
* Resolve all problems, which will be found with new checks.
* Add custom guidelines check to pep.

Dependencies
============

None.
