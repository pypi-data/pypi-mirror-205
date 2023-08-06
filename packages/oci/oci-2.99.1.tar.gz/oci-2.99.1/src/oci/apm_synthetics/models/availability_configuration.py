# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AvailabilityConfiguration(object):
    """
    Monitor availability configuration details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AvailabilityConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param max_allowed_failures_per_interval:
            The value to assign to the max_allowed_failures_per_interval property of this AvailabilityConfiguration.
        :type max_allowed_failures_per_interval: int

        :param min_allowed_runs_per_interval:
            The value to assign to the min_allowed_runs_per_interval property of this AvailabilityConfiguration.
        :type min_allowed_runs_per_interval: int

        """
        self.swagger_types = {
            'max_allowed_failures_per_interval': 'int',
            'min_allowed_runs_per_interval': 'int'
        }

        self.attribute_map = {
            'max_allowed_failures_per_interval': 'maxAllowedFailuresPerInterval',
            'min_allowed_runs_per_interval': 'minAllowedRunsPerInterval'
        }

        self._max_allowed_failures_per_interval = None
        self._min_allowed_runs_per_interval = None

    @property
    def max_allowed_failures_per_interval(self):
        """
        Gets the max_allowed_failures_per_interval of this AvailabilityConfiguration.
        Intervals with failed runs more than this value will be classified as UNAVAILABLE.


        :return: The max_allowed_failures_per_interval of this AvailabilityConfiguration.
        :rtype: int
        """
        return self._max_allowed_failures_per_interval

    @max_allowed_failures_per_interval.setter
    def max_allowed_failures_per_interval(self, max_allowed_failures_per_interval):
        """
        Sets the max_allowed_failures_per_interval of this AvailabilityConfiguration.
        Intervals with failed runs more than this value will be classified as UNAVAILABLE.


        :param max_allowed_failures_per_interval: The max_allowed_failures_per_interval of this AvailabilityConfiguration.
        :type: int
        """
        self._max_allowed_failures_per_interval = max_allowed_failures_per_interval

    @property
    def min_allowed_runs_per_interval(self):
        """
        Gets the min_allowed_runs_per_interval of this AvailabilityConfiguration.
        Intervals with runs less than this value will be classified as UNKNOWN and excluded from the availability calculations.


        :return: The min_allowed_runs_per_interval of this AvailabilityConfiguration.
        :rtype: int
        """
        return self._min_allowed_runs_per_interval

    @min_allowed_runs_per_interval.setter
    def min_allowed_runs_per_interval(self, min_allowed_runs_per_interval):
        """
        Sets the min_allowed_runs_per_interval of this AvailabilityConfiguration.
        Intervals with runs less than this value will be classified as UNKNOWN and excluded from the availability calculations.


        :param min_allowed_runs_per_interval: The min_allowed_runs_per_interval of this AvailabilityConfiguration.
        :type: int
        """
        self._min_allowed_runs_per_interval = min_allowed_runs_per_interval

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
