# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SensitiveObjectSummary(object):
    """
    Summary of a sensitive object present in a sensitive data model.
    """

    #: A constant which can be used with the object_type property of a SensitiveObjectSummary.
    #: This constant has a value of "TABLE"
    OBJECT_TYPE_TABLE = "TABLE"

    #: A constant which can be used with the object_type property of a SensitiveObjectSummary.
    #: This constant has a value of "EDITIONING_VIEW"
    OBJECT_TYPE_EDITIONING_VIEW = "EDITIONING_VIEW"

    def __init__(self, **kwargs):
        """
        Initializes a new SensitiveObjectSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param schema_name:
            The value to assign to the schema_name property of this SensitiveObjectSummary.
        :type schema_name: str

        :param object_name:
            The value to assign to the object_name property of this SensitiveObjectSummary.
        :type object_name: str

        :param object_type:
            The value to assign to the object_type property of this SensitiveObjectSummary.
            Allowed values for this property are: "TABLE", "EDITIONING_VIEW", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type object_type: str

        """
        self.swagger_types = {
            'schema_name': 'str',
            'object_name': 'str',
            'object_type': 'str'
        }

        self.attribute_map = {
            'schema_name': 'schemaName',
            'object_name': 'objectName',
            'object_type': 'objectType'
        }

        self._schema_name = None
        self._object_name = None
        self._object_type = None

    @property
    def schema_name(self):
        """
        **[Required]** Gets the schema_name of this SensitiveObjectSummary.
        The database schema that contains the sensitive column.


        :return: The schema_name of this SensitiveObjectSummary.
        :rtype: str
        """
        return self._schema_name

    @schema_name.setter
    def schema_name(self, schema_name):
        """
        Sets the schema_name of this SensitiveObjectSummary.
        The database schema that contains the sensitive column.


        :param schema_name: The schema_name of this SensitiveObjectSummary.
        :type: str
        """
        self._schema_name = schema_name

    @property
    def object_name(self):
        """
        **[Required]** Gets the object_name of this SensitiveObjectSummary.
        The database object that contains the sensitive column.


        :return: The object_name of this SensitiveObjectSummary.
        :rtype: str
        """
        return self._object_name

    @object_name.setter
    def object_name(self, object_name):
        """
        Sets the object_name of this SensitiveObjectSummary.
        The database object that contains the sensitive column.


        :param object_name: The object_name of this SensitiveObjectSummary.
        :type: str
        """
        self._object_name = object_name

    @property
    def object_type(self):
        """
        **[Required]** Gets the object_type of this SensitiveObjectSummary.
        The type of the database object that contains the sensitive column.

        Allowed values for this property are: "TABLE", "EDITIONING_VIEW", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The object_type of this SensitiveObjectSummary.
        :rtype: str
        """
        return self._object_type

    @object_type.setter
    def object_type(self, object_type):
        """
        Sets the object_type of this SensitiveObjectSummary.
        The type of the database object that contains the sensitive column.


        :param object_type: The object_type of this SensitiveObjectSummary.
        :type: str
        """
        allowed_values = ["TABLE", "EDITIONING_VIEW"]
        if not value_allowed_none_or_none_sentinel(object_type, allowed_values):
            object_type = 'UNKNOWN_ENUM_VALUE'
        self._object_type = object_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
