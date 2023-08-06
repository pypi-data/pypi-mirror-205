# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyAuthenticationFactorsRemoverUser(object):
    """
    User for whom the authentication factors need to be deleted

    **SCIM++ Properties:**
    - caseExact: false
    - idcsSearchable: true
    - multiValued: false
    - mutability: readWrite
    - required: true
    - returned: default
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MyAuthenticationFactorsRemoverUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this MyAuthenticationFactorsRemoverUser.
        :type value: str

        :param ref:
            The value to assign to the ref property of this MyAuthenticationFactorsRemoverUser.
        :type ref: str

        :param display:
            The value to assign to the display property of this MyAuthenticationFactorsRemoverUser.
        :type display: str

        :param ocid:
            The value to assign to the ocid property of this MyAuthenticationFactorsRemoverUser.
        :type ocid: str

        """
        self.swagger_types = {
            'value': 'str',
            'ref': 'str',
            'display': 'str',
            'ocid': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'ref': '$ref',
            'display': 'display',
            'ocid': 'ocid'
        }

        self._value = None
        self._ref = None
        self._display = None
        self._ocid = None

    @property
    def value(self):
        """
        **[Required]** Gets the value of this MyAuthenticationFactorsRemoverUser.
        The identifier of the user

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :return: The value of this MyAuthenticationFactorsRemoverUser.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this MyAuthenticationFactorsRemoverUser.
        The identifier of the user

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :param value: The value of this MyAuthenticationFactorsRemoverUser.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this MyAuthenticationFactorsRemoverUser.
        The URI that corresponds to the member Resource for whom the factors will be deleted

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this MyAuthenticationFactorsRemoverUser.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this MyAuthenticationFactorsRemoverUser.
        The URI that corresponds to the member Resource for whom the factors will be deleted

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this MyAuthenticationFactorsRemoverUser.
        :type: str
        """
        self._ref = ref

    @property
    def display(self):
        """
        Gets the display of this MyAuthenticationFactorsRemoverUser.
        User display name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display of this MyAuthenticationFactorsRemoverUser.
        :rtype: str
        """
        return self._display

    @display.setter
    def display(self, display):
        """
        Sets the display of this MyAuthenticationFactorsRemoverUser.
        User display name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display: The display of this MyAuthenticationFactorsRemoverUser.
        :type: str
        """
        self._display = display

    @property
    def ocid(self):
        """
        Gets the ocid of this MyAuthenticationFactorsRemoverUser.
        The OCID of the user

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: always
         - type: string
         - uniqueness: none


        :return: The ocid of this MyAuthenticationFactorsRemoverUser.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this MyAuthenticationFactorsRemoverUser.
        The OCID of the user

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: always
         - type: string
         - uniqueness: none


        :param ocid: The ocid of this MyAuthenticationFactorsRemoverUser.
        :type: str
        """
        self._ocid = ocid

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
