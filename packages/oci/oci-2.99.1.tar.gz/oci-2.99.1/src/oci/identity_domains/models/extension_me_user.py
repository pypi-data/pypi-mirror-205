# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionMeUser(object):
    """
    OCI IAM self service schema extension
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionMeUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param current_password:
            The value to assign to the current_password property of this ExtensionMeUser.
        :type current_password: str

        """
        self.swagger_types = {
            'current_password': 'str'
        }

        self.attribute_map = {
            'current_password': 'currentPassword'
        }

        self._current_password = None

    @property
    def current_password(self):
        """
        Gets the current_password of this ExtensionMeUser.
        The current password is required if the user attempts to change the values of attributes that are used in recovering or verifying the user's own identity.  If the current password is specified, it will be used to authenticate the user regardless of any change in these attribute values

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsSensitive: hash
         - multiValued: false
         - mutability: writeOnly
         - required: false
         - returned: never
         - type: string
         - uniqueness: none


        :return: The current_password of this ExtensionMeUser.
        :rtype: str
        """
        return self._current_password

    @current_password.setter
    def current_password(self, current_password):
        """
        Sets the current_password of this ExtensionMeUser.
        The current password is required if the user attempts to change the values of attributes that are used in recovering or verifying the user's own identity.  If the current password is specified, it will be used to authenticate the user regardless of any change in these attribute values

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsSensitive: hash
         - multiValued: false
         - mutability: writeOnly
         - required: false
         - returned: never
         - type: string
         - uniqueness: none


        :param current_password: The current_password of this ExtensionMeUser.
        :type: str
        """
        self._current_password = current_password

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
