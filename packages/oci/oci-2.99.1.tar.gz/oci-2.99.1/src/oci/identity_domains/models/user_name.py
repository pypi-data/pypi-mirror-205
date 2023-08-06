# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserName(object):
    """
    A complex attribute that contains attributes representing the name

    **SCIM++ Properties:**
    - idcsCsvAttributeNameMappings: [[columnHeaderName:Formatted Name, mapsTo:name.formatted], [columnHeaderName:Honorific Prefix, mapsTo:name.honorificPrefix], [columnHeaderName:First Name, mapsTo:name.givenName], [columnHeaderName:Middle Name, mapsTo:name.middleName], [columnHeaderName:Last Name, mapsTo:name.familyName], [columnHeaderName:Honorific Suffix, mapsTo:name.honorificSuffix]]
    - idcsPii: true
    - multiValued: false
    - mutability: readWrite
    - required: true
    - returned: default
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UserName object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param formatted:
            The value to assign to the formatted property of this UserName.
        :type formatted: str

        :param family_name:
            The value to assign to the family_name property of this UserName.
        :type family_name: str

        :param given_name:
            The value to assign to the given_name property of this UserName.
        :type given_name: str

        :param middle_name:
            The value to assign to the middle_name property of this UserName.
        :type middle_name: str

        :param honorific_prefix:
            The value to assign to the honorific_prefix property of this UserName.
        :type honorific_prefix: str

        :param honorific_suffix:
            The value to assign to the honorific_suffix property of this UserName.
        :type honorific_suffix: str

        """
        self.swagger_types = {
            'formatted': 'str',
            'family_name': 'str',
            'given_name': 'str',
            'middle_name': 'str',
            'honorific_prefix': 'str',
            'honorific_suffix': 'str'
        }

        self.attribute_map = {
            'formatted': 'formatted',
            'family_name': 'familyName',
            'given_name': 'givenName',
            'middle_name': 'middleName',
            'honorific_prefix': 'honorificPrefix',
            'honorific_suffix': 'honorificSuffix'
        }

        self._formatted = None
        self._family_name = None
        self._given_name = None
        self._middle_name = None
        self._honorific_prefix = None
        self._honorific_suffix = None

    @property
    def formatted(self):
        """
        Gets the formatted of this UserName.
        Full name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The formatted of this UserName.
        :rtype: str
        """
        return self._formatted

    @formatted.setter
    def formatted(self, formatted):
        """
        Sets the formatted of this UserName.
        Full name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param formatted: The formatted of this UserName.
        :type: str
        """
        self._formatted = formatted

    @property
    def family_name(self):
        """
        **[Required]** Gets the family_name of this UserName.
        Last name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Last Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The family_name of this UserName.
        :rtype: str
        """
        return self._family_name

    @family_name.setter
    def family_name(self, family_name):
        """
        Sets the family_name of this UserName.
        Last name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Last Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param family_name: The family_name of this UserName.
        :type: str
        """
        self._family_name = family_name

    @property
    def given_name(self):
        """
        Gets the given_name of this UserName.
        First name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: First Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The given_name of this UserName.
        :rtype: str
        """
        return self._given_name

    @given_name.setter
    def given_name(self, given_name):
        """
        Sets the given_name of this UserName.
        First name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: First Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param given_name: The given_name of this UserName.
        :type: str
        """
        self._given_name = given_name

    @property
    def middle_name(self):
        """
        Gets the middle_name of this UserName.
        Middle name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Middle Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The middle_name of this UserName.
        :rtype: str
        """
        return self._middle_name

    @middle_name.setter
    def middle_name(self, middle_name):
        """
        Sets the middle_name of this UserName.
        Middle name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Middle Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param middle_name: The middle_name of this UserName.
        :type: str
        """
        self._middle_name = middle_name

    @property
    def honorific_prefix(self):
        """
        Gets the honorific_prefix of this UserName.
        Prefix

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Honorific Prefix
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The honorific_prefix of this UserName.
        :rtype: str
        """
        return self._honorific_prefix

    @honorific_prefix.setter
    def honorific_prefix(self, honorific_prefix):
        """
        Sets the honorific_prefix of this UserName.
        Prefix

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Honorific Prefix
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param honorific_prefix: The honorific_prefix of this UserName.
        :type: str
        """
        self._honorific_prefix = honorific_prefix

    @property
    def honorific_suffix(self):
        """
        Gets the honorific_suffix of this UserName.
        Suffix

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Honorific Suffix
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The honorific_suffix of this UserName.
        :rtype: str
        """
        return self._honorific_suffix

    @honorific_suffix.setter
    def honorific_suffix(self, honorific_suffix):
        """
        Sets the honorific_suffix of this UserName.
        Suffix

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Honorific Suffix
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param honorific_suffix: The honorific_suffix of this UserName.
        :type: str
        """
        self._honorific_suffix = honorific_suffix

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
