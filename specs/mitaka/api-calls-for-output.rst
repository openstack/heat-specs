..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


==========================
API calls for stack output
==========================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/heat/+spec/api-call-output

Current Orchestration API has no special calls for showing and listing
stack output. Also, CLI commands output-show and output-list have to call
stack.get for resolving output, which is not correct.

Problem description
===================

Current output-show and output-list CLI commands implemented only in heat
client, they have to request stack.get, which load stack from database and
resolve all outputs, which can slow down command execution. So need to add
possibility to get desired outputs without resolving all outputs. It can
be done with adding new methods to heat engine, which will resolve only
specified outputs.

Proposed change
===============

The changes involves next steps:

 * Adding new functionality to heat service, which will implements showing and
   listing stack outputs. Moreover, output show should resolve only specified
   output;

 * Adding new API calls for showing specified stack output and listing all
   stack outputs.

   API for showing stack output will looks like::

     /stacks/{stack_name}/{stack_id}/outputs/{output_key}

   and will return next response::

      {
          "output": {
              "output_key": <output_key>,
              "output_value": <output_value>,
              "description": <description>
          }
      }

   API for listing stack outputs will looks like::

     /stacks/{stack_name}/{stack_id}/outputs/

   and will return next response::

      {
          "outputs": [
              ...
          ]
      }

 * Change output-show and output-list for heat client, which should call
   special API for showing output and listing output instead of calling
   stack.get and resolving outputs from it's response.

 * Add new API to API ref documentation (project api-site_).

 * Add corresponding API tests to tempest and heat client functional tests.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <prazumovsky>
  <ochuprykov>

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

* Add new methods to heat service for showing and listing outputs for stack.
* Add new API calls for showing and listing outputs for stack.
* Change output-show and output-list heat client methods with new APIs.
* Add new API to API ref documentation.
* Add corresponding API tests to tempest and heat client functional tests.


Dependencies
============

None

.. _api-site: https://github.com/openstack/api-site
