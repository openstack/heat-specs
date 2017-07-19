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

=========================
Improve "repeat" function
=========================

https://blueprints.launchpad.net/heat/+spec/improve-repeat-function

This specification improves the "repeat" intrinsic function.

Problem description
===================

The "repeat" function now only supports to iterates over all the permutations
of the elements in the given lists if more than one key/value pair is
included in the ``for_each`` section. Similar to how nested loops work in
most programming languages.

There are some user cases that user don't want to loop nested when using
"repeat" function. For example, there are some list parameters:
networks, subnets and ips::

    parameters:
      networks:
        type: comma_delimited_list
        default: "net1, net2, net3, ..., netn"
      subnets:
        type: comma_delimited_list
        default: "sub1, sub2, sub3, ..., subn"
      ips:
        type: comma_delimited_list
        default: "ip1, ip2, ip3, ..., ipn"

and user want to create a server with several nics::

  resources:
    my_server:
      type: OS::Nova::Server
      properties:
        ..... //some properties
        networks:
        - network: net1
          subnet: sub1
          fixed_ip: ip1
        - network: net2
          subnet: sub2
          fixed_ip: ip2
        - network: net3
          subnet: sub3
          fixed_ip: ip3
        - ...
        ...

The "repeat" function is a good choose for this case. But now
"repeat" function will do nested loops to iterate the over all the
permutations of the elements in the given lists:
[[net1, net2, net3, ...],[sub1, sub2, sub3, ...], [ip1, ip2, ip3, ...]]
Take the example of two items for each list::

   ...
   networks:
     repeat:
       for_each:
         %net%: [net1, net2]
         %sub%: [sub1, sub2]
         %ip%: [ip1, ip2]
       template:
         network: %net%
         subnet: %sub%
         fixed_ip: %ip%

We will get the result after resolved the function::

   [{'fixed_ip': 'ip1', 'network': 'net1', 'subnet': 'sub1'},
    {'fixed_ip': 'ip2', 'network': 'net1', 'subnet': 'sub1'},
    {'fixed_ip': 'ip1', 'network': 'net1', 'subnet': 'sub2'},
    {'fixed_ip': 'ip2', 'network': 'net1', 'subnet': 'sub2'},
    {'fixed_ip': 'ip1', 'network': 'net2', 'subnet': 'sub1'},
    {'fixed_ip': 'ip2', 'network': 'net2', 'subnet': 'sub1'},
    {'fixed_ip': 'ip1', 'network': 'net2', 'subnet': 'sub2'},
    {'fixed_ip': 'ip2', 'network': 'net2', 'subnet': 'sub2']

But what the user want is two nics::

    [{'fixed_ip': 'ip1', 'network': 'net1', 'subnet': 'sub1'},
     {'fixed_ip': 'ip2', 'network': 'net2', 'subnet': 'sub2']


Proposed change
===============

This proposal improves the "repeat" function to support above the user case.
Add a boolean flag section "permutations" for "repeat", and the default value
is 'True' to make sure the compatibility. Then the "repeat" function would be
used as follows::

   resources:
      my_server:
        type: OS::Nova::Server
        properties:
          (...other properties)
          networks:
            repeat:
              permutations: False
              for_each:
                %net%: { get_param: nets }
                %sub%: { get_param: subnets }
                %ip%: {get_param: ips}
              template:
                network: %net%
                subnet: %sub%
                fixed_ip: %ip%

As above, set the section 'permutations' to False, then the result of the
function will satisfy the user's requirement.

Notes:
   There is a constraint for it: the length of lists should be equal.

Alternatives
------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  huangtianhua@huawei.com

Milestones
----------

Target Milestone for completion:
  Pike-1

Work Items
----------

* Add "permutations" section for ``repeat`` function, and
  implement the new replacement method.
* Documentation.
* Add related tests.
* Add template examples.

Dependencies
============

None
