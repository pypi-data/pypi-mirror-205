# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SubscriptionDetail(object):
    """
    Detail for the FusionEnvironmentFamily subscription.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SubscriptionDetail object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param subscriptions:
            The value to assign to the subscriptions property of this SubscriptionDetail.
        :type subscriptions: list[oci.fusion_apps.models.Subscription]

        """
        self.swagger_types = {
            'subscriptions': 'list[Subscription]'
        }

        self.attribute_map = {
            'subscriptions': 'subscriptions'
        }

        self._subscriptions = None

    @property
    def subscriptions(self):
        """
        **[Required]** Gets the subscriptions of this SubscriptionDetail.
        List of subscriptions.


        :return: The subscriptions of this SubscriptionDetail.
        :rtype: list[oci.fusion_apps.models.Subscription]
        """
        return self._subscriptions

    @subscriptions.setter
    def subscriptions(self, subscriptions):
        """
        Sets the subscriptions of this SubscriptionDetail.
        List of subscriptions.


        :param subscriptions: The subscriptions of this SubscriptionDetail.
        :type: list[oci.fusion_apps.models.Subscription]
        """
        self._subscriptions = subscriptions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
