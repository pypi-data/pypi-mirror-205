# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class QueryProperties(object):
    """
    The query properties.
    """

    #: A constant which can be used with the granularity property of a QueryProperties.
    #: This constant has a value of "DAILY"
    GRANULARITY_DAILY = "DAILY"

    #: A constant which can be used with the granularity property of a QueryProperties.
    #: This constant has a value of "MONTHLY"
    GRANULARITY_MONTHLY = "MONTHLY"

    #: A constant which can be used with the query_type property of a QueryProperties.
    #: This constant has a value of "USAGE"
    QUERY_TYPE_USAGE = "USAGE"

    #: A constant which can be used with the query_type property of a QueryProperties.
    #: This constant has a value of "COST"
    QUERY_TYPE_COST = "COST"

    #: A constant which can be used with the query_type property of a QueryProperties.
    #: This constant has a value of "USAGE_AND_COST"
    QUERY_TYPE_USAGE_AND_COST = "USAGE_AND_COST"

    def __init__(self, **kwargs):
        """
        Initializes a new QueryProperties object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param group_by:
            The value to assign to the group_by property of this QueryProperties.
        :type group_by: list[str]

        :param group_by_tag:
            The value to assign to the group_by_tag property of this QueryProperties.
        :type group_by_tag: list[oci.usage_api.models.Tag]

        :param filter:
            The value to assign to the filter property of this QueryProperties.
        :type filter: oci.usage_api.models.Filter

        :param compartment_depth:
            The value to assign to the compartment_depth property of this QueryProperties.
        :type compartment_depth: float

        :param granularity:
            The value to assign to the granularity property of this QueryProperties.
            Allowed values for this property are: "DAILY", "MONTHLY", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type granularity: str

        :param query_type:
            The value to assign to the query_type property of this QueryProperties.
            Allowed values for this property are: "USAGE", "COST", "USAGE_AND_COST", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type query_type: str

        :param is_aggregate_by_time:
            The value to assign to the is_aggregate_by_time property of this QueryProperties.
        :type is_aggregate_by_time: bool

        :param date_range:
            The value to assign to the date_range property of this QueryProperties.
        :type date_range: oci.usage_api.models.DateRange

        """
        self.swagger_types = {
            'group_by': 'list[str]',
            'group_by_tag': 'list[Tag]',
            'filter': 'Filter',
            'compartment_depth': 'float',
            'granularity': 'str',
            'query_type': 'str',
            'is_aggregate_by_time': 'bool',
            'date_range': 'DateRange'
        }

        self.attribute_map = {
            'group_by': 'groupBy',
            'group_by_tag': 'groupByTag',
            'filter': 'filter',
            'compartment_depth': 'compartmentDepth',
            'granularity': 'granularity',
            'query_type': 'queryType',
            'is_aggregate_by_time': 'isAggregateByTime',
            'date_range': 'dateRange'
        }

        self._group_by = None
        self._group_by_tag = None
        self._filter = None
        self._compartment_depth = None
        self._granularity = None
        self._query_type = None
        self._is_aggregate_by_time = None
        self._date_range = None

    @property
    def group_by(self):
        """
        Gets the group_by of this QueryProperties.
        Aggregate the result by. For example: [ \"tagNamespace\", \"tagKey\", \"tagValue\", \"service\", \"skuName\", \"skuPartNumber\", \"unit\", \"compartmentName\", \"compartmentPath\", \"compartmentId\", \"platform\", \"region\", \"logicalAd\", \"resourceId\", \"tenantId\", \"tenantName\" ]


        :return: The group_by of this QueryProperties.
        :rtype: list[str]
        """
        return self._group_by

    @group_by.setter
    def group_by(self, group_by):
        """
        Sets the group_by of this QueryProperties.
        Aggregate the result by. For example: [ \"tagNamespace\", \"tagKey\", \"tagValue\", \"service\", \"skuName\", \"skuPartNumber\", \"unit\", \"compartmentName\", \"compartmentPath\", \"compartmentId\", \"platform\", \"region\", \"logicalAd\", \"resourceId\", \"tenantId\", \"tenantName\" ]


        :param group_by: The group_by of this QueryProperties.
        :type: list[str]
        """
        self._group_by = group_by

    @property
    def group_by_tag(self):
        """
        Gets the group_by_tag of this QueryProperties.
        GroupBy a specific tagKey. Provide the tagNamespace and tagKey in the tag object. Only supports one tag in the list. For example: [ { \"namespace\": \"oracle\", \"key\": \"createdBy\" ]


        :return: The group_by_tag of this QueryProperties.
        :rtype: list[oci.usage_api.models.Tag]
        """
        return self._group_by_tag

    @group_by_tag.setter
    def group_by_tag(self, group_by_tag):
        """
        Sets the group_by_tag of this QueryProperties.
        GroupBy a specific tagKey. Provide the tagNamespace and tagKey in the tag object. Only supports one tag in the list. For example: [ { \"namespace\": \"oracle\", \"key\": \"createdBy\" ]


        :param group_by_tag: The group_by_tag of this QueryProperties.
        :type: list[oci.usage_api.models.Tag]
        """
        self._group_by_tag = group_by_tag

    @property
    def filter(self):
        """
        Gets the filter of this QueryProperties.

        :return: The filter of this QueryProperties.
        :rtype: oci.usage_api.models.Filter
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """
        Sets the filter of this QueryProperties.

        :param filter: The filter of this QueryProperties.
        :type: oci.usage_api.models.Filter
        """
        self._filter = filter

    @property
    def compartment_depth(self):
        """
        Gets the compartment_depth of this QueryProperties.
        The depth level of the compartment.


        :return: The compartment_depth of this QueryProperties.
        :rtype: float
        """
        return self._compartment_depth

    @compartment_depth.setter
    def compartment_depth(self, compartment_depth):
        """
        Sets the compartment_depth of this QueryProperties.
        The depth level of the compartment.


        :param compartment_depth: The compartment_depth of this QueryProperties.
        :type: float
        """
        self._compartment_depth = compartment_depth

    @property
    def granularity(self):
        """
        **[Required]** Gets the granularity of this QueryProperties.
        The usage granularity. DAILY - Daily data aggregation. MONTHLY - Monthly data aggregation.
        Allowed values are:
          DAILY
          MONTHLY

        Allowed values for this property are: "DAILY", "MONTHLY", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The granularity of this QueryProperties.
        :rtype: str
        """
        return self._granularity

    @granularity.setter
    def granularity(self, granularity):
        """
        Sets the granularity of this QueryProperties.
        The usage granularity. DAILY - Daily data aggregation. MONTHLY - Monthly data aggregation.
        Allowed values are:
          DAILY
          MONTHLY


        :param granularity: The granularity of this QueryProperties.
        :type: str
        """
        allowed_values = ["DAILY", "MONTHLY"]
        if not value_allowed_none_or_none_sentinel(granularity, allowed_values):
            granularity = 'UNKNOWN_ENUM_VALUE'
        self._granularity = granularity

    @property
    def query_type(self):
        """
        Gets the query_type of this QueryProperties.
        The query usage type. COST by default if it is missing. Usage - Query the usage data. Cost - Query the cost/billing data.
        Allowed values are:
          USAGE
          COST
          USAGE_AND_COST

        Allowed values for this property are: "USAGE", "COST", "USAGE_AND_COST", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The query_type of this QueryProperties.
        :rtype: str
        """
        return self._query_type

    @query_type.setter
    def query_type(self, query_type):
        """
        Sets the query_type of this QueryProperties.
        The query usage type. COST by default if it is missing. Usage - Query the usage data. Cost - Query the cost/billing data.
        Allowed values are:
          USAGE
          COST
          USAGE_AND_COST


        :param query_type: The query_type of this QueryProperties.
        :type: str
        """
        allowed_values = ["USAGE", "COST", "USAGE_AND_COST"]
        if not value_allowed_none_or_none_sentinel(query_type, allowed_values):
            query_type = 'UNKNOWN_ENUM_VALUE'
        self._query_type = query_type

    @property
    def is_aggregate_by_time(self):
        """
        Gets the is_aggregate_by_time of this QueryProperties.
        Specifies whether aggregated by time. If isAggregateByTime is true, all usage or cost over the query time period will be added up.


        :return: The is_aggregate_by_time of this QueryProperties.
        :rtype: bool
        """
        return self._is_aggregate_by_time

    @is_aggregate_by_time.setter
    def is_aggregate_by_time(self, is_aggregate_by_time):
        """
        Sets the is_aggregate_by_time of this QueryProperties.
        Specifies whether aggregated by time. If isAggregateByTime is true, all usage or cost over the query time period will be added up.


        :param is_aggregate_by_time: The is_aggregate_by_time of this QueryProperties.
        :type: bool
        """
        self._is_aggregate_by_time = is_aggregate_by_time

    @property
    def date_range(self):
        """
        **[Required]** Gets the date_range of this QueryProperties.

        :return: The date_range of this QueryProperties.
        :rtype: oci.usage_api.models.DateRange
        """
        return self._date_range

    @date_range.setter
    def date_range(self, date_range):
        """
        Sets the date_range of this QueryProperties.

        :param date_range: The date_range of this QueryProperties.
        :type: oci.usage_api.models.DateRange
        """
        self._date_range = date_range

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
