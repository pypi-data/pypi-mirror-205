# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TableSummary(object):
    """
    Details of a table fetched from the database.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new TableSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param table_name:
            The value to assign to the table_name property of this TableSummary.
        :type table_name: str

        :param schema_name:
            The value to assign to the schema_name property of this TableSummary.
        :type schema_name: str

        """
        self.swagger_types = {
            'table_name': 'str',
            'schema_name': 'str'
        }

        self.attribute_map = {
            'table_name': 'tableName',
            'schema_name': 'schemaName'
        }

        self._table_name = None
        self._schema_name = None

    @property
    def table_name(self):
        """
        **[Required]** Gets the table_name of this TableSummary.
        Name of the table.


        :return: The table_name of this TableSummary.
        :rtype: str
        """
        return self._table_name

    @table_name.setter
    def table_name(self, table_name):
        """
        Sets the table_name of this TableSummary.
        Name of the table.


        :param table_name: The table_name of this TableSummary.
        :type: str
        """
        self._table_name = table_name

    @property
    def schema_name(self):
        """
        **[Required]** Gets the schema_name of this TableSummary.
        Name of the schema.


        :return: The schema_name of this TableSummary.
        :rtype: str
        """
        return self._schema_name

    @schema_name.setter
    def schema_name(self, schema_name):
        """
        Sets the schema_name of this TableSummary.
        Name of the schema.


        :param schema_name: The schema_name of this TableSummary.
        :type: str
        """
        self._schema_name = schema_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
