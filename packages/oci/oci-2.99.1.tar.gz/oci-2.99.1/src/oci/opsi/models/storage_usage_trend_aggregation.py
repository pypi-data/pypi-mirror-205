# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class StorageUsageTrendAggregation(object):
    """
    Usage data per filesystem.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new StorageUsageTrendAggregation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param file_system_name:
            The value to assign to the file_system_name property of this StorageUsageTrendAggregation.
        :type file_system_name: str

        :param mount_point:
            The value to assign to the mount_point property of this StorageUsageTrendAggregation.
        :type mount_point: str

        :param file_system_size_in_gbs:
            The value to assign to the file_system_size_in_gbs property of this StorageUsageTrendAggregation.
        :type file_system_size_in_gbs: float

        :param usage_data:
            The value to assign to the usage_data property of this StorageUsageTrendAggregation.
        :type usage_data: list[oci.opsi.models.StorageUsageTrend]

        """
        self.swagger_types = {
            'file_system_name': 'str',
            'mount_point': 'str',
            'file_system_size_in_gbs': 'float',
            'usage_data': 'list[StorageUsageTrend]'
        }

        self.attribute_map = {
            'file_system_name': 'fileSystemName',
            'mount_point': 'mountPoint',
            'file_system_size_in_gbs': 'fileSystemSizeInGBs',
            'usage_data': 'usageData'
        }

        self._file_system_name = None
        self._mount_point = None
        self._file_system_size_in_gbs = None
        self._usage_data = None

    @property
    def file_system_name(self):
        """
        **[Required]** Gets the file_system_name of this StorageUsageTrendAggregation.
        Name of filesystem.


        :return: The file_system_name of this StorageUsageTrendAggregation.
        :rtype: str
        """
        return self._file_system_name

    @file_system_name.setter
    def file_system_name(self, file_system_name):
        """
        Sets the file_system_name of this StorageUsageTrendAggregation.
        Name of filesystem.


        :param file_system_name: The file_system_name of this StorageUsageTrendAggregation.
        :type: str
        """
        self._file_system_name = file_system_name

    @property
    def mount_point(self):
        """
        **[Required]** Gets the mount_point of this StorageUsageTrendAggregation.
        Mount points are specialized NTFS filesystem objects.


        :return: The mount_point of this StorageUsageTrendAggregation.
        :rtype: str
        """
        return self._mount_point

    @mount_point.setter
    def mount_point(self, mount_point):
        """
        Sets the mount_point of this StorageUsageTrendAggregation.
        Mount points are specialized NTFS filesystem objects.


        :param mount_point: The mount_point of this StorageUsageTrendAggregation.
        :type: str
        """
        self._mount_point = mount_point

    @property
    def file_system_size_in_gbs(self):
        """
        **[Required]** Gets the file_system_size_in_gbs of this StorageUsageTrendAggregation.
        Size of filesystem.


        :return: The file_system_size_in_gbs of this StorageUsageTrendAggregation.
        :rtype: float
        """
        return self._file_system_size_in_gbs

    @file_system_size_in_gbs.setter
    def file_system_size_in_gbs(self, file_system_size_in_gbs):
        """
        Sets the file_system_size_in_gbs of this StorageUsageTrendAggregation.
        Size of filesystem.


        :param file_system_size_in_gbs: The file_system_size_in_gbs of this StorageUsageTrendAggregation.
        :type: float
        """
        self._file_system_size_in_gbs = file_system_size_in_gbs

    @property
    def usage_data(self):
        """
        **[Required]** Gets the usage_data of this StorageUsageTrendAggregation.
        List of usage data samples for a filesystem.


        :return: The usage_data of this StorageUsageTrendAggregation.
        :rtype: list[oci.opsi.models.StorageUsageTrend]
        """
        return self._usage_data

    @usage_data.setter
    def usage_data(self, usage_data):
        """
        Sets the usage_data of this StorageUsageTrendAggregation.
        List of usage data samples for a filesystem.


        :param usage_data: The usage_data of this StorageUsageTrendAggregation.
        :type: list[oci.opsi.models.StorageUsageTrend]
        """
        self._usage_data = usage_data

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
