# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SubscriptionInfo(object):
    """
    A single subscription's details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SubscriptionInfo object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param spm_subscription_id:
            The value to assign to the spm_subscription_id property of this SubscriptionInfo.
        :type spm_subscription_id: str

        :param service:
            The value to assign to the service property of this SubscriptionInfo.
        :type service: str

        :param start_date:
            The value to assign to the start_date property of this SubscriptionInfo.
        :type start_date: datetime

        :param end_date:
            The value to assign to the end_date property of this SubscriptionInfo.
        :type end_date: datetime

        :param skus:
            The value to assign to the skus property of this SubscriptionInfo.
        :type skus: list[oci.tenant_manager_control_plane.models.Sku]

        """
        self.swagger_types = {
            'spm_subscription_id': 'str',
            'service': 'str',
            'start_date': 'datetime',
            'end_date': 'datetime',
            'skus': 'list[Sku]'
        }

        self.attribute_map = {
            'spm_subscription_id': 'spmSubscriptionId',
            'service': 'service',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'skus': 'skus'
        }

        self._spm_subscription_id = None
        self._service = None
        self._start_date = None
        self._end_date = None
        self._skus = None

    @property
    def spm_subscription_id(self):
        """
        **[Required]** Gets the spm_subscription_id of this SubscriptionInfo.
        Subscription ID.


        :return: The spm_subscription_id of this SubscriptionInfo.
        :rtype: str
        """
        return self._spm_subscription_id

    @spm_subscription_id.setter
    def spm_subscription_id(self, spm_subscription_id):
        """
        Sets the spm_subscription_id of this SubscriptionInfo.
        Subscription ID.


        :param spm_subscription_id: The spm_subscription_id of this SubscriptionInfo.
        :type: str
        """
        self._spm_subscription_id = spm_subscription_id

    @property
    def service(self):
        """
        **[Required]** Gets the service of this SubscriptionInfo.
        Subscription service name.


        :return: The service of this SubscriptionInfo.
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service):
        """
        Sets the service of this SubscriptionInfo.
        Subscription service name.


        :param service: The service of this SubscriptionInfo.
        :type: str
        """
        self._service = service

    @property
    def start_date(self):
        """
        **[Required]** Gets the start_date of this SubscriptionInfo.
        Subscription start date. An RFC 3339-formatted date and time string.


        :return: The start_date of this SubscriptionInfo.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this SubscriptionInfo.
        Subscription start date. An RFC 3339-formatted date and time string.


        :param start_date: The start_date of this SubscriptionInfo.
        :type: datetime
        """
        self._start_date = start_date

    @property
    def end_date(self):
        """
        **[Required]** Gets the end_date of this SubscriptionInfo.
        Subscription end date. An RFC 3339-formatted date and time string.


        :return: The end_date of this SubscriptionInfo.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this SubscriptionInfo.
        Subscription end date. An RFC 3339-formatted date and time string.


        :param end_date: The end_date of this SubscriptionInfo.
        :type: datetime
        """
        self._end_date = end_date

    @property
    def skus(self):
        """
        **[Required]** Gets the skus of this SubscriptionInfo.
        List of SKUs the subscription contains.


        :return: The skus of this SubscriptionInfo.
        :rtype: list[oci.tenant_manager_control_plane.models.Sku]
        """
        return self._skus

    @skus.setter
    def skus(self, skus):
        """
        Sets the skus of this SubscriptionInfo.
        List of SKUs the subscription contains.


        :param skus: The skus of this SubscriptionInfo.
        :type: list[oci.tenant_manager_control_plane.models.Sku]
        """
        self._skus = skus

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
