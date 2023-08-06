# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ReportDefinitionSummary(object):
    """
    Summary of report definition.
    """

    #: A constant which can be used with the category property of a ReportDefinitionSummary.
    #: This constant has a value of "CUSTOM_REPORTS"
    CATEGORY_CUSTOM_REPORTS = "CUSTOM_REPORTS"

    #: A constant which can be used with the category property of a ReportDefinitionSummary.
    #: This constant has a value of "SUMMARY"
    CATEGORY_SUMMARY = "SUMMARY"

    #: A constant which can be used with the category property of a ReportDefinitionSummary.
    #: This constant has a value of "ACTIVITY_AUDITING"
    CATEGORY_ACTIVITY_AUDITING = "ACTIVITY_AUDITING"

    #: A constant which can be used with the data_source property of a ReportDefinitionSummary.
    #: This constant has a value of "EVENTS"
    DATA_SOURCE_EVENTS = "EVENTS"

    #: A constant which can be used with the data_source property of a ReportDefinitionSummary.
    #: This constant has a value of "ALERTS"
    DATA_SOURCE_ALERTS = "ALERTS"

    #: A constant which can be used with the lifecycle_state property of a ReportDefinitionSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ReportDefinitionSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a ReportDefinitionSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ReportDefinitionSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ReportDefinitionSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    def __init__(self, **kwargs):
        """
        Initializes a new ReportDefinitionSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this ReportDefinitionSummary.
        :type display_name: str

        :param id:
            The value to assign to the id property of this ReportDefinitionSummary.
        :type id: str

        :param category:
            The value to assign to the category property of this ReportDefinitionSummary.
            Allowed values for this property are: "CUSTOM_REPORTS", "SUMMARY", "ACTIVITY_AUDITING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type category: str

        :param description:
            The value to assign to the description property of this ReportDefinitionSummary.
        :type description: str

        :param is_seeded:
            The value to assign to the is_seeded property of this ReportDefinitionSummary.
        :type is_seeded: bool

        :param display_order:
            The value to assign to the display_order property of this ReportDefinitionSummary.
        :type display_order: int

        :param time_created:
            The value to assign to the time_created property of this ReportDefinitionSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ReportDefinitionSummary.
        :type time_updated: datetime

        :param compartment_id:
            The value to assign to the compartment_id property of this ReportDefinitionSummary.
        :type compartment_id: str

        :param data_source:
            The value to assign to the data_source property of this ReportDefinitionSummary.
            Allowed values for this property are: "EVENTS", "ALERTS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type data_source: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ReportDefinitionSummary.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param schedule:
            The value to assign to the schedule property of this ReportDefinitionSummary.
        :type schedule: str

        :param compliance_standards:
            The value to assign to the compliance_standards property of this ReportDefinitionSummary.
        :type compliance_standards: list[str]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ReportDefinitionSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this ReportDefinitionSummary.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'id': 'str',
            'category': 'str',
            'description': 'str',
            'is_seeded': 'bool',
            'display_order': 'int',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'compartment_id': 'str',
            'data_source': 'str',
            'lifecycle_state': 'str',
            'schedule': 'str',
            'compliance_standards': 'list[str]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'id': 'id',
            'category': 'category',
            'description': 'description',
            'is_seeded': 'isSeeded',
            'display_order': 'displayOrder',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'compartment_id': 'compartmentId',
            'data_source': 'dataSource',
            'lifecycle_state': 'lifecycleState',
            'schedule': 'schedule',
            'compliance_standards': 'complianceStandards',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._id = None
        self._category = None
        self._description = None
        self._is_seeded = None
        self._display_order = None
        self._time_created = None
        self._time_updated = None
        self._compartment_id = None
        self._data_source = None
        self._lifecycle_state = None
        self._schedule = None
        self._compliance_standards = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ReportDefinitionSummary.
        Name of the report definition.


        :return: The display_name of this ReportDefinitionSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ReportDefinitionSummary.
        Name of the report definition.


        :param display_name: The display_name of this ReportDefinitionSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ReportDefinitionSummary.
        The OCID of the report definition.


        :return: The id of this ReportDefinitionSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ReportDefinitionSummary.
        The OCID of the report definition.


        :param id: The id of this ReportDefinitionSummary.
        :type: str
        """
        self._id = id

    @property
    def category(self):
        """
        Gets the category of this ReportDefinitionSummary.
        Specifies the name of the category that this report belongs to.

        Allowed values for this property are: "CUSTOM_REPORTS", "SUMMARY", "ACTIVITY_AUDITING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The category of this ReportDefinitionSummary.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this ReportDefinitionSummary.
        Specifies the name of the category that this report belongs to.


        :param category: The category of this ReportDefinitionSummary.
        :type: str
        """
        allowed_values = ["CUSTOM_REPORTS", "SUMMARY", "ACTIVITY_AUDITING"]
        if not value_allowed_none_or_none_sentinel(category, allowed_values):
            category = 'UNKNOWN_ENUM_VALUE'
        self._category = category

    @property
    def description(self):
        """
        Gets the description of this ReportDefinitionSummary.
        A description of the report definition.


        :return: The description of this ReportDefinitionSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ReportDefinitionSummary.
        A description of the report definition.


        :param description: The description of this ReportDefinitionSummary.
        :type: str
        """
        self._description = description

    @property
    def is_seeded(self):
        """
        Gets the is_seeded of this ReportDefinitionSummary.
        Signifies whether the definition is seeded or user defined. Values can either be 'true' or 'false'.


        :return: The is_seeded of this ReportDefinitionSummary.
        :rtype: bool
        """
        return self._is_seeded

    @is_seeded.setter
    def is_seeded(self, is_seeded):
        """
        Sets the is_seeded of this ReportDefinitionSummary.
        Signifies whether the definition is seeded or user defined. Values can either be 'true' or 'false'.


        :param is_seeded: The is_seeded of this ReportDefinitionSummary.
        :type: bool
        """
        self._is_seeded = is_seeded

    @property
    def display_order(self):
        """
        Gets the display_order of this ReportDefinitionSummary.
        Specifies how the report definitions are ordered in the display.


        :return: The display_order of this ReportDefinitionSummary.
        :rtype: int
        """
        return self._display_order

    @display_order.setter
    def display_order(self, display_order):
        """
        Sets the display_order of this ReportDefinitionSummary.
        Specifies how the report definitions are ordered in the display.


        :param display_order: The display_order of this ReportDefinitionSummary.
        :type: int
        """
        self._display_order = display_order

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ReportDefinitionSummary.
        Specifies the time at which the report definition was created.


        :return: The time_created of this ReportDefinitionSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ReportDefinitionSummary.
        Specifies the time at which the report definition was created.


        :param time_created: The time_created of this ReportDefinitionSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this ReportDefinitionSummary.
        The date and time of the report definition update in Data Safe.


        :return: The time_updated of this ReportDefinitionSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ReportDefinitionSummary.
        The date and time of the report definition update in Data Safe.


        :param time_updated: The time_updated of this ReportDefinitionSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ReportDefinitionSummary.
        The OCID of the compartment containing the report definition.


        :return: The compartment_id of this ReportDefinitionSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ReportDefinitionSummary.
        The OCID of the compartment containing the report definition.


        :param compartment_id: The compartment_id of this ReportDefinitionSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def data_source(self):
        """
        Gets the data_source of this ReportDefinitionSummary.
        Specifies the name of a resource that provides data for the report. For example alerts, events.

        Allowed values for this property are: "EVENTS", "ALERTS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The data_source of this ReportDefinitionSummary.
        :rtype: str
        """
        return self._data_source

    @data_source.setter
    def data_source(self, data_source):
        """
        Sets the data_source of this ReportDefinitionSummary.
        Specifies the name of a resource that provides data for the report. For example alerts, events.


        :param data_source: The data_source of this ReportDefinitionSummary.
        :type: str
        """
        allowed_values = ["EVENTS", "ALERTS"]
        if not value_allowed_none_or_none_sentinel(data_source, allowed_values):
            data_source = 'UNKNOWN_ENUM_VALUE'
        self._data_source = data_source

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ReportDefinitionSummary.
        The current state of the audit report.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ReportDefinitionSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ReportDefinitionSummary.
        The current state of the audit report.


        :param lifecycle_state: The lifecycle_state of this ReportDefinitionSummary.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def schedule(self):
        """
        Gets the schedule of this ReportDefinitionSummary.
        The schedule to generate the report periodically in the specified format:
        <version-string>;<version-specific-schedule>

        Allowed version strings - \"v1\"
        v1's version specific schedule -<ss> <mm> <hh> <day-of-week> <day-of-month>
        Each of the above fields potentially introduce constraints. A work request is created only
        when clock time satisfies all the constraints. Constraints introduced:
        1. seconds = <ss> (So, the allowed range for <ss> is [0, 59])
        2. minutes = <mm> (So, the allowed range for <mm> is [0, 59])
        3. hours = <hh> (So, the allowed range for <hh> is [0, 23])
        4. <day-of-week> can be either '*' (without quotes or a number between 1(Monday) and 7(Sunday))
        No constraint introduced when it is '*'. When not, day of week must equal the given value.
        5. <day-of-month> can be either '*' (without quotes or a number between 1 and 28)
        No constraint introduced when it is '*'. When not, day of month must equal the given value


        :return: The schedule of this ReportDefinitionSummary.
        :rtype: str
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """
        Sets the schedule of this ReportDefinitionSummary.
        The schedule to generate the report periodically in the specified format:
        <version-string>;<version-specific-schedule>

        Allowed version strings - \"v1\"
        v1's version specific schedule -<ss> <mm> <hh> <day-of-week> <day-of-month>
        Each of the above fields potentially introduce constraints. A work request is created only
        when clock time satisfies all the constraints. Constraints introduced:
        1. seconds = <ss> (So, the allowed range for <ss> is [0, 59])
        2. minutes = <mm> (So, the allowed range for <mm> is [0, 59])
        3. hours = <hh> (So, the allowed range for <hh> is [0, 23])
        4. <day-of-week> can be either '*' (without quotes or a number between 1(Monday) and 7(Sunday))
        No constraint introduced when it is '*'. When not, day of week must equal the given value.
        5. <day-of-month> can be either '*' (without quotes or a number between 1 and 28)
        No constraint introduced when it is '*'. When not, day of month must equal the given value


        :param schedule: The schedule of this ReportDefinitionSummary.
        :type: str
        """
        self._schedule = schedule

    @property
    def compliance_standards(self):
        """
        Gets the compliance_standards of this ReportDefinitionSummary.
        The list of data protection regulations/standards used in the report that will help demonstrate compliance.


        :return: The compliance_standards of this ReportDefinitionSummary.
        :rtype: list[str]
        """
        return self._compliance_standards

    @compliance_standards.setter
    def compliance_standards(self, compliance_standards):
        """
        Sets the compliance_standards of this ReportDefinitionSummary.
        The list of data protection regulations/standards used in the report that will help demonstrate compliance.


        :param compliance_standards: The compliance_standards of this ReportDefinitionSummary.
        :type: list[str]
        """
        self._compliance_standards = compliance_standards

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this ReportDefinitionSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this ReportDefinitionSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this ReportDefinitionSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this ReportDefinitionSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this ReportDefinitionSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this ReportDefinitionSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this ReportDefinitionSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this ReportDefinitionSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
