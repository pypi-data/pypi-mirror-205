# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConditionGroup(object):
    """
    Condition configured on a target
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ConditionGroup object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this ConditionGroup.
        :type compartment_id: str

        :param condition:
            The value to assign to the condition property of this ConditionGroup.
        :type condition: oci.cloud_guard.models.Condition

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'condition': 'Condition'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'condition': 'condition'
        }

        self._compartment_id = None
        self._condition = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ConditionGroup.
        compartment associated with condition


        :return: The compartment_id of this ConditionGroup.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ConditionGroup.
        compartment associated with condition


        :param compartment_id: The compartment_id of this ConditionGroup.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def condition(self):
        """
        **[Required]** Gets the condition of this ConditionGroup.

        :return: The condition of this ConditionGroup.
        :rtype: oci.cloud_guard.models.Condition
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """
        Sets the condition of this ConditionGroup.

        :param condition: The condition of this ConditionGroup.
        :type: oci.cloud_guard.models.Condition
        """
        self._condition = condition

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
