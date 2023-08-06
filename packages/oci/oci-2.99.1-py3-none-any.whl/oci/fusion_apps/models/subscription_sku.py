# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SubscriptionSku(object):
    """
    SKU information.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SubscriptionSku object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param sku:
            The value to assign to the sku property of this SubscriptionSku.
        :type sku: str

        :param license_part_description:
            The value to assign to the license_part_description property of this SubscriptionSku.
        :type license_part_description: str

        :param metric_name:
            The value to assign to the metric_name property of this SubscriptionSku.
        :type metric_name: str

        :param quantity:
            The value to assign to the quantity property of this SubscriptionSku.
        :type quantity: int

        :param description:
            The value to assign to the description property of this SubscriptionSku.
        :type description: str

        """
        self.swagger_types = {
            'sku': 'str',
            'license_part_description': 'str',
            'metric_name': 'str',
            'quantity': 'int',
            'description': 'str'
        }

        self.attribute_map = {
            'sku': 'sku',
            'license_part_description': 'licensePartDescription',
            'metric_name': 'metricName',
            'quantity': 'quantity',
            'description': 'description'
        }

        self._sku = None
        self._license_part_description = None
        self._metric_name = None
        self._quantity = None
        self._description = None

    @property
    def sku(self):
        """
        **[Required]** Gets the sku of this SubscriptionSku.
        Stock keeping unit id.


        :return: The sku of this SubscriptionSku.
        :rtype: str
        """
        return self._sku

    @sku.setter
    def sku(self, sku):
        """
        Sets the sku of this SubscriptionSku.
        Stock keeping unit id.


        :param sku: The sku of this SubscriptionSku.
        :type: str
        """
        self._sku = sku

    @property
    def license_part_description(self):
        """
        Gets the license_part_description of this SubscriptionSku.
        Description of the covered product belonging to this Sku.


        :return: The license_part_description of this SubscriptionSku.
        :rtype: str
        """
        return self._license_part_description

    @license_part_description.setter
    def license_part_description(self, license_part_description):
        """
        Sets the license_part_description of this SubscriptionSku.
        Description of the covered product belonging to this Sku.


        :param license_part_description: The license_part_description of this SubscriptionSku.
        :type: str
        """
        self._license_part_description = license_part_description

    @property
    def metric_name(self):
        """
        Gets the metric_name of this SubscriptionSku.
        Base metric for billing the service.


        :return: The metric_name of this SubscriptionSku.
        :rtype: str
        """
        return self._metric_name

    @metric_name.setter
    def metric_name(self, metric_name):
        """
        Sets the metric_name of this SubscriptionSku.
        Base metric for billing the service.


        :param metric_name: The metric_name of this SubscriptionSku.
        :type: str
        """
        self._metric_name = metric_name

    @property
    def quantity(self):
        """
        **[Required]** Gets the quantity of this SubscriptionSku.
        Quantity of the stock units.


        :return: The quantity of this SubscriptionSku.
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """
        Sets the quantity of this SubscriptionSku.
        Quantity of the stock units.


        :param quantity: The quantity of this SubscriptionSku.
        :type: int
        """
        self._quantity = quantity

    @property
    def description(self):
        """
        Gets the description of this SubscriptionSku.
        Description of the stock units.


        :return: The description of this SubscriptionSku.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this SubscriptionSku.
        Description of the stock units.


        :param description: The description of this SubscriptionSku.
        :type: str
        """
        self._description = description

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
