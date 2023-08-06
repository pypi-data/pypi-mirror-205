# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionMessagesError(object):
    """
    Extension schema for error messages providing more details with the exception status.
    Returns messageId corresponding to the detailed error message and optionally additional data related to the error condition - for example reason for authentication failure such as user is disabled or locked.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionMessagesError object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param message_id:
            The value to assign to the message_id property of this ExtensionMessagesError.
        :type message_id: str

        :param additional_data:
            The value to assign to the additional_data property of this ExtensionMessagesError.
        :type additional_data: object

        """
        self.swagger_types = {
            'message_id': 'str',
            'additional_data': 'object'
        }

        self.attribute_map = {
            'message_id': 'messageId',
            'additional_data': 'additionalData'
        }

        self._message_id = None
        self._additional_data = None

    @property
    def message_id(self):
        """
        Gets the message_id of this ExtensionMessagesError.
        Internal error keyword pointing to the exception status message. REQUIRED.


        :return: The message_id of this ExtensionMessagesError.
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """
        Sets the message_id of this ExtensionMessagesError.
        Internal error keyword pointing to the exception status message. REQUIRED.


        :param message_id: The message_id of this ExtensionMessagesError.
        :type: str
        """
        self._message_id = message_id

    @property
    def additional_data(self):
        """
        Gets the additional_data of this ExtensionMessagesError.
        Contains Map based additional data for the exception message (as key-value pair). All keys and values are in string format.


        :return: The additional_data of this ExtensionMessagesError.
        :rtype: object
        """
        return self._additional_data

    @additional_data.setter
    def additional_data(self, additional_data):
        """
        Sets the additional_data of this ExtensionMessagesError.
        Contains Map based additional data for the exception message (as key-value pair). All keys and values are in string format.


        :param additional_data: The additional_data of this ExtensionMessagesError.
        :type: object
        """
        self._additional_data = additional_data

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
