..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

====================================
 Intrinsic function to split strings
====================================

https://blueprints.launchpad.net/heat/+spec/str-split

From HOT 2014-10-16 we no longer support the AWS compatible Fn::Split intrinsic
function in HOT templates, which means there's no way to split a string into
a list of components by delimiter.

Problem description
===================

The current use case is to avoid doing this in TripleO templates, but it's
likely a generally useful addition:


.. code-block:: yaml

  ip_subnet:
    # FIXME: this assumes a 2 digit subnet CIDR (need more heat functions?)
    description: IP/Subnet CIDR for the storage network IP
    value:
          list_join:
            - ''
            - - {get_attr: [StoragePort, fixed_ips, 0, ip_address]}
              - '/'
              - {get_attr: [StoragePort, subnets, 0, cidr, -2]}
              - {get_attr: [StoragePort, subnets, 0, cidr, -1]}

This is both fragile and cumbersome, it'd be better to allow easily splitting
on the "/" delimiter.

The second use-case is to enable joining of two (or more) lists together:

.. code-block:: yaml

  parameters:
    ExtraConfig:
      type: json
      default: []

  resources:
    type: OS::Heat::StructuredConfig
    properties:
      group: os-apply-config
      config:
        hiera:
          hierarchy:
            - controller
            - object
            - ceph
            - common
            - {get_param: ExtraConfig}

Here, the desired behavior is to merge/append the contents of the ExtraConfig
parameter, which may be either json or comma_delimited_list type, such that the
"hierarchy" list contains both the hard-coded items and whatever list is
provided via ExtraConfig.

Proposed change
===============

Add a str_split intrinsic function, such that the first example becomes:

.. code-block:: yaml

  list_join:
  - ''
  - - {get_attr: [StoragePort, fixed_ips, 0, ip_address]}
    - '/'
    - {str_split: ['/', {get_attr: [StoragePort, subnets, 0, cidr]}, 1]}

This means we can strip the subnet mask from the CIDR without hard-coded
assumptions around it always being 2 digits - path based lookup by index will
be supported, e.g the same syntax as get_attr and get_param, so when an index
is specified then the list item at that index is returned, otherwise the
entire list is returned.  This is consistent with current get_attr behavior
and avoids forcing the user to use Fn::Select to extract a list item.

To enable the second use-case, we can use the new str_split function, with
an enhanced version of list_join which can optionally take a list of lists,
e.g it's capable of joining multiple lists on a delimiter:

.. code-block:: yaml

    config:
      hiera:
        hierarchy:
          str_split:
          - ','
          - list_join:
            - ','
            - - controller
              - object
              - ceph
              - common
            - {get_param: ExtraConfig}

Alternatives
------------
For the list merging I was thinking we could use the YAML << merge directive,
but some experiements indicate this will only merge maps, not lists which
are required in this case.

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  shardy

Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

Changes to engine:
- Bump HOT template version for Liberty
- Enhance list_join to support optionally joining lists of lists.
- Add a new str_split function with associated tests.

Documentation changes:

- Update HOT specification as part of the commits above.


Dependencies
============

None
