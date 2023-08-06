# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionCapabilitiesUser(object):
    """
    User's Capabilities
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionCapabilitiesUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param can_use_api_keys:
            The value to assign to the can_use_api_keys property of this ExtensionCapabilitiesUser.
        :type can_use_api_keys: bool

        :param can_use_auth_tokens:
            The value to assign to the can_use_auth_tokens property of this ExtensionCapabilitiesUser.
        :type can_use_auth_tokens: bool

        :param can_use_console_password:
            The value to assign to the can_use_console_password property of this ExtensionCapabilitiesUser.
        :type can_use_console_password: bool

        :param can_use_customer_secret_keys:
            The value to assign to the can_use_customer_secret_keys property of this ExtensionCapabilitiesUser.
        :type can_use_customer_secret_keys: bool

        :param can_use_o_auth2_client_credentials:
            The value to assign to the can_use_o_auth2_client_credentials property of this ExtensionCapabilitiesUser.
        :type can_use_o_auth2_client_credentials: bool

        :param can_use_smtp_credentials:
            The value to assign to the can_use_smtp_credentials property of this ExtensionCapabilitiesUser.
        :type can_use_smtp_credentials: bool

        :param can_use_db_credentials:
            The value to assign to the can_use_db_credentials property of this ExtensionCapabilitiesUser.
        :type can_use_db_credentials: bool

        """
        self.swagger_types = {
            'can_use_api_keys': 'bool',
            'can_use_auth_tokens': 'bool',
            'can_use_console_password': 'bool',
            'can_use_customer_secret_keys': 'bool',
            'can_use_o_auth2_client_credentials': 'bool',
            'can_use_smtp_credentials': 'bool',
            'can_use_db_credentials': 'bool'
        }

        self.attribute_map = {
            'can_use_api_keys': 'canUseApiKeys',
            'can_use_auth_tokens': 'canUseAuthTokens',
            'can_use_console_password': 'canUseConsolePassword',
            'can_use_customer_secret_keys': 'canUseCustomerSecretKeys',
            'can_use_o_auth2_client_credentials': 'canUseOAuth2ClientCredentials',
            'can_use_smtp_credentials': 'canUseSmtpCredentials',
            'can_use_db_credentials': 'canUseDbCredentials'
        }

        self._can_use_api_keys = None
        self._can_use_auth_tokens = None
        self._can_use_console_password = None
        self._can_use_customer_secret_keys = None
        self._can_use_o_auth2_client_credentials = None
        self._can_use_smtp_credentials = None
        self._can_use_db_credentials = None

    @property
    def can_use_api_keys(self):
        """
        Gets the can_use_api_keys of this ExtensionCapabilitiesUser.
        Indicates weather a user can use api keys

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_api_keys of this ExtensionCapabilitiesUser.
        :rtype: bool
        """
        return self._can_use_api_keys

    @can_use_api_keys.setter
    def can_use_api_keys(self, can_use_api_keys):
        """
        Sets the can_use_api_keys of this ExtensionCapabilitiesUser.
        Indicates weather a user can use api keys

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_api_keys: The can_use_api_keys of this ExtensionCapabilitiesUser.
        :type: bool
        """
        self._can_use_api_keys = can_use_api_keys

    @property
    def can_use_auth_tokens(self):
        """
        Gets the can_use_auth_tokens of this ExtensionCapabilitiesUser.
        Indicates weather a user can use auth tokens

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_auth_tokens of this ExtensionCapabilitiesUser.
        :rtype: bool
        """
        return self._can_use_auth_tokens

    @can_use_auth_tokens.setter
    def can_use_auth_tokens(self, can_use_auth_tokens):
        """
        Sets the can_use_auth_tokens of this ExtensionCapabilitiesUser.
        Indicates weather a user can use auth tokens

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_auth_tokens: The can_use_auth_tokens of this ExtensionCapabilitiesUser.
        :type: bool
        """
        self._can_use_auth_tokens = can_use_auth_tokens

    @property
    def can_use_console_password(self):
        """
        Gets the can_use_console_password of this ExtensionCapabilitiesUser.
        Indicates weather a user can use console password

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_console_password of this ExtensionCapabilitiesUser.
        :rtype: bool
        """
        return self._can_use_console_password

    @can_use_console_password.setter
    def can_use_console_password(self, can_use_console_password):
        """
        Sets the can_use_console_password of this ExtensionCapabilitiesUser.
        Indicates weather a user can use console password

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_console_password: The can_use_console_password of this ExtensionCapabilitiesUser.
        :type: bool
        """
        self._can_use_console_password = can_use_console_password

    @property
    def can_use_customer_secret_keys(self):
        """
        Gets the can_use_customer_secret_keys of this ExtensionCapabilitiesUser.
        Indicates weather a user can use customer secret keys

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_customer_secret_keys of this ExtensionCapabilitiesUser.
        :rtype: bool
        """
        return self._can_use_customer_secret_keys

    @can_use_customer_secret_keys.setter
    def can_use_customer_secret_keys(self, can_use_customer_secret_keys):
        """
        Sets the can_use_customer_secret_keys of this ExtensionCapabilitiesUser.
        Indicates weather a user can use customer secret keys

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_customer_secret_keys: The can_use_customer_secret_keys of this ExtensionCapabilitiesUser.
        :type: bool
        """
        self._can_use_customer_secret_keys = can_use_customer_secret_keys

    @property
    def can_use_o_auth2_client_credentials(self):
        """
        Gets the can_use_o_auth2_client_credentials of this ExtensionCapabilitiesUser.
        Indicates weather a user can use oauth2 client credentials

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_o_auth2_client_credentials of this ExtensionCapabilitiesUser.
        :rtype: bool
        """
        return self._can_use_o_auth2_client_credentials

    @can_use_o_auth2_client_credentials.setter
    def can_use_o_auth2_client_credentials(self, can_use_o_auth2_client_credentials):
        """
        Sets the can_use_o_auth2_client_credentials of this ExtensionCapabilitiesUser.
        Indicates weather a user can use oauth2 client credentials

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_o_auth2_client_credentials: The can_use_o_auth2_client_credentials of this ExtensionCapabilitiesUser.
        :type: bool
        """
        self._can_use_o_auth2_client_credentials = can_use_o_auth2_client_credentials

    @property
    def can_use_smtp_credentials(self):
        """
        Gets the can_use_smtp_credentials of this ExtensionCapabilitiesUser.
        Indicates weather a user can use smtp credentials

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_smtp_credentials of this ExtensionCapabilitiesUser.
        :rtype: bool
        """
        return self._can_use_smtp_credentials

    @can_use_smtp_credentials.setter
    def can_use_smtp_credentials(self, can_use_smtp_credentials):
        """
        Sets the can_use_smtp_credentials of this ExtensionCapabilitiesUser.
        Indicates weather a user can use smtp credentials

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_smtp_credentials: The can_use_smtp_credentials of this ExtensionCapabilitiesUser.
        :type: bool
        """
        self._can_use_smtp_credentials = can_use_smtp_credentials

    @property
    def can_use_db_credentials(self):
        """
        Gets the can_use_db_credentials of this ExtensionCapabilitiesUser.
        Indicates weather a user can use db credentials

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_db_credentials of this ExtensionCapabilitiesUser.
        :rtype: bool
        """
        return self._can_use_db_credentials

    @can_use_db_credentials.setter
    def can_use_db_credentials(self, can_use_db_credentials):
        """
        Sets the can_use_db_credentials of this ExtensionCapabilitiesUser.
        Indicates weather a user can use db credentials

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_db_credentials: The can_use_db_credentials of this ExtensionCapabilitiesUser.
        :type: bool
        """
        self._can_use_db_credentials = can_use_db_credentials

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
