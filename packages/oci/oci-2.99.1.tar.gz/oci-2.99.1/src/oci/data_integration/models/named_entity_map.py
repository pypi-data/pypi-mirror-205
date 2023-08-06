# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .field_map import FieldMap
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class NamedEntityMap(FieldMap):
    """
    A named field map.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new NamedEntityMap object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.NamedEntityMap.model_type` attribute
        of this class is ``NAMED_ENTITY_MAP`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this NamedEntityMap.
            Allowed values for this property are: "DIRECT_NAMED_FIELD_MAP", "COMPOSITE_FIELD_MAP", "DIRECT_FIELD_MAP", "RULE_BASED_FIELD_MAP", "CONDITIONAL_COMPOSITE_FIELD_MAP", "NAMED_ENTITY_MAP", "RULE_BASED_ENTITY_MAP"
        :type model_type: str

        :param description:
            The value to assign to the description property of this NamedEntityMap.
        :type description: str

        :param key:
            The value to assign to the key property of this NamedEntityMap.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this NamedEntityMap.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this NamedEntityMap.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param config_values:
            The value to assign to the config_values property of this NamedEntityMap.
        :type config_values: oci.data_integration.models.ConfigValues

        :param source_entity:
            The value to assign to the source_entity property of this NamedEntityMap.
        :type source_entity: str

        :param target_entity:
            The value to assign to the target_entity property of this NamedEntityMap.
        :type target_entity: str

        :param object_status:
            The value to assign to the object_status property of this NamedEntityMap.
        :type object_status: int

        """
        self.swagger_types = {
            'model_type': 'str',
            'description': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'config_values': 'ConfigValues',
            'source_entity': 'str',
            'target_entity': 'str',
            'object_status': 'int'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'description': 'description',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'config_values': 'configValues',
            'source_entity': 'sourceEntity',
            'target_entity': 'targetEntity',
            'object_status': 'objectStatus'
        }

        self._model_type = None
        self._description = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._config_values = None
        self._source_entity = None
        self._target_entity = None
        self._object_status = None
        self._model_type = 'NAMED_ENTITY_MAP'

    @property
    def key(self):
        """
        Gets the key of this NamedEntityMap.
        The object key.


        :return: The key of this NamedEntityMap.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this NamedEntityMap.
        The object key.


        :param key: The key of this NamedEntityMap.
        :type: str
        """
        self._key = key

    @property
    def model_version(self):
        """
        Gets the model_version of this NamedEntityMap.
        The object's model version.


        :return: The model_version of this NamedEntityMap.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """
        Sets the model_version of this NamedEntityMap.
        The object's model version.


        :param model_version: The model_version of this NamedEntityMap.
        :type: str
        """
        self._model_version = model_version

    @property
    def parent_ref(self):
        """
        Gets the parent_ref of this NamedEntityMap.

        :return: The parent_ref of this NamedEntityMap.
        :rtype: oci.data_integration.models.ParentReference
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """
        Sets the parent_ref of this NamedEntityMap.

        :param parent_ref: The parent_ref of this NamedEntityMap.
        :type: oci.data_integration.models.ParentReference
        """
        self._parent_ref = parent_ref

    @property
    def config_values(self):
        """
        Gets the config_values of this NamedEntityMap.

        :return: The config_values of this NamedEntityMap.
        :rtype: oci.data_integration.models.ConfigValues
        """
        return self._config_values

    @config_values.setter
    def config_values(self, config_values):
        """
        Sets the config_values of this NamedEntityMap.

        :param config_values: The config_values of this NamedEntityMap.
        :type: oci.data_integration.models.ConfigValues
        """
        self._config_values = config_values

    @property
    def source_entity(self):
        """
        Gets the source_entity of this NamedEntityMap.
        The source entity name.


        :return: The source_entity of this NamedEntityMap.
        :rtype: str
        """
        return self._source_entity

    @source_entity.setter
    def source_entity(self, source_entity):
        """
        Sets the source_entity of this NamedEntityMap.
        The source entity name.


        :param source_entity: The source_entity of this NamedEntityMap.
        :type: str
        """
        self._source_entity = source_entity

    @property
    def target_entity(self):
        """
        Gets the target_entity of this NamedEntityMap.
        The target entity name.


        :return: The target_entity of this NamedEntityMap.
        :rtype: str
        """
        return self._target_entity

    @target_entity.setter
    def target_entity(self, target_entity):
        """
        Sets the target_entity of this NamedEntityMap.
        The target entity name.


        :param target_entity: The target_entity of this NamedEntityMap.
        :type: str
        """
        self._target_entity = target_entity

    @property
    def object_status(self):
        """
        Gets the object_status of this NamedEntityMap.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :return: The object_status of this NamedEntityMap.
        :rtype: int
        """
        return self._object_status

    @object_status.setter
    def object_status(self, object_status):
        """
        Sets the object_status of this NamedEntityMap.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :param object_status: The object_status of this NamedEntityMap.
        :type: int
        """
        self._object_status = object_status

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
