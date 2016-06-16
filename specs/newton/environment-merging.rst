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

=====================================
More flexible merging of environments
=====================================


https://blueprints.launchpad.net/heat/+spec/environment-merging


Since we now support server side merging of environment files, which is good
but it only supports the same "last one wins" merge strategy that we
previously had in heatclient.

In some situations more flexibility is required, e.g when composing a
deployment via multiple environment files where parameter key collisions
will occur.


Problem description
===================

Consider this scenario

heat stack-create foo -f foo.yaml -e one.yaml -e two.yaml

one.yaml contains

  parameters:
    ControllerServices:
      - Keystone

two.yaml contains

  parameters:
    ControllerServices:
      - Glance


With the current environment merging I will always get:

  parameters:
    ControllerServices:
      - Glance

But what I actually want is:

  parameters:
    ControllerServices:
      - Keystone
      - Glance

So, I need some way to specify that the heat server-side environment merging
will append to, rather than overwrite the ControllerServices parameter.
(Same problem exists for e.g json map parameters, where we probably want to
offer the option of shallow and deep merge vs just overwriting).

Note this is the exact same problem faced (and fixed) by some other tools
that accept potentially overlapping sections of yaml data, such
as cloud-init[1]

[1] http://cloudinit.readthedocs.io/en/latest/topics/merging.html

Proposed change
===============

Since parameters/parameter_defaults are simple key/value pairs it's hard to
come up with an interface that adds merge strategy data within the parameters
map, so we'd probably need a separate environment section, e.g:

1. Specify global merge strategy for all parameters:

  merge_strategy:
    list: extend
    dict: merge # we could support "merge" and "deep_merge" here?
    string: append

2. Specify per-parameter merge strategy

  merge_strategy:
    parameters:
      ControllerServices: extend

This is pretty similar to how the cloud-init "merge_how" directive works.

If multiple environments specified conflicting merge_strategy values, we'd
raise a validation error.

Alternatives
------------

The alternative is basically client-side munging of templates, which would
work, but makes the templates much less portable (e.g we'll end up
implementing a TripleO specific solution to this in tripleo-common, which
will result in our environments not working direct to heat via heatclient)


Implementation
==============

Since jdob added support for merging a list of environment_files in
engine/service.py, this should just be a case of adding support for these
optional strategies to the _merge_environments function in that file.

Assignee(s)
-----------

Primary assignee:
  ramishra

Milestones
----------

Target Milestone for completion:
  newton-2

Work Items
----------

- Update heat-engine code to support new optional merge_strategy key
- Comprehensive tests & docs for this new interface
- Add support to heatclient (not to support the merging, just to accept
  the key)

Dependencies
============

None
