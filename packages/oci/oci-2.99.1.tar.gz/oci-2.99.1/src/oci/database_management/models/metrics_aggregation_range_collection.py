# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MetricsAggregationRangeCollection(object):
    """
    The collection of metrics.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MetricsAggregationRangeCollection object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param items:
            The value to assign to the items property of this MetricsAggregationRangeCollection.
        :type items: list[oci.database_management.models.MetricsAggregationRange]

        :param start_time:
            The value to assign to the start_time property of this MetricsAggregationRangeCollection.
        :type start_time: str

        :param end_time:
            The value to assign to the end_time property of this MetricsAggregationRangeCollection.
        :type end_time: str

        """
        self.swagger_types = {
            'items': 'list[MetricsAggregationRange]',
            'start_time': 'str',
            'end_time': 'str'
        }

        self.attribute_map = {
            'items': 'items',
            'start_time': 'startTime',
            'end_time': 'endTime'
        }

        self._items = None
        self._start_time = None
        self._end_time = None

    @property
    def items(self):
        """
        **[Required]** Gets the items of this MetricsAggregationRangeCollection.
        The metric data.


        :return: The items of this MetricsAggregationRangeCollection.
        :rtype: list[oci.database_management.models.MetricsAggregationRange]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this MetricsAggregationRangeCollection.
        The metric data.


        :param items: The items of this MetricsAggregationRangeCollection.
        :type: list[oci.database_management.models.MetricsAggregationRange]
        """
        self._items = items

    @property
    def start_time(self):
        """
        Gets the start_time of this MetricsAggregationRangeCollection.
        The beginning of the metric data query time range. Expressed in UTC in
        ISO-8601 format, which is `yyyy-MM-dd'T'hh:mm:ss.sss'Z'`.


        :return: The start_time of this MetricsAggregationRangeCollection.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this MetricsAggregationRangeCollection.
        The beginning of the metric data query time range. Expressed in UTC in
        ISO-8601 format, which is `yyyy-MM-dd'T'hh:mm:ss.sss'Z'`.


        :param start_time: The start_time of this MetricsAggregationRangeCollection.
        :type: str
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """
        Gets the end_time of this MetricsAggregationRangeCollection.
        The end of the metric data query time range. Expressed in UTC in
        ISO-8601 format, which is `yyyy-MM-dd'T'hh:mm:ss.sss'Z'`.


        :return: The end_time of this MetricsAggregationRangeCollection.
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the end_time of this MetricsAggregationRangeCollection.
        The end of the metric data query time range. Expressed in UTC in
        ISO-8601 format, which is `yyyy-MM-dd'T'hh:mm:ss.sss'Z'`.


        :param end_time: The end_time of this MetricsAggregationRangeCollection.
        :type: str
        """
        self._end_time = end_time

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
