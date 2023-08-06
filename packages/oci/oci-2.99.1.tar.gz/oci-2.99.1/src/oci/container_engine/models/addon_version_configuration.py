# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddonVersionConfiguration(object):
    """
    Addon version configuration details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddonVersionConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param is_required:
            The value to assign to the is_required property of this AddonVersionConfiguration.
        :type is_required: bool

        :param key:
            The value to assign to the key property of this AddonVersionConfiguration.
        :type key: str

        :param value:
            The value to assign to the value property of this AddonVersionConfiguration.
        :type value: str

        :param display_name:
            The value to assign to the display_name property of this AddonVersionConfiguration.
        :type display_name: str

        :param description:
            The value to assign to the description property of this AddonVersionConfiguration.
        :type description: str

        """
        self.swagger_types = {
            'is_required': 'bool',
            'key': 'str',
            'value': 'str',
            'display_name': 'str',
            'description': 'str'
        }

        self.attribute_map = {
            'is_required': 'isRequired',
            'key': 'key',
            'value': 'value',
            'display_name': 'displayName',
            'description': 'description'
        }

        self._is_required = None
        self._key = None
        self._value = None
        self._display_name = None
        self._description = None

    @property
    def is_required(self):
        """
        Gets the is_required of this AddonVersionConfiguration.
        If the the configuration is required or not.


        :return: The is_required of this AddonVersionConfiguration.
        :rtype: bool
        """
        return self._is_required

    @is_required.setter
    def is_required(self, is_required):
        """
        Sets the is_required of this AddonVersionConfiguration.
        If the the configuration is required or not.


        :param is_required: The is_required of this AddonVersionConfiguration.
        :type: bool
        """
        self._is_required = is_required

    @property
    def key(self):
        """
        Gets the key of this AddonVersionConfiguration.
        Addon configuration key


        :return: The key of this AddonVersionConfiguration.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this AddonVersionConfiguration.
        Addon configuration key


        :param key: The key of this AddonVersionConfiguration.
        :type: str
        """
        self._key = key

    @property
    def value(self):
        """
        Gets the value of this AddonVersionConfiguration.
        Addon configuration value


        :return: The value of this AddonVersionConfiguration.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this AddonVersionConfiguration.
        Addon configuration value


        :param value: The value of this AddonVersionConfiguration.
        :type: str
        """
        self._value = value

    @property
    def display_name(self):
        """
        Gets the display_name of this AddonVersionConfiguration.
        Display name of addon version.


        :return: The display_name of this AddonVersionConfiguration.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this AddonVersionConfiguration.
        Display name of addon version.


        :param display_name: The display_name of this AddonVersionConfiguration.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this AddonVersionConfiguration.
        Information about the addon version configuration.


        :return: The description of this AddonVersionConfiguration.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AddonVersionConfiguration.
        Information about the addon version configuration.


        :param description: The description of this AddonVersionConfiguration.
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
