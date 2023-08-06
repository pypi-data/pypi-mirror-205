# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ReferencedDataObject(object):
    """
    The input Operation for which derived entity is to be formed.
    """

    #: A constant which can be used with the model_type property of a ReferencedDataObject.
    #: This constant has a value of "PROCEDURE"
    MODEL_TYPE_PROCEDURE = "PROCEDURE"

    #: A constant which can be used with the model_type property of a ReferencedDataObject.
    #: This constant has a value of "API"
    MODEL_TYPE_API = "API"

    def __init__(self, **kwargs):
        """
        Initializes a new ReferencedDataObject object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.data_integration.models.ReferencedDataObjectFromAPI`
        * :class:`~oci.data_integration.models.ReferencedDataObjectFromProcedure`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this ReferencedDataObject.
            Allowed values for this property are: "PROCEDURE", "API", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type model_type: str

        :param model_version:
            The value to assign to the model_version property of this ReferencedDataObject.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this ReferencedDataObject.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param name:
            The value to assign to the name property of this ReferencedDataObject.
        :type name: str

        :param object_version:
            The value to assign to the object_version property of this ReferencedDataObject.
        :type object_version: int

        :param resource_name:
            The value to assign to the resource_name property of this ReferencedDataObject.
        :type resource_name: str

        :param object_status:
            The value to assign to the object_status property of this ReferencedDataObject.
        :type object_status: int

        :param external_key:
            The value to assign to the external_key property of this ReferencedDataObject.
        :type external_key: str

        """
        self.swagger_types = {
            'model_type': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'object_version': 'int',
            'resource_name': 'str',
            'object_status': 'int',
            'external_key': 'str'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'object_version': 'objectVersion',
            'resource_name': 'resourceName',
            'object_status': 'objectStatus',
            'external_key': 'externalKey'
        }

        self._model_type = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._object_version = None
        self._resource_name = None
        self._object_status = None
        self._external_key = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['modelType']

        if type == 'API':
            return 'ReferencedDataObjectFromAPI'

        if type == 'PROCEDURE':
            return 'ReferencedDataObjectFromProcedure'
        else:
            return 'ReferencedDataObject'

    @property
    def model_type(self):
        """
        **[Required]** Gets the model_type of this ReferencedDataObject.
        The input Operation type.

        Allowed values for this property are: "PROCEDURE", "API", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The model_type of this ReferencedDataObject.
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """
        Sets the model_type of this ReferencedDataObject.
        The input Operation type.


        :param model_type: The model_type of this ReferencedDataObject.
        :type: str
        """
        allowed_values = ["PROCEDURE", "API"]
        if not value_allowed_none_or_none_sentinel(model_type, allowed_values):
            model_type = 'UNKNOWN_ENUM_VALUE'
        self._model_type = model_type

    @property
    def model_version(self):
        """
        Gets the model_version of this ReferencedDataObject.
        The object's model version.


        :return: The model_version of this ReferencedDataObject.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """
        Sets the model_version of this ReferencedDataObject.
        The object's model version.


        :param model_version: The model_version of this ReferencedDataObject.
        :type: str
        """
        self._model_version = model_version

    @property
    def parent_ref(self):
        """
        Gets the parent_ref of this ReferencedDataObject.

        :return: The parent_ref of this ReferencedDataObject.
        :rtype: oci.data_integration.models.ParentReference
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """
        Sets the parent_ref of this ReferencedDataObject.

        :param parent_ref: The parent_ref of this ReferencedDataObject.
        :type: oci.data_integration.models.ParentReference
        """
        self._parent_ref = parent_ref

    @property
    def name(self):
        """
        Gets the name of this ReferencedDataObject.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :return: The name of this ReferencedDataObject.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ReferencedDataObject.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :param name: The name of this ReferencedDataObject.
        :type: str
        """
        self._name = name

    @property
    def object_version(self):
        """
        Gets the object_version of this ReferencedDataObject.
        The version of the object that is used to track changes in the object instance.


        :return: The object_version of this ReferencedDataObject.
        :rtype: int
        """
        return self._object_version

    @object_version.setter
    def object_version(self, object_version):
        """
        Sets the object_version of this ReferencedDataObject.
        The version of the object that is used to track changes in the object instance.


        :param object_version: The object_version of this ReferencedDataObject.
        :type: int
        """
        self._object_version = object_version

    @property
    def resource_name(self):
        """
        Gets the resource_name of this ReferencedDataObject.
        The resource name.


        :return: The resource_name of this ReferencedDataObject.
        :rtype: str
        """
        return self._resource_name

    @resource_name.setter
    def resource_name(self, resource_name):
        """
        Sets the resource_name of this ReferencedDataObject.
        The resource name.


        :param resource_name: The resource_name of this ReferencedDataObject.
        :type: str
        """
        self._resource_name = resource_name

    @property
    def object_status(self):
        """
        Gets the object_status of this ReferencedDataObject.
        The status of an object that can be set to value 1 for shallow reference across objects, other values reserved.


        :return: The object_status of this ReferencedDataObject.
        :rtype: int
        """
        return self._object_status

    @object_status.setter
    def object_status(self, object_status):
        """
        Sets the object_status of this ReferencedDataObject.
        The status of an object that can be set to value 1 for shallow reference across objects, other values reserved.


        :param object_status: The object_status of this ReferencedDataObject.
        :type: int
        """
        self._object_status = object_status

    @property
    def external_key(self):
        """
        Gets the external_key of this ReferencedDataObject.
        The external key for the object.


        :return: The external_key of this ReferencedDataObject.
        :rtype: str
        """
        return self._external_key

    @external_key.setter
    def external_key(self, external_key):
        """
        Sets the external_key of this ReferencedDataObject.
        The external key for the object.


        :param external_key: The external_key of this ReferencedDataObject.
        :type: str
        """
        self._external_key = external_key

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
