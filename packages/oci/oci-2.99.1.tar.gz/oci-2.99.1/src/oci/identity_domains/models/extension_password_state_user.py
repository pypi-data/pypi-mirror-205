# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionPasswordStateUser(object):
    """
    This extension defines attributes used to manage account passwords within a Service Provider. The extension is typically applied to a User resource, but MAY be applied to other resources that use passwords.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionPasswordStateUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param last_successful_set_date:
            The value to assign to the last_successful_set_date property of this ExtensionPasswordStateUser.
        :type last_successful_set_date: str

        :param cant_change:
            The value to assign to the cant_change property of this ExtensionPasswordStateUser.
        :type cant_change: bool

        :param cant_expire:
            The value to assign to the cant_expire property of this ExtensionPasswordStateUser.
        :type cant_expire: bool

        :param must_change:
            The value to assign to the must_change property of this ExtensionPasswordStateUser.
        :type must_change: bool

        :param expired:
            The value to assign to the expired property of this ExtensionPasswordStateUser.
        :type expired: bool

        :param last_successful_validation_date:
            The value to assign to the last_successful_validation_date property of this ExtensionPasswordStateUser.
        :type last_successful_validation_date: str

        :param last_failed_validation_date:
            The value to assign to the last_failed_validation_date property of this ExtensionPasswordStateUser.
        :type last_failed_validation_date: str

        :param applicable_password_policy:
            The value to assign to the applicable_password_policy property of this ExtensionPasswordStateUser.
        :type applicable_password_policy: oci.identity_domains.models.UserExtApplicablePasswordPolicy

        """
        self.swagger_types = {
            'last_successful_set_date': 'str',
            'cant_change': 'bool',
            'cant_expire': 'bool',
            'must_change': 'bool',
            'expired': 'bool',
            'last_successful_validation_date': 'str',
            'last_failed_validation_date': 'str',
            'applicable_password_policy': 'UserExtApplicablePasswordPolicy'
        }

        self.attribute_map = {
            'last_successful_set_date': 'lastSuccessfulSetDate',
            'cant_change': 'cantChange',
            'cant_expire': 'cantExpire',
            'must_change': 'mustChange',
            'expired': 'expired',
            'last_successful_validation_date': 'lastSuccessfulValidationDate',
            'last_failed_validation_date': 'lastFailedValidationDate',
            'applicable_password_policy': 'applicablePasswordPolicy'
        }

        self._last_successful_set_date = None
        self._cant_change = None
        self._cant_expire = None
        self._must_change = None
        self._expired = None
        self._last_successful_validation_date = None
        self._last_failed_validation_date = None
        self._applicable_password_policy = None

    @property
    def last_successful_set_date(self):
        """
        Gets the last_successful_set_date of this ExtensionPasswordStateUser.
        A DateTime that specifies the date and time when the current password was set

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :return: The last_successful_set_date of this ExtensionPasswordStateUser.
        :rtype: str
        """
        return self._last_successful_set_date

    @last_successful_set_date.setter
    def last_successful_set_date(self, last_successful_set_date):
        """
        Sets the last_successful_set_date of this ExtensionPasswordStateUser.
        A DateTime that specifies the date and time when the current password was set

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :param last_successful_set_date: The last_successful_set_date of this ExtensionPasswordStateUser.
        :type: str
        """
        self._last_successful_set_date = last_successful_set_date

    @property
    def cant_change(self):
        """
        Gets the cant_change of this ExtensionPasswordStateUser.
        Indicates that the current password MAY NOT be changed and all other password expiry settings SHALL be ignored

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :return: The cant_change of this ExtensionPasswordStateUser.
        :rtype: bool
        """
        return self._cant_change

    @cant_change.setter
    def cant_change(self, cant_change):
        """
        Sets the cant_change of this ExtensionPasswordStateUser.
        Indicates that the current password MAY NOT be changed and all other password expiry settings SHALL be ignored

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :param cant_change: The cant_change of this ExtensionPasswordStateUser.
        :type: bool
        """
        self._cant_change = cant_change

    @property
    def cant_expire(self):
        """
        Gets the cant_expire of this ExtensionPasswordStateUser.
        Indicates that the password expiry policy will not be applied for the current Resource

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :return: The cant_expire of this ExtensionPasswordStateUser.
        :rtype: bool
        """
        return self._cant_expire

    @cant_expire.setter
    def cant_expire(self, cant_expire):
        """
        Sets the cant_expire of this ExtensionPasswordStateUser.
        Indicates that the password expiry policy will not be applied for the current Resource

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :param cant_expire: The cant_expire of this ExtensionPasswordStateUser.
        :type: bool
        """
        self._cant_expire = cant_expire

    @property
    def must_change(self):
        """
        Gets the must_change of this ExtensionPasswordStateUser.
        Indicates that the subject password value MUST change on next login. If not changed, typically the account is locked. The value may be set indirectly when the subject's current password expires or directly set by an administrator.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :return: The must_change of this ExtensionPasswordStateUser.
        :rtype: bool
        """
        return self._must_change

    @must_change.setter
    def must_change(self, must_change):
        """
        Sets the must_change of this ExtensionPasswordStateUser.
        Indicates that the subject password value MUST change on next login. If not changed, typically the account is locked. The value may be set indirectly when the subject's current password expires or directly set by an administrator.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :param must_change: The must_change of this ExtensionPasswordStateUser.
        :type: bool
        """
        self._must_change = must_change

    @property
    def expired(self):
        """
        Gets the expired of this ExtensionPasswordStateUser.
        Indicates that the password has expired

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :return: The expired of this ExtensionPasswordStateUser.
        :rtype: bool
        """
        return self._expired

    @expired.setter
    def expired(self, expired):
        """
        Sets the expired of this ExtensionPasswordStateUser.
        Indicates that the password has expired

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: boolean
         - uniqueness: none


        :param expired: The expired of this ExtensionPasswordStateUser.
        :type: bool
        """
        self._expired = expired

    @property
    def last_successful_validation_date(self):
        """
        Gets the last_successful_validation_date of this ExtensionPasswordStateUser.
        A DateTime that specifies the date and time when last successful password validation was set

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :return: The last_successful_validation_date of this ExtensionPasswordStateUser.
        :rtype: str
        """
        return self._last_successful_validation_date

    @last_successful_validation_date.setter
    def last_successful_validation_date(self, last_successful_validation_date):
        """
        Sets the last_successful_validation_date of this ExtensionPasswordStateUser.
        A DateTime that specifies the date and time when last successful password validation was set

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :param last_successful_validation_date: The last_successful_validation_date of this ExtensionPasswordStateUser.
        :type: str
        """
        self._last_successful_validation_date = last_successful_validation_date

    @property
    def last_failed_validation_date(self):
        """
        Gets the last_failed_validation_date of this ExtensionPasswordStateUser.
        A DateTime that specifies the date and time when last failed password validation was set

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :return: The last_failed_validation_date of this ExtensionPasswordStateUser.
        :rtype: str
        """
        return self._last_failed_validation_date

    @last_failed_validation_date.setter
    def last_failed_validation_date(self, last_failed_validation_date):
        """
        Sets the last_failed_validation_date of this ExtensionPasswordStateUser.
        A DateTime that specifies the date and time when last failed password validation was set

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :param last_failed_validation_date: The last_failed_validation_date of this ExtensionPasswordStateUser.
        :type: str
        """
        self._last_failed_validation_date = last_failed_validation_date

    @property
    def applicable_password_policy(self):
        """
        Gets the applicable_password_policy of this ExtensionPasswordStateUser.

        :return: The applicable_password_policy of this ExtensionPasswordStateUser.
        :rtype: oci.identity_domains.models.UserExtApplicablePasswordPolicy
        """
        return self._applicable_password_policy

    @applicable_password_policy.setter
    def applicable_password_policy(self, applicable_password_policy):
        """
        Sets the applicable_password_policy of this ExtensionPasswordStateUser.

        :param applicable_password_policy: The applicable_password_policy of this ExtensionPasswordStateUser.
        :type: oci.identity_domains.models.UserExtApplicablePasswordPolicy
        """
        self._applicable_password_policy = applicable_password_policy

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
