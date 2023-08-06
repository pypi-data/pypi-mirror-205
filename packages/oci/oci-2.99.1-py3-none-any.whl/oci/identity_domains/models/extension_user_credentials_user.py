# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionUserCredentialsUser(object):
    """
    User's credentials
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionUserCredentialsUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param db_credentials:
            The value to assign to the db_credentials property of this ExtensionUserCredentialsUser.
        :type db_credentials: list[oci.identity_domains.models.UserExtDbCredentials]

        :param customer_secret_keys:
            The value to assign to the customer_secret_keys property of this ExtensionUserCredentialsUser.
        :type customer_secret_keys: list[oci.identity_domains.models.UserExtCustomerSecretKeys]

        :param auth_tokens:
            The value to assign to the auth_tokens property of this ExtensionUserCredentialsUser.
        :type auth_tokens: list[oci.identity_domains.models.UserExtAuthTokens]

        :param smtp_credentials:
            The value to assign to the smtp_credentials property of this ExtensionUserCredentialsUser.
        :type smtp_credentials: list[oci.identity_domains.models.UserExtSmtpCredentials]

        :param api_keys:
            The value to assign to the api_keys property of this ExtensionUserCredentialsUser.
        :type api_keys: list[oci.identity_domains.models.UserExtApiKeys]

        :param o_auth2_client_credentials:
            The value to assign to the o_auth2_client_credentials property of this ExtensionUserCredentialsUser.
        :type o_auth2_client_credentials: list[oci.identity_domains.models.UserExtOAuth2ClientCredentials]

        """
        self.swagger_types = {
            'db_credentials': 'list[UserExtDbCredentials]',
            'customer_secret_keys': 'list[UserExtCustomerSecretKeys]',
            'auth_tokens': 'list[UserExtAuthTokens]',
            'smtp_credentials': 'list[UserExtSmtpCredentials]',
            'api_keys': 'list[UserExtApiKeys]',
            'o_auth2_client_credentials': 'list[UserExtOAuth2ClientCredentials]'
        }

        self.attribute_map = {
            'db_credentials': 'dbCredentials',
            'customer_secret_keys': 'customerSecretKeys',
            'auth_tokens': 'authTokens',
            'smtp_credentials': 'smtpCredentials',
            'api_keys': 'apiKeys',
            'o_auth2_client_credentials': 'oAuth2ClientCredentials'
        }

        self._db_credentials = None
        self._customer_secret_keys = None
        self._auth_tokens = None
        self._smtp_credentials = None
        self._api_keys = None
        self._o_auth2_client_credentials = None

    @property
    def db_credentials(self):
        """
        Gets the db_credentials of this ExtensionUserCredentialsUser.
        A list of db credentials corresponding to user.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The db_credentials of this ExtensionUserCredentialsUser.
        :rtype: list[oci.identity_domains.models.UserExtDbCredentials]
        """
        return self._db_credentials

    @db_credentials.setter
    def db_credentials(self, db_credentials):
        """
        Sets the db_credentials of this ExtensionUserCredentialsUser.
        A list of db credentials corresponding to user.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param db_credentials: The db_credentials of this ExtensionUserCredentialsUser.
        :type: list[oci.identity_domains.models.UserExtDbCredentials]
        """
        self._db_credentials = db_credentials

    @property
    def customer_secret_keys(self):
        """
        Gets the customer_secret_keys of this ExtensionUserCredentialsUser.
        A list of customer secret keys corresponding to user.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The customer_secret_keys of this ExtensionUserCredentialsUser.
        :rtype: list[oci.identity_domains.models.UserExtCustomerSecretKeys]
        """
        return self._customer_secret_keys

    @customer_secret_keys.setter
    def customer_secret_keys(self, customer_secret_keys):
        """
        Sets the customer_secret_keys of this ExtensionUserCredentialsUser.
        A list of customer secret keys corresponding to user.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param customer_secret_keys: The customer_secret_keys of this ExtensionUserCredentialsUser.
        :type: list[oci.identity_domains.models.UserExtCustomerSecretKeys]
        """
        self._customer_secret_keys = customer_secret_keys

    @property
    def auth_tokens(self):
        """
        Gets the auth_tokens of this ExtensionUserCredentialsUser.
        A list of auth tokens corresponding to user.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The auth_tokens of this ExtensionUserCredentialsUser.
        :rtype: list[oci.identity_domains.models.UserExtAuthTokens]
        """
        return self._auth_tokens

    @auth_tokens.setter
    def auth_tokens(self, auth_tokens):
        """
        Sets the auth_tokens of this ExtensionUserCredentialsUser.
        A list of auth tokens corresponding to user.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param auth_tokens: The auth_tokens of this ExtensionUserCredentialsUser.
        :type: list[oci.identity_domains.models.UserExtAuthTokens]
        """
        self._auth_tokens = auth_tokens

    @property
    def smtp_credentials(self):
        """
        Gets the smtp_credentials of this ExtensionUserCredentialsUser.
        A list of smtp credentials corresponding to user.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The smtp_credentials of this ExtensionUserCredentialsUser.
        :rtype: list[oci.identity_domains.models.UserExtSmtpCredentials]
        """
        return self._smtp_credentials

    @smtp_credentials.setter
    def smtp_credentials(self, smtp_credentials):
        """
        Sets the smtp_credentials of this ExtensionUserCredentialsUser.
        A list of smtp credentials corresponding to user.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param smtp_credentials: The smtp_credentials of this ExtensionUserCredentialsUser.
        :type: list[oci.identity_domains.models.UserExtSmtpCredentials]
        """
        self._smtp_credentials = smtp_credentials

    @property
    def api_keys(self):
        """
        Gets the api_keys of this ExtensionUserCredentialsUser.
        A list of api keys corresponding to user.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The api_keys of this ExtensionUserCredentialsUser.
        :rtype: list[oci.identity_domains.models.UserExtApiKeys]
        """
        return self._api_keys

    @api_keys.setter
    def api_keys(self, api_keys):
        """
        Sets the api_keys of this ExtensionUserCredentialsUser.
        A list of api keys corresponding to user.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param api_keys: The api_keys of this ExtensionUserCredentialsUser.
        :type: list[oci.identity_domains.models.UserExtApiKeys]
        """
        self._api_keys = api_keys

    @property
    def o_auth2_client_credentials(self):
        """
        Gets the o_auth2_client_credentials of this ExtensionUserCredentialsUser.
        A list of oauth2 client credentials corresponding to user.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The o_auth2_client_credentials of this ExtensionUserCredentialsUser.
        :rtype: list[oci.identity_domains.models.UserExtOAuth2ClientCredentials]
        """
        return self._o_auth2_client_credentials

    @o_auth2_client_credentials.setter
    def o_auth2_client_credentials(self, o_auth2_client_credentials):
        """
        Sets the o_auth2_client_credentials of this ExtensionUserCredentialsUser.
        A list of oauth2 client credentials corresponding to user.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param o_auth2_client_credentials: The o_auth2_client_credentials of this ExtensionUserCredentialsUser.
        :type: list[oci.identity_domains.models.UserExtOAuth2ClientCredentials]
        """
        self._o_auth2_client_credentials = o_auth2_client_credentials

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
