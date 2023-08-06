# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AdminUserSummary(object):
    """
    IDM admin credentials without password
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AdminUserSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param username:
            The value to assign to the username property of this AdminUserSummary.
        :type username: str

        :param email_address:
            The value to assign to the email_address property of this AdminUserSummary.
        :type email_address: str

        :param first_name:
            The value to assign to the first_name property of this AdminUserSummary.
        :type first_name: str

        :param last_name:
            The value to assign to the last_name property of this AdminUserSummary.
        :type last_name: str

        """
        self.swagger_types = {
            'username': 'str',
            'email_address': 'str',
            'first_name': 'str',
            'last_name': 'str'
        }

        self.attribute_map = {
            'username': 'username',
            'email_address': 'emailAddress',
            'first_name': 'firstName',
            'last_name': 'lastName'
        }

        self._username = None
        self._email_address = None
        self._first_name = None
        self._last_name = None

    @property
    def username(self):
        """
        **[Required]** Gets the username of this AdminUserSummary.
        Admin username


        :return: The username of this AdminUserSummary.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this AdminUserSummary.
        Admin username


        :param username: The username of this AdminUserSummary.
        :type: str
        """
        self._username = username

    @property
    def email_address(self):
        """
        **[Required]** Gets the email_address of this AdminUserSummary.
        Admin users email address


        :return: The email_address of this AdminUserSummary.
        :rtype: str
        """
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        """
        Sets the email_address of this AdminUserSummary.
        Admin users email address


        :param email_address: The email_address of this AdminUserSummary.
        :type: str
        """
        self._email_address = email_address

    @property
    def first_name(self):
        """
        **[Required]** Gets the first_name of this AdminUserSummary.
        Admin users first name


        :return: The first_name of this AdminUserSummary.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """
        Sets the first_name of this AdminUserSummary.
        Admin users first name


        :param first_name: The first_name of this AdminUserSummary.
        :type: str
        """
        self._first_name = first_name

    @property
    def last_name(self):
        """
        **[Required]** Gets the last_name of this AdminUserSummary.
        Admin users last name


        :return: The last_name of this AdminUserSummary.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """
        Sets the last_name of this AdminUserSummary.
        Admin users last name


        :param last_name: The last_name of this AdminUserSummary.
        :type: str
        """
        self._last_name = last_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
