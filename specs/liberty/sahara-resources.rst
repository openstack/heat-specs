..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


==============================
Implement Sahara EDP resources
==============================

https://blueprints.launchpad.net/heat/+spec/sahara-edp

Add support for Job, JobBinary and DataSource sahara objects as resources
in heat.

Using sahara EDP in heat we can create following resources:

  * ``Data source`` object stores a URL which designates the location of input
    or output data and any credentials needed to access the location;
  * ``Job binary`` object stores a URL to a single script or Jar file and any
    credentials needed to retrieve the file;
  * ``Job`` object specifies the type of the job and lists all of the
    individual ``job binary`` objects. Can be launched using resource-signal.

Problem description
===================

Currently we can't create Sahara EDP resources in Heat.

Proposed change
===============

Implement following resource types:

1. OS::Sahara::DataSource

  Properties:

  * name (optional) - name of the data source
  * type (required) - type of the data source
  * url (required) - URL for the data source
  * description (optional) - description of the data source
  * user (optional) - username for accessing the data source URL
  * password (optional) - password for accessing the data source URL

2. OS::Sahara::JobBinary

  Properties:

  * name (optional) - name of the job binary
  * url (required) - URL for the job binary
  * description (optional) - description of the job binary
  * user (optional) - username for accessing the job binary URL
  * password (optional) - password for accessing the job binary URL

3. OS::Sahara::Job

  Properties:

  * name (optional) - name of the job
  * type (required) - type of the job
  * main (optional) - ID for job's main job-binary
  * lib (list, optional) - ID of job's lib job-binary
  * description (optional) - description of the job

  Attributes:

  * executions - list of the job executions

  To execute the job run the following command::

    heat resource-signal stack_name job_name -D <data>

  ``data`` contains execution details including data sources, configuration
  values, and program arguments.

Alternatives
------------

None


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  tlashchova

Milestones
----------

Target Milestone for completion:
  Liberty-3

Work Items
----------

* Add Sahara data source resource
* Add Sahara job binary resource
* Add Sahara job resource
* Add required test cases
* Add sample templates in heat-template project

Dependencies
============

None
