# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RuleSummary(object):
    """
    The summary details of rules for Events. For more information, see
    `Managing Rules for Events`__.

    __ https://docs.cloud.oracle.com/iaas/Content/Events/Task/managingrules.htm
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RuleSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this RuleSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this RuleSummary.
        :type display_name: str

        :param description:
            The value to assign to the description property of this RuleSummary.
        :type description: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this RuleSummary.
        :type lifecycle_state: str

        :param condition:
            The value to assign to the condition property of this RuleSummary.
        :type condition: str

        :param compartment_id:
            The value to assign to the compartment_id property of this RuleSummary.
        :type compartment_id: str

        :param is_enabled:
            The value to assign to the is_enabled property of this RuleSummary.
        :type is_enabled: bool

        :param time_created:
            The value to assign to the time_created property of this RuleSummary.
        :type time_created: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this RuleSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this RuleSummary.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'description': 'str',
            'lifecycle_state': 'str',
            'condition': 'str',
            'compartment_id': 'str',
            'is_enabled': 'bool',
            'time_created': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'description': 'description',
            'lifecycle_state': 'lifecycleState',
            'condition': 'condition',
            'compartment_id': 'compartmentId',
            'is_enabled': 'isEnabled',
            'time_created': 'timeCreated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._display_name = None
        self._description = None
        self._lifecycle_state = None
        self._condition = None
        self._compartment_id = None
        self._is_enabled = None
        self._time_created = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this RuleSummary.
        The `OCID`__ of this rule.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this RuleSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this RuleSummary.
        The `OCID`__ of this rule.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this RuleSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this RuleSummary.
        A string that describes the rule. It does not have to be unique, and you can change it. Avoid entering
        confidential information.

        Example: `\"This rule sends a notification upon completion of DbaaS backup.\"`


        :return: The display_name of this RuleSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this RuleSummary.
        A string that describes the rule. It does not have to be unique, and you can change it. Avoid entering
        confidential information.

        Example: `\"This rule sends a notification upon completion of DbaaS backup.\"`


        :param display_name: The display_name of this RuleSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this RuleSummary.
        A string that describes the details of the rule. It does not have to be unique, and you can change it. Avoid entering
        confidential information.


        :return: The description of this RuleSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this RuleSummary.
        A string that describes the details of the rule. It does not have to be unique, and you can change it. Avoid entering
        confidential information.


        :param description: The description of this RuleSummary.
        :type: str
        """
        self._description = description

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this RuleSummary.

        :return: The lifecycle_state of this RuleSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this RuleSummary.

        :param lifecycle_state: The lifecycle_state of this RuleSummary.
        :type: str
        """
        self._lifecycle_state = lifecycle_state

    @property
    def condition(self):
        """
        **[Required]** Gets the condition of this RuleSummary.
        A filter that specifies the event that will trigger actions associated with this rule. A few
        important things to remember about filters:

        * Fields not mentioned in the condition are ignored. You can create a valid filter that matches
        all events with two curly brackets: `{}`

          For more examples, see
        `Matching Events with Filters`__.
        * For a condition with fields to match an event, the event must contain all the field names
        listed in the condition. Field names must appear in the condition with the same nesting
        structure used in the event.

          For a list of reference events, see
        `Services that Produce Events`__.
        * Rules apply to events in the compartment in which you create them and any child compartments.
        This means that a condition specified by a rule only matches events emitted from resources in
        the compartment or any of its child compartments.
        * Wildcard matching is supported with the asterisk (*) character.

          For examples of wildcard matching, see
        `Matching Events with Filters`__

        Example: `\\\"eventType\\\": \\\"com.oraclecloud.databaseservice.autonomous.database.backup.end\\\"`

        __ https://docs.cloud.oracle.com/iaas/Content/Events/Concepts/filterevents.htm
        __ https://docs.cloud.oracle.com/iaas/Content/Events/Reference/eventsproducers.htm
        __ https://docs.cloud.oracle.com/iaas/Content/Events/Concepts/filterevents.htm


        :return: The condition of this RuleSummary.
        :rtype: str
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """
        Sets the condition of this RuleSummary.
        A filter that specifies the event that will trigger actions associated with this rule. A few
        important things to remember about filters:

        * Fields not mentioned in the condition are ignored. You can create a valid filter that matches
        all events with two curly brackets: `{}`

          For more examples, see
        `Matching Events with Filters`__.
        * For a condition with fields to match an event, the event must contain all the field names
        listed in the condition. Field names must appear in the condition with the same nesting
        structure used in the event.

          For a list of reference events, see
        `Services that Produce Events`__.
        * Rules apply to events in the compartment in which you create them and any child compartments.
        This means that a condition specified by a rule only matches events emitted from resources in
        the compartment or any of its child compartments.
        * Wildcard matching is supported with the asterisk (*) character.

          For examples of wildcard matching, see
        `Matching Events with Filters`__

        Example: `\\\"eventType\\\": \\\"com.oraclecloud.databaseservice.autonomous.database.backup.end\\\"`

        __ https://docs.cloud.oracle.com/iaas/Content/Events/Concepts/filterevents.htm
        __ https://docs.cloud.oracle.com/iaas/Content/Events/Reference/eventsproducers.htm
        __ https://docs.cloud.oracle.com/iaas/Content/Events/Concepts/filterevents.htm


        :param condition: The condition of this RuleSummary.
        :type: str
        """
        self._condition = condition

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this RuleSummary.
        The `OCID`__ of the compartment to which this rule belongs.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this RuleSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this RuleSummary.
        The `OCID`__ of the compartment to which this rule belongs.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this RuleSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def is_enabled(self):
        """
        **[Required]** Gets the is_enabled of this RuleSummary.
        Whether or not this rule is currently enabled.

        Example: `true`


        :return: The is_enabled of this RuleSummary.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this RuleSummary.
        Whether or not this rule is currently enabled.

        Example: `true`


        :param is_enabled: The is_enabled of this RuleSummary.
        :type: bool
        """
        self._is_enabled = is_enabled

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this RuleSummary.
        The time this rule was created, expressed in `RFC 3339`__
        timestamp format.

        Example: `2018-09-12T22:47:12.613Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this RuleSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this RuleSummary.
        The time this rule was created, expressed in `RFC 3339`__
        timestamp format.

        Example: `2018-09-12T22:47:12.613Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this RuleSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this RuleSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. Exists for cross-compatibility only.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this RuleSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this RuleSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. Exists for cross-compatibility only.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this RuleSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this RuleSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this RuleSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this RuleSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this RuleSummary.
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
