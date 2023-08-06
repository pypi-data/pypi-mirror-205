# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyDeviceNonCompliances(object):
    """
    Device Non Compliances
    """

    #: A constant which can be used with the action property of a MyDeviceNonCompliances.
    #: This constant has a value of "NOTIFY"
    ACTION_NOTIFY = "NOTIFY"

    #: A constant which can be used with the action property of a MyDeviceNonCompliances.
    #: This constant has a value of "BLOCK"
    ACTION_BLOCK = "BLOCK"

    #: A constant which can be used with the action property of a MyDeviceNonCompliances.
    #: This constant has a value of "ALLOW"
    ACTION_ALLOW = "ALLOW"

    #: A constant which can be used with the action property of a MyDeviceNonCompliances.
    #: This constant has a value of "UNKNOWN"
    ACTION_UNKNOWN = "UNKNOWN"

    def __init__(self, **kwargs):
        """
        Initializes a new MyDeviceNonCompliances object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this MyDeviceNonCompliances.
        :type name: str

        :param value:
            The value to assign to the value property of this MyDeviceNonCompliances.
        :type value: str

        :param action:
            The value to assign to the action property of this MyDeviceNonCompliances.
            Allowed values for this property are: "NOTIFY", "BLOCK", "ALLOW", "UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type action: str

        """
        self.swagger_types = {
            'name': 'str',
            'value': 'str',
            'action': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'value': 'value',
            'action': 'action'
        }

        self._name = None
        self._value = None
        self._action = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this MyDeviceNonCompliances.
        Device Compliance name

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The name of this MyDeviceNonCompliances.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this MyDeviceNonCompliances.
        Device Compliance name

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param name: The name of this MyDeviceNonCompliances.
        :type: str
        """
        self._name = name

    @property
    def value(self):
        """
        **[Required]** Gets the value of this MyDeviceNonCompliances.
        Device Compliance value

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this MyDeviceNonCompliances.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this MyDeviceNonCompliances.
        Device Compliance value

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this MyDeviceNonCompliances.
        :type: str
        """
        self._value = value

    @property
    def action(self):
        """
        **[Required]** Gets the action of this MyDeviceNonCompliances.
        Device Compliance Action

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "NOTIFY", "BLOCK", "ALLOW", "UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The action of this MyDeviceNonCompliances.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this MyDeviceNonCompliances.
        Device Compliance Action

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param action: The action of this MyDeviceNonCompliances.
        :type: str
        """
        allowed_values = ["NOTIFY", "BLOCK", "ALLOW", "UNKNOWN"]
        if not value_allowed_none_or_none_sentinel(action, allowed_values):
            action = 'UNKNOWN_ENUM_VALUE'
        self._action = action

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
