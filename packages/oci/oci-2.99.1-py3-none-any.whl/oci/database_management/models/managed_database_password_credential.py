# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .managed_database_credential import ManagedDatabaseCredential
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ManagedDatabasePasswordCredential(ManagedDatabaseCredential):
    """
    User provides a password to be used to connect to the database.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ManagedDatabasePasswordCredential object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.ManagedDatabasePasswordCredential.credential_type` attribute
        of this class is ``PASSWORD`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param credential_type:
            The value to assign to the credential_type property of this ManagedDatabasePasswordCredential.
            Allowed values for this property are: "SECRET", "PASSWORD"
        :type credential_type: str

        :param username:
            The value to assign to the username property of this ManagedDatabasePasswordCredential.
        :type username: str

        :param role:
            The value to assign to the role property of this ManagedDatabasePasswordCredential.
            Allowed values for this property are: "NORMAL", "SYSDBA"
        :type role: str

        :param password:
            The value to assign to the password property of this ManagedDatabasePasswordCredential.
        :type password: str

        """
        self.swagger_types = {
            'credential_type': 'str',
            'username': 'str',
            'role': 'str',
            'password': 'str'
        }

        self.attribute_map = {
            'credential_type': 'credentialType',
            'username': 'username',
            'role': 'role',
            'password': 'password'
        }

        self._credential_type = None
        self._username = None
        self._role = None
        self._password = None
        self._credential_type = 'PASSWORD'

    @property
    def password(self):
        """
        **[Required]** Gets the password of this ManagedDatabasePasswordCredential.
        The database user's password encoded using BASE64 scheme.


        :return: The password of this ManagedDatabasePasswordCredential.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password of this ManagedDatabasePasswordCredential.
        The database user's password encoded using BASE64 scheme.


        :param password: The password of this ManagedDatabasePasswordCredential.
        :type: str
        """
        self._password = password

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
