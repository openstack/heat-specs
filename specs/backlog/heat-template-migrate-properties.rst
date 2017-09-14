..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================
Heat template migrate resources' properties
===========================================

https://blueprints.launchpad.net/heat/+spec/heat-template-port

Heat does not provide api/cli to migrate the given template from old heat
version to later.

Problem description
===================

Heat is being released inline with each Openstack release and there is a chance
that resource properties and attributes might have changed and/or deprecated
across these releases. A user may wish to migrate the template to current
version which was created during earlier version say juno. Currently heat
does not support it.

Proposed change
===============

Heat already having mechanism to define the translation rule for each of the
properties being deprecated by using translation.TranslationRule.
This is being implemented in resource plugins in order to support migration
to new property in place of deprecated one.

This feature could be updated with below command

``openstack orchestration template migrate -t <template-file> --output-format
[json|yaml] --output-file <output-file>``

This command will migrate the given template file and will write the template
output mentioned in output-format.

Command will provide messages of changes made to the deprecated properties in
below format::

    <resource-path> <property> <action> <details>

where:

*resource-path*
    Gives the resource path in the given template.

*property*:
    Property name to migrate to current version.

*action*:
    One of add, replace or delete.

*details*:
    Provides additional details about deprecation, if any.


Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  kanagaraj-manickam
  ananta

Milestones
----------

Target Milestone for completion:
  ocata-1

Work Items
----------

* For those deprecated properties in resource plugins, add translation rules
* Add required API and test cases
* update the python-openstackclient with new CLI as mentioned above.

Dependencies
============

None
