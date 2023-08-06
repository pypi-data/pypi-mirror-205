# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class KeyRange(object):
    """
    The information about key range.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new KeyRange object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this KeyRange.
        :type key: oci.data_connectivity.models.ShapeField

        :param range:
            The value to assign to the range property of this KeyRange.
        :type range: list[str]

        """
        self.swagger_types = {
            'key': 'ShapeField',
            'range': 'list[str]'
        }

        self.attribute_map = {
            'key': 'key',
            'range': 'range'
        }

        self._key = None
        self._range = None

    @property
    def key(self):
        """
        Gets the key of this KeyRange.

        :return: The key of this KeyRange.
        :rtype: oci.data_connectivity.models.ShapeField
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this KeyRange.

        :param key: The key of this KeyRange.
        :type: oci.data_connectivity.models.ShapeField
        """
        self._key = key

    @property
    def range(self):
        """
        Gets the range of this KeyRange.
        The key range.


        :return: The range of this KeyRange.
        :rtype: list[str]
        """
        return self._range

    @range.setter
    def range(self, range):
        """
        Sets the range of this KeyRange.
        The key range.


        :param range: The range of this KeyRange.
        :type: list[str]
        """
        self._range = range

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
