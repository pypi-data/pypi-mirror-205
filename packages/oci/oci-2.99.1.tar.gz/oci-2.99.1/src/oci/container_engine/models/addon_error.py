# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddonError(object):
    """
    The error info of the addon.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddonError object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param code:
            The value to assign to the code property of this AddonError.
        :type code: str

        :param message:
            The value to assign to the message property of this AddonError.
        :type message: str

        :param status:
            The value to assign to the status property of this AddonError.
        :type status: str

        """
        self.swagger_types = {
            'code': 'str',
            'message': 'str',
            'status': 'str'
        }

        self.attribute_map = {
            'code': 'code',
            'message': 'message',
            'status': 'status'
        }

        self._code = None
        self._message = None
        self._status = None

    @property
    def code(self):
        """
        Gets the code of this AddonError.
        A short error code that defines the upstream error, meant for programmatic parsing. See `API Errors`__.

        __ https://docs.cloud.oracle.com/Content/API/References/apierrors.htm


        :return: The code of this AddonError.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this AddonError.
        A short error code that defines the upstream error, meant for programmatic parsing. See `API Errors`__.

        __ https://docs.cloud.oracle.com/Content/API/References/apierrors.htm


        :param code: The code of this AddonError.
        :type: str
        """
        self._code = code

    @property
    def message(self):
        """
        Gets the message of this AddonError.
        A human-readable error string of the upstream error.


        :return: The message of this AddonError.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this AddonError.
        A human-readable error string of the upstream error.


        :param message: The message of this AddonError.
        :type: str
        """
        self._message = message

    @property
    def status(self):
        """
        Gets the status of this AddonError.
        The status of the HTTP response encountered in the upstream error.


        :return: The status of this AddonError.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this AddonError.
        The status of the HTTP response encountered in the upstream error.


        :param status: The status of this AddonError.
        :type: str
        """
        self._status = status

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
