# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DbManagementAnalyticsMetric(object):
    """
    The metric details of a Database Management resource.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DbManagementAnalyticsMetric object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param metric_name:
            The value to assign to the metric_name property of this DbManagementAnalyticsMetric.
        :type metric_name: str

        :param duration_in_seconds:
            The value to assign to the duration_in_seconds property of this DbManagementAnalyticsMetric.
        :type duration_in_seconds: int

        :param metadata:
            The value to assign to the metadata property of this DbManagementAnalyticsMetric.
        :type metadata: dict(str, str)

        :param dimensions:
            The value to assign to the dimensions property of this DbManagementAnalyticsMetric.
        :type dimensions: dict(str, str)

        :param start_timestamp_in_epoch_seconds:
            The value to assign to the start_timestamp_in_epoch_seconds property of this DbManagementAnalyticsMetric.
        :type start_timestamp_in_epoch_seconds: int

        :param mean:
            The value to assign to the mean property of this DbManagementAnalyticsMetric.
        :type mean: float

        """
        self.swagger_types = {
            'metric_name': 'str',
            'duration_in_seconds': 'int',
            'metadata': 'dict(str, str)',
            'dimensions': 'dict(str, str)',
            'start_timestamp_in_epoch_seconds': 'int',
            'mean': 'float'
        }

        self.attribute_map = {
            'metric_name': 'metricName',
            'duration_in_seconds': 'durationInSeconds',
            'metadata': 'metadata',
            'dimensions': 'dimensions',
            'start_timestamp_in_epoch_seconds': 'startTimestampInEpochSeconds',
            'mean': 'mean'
        }

        self._metric_name = None
        self._duration_in_seconds = None
        self._metadata = None
        self._dimensions = None
        self._start_timestamp_in_epoch_seconds = None
        self._mean = None

    @property
    def metric_name(self):
        """
        Gets the metric_name of this DbManagementAnalyticsMetric.
        The name of the metric.


        :return: The metric_name of this DbManagementAnalyticsMetric.
        :rtype: str
        """
        return self._metric_name

    @metric_name.setter
    def metric_name(self, metric_name):
        """
        Sets the metric_name of this DbManagementAnalyticsMetric.
        The name of the metric.


        :param metric_name: The metric_name of this DbManagementAnalyticsMetric.
        :type: str
        """
        self._metric_name = metric_name

    @property
    def duration_in_seconds(self):
        """
        Gets the duration_in_seconds of this DbManagementAnalyticsMetric.
        The duration of the returned aggregated data in seconds.


        :return: The duration_in_seconds of this DbManagementAnalyticsMetric.
        :rtype: int
        """
        return self._duration_in_seconds

    @duration_in_seconds.setter
    def duration_in_seconds(self, duration_in_seconds):
        """
        Sets the duration_in_seconds of this DbManagementAnalyticsMetric.
        The duration of the returned aggregated data in seconds.


        :param duration_in_seconds: The duration_in_seconds of this DbManagementAnalyticsMetric.
        :type: int
        """
        self._duration_in_seconds = duration_in_seconds

    @property
    def metadata(self):
        """
        Gets the metadata of this DbManagementAnalyticsMetric.
        The additional information about the metric.

        Example: `\"unit\": \"bytes\"`


        :return: The metadata of this DbManagementAnalyticsMetric.
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this DbManagementAnalyticsMetric.
        The additional information about the metric.

        Example: `\"unit\": \"bytes\"`


        :param metadata: The metadata of this DbManagementAnalyticsMetric.
        :type: dict(str, str)
        """
        self._metadata = metadata

    @property
    def dimensions(self):
        """
        Gets the dimensions of this DbManagementAnalyticsMetric.
        The qualifiers provided in the definition of the returned metric.


        :return: The dimensions of this DbManagementAnalyticsMetric.
        :rtype: dict(str, str)
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """
        Sets the dimensions of this DbManagementAnalyticsMetric.
        The qualifiers provided in the definition of the returned metric.


        :param dimensions: The dimensions of this DbManagementAnalyticsMetric.
        :type: dict(str, str)
        """
        self._dimensions = dimensions

    @property
    def start_timestamp_in_epoch_seconds(self):
        """
        Gets the start_timestamp_in_epoch_seconds of this DbManagementAnalyticsMetric.
        The start time associated with the value of the metric.


        :return: The start_timestamp_in_epoch_seconds of this DbManagementAnalyticsMetric.
        :rtype: int
        """
        return self._start_timestamp_in_epoch_seconds

    @start_timestamp_in_epoch_seconds.setter
    def start_timestamp_in_epoch_seconds(self, start_timestamp_in_epoch_seconds):
        """
        Sets the start_timestamp_in_epoch_seconds of this DbManagementAnalyticsMetric.
        The start time associated with the value of the metric.


        :param start_timestamp_in_epoch_seconds: The start_timestamp_in_epoch_seconds of this DbManagementAnalyticsMetric.
        :type: int
        """
        self._start_timestamp_in_epoch_seconds = start_timestamp_in_epoch_seconds

    @property
    def mean(self):
        """
        Gets the mean of this DbManagementAnalyticsMetric.
        The mean value of the metric.


        :return: The mean of this DbManagementAnalyticsMetric.
        :rtype: float
        """
        return self._mean

    @mean.setter
    def mean(self, mean):
        """
        Sets the mean of this DbManagementAnalyticsMetric.
        The mean value of the metric.


        :param mean: The mean of this DbManagementAnalyticsMetric.
        :type: float
        """
        self._mean = mean

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
