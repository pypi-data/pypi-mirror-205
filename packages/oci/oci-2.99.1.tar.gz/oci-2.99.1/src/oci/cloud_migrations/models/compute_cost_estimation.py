# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ComputeCostEstimation(object):
    """
    Cost estimation for compute
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ComputeCostEstimation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param ocpu_per_hour:
            The value to assign to the ocpu_per_hour property of this ComputeCostEstimation.
        :type ocpu_per_hour: float

        :param ocpu_per_hour_by_subscription:
            The value to assign to the ocpu_per_hour_by_subscription property of this ComputeCostEstimation.
        :type ocpu_per_hour_by_subscription: float

        :param memory_gb_per_hour:
            The value to assign to the memory_gb_per_hour property of this ComputeCostEstimation.
        :type memory_gb_per_hour: float

        :param memory_gb_per_hour_by_subscription:
            The value to assign to the memory_gb_per_hour_by_subscription property of this ComputeCostEstimation.
        :type memory_gb_per_hour_by_subscription: float

        :param gpu_per_hour:
            The value to assign to the gpu_per_hour property of this ComputeCostEstimation.
        :type gpu_per_hour: float

        :param gpu_per_hour_by_subscription:
            The value to assign to the gpu_per_hour_by_subscription property of this ComputeCostEstimation.
        :type gpu_per_hour_by_subscription: float

        :param total_per_hour:
            The value to assign to the total_per_hour property of this ComputeCostEstimation.
        :type total_per_hour: float

        :param total_per_hour_by_subscription:
            The value to assign to the total_per_hour_by_subscription property of this ComputeCostEstimation.
        :type total_per_hour_by_subscription: float

        :param ocpu_count:
            The value to assign to the ocpu_count property of this ComputeCostEstimation.
        :type ocpu_count: float

        :param memory_amount_gb:
            The value to assign to the memory_amount_gb property of this ComputeCostEstimation.
        :type memory_amount_gb: float

        :param gpu_count:
            The value to assign to the gpu_count property of this ComputeCostEstimation.
        :type gpu_count: float

        """
        self.swagger_types = {
            'ocpu_per_hour': 'float',
            'ocpu_per_hour_by_subscription': 'float',
            'memory_gb_per_hour': 'float',
            'memory_gb_per_hour_by_subscription': 'float',
            'gpu_per_hour': 'float',
            'gpu_per_hour_by_subscription': 'float',
            'total_per_hour': 'float',
            'total_per_hour_by_subscription': 'float',
            'ocpu_count': 'float',
            'memory_amount_gb': 'float',
            'gpu_count': 'float'
        }

        self.attribute_map = {
            'ocpu_per_hour': 'ocpuPerHour',
            'ocpu_per_hour_by_subscription': 'ocpuPerHourBySubscription',
            'memory_gb_per_hour': 'memoryGbPerHour',
            'memory_gb_per_hour_by_subscription': 'memoryGbPerHourBySubscription',
            'gpu_per_hour': 'gpuPerHour',
            'gpu_per_hour_by_subscription': 'gpuPerHourBySubscription',
            'total_per_hour': 'totalPerHour',
            'total_per_hour_by_subscription': 'totalPerHourBySubscription',
            'ocpu_count': 'ocpuCount',
            'memory_amount_gb': 'memoryAmountGb',
            'gpu_count': 'gpuCount'
        }

        self._ocpu_per_hour = None
        self._ocpu_per_hour_by_subscription = None
        self._memory_gb_per_hour = None
        self._memory_gb_per_hour_by_subscription = None
        self._gpu_per_hour = None
        self._gpu_per_hour_by_subscription = None
        self._total_per_hour = None
        self._total_per_hour_by_subscription = None
        self._ocpu_count = None
        self._memory_amount_gb = None
        self._gpu_count = None

    @property
    def ocpu_per_hour(self):
        """
        **[Required]** Gets the ocpu_per_hour of this ComputeCostEstimation.
        OCPU per hour


        :return: The ocpu_per_hour of this ComputeCostEstimation.
        :rtype: float
        """
        return self._ocpu_per_hour

    @ocpu_per_hour.setter
    def ocpu_per_hour(self, ocpu_per_hour):
        """
        Sets the ocpu_per_hour of this ComputeCostEstimation.
        OCPU per hour


        :param ocpu_per_hour: The ocpu_per_hour of this ComputeCostEstimation.
        :type: float
        """
        self._ocpu_per_hour = ocpu_per_hour

    @property
    def ocpu_per_hour_by_subscription(self):
        """
        Gets the ocpu_per_hour_by_subscription of this ComputeCostEstimation.
        OCPU per hour by subscription


        :return: The ocpu_per_hour_by_subscription of this ComputeCostEstimation.
        :rtype: float
        """
        return self._ocpu_per_hour_by_subscription

    @ocpu_per_hour_by_subscription.setter
    def ocpu_per_hour_by_subscription(self, ocpu_per_hour_by_subscription):
        """
        Sets the ocpu_per_hour_by_subscription of this ComputeCostEstimation.
        OCPU per hour by subscription


        :param ocpu_per_hour_by_subscription: The ocpu_per_hour_by_subscription of this ComputeCostEstimation.
        :type: float
        """
        self._ocpu_per_hour_by_subscription = ocpu_per_hour_by_subscription

    @property
    def memory_gb_per_hour(self):
        """
        **[Required]** Gets the memory_gb_per_hour of this ComputeCostEstimation.
        Gigabyte per hour


        :return: The memory_gb_per_hour of this ComputeCostEstimation.
        :rtype: float
        """
        return self._memory_gb_per_hour

    @memory_gb_per_hour.setter
    def memory_gb_per_hour(self, memory_gb_per_hour):
        """
        Sets the memory_gb_per_hour of this ComputeCostEstimation.
        Gigabyte per hour


        :param memory_gb_per_hour: The memory_gb_per_hour of this ComputeCostEstimation.
        :type: float
        """
        self._memory_gb_per_hour = memory_gb_per_hour

    @property
    def memory_gb_per_hour_by_subscription(self):
        """
        Gets the memory_gb_per_hour_by_subscription of this ComputeCostEstimation.
        Gigabyte per hour by subscription


        :return: The memory_gb_per_hour_by_subscription of this ComputeCostEstimation.
        :rtype: float
        """
        return self._memory_gb_per_hour_by_subscription

    @memory_gb_per_hour_by_subscription.setter
    def memory_gb_per_hour_by_subscription(self, memory_gb_per_hour_by_subscription):
        """
        Sets the memory_gb_per_hour_by_subscription of this ComputeCostEstimation.
        Gigabyte per hour by subscription


        :param memory_gb_per_hour_by_subscription: The memory_gb_per_hour_by_subscription of this ComputeCostEstimation.
        :type: float
        """
        self._memory_gb_per_hour_by_subscription = memory_gb_per_hour_by_subscription

    @property
    def gpu_per_hour(self):
        """
        **[Required]** Gets the gpu_per_hour of this ComputeCostEstimation.
        GPU per hour


        :return: The gpu_per_hour of this ComputeCostEstimation.
        :rtype: float
        """
        return self._gpu_per_hour

    @gpu_per_hour.setter
    def gpu_per_hour(self, gpu_per_hour):
        """
        Sets the gpu_per_hour of this ComputeCostEstimation.
        GPU per hour


        :param gpu_per_hour: The gpu_per_hour of this ComputeCostEstimation.
        :type: float
        """
        self._gpu_per_hour = gpu_per_hour

    @property
    def gpu_per_hour_by_subscription(self):
        """
        Gets the gpu_per_hour_by_subscription of this ComputeCostEstimation.
        GPU per hour by subscription


        :return: The gpu_per_hour_by_subscription of this ComputeCostEstimation.
        :rtype: float
        """
        return self._gpu_per_hour_by_subscription

    @gpu_per_hour_by_subscription.setter
    def gpu_per_hour_by_subscription(self, gpu_per_hour_by_subscription):
        """
        Sets the gpu_per_hour_by_subscription of this ComputeCostEstimation.
        GPU per hour by subscription


        :param gpu_per_hour_by_subscription: The gpu_per_hour_by_subscription of this ComputeCostEstimation.
        :type: float
        """
        self._gpu_per_hour_by_subscription = gpu_per_hour_by_subscription

    @property
    def total_per_hour(self):
        """
        **[Required]** Gets the total_per_hour of this ComputeCostEstimation.
        Total per hour


        :return: The total_per_hour of this ComputeCostEstimation.
        :rtype: float
        """
        return self._total_per_hour

    @total_per_hour.setter
    def total_per_hour(self, total_per_hour):
        """
        Sets the total_per_hour of this ComputeCostEstimation.
        Total per hour


        :param total_per_hour: The total_per_hour of this ComputeCostEstimation.
        :type: float
        """
        self._total_per_hour = total_per_hour

    @property
    def total_per_hour_by_subscription(self):
        """
        Gets the total_per_hour_by_subscription of this ComputeCostEstimation.
        Total usage per hour by subscription


        :return: The total_per_hour_by_subscription of this ComputeCostEstimation.
        :rtype: float
        """
        return self._total_per_hour_by_subscription

    @total_per_hour_by_subscription.setter
    def total_per_hour_by_subscription(self, total_per_hour_by_subscription):
        """
        Sets the total_per_hour_by_subscription of this ComputeCostEstimation.
        Total usage per hour by subscription


        :param total_per_hour_by_subscription: The total_per_hour_by_subscription of this ComputeCostEstimation.
        :type: float
        """
        self._total_per_hour_by_subscription = total_per_hour_by_subscription

    @property
    def ocpu_count(self):
        """
        Gets the ocpu_count of this ComputeCostEstimation.
        Total number of OCPUs


        :return: The ocpu_count of this ComputeCostEstimation.
        :rtype: float
        """
        return self._ocpu_count

    @ocpu_count.setter
    def ocpu_count(self, ocpu_count):
        """
        Sets the ocpu_count of this ComputeCostEstimation.
        Total number of OCPUs


        :param ocpu_count: The ocpu_count of this ComputeCostEstimation.
        :type: float
        """
        self._ocpu_count = ocpu_count

    @property
    def memory_amount_gb(self):
        """
        Gets the memory_amount_gb of this ComputeCostEstimation.
        Total usage of memory


        :return: The memory_amount_gb of this ComputeCostEstimation.
        :rtype: float
        """
        return self._memory_amount_gb

    @memory_amount_gb.setter
    def memory_amount_gb(self, memory_amount_gb):
        """
        Sets the memory_amount_gb of this ComputeCostEstimation.
        Total usage of memory


        :param memory_amount_gb: The memory_amount_gb of this ComputeCostEstimation.
        :type: float
        """
        self._memory_amount_gb = memory_amount_gb

    @property
    def gpu_count(self):
        """
        Gets the gpu_count of this ComputeCostEstimation.
        Total number of GPU


        :return: The gpu_count of this ComputeCostEstimation.
        :rtype: float
        """
        return self._gpu_count

    @gpu_count.setter
    def gpu_count(self, gpu_count):
        """
        Sets the gpu_count of this ComputeCostEstimation.
        Total number of GPU


        :param gpu_count: The gpu_count of this ComputeCostEstimation.
        :type: float
        """
        self._gpu_count = gpu_count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
