..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

===================================
 Add lock and unlock stack actions
===================================

https://blueprints.launchpad.net/heat/+spec/lock-stack

As application vendors deploy their applications using heat stacks, they
can currently use automatic processes such as ceilometer alarms,
auto-scaling groups, etc..., as well as manual processes such as stack-update.
In some cases ,for example manual maintenance of the application,
actions done on the stack can interrupt and prolong the maintenance period.
A lock on the stack to disable and block these types of processes should
solve this issue.


Problem description
===================

use cases:

1. application vendors are interested in a "maintenance mode" for their
application. When in maintenance no topology changes are permitted.
For example a maintenance mode is required for a clustered DB app that needs a
manual reboot of one of its servers - when the server reboots
all the other servers are redistributing the data among themselves which causes
high CPU levels which in turn might cause an undesired scale
out (which will cause another CPU spike and so on...).

2. some cloud-admins have a configuration stack that initializes the cloud
(Creating networks, flavors, images, ...) and these resources should always
exist while the cloud exists. Locking these configuration stacks, will
prevent someone from accidentally deleting/modifying the stack or its resources
.

This feature might even raise in significance, once convergence phase 2 is in
place, and many other automatic actions are performed by heat. The ability to
manually perform admin actions on the stack with no interruptions is important.


Proposed change
===============

The proposal is to add a "Lock" operation to be performed on the stack. Similar
to: nova server "lock" or glance-image "--is-protected" flag. Once a stack is
locked, the only operations allowed on the stack is "unlock" or "lock" which
in order to change locking level - heat engine should reject any stack
operations and ignore signals that modify the stack (such as scaling) and
optionally its underlying resources.

This API calls would be additional to the stack-actions API, of 'lock' and
'unlock'.

The lock operation should have a "level" flag with possible values of
{all, stacks} (default = all)
when level = stacks: perform heat lock - which would lock the stack and
all nested stacks (actions on the "physical" resources are still permitted).
this means any action on the stack or it's nested stack will be blocked. but
other stack resources will not be locked.
When level = all: perform heat lock and enable lock/protect for each stack
resource that supports it (nova server, glance image,...).

The lock operation should only be called once the stack is in a final state,
(a state which is not "IN_PROGRESS", not "INIT_COMPLETE" and not
"DELETE_COMPLETE").
when the api call is successful it will return with response code 200.
when calling the api when the stack is in an invalid state it will return a
response code 409.

The unlock operation can only be called on a stack that is either locked or
failed to lock/unlock. The ability to call the unlock api both when locking
or unlocking failed, is important for transient issues that leave the stack
in a "dirty" state and we want to bring it back to it's previous healthy one.

Alternatives
------------
In the future we might want to enable interrupting or rolling
back running processes (such as retry of stack-create or scaling) and
locking the stack, instead of waiting for the running process to finish.

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  noa-koffman
  melisha
  avi-vachnis



Milestones
----------

Target Milestone for completion:
  liberty-1

Work Items
----------

Changes to API:
- Support 'lock' and 'unlock' actions in the existing stack-action API.
- locking a stack, will be called by stack actions api:
HTTP POST /v1/{tenant_id}/stacks/{stack_name}/{stack_id}/actions
with the following body:
{
"lock":{"level": stacks }
}
- unlocking a stack will be called similarly with the following body:
{
"unlock": null
}


Changes to engine:
Develop a lock stack logic in heat which prevents stack actions
(suspend/resume), update-stack, auto-scaling,..., from taking place.
In the future we might add additional locking modes, to enable locking the
stack
from action but allowing auto-scaling or suspend and resume actions.

- the stack's ACTIONS will now contain two new actions ("LOCK" and "UNLOCK")
- new methods will be created for locking and unlocking a stack, which will
    be similar to the suspend and resume methods.
- similarly to the existing (suspend and resume) stack actions, the new
    methods will trigger calls to a "handle_lock" and "handle_unlock" method
    in the stack resources. for resources that will not implement locking,
    this method will not have any actual affect.
- appropriate stack and stack-resources states (LOCK_IN_PROGRESS,
    LOCK_COMPLETE, LOCK_FAILED, UNLOCK_IN_PROGRESS, UNLOCK_COMPLETE,
    UNLOCK_FAILED) should be added.
    allowed actions for each state are as follows:
    LOCK_IN_PROGRESS: none
    LOCK_COMPLETE: unlock, lock (in order to enable changing the locking level)
    LOCK_FAILED: unlock, delete, lock
    UNLOCK_COMPLETED: all actions except for unlock.
    UNLOCK_FAILED: delete, unlock
    UNLOCK_IN_PROGRESS: none
- Any action of the engine on the stack, except unlocking a stack, will
    only start after validating the stack is not locked.
- the engine should validate the stack status is in an appropriate state
    before starting the lock process.

Changes to client:

- action-lock command will be added this will include the "lock resources"
- the action-lock command will allow passing the "level" parameter using a
    "--level" flag (which will be added), similar to stack-create command.
    usage: heat action-lock <Name or ID of stack> --level=stacks
- action-unlock command will be added used the same as action-suspend and
    action-resume, with no parameter flags.
    usage: heat action-unlock <Name or ID of stack>

Documentation changes:

- update developer.openstack.org/api-ref-orchestration-v1.html with the
    additions to stack actions api
- add the lock stack design to wiki.openstack.org
- add the lock and unlock actions to developers api docs:
    in .../heat/sourcecode/heat/heat.api.openstack.v1.actions.html


Dependencies
============

None
