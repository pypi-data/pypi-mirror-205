# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .typed_object import TypedObject
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class InputProxyField(TypedObject):
    """
    A proxy field to be used as an input field.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new InputProxyField object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.InputProxyField.model_type` attribute
        of this class is ``INPUT_PROXY_FIELD`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this InputProxyField.
            Allowed values for this property are: "SHAPE", "INPUT_PORT", "SHAPE_FIELD", "INPUT_FIELD", "DERIVED_FIELD", "MACRO_FIELD", "OUTPUT_FIELD", "DYNAMIC_PROXY_FIELD", "OUTPUT_PORT", "DYNAMIC_INPUT_FIELD", "PROXY_FIELD", "PARAMETER", "PIVOT_FIELD", "MACRO_PIVOT_FIELD", "CONDITIONAL_OUTPUT_PORT", "INPUT_PROXY_FIELD", "MATERIALIZED_DYNAMIC_FIELD", "DECISION_OUTPUT_PORT"
        :type model_type: str

        :param key:
            The value to assign to the key property of this InputProxyField.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this InputProxyField.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this InputProxyField.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param config_values:
            The value to assign to the config_values property of this InputProxyField.
        :type config_values: oci.data_integration.models.ConfigValues

        :param object_status:
            The value to assign to the object_status property of this InputProxyField.
        :type object_status: int

        :param name:
            The value to assign to the name property of this InputProxyField.
        :type name: str

        :param description:
            The value to assign to the description property of this InputProxyField.
        :type description: str

        :param scope:
            The value to assign to the scope property of this InputProxyField.
        :type scope: object

        :param type:
            The value to assign to the type property of this InputProxyField.
        :type type: oci.data_integration.models.BaseType

        :param labels:
            The value to assign to the labels property of this InputProxyField.
        :type labels: list[str]

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'config_values': 'ConfigValues',
            'object_status': 'int',
            'name': 'str',
            'description': 'str',
            'scope': 'object',
            'type': 'BaseType',
            'labels': 'list[str]'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'config_values': 'configValues',
            'object_status': 'objectStatus',
            'name': 'name',
            'description': 'description',
            'scope': 'scope',
            'type': 'type',
            'labels': 'labels'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._config_values = None
        self._object_status = None
        self._name = None
        self._description = None
        self._scope = None
        self._type = None
        self._labels = None
        self._model_type = 'INPUT_PROXY_FIELD'

    @property
    def scope(self):
        """
        Gets the scope of this InputProxyField.
        Reference to a typed object, this can be either a key value to an object within the document, a shall referenced to a `TypedObject` or a full `TypedObject` definition.


        :return: The scope of this InputProxyField.
        :rtype: object
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """
        Sets the scope of this InputProxyField.
        Reference to a typed object, this can be either a key value to an object within the document, a shall referenced to a `TypedObject` or a full `TypedObject` definition.


        :param scope: The scope of this InputProxyField.
        :type: object
        """
        self._scope = scope

    @property
    def type(self):
        """
        Gets the type of this InputProxyField.

        :return: The type of this InputProxyField.
        :rtype: oci.data_integration.models.BaseType
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this InputProxyField.

        :param type: The type of this InputProxyField.
        :type: oci.data_integration.models.BaseType
        """
        self._type = type

    @property
    def labels(self):
        """
        Gets the labels of this InputProxyField.
        Labels are keywords or labels that you can add to data assets, dataflows and so on. You can define your own labels and use them to categorize content.


        :return: The labels of this InputProxyField.
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """
        Sets the labels of this InputProxyField.
        Labels are keywords or labels that you can add to data assets, dataflows and so on. You can define your own labels and use them to categorize content.


        :param labels: The labels of this InputProxyField.
        :type: list[str]
        """
        self._labels = labels

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
