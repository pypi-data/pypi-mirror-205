# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionKerberosUserUser(object):
    """
    Kerberos User extension
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionKerberosUserUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param realm_users:
            The value to assign to the realm_users property of this ExtensionKerberosUserUser.
        :type realm_users: list[oci.identity_domains.models.UserExtRealmUsers]

        """
        self.swagger_types = {
            'realm_users': 'list[UserExtRealmUsers]'
        }

        self.attribute_map = {
            'realm_users': 'realmUsers'
        }

        self._realm_users = None

    @property
    def realm_users(self):
        """
        Gets the realm_users of this ExtensionKerberosUserUser.
        A list of kerberos realm users for an OCI IAM User

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The realm_users of this ExtensionKerberosUserUser.
        :rtype: list[oci.identity_domains.models.UserExtRealmUsers]
        """
        return self._realm_users

    @realm_users.setter
    def realm_users(self, realm_users):
        """
        Sets the realm_users of this ExtensionKerberosUserUser.
        A list of kerberos realm users for an OCI IAM User

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param realm_users: The realm_users of this ExtensionKerberosUserUser.
        :type: list[oci.identity_domains.models.UserExtRealmUsers]
        """
        self._realm_users = realm_users

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
