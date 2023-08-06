# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class HostConfigurationMetricGroup(object):
    """
    Base Metric Group for Host configuration metrics
    """

    #: A constant which can be used with the metric_name property of a HostConfigurationMetricGroup.
    #: This constant has a value of "HOST_PRODUCT"
    METRIC_NAME_HOST_PRODUCT = "HOST_PRODUCT"

    #: A constant which can be used with the metric_name property of a HostConfigurationMetricGroup.
    #: This constant has a value of "HOST_RESOURCE_ALLOCATION"
    METRIC_NAME_HOST_RESOURCE_ALLOCATION = "HOST_RESOURCE_ALLOCATION"

    #: A constant which can be used with the metric_name property of a HostConfigurationMetricGroup.
    #: This constant has a value of "HOST_MEMORY_CONFIGURATION"
    METRIC_NAME_HOST_MEMORY_CONFIGURATION = "HOST_MEMORY_CONFIGURATION"

    #: A constant which can be used with the metric_name property of a HostConfigurationMetricGroup.
    #: This constant has a value of "HOST_HARDWARE_CONFIGURATION"
    METRIC_NAME_HOST_HARDWARE_CONFIGURATION = "HOST_HARDWARE_CONFIGURATION"

    #: A constant which can be used with the metric_name property of a HostConfigurationMetricGroup.
    #: This constant has a value of "HOST_CPU_HARDWARE_CONFIGURATION"
    METRIC_NAME_HOST_CPU_HARDWARE_CONFIGURATION = "HOST_CPU_HARDWARE_CONFIGURATION"

    #: A constant which can be used with the metric_name property of a HostConfigurationMetricGroup.
    #: This constant has a value of "HOST_NETWORK_CONFIGURATION"
    METRIC_NAME_HOST_NETWORK_CONFIGURATION = "HOST_NETWORK_CONFIGURATION"

    #: A constant which can be used with the metric_name property of a HostConfigurationMetricGroup.
    #: This constant has a value of "HOST_ENTITES"
    METRIC_NAME_HOST_ENTITES = "HOST_ENTITES"

    #: A constant which can be used with the metric_name property of a HostConfigurationMetricGroup.
    #: This constant has a value of "HOST_FILESYSTEM_CONFIGURATION"
    METRIC_NAME_HOST_FILESYSTEM_CONFIGURATION = "HOST_FILESYSTEM_CONFIGURATION"

    def __init__(self, **kwargs):
        """
        Initializes a new HostConfigurationMetricGroup object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.opsi.models.HostResourceAllocation`
        * :class:`~oci.opsi.models.HostProduct`
        * :class:`~oci.opsi.models.HostFilesystemConfiguration`
        * :class:`~oci.opsi.models.HostNetworkConfiguration`
        * :class:`~oci.opsi.models.HostEntities`
        * :class:`~oci.opsi.models.HostMemoryConfiguration`
        * :class:`~oci.opsi.models.HostCpuHardwareConfiguration`
        * :class:`~oci.opsi.models.HostHardwareConfiguration`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param metric_name:
            The value to assign to the metric_name property of this HostConfigurationMetricGroup.
            Allowed values for this property are: "HOST_PRODUCT", "HOST_RESOURCE_ALLOCATION", "HOST_MEMORY_CONFIGURATION", "HOST_HARDWARE_CONFIGURATION", "HOST_CPU_HARDWARE_CONFIGURATION", "HOST_NETWORK_CONFIGURATION", "HOST_ENTITES", "HOST_FILESYSTEM_CONFIGURATION"
        :type metric_name: str

        :param time_collected:
            The value to assign to the time_collected property of this HostConfigurationMetricGroup.
        :type time_collected: datetime

        """
        self.swagger_types = {
            'metric_name': 'str',
            'time_collected': 'datetime'
        }

        self.attribute_map = {
            'metric_name': 'metricName',
            'time_collected': 'timeCollected'
        }

        self._metric_name = None
        self._time_collected = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['metricName']

        if type == 'HOST_RESOURCE_ALLOCATION':
            return 'HostResourceAllocation'

        if type == 'HOST_PRODUCT':
            return 'HostProduct'

        if type == 'HOST_FILESYSTEM_CONFIGURATION':
            return 'HostFilesystemConfiguration'

        if type == 'HOST_NETWORK_CONFIGURATION':
            return 'HostNetworkConfiguration'

        if type == 'HOST_ENTITIES':
            return 'HostEntities'

        if type == 'HOST_MEMORY_CONFIGURATION':
            return 'HostMemoryConfiguration'

        if type == 'HOST_CPU_HARDWARE_CONFIGURATION':
            return 'HostCpuHardwareConfiguration'

        if type == 'HOST_HARDWARE_CONFIGURATION':
            return 'HostHardwareConfiguration'
        else:
            return 'HostConfigurationMetricGroup'

    @property
    def metric_name(self):
        """
        **[Required]** Gets the metric_name of this HostConfigurationMetricGroup.
        Name of the metric group

        Allowed values for this property are: "HOST_PRODUCT", "HOST_RESOURCE_ALLOCATION", "HOST_MEMORY_CONFIGURATION", "HOST_HARDWARE_CONFIGURATION", "HOST_CPU_HARDWARE_CONFIGURATION", "HOST_NETWORK_CONFIGURATION", "HOST_ENTITES", "HOST_FILESYSTEM_CONFIGURATION"


        :return: The metric_name of this HostConfigurationMetricGroup.
        :rtype: str
        """
        return self._metric_name

    @metric_name.setter
    def metric_name(self, metric_name):
        """
        Sets the metric_name of this HostConfigurationMetricGroup.
        Name of the metric group


        :param metric_name: The metric_name of this HostConfigurationMetricGroup.
        :type: str
        """
        allowed_values = ["HOST_PRODUCT", "HOST_RESOURCE_ALLOCATION", "HOST_MEMORY_CONFIGURATION", "HOST_HARDWARE_CONFIGURATION", "HOST_CPU_HARDWARE_CONFIGURATION", "HOST_NETWORK_CONFIGURATION", "HOST_ENTITES", "HOST_FILESYSTEM_CONFIGURATION"]
        if not value_allowed_none_or_none_sentinel(metric_name, allowed_values):
            raise ValueError(
                "Invalid value for `metric_name`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._metric_name = metric_name

    @property
    def time_collected(self):
        """
        **[Required]** Gets the time_collected of this HostConfigurationMetricGroup.
        Collection timestamp
        Example: `\"2020-05-06T00:00:00.000Z\"`


        :return: The time_collected of this HostConfigurationMetricGroup.
        :rtype: datetime
        """
        return self._time_collected

    @time_collected.setter
    def time_collected(self, time_collected):
        """
        Sets the time_collected of this HostConfigurationMetricGroup.
        Collection timestamp
        Example: `\"2020-05-06T00:00:00.000Z\"`


        :param time_collected: The time_collected of this HostConfigurationMetricGroup.
        :type: datetime
        """
        self._time_collected = time_collected

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
