# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class User(object):
    """
    User model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new User object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this User.
        :type id: str

        :param name:
            The value to assign to the name property of this User.
        :type name: str

        :param is_otp:
            The value to assign to the is_otp property of this User.
        :type is_otp: bool

        :param is_mfa_activated:
            The value to assign to the is_mfa_activated property of this User.
        :type is_mfa_activated: bool

        :param is_mfa_verified:
            The value to assign to the is_mfa_verified property of this User.
        :type is_mfa_verified: bool

        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'is_otp': 'bool',
            'is_mfa_activated': 'bool',
            'is_mfa_verified': 'bool'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'is_otp': 'isOTP',
            'is_mfa_activated': 'isMfaActivated',
            'is_mfa_verified': 'isMfaVerified'
        }

        self._id = None
        self._name = None
        self._is_otp = None
        self._is_mfa_activated = None
        self._is_mfa_verified = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this User.
        The user's Oracle ID (OCID).


        :return: The id of this User.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this User.
        The user's Oracle ID (OCID).


        :param id: The id of this User.
        :type: str
        """
        self._id = id

    @property
    def name(self):
        """
        **[Required]** Gets the name of this User.
        The name of the user.


        :return: The name of this User.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this User.
        The name of the user.


        :param name: The name of this User.
        :type: str
        """
        self._name = name

    @property
    def is_otp(self):
        """
        **[Required]** Gets the is_otp of this User.
        If the provided password is a one-time password.


        :return: The is_otp of this User.
        :rtype: bool
        """
        return self._is_otp

    @is_otp.setter
    def is_otp(self, is_otp):
        """
        Sets the is_otp of this User.
        If the provided password is a one-time password.


        :param is_otp: The is_otp of this User.
        :type: bool
        """
        self._is_otp = is_otp

    @property
    def is_mfa_activated(self):
        """
        **[Required]** Gets the is_mfa_activated of this User.
        If mfa is activated.


        :return: The is_mfa_activated of this User.
        :rtype: bool
        """
        return self._is_mfa_activated

    @is_mfa_activated.setter
    def is_mfa_activated(self, is_mfa_activated):
        """
        Sets the is_mfa_activated of this User.
        If mfa is activated.


        :param is_mfa_activated: The is_mfa_activated of this User.
        :type: bool
        """
        self._is_mfa_activated = is_mfa_activated

    @property
    def is_mfa_verified(self):
        """
        **[Required]** Gets the is_mfa_verified of this User.
        If the user has been mfa verified.


        :return: The is_mfa_verified of this User.
        :rtype: bool
        """
        return self._is_mfa_verified

    @is_mfa_verified.setter
    def is_mfa_verified(self, is_mfa_verified):
        """
        Sets the is_mfa_verified of this User.
        If the user has been mfa verified.


        :param is_mfa_verified: The is_mfa_verified of this User.
        :type: bool
        """
        self._is_mfa_verified = is_mfa_verified

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
