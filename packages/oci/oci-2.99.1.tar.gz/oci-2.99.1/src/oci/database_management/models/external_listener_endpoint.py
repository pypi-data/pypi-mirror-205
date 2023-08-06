# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalListenerEndpoint(object):
    """
    The protocol address that an external listener is configured to listen on.
    """

    #: A constant which can be used with the protocol property of a ExternalListenerEndpoint.
    #: This constant has a value of "IPC"
    PROTOCOL_IPC = "IPC"

    #: A constant which can be used with the protocol property of a ExternalListenerEndpoint.
    #: This constant has a value of "TCP"
    PROTOCOL_TCP = "TCP"

    #: A constant which can be used with the protocol property of a ExternalListenerEndpoint.
    #: This constant has a value of "TCPS"
    PROTOCOL_TCPS = "TCPS"

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalListenerEndpoint object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.database_management.models.ExternalListenerTcpEndpoint`
        * :class:`~oci.database_management.models.ExternalListenerTcpsEndpoint`
        * :class:`~oci.database_management.models.ExternalListenerIpcEndpoint`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param protocol:
            The value to assign to the protocol property of this ExternalListenerEndpoint.
            Allowed values for this property are: "IPC", "TCP", "TCPS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type protocol: str

        :param services:
            The value to assign to the services property of this ExternalListenerEndpoint.
        :type services: list[str]

        """
        self.swagger_types = {
            'protocol': 'str',
            'services': 'list[str]'
        }

        self.attribute_map = {
            'protocol': 'protocol',
            'services': 'services'
        }

        self._protocol = None
        self._services = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['protocol']

        if type == 'TCP':
            return 'ExternalListenerTcpEndpoint'

        if type == 'TCPS':
            return 'ExternalListenerTcpsEndpoint'

        if type == 'IPC':
            return 'ExternalListenerIpcEndpoint'
        else:
            return 'ExternalListenerEndpoint'

    @property
    def protocol(self):
        """
        **[Required]** Gets the protocol of this ExternalListenerEndpoint.
        The listener protocol.

        Allowed values for this property are: "IPC", "TCP", "TCPS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The protocol of this ExternalListenerEndpoint.
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        """
        Sets the protocol of this ExternalListenerEndpoint.
        The listener protocol.


        :param protocol: The protocol of this ExternalListenerEndpoint.
        :type: str
        """
        allowed_values = ["IPC", "TCP", "TCPS"]
        if not value_allowed_none_or_none_sentinel(protocol, allowed_values):
            protocol = 'UNKNOWN_ENUM_VALUE'
        self._protocol = protocol

    @property
    def services(self):
        """
        Gets the services of this ExternalListenerEndpoint.
        The list of services registered with the listener.


        :return: The services of this ExternalListenerEndpoint.
        :rtype: list[str]
        """
        return self._services

    @services.setter
    def services(self, services):
        """
        Sets the services of this ExternalListenerEndpoint.
        The list of services registered with the listener.


        :param services: The services of this ExternalListenerEndpoint.
        :type: list[str]
        """
        self._services = services

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
