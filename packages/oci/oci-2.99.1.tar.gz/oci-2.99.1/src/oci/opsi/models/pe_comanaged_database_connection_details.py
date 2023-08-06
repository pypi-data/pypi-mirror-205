# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PeComanagedDatabaseConnectionDetails(object):
    """
    Connection details of the private endpoints.
    """

    #: A constant which can be used with the protocol property of a PeComanagedDatabaseConnectionDetails.
    #: This constant has a value of "TCP"
    PROTOCOL_TCP = "TCP"

    #: A constant which can be used with the protocol property of a PeComanagedDatabaseConnectionDetails.
    #: This constant has a value of "TCPS"
    PROTOCOL_TCPS = "TCPS"

    def __init__(self, **kwargs):
        """
        Initializes a new PeComanagedDatabaseConnectionDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param hosts:
            The value to assign to the hosts property of this PeComanagedDatabaseConnectionDetails.
        :type hosts: list[oci.opsi.models.PeComanagedDatabaseHostDetails]

        :param protocol:
            The value to assign to the protocol property of this PeComanagedDatabaseConnectionDetails.
            Allowed values for this property are: "TCP", "TCPS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type protocol: str

        :param service_name:
            The value to assign to the service_name property of this PeComanagedDatabaseConnectionDetails.
        :type service_name: str

        """
        self.swagger_types = {
            'hosts': 'list[PeComanagedDatabaseHostDetails]',
            'protocol': 'str',
            'service_name': 'str'
        }

        self.attribute_map = {
            'hosts': 'hosts',
            'protocol': 'protocol',
            'service_name': 'serviceName'
        }

        self._hosts = None
        self._protocol = None
        self._service_name = None

    @property
    def hosts(self):
        """
        **[Required]** Gets the hosts of this PeComanagedDatabaseConnectionDetails.
        List of hosts and port for private endpoint accessed database resource.


        :return: The hosts of this PeComanagedDatabaseConnectionDetails.
        :rtype: list[oci.opsi.models.PeComanagedDatabaseHostDetails]
        """
        return self._hosts

    @hosts.setter
    def hosts(self, hosts):
        """
        Sets the hosts of this PeComanagedDatabaseConnectionDetails.
        List of hosts and port for private endpoint accessed database resource.


        :param hosts: The hosts of this PeComanagedDatabaseConnectionDetails.
        :type: list[oci.opsi.models.PeComanagedDatabaseHostDetails]
        """
        self._hosts = hosts

    @property
    def protocol(self):
        """
        Gets the protocol of this PeComanagedDatabaseConnectionDetails.
        Protocol used for connection requests for private endpoint accssed database resource.

        Allowed values for this property are: "TCP", "TCPS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The protocol of this PeComanagedDatabaseConnectionDetails.
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        """
        Sets the protocol of this PeComanagedDatabaseConnectionDetails.
        Protocol used for connection requests for private endpoint accssed database resource.


        :param protocol: The protocol of this PeComanagedDatabaseConnectionDetails.
        :type: str
        """
        allowed_values = ["TCP", "TCPS"]
        if not value_allowed_none_or_none_sentinel(protocol, allowed_values):
            protocol = 'UNKNOWN_ENUM_VALUE'
        self._protocol = protocol

    @property
    def service_name(self):
        """
        Gets the service_name of this PeComanagedDatabaseConnectionDetails.
        Database service name used for connection requests.


        :return: The service_name of this PeComanagedDatabaseConnectionDetails.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Sets the service_name of this PeComanagedDatabaseConnectionDetails.
        Database service name used for connection requests.


        :param service_name: The service_name of this PeComanagedDatabaseConnectionDetails.
        :type: str
        """
        self._service_name = service_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
