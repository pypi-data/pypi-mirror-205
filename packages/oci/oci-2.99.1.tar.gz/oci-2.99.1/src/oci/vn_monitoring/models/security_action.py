# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SecurityAction(object):
    """
    Defines the security action details taken on the traffic.
    """

    #: A constant which can be used with the action property of a SecurityAction.
    #: This constant has a value of "ALLOWED"
    ACTION_ALLOWED = "ALLOWED"

    #: A constant which can be used with the action property of a SecurityAction.
    #: This constant has a value of "DENIED"
    ACTION_DENIED = "DENIED"

    #: A constant which can be used with the action_type property of a SecurityAction.
    #: This constant has a value of "EXPLICIT"
    ACTION_TYPE_EXPLICIT = "EXPLICIT"

    #: A constant which can be used with the action_type property of a SecurityAction.
    #: This constant has a value of "IMPLICIT"
    ACTION_TYPE_IMPLICIT = "IMPLICIT"

    def __init__(self, **kwargs):
        """
        Initializes a new SecurityAction object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.vn_monitoring.models.AllowedSecurityAction`
        * :class:`~oci.vn_monitoring.models.DeniedSecurityAction`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param action:
            The value to assign to the action property of this SecurityAction.
            Allowed values for this property are: "ALLOWED", "DENIED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type action: str

        :param action_type:
            The value to assign to the action_type property of this SecurityAction.
            Allowed values for this property are: "EXPLICIT", "IMPLICIT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type action_type: str

        """
        self.swagger_types = {
            'action': 'str',
            'action_type': 'str'
        }

        self.attribute_map = {
            'action': 'action',
            'action_type': 'actionType'
        }

        self._action = None
        self._action_type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['action']

        if type == 'ALLOWED':
            return 'AllowedSecurityAction'

        if type == 'DENIED':
            return 'DeniedSecurityAction'
        else:
            return 'SecurityAction'

    @property
    def action(self):
        """
        **[Required]** Gets the action of this SecurityAction.
        Action taken on the traffic.

        Allowed values for this property are: "ALLOWED", "DENIED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The action of this SecurityAction.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this SecurityAction.
        Action taken on the traffic.


        :param action: The action of this SecurityAction.
        :type: str
        """
        allowed_values = ["ALLOWED", "DENIED"]
        if not value_allowed_none_or_none_sentinel(action, allowed_values):
            action = 'UNKNOWN_ENUM_VALUE'
        self._action = action

    @property
    def action_type(self):
        """
        **[Required]** Gets the action_type of this SecurityAction.
        Type of the `SecurityAction`.

        Allowed values for this property are: "EXPLICIT", "IMPLICIT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The action_type of this SecurityAction.
        :rtype: str
        """
        return self._action_type

    @action_type.setter
    def action_type(self, action_type):
        """
        Sets the action_type of this SecurityAction.
        Type of the `SecurityAction`.


        :param action_type: The action_type of this SecurityAction.
        :type: str
        """
        allowed_values = ["EXPLICIT", "IMPLICIT"]
        if not value_allowed_none_or_none_sentinel(action_type, allowed_values):
            action_type = 'UNKNOWN_ENUM_VALUE'
        self._action_type = action_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
