# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionSocialAccountUser(object):
    """
    Social User extension
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionSocialAccountUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param social_accounts:
            The value to assign to the social_accounts property of this ExtensionSocialAccountUser.
        :type social_accounts: list[oci.identity_domains.models.UserExtSocialAccounts]

        """
        self.swagger_types = {
            'social_accounts': 'list[UserExtSocialAccounts]'
        }

        self.attribute_map = {
            'social_accounts': 'socialAccounts'
        }

        self._social_accounts = None

    @property
    def social_accounts(self):
        """
        Gets the social_accounts of this ExtensionSocialAccountUser.
        Description:

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - idcsPii: true
         - type: complex
         - uniqueness: none


        :return: The social_accounts of this ExtensionSocialAccountUser.
        :rtype: list[oci.identity_domains.models.UserExtSocialAccounts]
        """
        return self._social_accounts

    @social_accounts.setter
    def social_accounts(self, social_accounts):
        """
        Sets the social_accounts of this ExtensionSocialAccountUser.
        Description:

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - idcsPii: true
         - type: complex
         - uniqueness: none


        :param social_accounts: The social_accounts of this ExtensionSocialAccountUser.
        :type: list[oci.identity_domains.models.UserExtSocialAccounts]
        """
        self._social_accounts = social_accounts

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
