# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConfigDetails(object):
    """
    Details about the required and optional Function configurations needed for proper performance of the PBF.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ConfigDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this ConfigDetails.
        :type key: str

        :param description:
            The value to assign to the description property of this ConfigDetails.
        :type description: str

        :param is_optional:
            The value to assign to the is_optional property of this ConfigDetails.
        :type is_optional: bool

        """
        self.swagger_types = {
            'key': 'str',
            'description': 'str',
            'is_optional': 'bool'
        }

        self.attribute_map = {
            'key': 'key',
            'description': 'description',
            'is_optional': 'isOptional'
        }

        self._key = None
        self._description = None
        self._is_optional = None

    @property
    def key(self):
        """
        **[Required]** Gets the key of this ConfigDetails.
        The key name of the config param.


        :return: The key of this ConfigDetails.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this ConfigDetails.
        The key name of the config param.


        :param key: The key of this ConfigDetails.
        :type: str
        """
        self._key = key

    @property
    def description(self):
        """
        **[Required]** Gets the description of this ConfigDetails.
        Details about why this config is required and what it will be used for.


        :return: The description of this ConfigDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ConfigDetails.
        Details about why this config is required and what it will be used for.


        :param description: The description of this ConfigDetails.
        :type: str
        """
        self._description = description

    @property
    def is_optional(self):
        """
        Gets the is_optional of this ConfigDetails.
        Is this a required config or an optional one. Requests with required config params missing will be rejected.


        :return: The is_optional of this ConfigDetails.
        :rtype: bool
        """
        return self._is_optional

    @is_optional.setter
    def is_optional(self, is_optional):
        """
        Sets the is_optional of this ConfigDetails.
        Is this a required config or an optional one. Requests with required config params missing will be rejected.


        :param is_optional: The is_optional of this ConfigDetails.
        :type: bool
        """
        self._is_optional = is_optional

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
