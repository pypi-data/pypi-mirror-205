# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .validate_database_tools_connection_result import ValidateDatabaseToolsConnectionResult
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ValidateDatabaseToolsConnectionOracleDatabaseResult(ValidateDatabaseToolsConnectionResult):
    """
    Connection validaton result for the Oracle Database.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ValidateDatabaseToolsConnectionOracleDatabaseResult object with values from keyword arguments. The default value of the :py:attr:`~oci.database_tools.models.ValidateDatabaseToolsConnectionOracleDatabaseResult.type` attribute
        of this class is ``ORACLE_DATABASE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
            Allowed values for this property are: "ORACLE_DATABASE", "MYSQL"
        :type type: str

        :param code:
            The value to assign to the code property of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :type code: str

        :param message:
            The value to assign to the message property of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :type message: str

        :param cause:
            The value to assign to the cause property of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :type cause: str

        :param action:
            The value to assign to the action property of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :type action: str

        :param database_name:
            The value to assign to the database_name property of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :type database_name: str

        :param database_version:
            The value to assign to the database_version property of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :type database_version: str

        """
        self.swagger_types = {
            'type': 'str',
            'code': 'str',
            'message': 'str',
            'cause': 'str',
            'action': 'str',
            'database_name': 'str',
            'database_version': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'code': 'code',
            'message': 'message',
            'cause': 'cause',
            'action': 'action',
            'database_name': 'databaseName',
            'database_version': 'databaseVersion'
        }

        self._type = None
        self._code = None
        self._message = None
        self._cause = None
        self._action = None
        self._database_name = None
        self._database_version = None
        self._type = 'ORACLE_DATABASE'

    @property
    def database_name(self):
        """
        Gets the database_name of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        The database name.


        :return: The database_name of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :rtype: str
        """
        return self._database_name

    @database_name.setter
    def database_name(self, database_name):
        """
        Sets the database_name of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        The database name.


        :param database_name: The database_name of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :type: str
        """
        self._database_name = database_name

    @property
    def database_version(self):
        """
        Gets the database_version of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        The database version.


        :return: The database_version of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :rtype: str
        """
        return self._database_version

    @database_version.setter
    def database_version(self, database_version):
        """
        Sets the database_version of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        The database version.


        :param database_version: The database_version of this ValidateDatabaseToolsConnectionOracleDatabaseResult.
        :type: str
        """
        self._database_version = database_version

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
