# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PolicyDetails(object):
    """
    A policy required for this PBF execution.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PolicyDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param policy:
            The value to assign to the policy property of this PolicyDetails.
        :type policy: str

        :param description:
            The value to assign to the description property of this PolicyDetails.
        :type description: str

        """
        self.swagger_types = {
            'policy': 'str',
            'description': 'str'
        }

        self.attribute_map = {
            'policy': 'policy',
            'description': 'description'
        }

        self._policy = None
        self._description = None

    @property
    def policy(self):
        """
        **[Required]** Gets the policy of this PolicyDetails.
        Policy required for PBF execution


        :return: The policy of this PolicyDetails.
        :rtype: str
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """
        Sets the policy of this PolicyDetails.
        Policy required for PBF execution


        :param policy: The policy of this PolicyDetails.
        :type: str
        """
        self._policy = policy

    @property
    def description(self):
        """
        **[Required]** Gets the description of this PolicyDetails.
        Details about why this policy is required and what it will be used for.


        :return: The description of this PolicyDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PolicyDetails.
        Details about why this policy is required and what it will be used for.


        :param description: The description of this PolicyDetails.
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
