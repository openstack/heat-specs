..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================
Stack Breakpoint
================

https://blueprints.launchpad.net/heat/+spec/stack-breakpoint

Orchestration template is a powerful automation tool when it works;  however
when it fails, troubleshooting can be quite difficult. During development,
debugging failed template is simply part of the process, but in production,
a previously working template can also fail for many reasons. Providing support
for troubleshooting template will not only increase productivity but will also
help the adoption of Heat template by allowing users to "look under the hood"
and have a better handle on the automation.

Typically, the user would start by checking the logs to get some bearing on
the error.  If possible, the user may try to enhance the logs by adding more
log message in the script.  This initial approach should resolve many errors,
but difficult error may require more active debugging.  The user would need to
stop at or before the point of template failure, inspect variables, check the
environment, run command or script manually, etc.  Since the template is 
declarative, the user would need to be able to recreate the error consistently.

Support for troubleshooting is broad and will require many blueprints to
implement the different features to control the template flow, recreate the
error, and inspect the elements.  Related blueprints include
troubleshooting-low-level-control_, resolve-failed-stack-attributes_,
user-visible-logs_, user-friendly-template-errors_.  This blueprint covers the
particular scenario of how to better control the stack deployment while
troubleshooting.

.. _troubleshooting-low-level-control: https://blueprints.launchpad.net/heat/+spec/troubleshooting-low-level-control
.. _resolve-failed-stack-attributes: https://blueprints.launchpad.net/heat/+spec/resolve-failed-stack-attributes
.. _user-visible-logs: https://blueprints.launchpad.net/heat/+spec/user-visible-logs
.. _user-friendly-template-errors: https://blueprints.launchpad.net/heat/+spec/user-friendly-template-errors

Problem description
===================

With a failing stack, currently we can stop on the point of failure by
disabling rollback:  the stack will stop when a resource fails, leaving in
place the resources that have been created successfully.  There may be some
false failures because some resources may be aborted, but they can be easily
identified by displaying the state of the resource.  This technique works well
for troubleshooting stack-create;  stack-update can be handled similarly once
the blueprint update-failure-recovery is implemented.

In many cases however, the point of failure may be too late or too hard to
debug because the original cause of the failure may not be obvious or the
environment may have been changed.  If we can pause the stack at a point before
the failure, then we are in a better position to troubleshoot.  For instance,
we can check whether the state of the environment and the stack is what we
expect, we can manually run the next step to see how it fails, etc.

While developing new template or resource type, it is also useful to bring up
a stack to a point before the new code is to be executed.  Then the developer
can manually execute and debug the new code.


Proposed change
===============

The usage would be as follows:

- Run stack-create or stack-update with one or more resource name specified
  as breakpoint, for example:

	heat stack-create my_stack --template-file my_template.yaml
	--breakpoint failing_resource_name

	heat stack-update my_stack --template-file my_template.yaml
	--breakpoint failing_resource_name

- The breakpoint can also be coded in the environment file pointing to
  a particular resource, for example:

	breakpoints:
	  resource: failing_resource_name

- As the engine traverses down the dependency graph, it would stop at the
  breakpoint resource and all dependent resources.  Other resources with no
  dependency will proceed to completion before stopping.  Multiple breakpoints
  can be set to control parallel paths in the graph.

- Running resource-list or resource-show will show the resource at the
  breakpoint as "CREATE.INPROGRESS" or "UPDATE.INPROGRESS" and the resource
  is not created or updated yet.  Running event-list will show that the
  breakpoint has occurred, and event-show will give more details on the
  breakpoint.

- The breakpoint can be deleted on the command line by:

	heat stack-update my_stack --template-file my_template.yaml
	--nobreakpoint failing_resource_name

- In the environment file, the breakpoint can be deleted simply by deleting
  the resource name in the breakpoint property.  This would take effect the
  next time the environment file is specified on stack-update.  The user
  is probably more likely to use the command line option.

- After debugging, continue the stack by (done manually, but can also be
  automated by a high level debugger):

    - Stepping: remove current breakpoint, set breakpoint for next resource(s)
      in dependency graph, resume stack-create (or stack-update).
    - Running to completion: remove current breakpoint, resume stack-create or
      stack-update by running stack-update with the same
      template and parameters.

For nested stack, the breakpoint would be prefixed with the name of the
nested template.

The change will include the heat client, api and environment to add the
breakpoint option.
For the Heat engine to stop at a resource, we will leverage the blueprint
lifecycle-callbacks_.  Some code to set up and interface with the callback
will be needed and the details will be determined when this blueprint is
implemented.

.. _lifecycle-callbacks: https://wiki.openstack.org/wiki/Heat/Blueprints/lifecycle-callbacks

Alternatives
------------

The manual approach is simply to edit the template and delete any failing
resources until the remaining resources can be created successfully.
Then stepping each resource can be done by adding it back to the template and
running stack-update.  The full stack will need to be deleted and recreated
for each iteration.
This manual technique cannot be incorporated into high level tool.


Implementation
==============
Assignee(s)
-----------
Primary assignee:
  Ton Ngo

Milestones
----------
Target Milestone for completion:
    Juno-3 or further


Work Items
----------

- Heat client:  add option to specify breakpoint
- Heat API:  add option to specify breakpoint
- Environment:  add option to specify breakpoint
- Interface with lifecycle-callbacks_

.. lifecycle-callbacks_: https://wiki.openstack.org/wiki/Heat/Blueprints/lifecycle-callbacks


Dependencies
============
https://wiki.openstack.org/wiki/Heat/Blueprints/lifecycle-callbacks

