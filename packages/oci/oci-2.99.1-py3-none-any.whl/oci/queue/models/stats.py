# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Stats(object):
    """
    The stats for a queue or a dead letter queue.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new Stats object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param visible_messages:
            The value to assign to the visible_messages property of this Stats.
        :type visible_messages: int

        :param in_flight_messages:
            The value to assign to the in_flight_messages property of this Stats.
        :type in_flight_messages: int

        :param size_in_bytes:
            The value to assign to the size_in_bytes property of this Stats.
        :type size_in_bytes: int

        """
        self.swagger_types = {
            'visible_messages': 'int',
            'in_flight_messages': 'int',
            'size_in_bytes': 'int'
        }

        self.attribute_map = {
            'visible_messages': 'visibleMessages',
            'in_flight_messages': 'inFlightMessages',
            'size_in_bytes': 'sizeInBytes'
        }

        self._visible_messages = None
        self._in_flight_messages = None
        self._size_in_bytes = None

    @property
    def visible_messages(self):
        """
        **[Required]** Gets the visible_messages of this Stats.
        The approximate number of visible messages (available for delivery) currently in the queue.


        :return: The visible_messages of this Stats.
        :rtype: int
        """
        return self._visible_messages

    @visible_messages.setter
    def visible_messages(self, visible_messages):
        """
        Sets the visible_messages of this Stats.
        The approximate number of visible messages (available for delivery) currently in the queue.


        :param visible_messages: The visible_messages of this Stats.
        :type: int
        """
        self._visible_messages = visible_messages

    @property
    def in_flight_messages(self):
        """
        **[Required]** Gets the in_flight_messages of this Stats.
        The approximate number of messages delivered to a consumer but not yet deleted and so unavailable for re-delivery.


        :return: The in_flight_messages of this Stats.
        :rtype: int
        """
        return self._in_flight_messages

    @in_flight_messages.setter
    def in_flight_messages(self, in_flight_messages):
        """
        Sets the in_flight_messages of this Stats.
        The approximate number of messages delivered to a consumer but not yet deleted and so unavailable for re-delivery.


        :param in_flight_messages: The in_flight_messages of this Stats.
        :type: int
        """
        self._in_flight_messages = in_flight_messages

    @property
    def size_in_bytes(self):
        """
        **[Required]** Gets the size_in_bytes of this Stats.
        The approximate size of the queue in bytes. Sum of the size of visible of in-flight messages.


        :return: The size_in_bytes of this Stats.
        :rtype: int
        """
        return self._size_in_bytes

    @size_in_bytes.setter
    def size_in_bytes(self, size_in_bytes):
        """
        Sets the size_in_bytes of this Stats.
        The approximate size of the queue in bytes. Sum of the size of visible of in-flight messages.


        :param size_in_bytes: The size_in_bytes of this Stats.
        :type: int
        """
        self._size_in_bytes = size_in_bytes

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
