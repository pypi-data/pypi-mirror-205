# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserPhoneNumbers(object):
    """
    Phone numbers
    """

    #: A constant which can be used with the type property of a UserPhoneNumbers.
    #: This constant has a value of "work"
    TYPE_WORK = "work"

    #: A constant which can be used with the type property of a UserPhoneNumbers.
    #: This constant has a value of "home"
    TYPE_HOME = "home"

    #: A constant which can be used with the type property of a UserPhoneNumbers.
    #: This constant has a value of "mobile"
    TYPE_MOBILE = "mobile"

    #: A constant which can be used with the type property of a UserPhoneNumbers.
    #: This constant has a value of "fax"
    TYPE_FAX = "fax"

    #: A constant which can be used with the type property of a UserPhoneNumbers.
    #: This constant has a value of "pager"
    TYPE_PAGER = "pager"

    #: A constant which can be used with the type property of a UserPhoneNumbers.
    #: This constant has a value of "other"
    TYPE_OTHER = "other"

    #: A constant which can be used with the type property of a UserPhoneNumbers.
    #: This constant has a value of "recovery"
    TYPE_RECOVERY = "recovery"

    def __init__(self, **kwargs):
        """
        Initializes a new UserPhoneNumbers object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this UserPhoneNumbers.
        :type value: str

        :param display:
            The value to assign to the display property of this UserPhoneNumbers.
        :type display: str

        :param type:
            The value to assign to the type property of this UserPhoneNumbers.
            Allowed values for this property are: "work", "home", "mobile", "fax", "pager", "other", "recovery", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param primary:
            The value to assign to the primary property of this UserPhoneNumbers.
        :type primary: bool

        :param verified:
            The value to assign to the verified property of this UserPhoneNumbers.
        :type verified: bool

        """
        self.swagger_types = {
            'value': 'str',
            'display': 'str',
            'type': 'str',
            'primary': 'bool',
            'verified': 'bool'
        }

        self.attribute_map = {
            'value': 'value',
            'display': 'display',
            'type': 'type',
            'primary': 'primary',
            'verified': 'verified'
        }

        self._value = None
        self._display = None
        self._type = None
        self._primary = None
        self._verified = None

    @property
    def value(self):
        """
        **[Required]** Gets the value of this UserPhoneNumbers.
        User's phone number

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this UserPhoneNumbers.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this UserPhoneNumbers.
        User's phone number

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this UserPhoneNumbers.
        :type: str
        """
        self._value = value

    @property
    def display(self):
        """
        Gets the display of this UserPhoneNumbers.
        A human-readable name, primarily used for display purposes. READ ONLY

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display of this UserPhoneNumbers.
        :rtype: str
        """
        return self._display

    @display.setter
    def display(self, display):
        """
        Sets the display of this UserPhoneNumbers.
        A human-readable name, primarily used for display purposes. READ ONLY

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display: The display of this UserPhoneNumbers.
        :type: str
        """
        self._display = display

    @property
    def type(self):
        """
        **[Required]** Gets the type of this UserPhoneNumbers.
        A label that indicates the attribute's function- for example, 'work', 'home', or 'mobile'

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "work", "home", "mobile", "fax", "pager", "other", "recovery", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this UserPhoneNumbers.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this UserPhoneNumbers.
        A label that indicates the attribute's function- for example, 'work', 'home', or 'mobile'

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param type: The type of this UserPhoneNumbers.
        :type: str
        """
        allowed_values = ["work", "home", "mobile", "fax", "pager", "other", "recovery"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def primary(self):
        """
        Gets the primary of this UserPhoneNumbers.
        A Boolean value that indicates the 'primary' or preferred attribute value for this attribute--for example, the preferred phone number or primary phone number. The primary attribute value 'true' MUST appear no more than once.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The primary of this UserPhoneNumbers.
        :rtype: bool
        """
        return self._primary

    @primary.setter
    def primary(self, primary):
        """
        Sets the primary of this UserPhoneNumbers.
        A Boolean value that indicates the 'primary' or preferred attribute value for this attribute--for example, the preferred phone number or primary phone number. The primary attribute value 'true' MUST appear no more than once.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param primary: The primary of this UserPhoneNumbers.
        :type: bool
        """
        self._primary = primary

    @property
    def verified(self):
        """
        Gets the verified of this UserPhoneNumbers.
        A Boolean value that indicates if the phone number is verified.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The verified of this UserPhoneNumbers.
        :rtype: bool
        """
        return self._verified

    @verified.setter
    def verified(self, verified):
        """
        Sets the verified of this UserPhoneNumbers.
        A Boolean value that indicates if the phone number is verified.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param verified: The verified of this UserPhoneNumbers.
        :type: bool
        """
        self._verified = verified

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
