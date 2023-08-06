# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateMessageDetails(object):
    """
    Updates the visibility of a message
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateMessageDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param visibility_in_seconds:
            The value to assign to the visibility_in_seconds property of this UpdateMessageDetails.
        :type visibility_in_seconds: int

        """
        self.swagger_types = {
            'visibility_in_seconds': 'int'
        }

        self.attribute_map = {
            'visibility_in_seconds': 'visibilityInSeconds'
        }

        self._visibility_in_seconds = None

    @property
    def visibility_in_seconds(self):
        """
        **[Required]** Gets the visibility_in_seconds of this UpdateMessageDetails.
        The new visibility of the message relative to the current time (as-per the clock of the server receiving the request).


        :return: The visibility_in_seconds of this UpdateMessageDetails.
        :rtype: int
        """
        return self._visibility_in_seconds

    @visibility_in_seconds.setter
    def visibility_in_seconds(self, visibility_in_seconds):
        """
        Sets the visibility_in_seconds of this UpdateMessageDetails.
        The new visibility of the message relative to the current time (as-per the clock of the server receiving the request).


        :param visibility_in_seconds: The visibility_in_seconds of this UpdateMessageDetails.
        :type: int
        """
        self._visibility_in_seconds = visibility_in_seconds

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
