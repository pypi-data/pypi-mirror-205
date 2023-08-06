# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AuthorizeSubscriptionPaymentDetails(object):
    """
    Request object for a subscription payment authorization
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AuthorizeSubscriptionPaymentDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param subscription:
            The value to assign to the subscription property of this AuthorizeSubscriptionPaymentDetails.
        :type subscription: oci.osp_gateway.models.Subscription

        :param language_code:
            The value to assign to the language_code property of this AuthorizeSubscriptionPaymentDetails.
        :type language_code: str

        :param email:
            The value to assign to the email property of this AuthorizeSubscriptionPaymentDetails.
        :type email: str

        """
        self.swagger_types = {
            'subscription': 'Subscription',
            'language_code': 'str',
            'email': 'str'
        }

        self.attribute_map = {
            'subscription': 'subscription',
            'language_code': 'languageCode',
            'email': 'email'
        }

        self._subscription = None
        self._language_code = None
        self._email = None

    @property
    def subscription(self):
        """
        **[Required]** Gets the subscription of this AuthorizeSubscriptionPaymentDetails.

        :return: The subscription of this AuthorizeSubscriptionPaymentDetails.
        :rtype: oci.osp_gateway.models.Subscription
        """
        return self._subscription

    @subscription.setter
    def subscription(self, subscription):
        """
        Sets the subscription of this AuthorizeSubscriptionPaymentDetails.

        :param subscription: The subscription of this AuthorizeSubscriptionPaymentDetails.
        :type: oci.osp_gateway.models.Subscription
        """
        self._subscription = subscription

    @property
    def language_code(self):
        """
        **[Required]** Gets the language_code of this AuthorizeSubscriptionPaymentDetails.
        Language code


        :return: The language_code of this AuthorizeSubscriptionPaymentDetails.
        :rtype: str
        """
        return self._language_code

    @language_code.setter
    def language_code(self, language_code):
        """
        Sets the language_code of this AuthorizeSubscriptionPaymentDetails.
        Language code


        :param language_code: The language_code of this AuthorizeSubscriptionPaymentDetails.
        :type: str
        """
        self._language_code = language_code

    @property
    def email(self):
        """
        **[Required]** Gets the email of this AuthorizeSubscriptionPaymentDetails.
        User email


        :return: The email of this AuthorizeSubscriptionPaymentDetails.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this AuthorizeSubscriptionPaymentDetails.
        User email


        :param email: The email of this AuthorizeSubscriptionPaymentDetails.
        :type: str
        """
        self._email = email

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
