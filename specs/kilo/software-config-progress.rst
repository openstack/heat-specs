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
 For help with syntax, see http://sphinx-doc.org/rest.html To test out your
 formatting, see http://www.tele3.cz/jbar/rest/rest.html

==========================================
Software config notify deployment progress
==========================================

https://blueprints.launchpad.net/heat/+spec/software-config-progress

Currently when a deployment resource remains IN_PROGRESS there is no way of
knowing whether configuration is taking a long time, or if an unrelated
problem occured before or after. The only option is to ssh into a server to
diagnose the issue. This blueprint proposes that the server signal to heat
when any deployment activity starts.

Problem description
===================

Currently when a deployment resource remains IN_PROGRESS the configuration may
be taking a legitimately long time. In other cases there may be a failure due
to one of the following problems.

The potential problems during server boot include:

1. Nova says the server has booted but the image failed to actually boot

2. The server booted, but was not successfully assigned an IP address

3. Nova metadata server cannot be reached on boot to poll for initial metadata

The potential problems which occur after boot but before a specific deployment
is executed include:

4. Misconfiguration in the installed server agent, hooks and config tools

5. Failure to poll deployment metadata from heat (or other configured polling
source)

And finally the potential problems when actually executing the deployment:

6. Inability for the server to signal the results back to heat, either due to
authentication or connectivity issues.

Currently there is no feedback that the actual deployment has started. If the
user had earlier feedback that deployment has started then they can eliminate
the above six failures as the cause of the deployment being IN_PROGRESS.

Proposed change
===============

Currently SoftwareDeployment.signal assumes that as soon as a signal is
received the deployment task is complete. This will be changed so that the
signal details are checked for extra data which indicates that this is an
IN_PROGRESS signal rather than a COMPLETE/FAILED signal. The software-config
hooks will be modified to send an IN_PROGRESS signal before they start the
deployment task.

The signal details are currently a JSON map with entries for each output
value, plus ``deploy_stdout``, ``deploy_stderr`` and ``deploy_status_code``.
Two new entries will be expected, ``deploy_status`` and
``deploy_status_reason``. SoftwareDeployment.signal will check for this and
if ``deploy_status`` is ``IN_PROGRESS`` then the deployment resource will
remain in an IN_PROGRESS state. However there will be a resource event
generated to give the user some feedback that their deployment task has
started.

Backwards-compatibility concerns need to be considered both with old images
running on new heat, and new images running on old heat.

Old image, new heat
-------------------

There is nothing special to consider here. The server will not signal heat
that a deployment is starting, but the deployment resource will already be in
an IN_PROGRESS state. The only implication is that the user will not see the
extra IN_PROGRESS event telling them that the deployment has started.

New image, old heat
-------------------

Since old heat assumes that the deployment is complete as soon as a signal is
received, the hooks need to suppress sending any IN_PROGRESS signals. This
can be achieved by the hooks checking for the input ``deploy_status_aware``
being set to ``true``. Only new heat will set this input value to ``true`` so
the hook can check this input and behave accordingly.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <steve-stevebaker>

Milestones
----------

Target Milestone for completion:
  Kilo-1

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different
people, but we're mostly trying to understand the timeline for implementation.


Dependencies
============

There are no blueprint or library dependencies for this blueprint
