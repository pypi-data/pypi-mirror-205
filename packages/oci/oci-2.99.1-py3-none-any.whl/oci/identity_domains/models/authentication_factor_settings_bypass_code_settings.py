# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AuthenticationFactorSettingsBypassCodeSettings(object):
    """
    Settings related to the bypass code, such as bypass code length, bypass code expiry, max active bypass codes, and so on

    **SCIM++ Properties:**
    - idcsSearchable: false
    - multiValued: false
    - mutability: readWrite
    - required: true
    - returned: default
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AuthenticationFactorSettingsBypassCodeSettings object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param self_service_generation_enabled:
            The value to assign to the self_service_generation_enabled property of this AuthenticationFactorSettingsBypassCodeSettings.
        :type self_service_generation_enabled: bool

        :param help_desk_generation_enabled:
            The value to assign to the help_desk_generation_enabled property of this AuthenticationFactorSettingsBypassCodeSettings.
        :type help_desk_generation_enabled: bool

        :param length:
            The value to assign to the length property of this AuthenticationFactorSettingsBypassCodeSettings.
        :type length: int

        :param max_active:
            The value to assign to the max_active property of this AuthenticationFactorSettingsBypassCodeSettings.
        :type max_active: int

        :param help_desk_code_expiry_in_mins:
            The value to assign to the help_desk_code_expiry_in_mins property of this AuthenticationFactorSettingsBypassCodeSettings.
        :type help_desk_code_expiry_in_mins: int

        :param help_desk_max_usage:
            The value to assign to the help_desk_max_usage property of this AuthenticationFactorSettingsBypassCodeSettings.
        :type help_desk_max_usage: int

        """
        self.swagger_types = {
            'self_service_generation_enabled': 'bool',
            'help_desk_generation_enabled': 'bool',
            'length': 'int',
            'max_active': 'int',
            'help_desk_code_expiry_in_mins': 'int',
            'help_desk_max_usage': 'int'
        }

        self.attribute_map = {
            'self_service_generation_enabled': 'selfServiceGenerationEnabled',
            'help_desk_generation_enabled': 'helpDeskGenerationEnabled',
            'length': 'length',
            'max_active': 'maxActive',
            'help_desk_code_expiry_in_mins': 'helpDeskCodeExpiryInMins',
            'help_desk_max_usage': 'helpDeskMaxUsage'
        }

        self._self_service_generation_enabled = None
        self._help_desk_generation_enabled = None
        self._length = None
        self._max_active = None
        self._help_desk_code_expiry_in_mins = None
        self._help_desk_max_usage = None

    @property
    def self_service_generation_enabled(self):
        """
        **[Required]** Gets the self_service_generation_enabled of this AuthenticationFactorSettingsBypassCodeSettings.
        If true, indicates that self-service bypass code generation is enabled

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The self_service_generation_enabled of this AuthenticationFactorSettingsBypassCodeSettings.
        :rtype: bool
        """
        return self._self_service_generation_enabled

    @self_service_generation_enabled.setter
    def self_service_generation_enabled(self, self_service_generation_enabled):
        """
        Sets the self_service_generation_enabled of this AuthenticationFactorSettingsBypassCodeSettings.
        If true, indicates that self-service bypass code generation is enabled

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :param self_service_generation_enabled: The self_service_generation_enabled of this AuthenticationFactorSettingsBypassCodeSettings.
        :type: bool
        """
        self._self_service_generation_enabled = self_service_generation_enabled

    @property
    def help_desk_generation_enabled(self):
        """
        **[Required]** Gets the help_desk_generation_enabled of this AuthenticationFactorSettingsBypassCodeSettings.
        If true, indicates that help desk bypass code generation is enabled

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The help_desk_generation_enabled of this AuthenticationFactorSettingsBypassCodeSettings.
        :rtype: bool
        """
        return self._help_desk_generation_enabled

    @help_desk_generation_enabled.setter
    def help_desk_generation_enabled(self, help_desk_generation_enabled):
        """
        Sets the help_desk_generation_enabled of this AuthenticationFactorSettingsBypassCodeSettings.
        If true, indicates that help desk bypass code generation is enabled

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :param help_desk_generation_enabled: The help_desk_generation_enabled of this AuthenticationFactorSettingsBypassCodeSettings.
        :type: bool
        """
        self._help_desk_generation_enabled = help_desk_generation_enabled

    @property
    def length(self):
        """
        **[Required]** Gets the length of this AuthenticationFactorSettingsBypassCodeSettings.
        Exact length of the bypass code to be generated

        **SCIM++ Properties:**
         - idcsMaxValue: 20
         - idcsMinValue: 8
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The length of this AuthenticationFactorSettingsBypassCodeSettings.
        :rtype: int
        """
        return self._length

    @length.setter
    def length(self, length):
        """
        Sets the length of this AuthenticationFactorSettingsBypassCodeSettings.
        Exact length of the bypass code to be generated

        **SCIM++ Properties:**
         - idcsMaxValue: 20
         - idcsMinValue: 8
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: integer
         - uniqueness: none


        :param length: The length of this AuthenticationFactorSettingsBypassCodeSettings.
        :type: int
        """
        self._length = length

    @property
    def max_active(self):
        """
        **[Required]** Gets the max_active of this AuthenticationFactorSettingsBypassCodeSettings.
        The maximum number of bypass codes that can be issued to any user

        **SCIM++ Properties:**
         - idcsMaxValue: 6
         - idcsMinValue: 1
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The max_active of this AuthenticationFactorSettingsBypassCodeSettings.
        :rtype: int
        """
        return self._max_active

    @max_active.setter
    def max_active(self, max_active):
        """
        Sets the max_active of this AuthenticationFactorSettingsBypassCodeSettings.
        The maximum number of bypass codes that can be issued to any user

        **SCIM++ Properties:**
         - idcsMaxValue: 6
         - idcsMinValue: 1
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: integer
         - uniqueness: none


        :param max_active: The max_active of this AuthenticationFactorSettingsBypassCodeSettings.
        :type: int
        """
        self._max_active = max_active

    @property
    def help_desk_code_expiry_in_mins(self):
        """
        **[Required]** Gets the help_desk_code_expiry_in_mins of this AuthenticationFactorSettingsBypassCodeSettings.
        Expiry (in minutes) of any bypass code that is generated by the help desk

        **SCIM++ Properties:**
         - idcsMaxValue: 9999999
         - idcsMinValue: 1
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The help_desk_code_expiry_in_mins of this AuthenticationFactorSettingsBypassCodeSettings.
        :rtype: int
        """
        return self._help_desk_code_expiry_in_mins

    @help_desk_code_expiry_in_mins.setter
    def help_desk_code_expiry_in_mins(self, help_desk_code_expiry_in_mins):
        """
        Sets the help_desk_code_expiry_in_mins of this AuthenticationFactorSettingsBypassCodeSettings.
        Expiry (in minutes) of any bypass code that is generated by the help desk

        **SCIM++ Properties:**
         - idcsMaxValue: 9999999
         - idcsMinValue: 1
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: integer
         - uniqueness: none


        :param help_desk_code_expiry_in_mins: The help_desk_code_expiry_in_mins of this AuthenticationFactorSettingsBypassCodeSettings.
        :type: int
        """
        self._help_desk_code_expiry_in_mins = help_desk_code_expiry_in_mins

    @property
    def help_desk_max_usage(self):
        """
        **[Required]** Gets the help_desk_max_usage of this AuthenticationFactorSettingsBypassCodeSettings.
        The maximum number of times that any bypass code that is generated by the help desk can be used

        **SCIM++ Properties:**
         - idcsMaxValue: 999
         - idcsMinValue: 1
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The help_desk_max_usage of this AuthenticationFactorSettingsBypassCodeSettings.
        :rtype: int
        """
        return self._help_desk_max_usage

    @help_desk_max_usage.setter
    def help_desk_max_usage(self, help_desk_max_usage):
        """
        Sets the help_desk_max_usage of this AuthenticationFactorSettingsBypassCodeSettings.
        The maximum number of times that any bypass code that is generated by the help desk can be used

        **SCIM++ Properties:**
         - idcsMaxValue: 999
         - idcsMinValue: 1
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: integer
         - uniqueness: none


        :param help_desk_max_usage: The help_desk_max_usage of this AuthenticationFactorSettingsBypassCodeSettings.
        :type: int
        """
        self._help_desk_max_usage = help_desk_max_usage

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
