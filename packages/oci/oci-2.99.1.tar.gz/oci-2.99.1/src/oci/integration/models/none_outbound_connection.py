# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .outbound_connection import OutboundConnection
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class NoneOutboundConnection(OutboundConnection):
    """
    Details required for removing Private Endpoint Outbound Connection (ReverseConnection).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new NoneOutboundConnection object with values from keyword arguments. The default value of the :py:attr:`~oci.integration.models.NoneOutboundConnection.outbound_connection_type` attribute
        of this class is ``NONE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param outbound_connection_type:
            The value to assign to the outbound_connection_type property of this NoneOutboundConnection.
            Allowed values for this property are: "PRIVATE_ENDPOINT", "NONE"
        :type outbound_connection_type: str

        """
        self.swagger_types = {
            'outbound_connection_type': 'str'
        }

        self.attribute_map = {
            'outbound_connection_type': 'outboundConnectionType'
        }

        self._outbound_connection_type = None
        self._outbound_connection_type = 'NONE'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
