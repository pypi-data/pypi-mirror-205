# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TunnelSecurityAssociationSummary(object):
    """
    A summary of the IPSec tunnel security association details.
    """

    #: A constant which can be used with the tunnel_sa_status property of a TunnelSecurityAssociationSummary.
    #: This constant has a value of "INITIATING"
    TUNNEL_SA_STATUS_INITIATING = "INITIATING"

    #: A constant which can be used with the tunnel_sa_status property of a TunnelSecurityAssociationSummary.
    #: This constant has a value of "LISTENING"
    TUNNEL_SA_STATUS_LISTENING = "LISTENING"

    #: A constant which can be used with the tunnel_sa_status property of a TunnelSecurityAssociationSummary.
    #: This constant has a value of "UP"
    TUNNEL_SA_STATUS_UP = "UP"

    #: A constant which can be used with the tunnel_sa_status property of a TunnelSecurityAssociationSummary.
    #: This constant has a value of "DOWN"
    TUNNEL_SA_STATUS_DOWN = "DOWN"

    #: A constant which can be used with the tunnel_sa_status property of a TunnelSecurityAssociationSummary.
    #: This constant has a value of "ERROR"
    TUNNEL_SA_STATUS_ERROR = "ERROR"

    #: A constant which can be used with the tunnel_sa_status property of a TunnelSecurityAssociationSummary.
    #: This constant has a value of "UNKNOWN"
    TUNNEL_SA_STATUS_UNKNOWN = "UNKNOWN"

    def __init__(self, **kwargs):
        """
        Initializes a new TunnelSecurityAssociationSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param cpe_subnet:
            The value to assign to the cpe_subnet property of this TunnelSecurityAssociationSummary.
        :type cpe_subnet: str

        :param oracle_subnet:
            The value to assign to the oracle_subnet property of this TunnelSecurityAssociationSummary.
        :type oracle_subnet: str

        :param tunnel_sa_status:
            The value to assign to the tunnel_sa_status property of this TunnelSecurityAssociationSummary.
            Allowed values for this property are: "INITIATING", "LISTENING", "UP", "DOWN", "ERROR", "UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type tunnel_sa_status: str

        :param tunnel_sa_error_info:
            The value to assign to the tunnel_sa_error_info property of this TunnelSecurityAssociationSummary.
        :type tunnel_sa_error_info: str

        :param time:
            The value to assign to the time property of this TunnelSecurityAssociationSummary.
        :type time: str

        """
        self.swagger_types = {
            'cpe_subnet': 'str',
            'oracle_subnet': 'str',
            'tunnel_sa_status': 'str',
            'tunnel_sa_error_info': 'str',
            'time': 'str'
        }

        self.attribute_map = {
            'cpe_subnet': 'cpeSubnet',
            'oracle_subnet': 'oracleSubnet',
            'tunnel_sa_status': 'tunnelSaStatus',
            'tunnel_sa_error_info': 'tunnelSaErrorInfo',
            'time': 'time'
        }

        self._cpe_subnet = None
        self._oracle_subnet = None
        self._tunnel_sa_status = None
        self._tunnel_sa_error_info = None
        self._time = None

    @property
    def cpe_subnet(self):
        """
        Gets the cpe_subnet of this TunnelSecurityAssociationSummary.
        The IP address and mask of the partner subnet used in policy based VPNs or static routes.


        :return: The cpe_subnet of this TunnelSecurityAssociationSummary.
        :rtype: str
        """
        return self._cpe_subnet

    @cpe_subnet.setter
    def cpe_subnet(self, cpe_subnet):
        """
        Sets the cpe_subnet of this TunnelSecurityAssociationSummary.
        The IP address and mask of the partner subnet used in policy based VPNs or static routes.


        :param cpe_subnet: The cpe_subnet of this TunnelSecurityAssociationSummary.
        :type: str
        """
        self._cpe_subnet = cpe_subnet

    @property
    def oracle_subnet(self):
        """
        Gets the oracle_subnet of this TunnelSecurityAssociationSummary.
        The IP address and mask of the local subnet used in policy based VPNs or static routes.


        :return: The oracle_subnet of this TunnelSecurityAssociationSummary.
        :rtype: str
        """
        return self._oracle_subnet

    @oracle_subnet.setter
    def oracle_subnet(self, oracle_subnet):
        """
        Sets the oracle_subnet of this TunnelSecurityAssociationSummary.
        The IP address and mask of the local subnet used in policy based VPNs or static routes.


        :param oracle_subnet: The oracle_subnet of this TunnelSecurityAssociationSummary.
        :type: str
        """
        self._oracle_subnet = oracle_subnet

    @property
    def tunnel_sa_status(self):
        """
        Gets the tunnel_sa_status of this TunnelSecurityAssociationSummary.
        The IPSec tunnel's phase one status.

        Allowed values for this property are: "INITIATING", "LISTENING", "UP", "DOWN", "ERROR", "UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The tunnel_sa_status of this TunnelSecurityAssociationSummary.
        :rtype: str
        """
        return self._tunnel_sa_status

    @tunnel_sa_status.setter
    def tunnel_sa_status(self, tunnel_sa_status):
        """
        Sets the tunnel_sa_status of this TunnelSecurityAssociationSummary.
        The IPSec tunnel's phase one status.


        :param tunnel_sa_status: The tunnel_sa_status of this TunnelSecurityAssociationSummary.
        :type: str
        """
        allowed_values = ["INITIATING", "LISTENING", "UP", "DOWN", "ERROR", "UNKNOWN"]
        if not value_allowed_none_or_none_sentinel(tunnel_sa_status, allowed_values):
            tunnel_sa_status = 'UNKNOWN_ENUM_VALUE'
        self._tunnel_sa_status = tunnel_sa_status

    @property
    def tunnel_sa_error_info(self):
        """
        Gets the tunnel_sa_error_info of this TunnelSecurityAssociationSummary.
        Current state if the IPSec tunnel status is not `UP`, including phase one and phase two details and a possible reason the tunnel is not `UP`.


        :return: The tunnel_sa_error_info of this TunnelSecurityAssociationSummary.
        :rtype: str
        """
        return self._tunnel_sa_error_info

    @tunnel_sa_error_info.setter
    def tunnel_sa_error_info(self, tunnel_sa_error_info):
        """
        Sets the tunnel_sa_error_info of this TunnelSecurityAssociationSummary.
        Current state if the IPSec tunnel status is not `UP`, including phase one and phase two details and a possible reason the tunnel is not `UP`.


        :param tunnel_sa_error_info: The tunnel_sa_error_info of this TunnelSecurityAssociationSummary.
        :type: str
        """
        self._tunnel_sa_error_info = tunnel_sa_error_info

    @property
    def time(self):
        """
        Gets the time of this TunnelSecurityAssociationSummary.
        Time in the current state, in seconds.


        :return: The time of this TunnelSecurityAssociationSummary.
        :rtype: str
        """
        return self._time

    @time.setter
    def time(self, time):
        """
        Sets the time of this TunnelSecurityAssociationSummary.
        Time in the current state, in seconds.


        :param time: The time of this TunnelSecurityAssociationSummary.
        :type: str
        """
        self._time = time

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
