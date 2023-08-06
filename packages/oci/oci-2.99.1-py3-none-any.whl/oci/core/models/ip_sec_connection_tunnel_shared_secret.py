# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class IPSecConnectionTunnelSharedSecret(object):
    """
    The tunnel's shared secret (pre-shared key).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new IPSecConnectionTunnelSharedSecret object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param shared_secret:
            The value to assign to the shared_secret property of this IPSecConnectionTunnelSharedSecret.
        :type shared_secret: str

        """
        self.swagger_types = {
            'shared_secret': 'str'
        }

        self.attribute_map = {
            'shared_secret': 'sharedSecret'
        }

        self._shared_secret = None

    @property
    def shared_secret(self):
        """
        **[Required]** Gets the shared_secret of this IPSecConnectionTunnelSharedSecret.
        The tunnel's shared secret (pre-shared key).


        :return: The shared_secret of this IPSecConnectionTunnelSharedSecret.
        :rtype: str
        """
        return self._shared_secret

    @shared_secret.setter
    def shared_secret(self, shared_secret):
        """
        Sets the shared_secret of this IPSecConnectionTunnelSharedSecret.
        The tunnel's shared secret (pre-shared key).


        :param shared_secret: The shared_secret of this IPSecConnectionTunnelSharedSecret.
        :type: str
        """
        self._shared_secret = shared_secret

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
