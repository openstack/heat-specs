..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
"repeat" function for HOT templates
===================================

https://blueprints.launchpad.net/heat/+spec/repeat-function

This specification introduces a "repeat" control structure for HOT
templates.

Problem description
===================

Parameters of type "comma_delimited_list" are useful to define lists of items,
but the HOT template syntax does not provide any way to map or transform those
items.

For example, consider the use of a parameter to specify a list of ports to
include in a security group::

    parameters:
      ports:
        type: comma_delimited_list
        label: ports
        default: "80,443,8080"

The desired outcome, which is currently not possible to obtain, is that the
above parameter can be used to construct a resource as follows::

    resources:
      security_group:
        type: OS::Neutron::SecurityGroup
        properties:
          name: web_server_security_group
          rules:
            - protocol: tcp
              port_range_min: 80
              port_range_max: 80
            - protocol: tcp
              port_range_min: 443
              port_range_max: 443
            - protocol: tcp
              port_range_min: 8080
              port_range_max: 8080

Proposed change
===============

This proposal introduces a new function called ``repeat`` that iterates over
the elements of a list, replacing each item into a given template.

Following the security group example from the previous section, the
``repeat`` function would be used as follows::

    resources:
      security_group:
        type: OS::Neutron::SecurityGroup
        properties:
          name: web_server_security_group
          rules:
            repeat:
              for_each:
                %port%: { get_param: ports }
              template:
                protocol: tcp
                port_range_min: %port%
                port_range_max: %port%

Below is another example in which this function enables a solution that is
currently impossible to implement::

    resources:
      my_server:
        type: OS::Nova::Server
        properties:
          networks:
            repeat:
              for_each:
                %net_name%: { get_param: networks }
              template:
                network: %net_name%

In this example a list of networks that an instance needs to be attached to is
given as a list in a parameter.

Another interesting possibility is to generate permutations of two or more
lists. For example, the security group example above can be extended to also
support parametrized protocols as follows::

    resources:
      security_group:
        type: OS::Neutron::SecurityGroup
        properties:
          name: web_server_security_group
          rules:
            repeat:
              for_each:
                %port%: { get_param: ports }
                %protocol%: { get_param: protocols }
              template:
                protocol: %protocol%
                port_range_min: %port%

The ``for_each`` argument specifies the loop variable and the list to
iterate on as a key-value pair. The loop variable has to be chosen carefully,
as any occurrences will be replaced with each of the items in the list in each
iteration.

If more than one key/value pair is included in the ``for_each`` section, then
the iterations are done over all the permutations of the elements in
the given lists, similar to how nested loops work in most programming
languages.

The result of the ``repeat`` function is a new list, with its elements set to
the data generated in each of the loop iterations. When a single list is given,
the size of the resulting list is equal to the size of the input list. When
multiple lists are given as input, the size of the resulting list will be equal
to the sizes of all the input lists multipled.

Alternatives
------------

An alternative that was explored was to extend the ``str_replace`` function to
accomodate this functionality, but in the end it was agreed that there are
significant differences between the two usages.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  miguelgrinberg

Milestones
----------

Target Milestone for completion:
  Kilo-3

Work Items
----------

* Write the ``repeat`` function.
* Documentation.
* Unit tests.

Dependencies
============

None
