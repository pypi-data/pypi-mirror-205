# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class GroupMembers(object):
    """
    Group members - when requesting members attribute, a max of 10,000 members will be returned in a single request. It is recommended to use startIndex and count to return members in pages instead of in a single response, eg : #attributes=members[startIndex=1%26count=10]
    """

    #: A constant which can be used with the type property of a GroupMembers.
    #: This constant has a value of "User"
    TYPE_USER = "User"

    def __init__(self, **kwargs):
        """
        Initializes a new GroupMembers object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this GroupMembers.
        :type value: str

        :param date_added:
            The value to assign to the date_added property of this GroupMembers.
        :type date_added: str

        :param ocid:
            The value to assign to the ocid property of this GroupMembers.
        :type ocid: str

        :param membership_ocid:
            The value to assign to the membership_ocid property of this GroupMembers.
        :type membership_ocid: str

        :param ref:
            The value to assign to the ref property of this GroupMembers.
        :type ref: str

        :param display:
            The value to assign to the display property of this GroupMembers.
        :type display: str

        :param type:
            The value to assign to the type property of this GroupMembers.
            Allowed values for this property are: "User", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param name:
            The value to assign to the name property of this GroupMembers.
        :type name: str

        """
        self.swagger_types = {
            'value': 'str',
            'date_added': 'str',
            'ocid': 'str',
            'membership_ocid': 'str',
            'ref': 'str',
            'display': 'str',
            'type': 'str',
            'name': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'date_added': 'dateAdded',
            'ocid': 'ocid',
            'membership_ocid': 'membershipOcid',
            'ref': '$ref',
            'display': 'display',
            'type': 'type',
            'name': 'name'
        }

        self._value = None
        self._date_added = None
        self._ocid = None
        self._membership_ocid = None
        self._ref = None
        self._display = None
        self._type = None
        self._name = None

    @property
    def value(self):
        """
        **[Required]** Gets the value of this GroupMembers.
        ID of the member of this Group

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :return: The value of this GroupMembers.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this GroupMembers.
        ID of the member of this Group

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :param value: The value of this GroupMembers.
        :type: str
        """
        self._value = value

    @property
    def date_added(self):
        """
        Gets the date_added of this GroupMembers.
        The DateTime the member was added to the Group.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readOnly
         - returned: default
         - type: dateTime
         - uniqueness: none


        :return: The date_added of this GroupMembers.
        :rtype: str
        """
        return self._date_added

    @date_added.setter
    def date_added(self, date_added):
        """
        Sets the date_added of this GroupMembers.
        The DateTime the member was added to the Group.

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readOnly
         - returned: default
         - type: dateTime
         - uniqueness: none


        :param date_added: The date_added of this GroupMembers.
        :type: str
        """
        self._date_added = date_added

    @property
    def ocid(self):
        """
        Gets the ocid of this GroupMembers.
        OCID of the member of this Group

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: always
         - type: string
         - uniqueness: none


        :return: The ocid of this GroupMembers.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this GroupMembers.
        OCID of the member of this Group

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: always
         - type: string
         - uniqueness: none


        :param ocid: The ocid of this GroupMembers.
        :type: str
        """
        self._ocid = ocid

    @property
    def membership_ocid(self):
        """
        Gets the membership_ocid of this GroupMembers.
        Membership Ocid

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The membership_ocid of this GroupMembers.
        :rtype: str
        """
        return self._membership_ocid

    @membership_ocid.setter
    def membership_ocid(self, membership_ocid):
        """
        Sets the membership_ocid of this GroupMembers.
        Membership Ocid

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param membership_ocid: The membership_ocid of this GroupMembers.
        :type: str
        """
        self._membership_ocid = membership_ocid

    @property
    def ref(self):
        """
        Gets the ref of this GroupMembers.
        The URI that corresponds to the member Resource of this Group

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this GroupMembers.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this GroupMembers.
        The URI that corresponds to the member Resource of this Group

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this GroupMembers.
        :type: str
        """
        self._ref = ref

    @property
    def display(self):
        """
        Gets the display of this GroupMembers.
        Member display name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display of this GroupMembers.
        :rtype: str
        """
        return self._display

    @display.setter
    def display(self, display):
        """
        Sets the display of this GroupMembers.
        Member display name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display: The display of this GroupMembers.
        :type: str
        """
        self._display = display

    @property
    def type(self):
        """
        **[Required]** Gets the type of this GroupMembers.
        Indicates the type of resource--for example, User or Group

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - idcsDefaultValue: User
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "User", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this GroupMembers.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this GroupMembers.
        Indicates the type of resource--for example, User or Group

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - idcsDefaultValue: User
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param type: The type of this GroupMembers.
        :type: str
        """
        allowed_values = ["User"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def name(self):
        """
        Gets the name of this GroupMembers.
        Member name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The name of this GroupMembers.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this GroupMembers.
        Member name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param name: The name of this GroupMembers.
        :type: str
        """
        self._name = name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
