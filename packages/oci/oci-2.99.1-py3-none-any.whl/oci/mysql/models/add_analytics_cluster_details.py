# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddAnalyticsClusterDetails(object):
    """
    DEPRECATED -- please use HeatWave API instead.
    Details required to add an Analytics Cluster.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddAnalyticsClusterDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param shape_name:
            The value to assign to the shape_name property of this AddAnalyticsClusterDetails.
        :type shape_name: str

        :param cluster_size:
            The value to assign to the cluster_size property of this AddAnalyticsClusterDetails.
        :type cluster_size: int

        """
        self.swagger_types = {
            'shape_name': 'str',
            'cluster_size': 'int'
        }

        self.attribute_map = {
            'shape_name': 'shapeName',
            'cluster_size': 'clusterSize'
        }

        self._shape_name = None
        self._cluster_size = None

    @property
    def shape_name(self):
        """
        **[Required]** Gets the shape_name of this AddAnalyticsClusterDetails.
        The shape determines resources to allocate to the Analytics
        Cluster nodes - CPU cores, memory.


        :return: The shape_name of this AddAnalyticsClusterDetails.
        :rtype: str
        """
        return self._shape_name

    @shape_name.setter
    def shape_name(self, shape_name):
        """
        Sets the shape_name of this AddAnalyticsClusterDetails.
        The shape determines resources to allocate to the Analytics
        Cluster nodes - CPU cores, memory.


        :param shape_name: The shape_name of this AddAnalyticsClusterDetails.
        :type: str
        """
        self._shape_name = shape_name

    @property
    def cluster_size(self):
        """
        **[Required]** Gets the cluster_size of this AddAnalyticsClusterDetails.
        The number of analytics-processing nodes provisioned for the
        Analytics Cluster.


        :return: The cluster_size of this AddAnalyticsClusterDetails.
        :rtype: int
        """
        return self._cluster_size

    @cluster_size.setter
    def cluster_size(self, cluster_size):
        """
        Sets the cluster_size of this AddAnalyticsClusterDetails.
        The number of analytics-processing nodes provisioned for the
        Analytics Cluster.


        :param cluster_size: The cluster_size of this AddAnalyticsClusterDetails.
        :type: int
        """
        self._cluster_size = cluster_size

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
