# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .web_app_firewall_policy_rule import WebAppFirewallPolicyRule
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RequestRateLimitingRule(WebAppFirewallPolicyRule):
    """
    Rule that represents RequestRateLimitingConfigurations.
    Only actions of the following types are allowed to be referenced in this rule:
    * CHECK
    * RETURN_HTTP_RESPONSE
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RequestRateLimitingRule object with values from keyword arguments. The default value of the :py:attr:`~oci.waf.models.RequestRateLimitingRule.type` attribute
        of this class is ``REQUEST_RATE_LIMITING`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this RequestRateLimitingRule.
            Allowed values for this property are: "ACCESS_CONTROL", "PROTECTION", "REQUEST_RATE_LIMITING"
        :type type: str

        :param name:
            The value to assign to the name property of this RequestRateLimitingRule.
        :type name: str

        :param condition_language:
            The value to assign to the condition_language property of this RequestRateLimitingRule.
            Allowed values for this property are: "JMESPATH"
        :type condition_language: str

        :param condition:
            The value to assign to the condition property of this RequestRateLimitingRule.
        :type condition: str

        :param action_name:
            The value to assign to the action_name property of this RequestRateLimitingRule.
        :type action_name: str

        :param configurations:
            The value to assign to the configurations property of this RequestRateLimitingRule.
        :type configurations: list[oci.waf.models.RequestRateLimitingConfiguration]

        """
        self.swagger_types = {
            'type': 'str',
            'name': 'str',
            'condition_language': 'str',
            'condition': 'str',
            'action_name': 'str',
            'configurations': 'list[RequestRateLimitingConfiguration]'
        }

        self.attribute_map = {
            'type': 'type',
            'name': 'name',
            'condition_language': 'conditionLanguage',
            'condition': 'condition',
            'action_name': 'actionName',
            'configurations': 'configurations'
        }

        self._type = None
        self._name = None
        self._condition_language = None
        self._condition = None
        self._action_name = None
        self._configurations = None
        self._type = 'REQUEST_RATE_LIMITING'

    @property
    def configurations(self):
        """
        **[Required]** Gets the configurations of this RequestRateLimitingRule.
        Rate Limiting Configurations.
        Each configuration counts requests towards its own `requestsLimit`.


        :return: The configurations of this RequestRateLimitingRule.
        :rtype: list[oci.waf.models.RequestRateLimitingConfiguration]
        """
        return self._configurations

    @configurations.setter
    def configurations(self, configurations):
        """
        Sets the configurations of this RequestRateLimitingRule.
        Rate Limiting Configurations.
        Each configuration counts requests towards its own `requestsLimit`.


        :param configurations: The configurations of this RequestRateLimitingRule.
        :type: list[oci.waf.models.RequestRateLimitingConfiguration]
        """
        self._configurations = configurations

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
