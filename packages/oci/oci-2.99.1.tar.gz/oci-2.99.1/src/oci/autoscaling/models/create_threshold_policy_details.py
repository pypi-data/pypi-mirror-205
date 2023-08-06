# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_auto_scaling_policy_details import CreateAutoScalingPolicyDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateThresholdPolicyDetails(CreateAutoScalingPolicyDetails):
    """
    Creation details for a threshold-based autoscaling policy.

    In a threshold-based autoscaling policy, an autoscaling action is triggered when a performance metric meets
    or exceeds a threshold.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateThresholdPolicyDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.autoscaling.models.CreateThresholdPolicyDetails.policy_type` attribute
        of this class is ``threshold`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param capacity:
            The value to assign to the capacity property of this CreateThresholdPolicyDetails.
        :type capacity: oci.autoscaling.models.Capacity

        :param display_name:
            The value to assign to the display_name property of this CreateThresholdPolicyDetails.
        :type display_name: str

        :param policy_type:
            The value to assign to the policy_type property of this CreateThresholdPolicyDetails.
        :type policy_type: str

        :param is_enabled:
            The value to assign to the is_enabled property of this CreateThresholdPolicyDetails.
        :type is_enabled: bool

        :param rules:
            The value to assign to the rules property of this CreateThresholdPolicyDetails.
        :type rules: list[oci.autoscaling.models.CreateConditionDetails]

        """
        self.swagger_types = {
            'capacity': 'Capacity',
            'display_name': 'str',
            'policy_type': 'str',
            'is_enabled': 'bool',
            'rules': 'list[CreateConditionDetails]'
        }

        self.attribute_map = {
            'capacity': 'capacity',
            'display_name': 'displayName',
            'policy_type': 'policyType',
            'is_enabled': 'isEnabled',
            'rules': 'rules'
        }

        self._capacity = None
        self._display_name = None
        self._policy_type = None
        self._is_enabled = None
        self._rules = None
        self._policy_type = 'threshold'

    @property
    def rules(self):
        """
        **[Required]** Gets the rules of this CreateThresholdPolicyDetails.

        :return: The rules of this CreateThresholdPolicyDetails.
        :rtype: list[oci.autoscaling.models.CreateConditionDetails]
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """
        Sets the rules of this CreateThresholdPolicyDetails.

        :param rules: The rules of this CreateThresholdPolicyDetails.
        :type: list[oci.autoscaling.models.CreateConditionDetails]
        """
        self._rules = rules

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
