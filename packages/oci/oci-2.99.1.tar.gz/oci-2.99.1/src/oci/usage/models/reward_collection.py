# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RewardCollection(object):
    """
    The response object for the ListRewards API call. Provides information about the subscription rewards.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RewardCollection object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param summary:
            The value to assign to the summary property of this RewardCollection.
        :type summary: oci.usage.models.RewardDetails

        :param items:
            The value to assign to the items property of this RewardCollection.
        :type items: list[oci.usage.models.MonthlyRewardSummary]

        """
        self.swagger_types = {
            'summary': 'RewardDetails',
            'items': 'list[MonthlyRewardSummary]'
        }

        self.attribute_map = {
            'summary': 'summary',
            'items': 'items'
        }

        self._summary = None
        self._items = None

    @property
    def summary(self):
        """
        **[Required]** Gets the summary of this RewardCollection.

        :return: The summary of this RewardCollection.
        :rtype: oci.usage.models.RewardDetails
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this RewardCollection.

        :param summary: The summary of this RewardCollection.
        :type: oci.usage.models.RewardDetails
        """
        self._summary = summary

    @property
    def items(self):
        """
        Gets the items of this RewardCollection.
        The monthly summary of rewards.


        :return: The items of this RewardCollection.
        :rtype: list[oci.usage.models.MonthlyRewardSummary]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this RewardCollection.
        The monthly summary of rewards.


        :param items: The items of this RewardCollection.
        :type: list[oci.usage.models.MonthlyRewardSummary]
        """
        self._items = items

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
