# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class JsonWebTokenClaim(object):
    """
    An individual JWT claim.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new JsonWebTokenClaim object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this JsonWebTokenClaim.
        :type key: str

        :param values:
            The value to assign to the values property of this JsonWebTokenClaim.
        :type values: list[str]

        :param is_required:
            The value to assign to the is_required property of this JsonWebTokenClaim.
        :type is_required: bool

        """
        self.swagger_types = {
            'key': 'str',
            'values': 'list[str]',
            'is_required': 'bool'
        }

        self.attribute_map = {
            'key': 'key',
            'values': 'values',
            'is_required': 'isRequired'
        }

        self._key = None
        self._values = None
        self._is_required = None

    @property
    def key(self):
        """
        **[Required]** Gets the key of this JsonWebTokenClaim.
        Name of the claim.


        :return: The key of this JsonWebTokenClaim.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this JsonWebTokenClaim.
        Name of the claim.


        :param key: The key of this JsonWebTokenClaim.
        :type: str
        """
        self._key = key

    @property
    def values(self):
        """
        Gets the values of this JsonWebTokenClaim.
        The list of acceptable values for a given claim.
        If this value is \"null\" or empty and \"isRequired\" set to \"true\", then
        the presence of this claim in the JWT is validated.


        :return: The values of this JsonWebTokenClaim.
        :rtype: list[str]
        """
        return self._values

    @values.setter
    def values(self, values):
        """
        Sets the values of this JsonWebTokenClaim.
        The list of acceptable values for a given claim.
        If this value is \"null\" or empty and \"isRequired\" set to \"true\", then
        the presence of this claim in the JWT is validated.


        :param values: The values of this JsonWebTokenClaim.
        :type: list[str]
        """
        self._values = values

    @property
    def is_required(self):
        """
        Gets the is_required of this JsonWebTokenClaim.
        Whether the claim is required to be present in the JWT or not. If set
        to \"false\", the claim values will be matched only if the claim is
        present in the JWT.


        :return: The is_required of this JsonWebTokenClaim.
        :rtype: bool
        """
        return self._is_required

    @is_required.setter
    def is_required(self, is_required):
        """
        Sets the is_required of this JsonWebTokenClaim.
        Whether the claim is required to be present in the JWT or not. If set
        to \"false\", the claim values will be matched only if the claim is
        present in the JWT.


        :param is_required: The is_required of this JsonWebTokenClaim.
        :type: bool
        """
        self._is_required = is_required

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
