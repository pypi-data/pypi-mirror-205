# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserExtRealmUsers(object):
    """
    A list of kerberos realm users for an OCI IAM User

    **SCIM++ Properties:**
    - idcsCompositeKey: [value]
    - multiValued: true
    - mutability: readWrite
    - required: false
    - returned: request
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UserExtRealmUsers object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this UserExtRealmUsers.
        :type value: str

        :param ref:
            The value to assign to the ref property of this UserExtRealmUsers.
        :type ref: str

        :param principal_name:
            The value to assign to the principal_name property of this UserExtRealmUsers.
        :type principal_name: str

        :param realm_name:
            The value to assign to the realm_name property of this UserExtRealmUsers.
        :type realm_name: str

        """
        self.swagger_types = {
            'value': 'str',
            'ref': 'str',
            'principal_name': 'str',
            'realm_name': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'ref': '$ref',
            'principal_name': 'principalName',
            'realm_name': 'realmName'
        }

        self._value = None
        self._ref = None
        self._principal_name = None
        self._realm_name = None

    @property
    def value(self):
        """
        **[Required]** Gets the value of this UserExtRealmUsers.
        id of the KerberosRealmUser associated with the OCI IAM User.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this UserExtRealmUsers.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this UserExtRealmUsers.
        id of the KerberosRealmUser associated with the OCI IAM User.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this UserExtRealmUsers.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this UserExtRealmUsers.
        The URI of the corresponding KerberosRealmUser resource associated with the OCI IAM User.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this UserExtRealmUsers.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this UserExtRealmUsers.
        The URI of the corresponding KerberosRealmUser resource associated with the OCI IAM User.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this UserExtRealmUsers.
        :type: str
        """
        self._ref = ref

    @property
    def principal_name(self):
        """
        Gets the principal_name of this UserExtRealmUsers.
        Principal Name of the KerberosRealmUser associated with the OCI IAM User.

        **SCIM++ Properties:**
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The principal_name of this UserExtRealmUsers.
        :rtype: str
        """
        return self._principal_name

    @principal_name.setter
    def principal_name(self, principal_name):
        """
        Sets the principal_name of this UserExtRealmUsers.
        Principal Name of the KerberosRealmUser associated with the OCI IAM User.

        **SCIM++ Properties:**
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param principal_name: The principal_name of this UserExtRealmUsers.
        :type: str
        """
        self._principal_name = principal_name

    @property
    def realm_name(self):
        """
        Gets the realm_name of this UserExtRealmUsers.
        Realm Name for the KerberosRealmUser associated with the OCI IAM User.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The realm_name of this UserExtRealmUsers.
        :rtype: str
        """
        return self._realm_name

    @realm_name.setter
    def realm_name(self, realm_name):
        """
        Sets the realm_name of this UserExtRealmUsers.
        Realm Name for the KerberosRealmUser associated with the OCI IAM User.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param realm_name: The realm_name of this UserExtRealmUsers.
        :type: str
        """
        self._realm_name = realm_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
