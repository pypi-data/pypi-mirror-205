# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .dimension_value_details import DimensionValueDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class StaticDimensionValue(DimensionValueDetails):
    """
    Static type of dimension value (passed as-is).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new StaticDimensionValue object with values from keyword arguments. The default value of the :py:attr:`~oci.sch.models.StaticDimensionValue.kind` attribute
        of this class is ``static`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this StaticDimensionValue.
            Allowed values for this property are: "jmesPath", "static"
        :type kind: str

        :param value:
            The value to assign to the value property of this StaticDimensionValue.
        :type value: str

        """
        self.swagger_types = {
            'kind': 'str',
            'value': 'str'
        }

        self.attribute_map = {
            'kind': 'kind',
            'value': 'value'
        }

        self._kind = None
        self._value = None
        self._kind = 'static'

    @property
    def value(self):
        """
        **[Required]** Gets the value of this StaticDimensionValue.
        The data extracted from the specified dimension value (passed as-is). Unicode characters only.
        For information on valid dimension keys and values, see :func:`metric_data_details`.


        :return: The value of this StaticDimensionValue.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this StaticDimensionValue.
        The data extracted from the specified dimension value (passed as-is). Unicode characters only.
        For information on valid dimension keys and values, see :func:`metric_data_details`.


        :param value: The value of this StaticDimensionValue.
        :type: str
        """
        self._value = value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
