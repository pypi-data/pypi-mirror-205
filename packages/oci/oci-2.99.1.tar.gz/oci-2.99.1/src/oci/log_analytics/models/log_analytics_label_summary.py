# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LogAnalyticsLabelSummary(object):
    """
    LogAnalytics label
    """

    #: A constant which can be used with the priority property of a LogAnalyticsLabelSummary.
    #: This constant has a value of "NONE"
    PRIORITY_NONE = "NONE"

    #: A constant which can be used with the priority property of a LogAnalyticsLabelSummary.
    #: This constant has a value of "LOW"
    PRIORITY_LOW = "LOW"

    #: A constant which can be used with the priority property of a LogAnalyticsLabelSummary.
    #: This constant has a value of "MEDIUM"
    PRIORITY_MEDIUM = "MEDIUM"

    #: A constant which can be used with the priority property of a LogAnalyticsLabelSummary.
    #: This constant has a value of "HIGH"
    PRIORITY_HIGH = "HIGH"

    #: A constant which can be used with the type property of a LogAnalyticsLabelSummary.
    #: This constant has a value of "INFO"
    TYPE_INFO = "INFO"

    #: A constant which can be used with the type property of a LogAnalyticsLabelSummary.
    #: This constant has a value of "PROBLEM"
    TYPE_PROBLEM = "PROBLEM"

    def __init__(self, **kwargs):
        """
        Initializes a new LogAnalyticsLabelSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param aliases:
            The value to assign to the aliases property of this LogAnalyticsLabelSummary.
        :type aliases: list[oci.log_analytics.models.LogAnalyticsLabelAlias]

        :param count_usage_in_source:
            The value to assign to the count_usage_in_source property of this LogAnalyticsLabelSummary.
        :type count_usage_in_source: int

        :param suggest_type:
            The value to assign to the suggest_type property of this LogAnalyticsLabelSummary.
        :type suggest_type: int

        :param description:
            The value to assign to the description property of this LogAnalyticsLabelSummary.
        :type description: str

        :param display_name:
            The value to assign to the display_name property of this LogAnalyticsLabelSummary.
        :type display_name: str

        :param edit_version:
            The value to assign to the edit_version property of this LogAnalyticsLabelSummary.
        :type edit_version: int

        :param impact:
            The value to assign to the impact property of this LogAnalyticsLabelSummary.
        :type impact: str

        :param is_system:
            The value to assign to the is_system property of this LogAnalyticsLabelSummary.
        :type is_system: bool

        :param name:
            The value to assign to the name property of this LogAnalyticsLabelSummary.
        :type name: str

        :param priority:
            The value to assign to the priority property of this LogAnalyticsLabelSummary.
            Allowed values for this property are: "NONE", "LOW", "MEDIUM", "HIGH", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type priority: str

        :param recommendation:
            The value to assign to the recommendation property of this LogAnalyticsLabelSummary.
        :type recommendation: str

        :param type:
            The value to assign to the type property of this LogAnalyticsLabelSummary.
            Allowed values for this property are: "INFO", "PROBLEM", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param is_user_deleted:
            The value to assign to the is_user_deleted property of this LogAnalyticsLabelSummary.
        :type is_user_deleted: bool

        """
        self.swagger_types = {
            'aliases': 'list[LogAnalyticsLabelAlias]',
            'count_usage_in_source': 'int',
            'suggest_type': 'int',
            'description': 'str',
            'display_name': 'str',
            'edit_version': 'int',
            'impact': 'str',
            'is_system': 'bool',
            'name': 'str',
            'priority': 'str',
            'recommendation': 'str',
            'type': 'str',
            'is_user_deleted': 'bool'
        }

        self.attribute_map = {
            'aliases': 'aliases',
            'count_usage_in_source': 'countUsageInSource',
            'suggest_type': 'suggestType',
            'description': 'description',
            'display_name': 'displayName',
            'edit_version': 'editVersion',
            'impact': 'impact',
            'is_system': 'isSystem',
            'name': 'name',
            'priority': 'priority',
            'recommendation': 'recommendation',
            'type': 'type',
            'is_user_deleted': 'isUserDeleted'
        }

        self._aliases = None
        self._count_usage_in_source = None
        self._suggest_type = None
        self._description = None
        self._display_name = None
        self._edit_version = None
        self._impact = None
        self._is_system = None
        self._name = None
        self._priority = None
        self._recommendation = None
        self._type = None
        self._is_user_deleted = None

    @property
    def aliases(self):
        """
        Gets the aliases of this LogAnalyticsLabelSummary.
        The alias list.


        :return: The aliases of this LogAnalyticsLabelSummary.
        :rtype: list[oci.log_analytics.models.LogAnalyticsLabelAlias]
        """
        return self._aliases

    @aliases.setter
    def aliases(self, aliases):
        """
        Sets the aliases of this LogAnalyticsLabelSummary.
        The alias list.


        :param aliases: The aliases of this LogAnalyticsLabelSummary.
        :type: list[oci.log_analytics.models.LogAnalyticsLabelAlias]
        """
        self._aliases = aliases

    @property
    def count_usage_in_source(self):
        """
        Gets the count_usage_in_source of this LogAnalyticsLabelSummary.
        The source usage count for this label.


        :return: The count_usage_in_source of this LogAnalyticsLabelSummary.
        :rtype: int
        """
        return self._count_usage_in_source

    @count_usage_in_source.setter
    def count_usage_in_source(self, count_usage_in_source):
        """
        Sets the count_usage_in_source of this LogAnalyticsLabelSummary.
        The source usage count for this label.


        :param count_usage_in_source: The count_usage_in_source of this LogAnalyticsLabelSummary.
        :type: int
        """
        self._count_usage_in_source = count_usage_in_source

    @property
    def suggest_type(self):
        """
        Gets the suggest_type of this LogAnalyticsLabelSummary.
        The type of suggestion for label usage.


        :return: The suggest_type of this LogAnalyticsLabelSummary.
        :rtype: int
        """
        return self._suggest_type

    @suggest_type.setter
    def suggest_type(self, suggest_type):
        """
        Sets the suggest_type of this LogAnalyticsLabelSummary.
        The type of suggestion for label usage.


        :param suggest_type: The suggest_type of this LogAnalyticsLabelSummary.
        :type: int
        """
        self._suggest_type = suggest_type

    @property
    def description(self):
        """
        Gets the description of this LogAnalyticsLabelSummary.
        The label description.


        :return: The description of this LogAnalyticsLabelSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this LogAnalyticsLabelSummary.
        The label description.


        :param description: The description of this LogAnalyticsLabelSummary.
        :type: str
        """
        self._description = description

    @property
    def display_name(self):
        """
        Gets the display_name of this LogAnalyticsLabelSummary.
        The label display name.


        :return: The display_name of this LogAnalyticsLabelSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this LogAnalyticsLabelSummary.
        The label display name.


        :param display_name: The display_name of this LogAnalyticsLabelSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def edit_version(self):
        """
        Gets the edit_version of this LogAnalyticsLabelSummary.
        The label edit version.


        :return: The edit_version of this LogAnalyticsLabelSummary.
        :rtype: int
        """
        return self._edit_version

    @edit_version.setter
    def edit_version(self, edit_version):
        """
        Sets the edit_version of this LogAnalyticsLabelSummary.
        The label edit version.


        :param edit_version: The edit_version of this LogAnalyticsLabelSummary.
        :type: int
        """
        self._edit_version = edit_version

    @property
    def impact(self):
        """
        Gets the impact of this LogAnalyticsLabelSummary.
        The label impact.


        :return: The impact of this LogAnalyticsLabelSummary.
        :rtype: str
        """
        return self._impact

    @impact.setter
    def impact(self, impact):
        """
        Sets the impact of this LogAnalyticsLabelSummary.
        The label impact.


        :param impact: The impact of this LogAnalyticsLabelSummary.
        :type: str
        """
        self._impact = impact

    @property
    def is_system(self):
        """
        Gets the is_system of this LogAnalyticsLabelSummary.
        The system flag.  A value of false denotes a custom, or user
        defined label.  A value of true denotes a built in label.


        :return: The is_system of this LogAnalyticsLabelSummary.
        :rtype: bool
        """
        return self._is_system

    @is_system.setter
    def is_system(self, is_system):
        """
        Sets the is_system of this LogAnalyticsLabelSummary.
        The system flag.  A value of false denotes a custom, or user
        defined label.  A value of true denotes a built in label.


        :param is_system: The is_system of this LogAnalyticsLabelSummary.
        :type: bool
        """
        self._is_system = is_system

    @property
    def name(self):
        """
        Gets the name of this LogAnalyticsLabelSummary.
        The label name.


        :return: The name of this LogAnalyticsLabelSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this LogAnalyticsLabelSummary.
        The label name.


        :param name: The name of this LogAnalyticsLabelSummary.
        :type: str
        """
        self._name = name

    @property
    def priority(self):
        """
        Gets the priority of this LogAnalyticsLabelSummary.
        The label priority. Valid values are (NONE, LOW, HIGH). NONE is default.

        Allowed values for this property are: "NONE", "LOW", "MEDIUM", "HIGH", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The priority of this LogAnalyticsLabelSummary.
        :rtype: str
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """
        Sets the priority of this LogAnalyticsLabelSummary.
        The label priority. Valid values are (NONE, LOW, HIGH). NONE is default.


        :param priority: The priority of this LogAnalyticsLabelSummary.
        :type: str
        """
        allowed_values = ["NONE", "LOW", "MEDIUM", "HIGH"]
        if not value_allowed_none_or_none_sentinel(priority, allowed_values):
            priority = 'UNKNOWN_ENUM_VALUE'
        self._priority = priority

    @property
    def recommendation(self):
        """
        Gets the recommendation of this LogAnalyticsLabelSummary.
        The label recommendation.


        :return: The recommendation of this LogAnalyticsLabelSummary.
        :rtype: str
        """
        return self._recommendation

    @recommendation.setter
    def recommendation(self, recommendation):
        """
        Sets the recommendation of this LogAnalyticsLabelSummary.
        The label recommendation.


        :param recommendation: The recommendation of this LogAnalyticsLabelSummary.
        :type: str
        """
        self._recommendation = recommendation

    @property
    def type(self):
        """
        Gets the type of this LogAnalyticsLabelSummary.
        The label type.  Valid values are (INFO, PROBLEM). INFO is default.

        Allowed values for this property are: "INFO", "PROBLEM", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this LogAnalyticsLabelSummary.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this LogAnalyticsLabelSummary.
        The label type.  Valid values are (INFO, PROBLEM). INFO is default.


        :param type: The type of this LogAnalyticsLabelSummary.
        :type: str
        """
        allowed_values = ["INFO", "PROBLEM"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def is_user_deleted(self):
        """
        Gets the is_user_deleted of this LogAnalyticsLabelSummary.
        A flag indicating whether or not the label has been deleted.


        :return: The is_user_deleted of this LogAnalyticsLabelSummary.
        :rtype: bool
        """
        return self._is_user_deleted

    @is_user_deleted.setter
    def is_user_deleted(self, is_user_deleted):
        """
        Sets the is_user_deleted of this LogAnalyticsLabelSummary.
        A flag indicating whether or not the label has been deleted.


        :param is_user_deleted: The is_user_deleted of this LogAnalyticsLabelSummary.
        :type: bool
        """
        self._is_user_deleted = is_user_deleted

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
