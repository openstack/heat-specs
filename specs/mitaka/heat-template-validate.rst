..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================
Heat template-validate improvements
===================================

https://blueprints.launchpad.net/heat/+spec/heat-template-validate-improvements

Improves the validation of template feature to be more easier and customizable.

Problem description
===================

Template validation in heat needs be improved for following reasons:

1. Heat aborts the validation of template on first occurrence of the error.
It makes user to validate template and trial-and-error approach and may goes
for many iterations.

2. Heat does not report the line number at which the error occurred. Sometime,
it causes difficulties to user to spot the issue especially in big templates.

3. Heat aborts the template validation when corresponding service is not
available in the heat cloud. So user like template designer/architects needs
to install all required services in heat cloud to validate it though their
intention is creating valid template.

4. Sometime user wants to validate only the schematic of the template without
bother about the values used for properties. This will help the user to
create 'proper template'

5. There is no option to provide the recommendation when user uses deprecated
one, use the alternate new one.

Proposed change
===============

These issues or improvements could be implemented as below:

Validate template and report warnings and errors in the template as whole
instead of failing on the first error. The output will be provided with new
sections called 'errors' and 'warnings' in list format as provided below.
And provide an option to continue on the error as below. If the option
ignore-errors is empty, all the errors will be ignored, otherwise, it
will ignore only those list of errors specified. This will solve the
first and third problem mentioned above.

``template-validate --ignore-errors``

.. code-block:: yaml

   errors:
    - 10 ERR100 some error occurred.
   warnings:
    - 10 WARN100 some warning occurred.

Provide the line number at which the warnings or errors reported in the form
of '<line number> [ERRxxx|WARNxxx] <error title>'. Here errors are like
validation error and warnings are like deprecated details, and any
recommendation resources wants to provide for a given property in a resource.
This will solve the second problem mentioned above.

Provide the option to validate only the schematic of the template, which
ignores the validation of value. This will help the user to identify the
issues in the structure of the template. This could be as below, and this
will solve the fourth problem mentioned above:

``template-validate --only-schematics``

By default report all the deprecated warnings as part of validation. In case
user wants to ignore some warnings, provide an option similar to ignore-errors
as below. If there is no warnings provided, then all the warning will be
reported, otherwise, only those warnings given will be ignored. This will
solve the fifth problem.

``template-validate --ignore-warnings``

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:

kanagaraj-manickam
ishant-tyagi

Milestones
----------

Target Milestone for completion:
  mitaka-1

Work Items
----------

* Tag the user visible HeatException with proper error code like 'HExxx'

* Improve the validate_template() method in heat.engine.service module
  to  capture all the errors and warnings like deprecated.

* while reporting, if some of these errors are part of ignore-errors list,
   those can be removed from the output response.

* if report-deprecated option is not provided, then ignore those deprecated
   warning from the output response.

* Improve the validate_template() method to validate the template based on
  the required output like parameters, parameter_groups, description and
  resources. Optimally preview_stack() method needs to be utilized in place
  of resources output

* Improve the validate_template() method to avoid the constrain validation
  if the option only-schematics is provided.

* Improve the cli to parse the response and print the output in yaml or json
  appropriately.

* Add required test cases


Dependencies
============

None
