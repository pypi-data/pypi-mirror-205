# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .asm_connection_credentials import AsmConnectionCredentials
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AsmConnectionCredentialsByDetails(AsmConnectionCredentials):
    """
    The credentials used to connect to the ASM instance.
    """

    #: A constant which can be used with the role property of a AsmConnectionCredentialsByDetails.
    #: This constant has a value of "SYSASM"
    ROLE_SYSASM = "SYSASM"

    #: A constant which can be used with the role property of a AsmConnectionCredentialsByDetails.
    #: This constant has a value of "SYSDBA"
    ROLE_SYSDBA = "SYSDBA"

    #: A constant which can be used with the role property of a AsmConnectionCredentialsByDetails.
    #: This constant has a value of "SYSOPER"
    ROLE_SYSOPER = "SYSOPER"

    def __init__(self, **kwargs):
        """
        Initializes a new AsmConnectionCredentialsByDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.AsmConnectionCredentialsByDetails.credential_type` attribute
        of this class is ``DETAILS`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param credential_type:
            The value to assign to the credential_type property of this AsmConnectionCredentialsByDetails.
            Allowed values for this property are: "NAME_REFERENCE", "DETAILS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type credential_type: str

        :param credential_name:
            The value to assign to the credential_name property of this AsmConnectionCredentialsByDetails.
        :type credential_name: str

        :param user_name:
            The value to assign to the user_name property of this AsmConnectionCredentialsByDetails.
        :type user_name: str

        :param password_secret_id:
            The value to assign to the password_secret_id property of this AsmConnectionCredentialsByDetails.
        :type password_secret_id: str

        :param role:
            The value to assign to the role property of this AsmConnectionCredentialsByDetails.
            Allowed values for this property are: "SYSASM", "SYSDBA", "SYSOPER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type role: str

        """
        self.swagger_types = {
            'credential_type': 'str',
            'credential_name': 'str',
            'user_name': 'str',
            'password_secret_id': 'str',
            'role': 'str'
        }

        self.attribute_map = {
            'credential_type': 'credentialType',
            'credential_name': 'credentialName',
            'user_name': 'userName',
            'password_secret_id': 'passwordSecretId',
            'role': 'role'
        }

        self._credential_type = None
        self._credential_name = None
        self._user_name = None
        self._password_secret_id = None
        self._role = None
        self._credential_type = 'DETAILS'

    @property
    def credential_name(self):
        """
        Gets the credential_name of this AsmConnectionCredentialsByDetails.
        The name of the credential information that used to connect to the DB system resource.
        The name should be in \"x.y\" format, where the length of \"x\" has a maximum of 64 characters,
        and length of \"y\" has a maximum of 199 characters. The name strings can contain letters,
        numbers and the underscore character only. Other characters are not valid, except for
        the \".\" character that separates the \"x\" and \"y\" portions of the name.
        *IMPORTANT* - The name must be unique within the OCI region the credential is being created in.
        If you specify a name that duplicates the name of another credential within the same OCI region,
        you may overwrite or corrupt the credential that is already using the name.

        For example: inventorydb.abc112233445566778899


        :return: The credential_name of this AsmConnectionCredentialsByDetails.
        :rtype: str
        """
        return self._credential_name

    @credential_name.setter
    def credential_name(self, credential_name):
        """
        Sets the credential_name of this AsmConnectionCredentialsByDetails.
        The name of the credential information that used to connect to the DB system resource.
        The name should be in \"x.y\" format, where the length of \"x\" has a maximum of 64 characters,
        and length of \"y\" has a maximum of 199 characters. The name strings can contain letters,
        numbers and the underscore character only. Other characters are not valid, except for
        the \".\" character that separates the \"x\" and \"y\" portions of the name.
        *IMPORTANT* - The name must be unique within the OCI region the credential is being created in.
        If you specify a name that duplicates the name of another credential within the same OCI region,
        you may overwrite or corrupt the credential that is already using the name.

        For example: inventorydb.abc112233445566778899


        :param credential_name: The credential_name of this AsmConnectionCredentialsByDetails.
        :type: str
        """
        self._credential_name = credential_name

    @property
    def user_name(self):
        """
        **[Required]** Gets the user_name of this AsmConnectionCredentialsByDetails.
        The user name used to connect to the ASM instance.


        :return: The user_name of this AsmConnectionCredentialsByDetails.
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """
        Sets the user_name of this AsmConnectionCredentialsByDetails.
        The user name used to connect to the ASM instance.


        :param user_name: The user_name of this AsmConnectionCredentialsByDetails.
        :type: str
        """
        self._user_name = user_name

    @property
    def password_secret_id(self):
        """
        **[Required]** Gets the password_secret_id of this AsmConnectionCredentialsByDetails.
        The `OCID`__ of the secret containing the user password.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The password_secret_id of this AsmConnectionCredentialsByDetails.
        :rtype: str
        """
        return self._password_secret_id

    @password_secret_id.setter
    def password_secret_id(self, password_secret_id):
        """
        Sets the password_secret_id of this AsmConnectionCredentialsByDetails.
        The `OCID`__ of the secret containing the user password.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param password_secret_id: The password_secret_id of this AsmConnectionCredentialsByDetails.
        :type: str
        """
        self._password_secret_id = password_secret_id

    @property
    def role(self):
        """
        **[Required]** Gets the role of this AsmConnectionCredentialsByDetails.
        The role of the user connecting to the ASM instance.

        Allowed values for this property are: "SYSASM", "SYSDBA", "SYSOPER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The role of this AsmConnectionCredentialsByDetails.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the role of this AsmConnectionCredentialsByDetails.
        The role of the user connecting to the ASM instance.


        :param role: The role of this AsmConnectionCredentialsByDetails.
        :type: str
        """
        allowed_values = ["SYSASM", "SYSDBA", "SYSOPER"]
        if not value_allowed_none_or_none_sentinel(role, allowed_values):
            role = 'UNKNOWN_ENUM_VALUE'
        self._role = role

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
