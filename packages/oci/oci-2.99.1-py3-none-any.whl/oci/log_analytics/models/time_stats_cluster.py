# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TimeStatsCluster(object):
    """
    Object representing a timeseries cluster.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new TimeStatsCluster object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param group_by_facets:
            The value to assign to the group_by_facets property of this TimeStatsCluster.
        :type group_by_facets: list[dict(str, object)]

        :param count:
            The value to assign to the count property of this TimeStatsCluster.
        :type count: int

        """
        self.swagger_types = {
            'group_by_facets': 'list[dict(str, object)]',
            'count': 'int'
        }

        self.attribute_map = {
            'group_by_facets': 'groupByFacets',
            'count': 'count'
        }

        self._group_by_facets = None
        self._count = None

    @property
    def group_by_facets(self):
        """
        Gets the group_by_facets of this TimeStatsCluster.
        Group by field facets within the cluster.


        :return: The group_by_facets of this TimeStatsCluster.
        :rtype: list[dict(str, object)]
        """
        return self._group_by_facets

    @group_by_facets.setter
    def group_by_facets(self, group_by_facets):
        """
        Sets the group_by_facets of this TimeStatsCluster.
        Group by field facets within the cluster.


        :param group_by_facets: The group_by_facets of this TimeStatsCluster.
        :type: list[dict(str, object)]
        """
        self._group_by_facets = group_by_facets

    @property
    def count(self):
        """
        Gets the count of this TimeStatsCluster.
        Number of timeseries within the cluster.


        :return: The count of this TimeStatsCluster.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """
        Sets the count of this TimeStatsCluster.
        Number of timeseries within the cluster.


        :param count: The count of this TimeStatsCluster.
        :type: int
        """
        self._count = count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
