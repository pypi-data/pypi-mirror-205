# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .base_type import BaseType
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MapType(BaseType):
    """
    Map type object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MapType object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.MapType.model_type` attribute
        of this class is ``MAP_TYPE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this MapType.
            Allowed values for this property are: "DYNAMIC_TYPE", "STRUCTURED_TYPE", "DATA_TYPE", "JAVA_TYPE", "CONFIGURED_TYPE", "COMPOSITE_TYPE", "DERIVED_TYPE", "ARRAY_TYPE", "MAP_TYPE", "MATERIALIZED_COMPOSITE_TYPE"
        :type model_type: str

        :param key:
            The value to assign to the key property of this MapType.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this MapType.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this MapType.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param name:
            The value to assign to the name property of this MapType.
        :type name: str

        :param object_status:
            The value to assign to the object_status property of this MapType.
        :type object_status: int

        :param description:
            The value to assign to the description property of this MapType.
        :type description: str

        :param key_element_type:
            The value to assign to the key_element_type property of this MapType.
        :type key_element_type: str

        :param value_element_type:
            The value to assign to the value_element_type property of this MapType.
        :type value_element_type: str

        :param contains_null:
            The value to assign to the contains_null property of this MapType.
        :type contains_null: bool

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'object_status': 'int',
            'description': 'str',
            'key_element_type': 'str',
            'value_element_type': 'str',
            'contains_null': 'bool'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'object_status': 'objectStatus',
            'description': 'description',
            'key_element_type': 'keyElementType',
            'value_element_type': 'valueElementType',
            'contains_null': 'containsNull'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._object_status = None
        self._description = None
        self._key_element_type = None
        self._value_element_type = None
        self._contains_null = None
        self._model_type = 'MAP_TYPE'

    @property
    def key_element_type(self):
        """
        Gets the key_element_type of this MapType.
        Seeded type


        :return: The key_element_type of this MapType.
        :rtype: str
        """
        return self._key_element_type

    @key_element_type.setter
    def key_element_type(self, key_element_type):
        """
        Sets the key_element_type of this MapType.
        Seeded type


        :param key_element_type: The key_element_type of this MapType.
        :type: str
        """
        self._key_element_type = key_element_type

    @property
    def value_element_type(self):
        """
        Gets the value_element_type of this MapType.
        Seeded type


        :return: The value_element_type of this MapType.
        :rtype: str
        """
        return self._value_element_type

    @value_element_type.setter
    def value_element_type(self, value_element_type):
        """
        Sets the value_element_type of this MapType.
        Seeded type


        :param value_element_type: The value_element_type of this MapType.
        :type: str
        """
        self._value_element_type = value_element_type

    @property
    def contains_null(self):
        """
        Gets the contains_null of this MapType.
        Defines whether null values are allowed.


        :return: The contains_null of this MapType.
        :rtype: bool
        """
        return self._contains_null

    @contains_null.setter
    def contains_null(self, contains_null):
        """
        Sets the contains_null of this MapType.
        Defines whether null values are allowed.


        :param contains_null: The contains_null of this MapType.
        :type: bool
        """
        self._contains_null = contains_null

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
